# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

# Version info tuple in same format as sys.version_info.
__version_info__ = (0, 6, 0, "final", 0)

# The below code defines a function called _get_version_string. 
# The underscore is added to the beginning to signify that the function itself isn't part of the public API.

def _get_version_string(version_info: tuple = __version_info__) -> str:
    # Get the major.minor.patch integers as a list of strings.
    _parsed_version_info = [str(x) for x in version_info[:3]]

    # This if condition runs on prereleases (alpha, beta, and release candidate).
    if version_info[3] != "final":
        # For prereleases, first map the prerelease string ("alpha", "beta", "candidate")
        # to its appropriate PEP 440 prerelease tag before appending the prerelease number to it.

        # Then, we append the prerelease tag and number (e.g. a1, b2, rc3) to the last list element.
        # We append it to the last list element instead of making its own list element because prereleases 
        # CANNOT be seperated by periods. So 1.2.3a4 is valid, but 1.2.3.a4 is not.
        _parsed_version_info[2] += {
            "alpha": "a", 
            "beta": "b", 
            "candidate": "rc",
        }[version_info[3]] + str(version_info[4])

    # Join everything in the _parsed_version_info list while separating it with dots.
    return ".".join([str(x) for x in _parsed_version_info])

# Generate the PEP 440 compliant version string.
__version__ = _get_version_string()