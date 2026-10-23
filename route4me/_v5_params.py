"""Parameter helpers shared by the vehicle and optimization-profile resources (API V5).

Each method of those resources takes its query or its JSON body as keyword
arguments. :func:`query` copies the query of one call and :func:`require`
checks the names the API marks as required, before anything is sent.
"""

from .exceptions import ParamValueException


def query(params):
    """Copy the query keywords of one call, sending each ``bool`` as ``1`` or ``0``.

    ``requests`` would send ``True`` as the string ``"True"``. Like the C# SDK,
    these resources send ``1`` and ``0`` instead.

    >>> query({"with_pagination": True, "page": 2})
    {'with_pagination': 1, 'page': 2}

    :param params: the query keywords of one call.
    :return: a new dict, so no value is kept on the resource between calls.
    """
    return {name: int(value) if isinstance(value, bool) else value for name, value in params.items()}


def require(params, names):
    """Check that the keywords of one call contain every required name.

    :param params: the keywords of one call.
    :param names: the names the API requires.
    :raise ParamValueException: naming each missing parameter.
    """
    missing = [name for name in names if name not in params]
    if missing:
        raise ParamValueException(", ".join(missing), "Missing required params")
