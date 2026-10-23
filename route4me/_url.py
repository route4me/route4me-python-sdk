"""Safe URL construction helpers.

The SDK interpolates caller-supplied values straight into URL *paths* --
zip codes, house numbers, offsets, and (from API V5 onward) resource IDs in
endpoints like ``/route-status/{route_id}``. Without escaping, a value
containing ``/``, ``?``, ``#`` or ``..`` rewrites the request path against the
target host instead of being passed as data.

V5 is REST-style, so every one of its ~200 endpoints has this same surface.
Use these helpers for anything that lands in a path; they are not optional.
"""

from urllib.parse import quote

from .exceptions import ParamValueException


def path_segment(value, name="value"):
    """Return ``value`` percent-encoded for use as a single URL path segment.

    ``safe=""`` is the point: the default ``quote`` behaviour leaves ``/``
    untouched, which is precisely the character that lets a value escape its
    segment.

    >>> path_segment("00602", "zipcode")
    '00602'
    >>> path_segment("../../admin", "zipcode")
    '..%2F..%2Fadmin'
    >>> path_segment("a b?c#d", "alias")
    'a%20b%3Fc%23d'

    :param value: the value to encode; converted with ``str()``.
    :param name: parameter name reported in the error.
    :return: the percent-encoded segment.
    :raise ParamValueException: if the value is ``None`` or empty. An empty
        segment would silently collapse the path and hit the wrong endpoint.
    """
    if value is None:
        raise ParamValueException(name, "must not be None")
    text = str(value)
    if not text or text.isspace():
        raise ParamValueException(name, "must not be empty")
    return quote(text, safe="")


def path_int(value, name="value", minimum=0):
    """Return ``value`` validated as a non-negative integer, as a string.

    Used for ``offset``/``limit`` style path components. Rejecting rather than
    escaping is right here: a non-numeric offset is a caller bug, and encoding
    it would produce a confusing 404 instead of a clear error.

    >>> path_int(10, "offset")
    '10'

    :param value: an ``int``, or a string holding one. ``bool`` is rejected.
    :param name: parameter name reported in the error.
    :param minimum: smallest accepted value.
    :return: the integer as a string.
    :raise ParamValueException: if the value is not an integer, or is below
        ``minimum``.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        # bool is an int subclass; a True offset is never intended.
        try:
            value = int(str(value))
        except (TypeError, ValueError):
            raise ParamValueException(name, "must be an integer") from None
    if value < minimum:
        raise ParamValueException(name, f"must be >= {minimum}")
    return str(value)


def join_path(base, *segments):
    """Append already-encoded ``segments`` to ``base``, normalising slashes.

    Does **not** encode -- pass values through :func:`path_segment` or
    :func:`path_int` first. Keeping encoding separate from joining means a
    double-encoding bug is impossible to introduce by accident here.

    >>> join_path("https://rapid.route4me.com/street_data/", "00602", "17")
    'https://rapid.route4me.com/street_data/00602/17/'

    :param base: the base URL.
    :param segments: path segments, already encoded.
    :return: the joined URL, always ending with ``/``.
    """
    url = base.rstrip("/")
    for segment in segments:
        url = f"{url}/{str(segment).strip('/')}"
    return url + "/"


#: URL prefix of every API V5 endpoint.
API_V5_PREFIX = "https://wh.route4me.com/modules/api/v5."


def is_v5_url(url):
    """Tell whether ``url`` is an API V5 endpoint, which takes a bearer token.

    >>> is_v5_url("https://wh.route4me.com/modules/api/v5.0/route-status/X")
    True
    >>> is_v5_url("https://api.route4me.com/api.v4/route.php")
    False

    :param url: absolute URL of the endpoint.
    :return: ``True`` for ``https://wh.route4me.com/modules/api/v5.*`` URLs.
    """
    return str(url).startswith(API_V5_PREFIX)
