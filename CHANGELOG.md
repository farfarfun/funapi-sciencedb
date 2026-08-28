# Changelog

## [1.1.0] - 2026-08-28

### Changed（破坏性变更）

- 包内导入路径从 `sciencedb` 统一改为 `funapi_sciencedb`，与仓库名、PyPI 发布名
  （一直都是 `funapi-sciencedb`）保持一致。`generate.py` 里 OpenAPI 客户端代码的
  生成目标目录也同步改为 `src/funapi_sciencedb`，以后重新生成不会再退回旧名。
- 保留了 `sciencedb` 兼容层（`src/sciencedb/__init__.py`，仅一个文件）：
  `import sciencedb` 仍然可用，会转发到 `funapi_sciencedb` 并抛出
  `DeprecationWarning`。计划在下一次破坏性版本中删除这个兼容层，请尽快把代码里的
  `import sciencedb` / `from sciencedb...` 换成
  `import funapi_sciencedb` / `from funapi_sciencedb...`。
