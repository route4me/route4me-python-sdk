# -*- coding: utf-8 -*-

from .api import Route4Me
from .advanced_constraint import AdvancedConstraint
from .exceptions import APIException, ParamValueException
from .bundling import Bundling
from .bundling import BUNDLING_MODE, BUNDLING_FIRST_ITEM_MODE, BUNDLING_ADDITIONAL_ITEM_MODE, BUNDLING_MERGE_MODE

from .version import PROJECT
from .version import COPYRIGHT
from .version import AUTHOR
from .version import TITLE
from .version import LICENSE
from .version import VERSION_STRING
from .version import RELEASE_STRING
from .version import BUILD
from .version import COMMIT

__project__ = PROJECT
__copyright__ = COPYRIGHT
__author__ = AUTHOR
__title__ = TITLE
__license__ = LICENSE
__version__ = VERSION_STRING
__release__ = RELEASE_STRING
__build__ = BUILD
__commit__ = COMMIT


__all__ = [
    'Route4Me',
    'APIException',
    'ParamValueException',
    '__project__',
    '__copyright__',
    '__author__',
    '__title__',
    '__license__',
    '__version__',
    '__release__',
    '__build__',
    '__commit__',
    'AdvancedConstraint',
    'Bundling',
    'BUNDLING_MODE',
    'BUNDLING_FIRST_ITEM_MODE',
    'BUNDLING_ADDITIONAL_ITEM_MODE',
    'BUNDLING_MERGE_MODE'
]
