"""把生成产物里的英文文案统一替换成中文（SPEC §7「注释和 docstring 用中文」）。

`src/funapi_sciencedb` 整个目录都是 `openapi-python-client` 按 OpenAPI 文档自动生成的，
里面的英文来自两个地方，所以这里也分两张表：

1. **上游文档文案**（`OPENAPI_TEXTS`）：ScienceDB 官方 OpenAPI 文档里的 `summary`、
   `description`。这些文字会被生成器写进函数和模型的 docstring，所以在 `generate.py`
   拉取文档之后、生成代码之前就替换掉，生成出来的就直接是中文。
2. **生成器模板文案**（`TEMPLATE_TEXTS`）：`Args:`、`Raises:`、`Client` 的类
   docstring 等等，由 `openapi-python-client` 的模板写死，不在 OpenAPI 文档里，
   只能在生成之后替换。

两张表都是**精确文案映射**，不做任何猜测式翻译：没登记的英文原样保留，并且可以用
`python localize.py --check` 查出来（重新生成后上游新增了文案就会在这里暴露），
再补到表里。替换是幂等的——中文不会再匹配英文键，重复跑结果一致。

用法：

```bash
uv run python localize.py          # 对 openapi-*.json 和 src/ 重新应用中文化
uv run python localize.py --check  # 只检查，列出还没中文化的 docstring
```

正常流程不用单独跑，`generate.py` 已经把这两步接进去了。
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

OPENAPI_FILES = ("openapi-ori.json", "openapi-v3.json")
GENERATED_DIR = Path("src/funapi_sciencedb")

#: OpenAPI 文档里需要中文化的 `summary` / `description` 原文 -> 中文。
#: `info`、`tags` 里的产品名（`ScienceDB API` 之类）是专有名词，故意不翻译。
OPENAPI_TEXTS: dict[str, str] = {
    # ---- /harvest ----
    "harvest dataset by dataset's publish time period(start_time and end_time)": "按数据集发布时间区间（start_time 与 end_time）批量获取数据集",
    "result is order by publish time desc": "结果按发布时间降序排列",
    "date format : 'yyyy-MM-dd'": "日期格式为 'yyyy-MM-dd'",
    "Page No": "页码",
    "Page Size": "每页条数",
    "OK": "成功",
    # ---- /json ----
    "get dataset's detail information by it's doi": "按 DOI 获取数据集的详细信息",
    "information's format is referenced by https://schema.org/Dataset": "信息格式参照 https://schema.org/Dataset",
    "dataset's DOI": "数据集的 DOI",
    # ---- /metrics ----
    "search dataset metrics by doi": "按 DOI 查询数据集的统计指标",
    "doi": "数据集的 DOI",
    # ---- /report/{id} ----
    "This resource returns the COUNTER Dataset Report by id": "按 id 返回 COUNTER 数据集报告",
    "id": "报告 id",
    "publisher": "出版方",
    # ---- /reports ----
    "getReports": "获取报告列表",
    "This resource returns a list of reports supported by the API for a given application.": "返回该 API 为指定应用支持的报告列表。",
    "page[number]": "页码",
    "page[size]": "每页条数",
    # ---- /search ----
    "search dataset by page": "分页搜索数据集",
    "Defines how many days of data have been published, if not set the range means search full time range": "限定最近多少天内发布的数据，不传表示搜索全部时间范围",
    # ---- /status ----
    "getAPIStatus": "获取 API 服务状态",
    "This resource returns the current status of the reporting service supported by this API.": "返回该 API 所支持的报告服务的当前状态。",
    "Name of the Platform the report data is being requested for.  This can be omitted if the service provides report data for only one platform.": "请求报告数据所针对的平台名称。若服务只提供单一平台的报告数据，可以省略。",
    "Status of the reporting service(s) supported by this API.": "该 API 所支持的报告服务的状态。",
    # ---- APIResult ----
    "the api result model": "接口统一返回结构",
    "20000 means success, other means error": "20000 表示成功，其他值表示错误",
    "code's description in Chinese": "code 对应的中文说明",
    "code's description in English": "code 对应的英文说明",
    "the data api return": "接口返回的数据",
    # ---- COUNTER* ----
    "Item attribute types are defined by NISO Journal Article Version and other work...": "条目属性类型，依据 NISO Journal Article Version 等规范定义……",
    "Value of the item attribute": "条目属性的值",
    "Value of the contributor identifier": "贡献者标识的值",
    "Value of the dataset date": "数据集日期的值",
    "Value of the dataset identifier": "数据集标识的值",
    "Identifies if the usage activity was 'Regular' usage - a user doing research on a content site, or if the usage activity was 'Machine' - for the purpose of retrieving content for Text and Data Mining (TDM)": "标识该使用行为是 'Regular'（用户在内容站点上做研究的常规访问），还是 'Machine'（为文本与数据挖掘 TDM 抓取内容）",
    "id of report.": "报告 id。",
    # 上游把 report 拼成了 repoart，照原样登记，不改上游。
    "repoart header.": "报告头。",
    "list of datasets .": "数据集列表。",
    "Describes the formatting needs for the COUNTER Dataset Report. Response may include the Report_Header (optional), Report_Datasets (usage stats).": "描述 COUNTER 数据集报告的组织形式。响应可以包含 Report_Header（可选）与 Report_Datasets（使用量统计）。",
    "Defines the output for the Report_Datasets being returned in a Dataset Report.": "定义数据集报告中 Report_Datasets 的输出结构。",
    "Nature of the dataset being reported.": "所报告数据集的类型。",
    "Other attributes related related to the dataset.": "与该数据集相关的其他属性。",
    "The identifier for contributor (i.e. creator) of the dataset.": "数据集贡献者（即创建者）的标识。",
    "Publication or other date(s)related to the dataset.": "与该数据集相关的出版日期或其他日期。",
    "The identifier for the report dataset": "报告中该数据集的标识",
    "Name of the dataset being reported.": "所报告数据集的名称。",
    "The usage data related to the report dataset": "报告中该数据集对应的使用量数据",
    "Name of the platform": "平台名称",
    "Name of publisher of the dataset": "数据集出版方名称",
    "The identifier for the publisher.": "出版方的标识。",
    "Year of publication in the format of 'yyyy'. Use '0001' for unknown and '9999' for articles in press.": "出版年份，格式为 'yyyy'。未知填 '0001'，在印填 '9999'。",
    "Value of the publisher identifier": "出版方标识的值",
    # ---- MetricsResult ----
    "Chinese title of dataset": "数据集的中文标题",
    "English title of dataset": "数据集的英文标题",
    "Number of data set accesses": "数据集的访问次数",
    "Number of data set downloads": "数据集的下载次数",
    "The number of papers cited in the dataset": "引用该数据集的论文数量",
    "wrapper of records of '/harvest' and '/search' and '/metrics' API": "'/harvest'、'/search' 与 '/metrics' 接口记录的包装结构",
    # ---- SUSHI* ----
    "Generalized format for presenting errors and exceptions.": "错误与异常的通用表示结构。",
    "Error number. See table of error.": "错误码，含义见错误码表。",
    "Additional data provided by the server to clarify the error.": "服务端提供的补充信息，用于进一步说明该错误。",
    "URL describing error details.": "描述错误详情的 URL。",
    "Text describing the error.": "错误的文字描述。",
    "Severity of the error.": "错误的严重级别。",
    "page number.": "页码。",
    "count of reports.": "报告总数。",
    "count of pages.": "总页数。",
    "page wrapper of reports": "报告的分页包装结构",
    "Generalized report header that defines the requested report, the requestor, the customer, filters applied, reportAttributes applied and any exceptions.": "通用报告头，描述所请求的报告、请求方、客户、生效的过滤条件、生效的 reportAttributes 以及出现的异常。",
    "Time the report was prepared": "报告生成时间",
    "Name of the organization producing the report.": "生成该报告的机构名称。",
    "Series of exceptions encounted when preparing the report.": "生成报告过程中遇到的异常列表。",
    "The release or version of the report.": "报告的发布版本。",
    "Zero or more additional attributes applied to the report. Attributes inform the level of detail in the report.": "作用于该报告的零个或多个附加属性，属性决定报告的明细程度。",
    "Zero or more report filters used for this report.  Typically  reflect filters provided on the Request.  Filters limit the data to be reported on.": "该报告使用的零个或多个过滤条件，通常对应请求里传入的过滤条件，用于限定报告的数据范围。",
    "The report ID or code or shortname. Typically this will be the same code provided in the Report parameter of the request.": "报告的 ID、代码或简称，通常与请求中 Report 参数传入的代码一致。",
    "The long name of the report.": "报告的完整名称。",
    "report id.": "报告 id。",
    "report headers": "报告头",
    "list wrapper of reports": "报告的列表包装结构",
    "list of reports": "报告列表",
    "meta of page info.": "分页信息。",
    "Any alerts related to service interuptions and status.": "与服务中断及状态相关的告警。",
    "Description of the service.": "服务说明。",
    "A general note about the service.": "关于该服务的一般性说明。",
    "If available, the URL separate registry with additional information about the service.": "如有，指向包含该服务补充信息的独立注册表 URL。",
    "Indicator if the service is currently able to deliver reports.": "标识该服务当前是否可以提供报告。",
    # ---- SearchRecord / SearchResult ----
    "dataset's brief record of '/harvest' and '/search' API": "'/harvest' 与 '/search' 接口返回的数据集简要记录",
    "dataset's title": "数据集标题",
    "dataset's introduction": "数据集简介",
    "dataset's keywords, put together in quotation marks": "数据集关键词，整体放在引号内",
    "dataset's authors, put together in quotation marks": "数据集作者，整体放在引号内",
    "publish date in ScienceDB": "在 ScienceDB 的发布日期",
    "taxonomy in ScienceDB,put together in quotation marks,format is 'code'-'taxonomy'": "在 ScienceDB 的学科分类，整体放在引号内，格式为 'code'-'taxonomy'",
    "publish year in ScienceDB": "在 ScienceDB 的发布年份",
    "dataset's doi": "数据集的 DOI",
    "wrapper of records of '/harvest' and '/search' API": "'/harvest' 与 '/search' 接口记录的包装结构",
    "total pages of records": "记录总页数",
    "total number of records": "记录总数",
    "the list of current page records": "当前页的记录列表",
}

#: 只出现在 OpenAPI 文档里、不会进 docstring 的短文案（接口参数说明、响应说明）。
#: 它们太短（`id`、`doi`、`OK`…），拿去在代码里做替换会误伤，所以只用于 JSON。
_JSON_ONLY_TEXTS = frozenset(
    {
        "date format : 'yyyy-MM-dd'",
        "Page No",
        "Page Size",
        "OK",
        "dataset's DOI",
        "doi",
        "id",
        "publisher",
        "page[number]",
        "page[size]",
        "Defines how many days of data have been published, if not set the range means search full time range",
        "Name of the Platform the report data is being requested for.  This can be omitted if the service provides report data for only one platform.",
        "Status of the reporting service(s) supported by this API.",
    }
)

#: `openapi-python-client` 模板写死的英文 -> 中文。这些文案不在 OpenAPI 文档里，
#: 只能在生成之后替换。
TEMPLATE_TEXTS: dict[str, str] = {
    # ---- 包级 docstring ----
    "A client library for accessing ScienceDB API Doc": "访问 ScienceDB 开放接口（ScienceDB API Doc）的客户端库。",
    "Contains methods for accessing the API": "按 OpenAPI 文档生成的接口调用方法。",
    "Contains all the data models used in inputs/outputs": "接口入参与返回值用到的全部数据模型。",
    # ---- docstring 小节标题与行内标记 ----
    "Args:": "参数：",
    "Raises:": "抛出：",
    "Returns:": "返回：",
    "Attributes:": "属性：",
    "Example:": "示例为",
    "Default:": "默认值为",
    "errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.": "errors.UnexpectedStatus：服务端返回了文档里没有声明的状态码，且 Client.raise_on_unexpected_status 为 True。",
    "httpx.TimeoutException: If the request takes longer than Client.timeout.": "httpx.TimeoutException：请求耗时超过 Client.timeout。",
    # ---- client.py 类 docstring ----
    "A class for keeping track of data related to the API": "用于保存 API 相关数据的客户端。",
    "A Client which has been authenticated for use on secured endpoints": "已完成认证、可以访问受保护端点的客户端。",
    "The following are accepted as keyword arguments and will be used to construct httpx Clients internally:": "下列参数以关键字参数传入，用于在内部构造 httpx 客户端：",
    "``base_url``: The base URL for the API, all requests are made to a relative path to this URL": "``base_url``：API 的基础 URL，所有请求都使用相对于它的路径。",
    "``cookies``: A dictionary of cookies to be sent with every request": "``cookies``：每个请求都会带上的 cookie 字典。",
    "``headers``: A dictionary of headers to be sent with every request": "``headers``：每个请求都会带上的请求头字典。",
    "``timeout``: The maximum amount of a time a request can take. API functions will raise httpx.TimeoutException if this is exceeded.": "``timeout``：单个请求允许的最长耗时，超过后 API 函数会抛出 httpx.TimeoutException。",
    "``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production, but can be set to False for testing purposes.": "``verify_ssl``：是否校验 API 服务端的 SSL 证书。生产环境应为 True，仅测试时可以设为 False。",
    "``follow_redirects``: Whether or not to follow redirects. Default value is False.": "``follow_redirects``：是否跟随重定向，默认为 False。",
    "``httpx_args``: A dictionary of additional arguments to be passed to the ``httpx.Client`` and ``httpx.AsyncClient`` constructor.": "``httpx_args``：传给 ``httpx.Client`` 与 ``httpx.AsyncClient`` 构造函数的额外参数字典。",
    "raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a status code that was not documented in the source OpenAPI document. Can also be provided as a keyword argument to the constructor.": "raise_on_unexpected_status：当 API 返回的状态码没有写在源 OpenAPI 文档里时，是否抛出 errors.UnexpectedStatus。也可以作为关键字参数传给构造函数。",
    "token: The token to use for authentication": "token：用于认证的令牌。",
    "prefix: The prefix to use for the Authorization header": "prefix：认证请求头里令牌的前缀。",
    "auth_header_name: The name of the Authorization header": "auth_header_name：认证请求头的名称。",
    # ---- client.py 方法 docstring ----
    "Get a new client matching this one with additional headers": "返回一个与当前客户端一致、但追加了请求头的新客户端",
    "Get a new client matching this one with additional cookies": "返回一个与当前客户端一致、但追加了 cookie 的新客户端",
    "Get a new client matching this one with a new timeout (in seconds)": "返回一个与当前客户端一致、但使用新超时时间（秒）的新客户端",
    "Manually set the underlying httpx.Client": "手动设置底层的 httpx.Client",
    # 上游模板这句少了 set，照原样登记。
    "Manually the underlying httpx.AsyncClient": "手动设置底层的 httpx.AsyncClient",
    "**NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.": "**注意**：这会覆盖客户端上的其他设置，包括 cookies、headers 和 timeout。",
    "Get the underlying httpx.Client, constructing a new one if not previously set": "获取底层的 httpx.Client，没有设置过就新建一个",
    "Get the underlying httpx.AsyncClient, constructing a new one if not previously set": "获取底层的 httpx.AsyncClient，没有设置过就新建一个",
    "Enter a context manager for self.client—you cannot enter twice (see httpx docs)": "进入 self.client 的上下文管理器，不能重复进入（见 httpx 文档）",
    "Exit a context manager for internal httpx.Client (see httpx docs)": "退出内部 httpx.Client 的上下文管理器（见 httpx 文档）",
    "Enter a context manager for underlying httpx.AsyncClient—you cannot enter twice (see httpx docs)": "进入底层 httpx.AsyncClient 的上下文管理器，不能重复进入（见 httpx 文档）",
    "Exit a context manager for underlying httpx.AsyncClient (see httpx docs)": "退出底层 httpx.AsyncClient 的上下文管理器（见 httpx 文档）",
    # ---- errors.py / types.py ----
    "Contains shared errors types that can be raised from API functions": "API 函数可能抛出的公共异常类型。",
    "Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True": "当响应状态码没有写在文档里、且 Client.raise_on_unexpected_status 为 True 时，由 API 函数抛出。",
    "Contains some shared types for properties": "模型属性用到的公共类型。",
    "Contains information for file uploads": "文件上传所需的信息。",
    "A response from an endpoint": "接口返回的响应。",
    "Return a tuple representation that httpx will accept for multipart/form-data": "返回 httpx 能用于 multipart/form-data 的元组表示",
}

_CJK = re.compile(r"[一-鿿]")


def _code_replacements() -> list[tuple[re.Pattern[str], str]]:
    """构造 docstring 替换规则，长文案优先，避免短文案先把长文案切断。

    生成器会按行宽把长文案折行，所以这里把原文按空白切开、用 `\\s+` 连接，
    折过行的文案（换行 + 缩进）同样能匹配上。
    """
    texts = {k: v for k, v in OPENAPI_TEXTS.items() if k not in _JSON_ONLY_TEXTS}
    texts.update(TEMPLATE_TEXTS)
    rules = []
    for english in sorted(texts, key=len, reverse=True):
        pattern = r"\s+".join(re.escape(part) for part in english.split())
        rules.append((re.compile(pattern), texts[english]))
    return rules


def localize_openapi(doc: object) -> object:
    """就地把 OpenAPI 文档里的 `summary` / `description` 替换成中文，返回同一个对象。"""
    if isinstance(doc, dict):
        for key, value in doc.items():
            if key in ("summary", "description") and isinstance(value, str):
                doc[key] = OPENAPI_TEXTS.get(value, value)
            else:
                localize_openapi(value)
    elif isinstance(doc, list):
        for item in doc:
            localize_openapi(item)
    return doc


def _docstring_spans(source: str) -> list[tuple[int, int]]:
    """返回源码里所有 docstring 占用的行号区间（1 起、含两端）。"""
    spans: list[tuple[int, int]] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(
            node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
        ):
            continue
        body = getattr(node, "body", None)
        if not body:
            continue
        first = body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
            and first.value.end_lineno is not None
        ):
            spans.append((first.value.lineno, first.value.end_lineno))
    return sorted(spans)


def localize_source(source: str) -> str:
    """把一份生成代码里 docstring 的英文替换成中文，代码本身不动。"""
    rules = _code_replacements()
    lines = source.splitlines(keepends=True)
    # 从后往前改，前面的行号才不会被已完成的替换顶掉。
    for start, end in reversed(_docstring_spans(source)):
        chunk = "".join(lines[start - 1 : end])
        new_chunk = chunk
        for pattern, chinese in rules:
            new_chunk = pattern.sub(lambda m, zh=chinese: zh, new_chunk)
        if new_chunk != chunk:
            lines[start - 1 : end] = [new_chunk]
    return "".join(lines)


def untranslated_docstrings(root: Path = GENERATED_DIR) -> list[str]:
    """列出仍然不含中文的 docstring，形如 `路径:行号`。"""
    missing = []
    for path in sorted(root.rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        for start, end in _docstring_spans(source):
            chunk = "".join(source.splitlines(keepends=True)[start - 1 : end])
            if not _CJK.search(chunk):
                missing.append(f"{path}:{start}")
    return missing


def localize_generated(root: Path = GENERATED_DIR) -> list[Path]:
    """对生成目录下所有 `.py` 应用中文化，返回实际被改写的文件。"""
    changed = []
    for path in sorted(root.rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        new_source = localize_source(source)
        if new_source != source:
            path.write_text(new_source, encoding="utf-8")
            changed.append(path)
    return changed


def localize_openapi_files(files: tuple[str, ...] = OPENAPI_FILES) -> list[Path]:
    """对本地已有的 OpenAPI 文档应用中文化，返回实际被改写的文件。"""
    changed = []
    for name in files:
        path = Path(name)
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        doc = json.loads(original)
        text = json.dumps(localize_openapi(doc), indent=4, ensure_ascii=False) + "\n"
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(path)
    return changed


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "--check":
        missing = untranslated_docstrings()
        for item in missing:
            print(f"still english: {item}")
        return 1 if missing else 0

    for path in localize_openapi_files():
        print(f"localized: {path}")
    for path in localize_generated():
        print(f"localized: {path}")
    missing = untranslated_docstrings()
    for item in missing:
        print(f"still english: {item}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
