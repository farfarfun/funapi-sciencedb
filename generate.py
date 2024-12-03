import json
from pathlib import Path

import requests
from funapi.convert import convert_openapi_v3
from funapi.generate import generate_api
from openapi_python_client import MetaType

openapi_filepath_ori = "openapi-ori.json"
openapi_filepath_v3 = "openapi-v3.json"


def load_openapi_ori():
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
        "acw_tc": "3adc341c17331953480173868ed3c0ca24d7a278bcc0c3dafa5e1618a7",
        "cdn_sec_tc": "3adc341c17331953480173868ed3c0ca24d7a278bcc0c3dafa5e1618a7",
        "lang": "zh",
        "traceId": "cf6c6aa6-3acd-4840-96b7-11cc7ab0b561",
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    with open(openapi_filepath_ori, "w", encoding="utf-8") as f:
        f.write(json.dumps(response.json(), indent=4, ensure_ascii=False))


load_openapi_ori()
convert_openapi_v3()
generate_api(
    path=Path(openapi_filepath_v3),
    output_path=Path("./src/sciencedb"),
    meta=MetaType.NONE,
    overwrite=True,
)
