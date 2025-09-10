# PyCharm 运行配置指南

## 1. 项目设置

### 打开项目
1. 在PyCharm中选择 `File` -> `Open`
2. 选择项目根目录（包含 `ai_core` 文件夹的目录）
3. 点击 `OK`

### 配置Python解释器
1. 打开 `File` -> `Settings` (Windows) 或 `PyCharm` -> `Preferences` (macOS)
2. 导航到 `Project` -> `Python Interpreter`
3. 选择项目的Python解释器（建议使用虚拟环境）

### 标记源代码根目录
1. 在项目视图中右键点击项目根目录
2. 选择 `Mark Directory as` -> `Sources Root`
3. 确保 `ai_core` 文件夹被识别为源代码

## 2. 运行方式

### 方式一：直接运行示例脚本
1. 打开 `run_example.py` 文件
2. 右键点击文件内容区域
3. 选择 `Run 'run_example'`

### 方式二：使用运行配置
1. 点击 `Run` -> `Edit Configurations`
2. 点击 `+` 添加新配置
3. 选择 `Python`
4. 配置如下：
   - Name: `Hegelian AI Example`
   - Script path: `项目根目录/run_example.py`
   - Working directory: `项目根目录`
5. 点击 `OK`
6. 使用绿色运行按钮运行

### 方式三：测试导入
1. 打开 `test_models_import.py`
2. 右键运行此文件
3. 检查导入是否成功

## 3. 常见问题解决

### 问题1: ImportError: attempted relative import with no known parent package
**解决方案:**
- 确保项目根目录被标记为Sources Root
- 不要直接运行 `ai_core/models/__init__.py`
- 使用提供的运行脚本

### 问题2: ModuleNotFoundError: No module named 'ai_core'
**解决方案:**
- 检查Python解释器配置
- 确保在正确的项目目录中
- 重新标记Sources Root

### 问题3: 依赖包缺失
**解决方案:**
```bash
# 在PyCharm终端中运行
pip install -r requirements.txt
```

## 4. 调试设置

### 设置断点调试
1. 在代码行号左侧点击设置断点
2. 右键选择 `Debug 'run_example'`
3. 使用调试控制台查看变量值

### 查看变量
- 在调试模式下，Variables窗口会显示所有变量
- 可以在Console中执行Python代码

## 5. 项目结构确认

确保你的项目结构如下：
```
项目根目录/
├── ai_core/
│   ├── __init__.py
│   └── models/
│       ├── __init__.py
│       ├── ethical_case.py
│       └── decision_result.py
├── run_example.py
├── test_models_import.py
└── 其他文件...
```

## 6. 快速测试

运行以下命令测试设置是否正确：

```python
# 在PyCharm的Python Console中执行
import sys
print("Python路径:", sys.path)

from ai_core.models import EthicalCase
print("导入成功!")
```

如果遇到问题，请检查上述配置步骤。