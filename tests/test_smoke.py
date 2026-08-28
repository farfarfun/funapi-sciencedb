"""Smoke tests for funapi-sciencedb (import name: funapi_sciencedb).

funapi-sciencedb is an auto-generated OpenAPI client (via openapi-python-client)
for the ScienceDB (scidb.cn) Open API. These tests only check that the client
constructs correctly and that its generated request functions behave as
expected when the underlying HTTP layer is mocked. No real network calls are
made against scidb.cn.
"""

from unittest.mock import MagicMock

import httpx
import pytest

from funapi_sciencedb import AuthenticatedClient, Client
from funapi_sciencedb.api.open_api_controller import harvest_using_get, search_using_get
from funapi_sciencedb.api.sushi_controller import get_api_status
from funapi_sciencedb.models.api_result_search_result import APIResultSearchResult
from funapi_sciencedb.types import UNSET


def test_import_top_level_package():
    """Importing the top-level package and its main symbols should succeed."""
    import funapi_sciencedb

    assert hasattr(funapi_sciencedb, "Client")
    assert hasattr(funapi_sciencedb, "AuthenticatedClient")


def test_client_construction():
    """Client can be constructed with a trivial base_url, no network call happens."""
    client = Client(base_url="https://example.invalid/open-api/v2")

    assert client is not None
    # Underlying httpx.Client is lazily constructed, not eagerly.
    assert client._client is None


def test_authenticated_client_construction():
    """AuthenticatedClient can be constructed with a fake token."""
    client = AuthenticatedClient(
        base_url="https://example.invalid/open-api/v2",
        token="fake-token",
    )

    assert client is not None
    assert client.token == "fake-token"
    assert client._client is None


def test_get_httpx_client_builds_without_network_call():
    """Building the underlying httpx.Client should not perform any I/O."""
    client = Client(base_url="https://example.invalid/open-api/v2")

    httpx_client = client.get_httpx_client()

    assert isinstance(httpx_client, httpx.Client)
    # Calling again should return the same cached instance.
    assert client.get_httpx_client() is httpx_client


def test_search_using_get_sync_with_mocked_http(monkeypatch):
    """search_using_get.sync() should parse a mocked HTTP response without
    ever touching the real scidb.cn API."""
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
    """sync_detailed() should return the full Response wrapper (status, headers, parsed)."""
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
    """A second representative *Api module (harvest) also avoids real network calls."""
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
    """sushi_controller.get_api_status parses a JSON list response into models."""
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
    """Non-200 responses are returned as None unless raise_on_unexpected_status is set."""
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


def test_real_credentials_not_available():
    """Hitting the real scidb.cn API requires network access / real credentials
    that are not available in this test environment."""
    pytest.skip("需要真实凭据/网络访问 scidb.cn，跳过")
