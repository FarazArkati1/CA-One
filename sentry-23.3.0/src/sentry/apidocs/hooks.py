from typing import Any, Dict, Literal, Mapping, Set, TypedDict

from sentry.apidocs.build import OPENAPI_TAGS
from sentry.apidocs.utils import SentryApiBuildError

HTTP_METHODS_SET = Set[
    Literal["GET", "POST", "PUT", "OPTIONS", "HEAD", "DELETE", "TRACE", "CONNECT", "PATCH"]
]


class EndpointRegistryType(TypedDict):
    methods: HTTP_METHODS_SET


PUBLIC_ENDPOINTS: Dict[str, EndpointRegistryType] = {}


_DEFINED_TAG_SET = {t["name"] for t in OPENAPI_TAGS}

# path prefixes to exclude
# this is useful if we're duplicating an endpoint for legacy purposes
# but do not want to document it
EXCLUSION_PATH_PREFIXES = ["/api/0/monitors/"]


def custom_preprocessing_hook(endpoints: Any) -> Any:  # TODO: organize method, rename

    filtered = []
    for (path, path_regex, method, callback) in endpoints:

        if any(path.startswith(p) for p in EXCLUSION_PATH_PREFIXES):
            pass

        elif callback.view_class.public:
            # endpoints that are documented via tooling
            if method in callback.view_class.public:
                # only pass declared public methods of the endpoint
                # to the rest of the OpenAPI build pipeline
                filtered.append((path, path_regex, method, callback))

        else:
            # if an endpoint doesn't have any registered public methods, don't check it.
            pass

    return filtered


def custom_postprocessing_hook(result: Any, generator: Any, **kwargs: Any) -> Any:
    for path, endpoints in result["paths"].items():
        for method_info in endpoints.values():
            _check_tag(path, method_info)

            if method_info.get("description") is None:
                raise SentryApiBuildError(
                    "Please add a description to your endpoint method via a docstring"
                )

    return result


def _check_tag(path: str, method_info: Mapping[str, Any]) -> None:
    if method_info.get("tags") is None:
        raise SentryApiBuildError(
            f"Please add a single tag to {path}. The list of tags is defined at OPENAPI_TAGS in src/sentry/apidocs/build.py "
        )

    num_of_tags = len(method_info["tags"])

    if num_of_tags > 1:
        raise SentryApiBuildError(
            f"Please add only a single tag to {path}. Right now there are {num_of_tags}."
        )

    tag = method_info["tags"][0]

    if tag not in _DEFINED_TAG_SET:
        raise SentryApiBuildError(
            f"{tag} is not defined by OPENAPI_TAGS in src/sentry/apidocs/build.py. "
            "Please use a suitable tag or add a new one to OPENAPI_TAGS"
        )
