# Publishing pre-releases to PyPI

Publishing uses [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
(GitHub Actions OIDC), not a stored PyPI password or API token.
This setup does not create releases or change the package version.

## One-time setup for Alexei

First complete the access checks in [issue #84](https://github.com/hsluv/hsluv-python/issues/84):
sign in to PyPI using your individual **`boronine`** account and verify that it
has the **Owner** role on the existing `hsluv` project. If needed, have a current
Owner invite it, accept the invitation, and verify access before removing any
existing access. Each human maintainer should use their own account with 2FA
and securely stored recovery codes; consider a second trusted individual Owner
for continuity.

Do not share the login for an ordinary PyPI user account named `hsluv`.
[PyPI's terms prohibit shared logins](https://policies.python.org/pypi.org/Terms-of-Service/#3-account-requirements).
A genuine [community PyPI organization](https://docs.pypi.org/organization-accounts/)
is an optional way to manage the project and individual members, not a
prerequisite for Trusted Publishing. Confirm the existing account's type before
changing it. Do not delete or recreate the package, or delete an old account
before checking all its projects and access dependencies.

1. Merge the workflow into `main`.
2. In the **hsluv/hsluv-python** GitHub repository, open **Settings → Environments**
   and create an environment named **`pypi`**.
   - Add Alexei (`boronine`) as a required reviewer. Add other trusted release
     maintainers if desired. Approval is required before the upload job starts.
   - Under deployment branches and tags, select **Selected branches and tags**
     and allow the **branch `main`** only. If an existing rule still names
     `master`, replace it with `main` while keeping required reviewers.
     The workflow is dispatched from `main`; its build job separately checks
     out the requested tag.
   - If GitHub does not offer required reviewers under the repository's plan,
     do not assume that the workflow itself provides an approval gate. Resolve
     that limitation before enabling publishing.
3. While signed in to PyPI as **`boronine`**, an Owner of the existing `hsluv`
   project, open
   <https://pypi.org/manage/project/hsluv/settings/publishing/> and add a
   **GitHub** trusted publisher with exactly these values:

   | Field | Value |
   | --- | --- |
   | Owner (GitHub repository owner) | `hsluv` |
   | Repository name | `hsluv-python` |
   | Workflow name (filename, not display name) | `publish-prerelease.yml` |
   | Environment name | `pypi` |

   Register against the **existing project**, not as a pending publisher.
   Here `hsluv` identifies the **GitHub organization**, not the PyPI account
   used to log in. Future uploads authenticate as the trusted workflow, not as
   `boronine` or a shared `hsluv` login.
   See [PyPI's setup instructions](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).
4. Do not add `PYPI_API_TOKEN`, a password, or other PyPI secrets to GitHub.
   Only the isolated upload job receives `id-token: write`; it downloads the
   tested artifacts and does not check out or execute the package source.

After individual-owner access and the publishing setup have been verified,
retire any shared-login arrangement and revoke obsolete CI tokens once their
replacement is confirmed working, as tracked in issue #84. An organization
transfer, if desired, is a separate administration step; it does not require
changing the package name, authors, or license.

**Stop here for the setup PR.** Do not bump the version, create a tag, dispatch
the workflow, or approve a deployment yet. Those steps belong to a follow-up.

## Publishing later, after a separate release-preparation PR

1. Choose an unused alpha, beta, or release-candidate version, such as
   `5.0.5rc1` (**example only**, not a version selected by this setup).
   Update `hsluv.__version__`, merge that change into `main`, and ensure CI passes.
2. Create and push a tag on that reviewed commit, named exactly `v` followed by
   the version (for example, `v5.0.5rc1`). The tag must point to a commit in
   `main`'s history. Protect release tags against modification/deletion using
   repository rules where available.
3. Open **Actions → Publish a pre-release to PyPI → Run workflow**. Select
   **`main`** as the workflow branch and enter the existing tag as **tag**.
   Creating a tag or a GitHub release alone does **not** trigger publication.
4. The workflow rejects stable, development, local, or mismatched versions,
   builds both distributions, checks their metadata, and tests installation of
   the source archive and wheel on Python 3.11 and 3.15.
5. Review the workflow run, tag/commit, and build artifacts. Approve the **`pypi`**
   deployment only when ready: approval publishes to **production PyPI**, not
   TestPyPI. OIDC setup or environment configuration errors must be fixed before
   approving a new attempt; do not work around them by adding a long-lived token.
6. Confirm the version and files at <https://pypi.org/project/hsluv/>. Test with
   `python -m pip install --pre hsluv` in a clean environment (or pin the exact
   version). Ordinary installs generally do not select pre-releases when a
   satisfactory stable release exists.

PyPI does not let you overwrite an uploaded filename. If a published artifact
needs correction, prepare a new pre-release version instead of moving the tag
or rebuilding the same version. This workflow intentionally does not skip
already-uploaded files.

## Stable releases

Stable publication is intentionally unsupported by this workflow. Enabling it
requires a separately reviewed change; do not bypass the pre-release checks.
