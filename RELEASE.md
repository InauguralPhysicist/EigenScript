# Release Process for EigenScript

This document describes the release process for EigenScript.

## Overview

EigenScript uses automated GitHub Actions workflows to build, test, and publish releases. The process is triggered by pushing version tags to the repository.

## Prerequisites

Before creating a release, ensure:

1. **Version is updated** in `pyproject.toml`
2. **CHANGELOG.md is updated** with release notes for the new version
3. **All tests pass** on the main/develop branch
4. **Documentation is up to date**

## Release Workflow

The release workflow (`.github/workflows/release.yml`) consists of several jobs:

### 1. Build Distribution
- Builds both wheel (`.whl`) and source distribution (`.tar.gz`)
- Validates the built packages with `twine check`
- Uploads artifacts for use by subsequent jobs

### 2. Test Built Package
- Tests the built package across Python 3.9, 3.10, 3.11, and 3.12
- Installs the wheel and verifies basic functionality
- Ensures the package works on all supported Python versions

### 3. Create GitHub Release
- Extracts release notes from CHANGELOG.md for the specific version
- Creates a GitHub Release with the extracted notes
- Attaches the built distributions to the release
- Marks as pre-release if version contains 'alpha', 'beta', or 'rc'

### 4. Publish to TestPyPI (Optional)
- Publishes to TestPyPI for validation
- Requires environment approval (configured in GitHub Settings)
- Allows testing installation from TestPyPI before publishing to production

### 5. Publish to PyPI (Optional)
- Publishes to production PyPI
- Requires environment approval (configured in GitHub Settings)
- Makes the package publicly available via `pip install eigenscript`

## Creating a Release

### Step 1: Prepare the Release

1. Update version in `pyproject.toml`:
   ```toml
   [project]
   version = "0.2.0-beta"
   ```

2. Update `CHANGELOG.md` with release notes:
   ```markdown
   ## [0.2.0-beta] - 2025-11-23
   
   ### Added
   - Feature 1
   - Feature 2
   
   ### Changed
   - Change 1
   
   ### Fixed
   - Bug fix 1
   ```

3. Commit the changes:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Prepare release v0.2.0-beta"
   git push
   ```

### Step 2: Create and Push the Tag

```bash
# Create annotated tag
git tag -a v0.2.0-beta -m "Release v0.2.0-beta"

# Push the tag to trigger the release workflow
git push origin v0.2.0-beta
```

### Step 3: Monitor the Workflow

1. Go to the "Actions" tab in the GitHub repository
2. Watch the "Release" workflow execution
3. The workflow will:
   - Build the package
   - Test it across Python versions
   - Create a GitHub Release
   - Wait for approval to publish to TestPyPI
   - Wait for approval to publish to PyPI

### Step 4: Approve PyPI Publication (Optional)

If you want to publish to PyPI:

1. Go to the workflow run in GitHub Actions
2. Approve the "testpypi" environment deployment
3. Verify the package on TestPyPI: https://test.pypi.org/project/eigenscript/
4. Test installation from TestPyPI:
   ```bash
   pip install -i https://test.pypi.org/simple/ eigenscript
   ```
5. If everything looks good, approve the "pypi" environment deployment
6. The package will be published to production PyPI

## Setting Up PyPI Environments

To enable PyPI publishing, you need to configure GitHub environments and secrets:

### TestPyPI Setup

1. Register at https://test.pypi.org/
2. Create an API token at https://test.pypi.org/manage/account/token/
3. In GitHub repository settings:
   - Go to Settings → Environments
   - Create environment named "testpypi"
   - Add protection rules (e.g., required reviewers)
   - Add environment secret `PYPI_API_TOKEN` with TestPyPI token

### PyPI Setup

1. Register at https://pypi.org/
2. Create an API token at https://pypi.org/manage/account/token/
3. In GitHub repository settings:
   - Go to Settings → Environments
   - Create environment named "pypi"
   - Add protection rules (e.g., required reviewers)
   - Add environment secret `PYPI_API_TOKEN` with PyPI token

**Note**: The workflow uses Trusted Publishing (OIDC) which is more secure than API tokens. To set up Trusted Publishing:

1. Go to PyPI project settings
2. Add a "Trusted Publisher"
3. Configure:
   - Owner: InauguralPhysicist
   - Repository: EigenScript
   - Workflow: release.yml
   - Environment: pypi (or testpypi)

## Manual Release Trigger

The workflow can also be triggered manually via GitHub Actions UI:

1. Go to Actions → Release workflow
2. Click "Run workflow"
3. Enter the tag name (e.g., `v0.2.0-beta`)
4. Click "Run workflow"

## Version Numbering

EigenScript follows [Semantic Versioning](https://semver.org/):

- **Major version** (X.0.0): Breaking changes
- **Minor version** (0.X.0): New features, backward compatible
- **Patch version** (0.0.X): Bug fixes, backward compatible

Pre-release versions:
- **Alpha** (0.X.0-alpha): Early development, unstable
- **Beta** (0.X.0-beta): Feature complete, testing phase
- **RC** (0.X.0-rc1): Release candidate, final testing

## Rollback

If a release needs to be rolled back:

1. Delete the GitHub Release (if published)
2. Delete the git tag:
   ```bash
   git tag -d v0.2.0-beta
   git push origin :refs/tags/v0.2.0-beta
   ```
3. If published to PyPI, you cannot delete a version (PyPI policy)
   - Instead, publish a new patch version with fixes
   - Use `yank` feature on PyPI to mark version as problematic

## Troubleshooting

### Build Fails

- Check that `pyproject.toml` is valid
- Ensure all dependencies are correctly specified
- Review build logs in GitHub Actions

### Tests Fail

- Run tests locally before creating tag
- Check compatibility across Python versions
- Review test logs in GitHub Actions

### PyPI Upload Fails

- Verify API token is correct
- Check that version doesn't already exist on PyPI
- Ensure package metadata is valid (run `twine check dist/*`)

### Release Notes Not Extracted

- Ensure CHANGELOG.md follows the format: `## [VERSION] - DATE`
- Version in CHANGELOG should match the tag version (without 'v' prefix)
- Check that there's content between version headers

## Current Release: v0.2.0-beta

For the current release:

```bash
# Tag has been created as part of this setup
git tag -a v0.2.0-beta -m "Release v0.2.0-beta - Native LLVM Compiler"
git push origin v0.2.0-beta
```

This will trigger the release workflow and create:
- GitHub Release with CHANGELOG notes
- Built distributions (wheel and sdist)
- Optional publication to PyPI (requires environment approval)

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub Actions: Publishing to PyPI](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
