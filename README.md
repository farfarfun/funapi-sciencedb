# funapi-sciencedb

科学数据银行（[ScienceDB](https://www.scidb.cn)）Open API 的 Python 客户端，由 `openapi-python-client` 根据 ScienceDB 官方 OpenAPI 文档（`https://www.scidb.cn/open-api/v2/api-docs`）自动生成，仓库里的 `generate.py` 就是重新拉取该文档并重新生成客户端代码的脚本。

## 安装

```bash
pip install funapi-sciencedb
```

## 用法示例

```python
from funapi_sciencedb import Client
from funapi_sciencedb.api.open_api_controller import search_using_get

client = Client(base_url="https://www.scidb.cn/open-api/v2")

# 按发布时间倒序分页搜索数据集
result = search_using_get.sync(client=client, page=1, size=10)
```

除了开放接口（`open_api_controller`，搜索/harvest/metrics/json 等），还包含 COUNTER 标准的用量统计报表接口（`sushi_controller`：`get_api_status`、`get_reports`、`get_report_by_id_using_get`）。每个接口都提供 `sync` / `sync_detailed` / `asyncio` / `asyncio_detailed` 四种调用方式，返回值是 `models/` 目录下对应的强类型模型对象。

由于是自动生成的客户端，具体字段和返回结构以 `src/funapi_sciencedb/models/` 下的类定义为准。

## 重新生成客户端

`generate.py` 会重新拉取 ScienceDB 官方 OpenAPI 文档并重新生成 `src/funapi_sciencedb/` 下的全部代码，运行前需要安装 `generate` 依赖组：

```bash
uv sync --group generate
uv run python generate.py
```

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
