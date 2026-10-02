from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_result import SearchResult


T = TypeVar("T", bound="APIResultSearchResult")


@_attrs_define
class APIResultSearchResult:
    """接口统一返回结构

    属性：
        code (Unset | int): 20000 表示成功，其他值表示错误
        message (Unset | str): code 对应的中文说明
        get_message_en (Unset | str): code 对应的英文说明
        data (Union[Unset, SearchResult]): '/harvest' 与 '/search' 接口记录的包装结构
    """

    code: Unset | int = UNSET
    message: Unset | str = UNSET
    get_message_en: Unset | str = UNSET
    data: Union[Unset, "SearchResult"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        get_message_en = self.get_message_en

        data: Unset | dict[str, Any] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if message is not UNSET:
            field_dict["message"] = message
        if get_message_en is not UNSET:
            field_dict["getMessageEn"] = get_message_en
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        from ..models.search_result import SearchResult

        d = src_dict.copy()
        code = d.pop("code", UNSET)

        message = d.pop("message", UNSET)

        get_message_en = d.pop("getMessageEn", UNSET)

        _data = d.pop("data", UNSET)
        data: Unset | SearchResult
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = SearchResult.from_dict(_data)

        api_result_search_result = cls(
            code=code,
            message=message,
            get_message_en=get_message_en,
            data=data,
        )

        api_result_search_result.additional_properties = d
        return api_result_search_result

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
