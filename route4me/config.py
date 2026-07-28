"""Process-wide SDK configuration.

Mirrors ``Route4MeConfig`` in the C# SDK so the two clients can be tuned the
same way. Every knob here is also accepted as a constructor keyword on
:class:`route4me.Route4Me`, and resolution runs:

    per-call argument  >  constructor argument  >  Route4MeConfig  >  default

The global exists for operators: bumping a timeout for a whole service without
touching call sites. The constructor argument exists because a process that
talks to two accounts, or to staging and production, needs per-client settings
and a process-global would be a footgun in a library.

Usage::

    from route4me.config import Route4MeConfig

    Route4MeConfig.timeout = (3.05, 60.0)   # slow optimizations
    Route4MeConfig.redact_urls = False      # debugging only -- see the warning
"""


#: Sentinel for "the caller did not supply this", so that an explicit ``None``
#: can carry its own meaning (for ``timeout``, "wait forever").
class _Unset:
    __slots__ = ()

    def __repr__(self):
        return "UNSET"

    def __bool__(self):
        return False


UNSET = _Unset()

#: ``(connect, read)`` in seconds.
#:
#: ``read = 30.0`` matches the C# SDK's ``Route4MeConfig.HttpTimeout``, so both
#: clients behave the same.
#:
#: ``connect = 6.05`` clears two Linux TCP SYN retransmits (1s + 2s + 3s) with
#: the small offset the ``requests`` docs recommend, so the deadline never lands
#: exactly on a retransmit boundary. A single 30s scalar would make a
#: blackholed SYN cost 30 seconds instead of 6.
#:
#: A tuple rather than a scalar because the two failure modes differ: a dead
#: host should fail fast, while a running optimization legitimately takes 20s.
DEFAULT_TIMEOUT = (6.05, 30.0)


class Route4MeConfig:
    """Global defaults. Assign to the class attributes to change them."""

    #: Default request timeout. ``None`` disables timeouts entirely (the
    #: pre-0.2.0 behaviour), which risks hanging the calling thread forever.
    timeout = DEFAULT_TIMEOUT

    #: When True (the default), credentials are stripped from URLs before they
    #: are stored on :class:`route4me.exceptions.APIException`.
    #:
    #: .. warning::
    #:    Setting this False puts the plaintext API key back into every
    #:    traceback, log line and error report -- including anything forwarded
    #:    to Sentry, Datadog or a similar service, which serialise exception
    #:    attributes by default. Turn it on deliberately, for local debugging,
    #:    and turn it back off.
    redact_urls = True


def normalize_timeout(value):
    """Validate and normalise a timeout into something ``requests`` accepts.

    Accepted forms:

    * ``None`` -- no timeout (explicit, greppable opt-out)
    * a number -- applied to both the connect and read phases
    * a 2-sequence -- ``(connect, read)``

    :raise ValueError: on any other shape, rather than letting ``requests``
        fail later with a less obvious message.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value <= 0:
            raise ValueError(f"timeout must be positive, got {value!r}")
        return float(value)
    if isinstance(value, (tuple, list)):
        if len(value) != 2:
            raise ValueError(f"a timeout sequence must be (connect, read), got {value!r}")
        connect, read = value
        for part in (connect, read):
            if not isinstance(part, (int, float)) or isinstance(part, bool) or part <= 0:
                raise ValueError(f"timeout components must be positive numbers, got {value!r}")
        return (float(connect), float(read))
    raise ValueError(f"timeout must be None, a number, or a (connect, read) pair; got {value!r}")


def resolve_timeout(*candidates):
    """Return the first candidate that is not :data:`UNSET`, normalised.

    Falls back to :attr:`Route4MeConfig.timeout`, then to
    :data:`DEFAULT_TIMEOUT` if someone has set the global to ``UNSET``.
    """
    for candidate in candidates:
        if candidate is not UNSET:
            return normalize_timeout(candidate)
    if Route4MeConfig.timeout is not UNSET:
        return normalize_timeout(Route4MeConfig.timeout)
    return DEFAULT_TIMEOUT
