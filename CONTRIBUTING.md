# Contributing to pygame-topdownengine
Thank you for your interest in contributing to pygame-topdownengine! 

Please review the following before making contributions to this project.

## Issues
Whenever you have discovered a bug or would like to request a feature to be added to pygame-topdownengine, please create an issue on GitHub. Regardless of what type of issue you are raising, please make sure to always check for if the issue you are raising already exists and use a descriptive title that clearly describes the issue.

### Bug Reports
Whenever you are submitting a bug report, always include the following:
- detailed, step-by-step instructions to reproduce the bug
- environment information (e.g. package version, operating system)
- the expected behavior vs. the actual behavior

### Feature Requests
Whenever you are submitting a feature request, consider the core problem you are trying to solve and why the feature would be beneficial for the entire package. 

For example, a feature request for a `GameObject` subclass that has health baked-in would be rejected because it's something users can easily implement on their own, it doesn't benefit the package much, if at all, and the requirements users would have for such a class could vary on a case-by-case basic.

## Pull Requests
For any pull request that does more than one of the following, you **MUST** submit an issue first (see the Issues section above):
- Fixing a minor typo in the documentation, README, etc.
- Correcting small formatting errors.
- Extremely minor and obvious code cleanups that do not change application logic.

Examples of changes that would require an issue are bug fixes, new features, and substantial refactors.

When in doubt, just make an issue first!

### Developer Certificate of Origin (DCO)
All contributions to this project must be signed off under the Developer Certificate of Origin (DCO). This is a lightweight agreement that certifies you wrote (or have the right to submit) the contribution. Below is the full text of the DCO:

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

#### How to sign off on the DCO
Add a Signed-off-by trailer to every commit:
```
git commit -s -m "Your commit message"
```

This appends a line like:
```
Signed-off-by: Your Name <your.email@example.com>
```

If you forget, amend the most recent commit:
```
git commit --amend -s
```

If you have multiple unsigned commits already pushed to a branch, use an interactive rebase to sign them off all at once:
```
git rebase --signoff HEAD~N
```

### License
By contributing to this repository, you agree that your contributions will be licensed according to the target directory of your contribution:

- Core Package Files: Licensed under the MIT License found in the `LICENSE` file of the root folder.
- Examples (`examples/` folder): Licensed under the Creative Commons Zero 1.0 Universal license found in `examples/LICENSE`.
- Documentation (`docs/` folder): Licensed under the Creative Commons Zero 1.0 Universal license found in `docs/LICENSE`.