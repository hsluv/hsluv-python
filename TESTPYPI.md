# Rehearsing publishing with TestPyPI

This is an alternative to the production pre-release workflow proposed in
[PR #81](https://github.com/hsluv/hsluv-python/pull/81). It publishes **only to
TestPyPI**, using OIDC Trusted Publishing, and then downloads and tests the
uploaded wheel. It does not publish to production PyPI or require a release tag.

## One-time setup for Alexei

1. Merge `.github/workflows/testpypi.yml` into `main`.
2. Sign in to your **individual TestPyPI account** at <https://test.pypi.org/>.
   Accounts, project permissions, and Trusted Publishers are separate from
   production PyPI. Follow the individual-account guidance in
   [issue #84](https://github.com/hsluv/hsluv-python/issues/84): do not share
   credentials; use 2FA and store recovery codes securely.
3. In GitHub **Settings → Environments**, create **`testpypi`**. Restrict
   deployments to the **branch `main`**. For this initial rehearsal, adding
   `boronine` as a required reviewer is recommended where available. This is a
   GitHub identity, independent of your TestPyPI username.
4. If you already own `hsluv` on TestPyPI, add a GitHub Trusted Publisher at
   <https://test.pypi.org/manage/project/hsluv/settings/publishing/>. Otherwise,
   if the name is available, register a **pending publisher** at
   <https://test.pypi.org/manage/account/publishing/> with project name `hsluv`.
   A pending publisher creates the project on first upload, not at registration.
   If someone else owns the name, resolve ownership first; production ownership
   does not grant access on TestPyPI.

   | Field | Value |
   | --- | --- |
   | Owner (GitHub repository owner) | `hsluv` |
   | Repository name | `hsluv-python` |
   | Workflow filename | `testpypi.yml` |
   | Environment | `testpypi` |

   `Owner: hsluv` means the **GitHub organization**, not a shared TestPyPI login.
   No password or API token is stored in GitHub. Do not register this test
   workflow as a Trusted Publisher on **production** PyPI.

See the official [TestPyPI guide](https://packaging.python.org/en/latest/guides/using-testpypi/)
and [Trusted Publishing instructions](https://docs.pypi.org/trusted-publishers/using-a-publisher/).

## Run a rehearsal

1. Open **Actions → Rehearse publishing to TestPyPI → Run workflow** and select
   **`main`**.
2. Enter an **unused**, canonical PEP 440 development or pre-release version,
   for example `5.0.5.dev2026102101`. This is a testing example, not a decision
   about the next real release. Increase the test suffix for subsequent runs.
   Stable versions and local suffixes such as `+test` are deliberately rejected.
3. The workflow changes the literal `hsluv.__version__` in the runner's build
   copy only. It does **not** commit a version bump, modify the repository on
   GitHub, or create a tag. The test version also appears in the built package
   metadata, so `hsluv.__version__` and the installed version remain consistent.
4. Review the build results on Python 3.11 and 3.15. Approve the `testpypi`
   deployment if you configured required reviewers. Both builds must pass
   before the isolated OIDC upload job runs.
5. Confirm that the verification job downloads the exact wheel from TestPyPI,
   compares its SHA-256 hash to the tested build artifact, installs it, and runs
   the tests outside the source tree. It retries briefly for index propagation.
6. Inspect the version, files, and rendered description at
   <https://test.pypi.org/project/hsluv/>.

To try the uploaded wheel yourself, use a fresh virtual environment and replace
the example version with the one you published:

```sh
python -m pip --isolated install --index-url https://test.pypi.org/simple/ \
  --only-binary=:all: --no-deps "hsluv==5.0.5.dev2026102101"
```

HSLuv has no runtime dependencies, so there is no need to mix production PyPI
and TestPyPI with `--extra-index-url`. The workflow installs its build tools
from production PyPI, but uploads distributions and fetches the published wheel
only from TestPyPI.

## Limits and retries

- TestPyPI may periodically prune projects or accounts. Recheck ownership and
  publisher configuration if a previously working setup stops working.
- Uploaded filenames cannot be overwritten. For another build, choose a new
  test version; do not enable `skip-existing` to mask a failed rehearsal.
  If only verification failed after a successful upload, retry the verification
  job rather than re-uploading the same files.
- This workflow is intentionally manual. It does not upload on every push or PR.
- TestPyPI success does not verify production PyPI ownership or its OIDC
  publisher configuration. A production release needs separate authorization
  and configuration. This PR does not select a real release version or enable
  production publishing.
