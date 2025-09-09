# Python 包导入使用指南

## 问题描述

当您尝试直接运行 `ai_core/models/__init__.py` 时，会出现以下错误：
```
ImportError: attempted relative import with no known parent package
```

## 原因分析

这是 Python 包系统的正常行为：
1. `__init__.py` 文件用于定义包的导出内容
2. 它不应该被直接执行，而是通过导入来使用
3. 相对导入（如 `from .ethical_case import EthicalCase`）需要包上下文

## 正确使用方法

### 方法 1：从项目根目录导入
```python
# 在项目根目录下的任何文件中
from ai_core.models import EthicalCase, DecisionResult

# 使用模型
case = EthicalCase(title="测试案例", description="描述")
```

### 方法 2：添加项目根目录到 Python 路径
```python
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_core.models import EthicalCase
```

### 方法 3：使用现有的测试脚本
我们已经创建了 `test_models_import.py`，展示了正确的导入方法：
```bash
python test_models_import.py
```

## 错误示例（不要这样做）

```bash
# 错误：直接运行 __init__.py
python ai_core/models/__init__.py

# 错误：在 models 目录中运行
cd ai_core/models
python __init__.py
```

## 技术细节

- **相对导入**：`from .ethical_case import EthicalCase` 中的 `.` 表示当前包
- **包上下文**：Python 需要知道当前文件属于哪个包才能解析相对导入
- **PYTHONPATH**：确保项目根目录在 Python 路径中

## 验证导入

运行测试脚本验证一切正常：
```bash
python test_models_import.py
```

应该看到成功消息和创建的 EthicalCase 实例。

## 常见问题解决

1. **如果仍然遇到导入错误**：检查 Python 路径是否包含项目根目录
2. **确保使用正确的 Python 环境**：使用项目虚拟环境（如果存在）
3. **检查文件权限**：确保所有 .py 文件可读

## 开发建议

- 总是在项目根目录或适当的包层级中工作
- 使用 IDE 的包感知功能（如 VS Code、PyCharm）
- 设置正确的 PYTHONPATH 环境变量（如果需要）