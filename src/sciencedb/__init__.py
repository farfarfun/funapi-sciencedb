"""兼容层：`import sciencedb` 已废弃，请改用 `import funapi_sciencedb`。

PyPI 发行名一直是 `funapi-sciencedb`，但包内导入名过去一直是 `sciencedb`——这里
把它们统一成 `funapi_sciencedb`。已经 `pip install funapi-sciencedb` 的用户下次
升级时，旧代码里的 `import sciencedb` 不应该直接 ModuleNotFoundError，所以保留
这一层转发。计划在下一次破坏性版本中删除这个兼容层。
"""

import sys
import warnings

import funapi_sciencedb

warnings.warn(
    "`import sciencedb` 已废弃，请改用 `import funapi_sciencedb`。"
    "这个兼容层会在未来某个版本被移除。",
    DeprecationWarning,
    stacklevel=2,
)

sys.modules[__name__] = funapi_sciencedb
