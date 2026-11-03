# Git workflow

The repository integrates changes through branches and pull requests (PRs); do not make work changes directly on shared branches.

## Branches and targets

- `main`: production branch.
- `develop`: integration branch and starting point for regular work.
- `release`: stabilization branch before production.
- `feature/<name>`: new functionality, created from `develop` and submitted to `develop` by PR.
- `fix/<name>`: non-urgent correction, created from `develop` and submitted to `develop` by PR.
- `hotfix/<name>`: urgent correction based on `main`; when complete, integrate it into `main`, `release`, and `develop` through PRs to keep the shared branches in sync.

## Normal flow

1. Update `develop` and create a descriptive `feature/*` or `fix/*` branch from it.
2. Implement the change and add or update relevant tests and documentation.
3. Open a PR targeting `develop`. Explain its purpose, summarize the changes, and note the tests run.
4. When integration is ready for a release, open a PR from `develop` to `release` and validate that branch.
5. After stabilization, open a PR from `release` to `main` to publish.

For a `hotfix/*`, base the branch on `main`, validate the correction, and open the synchronization PRs to the shared branches listed above.

## Continuous integration

The `.github/workflows/test.yml` workflow runs on pushes to `main`, `develop`, `release`, `feature/**`, `release/**`, and `hotfix/**`, and on PRs targeting `develop`, `release`, or `main`. It uses Ubuntu and Python 3.12, installs `.[dev]`, runs `pytest` with `QT_QPA_PLATFORM=offscreen`, and checks imports. `compileall` and `git diff --check` also run, but their steps do not block the workflow on failure. Pushes to `fix/*` branches are not listed as a trigger; the test suite does run when their PR to `develop` is opened or updated. See [Development](development.md) for the local command.

The CI deploy job runs after tests only for pushes to `release` or `main`. It reports that Render will auto-deploy; the service and watched branch are configured in Render. See [Deployment](deployment.md) for environment variables and the smoke test.
