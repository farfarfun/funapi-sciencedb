"""`localize.py`（生成产物中文化）的测试。

重点是两件事：
1. 仓库里现在**确实**没有残留英文 docstring（SPEC §7）；
2. 中文化是幂等的、只动 docstring 不动代码，所以重新生成客户端之后再跑一遍也安全。
"""

import ast
import json
from pathlib import Path

import pytest

from localize import (
    _JSON_ONLY_TEXTS,
    GENERATED_DIR,
    OPENAPI_FILES,
    OPENAPI_TEXTS,
    TEMPLATE_TEXTS,
    add_model_method_docstrings,
    localize_openapi,
    localize_source,
    untranslated_docstrings,
)

ROOT = Path(__file__).resolve().parent.parent


def test_generated_package_has_no_english_docstring():
    """已提交的生成代码里不应该再有不含中文的 docstring。"""
    assert untranslated_docstrings(ROOT / GENERATED_DIR) == []


def test_generated_model_public_methods_have_chinese_docstrings():
    """模型的公开序列化方法应有说明用途、参数和返回值的中文 docstring。"""
    for path in (ROOT / GENERATED_DIR / "models").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for class_node in (node for node in tree.body if isinstance(node, ast.ClassDef)):
            for node in class_node.body:
                if not isinstance(node, ast.FunctionDef) or node.name not in {
                    "to_dict",
                    "from_dict",
                    "additional_keys",
                }:
                    continue
                docstring = ast.get_docstring(node)
                assert docstring is not None, f"{path}:{node.lineno}"
                assert all(part in docstring for part in ("参数：", "返回："))


@pytest.mark.parametrize("name", OPENAPI_FILES)
def test_openapi_files_are_already_localized(name):
    """已提交的 OpenAPI 文档再跑一遍中文化不应该有变化（说明已经是终态）。"""
    path = ROOT / name
    doc = json.loads(path.read_text(encoding="utf-8"))
    before = json.dumps(doc, ensure_ascii=False, sort_keys=True)
    after = json.dumps(localize_openapi(doc), ensure_ascii=False, sort_keys=True)

    assert before == after


def test_localize_openapi_replaces_only_known_texts():
    """只替换登记过的 summary/description，其他字段和未登记文案原样保留。"""
    doc = {
        "paths": {
            "/search": {
                "get": {
                    "summary": "search dataset by page",
                    "description": "result is order by publish time desc",
                    "operationId": "searchUsingGET",
                }
            }
        },
        "info": {"title": "ScienceDB API Doc", "description": "ScienceDB API"},
        "definitions": {"X": {"description": "something nobody registered"}},
    }

    localize_openapi(doc)
    get = doc["paths"]["/search"]["get"]

    assert get["summary"] == "分页搜索数据集"
    assert get["description"] == "结果按发布时间降序排列"
    # operationId 不是文案字段，必须原样保留，否则会改掉生成出来的函数名。
    assert get["operationId"] == "searchUsingGET"
    # 产品名没登记，不翻译。
    assert doc["info"]["description"] == "ScienceDB API"
    assert doc["definitions"]["X"]["description"] == "something nobody registered"


def test_localize_source_translates_boilerplate_and_keeps_code():
    source = '''def sync(*, client: Client) -> None:
    """getReports

     This resource returns a list of reports supported by the API for a given application.

    Args:
        pagenumber (Unset | int):  Default: 1.

    Raises:
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SUSHIReportPage
    """

    args_value = "Args:"
    return None
'''

    result = localize_source(source)

    assert "获取报告列表" in result
    assert "返回该 API 为指定应用支持的报告列表。" in result
    assert "参数：" in result
    assert "抛出：" in result
    assert "返回：" in result
    assert "默认值为 1." in result
    assert "httpx.TimeoutException：请求耗时超过 Client.timeout。" in result
    # docstring 之外的代码一律不碰，哪怕字面量长得跟模板文案一样。
    assert 'args_value = "Args:"' in result
    assert "def sync(*, client: Client) -> None:" in result


def test_localize_source_matches_text_wrapped_across_lines():
    """生成器会按行宽折行，折过行的长文案也必须能命中。"""
    source = '''class SUSHIReportList:
    """list wrapper of reports

    Attributes:
        report_header (Union[Unset, SUSHIReportHeader]): Generalized report header that defines the requested report,
            the requestor, the customer, filters applied, reportAttributes applied and any exceptions.
    """
'''

    result = localize_source(source)

    assert "报告的列表包装结构" in result
    assert "通用报告头，描述所请求的报告" in result
    assert "Generalized report header" not in result


def test_localize_source_is_idempotent():
    source = '''def sync() -> None:
    """search dataset by page

    Args:
        page (Unset | int):  Default: 1.

    Returns:
        None
    """
'''

    once = localize_source(source)

    assert localize_source(once) == once


def test_add_model_method_docstrings_is_idempotent():
    source = '''class Model:
    def to_dict(self) -> dict[str, object]:
        return {}

    @classmethod
    def from_dict(cls, src_dict: dict[str, object]) -> "Model":
        return cls()

    @property
    def additional_keys(self) -> list[str]:
        return []
'''

    once = add_model_method_docstrings(source)

    assert add_model_method_docstrings(once) == once
    assert once.count("参数：") == 3
    assert once.count("返回：") == 3


def test_localize_source_leaves_untranslated_text_alone():
    """没登记的英文原样留着，好让 --check 把它暴露出来，而不是被猜着翻掉。"""
    source = '''def sync() -> None:
    """brand new endpoint nobody registered yet

    Args:
        page (Unset | int):
    """
'''

    result = localize_source(source)

    assert "brand new endpoint nobody registered yet" in result
    assert "参数：" in result


def test_untranslated_docstrings_reports_english_docstring(tmp_path):
    (tmp_path / "mod.py").write_text(
        'def f():\n    """totally english docstring"""\n', encoding="utf-8"
    )

    missing = untranslated_docstrings(tmp_path)

    assert len(missing) == 1
    assert "mod.py" in missing[0]


def test_translation_tables_are_sane():
    for table in (OPENAPI_TEXTS, TEMPLATE_TEXTS):
        for english, chinese in table.items():
            assert english != chinese
            assert chinese.strip(), english
    # 两张表不能对同一段英文给出不同译法。
    overlap = set(OPENAPI_TEXTS) & set(TEMPLATE_TEXTS)
    assert all(OPENAPI_TEXTS[key] == TEMPLATE_TEXTS[key] for key in overlap)
    # 只用于 JSON 的短文案必须确实登记在 OPENAPI_TEXTS 里。
    assert _JSON_ONLY_TEXTS <= set(OPENAPI_TEXTS)
