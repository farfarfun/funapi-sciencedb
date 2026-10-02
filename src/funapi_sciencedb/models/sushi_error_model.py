from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sushi_error_model_severity import SUSHIErrorModelSeverity
from ..types import UNSET, Unset

T = TypeVar("T", bound="SUSHIErrorModel")


@_attrs_define
class SUSHIErrorModel:
    """错误与异常的通用表示结构。

    属性：
        code (int): 错误码，含义见错误码表。 示例为 3040.
        message (str): 错误的文字描述。 示例为 Partial Data Returned..
        severity (SUSHIErrorModelSeverity): 错误的严重级别。 示例为 Warning.
        data (Unset | str): 服务端提供的补充信息，用于进一步说明该错误。 示例为 Usage data has
            not been processed for all requested months..
        help_url (Unset | str): 描述错误详情的 URL。
    """

    code: int
    message: str
    severity: SUSHIErrorModelSeverity
    data: Unset | str = UNSET
    help_url: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        severity = self.severity.value

        data = self.data

        help_url = self.help_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Code": code,
                "Message": message,
                "Severity": severity,
            }
        )
        if data is not UNSET:
            field_dict["Data"] = data
        if help_url is not UNSET:
            field_dict["Help_URL"] = help_url

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("Code")

        message = d.pop("Message")

        severity = SUSHIErrorModelSeverity(d.pop("Severity"))

        data = d.pop("Data", UNSET)

        help_url = d.pop("Help_URL", UNSET)

        sushi_error_model = cls(
            code=code,
            message=message,
            severity=severity,
            data=data,
            help_url=help_url,
        )

        sushi_error_model.additional_properties = d
        return sushi_error_model

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
