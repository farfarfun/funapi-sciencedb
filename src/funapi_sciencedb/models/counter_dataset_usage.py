from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.counter_dataset_usage_data_type import COUNTERDatasetUsageDataType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.counter_dataset_attributes import COUNTERDatasetAttributes
    from ..models.counter_dataset_contributors import COUNTERDatasetContributors
    from ..models.counter_dataset_dates import COUNTERDatasetDates
    from ..models.counter_dataset_identifiers import COUNTERDatasetIdentifiers
    from ..models.counter_dataset_performance import COUNTERDatasetPerformance
    from ..models.counter_publisher_identifiers import COUNTERPublisherIdentifiers


T = TypeVar("T", bound="COUNTERDatasetUsage")


@_attrs_define
class COUNTERDatasetUsage:
    """定义数据集报告中 Report_Datasets 的输出结构。

    属性：
        data_type (COUNTERDatasetUsageDataType): 所报告数据集的类型。 示例为 Dataset.
        dataset_title (str): 所报告数据集的名称。 示例为 Lake Erie Fish Community Data.
        performance (list['COUNTERDatasetPerformance']): 报告中该数据集对应的使用量数据
        platform (str): 平台名称 示例为 Science Data Bank.
        publisher (str): 数据集出版方名称 示例为 Science Data Bank.
        publisher_id (list['COUNTERPublisherIdentifiers']): 出版方的标识。
        dataset_attributes (Union[Unset, list['COUNTERDatasetAttributes']]): 与该数据集相关的其他属性。
        dataset_contributors (Union[Unset, list['COUNTERDatasetContributors']]): 数据集贡献者（即创建者）的标识。
        dataset_dates (Union[Unset, list['COUNTERDatasetDates']]): 与该数据集相关的出版日期或其他日期。
        dataset_id (Union[Unset, list['COUNTERDatasetIdentifiers']]): 报告中该数据集的标识
        yop (Unset | str): 出版年份，格式为 'yyyy'。未知填 '0001'，在印填 '9999'。 示例为 2010.
    """

    data_type: COUNTERDatasetUsageDataType
    dataset_title: str
    performance: list["COUNTERDatasetPerformance"]
    platform: str
    publisher: str
    publisher_id: list["COUNTERPublisherIdentifiers"]
    dataset_attributes: Unset | list["COUNTERDatasetAttributes"] = UNSET
    dataset_contributors: Unset | list["COUNTERDatasetContributors"] = UNSET
    dataset_dates: Unset | list["COUNTERDatasetDates"] = UNSET
    dataset_id: Unset | list["COUNTERDatasetIdentifiers"] = UNSET
    yop: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """将模型实例序列化为字典。

        参数：
            无。

        返回：
            dict[str, Any]: 包含已设置字段和额外属性的字典。
        """

        data_type = self.data_type.value

        dataset_title = self.dataset_title

        performance = []
        for performance_item_data in self.performance:
            performance_item = performance_item_data.to_dict()
            performance.append(performance_item)

        platform = self.platform

        publisher = self.publisher

        publisher_id = []
        for publisher_id_item_data in self.publisher_id:
            publisher_id_item = publisher_id_item_data.to_dict()
            publisher_id.append(publisher_id_item)

        dataset_attributes: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.dataset_attributes, Unset):
            dataset_attributes = []
            for dataset_attributes_item_data in self.dataset_attributes:
                dataset_attributes_item = dataset_attributes_item_data.to_dict()
                dataset_attributes.append(dataset_attributes_item)

        dataset_contributors: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.dataset_contributors, Unset):
            dataset_contributors = []
            for dataset_contributors_item_data in self.dataset_contributors:
                dataset_contributors_item = dataset_contributors_item_data.to_dict()
                dataset_contributors.append(dataset_contributors_item)

        dataset_dates: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.dataset_dates, Unset):
            dataset_dates = []
            for dataset_dates_item_data in self.dataset_dates:
                dataset_dates_item = dataset_dates_item_data.to_dict()
                dataset_dates.append(dataset_dates_item)

        dataset_id: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.dataset_id, Unset):
            dataset_id = []
            for dataset_id_item_data in self.dataset_id:
                dataset_id_item = dataset_id_item_data.to_dict()
                dataset_id.append(dataset_id_item)

        yop = self.yop

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data-type": data_type,
                "dataset-title": dataset_title,
                "performance": performance,
                "platform": platform,
                "publisher": publisher,
                "publisher-id": publisher_id,
            }
        )
        if dataset_attributes is not UNSET:
            field_dict["dataset-attributes"] = dataset_attributes
        if dataset_contributors is not UNSET:
            field_dict["dataset-contributors"] = dataset_contributors
        if dataset_dates is not UNSET:
            field_dict["dataset-dates"] = dataset_dates
        if dataset_id is not UNSET:
            field_dict["dataset-id"] = dataset_id
        if yop is not UNSET:
            field_dict["yop"] = yop

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        """从字典反序列化为模型实例。

        参数：
            src_dict (dict[str, Any]): 待解析的字典。

        返回：
            T: 解析得到的模型实例。
        """

        from ..models.counter_dataset_attributes import COUNTERDatasetAttributes
        from ..models.counter_dataset_contributors import COUNTERDatasetContributors
        from ..models.counter_dataset_dates import COUNTERDatasetDates
        from ..models.counter_dataset_identifiers import COUNTERDatasetIdentifiers
        from ..models.counter_dataset_performance import COUNTERDatasetPerformance
        from ..models.counter_publisher_identifiers import COUNTERPublisherIdentifiers

        d = src_dict.copy()
        data_type = COUNTERDatasetUsageDataType(d.pop("data-type"))

        dataset_title = d.pop("dataset-title")

        performance = []
        _performance = d.pop("performance")
        for performance_item_data in _performance:
            performance_item = COUNTERDatasetPerformance.from_dict(
                performance_item_data
            )

            performance.append(performance_item)

        platform = d.pop("platform")

        publisher = d.pop("publisher")

        publisher_id = []
        _publisher_id = d.pop("publisher-id")
        for publisher_id_item_data in _publisher_id:
            publisher_id_item = COUNTERPublisherIdentifiers.from_dict(
                publisher_id_item_data
            )

            publisher_id.append(publisher_id_item)

        dataset_attributes = []
        _dataset_attributes = d.pop("dataset-attributes", UNSET)
        for dataset_attributes_item_data in _dataset_attributes or []:
            dataset_attributes_item = COUNTERDatasetAttributes.from_dict(
                dataset_attributes_item_data
            )

            dataset_attributes.append(dataset_attributes_item)

        dataset_contributors = []
        _dataset_contributors = d.pop("dataset-contributors", UNSET)
        for dataset_contributors_item_data in _dataset_contributors or []:
            dataset_contributors_item = COUNTERDatasetContributors.from_dict(
                dataset_contributors_item_data
            )

            dataset_contributors.append(dataset_contributors_item)

        dataset_dates = []
        _dataset_dates = d.pop("dataset-dates", UNSET)
        for dataset_dates_item_data in _dataset_dates or []:
            dataset_dates_item = COUNTERDatasetDates.from_dict(dataset_dates_item_data)

            dataset_dates.append(dataset_dates_item)

        dataset_id = []
        _dataset_id = d.pop("dataset-id", UNSET)
        for dataset_id_item_data in _dataset_id or []:
            dataset_id_item = COUNTERDatasetIdentifiers.from_dict(dataset_id_item_data)

            dataset_id.append(dataset_id_item)

        yop = d.pop("yop", UNSET)

        counter_dataset_usage = cls(
            data_type=data_type,
            dataset_title=dataset_title,
            performance=performance,
            platform=platform,
            publisher=publisher,
            publisher_id=publisher_id,
            dataset_attributes=dataset_attributes,
            dataset_contributors=dataset_contributors,
            dataset_dates=dataset_dates,
            dataset_id=dataset_id,
            yop=yop,
        )

        counter_dataset_usage.additional_properties = d
        return counter_dataset_usage

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
