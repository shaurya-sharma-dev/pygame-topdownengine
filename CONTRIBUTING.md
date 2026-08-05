# Contributing to pygame-topdownengine
Thank you for your interest in contributing to pygame-topdownengine! 

Please review the following before making contributions to this project.

> [!NOTE]
> Always follow the [Code of Conduct](CODE_OF_CONDUCT.md) when making contributions to this repository.

## Issues
Please create an issue on GitHub to report bugs and request new features. Regardless of what type of issue you are raising, please make sure to always check for if the issue you are raising already exists and use a descriptive title that clearly describes the issue.

### Bug Reports
Whenever you are submitting a bug report, always include the following:
- detailed, step-by-step instructions to reproduce the bug
- environment information (e.g. package version, operating system)
- the expected behavior vs. the actual behavior

### Feature Requests
Whenever you are submitting a feature request, consider the core problem you are trying to solve and why the feature would be beneficial for the entire package. Make sure your feature request isn't outside of scope as well before submitting an issue!

In other words, **do not request highly specific or customizable features**. For example, a request for a subclass of `GameObject` with health would be rejected for the following reasons:
- **High Customization**: User requirements for a health class vary too much.
- **Low Value**: It adds little to no value to the core package.
- **Simple Self-Implementation**: Users can easily build this functionality on their own.

## Pull Requests
Only maintainers can create pull requests.

## Releasing (Maintainers Only)
1. Change version number in pyproject.toml and update changelog with new version header.
2. Run `git add . && git commit -m "chore: bump version."`
3. Run `git push origin main`.
4. Run `git tag v[version number]`. Make sure the version number used is the EXACT same one used in the pyproject.toml file.
5. Run `git push origin v[version number]`. This will push the tag to GitHub and start the release workflow.
6. Once the Test PyPI deployment is finished, check the project to ensure the new release is functioning and everything is correct. Once verified, accept the deployment to the production PyPI project on GitHub.
7. Once the PyPI deployment is finished, check the project on PyPI.