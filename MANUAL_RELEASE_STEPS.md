# Manual Steps to Complete the Release

## What Has Been Done ✅

The release infrastructure for EigenScript v0.2.0-beta has been fully prepared:

1. ✅ Created comprehensive GitHub Actions release workflow (`.github/workflows/release.yml`)
2. ✅ Created detailed release documentation (`RELEASE.md`)
3. ✅ Synchronized version in `src/eigenscript/__init__.py` to match `pyproject.toml` (0.2.0-beta)
4. ✅ Created git tag `v0.2.0-beta` locally
5. ✅ Pushed commits to branch `copilot/release-new-version`

## What You Need to Do Manually 🚀

### Push the Release Tag

The git tag `v0.2.0-beta` has been created locally but needs to be pushed to GitHub to trigger the automated release workflow.

**Run this command:**

```bash
git push origin v0.2.0-beta
```

This single command will:
1. Push the tag to GitHub
2. Automatically trigger the release workflow
3. Build the Python package
4. Test across Python 3.9-3.12
5. Create a GitHub Release with CHANGELOG notes
6. Prepare for PyPI publishing (requires approval)

### Monitor the Release Workflow

After pushing the tag:

1. Go to: https://github.com/InauguralPhysicist/EigenScript/actions
2. Look for the "Release" workflow run
3. Monitor its progress through the stages:
   - Build Distribution
   - Test Built Package
   - Create GitHub Release
   - Publish to TestPyPI (requires approval)
   - Publish to PyPI (requires approval)

### Optional: Configure PyPI Publishing

If you want to publish to PyPI, you'll need to:

1. **Set up Trusted Publishing (Recommended)**:
   - Go to https://pypi.org/manage/account/publishing/
   - Add a new pending publisher:
     - PyPI Project Name: `eigenscript`
     - Owner: `InauguralPhysicist`
     - Repository name: `EigenScript`
     - Workflow name: `release.yml`
     - Environment name: `pypi` (for production) or `testpypi` (for testing)

2. **Create GitHub Environments** (optional, for approval gates):
   - Go to repository Settings → Environments
   - Create environments named `testpypi` and `pypi`
   - Add required reviewers for approval before publishing

For detailed instructions, see `RELEASE.md`.

## What the Release Workflow Will Do Automatically

Once the tag is pushed:

1. **Build Package**: Creates wheel and source distributions
2. **Test**: Installs and tests the package on Python 3.9, 3.10, 3.11, 3.12
3. **Create GitHub Release**: 
   - Extracts v0.2.0-beta notes from CHANGELOG.md
   - Creates a new GitHub Release
   - Attaches the built packages
   - Marks as pre-release (because it's a beta version)
4. **Publish** (if PyPI is configured):
   - TestPyPI: For validation
   - PyPI: For public distribution

## Summary

**Your next action:** Push the tag with:
```bash
git push origin v0.2.0-beta
```

Then monitor the Actions tab to see the automated release process in action!
