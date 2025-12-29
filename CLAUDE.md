# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a GitHub Action that finds matching commits between two git refs, with special handling for expanding merge and squash PRs. It filters commits by GitHub PR labels (default: "hotfix") and returns space-separated commit SHAs.

## Core Architecture

The codebase consists of four main modules that work together:

1. **git_matching_commits.py** - Main entry point
   - `get_matching_commits()` orchestrates the workflow
   - Iterates through commits in a range (start_ref..end_ref)
   - Fetches PR data for each commit via GitHub API
   - Filters commits by required labels (defaults to ["hotfix"])
   - Delegates to expansion functions based on parent count
   - Deduplicates results while preserving order

2. **git_expansion.py** - Commit expansion logic
   - `expand_merge_commit()` - Handles 2-parent merge commits by extracting all commits from the PR branch
   - `expand_squash_commit()` - Handles single-parent squash merges by returning the squash commit itself
   - Key distinction: merge commits are expanded to their constituent commits, squash commits are returned as-is

3. **github_pr.py** - GitHub API integration
   - `get_pr_for_commit()` - Uses PyGithub to find PR associated with a commit SHA
   - `pr_has_label()` - Checks if a PR has a specific label
   - Exits with error if GitHub token is missing/empty

4. **action.yml** - GitHub Action composite wrapper
   - Sets up Python 3.11 and installs dependencies
   - Calls `get_matching_commits()` with inputs
   - Writes outputs to GITHUB_OUTPUT: commits (space-separated SHAs), count, first_commit, and last_commit

## Development Commands

### Linting and Formatting
```bash
# Run all linters (via Trunk)
trunk check

# Format Python code
trunk fmt

# Individual linters (via Trunk)
black .
isort .
ruff check .
bandit -r .
```

### Testing
```bash
# Run tests with pytest
pytest

# Run specific test file
pytest test_merge_hotfix.py
pytest test_squash_hotfix.py

# Tests use monkeypatch to mock GitHub PR API calls
# Test fixtures are in test/fixtures/ directory
```

### Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Required packages:
# - GitPython (git operations)
# - PyGithub (GitHub API)
# - github_action_utils (GitHub Actions utilities)
# - Repo, requests
```

## Important Implementation Details

### PR-Only Filtering (CRITICAL)
- The action **ONLY** returns commits associated with Pull Requests
- Direct commits to branches (no PR) are **never** returned, regardless of commit message
- Filtering is based on GitHub PR labels via the API, not commit message patterns
- If `get_pr_for_commit()` returns None, the commit is skipped entirely (git_matching_commits.py:27-29)

### Commit Matching Logic
- The action matches commits at the **merge/squash PR level**, not individual commit messages
- If a merged commit has a matching label, **all commits within that PR** are returned
- Labels are checked on the PR object using `pr_has_label()`, not on commit metadata

### Parent Count Pattern
The code uses parent count to determine commit type:
- 2 parents = merge commit → expand to all PR commits
- 1 parent = squash commit → return the commit itself
- Other parent counts = skip

### Token Validation
The github_pr.py module performs strict token validation and exits with error messages if token is missing. Always ensure github_token input is provided.

### Output Format
- Commits are returned as space-separated SHA strings
- Order is preserved based on git log committerdate
- Duplicates are removed while maintaining order

## Testing Strategy

Tests use pytest with monkeypatch to mock GitHub API calls. Each test:
1. Mocks `get_pr_for_commit` to return a PR with "hotfix" label
2. Uses fixture repositories in test/fixtures/
3. Calls `get_matching_commits` with `required_labels=["hotfix"]`
4. Verifies the correct commits are extracted
