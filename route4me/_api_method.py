from .exceptions import APIException, ParamValueException


def make_request(resource, endpoint, method, params, required=None, body=None, body_key="json"):
    """
    Shared CRUD helper. Validates required params, makes request, handles errors.
    Returns response.json() or error dict.
    """
    # Required params are always validated against `params`. The previous
    # `params if body is None else params` ternary had identical branches --
    # a leftover from a refactor that intended to validate against `body` in
    # the body case. Callers that need body validation do it before calling.
    if required and not resource.check_required_params(params, required):
        raise ParamValueException("params", "Params are not complete")
    request_fn = getattr(resource.api, f"_request_{method}")
    try:
        kwargs = {}
        if body is not None:
            kwargs[body_key] = body
        resource.response = resource.api._make_request(endpoint, params, request_fn, **kwargs)
        return resource.response.json()
    except APIException as e:
        return e.to_dict()
