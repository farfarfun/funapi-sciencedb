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
