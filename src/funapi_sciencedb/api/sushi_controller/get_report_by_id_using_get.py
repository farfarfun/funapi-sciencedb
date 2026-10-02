from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sushi_report import SUSHIReport
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    publisher: Unset | str = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["publisher"] = publisher

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/report/{id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> SUSHIReport | None:
    if response.status_code == 200:
        response_200 = SUSHIReport.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[SUSHIReport]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    publisher: Unset | str = UNSET,
) -> Response[SUSHIReport]:
    """按 id 返回 COUNTER 数据集报告

    参数：
        id (str):
        publisher (Unset | str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        Response[SUSHIReport]
    """

    kwargs = _get_kwargs(
        id=id,
        publisher=publisher,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    publisher: Unset | str = UNSET,
) -> SUSHIReport | None:
    """按 id 返回 COUNTER 数据集报告

    参数：
        id (str):
        publisher (Unset | str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        SUSHIReport
    """

    return sync_detailed(
        id=id,
        client=client,
        publisher=publisher,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    publisher: Unset | str = UNSET,
) -> Response[SUSHIReport]:
    """按 id 返回 COUNTER 数据集报告

    参数：
        id (str):
        publisher (Unset | str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        Response[SUSHIReport]
    """

    kwargs = _get_kwargs(
        id=id,
        publisher=publisher,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    publisher: Unset | str = UNSET,
) -> SUSHIReport | None:
    """按 id 返回 COUNTER 数据集报告

    参数：
        id (str):
        publisher (Unset | str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        SUSHIReport
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            publisher=publisher,
        )
    ).parsed
