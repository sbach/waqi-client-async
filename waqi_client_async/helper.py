""" Waqi-client-async helper functions."""

from typing import Any, Dict

from .exceptions import (
    APIError,
    InvalidToken,
    OverQuota,
    UnknownCity,
    UnknownID,
)


def assert_valid(result: Dict[str, Any]) -> None:
    "Helper function for error-handling."
    if (status := result.get("status")) is not None:
        if status == "ok":
            if (data := result.get("data")) is not None:
                # data = []
                if not data:
                    raise UnknownCity()
                if data.get("msg") == "Unknown ID":
                    raise UnknownID()
                return

            # no data in result:
            raise APIError(result)

        if status == "error":
            if (data := result.get("data")) is not None:
                if data == "Invalid key":
                    raise InvalidToken()
                if data == "Over quota":
                    raise OverQuota()
                # unknown data for status = error
                raise APIError(data)

        # unknown status in result
        raise APIError(status)

    # no status in result, look for specific feed-search error
    obs_list: list[Dict[str, str]] = result["rxs"]["obs"]
    if "Invalid key" in obs_list[0]["msg"]:
        raise InvalidToken()
