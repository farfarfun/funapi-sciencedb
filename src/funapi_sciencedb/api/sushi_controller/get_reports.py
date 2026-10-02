from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sushi_report_page import SUSHIReportPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    pagenumber: Unset | int = 1,
    pagesize: Unset | int = 10,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page[number]"] = pagenumber

    params["page[size]"] = pagesize

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/reports",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> SUSHIReportPage | None:
    if response.status_code == 200:
        response_200 = SUSHIReportPage.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[SUSHIReportPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    pagenumber: Unset | int = 1,
    pagesize: Unset | int = 10,
) -> Response[SUSHIReportPage]:
    """获取报告列表

     返回该 API 为指定应用支持的报告列表。

    参数：
        pagenumber (Unset | int):  默认值为 1.
        pagesize (Unset | int):  默认值为 10.

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        Response[SUSHIReportPage]
    """

    kwargs = _get_kwargs(
        pagenumber=pagenumber,
        pagesize=pagesize,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    pagenumber: Unset | int = 1,
    pagesize: Unset | int = 10,
) -> SUSHIReportPage | None:
    """获取报告列表

     返回该 API 为指定应用支持的报告列表。

    参数：
        pagenumber (Unset | int):  默认值为 1.
        pagesize (Unset | int):  默认值为 10.

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        SUSHIReportPage
    """

    return sync_detailed(
        client=client,
        pagenumber=pagenumber,
        pagesize=pagesize,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    pagenumber: Unset | int = 1,
    pagesize: Unset | int = 10,
) -> Response[SUSHIReportPage]:
    """获取报告列表

     返回该 API 为指定应用支持的报告列表。

    参数：
        pagenumber (Unset | int):  默认值为 1.
        pagesize (Unset | int):  默认值为 10.

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        Response[SUSHIReportPage]
    """

    kwargs = _get_kwargs(
        pagenumber=pagenumber,
        pagesize=pagesize,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    pagenumber: Unset | int = 1,
    pagesize: Unset | int = 10,
) -> SUSHIReportPage | None:
    """获取报告列表

     返回该 API 为指定应用支持的报告列表。

    参数：
        pagenumber (Unset | int):  默认值为 1.
        pagesize (Unset | int):  默认值为 10.

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        SUSHIReportPage
    """

    return (
        await asyncio_detailed(
            client=client,
            pagenumber=pagenumber,
            pagesize=pagesize,
        )
    ).parsed
