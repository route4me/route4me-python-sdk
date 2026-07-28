"""Guards on the package version.

``route4me/version.py`` and ``pyproject.toml`` each carry the version string:
version.py so ``route4me.__version__`` works without reading package metadata,
pyproject.toml so the build backend and ``python setup.py`` agree. Nothing
enforces that at runtime, so it is enforced here.
"""

import pathlib
import re
import unittest

import route4me
from route4me import version

PYPROJECT = pathlib.Path(__file__).resolve().parent.parent / "pyproject.toml"

# PEP 440, restricted to the shapes this project actually releases:
# four numeric components, optionally followed by a dev/alpha/beta/rc suffix.
PEP440 = re.compile(r"^\d+(\.\d+)*((a|b|rc|\.post|\.dev)\d+)?$")


def _pyproject_version():
    """Read ``project.version`` without needing a TOML parser on Python 3.9."""
    text = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    assert match, 'no `version = "..."` line found in pyproject.toml'
    return match.group(1)


class VersionTests(unittest.TestCase):
    """The version string is consistent everywhere it appears."""

    def test_pyproject_matches_version_module(self):
        """A release bump must touch both files, or the build is wrong."""
        self.assertEqual(
            _pyproject_version(),
            version.__version__,
            "pyproject.toml `version` and route4me/version.py `__version__` have drifted; bump both together",
        )

    def test_package_exports_version(self):
        self.assertEqual(route4me.__version__, version.__version__)

    def test_version_is_pep440(self):
        self.assertRegex(version.__version__, PEP440)

    def test_numeric_tuple_is_derived_from_the_string(self):
        self.assertEqual(version.VERSION, (0, 3, 0, 0))
        self.assertTrue(all(isinstance(part, int) for part in version.VERSION))

    def test_suffix_completes_the_string(self):
        numeric = ".".join(str(part) for part in version.VERSION)
        self.assertEqual(numeric + version.RELEASE_SUFFIX, version.__version__)

    def test_release_string_is_tag_shaped(self):
        """Git tags in this repo are `v` + the version, e.g. `v0.1.7.0`."""
        self.assertEqual(version.RELEASE_STRING, "v" + version.__version__)


if __name__ == "__main__":
    unittest.main()
