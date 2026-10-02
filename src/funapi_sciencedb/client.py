import ssl
from typing import Any

import httpx
from attrs import define, evolve, field


@define
class Client:
    """用于保存 API 相关数据的客户端。

    下列参数以关键字参数传入，用于在内部构造 httpx 客户端：

        ``base_url``：API 的基础 URL，所有请求都使用相对于它的路径。

        ``cookies``：每个请求都会带上的 cookie 字典。

        ``headers``：每个请求都会带上的请求头字典。

        ``timeout``：单个请求允许的最长耗时，超过后 API 函数会抛出 httpx.TimeoutException。

        ``verify_ssl``：是否校验 API 服务端的 SSL 证书。生产环境应为 True，仅测试时可以设为 False。

        ``follow_redirects``：是否跟随重定向，默认为 False。

        ``httpx_args``：传给 ``httpx.Client`` 与 ``httpx.AsyncClient`` 构造函数的额外参数字典。


    属性：
        raise_on_unexpected_status：当 API 返回的状态码没有写在源 OpenAPI 文档里时，是否抛出 errors.UnexpectedStatus。也可以作为关键字参数传给构造函数。
    """

    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str = field(alias="base_url")
    _cookies: dict[str, str] = field(factory=dict, kw_only=True, alias="cookies")
    _headers: dict[str, str] = field(factory=dict, kw_only=True, alias="headers")
    _timeout: httpx.Timeout | None = field(default=None, kw_only=True, alias="timeout")
    _verify_ssl: str | bool | ssl.SSLContext = field(
        default=True, kw_only=True, alias="verify_ssl"
    )
    _follow_redirects: bool = field(
        default=False, kw_only=True, alias="follow_redirects"
    )
    _httpx_args: dict[str, Any] = field(factory=dict, kw_only=True, alias="httpx_args")
    _client: httpx.Client | None = field(default=None, init=False)
    _async_client: httpx.AsyncClient | None = field(default=None, init=False)

    def with_headers(self, headers: dict[str, str]) -> "Client":
        """返回一个与当前客户端一致、但追加了请求头的新客户端"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return evolve(self, headers={**self._headers, **headers})

    def with_cookies(self, cookies: dict[str, str]) -> "Client":
        """返回一个与当前客户端一致、但追加了 cookie 的新客户端"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return evolve(self, cookies={**self._cookies, **cookies})

    def with_timeout(self, timeout: httpx.Timeout) -> "Client":
        """返回一个与当前客户端一致、但使用新超时时间（秒）的新客户端"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return evolve(self, timeout=timeout)

    def set_httpx_client(self, client: httpx.Client) -> "Client":
        """手动设置底层的 httpx.Client

        **注意**：这会覆盖客户端上的其他设置，包括 cookies、headers 和 timeout。
        """
        self._client = client
        return self

    def get_httpx_client(self) -> httpx.Client:
        """获取底层的 httpx.Client，没有设置过就新建一个"""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._client

    def __enter__(self) -> "Client":
        """进入 self.client 的上下文管理器，不能重复进入（见 httpx 文档）"""
        self.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: object, **kwargs: Any) -> None:
        """退出内部 httpx.Client 的上下文管理器（见 httpx 文档）"""
        self.get_httpx_client().__exit__(*args, **kwargs)

    def set_async_httpx_client(self, async_client: httpx.AsyncClient) -> "Client":
        """手动设置底层的 httpx.AsyncClient

        **注意**：这会覆盖客户端上的其他设置，包括 cookies、headers 和 timeout。
        """
        self._async_client = async_client
        return self

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """获取底层的 httpx.AsyncClient，没有设置过就新建一个"""
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._async_client

    async def __aenter__(self) -> "Client":
        """进入底层 httpx.AsyncClient 的上下文管理器，不能重复进入（见 httpx 文档）"""
        await self.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: object, **kwargs: Any) -> None:
        """退出底层 httpx.AsyncClient 的上下文管理器（见 httpx 文档）"""
        await self.get_async_httpx_client().__aexit__(*args, **kwargs)


@define
class AuthenticatedClient:
    """已完成认证、可以访问受保护端点的客户端。

    下列参数以关键字参数传入，用于在内部构造 httpx 客户端：

        ``base_url``：API 的基础 URL，所有请求都使用相对于它的路径。

        ``cookies``：每个请求都会带上的 cookie 字典。

        ``headers``：每个请求都会带上的请求头字典。

        ``timeout``：单个请求允许的最长耗时，超过后 API 函数会抛出 httpx.TimeoutException。

        ``verify_ssl``：是否校验 API 服务端的 SSL 证书。生产环境应为 True，仅测试时可以设为 False。

        ``follow_redirects``：是否跟随重定向，默认为 False。

        ``httpx_args``：传给 ``httpx.Client`` 与 ``httpx.AsyncClient`` 构造函数的额外参数字典。


    属性：
        raise_on_unexpected_status：当 API 返回的状态码没有写在源 OpenAPI 文档里时，是否抛出 errors.UnexpectedStatus。也可以作为关键字参数传给构造函数。
        token：用于认证的令牌。
        prefix：认证请求头里令牌的前缀。
        auth_header_name：认证请求头的名称。
    """

    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str = field(alias="base_url")
    _cookies: dict[str, str] = field(factory=dict, kw_only=True, alias="cookies")
    _headers: dict[str, str] = field(factory=dict, kw_only=True, alias="headers")
    _timeout: httpx.Timeout | None = field(default=None, kw_only=True, alias="timeout")
    _verify_ssl: str | bool | ssl.SSLContext = field(
        default=True, kw_only=True, alias="verify_ssl"
    )
    _follow_redirects: bool = field(
        default=False, kw_only=True, alias="follow_redirects"
    )
    _httpx_args: dict[str, Any] = field(factory=dict, kw_only=True, alias="httpx_args")
    _client: httpx.Client | None = field(default=None, init=False)
    _async_client: httpx.AsyncClient | None = field(default=None, init=False)

    token: str
    prefix: str = "Bearer"
    auth_header_name: str = "Authorization"

    def with_headers(self, headers: dict[str, str]) -> "AuthenticatedClient":
        """返回一个与当前客户端一致、但追加了请求头的新客户端"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return evolve(self, headers={**self._headers, **headers})

    def with_cookies(self, cookies: dict[str, str]) -> "AuthenticatedClient":
        """返回一个与当前客户端一致、但追加了 cookie 的新客户端"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return evolve(self, cookies={**self._cookies, **cookies})

    def with_timeout(self, timeout: httpx.Timeout) -> "AuthenticatedClient":
        """返回一个与当前客户端一致、但使用新超时时间（秒）的新客户端"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return evolve(self, timeout=timeout)

    def set_httpx_client(self, client: httpx.Client) -> "AuthenticatedClient":
        """手动设置底层的 httpx.Client

        **注意**：这会覆盖客户端上的其他设置，包括 cookies、headers 和 timeout。
        """
        self._client = client
        return self

    def get_httpx_client(self) -> httpx.Client:
        """获取底层的 httpx.Client，没有设置过就新建一个"""
        if self._client is None:
            self._headers[self.auth_header_name] = (
                f"{self.prefix} {self.token}" if self.prefix else self.token
            )
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._client

    def __enter__(self) -> "AuthenticatedClient":
        """进入 self.client 的上下文管理器，不能重复进入（见 httpx 文档）"""
        self.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: object, **kwargs: Any) -> None:
        """退出内部 httpx.Client 的上下文管理器（见 httpx 文档）"""
        self.get_httpx_client().__exit__(*args, **kwargs)

    def set_async_httpx_client(
        self, async_client: httpx.AsyncClient
    ) -> "AuthenticatedClient":
        """手动设置底层的 httpx.AsyncClient

        **注意**：这会覆盖客户端上的其他设置，包括 cookies、headers 和 timeout。
        """
        self._async_client = async_client
        return self

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """获取底层的 httpx.AsyncClient，没有设置过就新建一个"""
        if self._async_client is None:
            self._headers[self.auth_header_name] = (
                f"{self.prefix} {self.token}" if self.prefix else self.token
            )
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._async_client

    async def __aenter__(self) -> "AuthenticatedClient":
        """进入底层 httpx.AsyncClient 的上下文管理器，不能重复进入（见 httpx 文档）"""
        await self.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: object, **kwargs: Any) -> None:
        """退出底层 httpx.AsyncClient 的上下文管理器（见 httpx 文档）"""
        await self.get_async_httpx_client().__aexit__(*args, **kwargs)
