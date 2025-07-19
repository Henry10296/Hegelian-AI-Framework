# 🚀 Hegelian-AI-Framework 配置指南

## 1. 安装 Python 依赖 (必需)

### 基础依赖安装
```bash
# 安装核心 Web 框架
pip install fastapi==0.104.1 uvicorn==0.24.0
pip install sqlalchemy==2.0.23
pip install pydantic==2.5.0 pydantic-settings==2.1.0

# 安装数据库驱动
pip install aiosqlite  # SQLite 异步驱动

# 安装其他必需包
pip install python-dotenv==1.0.0
pip install jsonschema==4.20.0
pip install python-dateutil==2.8.2
pip install requests==2.31.0
pip install colorlog==6.8.0
```

### 可选依赖（建议逐个安装）
```bash
# 图数据库（可选）
pip install neo4j==5.15.0

# 缓存系统（可选）
pip install redis==5.0.1

# 监控系统（可选）
pip install prometheus-client==0.19.0
pip install psutil  # 系统监控

# 机器学习（可选，如果需要）
pip install torch numpy pandas scikit-learn
```

## 2. 环境变量配置

### 创建 .env 文件
```env
# 基础配置
DEBUG=true
HOST=localhost
PORT=8000
ENVIRONMENT=development

# 数据库配置
DATABASE_URL=sqlite:///./hegelian_ai.db

# 安全配置
JWT_SECRET_KEY=your-secret-key-change-this-in-production
ENCRYPTION_KEY=your-encryption-key-change-this-in-production

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# 功能开关
ENABLE_ADVERSARIAL_TRAINING=true
ENABLE_MULTI_AGENT_SYSTEM=true
ENABLE_BLOCKCHAIN_LOGGING=false
METRICS_ENABLED=true

# Neo4j 配置 (可选)
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Redis 配置 (可选)
REDIS_URL=redis://localhost:6379
```

## 3. 目录结构创建

### 创建必需目录
```bash
mkdir -p logs
mkdir -p models
mkdir -p data/ethical_cases
mkdir -p data/knowledge_graphs
mkdir -p data/training_data
```

## 4. 数据库初始化

### SQLite 配置 (推荐开始使用)
- 项目默认使用 SQLite，无需额外配置
- 数据库文件会自动创建在项目根目录

### PostgreSQL 配置 (可选)
如果要使用 PostgreSQL：
```bash
pip install asyncpg
```

在 .env 文件中修改：
```env
DATABASE_URL=postgresql://username:password@localhost:5432/hegelian_ai
```

## 5. 日志配置

### 创建日志目录
```bash
mkdir logs
```

### 日志轮转配置
项目已内置日志轮转配置，无需额外设置。

## 6. Neo4j 图数据库设置 (可选)

如果需要使用知识图谱功能：

1. 下载并安装 Neo4j Community Edition
2. 启动 Neo4j 服务
3. 在 .env 文件中配置连接信息
4. 安装 Python 驱动：`pip install neo4j==5.15.0`

## 7. Redis 缓存设置 (可选)

如果需要缓存功能：

1. 安装 Redis 服务器
2. 启动 Redis 服务
3. 在 .env 文件中配置连接信息
4. 安装 Python 驱动：`pip install redis==5.0.1`

## 8. 验证配置

### 检查项目结构
```bash
# 验证 Python 文件编译
python -m py_compile backend/main.py

# 测试基础导入
python -c "from backend.main import app; print('✅ 导入成功')"
```

### 运行项目
```bash
# 启动开发服务器
python backend/main.py

# 或使用 uvicorn
uvicorn backend.main:app --reload --host localhost --port 8000
```

## 9. 最小化配置运行

### 仅使用核心功能
如果只想运行基本功能，只需：

1. 安装核心依赖：
```bash
pip install fastapi uvicorn sqlalchemy aiosqlite pydantic python-dotenv
```

2. 创建 .env 文件（使用上面的基础配置）

3. 运行项目：
```bash
python backend/main.py
```

## 10. 常见问题解决

### 依赖安装失败
- 如果 pandas/numpy 安装失败，可以跳过机器学习相关功能
- 如果 Neo4j 连接失败，系统会自动降级到内存模式
- 如果 Redis 连接失败，系统会禁用缓存功能

### 端口冲突
如果 8000 端口被占用，修改 .env 文件中的 PORT 值。

### 权限问题
确保项目目录有读写权限，特别是 logs/ 目录。

## 🎯 快速开始命令

```bash
# 1. 进入项目目录
cd "D:\Code tool\Github Project Hierarchty\Hegelian-AI-Framework"

# 2. 安装最小依赖
pip install fastapi uvicorn sqlalchemy aiosqlite pydantic python-dotenv

# 3. 创建必需目录
mkdir logs

# 4. 创建 .env 文件（复制上面的环境变量配置）

# 5. 运行项目
python backend/main.py
```

访问 http://localhost:8000 查看 API 文档。