import json
import os
import uuid
from pathlib import Path

import requests
from funapi.convert import convert_openapi_v3
from funapi.generate import generate_api
from openapi_python_client import MetaType

from localize import localize_generated, localize_openapi

OPENAPI_FILEPATH_ORI = "openapi-ori.json"
OPENAPI_FILEPATH_V3 = "openapi-v3.json"
OUTPUT_DIR = Path("./src/funapi_sciencedb")
OPENAPI_REQUEST_TIMEOUT = 30


def load_openapi_ori() -> None:
    """拉取 ScienceDB 官方 OpenAPI 文档，写入本地 `openapi-ori.json`。

    `acw_tc` / `cdn_sec_tc` 是阿里云 WAF 下发的反爬会话 cookie（不是账号凭据），
    每次访问都会重新生成、很快过期，不应该写死在代码里。这里改为从环境变量读取，
    留空时也能直接访问——大多数情况下 ScienceDB 的这个文档地址不依赖这两个 cookie
    也能正常返回；如果本地实测确实需要，临时用
    `SCIDB_ACW_TC` / `SCIDB_CDN_SEC_TC` 环境变量传入即可，不要提交到仓库。
    """
    url = "https://www.scidb.cn/open-api/v2/api-docs"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "referer": "https://www.scidb.cn/open-api/swagger-ui.html",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    }
    cookies = {
        "acw_tc": os.environ.get("SCIDB_ACW_TC", ""),
        "cdn_sec_tc": os.environ.get("SCIDB_CDN_SEC_TC", ""),
        "lang": "zh",
        "traceId": str(uuid.uuid4()),
    }
    cookies = {k: v for k, v in cookies.items() if v}

    try:
        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            timeout=OPENAPI_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "未知"
        raise RuntimeError(
            f"下载 ScienceDB OpenAPI 文档失败：{url}（HTTP {status}，{exc}）"
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"下载 ScienceDB OpenAPI 文档失败：{url}（{exc}）") from exc

    try:
        openapi = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "ScienceDB OpenAPI 文档不是合法 JSON："
            f"{url}（HTTP {response.status_code}）"
        ) from exc
    # 上游文档是英文的，先按 localize.py 的映射表换成中文再落盘，这样后面生成出来的
    # docstring 直接就是中文（SPEC §7），不用事后再补。
    openapi = localize_openapi(openapi)
    with open(OPENAPI_FILEPATH_ORI, "w", encoding="utf-8") as f:
        f.write(json.dumps(openapi, indent=4, ensure_ascii=False) + "\n")


def main() -> None:
    """拉取并转换 OpenAPI 文档，然后重新生成客户端代码。"""
    load_openapi_ori()
    convert_openapi_v3()
    generate_api(
        path=Path(OPENAPI_FILEPATH_V3),
        output_path=OUTPUT_DIR,
        meta=MetaType.NONE,
        overwrite=True,
    )
    # 生成器模板自带的英文（`Args:`、`Client` 类说明等）不在 OpenAPI 文档里，
    # 只能生成完再替换一遍。
    localize_generated(OUTPUT_DIR)


if __name__ == "__main__":
    main()
