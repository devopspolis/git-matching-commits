from git import Repo
from github_pr import get_pr_for_commit, pr_has_label
from git_expansion import expand_merge_commit, expand_squash_commit


def get_matching_commits(
    repo_path,
    repo_full_name,
    start_ref,
    end_ref,
    github_token,
    required_labels=None
):
    repo = Repo(repo_path)

    start = repo.commit(start_ref)
    end = repo.commit(end_ref)

    shas = repo.git.log('--format=%H', f"{start.hexsha}..{end.hexsha}").splitlines()
    commits = [repo.commit(sha) for sha in shas]

    result = []

    required_labels = required_labels or ["hotfix"]

    for commit in commits:
        pr = get_pr_for_commit(repo_full_name, commit.hexsha, github_token)
        if not pr:
            continue

        if not any(pr_has_label(pr, label) for label in required_labels):
            continue

        if len(commit.parents) == 2:
            result.extend(expand_merge_commit(repo, commit))
        elif len(commit.parents) == 1:
            result.extend(expand_squash_commit(repo, commit))

    # Deduplicate, preserve order
    seen = set()
    unique = []
    for c in result:
        if c.hexsha not in seen:
            seen.add(c.hexsha)
            unique.append(c)

    return unique

