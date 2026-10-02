from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_metrics_result import APIResultMetricsResult
from ...types import UNSET, Response


def _get_kwargs(
    *,
    doi: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["doi"] = doi

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/metrics",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> APIResultMetricsResult | None:
    if response.status_code == 200:
        response_200 = APIResultMetricsResult.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[APIResultMetricsResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    doi: str,
) -> Response[APIResultMetricsResult]:
    """按 DOI 查询数据集的统计指标

     按 DOI 查询数据集的统计指标

    参数：
        doi (str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        Response[APIResultMetricsResult]
    """

    kwargs = _get_kwargs(
        doi=doi,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    doi: str,
) -> APIResultMetricsResult | None:
    """按 DOI 查询数据集的统计指标

     按 DOI 查询数据集的统计指标

    参数：
        doi (str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        APIResultMetricsResult
    """

    return sync_detailed(
        client=client,
        doi=doi,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    doi: str,
) -> Response[APIResultMetricsResult]:
    """按 DOI 查询数据集的统计指标

     按 DOI 查询数据集的统计指标

    参数：
        doi (str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        Response[APIResultMetricsResult]
    """

    kwargs = _get_kwargs(
        doi=doi,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    doi: str,
) -> APIResultMetricsResult | None:
    """按 DOI 查询数据集的统计指标

     按 DOI 查询数据集的统计指标

    参数：
        doi (str):

    抛出：
        errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。
        httpx.TimeoutException：请求耗时超过 Client.timeout。

    返回：
        APIResultMetricsResult
    """

    return (
        await asyncio_detailed(
            client=client,
            doi=doi,
        )
    ).parsed
