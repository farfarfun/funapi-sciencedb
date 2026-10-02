from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_search_result import APIResultSearchResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    end_time: Unset | str = "2099-01-01",
    page: Unset | int = 1,
    size: Unset | int = 10,
    start_time: Unset | str = "1970-01-01",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["end_time"] = end_time

    params["page"] = page

    params["size"] = size

    params["start_time"] = start_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/harvest",
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
    end_time: Unset | str = "2099-01-01",
    page: Unset | int = 1,
    size: Unset | int = 10,
    start_time: Unset | str = "1970-01-01",
) -> Response[APIResultSearchResult]:
    """按数据集发布时间区间（start_time 与 end_time）批量获取数据集

     结果按发布时间降序排列

    参数：
        end_time (Unset | str):  默认值为 '2099-01-01'.
        page (Unset | int):  默认值为 1.
        size (Unset | int):  默认值为 10.
        start_time (Unset | str):  默认值为 '1970-01-01'.

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        Response[APIResultSearchResult]
    """

    kwargs = _get_kwargs(
        end_time=end_time,
        page=page,
        size=size,
        start_time=start_time,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    end_time: Unset | str = "2099-01-01",
    page: Unset | int = 1,
    size: Unset | int = 10,
    start_time: Unset | str = "1970-01-01",
) -> APIResultSearchResult | None:
    """按数据集发布时间区间（start_time 与 end_time）批量获取数据集

     结果按发布时间降序排列

    参数：
        end_time (Unset | str):  默认值为 '2099-01-01'.
        page (Unset | int):  默认值为 1.
        size (Unset | int):  默认值为 10.
        start_time (Unset | str):  默认值为 '1970-01-01'.

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        APIResultSearchResult
    """

    return sync_detailed(
        client=client,
        end_time=end_time,
        page=page,
        size=size,
        start_time=start_time,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    end_time: Unset | str = "2099-01-01",
    page: Unset | int = 1,
    size: Unset | int = 10,
    start_time: Unset | str = "1970-01-01",
) -> Response[APIResultSearchResult]:
    """按数据集发布时间区间（start_time 与 end_time）批量获取数据集

     结果按发布时间降序排列

    参数：
        end_time (Unset | str):  默认值为 '2099-01-01'.
        page (Unset | int):  默认值为 1.
        size (Unset | int):  默认值为 10.
        start_time (Unset | str):  默认值为 '1970-01-01'.

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        Response[APIResultSearchResult]
    """

    kwargs = _get_kwargs(
        end_time=end_time,
        page=page,
        size=size,
        start_time=start_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    end_time: Unset | str = "2099-01-01",
    page: Unset | int = 1,
    size: Unset | int = 10,
    start_time: Unset | str = "1970-01-01",
) -> APIResultSearchResult | None:
    """按数据集发布时间区间（start_time 与 end_time）批量获取数据集

     结果按发布时间降序排列

    参数：
        end_time (Unset | str):  默认值为 '2099-01-01'.
        page (Unset | int):  默认值为 1.
        size (Unset | int):  默认值为 10.
        start_time (Unset | str):  默认值为 '1970-01-01'.

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        APIResultSearchResult
    """

    return (
        await asyncio_detailed(
            client=client,
            end_time=end_time,
            page=page,
            size=size,
            start_time=start_time,
        )
    ).parsed
