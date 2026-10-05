from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sushi_page_meta import SUSHIPageMeta
    from ..models.sushi_report_list import SUSHIReportList


T = TypeVar("T", bound="SUSHIReportPage")


@_attrs_define
class SUSHIReportPage:
    """报告的分页包装结构

    属性：
        reports (Union[Unset, list['SUSHIReportList']]): 报告列表
        meta (Union[Unset, SUSHIPageMeta]): 报告的分页包装结构
    """

    reports: Unset | list["SUSHIReportList"] = UNSET
    meta: Union[Unset, "SUSHIPageMeta"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """将模型实例序列化为字典。

        参数：
            无。

        返回：
            dict[str, Any]: 包含已设置字段和额外属性的字典。
        """

        reports: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.reports, Unset):
            reports = []
            for reports_item_data in self.reports:
                reports_item = reports_item_data.to_dict()
                reports.append(reports_item)

        meta: Unset | dict[str, Any] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reports is not UNSET:
            field_dict["reports"] = reports
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        """从字典反序列化为模型实例。

        参数：
            src_dict (dict[str, Any]): 待解析的字典。

        返回：
            T: 解析得到的模型实例。
        """

        from ..models.sushi_page_meta import SUSHIPageMeta
        from ..models.sushi_report_list import SUSHIReportList

        d = src_dict.copy()
        reports = []
        _reports = d.pop("reports", UNSET)
        for reports_item_data in _reports or []:
            reports_item = SUSHIReportList.from_dict(reports_item_data)

            reports.append(reports_item)

        _meta = d.pop("meta", UNSET)
        meta: Unset | SUSHIPageMeta
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = SUSHIPageMeta.from_dict(_meta)

        sushi_report_page = cls(
            reports=reports,
            meta=meta,
        )

        sushi_report_page.additional_properties = d
        return sushi_report_page

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
