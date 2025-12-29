from git import Repo

def expand_merge_commit(repo: Repo, merge_commit):
    """
    Expand a standard 2-parent merge commit.
    Returns PR commits only.
    """
    if len(merge_commit.parents) != 2:
        return []

    base, head = merge_commit.parents
    rev_range = f"{base.hexsha}..{head.hexsha}"

    shas = repo.git.log('--format=%H', '--reverse', rev_range).splitlines()
    return [repo.commit(sha) for sha in shas]


def expand_squash_commit(repo: Repo, squash_commit):
    """
    Squash merge:
    - Single parent
    - The squash commit itself represents PR content
    """
    return [squash_commit]

