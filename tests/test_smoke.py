"""funapi-sciencedb（导入名 funapi_sciencedb）的冒烟测试。

本包是用 openapi-python-client 按 ScienceDB（scidb.cn）开放接口文档自动生成的客户端。
这些测试只验证客户端能正确构造，以及在 mock 掉底层 HTTP 之后生成的请求函数行为符合预期，
不会真的去访问 scidb.cn。
"""

import asyncio
import runpy
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock

import httpx
import pytest

from funapi_sciencedb import AuthenticatedClient, Client
from funapi_sciencedb.api.open_api_controller import (
    harvest_using_get,
    json_using_get,
    metrics_using_get,
    search_using_get,
)
from funapi_sciencedb.api.sushi_controller import (
    get_api_status,
    get_report_by_id_using_get,
    get_reports,
)
from funapi_sciencedb.models.api_result_metrics_result import APIResultMetricsResult
from funapi_sciencedb.models.api_result_search_result import APIResultSearchResult
from funapi_sciencedb.models.sushi_report import SUSHIReport
from funapi_sciencedb.models.sushi_report_page import SUSHIReportPage

ROOT = Path(__file__).resolve().parent.parent


def test_import_generate_has_no_side_effects(monkeypatch):
    """导入 generate 模块不应该触发网络请求或重新生成代码。"""
    calls = []

    requests = ModuleType("requests")
    requests.get = lambda *args, **kwargs: calls.append("request")
    convert = ModuleType("funapi.convert")
    convert.convert_openapi_v3 = lambda: calls.append("convert")
    generate = ModuleType("funapi.generate")
    generate.generate_api = lambda **kwargs: calls.append("generate")
    client = ModuleType("openapi_python_client")
    client.MetaType = SimpleNamespace(NONE=None)

    monkeypatch.setitem(sys.modules, "requests", requests)
    monkeypatch.setitem(sys.modules, "funapi", ModuleType("funapi"))
    monkeypatch.setitem(sys.modules, "funapi.convert", convert)
    monkeypatch.setitem(sys.modules, "funapi.generate", generate)
    monkeypatch.setitem(sys.modules, "openapi_python_client", client)

    runpy.run_path(str(ROOT / "generate.py"), run_name="generate")

    assert calls == []


def test_import_top_level_package():
    """导入顶层包及其主要符号应当成功。"""
    import funapi_sciencedb

    assert hasattr(funapi_sciencedb, "Client")
    assert hasattr(funapi_sciencedb, "AuthenticatedClient")


def test_client_construction():
    """只给一个 base_url 就能构造出 Client，过程中不发起网络请求。"""
    client = Client(base_url="https://example.invalid/open-api/v2")

    assert client is not None
    # 底层 httpx.Client 是惰性构造的，不会在这里就建好。
    assert client._client is None


def test_authenticated_client_construction():
    """用假 token 就能构造出 AuthenticatedClient。"""
    client = AuthenticatedClient(
        base_url="https://example.invalid/open-api/v2",
        token="fake-token",
    )

    assert client is not None
    assert client.token == "fake-token"
    assert client._client is None


def test_get_httpx_client_builds_without_network_call():
    """构造底层 httpx.Client 不应该产生任何 I/O。"""
    client = Client(base_url="https://example.invalid/open-api/v2")

    httpx_client = client.get_httpx_client()

    assert isinstance(httpx_client, httpx.Client)
    # 再调用一次应当拿到同一个缓存实例。
    assert client.get_httpx_client() is httpx_client


def test_search_using_get_sync_with_mocked_http(monkeypatch):
    """search_using_get.sync() 能解析 mock 出来的 HTTP 响应，且完全不碰真实接口。"""
    client = Client(base_url="https://example.invalid/open-api/v2")

    fake_response = httpx.Response(
        status_code=200,
        json={"code": 20000, "message": "ok"},
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/search"),
    )

    mock_request = MagicMock(return_value=fake_response)
    monkeypatch.setattr(client.get_httpx_client(), "request", mock_request)

    result = search_using_get.sync(client=client, page=1, size=10)

    mock_request.assert_called_once()
    called_kwargs = mock_request.call_args.kwargs
    assert called_kwargs["method"] == "get"
    assert called_kwargs["url"] == "/search"

    assert isinstance(result, APIResultSearchResult)
    assert result.code == 20000
    assert result.message == "ok"


def test_search_using_get_sync_detailed_returns_response_wrapper(monkeypatch):
    """sync_detailed() 返回完整的 Response 包装对象（状态码、响应头、解析结果）。"""
    client = Client(base_url="https://example.invalid/open-api/v2")

    fake_response = httpx.Response(
        status_code=200,
        json={},
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/search"),
    )
    monkeypatch.setattr(
        client.get_httpx_client(), "request", MagicMock(return_value=fake_response)
    )

    response = search_using_get.sync_detailed(client=client)

    assert response.status_code == 200
    assert isinstance(response.parsed, APIResultSearchResult)


def test_harvest_using_get_builds_expected_request_kwargs(monkeypatch):
    """再挑一个代表性接口模块（harvest）验证同样不会发起真实网络请求。"""
    client = Client(base_url="https://example.invalid/open-api/v2")

    fake_response = httpx.Response(
        status_code=200,
        json={},
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/harvest"),
    )
    mock_request = MagicMock(return_value=fake_response)
    monkeypatch.setattr(client.get_httpx_client(), "request", mock_request)

    harvest_using_get.sync(client=client)

    mock_request.assert_called_once()
    assert mock_request.call_args.kwargs["method"] == "get"


def test_get_api_status_parses_list_response(monkeypatch):
    """sushi_controller.get_api_status 能把 JSON 数组响应解析成模型列表。"""
    client = AuthenticatedClient(
        base_url="https://example.invalid/open-api/v2", token="fake-token"
    )

    fake_response = httpx.Response(
        status_code=200,
        json=[{"ServiceActive": True, "Description": "fake service"}],
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/status"),
    )
    monkeypatch.setattr(
        client.get_httpx_client(), "request", MagicMock(return_value=fake_response)
    )

    result = get_api_status.sync(client=client)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].service_active is True
    assert result[0].description == "fake service"


def test_search_using_get_unexpected_status_returns_none_by_default(monkeypatch):
    """没开 raise_on_unexpected_status 时，非 200 响应统一返回 None。"""
    client = Client(base_url="https://example.invalid/open-api/v2")

    fake_response = httpx.Response(
        status_code=500,
        json={"error": "boom"},
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/search"),
    )
    monkeypatch.setattr(
        client.get_httpx_client(), "request", MagicMock(return_value=fake_response)
    )

    result = search_using_get.sync(client=client)

    assert result is None


def test_metrics_using_get_sync_with_mocked_http(monkeypatch):
    """open_api_controller.metrics_using_get.sync() 能解析 mock 响应。"""
    client = Client(base_url="https://example.invalid/open-api/v2")

    fake_response = httpx.Response(
        status_code=200,
        json={"code": 20000, "message": "ok"},
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/metrics"),
    )
    mock_request = MagicMock(return_value=fake_response)
    monkeypatch.setattr(client.get_httpx_client(), "request", mock_request)

    result = metrics_using_get.sync(client=client, doi="10.11922/fake.doi")

    mock_request.assert_called_once()
    assert mock_request.call_args.kwargs["params"]["doi"] == "10.11922/fake.doi"
    assert isinstance(result, APIResultMetricsResult)
    assert result.code == 20000


def test_json_using_get_sync_returns_raw_string(monkeypatch):
    """open_api_controller.json_using_get.sync() 原样返回字符串形式的 JSON 响应体。"""
    client = Client(base_url="https://example.invalid/open-api/v2")

    fake_response = httpx.Response(
        status_code=200,
        json="raw-json-payload",
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/json"),
    )
    monkeypatch.setattr(
        client.get_httpx_client(), "request", MagicMock(return_value=fake_response)
    )

    result = json_using_get.sync(client=client, doi="10.11922/fake.doi")

    assert result == "raw-json-payload"


def test_json_using_get_unexpected_status_returns_none_by_default(monkeypatch):
    """没开 raise_on_unexpected_status 时，非 200 响应退化为 None。"""
    client = Client(base_url="https://example.invalid/open-api/v2")

    fake_response = httpx.Response(
        status_code=404,
        json={"error": "not found"},
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/json"),
    )
    monkeypatch.setattr(
        client.get_httpx_client(), "request", MagicMock(return_value=fake_response)
    )

    result = json_using_get.sync(client=client, doi="does-not-exist")

    assert result is None


def test_get_reports_sync_with_default_pagination(monkeypatch):
    """sushi_controller.get_reports.sync() 默认用 page[number]=1 / page[size]=10 分页。"""
    client = AuthenticatedClient(
        base_url="https://example.invalid/open-api/v2", token="fake-token"
    )

    fake_response = httpx.Response(
        status_code=200,
        json={"reports": [], "meta": {}},
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/reports"),
    )
    mock_request = MagicMock(return_value=fake_response)
    monkeypatch.setattr(client.get_httpx_client(), "request", mock_request)

    result = get_reports.sync(client=client)

    assert mock_request.call_args.kwargs["params"]["page[number]"] == 1
    assert mock_request.call_args.kwargs["params"]["page[size]"] == 10
    assert isinstance(result, SUSHIReportPage)


def test_get_report_by_id_using_get_sync_with_mocked_http(monkeypatch):
    """sushi_controller.get_report_by_id_using_get.sync() 会把报告 id 拼进请求路径。"""
    client = AuthenticatedClient(
        base_url="https://example.invalid/open-api/v2", token="fake-token"
    )

    fake_response = httpx.Response(
        status_code=200,
        json={"report": {}},
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/report/TR"),
    )
    mock_request = MagicMock(return_value=fake_response)
    monkeypatch.setattr(client.get_httpx_client(), "request", mock_request)

    result = get_report_by_id_using_get.sync(id="TR", client=client)

    assert mock_request.call_args.kwargs["url"] == "/report/TR"
    assert isinstance(result, SUSHIReport)


def test_get_report_by_id_using_get_empty_id_returns_none(monkeypatch):
    """非 200 响应（比如报告 id 不存在）退化为 None。"""
    client = AuthenticatedClient(
        base_url="https://example.invalid/open-api/v2", token="fake-token"
    )

    fake_response = httpx.Response(
        status_code=404,
        json={"error": "unknown report"},
        request=httpx.Request(
            "GET", "https://example.invalid/open-api/v2/report/does-not-exist"
        ),
    )
    monkeypatch.setattr(
        client.get_httpx_client(), "request", MagicMock(return_value=fake_response)
    )

    result = get_report_by_id_using_get.sync(id="does-not-exist", client=client)

    assert result is None


def test_search_using_get_asyncio_with_mocked_http(monkeypatch):
    """search_using_get.asyncio()（sync() 的异步版本）同样不会发起真实网络请求。

    仓库没有引入 pytest-asyncio 依赖，所以这里不写 ``async def`` 测试，
    直接用 ``asyncio.run`` 驱动协程。
    """
    client = Client(base_url="https://example.invalid/open-api/v2")

    fake_response = httpx.Response(
        status_code=200,
        json={"code": 20000, "message": "ok"},
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/search"),
    )

    async def fake_request(*args, **kwargs):
        return fake_response

    monkeypatch.setattr(client.get_async_httpx_client(), "request", fake_request)

    result = asyncio.run(search_using_get.asyncio(client=client, page=1, size=10))

    assert isinstance(result, APIResultSearchResult)
    assert result.code == 20000


def test_get_api_status_asyncio_detailed_returns_response_wrapper(monkeypatch):
    """异步路径下，get_api_status.asyncio_detailed() 同样返回完整的 Response 包装对象。"""
    client = AuthenticatedClient(
        base_url="https://example.invalid/open-api/v2", token="fake-token"
    )

    fake_response = httpx.Response(
        status_code=200,
        json=[{"ServiceActive": False, "Description": "maintenance"}],
        request=httpx.Request("GET", "https://example.invalid/open-api/v2/status"),
    )

    async def fake_request(*args, **kwargs):
        return fake_response

    monkeypatch.setattr(client.get_async_httpx_client(), "request", fake_request)

    response = asyncio.run(get_api_status.asyncio_detailed(client=client))

    assert response.status_code == 200
    assert response.parsed[0].service_active is False


def test_real_credentials_not_available():
    """访问真实 scidb.cn 接口需要网络和真实凭据，当前测试环境没有。"""
    pytest.skip("需要真实凭据/网络访问 scidb.cn，跳过")
