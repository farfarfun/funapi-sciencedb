"""模型属性用到的公共类型。"""

from collections.abc import MutableMapping
from http import HTTPStatus
from typing import (
    BinaryIO,
    Generic,
    Literal,
    TypeVar,
)

from attrs import define


class Unset:
    def __bool__(self) -> Literal[False]:
        return False


UNSET: Unset = Unset()

FileJsonType = tuple[str | None, BinaryIO, str | None]


@define
class File:
    """文件上传所需的信息。"""

    payload: BinaryIO
    file_name: str | None = None
    mime_type: str | None = None

    def to_tuple(self) -> FileJsonType:
        """返回 httpx 能用于 multipart/form-data 的元组表示"""
        return self.file_name, self.payload, self.mime_type


T = TypeVar("T")


@define
class Response(Generic[T]):
    """接口返回的响应。"""

    status_code: HTTPStatus
    content: bytes
    headers: MutableMapping[str, str]
    parsed: T | None


__all__ = ["UNSET", "File", "FileJsonType", "Response", "Unset"]
