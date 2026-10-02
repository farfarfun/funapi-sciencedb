"""把仓库根目录加进 `sys.path`，让测试能 import 根目录下的 `generate` / `localize`。

这两个模块是开发期脚本（不进发布包），所以不在 `src/` 里，默认不在导入路径上。
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
