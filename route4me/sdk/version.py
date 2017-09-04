# -*- coding: utf-8 -*-

# ==============================================================================
#
# There are TWO copies of this file in the project.
# 1. /VERSION.py
# 2. /route4me/sdk/version.py
#
# First one is original, and should be used to describe meta information about
# package.
#
# Second is replaced during build on Travis CI, and published packaged contains
# a copy of /VERSION.py, extended with build info
#
# If you are MAINTAINER of this package - you should know, that BUMP VERSION
# occures in the /VERSION.py
#
# ==============================================================================

VERSION = (0, 1, 0)
RELEASE_SUFFIX = '-dev.8'

VERSION_STRING = '.'.join([str(x) for x in VERSION[0:3]])
RELEASE_STRING = VERSION_STRING + RELEASE_SUFFIX

PROJECT = 'Route4Me Python SDK'
COPYRIGHT = '2016-2017 © Route4Me Python Team'
AUTHOR = 'Route4Me Python Team (SDK)'
TITLE = 'route4me-sdk'
LICENSE = 'ISC'
BUILD = None   # TRAVIS_COMMIT
COMMIT = None  # TRAVIS_BUILD_NUMBER
