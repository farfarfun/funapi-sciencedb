from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sushi_service_status import SUSHIServiceStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    platform: Unset | str = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["platform"] = platform

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/status",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list["SUSHIServiceStatus"] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SUSHIServiceStatus.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list["SUSHIServiceStatus"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    platform: Unset | str = UNSET,
) -> Response[list["SUSHIServiceStatus"]]:
    """获取 API 服务状态

     返回该 API 所支持的报告服务的当前状态。

    参数：
        platform (Unset | str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        Response[list['SUSHIServiceStatus']]
    """

    kwargs = _get_kwargs(
        platform=platform,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    platform: Unset | str = UNSET,
) -> list["SUSHIServiceStatus"] | None:
    """获取 API 服务状态

     返回该 API 所支持的报告服务的当前状态。

    参数：
        platform (Unset | str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        list['SUSHIServiceStatus']
    """

    return sync_detailed(
        client=client,
        platform=platform,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    platform: Unset | str = UNSET,
) -> Response[list["SUSHIServiceStatus"]]:
    """获取 API 服务状态

     返回该 API 所支持的报告服务的当前状态。

    参数：
        platform (Unset | str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        Response[list['SUSHIServiceStatus']]
    """

    kwargs = _get_kwargs(
        platform=platform,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    platform: Unset | str = UNSET,
) -> list["SUSHIServiceStatus"] | None:
    """获取 API 服务状态

     返回该 API 所支持的报告服务的当前状态。

    参数：
        platform (Unset | str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        list['SUSHIServiceStatus']
    """

    return (
        await asyncio_detailed(
            client=client,
            platform=platform,
        )
    ).parsed
