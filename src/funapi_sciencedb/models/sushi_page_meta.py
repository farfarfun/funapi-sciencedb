from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SUSHIPageMeta")


@_attrs_define
class SUSHIPageMeta:
    """报告的分页包装结构

    属性：
        page (Unset | int): 页码。 示例为 1.
        total (Unset | int): 报告总数。 示例为 100.
        total_pages (Unset | int): 总页数。 示例为 10.
    """

    page: Unset | int = UNSET
    total: Unset | int = UNSET
    total_pages: Unset | int = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """将模型实例序列化为字典。

        参数：
            无。

        返回：
            dict[str, Any]: 包含已设置字段和额外属性的字典。
        """

        page = self.page

        total = self.total

        total_pages = self.total_pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page is not UNSET:
            field_dict["page"] = page
        if total is not UNSET:
            field_dict["total"] = total
        if total_pages is not UNSET:
            field_dict["totalPages"] = total_pages

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        """从字典反序列化为模型实例。

        参数：
            src_dict (dict[str, Any]): 待解析的字典。

        返回：
            T: 解析得到的模型实例。
        """

        d = src_dict.copy()
        page = d.pop("page", UNSET)

        total = d.pop("total", UNSET)

        total_pages = d.pop("totalPages", UNSET)

        sushi_page_meta = cls(
            page=page,
            total=total,
            total_pages=total_pages,
        )

        sushi_page_meta.additional_properties = d
        return sushi_page_meta

    @property
    def additional_keys(self) -> list[str]:
        """获取额外属性的键列表。

        参数：
            无。

        返回：
            list[str]: 额外属性的键列表。
        """

        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
