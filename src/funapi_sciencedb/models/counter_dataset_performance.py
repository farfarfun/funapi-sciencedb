from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.counter_dataset_instance import COUNTERDatasetInstance
    from ..models.counter_dataset_period import COUNTERDatasetPeriod


T = TypeVar("T", bound="COUNTERDatasetPerformance")


@_attrs_define
class COUNTERDatasetPerformance:
    """
    Attributes:
        instance (list['COUNTERDatasetInstance']):
        period (COUNTERDatasetPeriod):
    """

    instance: list["COUNTERDatasetInstance"]
    period: "COUNTERDatasetPeriod"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instance = []
        for instance_item_data in self.instance:
            instance_item = instance_item_data.to_dict()
            instance.append(instance_item)

        period = self.period.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "instance": instance,
                "period": period,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        from ..models.counter_dataset_instance import COUNTERDatasetInstance
        from ..models.counter_dataset_period import COUNTERDatasetPeriod

        d = src_dict.copy()
        instance = []
        _instance = d.pop("instance")
        for instance_item_data in _instance:
            instance_item = COUNTERDatasetInstance.from_dict(instance_item_data)

            instance.append(instance_item)

        period = COUNTERDatasetPeriod.from_dict(d.pop("period"))

        counter_dataset_performance = cls(
            instance=instance,
            period=period,
        )

        counter_dataset_performance.additional_properties = d
        return counter_dataset_performance

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
