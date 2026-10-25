"""Route4Me Python SDK.

A client for the Route4Me route optimization API. Create a :class:`Route4Me`
client with an API key and use its resource attributes::

    from route4me import Route4Me

    route4me = Route4Me("11111111111111111111111111111111")
    routes = route4me.route.get_routes(limit=10, offset=0)

The package also exports the exceptions, :class:`AdvancedConstraint`,
:class:`Bundling` and the bundling mode constants.
"""

from .advanced_constraint import AdvancedConstraint
from .api import Route4Me
from .bundling import (
    BUNDLING_ADDITIONAL_ITEM_MODE,
    BUNDLING_FIRST_ITEM_MODE,
    BUNDLING_MERGE_MODE,
    BUNDLING_MODE,
    Bundling,
)
from .exceptions import APIException, ParamValueException
from .version import AUTHOR, BUILD, COMMIT, COPYRIGHT, LICENSE, PROJECT, RELEASE_STRING, TITLE, VERSION_STRING

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
    "BUNDLING_ADDITIONAL_ITEM_MODE",
    "BUNDLING_FIRST_ITEM_MODE",
    "BUNDLING_MERGE_MODE",
    "BUNDLING_MODE",
    "APIException",
    "AdvancedConstraint",
    "Bundling",
    "ParamValueException",
    "Route4Me",
    "__author__",
    "__build__",
    "__commit__",
    "__copyright__",
    "__license__",
    "__project__",
    "__release__",
    "__title__",
    "__version__",
]
