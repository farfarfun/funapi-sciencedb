from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sushi_report_header import SUSHIReportHeader


T = TypeVar("T", bound="SUSHIReportList")


@_attrs_define
class SUSHIReportList:
    """报告的列表包装结构

    属性：
        id (Unset | str): 报告 id。 示例为 sciencedb-2022-01.
        report_header (Union[Unset, SUSHIReportHeader]): 通用报告头，描述所请求的报告、请求方、客户、生效的过滤条件、生效的 reportAttributes 以及出现的异常。
    """

    id: Unset | str = UNSET
    report_header: Union[Unset, "SUSHIReportHeader"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """将模型实例序列化为字典。

        参数：
            无。

        返回：
            dict[str, Any]: 包含已设置字段和额外属性的字典。
        """

        id = self.id

        report_header: Unset | dict[str, Any] = UNSET
        if not isinstance(self.report_header, Unset):
            report_header = self.report_header.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if report_header is not UNSET:
            field_dict["report-header"] = report_header

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        """从字典反序列化为模型实例。

        参数：
            src_dict (dict[str, Any]): 待解析的字典。

        返回：
            T: 解析得到的模型实例。
        """

        from ..models.sushi_report_header import SUSHIReportHeader

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _report_header = d.pop("report-header", UNSET)
        report_header: Unset | SUSHIReportHeader
        if isinstance(_report_header, Unset):
            report_header = UNSET
        else:
            report_header = SUSHIReportHeader.from_dict(_report_header)

        sushi_report_list = cls(
            id=id,
            report_header=report_header,
        )

        sushi_report_list.additional_properties = d
        return sushi_report_list

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
