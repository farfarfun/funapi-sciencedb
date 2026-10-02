from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.counter_dataset_instance_access_method import (
    COUNTERDatasetInstanceAccessMethod,
)
from ..models.counter_dataset_instance_metric_type import (
    COUNTERDatasetInstanceMetricType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="COUNTERDatasetInstance")


@_attrs_define
class COUNTERDatasetInstance:
    """
    属性：
        access_method (Union[Unset, COUNTERDatasetInstanceAccessMethod]): 标识该使用行为是 'Regular'（用户在内容站点上做研究的常规访问），还是 'Machine'（为文本与数据挖掘 TDM 抓取内容） 示例为 regular.
        count (Unset | int):
        metric_type (Union[Unset, COUNTERDatasetInstanceMetricType]):
    """

    access_method: Unset | COUNTERDatasetInstanceAccessMethod = UNSET
    count: Unset | int = UNSET
    metric_type: Unset | COUNTERDatasetInstanceMetricType = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_method: Unset | str = UNSET
        if not isinstance(self.access_method, Unset):
            access_method = self.access_method.value

        count = self.count

        metric_type: Unset | str = UNSET
        if not isinstance(self.metric_type, Unset):
            metric_type = self.metric_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if access_method is not UNSET:
            field_dict["access-method"] = access_method
        if count is not UNSET:
            field_dict["count"] = count
        if metric_type is not UNSET:
            field_dict["metric-type"] = metric_type

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _access_method = d.pop("access-method", UNSET)
        access_method: Unset | COUNTERDatasetInstanceAccessMethod
        if isinstance(_access_method, Unset):
            access_method = UNSET
        else:
            access_method = COUNTERDatasetInstanceAccessMethod(_access_method)

        count = d.pop("count", UNSET)

        _metric_type = d.pop("metric-type", UNSET)
        metric_type: Unset | COUNTERDatasetInstanceMetricType
        if isinstance(_metric_type, Unset):
            metric_type = UNSET
        else:
            metric_type = COUNTERDatasetInstanceMetricType(_metric_type)

        counter_dataset_instance = cls(
            access_method=access_method,
            count=count,
            metric_type=metric_type,
        )

        counter_dataset_instance.additional_properties = d
        return counter_dataset_instance

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
