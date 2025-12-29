from github import Github
import requests
import sys

def get_pr_for_commit(repo_full_name, commit_sha, token):
    if not token or len(token.strip()) == 0:
        print("ERROR: GitHub token is empty or not provided.", file=sys.stderr)
        print("Please ensure the 'github_token' input is set correctly.", file=sys.stderr)
        print("For workflow_dispatch, use: github_token: ${{ secrets.GITHUB_TOKEN }}", file=sys.stderr)
        print("For workflow_call, ensure the token is passed from the calling workflow.", file=sys.stderr)
        sys.exit(1)

    g = Github(token)
    repo = g.get_repo(repo_full_name)

    pulls = repo.get_commit(commit_sha).get_pulls()
    return pulls[0] if pulls.totalCount > 0 else None


def pr_has_label(pr, label_name):
    return any(label.name == label_name for label in pr.get_labels())

