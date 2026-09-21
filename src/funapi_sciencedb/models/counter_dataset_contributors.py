from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.counter_dataset_contributors_type import COUNTERDatasetContributorsType

T = TypeVar("T", bound="COUNTERDatasetContributors")


@_attrs_define
class COUNTERDatasetContributors:
    """
    Attributes:
        type (COUNTERDatasetContributorsType):  Example: name.
        value (str): Value of the contributor identifier Example: John Smith.
    """

    type: COUNTERDatasetContributorsType
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type = self.type.value

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "Value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        type = COUNTERDatasetContributorsType(d.pop("type"))

        value = d.pop("Value")

        counter_dataset_contributors = cls(
            type=type,
            value=value,
        )

        counter_dataset_contributors.additional_properties = d
        return counter_dataset_contributors

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
