# Changelog

## [1.1.2] - 2026-10-02

### 修复

- 生成的客户端代码 docstring 全面中文化（SPEC §7）。此前只有 `client.py` 的两个类
  docstring 和 `search_using_get.py` 被手工翻过，其余 28 个文件（全部模型、
  `sushi_controller` 下的接口、`errors.py`、`types.py`、各级 `__init__.py`）以及
  `client.py` 的方法 docstring 都还是英文，而且手工翻译在下次重新生成时会被覆盖掉。
- `tests/test_smoke.py` 的模块/用例 docstring 与注释改为中文。

### 新增

- `localize.py`：生成产物中文化脚本，两张精确文案映射表分别处理上游 OpenAPI 文档里的
  `summary` / `description` 和 `openapi-python-client` 模板写死的英文。`generate.py`
  已接入——拉取文档后先中文化文档，生成代码后再中文化模板文案，所以重新生成客户端
  不会再退回英文。映射表只做精确匹配，上游新增文案原样保留，
  `uv run python localize.py --check` 可以把漏网的 docstring 列出来。
- `tests/test_localize.py`：覆盖中文化的幂等性、折行长文案的匹配、只改 docstring 不动
  代码、未登记文案不乱翻，以及「已提交的生成代码里没有残留英文 docstring」这条守卫。
- 仓库根目录 `conftest.py`：把根目录加进 `sys.path`，让测试能 import 根目录下的
  `generate` / `localize` 这两个开发期脚本。

### 变更

- `openapi-ori.json` / `openapi-v3.json` 里的接口与模型说明同步改为中文，并补上文件
  末尾换行。
- README 的「重新生成客户端」补充中文化步骤与 `localize.py --check` 用法。
- `uv.lock` 中的传递依赖 urllib3 由 2.7.0 升到 2.8.0，修掉 GitHub dependabot 报出的
  3 个漏洞（2 个 HIGH：`HTTPResponse.stream()/read_chunked()` 无界缓冲、HTTPS 代理的
  TLS 配置可能被忽略；1 个 MEDIUM：chunked deflate 可进入无限循环）。本包代码未改动。

### 废弃

- 无。

## [1.1.1] - 2026-09-03

### 修复

- `generate.py` 不再把 `acw_tc`、`cdn_sec_tc` 这两个反爬会话 cookie 和 `traceId`
  写死在代码里，改为从环境变量（`SCIDB_ACW_TC` / `SCIDB_CDN_SEC_TC`）读取，
  `traceId` 每次运行随机生成。
- `pyproject.toml` 的 `description` 从占位符 `Add your description here` 改成
  实际的中文一句话说明，并同步更新了 GitHub 仓库的 description。
- `sciencedb` 兼容层的 `DeprecationWarning` 明确了移除版本：将于 2.0 移除
  （此前只写“未来某个版本”）。

### 新增

- README 补充「重新生成客户端」使用说明，以及末尾统一的「关于 farfarfun」组织
  介绍区块。
- `generate.py` 运行所需的 `requests`、`funapi`、`openapi-python-client` 纳入
  `pyproject.toml` 的 `generate` 依赖组，`uv sync --group generate` 即可复现。
- `tests/test_smoke.py` 补充 `metrics_using_get`、`json_using_get`、
  `get_reports`、`get_report_by_id_using_get` 以及 `asyncio`/`asyncio_detailed`
  异步调用路径的 mock HTTP 测试。

### 变更

- `pyproject.toml` 补充 `license = "MIT"` 字段。
- `[tool.ruff]` 按 Python 3.10 规则检查生成客户端代码。
- 本文件历史条目按「新增/修复/变更/废弃」四分类重新归类整理，不改变实际内容含义。

### 废弃

- 无。

## [1.1.0] - 2026-08-28

### 变更（破坏性变更）

- 包内导入路径从 `sciencedb` 统一改为 `funapi_sciencedb`，与仓库名、PyPI 发布名
  （一直都是 `funapi-sciencedb`）保持一致。`generate.py` 里 OpenAPI 客户端代码的
  生成目标目录也同步改为 `src/funapi_sciencedb`，以后重新生成不会再退回旧名。

### 新增

- 保留了 `sciencedb` 兼容层（`src/sciencedb/__init__.py`，仅一个文件）：
  `import sciencedb` 仍然可用，会转发到 `funapi_sciencedb` 并抛出
  `DeprecationWarning`。计划在下一次破坏性版本中删除这个兼容层，请尽快把代码里的
  `import sciencedb` / `from sciencedb...` 换成
  `import funapi_sciencedb` / `from funapi_sciencedb...`。

### 修复

- 无。

### 废弃

- `sciencedb` 兼容导入将在 2.0 移除，请迁移到 `funapi_sciencedb`。
