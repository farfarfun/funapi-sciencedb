from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.counter_dataset_identifiers_type import COUNTERDatasetIdentifiersType

T = TypeVar("T", bound="COUNTERDatasetIdentifiers")


@_attrs_define
class COUNTERDatasetIdentifiers:
    """
    属性：
        type (COUNTERDatasetIdentifiersType):  示例为 doi.
        value (str): 数据集标识的值 示例为 0931-865.
    """

    type: COUNTERDatasetIdentifiersType
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """将模型实例序列化为字典。

        参数：
            无。

        返回：
            dict[str, Any]: 包含已设置字段和额外属性的字典。
        """

        type = self.type.value

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "value": value,
            }
        )

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
        type = COUNTERDatasetIdentifiersType(d.pop("type"))

        value = d.pop("value")

        counter_dataset_identifiers = cls(
            type=type,
            value=value,
        )

        counter_dataset_identifiers.additional_properties = d
        return counter_dataset_identifiers

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
