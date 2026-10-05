from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.counter_dataset_usage import COUNTERDatasetUsage
    from ..models.sushi_report_header import SUSHIReportHeader


T = TypeVar("T", bound="COUNTERDatasetReport")


@_attrs_define
class COUNTERDatasetReport:
    """描述 COUNTER 数据集报告的组织形式。响应可以包含 Report_Header（可选）与 Report_Datasets（使用量统计）。

    属性：
        id (Unset | str): 报告 id。
        report_header (Union[Unset, SUSHIReportHeader]): 通用报告头，描述所请求的报告、请求方、客户、生效的过滤条件、生效的 reportAttributes 以及出现的异常。
        report_datasets (Union[Unset, list['COUNTERDatasetUsage']]): 数据集列表。
    """

    id: Unset | str = UNSET
    report_header: Union[Unset, "SUSHIReportHeader"] = UNSET
    report_datasets: Unset | list["COUNTERDatasetUsage"] = UNSET
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

        report_datasets: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.report_datasets, Unset):
            report_datasets = []
            for report_datasets_item_data in self.report_datasets:
                report_datasets_item = report_datasets_item_data.to_dict()
                report_datasets.append(report_datasets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if report_header is not UNSET:
            field_dict["report-header"] = report_header
        if report_datasets is not UNSET:
            field_dict["report-datasets"] = report_datasets

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        """从字典反序列化为模型实例。

        参数：
            src_dict (dict[str, Any]): 待解析的字典。

        返回：
            T: 解析得到的模型实例。
        """

        from ..models.counter_dataset_usage import COUNTERDatasetUsage
        from ..models.sushi_report_header import SUSHIReportHeader

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _report_header = d.pop("report-header", UNSET)
        report_header: Unset | SUSHIReportHeader
        if isinstance(_report_header, Unset):
            report_header = UNSET
        else:
            report_header = SUSHIReportHeader.from_dict(_report_header)

        report_datasets = []
        _report_datasets = d.pop("report-datasets", UNSET)
        for report_datasets_item_data in _report_datasets or []:
            report_datasets_item = COUNTERDatasetUsage.from_dict(
                report_datasets_item_data
            )

            report_datasets.append(report_datasets_item)

        counter_dataset_report = cls(
            id=id,
            report_header=report_header,
            report_datasets=report_datasets,
        )

        counter_dataset_report.additional_properties = d
        return counter_dataset_report

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
