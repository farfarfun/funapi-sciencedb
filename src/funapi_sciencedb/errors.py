"""API 函数可能抛出的公共异常类型。"""


class UnexpectedStatus(Exception):
    """当响应状态码没有写在文档里、且 Client.raise_on_unexpected_status 为 True 时，由 API 函数抛出。"""

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content

        super().__init__(
            f"Unexpected status code: {status_code}\n\nResponse content:\n{content.decode(errors='ignore')}"
        )


__all__ = ["UnexpectedStatus"]
