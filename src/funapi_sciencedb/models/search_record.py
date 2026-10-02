from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchRecord")


@_attrs_define
class SearchRecord:
    """'/harvest' 与 '/search' 接口返回的数据集简要记录

    属性：
        clicks (Unset | int):
        language (Unset | str):
        reference_number (Unset | int):
        title (Unset | str): 数据集标题
        introduction (Unset | str): 数据集简介
        keyword (Unset | str): 数据集关键词，整体放在引号内 示例为 kw_1;kw_2;kw_3.
        author (Unset | str): 数据集作者，整体放在引号内 示例为 2021-08-11 18:20:51.
        publish_date (Unset | str): 在 ScienceDB 的发布日期 示例为 author_1;author_2;author_3.
        taxonomy (Unset | str): 在 ScienceDB 的学科分类，整体放在引号内，格式为 'code'-'taxonomy'
            示例为 170-Earth science;00-Others.
        year (Unset | str): 在 ScienceDB 的发布年份 示例为 2021.
        doi (Unset | str): 数据集的 DOI 示例为 10.11922/sciencedb.00101.
    """

    clicks: Unset | int = UNSET
    language: Unset | str = UNSET
    reference_number: Unset | int = UNSET
    title: Unset | str = UNSET
    introduction: Unset | str = UNSET
    keyword: Unset | str = UNSET
    author: Unset | str = UNSET
    publish_date: Unset | str = UNSET
    taxonomy: Unset | str = UNSET
    year: Unset | str = UNSET
    doi: Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clicks = self.clicks

        language = self.language

        reference_number = self.reference_number

        title = self.title

        introduction = self.introduction

        keyword = self.keyword

        author = self.author

        publish_date = self.publish_date

        taxonomy = self.taxonomy

        year = self.year

        doi = self.doi

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clicks is not UNSET:
            field_dict["clicks"] = clicks
        if language is not UNSET:
            field_dict["language"] = language
        if reference_number is not UNSET:
            field_dict["referenceNumber"] = reference_number
        if title is not UNSET:
            field_dict["title"] = title
        if introduction is not UNSET:
            field_dict["introduction"] = introduction
        if keyword is not UNSET:
            field_dict["keyword"] = keyword
        if author is not UNSET:
            field_dict["author"] = author
        if publish_date is not UNSET:
            field_dict["publishDate"] = publish_date
        if taxonomy is not UNSET:
            field_dict["taxonomy"] = taxonomy
        if year is not UNSET:
            field_dict["year"] = year
        if doi is not UNSET:
            field_dict["doi"] = doi

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        clicks = d.pop("clicks", UNSET)

        language = d.pop("language", UNSET)

        reference_number = d.pop("referenceNumber", UNSET)

        title = d.pop("title", UNSET)

        introduction = d.pop("introduction", UNSET)

        keyword = d.pop("keyword", UNSET)

        author = d.pop("author", UNSET)

        publish_date = d.pop("publishDate", UNSET)

        taxonomy = d.pop("taxonomy", UNSET)

        year = d.pop("year", UNSET)

        doi = d.pop("doi", UNSET)

        search_record = cls(
            clicks=clicks,
            language=language,
            reference_number=reference_number,
            title=title,
            introduction=introduction,
            keyword=keyword,
            author=author,
            publish_date=publish_date,
            taxonomy=taxonomy,
            year=year,
            doi=doi,
        )

        search_record.additional_properties = d
        return search_record

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
