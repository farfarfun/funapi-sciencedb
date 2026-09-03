# Changelog

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
- `[tool.ruff]` 显式排除 `src/funapi_sciencedb`（openapi-python-client 生成的
  客户端代码，见下方「已知限制」）。
- 本文件历史条目按「新增/修复/变更/废弃」四分类重新归类整理，不改变实际内容含义。

### 已知限制

- `src/funapi_sciencedb/`（`client.py`、`types.py`、`errors.py`、`api/`、
  `models/`）由 `openapi-python-client` 全量生成，使用该工具自带模板：英文
  docstring、`typing.Optional`/`Dict`/`Union`/`Tuple` 旧式类型标注。
  openapi-python-client 目前没有可配置类型标注风格或 docstring 语言的模板选项，
  手工改写生成产物没有意义（下次 `generate.py` 会整体覆盖），暂不修复，仅在
  `pyproject.toml` 的 `[tool.ruff]` 中排除这部分目录。

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
