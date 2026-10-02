from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sushi_service_status_alerts_item import SUSHIServiceStatusAlertsItem


T = TypeVar("T", bound="SUSHIServiceStatus")


@_attrs_define
class SUSHIServiceStatus:
    """
    属性：
        service_active (bool): 标识该服务当前是否可以提供报告。 示例为 True.
        alerts (Union[Unset, list['SUSHIServiceStatusAlertsItem']]): 与服务中断及状态相关的告警。
        description (Unset | str): 服务说明。 示例为 COUNTER Research Data Usage Reports for
            the UK Data Service - ReShare..
        note (Unset | str): 关于该服务的一般性说明。 示例为 A given customer can request a maximum of 5
            requests per day for a given report.
        registry_url (Unset | str): 如有，指向包含该服务补充信息的独立注册表 URL。 示例为 https://www.projectcounter.org/counter-user/ebsco-database/.
    """

    service_active: bool
    alerts: Unset | list["SUSHIServiceStatusAlertsItem"] = UNSET
    description: Unset | str = UNSET
    note: Unset | str = UNSET
    registry_url: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_active = self.service_active

        alerts: Unset | list[dict[str, Any]] = UNSET
        if not isinstance(self.alerts, Unset):
            alerts = []
            for alerts_item_data in self.alerts:
                alerts_item = alerts_item_data.to_dict()
                alerts.append(alerts_item)

        description = self.description

        note = self.note

        registry_url = self.registry_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ServiceActive": service_active,
            }
        )
        if alerts is not UNSET:
            field_dict["Alerts"] = alerts
        if description is not UNSET:
            field_dict["Description"] = description
        if note is not UNSET:
            field_dict["Note"] = note
        if registry_url is not UNSET:
            field_dict["RegistryURL"] = registry_url

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        from ..models.sushi_service_status_alerts_item import (
            SUSHIServiceStatusAlertsItem,
        )

        d = src_dict.copy()
        service_active = d.pop("ServiceActive")

        alerts = []
        _alerts = d.pop("Alerts", UNSET)
        for alerts_item_data in _alerts or []:
            alerts_item = SUSHIServiceStatusAlertsItem.from_dict(alerts_item_data)

            alerts.append(alerts_item)

        description = d.pop("Description", UNSET)

        note = d.pop("Note", UNSET)

        registry_url = d.pop("RegistryURL", UNSET)

        sushi_service_status = cls(
            service_active=service_active,
            alerts=alerts,
            description=description,
            note=note,
            registry_url=registry_url,
        )

        sushi_service_status.additional_properties = d
        return sushi_service_status

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
