from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_search_result import APIResultSearchResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Unset | int = 1,
    range_: Unset | int = UNSET,
    size: Unset | int = 10,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["range"] = range_

    params["size"] = size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIResultSearchResult | None:
    if response.status_code == 200:
        response_200 = APIResultSearchResult.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[APIResultSearchResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    page: Unset | int = 1,
    range_: Unset | int = UNSET,
    size: Unset | int = 10,
) -> Response[APIResultSearchResult]:
    """search dataset by page

     result is order by publish time desc

    Args:
        page (Unset | int):  Default: 1.
        range_ (Unset | int):
        size (Unset | int):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIResultSearchResult]
    """

    kwargs = _get_kwargs(
        page=page,
        range_=range_,
        size=size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    page: Unset | int = 1,
    range_: Unset | int = UNSET,
    size: Unset | int = 10,
) -> APIResultSearchResult | None:
    """search dataset by page

     result is order by publish time desc

    Args:
        page (Unset | int):  Default: 1.
        range_ (Unset | int):
        size (Unset | int):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIResultSearchResult
    """

    return sync_detailed(
        client=client,
        page=page,
        range_=range_,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    page: Unset | int = 1,
    range_: Unset | int = UNSET,
    size: Unset | int = 10,
) -> Response[APIResultSearchResult]:
    """search dataset by page

     result is order by publish time desc

    Args:
        page (Unset | int):  Default: 1.
        range_ (Unset | int):
        size (Unset | int):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[APIResultSearchResult]
    """

    kwargs = _get_kwargs(
        page=page,
        range_=range_,
        size=size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    page: Unset | int = 1,
    range_: Unset | int = UNSET,
    size: Unset | int = 10,
) -> APIResultSearchResult | None:
    """search dataset by page

     result is order by publish time desc

    Args:
        page (Unset | int):  Default: 1.
        range_ (Unset | int):
        size (Unset | int):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        APIResultSearchResult
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            range_=range_,
            size=size,
        )
    ).parsed
