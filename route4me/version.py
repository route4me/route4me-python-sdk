# -*- coding: utf-8 -*-

# ==============================================================================
# Source of truth for the package version.
#
# This file used to be generated at *import* time by ``rewrite_version()`` in
# setup.py, which copied the top-level VERSION.py over it. That broke PEP 517
# isolated builds (they run in a temp copy, where the write lands nowhere
# useful) and made sdists non-reproducible. It is now hand-maintained.
#
# When releasing, bump ``__version__`` here AND ``project.version`` in
# pyproject.toml. ``tests/test_version.py`` fails the build if they drift.
# ==============================================================================

__version__ = "0.2.0.0.dev0"

#: Numeric release components, derived from :data:`__version__`.
#: ``"0.2.0.0.dev0"`` -> ``(0, 2, 0, 0)``.
VERSION = tuple(int(part) for part in __version__.split(".") if part.isdigit())

#: Any PEP 440 suffix trailing the numeric components -- ``".dev0"``, ``"rc1"``,
#: or ``""`` for a final release.
RELEASE_SUFFIX = __version__[len(".".join(str(part) for part in VERSION)):]

VERSION_STRING = __version__
RELEASE_STRING = "v{}".format(__version__)

PROJECT = "Route4Me Python SDK"
COPYRIGHT = "2016-2026 © Route4Me Python Team"
AUTHOR = "Route4Me Python Team (SDK)"
AUTHOR_EMAIL = "juan@route4me.com"
TITLE = "route4me"
LICENSE = "ISC"

#: Populated by CI at build time; ``None`` for local and source installs.
BUILD = None
COMMIT = None
