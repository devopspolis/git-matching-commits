def test_squash_hotfix(monkeypatch):
    from git_matching_commits import get_matching_commits

    def mock_get_pr(*args, **kwargs):
        class PR:
            def get_labels(self):
                return [type("L", (), {"name": "hotfix"})()]
        return PR()

    monkeypatch.setattr("github_pr.get_pr_for_commit", mock_get_pr)

    commits = get_matching_commits(
        repo_path="tests/fixtures/squash-repo",
        repo_full_name="org/repo",
        start_ref="HEAD~1",
        end_ref="HEAD",
        github_token="x",
        required_labels=["hotfix"]
    )

    assert len(commits) == 1
    assert "Squash PR" in commits[0].message

