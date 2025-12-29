# git-matching-commits

This GitHub Action finds all commits between two git refs (tags, branches, or SHAs) where the associated Pull Request has a matching GitHub label. For merge commits, it expands to include all individual commits from the PR. For squash commits, it returns the squash commit itself.

The order of the returned commits is according to `committerdate`.


## Usage

### Required Permissions
This action requires a GitHub token and `pull-requests: read` permission to fetch PR information:

```yaml
permissions:
  contents: read
  pull-requests: read  # Required for git-matching-commits to access PR data
```

**Important:** The workflow will fail with an AssertionError if the token is empty or missing.

### How It Works

This action **only returns commits that are associated with Pull Requests**. The filtering is based on GitHub PR labels, not commit messages or tags.

**Commits that WILL be returned:**
- Commits from merged PRs with matching labels
- Commits from squashed PRs with matching labels
- All individual commits within a merge PR (if the PR has a matching label)

**Commits that will NOT be returned:**
- Direct commits to any branch (commits made without a PR)
- Commits pushed directly via `git push` (bypassing PR workflow)
- Commits made through GitHub web UI edits (unless done via a PR)
- Commits with "hotfix" or other keywords in the message but no associated PR

> **Note:** If your workflow includes direct commits to branches, those commits will never be detected by this action, even if they contain matching keywords or are tagged. This is by design since the action relies entirely on GitHub PR labels for filtering.

### Basic Usage
```yaml
    - uses: devopspolis/git-matching-commits@v1
      with:
        start_ref: v1.0.0
        end_ref: HEAD
        github_repository: ${{ github.repository }}
        github_token: ${{ secrets.GITHUB_TOKEN }}
        github_labels: hotfix
```

### Inputs

| Name                   | Description                                 | Required | Default              |
| ---------------------- |:------------------------------------------- |:-------- | :------------------- |
| start_ref              | Start git ref (tag, branch, or SHA)         | Yes      | -                    |
| end_ref                | End git ref (tag, branch, or SHA)           | Yes      | -                    |
| github_repository      | GitHub repository in owner/name format      | Yes      | -                    |
| github_token           | GitHub token for API access                 | Yes      | -                    |
| github_labels          | Comma-separated list of GitHub PR labels (at least one must be present on the PR) | No | hotfix |
| repo_path              | Path to the git repository                  | No       | .                    |

## Examples

### Example 1: Find commits with 'hotfix' label between latest v1.x.0 tag and HEAD
```yaml
    - uses: devopspolis/git-matching-commits@v1
      id: git-matching-commits
      with:
        start_ref: v1.0.0
        end_ref: HEAD
        github_repository: ${{ github.repository }}
        github_token: ${{ secrets.GITHUB_TOKEN }}
        github_labels: hotfix

    - name: Get matched commits
      run: echo "MATCHED_COMMITS=${{ steps.git-matching-commits.outputs.commits }}" >> $GITHUB_ENV
```

### Example 2: Find commits with multiple possible labels
```yaml
    - uses: devopspolis/git-matching-commits@v1
      id: git-matching-commits
      with:
        start_ref: v2.5.0
        end_ref: v2.6.0
        github_repository: myorganization/myrepo
        github_token: ${{ secrets.GITHUB_TOKEN }}
        github_labels: hotfix,bugfix,critical

    - name: Display results
      run: |
        echo "Found ${{ steps.git-matching-commits.outputs.count }} commits"
        echo "First: ${{ steps.git-matching-commits.outputs.first_commit }}"
        echo "Last: ${{ steps.git-matching-commits.outputs.last_commit }}"
        echo "All: ${{ steps.git-matching-commits.outputs.commits }}"
```

### Example 3: Use with a specific branch
```yaml
    - uses: devopspolis/git-matching-commits@v1
      id: git-matching-commits
      with:
        start_ref: origin/main
        end_ref: origin/release-branch
        github_repository: ${{ github.repository }}
        github_token: ${{ secrets.GITHUB_TOKEN }}
        github_labels: cherry-pick
```


## Output
```shell
steps.git-matching-commits.outputs.commits      # Set to space separated list of matched commit SHAs
steps.git-matching-commits.outputs.count        # The number of matched commits
steps.git-matching-commits.outputs.first_commit # The first commitSHA in the list
steps.git-matching-commits.outputs.last_commit  # The last commitSHA in the list

Example:
steps.git-matching-commits.outputs.commits=f9e96e6afbf893795c3c5f44d968b19fa51925cc e5b84631f0824d9e8c57d44893abdae96917aab9 186e65812e63c80fbf3690723454ebc5f09fb05b 0f3e43604075eafe0a432cc4d4f1bb421aa800c3 285f45cb9871d3b6cf9758700f85fb51436dbcd2
steps.git-matching-commits.outputs.count=5
steps.git-matching-commits.outputs.first_commit=f9e96e6afbf893795c3c5f44d968b19fa51925cc
steps.git-matching-commits.outputs.last_commit=285f45cb9871d3b6cf9758700f85fb51436dbcd2
```

## License
The MIT License (MIT)
