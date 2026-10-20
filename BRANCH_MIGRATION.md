# Renaming the default branch from master to main

This checklist prepares the rename; merging it does **not** rename a branch,
change GitHub settings, or publish a release. An administrator such as Alexei
must perform the GitHub steps below.

## Before the rename

- [ ] Merge this checklist into the current default branch.
- [ ] Review any changes merged since this checklist was written for explicit
  `master` references. The existing test workflow has no branch filters,
  Dependabot has no `target-branch`, and the README badges do not specify a
  branch, so those configurations already work with `main`.
- [ ] Coordinate the pending [PyPI publishing setup PR #81](https://github.com/hsluv/hsluv-python/pull/81).
  Its initial version hard-codes `master` in the build-job condition, the tag
  ancestry check, and `RELEASING.md`. Do not assume GitHub will rewrite these.
  Before enabling publishing, either update that PR to use the repository's
  default branch dynamically, or change those references to `main` after the
  rename. If it has already merged, make the equivalent follow-up change.
  A branch-independent implementation can use:

  ```yaml
  if: github.repository == 'hsluv/hsluv-python' && github.ref == format('refs/heads/{0}', github.event.repository.default_branch)
  ```

  and pass `github.event.repository.default_branch` through an environment
  variable for the ancestry check:

  ```yaml
  env:
    DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}
  run: git merge-base --is-ancestor HEAD "origin/$DEFAULT_BRANCH"
  ```

  Keep the upstream-repository restriction, pre-release checks, and approval
  requirements intact. Update the release instructions to select the default
  branch in the workflow-dispatch UI.
- [ ] Review branch protection, repository/organization rulesets, required status
  checks, environment deployment restrictions, webhooks, external CI, and any
  scripts outside this repository. Record the current settings before changing
  them; not all are visible to contributors or represented in Git.
- [ ] Confirm that no existing `main` branch conflicts with the rename. Do not
  overwrite or delete an existing branch to make room without investigating it.
- [ ] Avoid publishing or approving a release while the rename is in progress.

## Administrator steps on GitHub

1. Open the repository's [branches page](https://github.com/hsluv/hsluv-python/branches).
   Use the branch menu's **Rename branch** operation to rename **`master`** to
   **`main`**. Rename the existing branch rather than creating a second branch
   and deleting the first. Organization rules may require an organization
   administrator to authorize this.
2. Verify that **Settings → General → Default branch** now names **`main`**.
   GitHub normally updates branch protection policies and the base branch of
   open PRs when renaming a branch; verify those changes instead of assuming
   every rule or external integration was updated.
3. Verify that open PRs target `main`, including PRs from forks, and that their
   checks still run. Reconcile conflicts with the new base as needed.
4. If the **`pypi`** environment from PR #81 exists, inspect **Settings →
   Environments → pypi → Deployment branches and tags**. Replace any explicit
   **branch `master`** restriction with **branch `main`** and retain required
   reviewers. Do not remove deployment restrictions just to get a run working.
5. The proposed PyPI Trusted Publisher identifies the repository, workflow
   filename, and environment—not the default branch—so those PyPI fields do
   not need changing solely for this rename. Keep `publish-prerelease.yml` and
   `pypi` unchanged, and verify the actual configured publisher still matches.
6. Update external integrations, raw-content URLs, scripts, or consumers that
   explicitly request `master`. GitHub redirects ordinary file URLs, but not
   raw file URLs, Git fetch/pull requests, or action references such as
   `uses: owner/repository@master`.

## Updating local clones

First ensure the working tree is safe to switch branches and that no unrelated
local branch named `main` already exists. With `origin` pointing to
`hsluv/hsluv-python`, run:

```sh
git branch -m master main
git fetch origin
git branch --set-upstream-to=origin/main main
git remote set-head origin -a
```

These commands rename the local default branch; feature branches need not be
renamed. If your upstream repository is named `upstream` rather than `origin`,
substitute that remote in the commands. Fork owners should also check their
fork's default branch and update it separately if necessary. There is no need
to reset commits, force-push, or discard local work.

## Final verification

- [ ] `gh repo view hsluv/hsluv-python --json defaultBranchRef` reports `main`.
- [ ] The renamed branch points to the expected commit history.
- [ ] Existing protection/ruleset requirements and required checks still apply.
- [ ] A push or PR runs the test workflow successfully on Python 3.11 and 3.15.
- [ ] The test workflow is available for manual dispatch from `main`; scheduled
  workflows and Dependabot continue to use the repository's default branch.
- [ ] README badges and links still work.
- [ ] Any publishing workflow and release instructions now use `main` or discover
  the default branch dynamically, and the `pypi` environment allows `main` only.
- [ ] No publishing workflow was dispatched merely to test the rename. Its
  end-to-end publishing test remains part of the separately approved pre-release.

Reference: [GitHub's branch-renaming documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/renaming-a-branch).
