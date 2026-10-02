"""访问 ScienceDB 开放接口（ScienceDB API Doc）的客户端库。"""

from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
