import datetime
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sushi_error_model import SUSHIErrorModel
    from ..models.sushi_report_header_report_attributes_item import (
        SUSHIReportHeaderReportAttributesItem,
    )
    from ..models.sushi_report_header_report_filters_item import (
        SUSHIReportHeaderReportFiltersItem,
    )


T = TypeVar("T", bound="SUSHIReportHeader")


@_attrs_define
class SUSHIReportHeader:
    """通用报告头，描述所请求的报告、请求方、客户、生效的过滤条件、生效的 reportAttributes 以及出现的异常。

    属性：
        release (str): 报告的发布版本。 示例为 RD1.
        report_id (str): 报告的 ID、代码或简称，通常与请求中 Report 参数传入的代码一致。 示例为 DSR.
        report_name (str): 报告的完整名称。 示例为 Dataset Report.
        created (Union[Unset, datetime.datetime]): 报告生成时间
        created_by (Unset | str): 生成该报告的机构名称。 示例为 Science Data Bank.
        exceptions (Union[Unset, list['SUSHIErrorModel']]): 生成报告过程中遇到的异常列表。
        report_attributes (Union[Unset, list['SUSHIReportHeaderReportAttributesItem']]): 作用于该报告的零个或多个附加属性，属性决定报告的明细程度。
        report_filters (Union[Unset, list['SUSHIReportHeaderReportFiltersItem']]): 该报告使用的零个或多个过滤条件，通常对应请求里传入的过滤条件，用于限定报告的数据范围。
    """

    release: str
    report_id: str
    report_name: str
    created: Unset | datetime.datetime = UNSET
    created_by: Unset | str = UNSET
    exceptions: Unset | list["SUSHIErrorModel"] = UNSET
    report_attributes: Unset | list["SUSHIReportHeaderReportAttributesItem"] = UNSET
    report_filters: Unset | list["SUSHIReportHeaderReportFiltersItem"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """将模型实例序列化为字典。

        参数：
            无。

        返回：
            dict[str, Any]: 包含已设置字段和额外属性的字典。
        """

        release = self.release

        report_id = self.report_id

        report_name = self.report_name

        created: Unset | str = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        created_by = self.created_by

        exceptions: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.exceptions, Unset):
            exceptions = []
            for exceptions_item_data in self.exceptions:
                exceptions_item = exceptions_item_data.to_dict()
                exceptions.append(exceptions_item)

        report_attributes: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.report_attributes, Unset):
            report_attributes = []
            for report_attributes_item_data in self.report_attributes:
                report_attributes_item = report_attributes_item_data.to_dict()
                report_attributes.append(report_attributes_item)

        report_filters: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.report_filters, Unset):
            report_filters = []
            for report_filters_item_data in self.report_filters:
                report_filters_item = report_filters_item_data.to_dict()
                report_filters.append(report_filters_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "release": release,
                "report-id": report_id,
                "report-name": report_name,
            }
        )
        if created is not UNSET:
            field_dict["created"] = created
        if created_by is not UNSET:
            field_dict["created-by"] = created_by
        if exceptions is not UNSET:
            field_dict["exceptions"] = exceptions
        if report_attributes is not UNSET:
            field_dict["report-attributes"] = report_attributes
        if report_filters is not UNSET:
            field_dict["report-filters"] = report_filters

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        """从字典反序列化为模型实例。

        参数：
            src_dict (dict[str, Any]): 待解析的字典。

        返回：
            T: 解析得到的模型实例。
        """

        from ..models.sushi_error_model import SUSHIErrorModel
        from ..models.sushi_report_header_report_attributes_item import (
            SUSHIReportHeaderReportAttributesItem,
        )
        from ..models.sushi_report_header_report_filters_item import (
            SUSHIReportHeaderReportFiltersItem,
        )

        d = src_dict.copy()
        release = d.pop("release")

        report_id = d.pop("report-id")

        report_name = d.pop("report-name")

        _created = d.pop("created", UNSET)
        created: Unset | datetime.datetime
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        created_by = d.pop("created-by", UNSET)

        exceptions = []
        _exceptions = d.pop("exceptions", UNSET)
        for exceptions_item_data in _exceptions or []:
            exceptions_item = SUSHIErrorModel.from_dict(exceptions_item_data)

            exceptions.append(exceptions_item)

        report_attributes = []
        _report_attributes = d.pop("report-attributes", UNSET)
        for report_attributes_item_data in _report_attributes or []:
            report_attributes_item = SUSHIReportHeaderReportAttributesItem.from_dict(
                report_attributes_item_data
            )

            report_attributes.append(report_attributes_item)

        report_filters = []
        _report_filters = d.pop("report-filters", UNSET)
        for report_filters_item_data in _report_filters or []:
            report_filters_item = SUSHIReportHeaderReportFiltersItem.from_dict(
                report_filters_item_data
            )

            report_filters.append(report_filters_item)

        sushi_report_header = cls(
            release=release,
            report_id=report_id,
            report_name=report_name,
            created=created,
            created_by=created_by,
            exceptions=exceptions,
            report_attributes=report_attributes,
            report_filters=report_filters,
        )

        sushi_report_header.additional_properties = d
        return sushi_report_header

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
