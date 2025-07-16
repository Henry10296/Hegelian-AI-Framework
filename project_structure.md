# 项目目录结构规划

## 完整项目结构
```
Hegelian-AI-Framework/
├── README.md                    # 项目说明
├── .gitignore                   # Git忽略文件
├── requirements.txt             # Python依赖
├── package.json                 # 前端依赖
├── docker-compose.yml           # 容器化部署
├── 
├── frontend/                    # 前端代码
│   ├── public/                  # 静态文件
│   ├── src/                     # 源代码
│   │   ├── components/          # 组件
│   │   ├── pages/              # 页面
│   │   ├── services/           # API服务
│   │   ├── utils/              # 工具函数
│   │   └── App.tsx             # 主应用
│   ├── package.json
│   └── tsconfig.json
├── 
├── backend/                     # 后端代码
│   ├── app/                     # 应用主目录
│   │   ├── models/             # 数据模型
│   │   ├── api/                # API路由
│   │   ├── services/           # 业务逻辑
│   │   ├── utils/              # 工具函数
│   │   └── config/             # 配置文件
│   ├── tests/                  # 测试文件
│   ├── migrations/             # 数据库迁移
│   └── main.py                 # 应用入口
├── 
├── ai_core/                     # AI核心模块
│   ├── dialectical_engine/      # 辩证决策引擎
│   ├── knowledge_base/          # 知识库
│   ├── decision_rules/          # 决策规则
│   └── utils/                  # AI工具
├── 
├── data/                        # 数据文件
│   ├── ethical_cases/          # 伦理案例
│   ├── knowledge_graphs/       # 知识图谱
│   └── training_data/          # 训练数据
├── 
├── docs/                        # 文档
│   ├── api/                    # API文档
│   ├── user_guide/             # 用户指南
│   └── development/            # 开发文档
├── 
├── scripts/                     # 脚本工具
│   ├── setup.sh               # 环境设置
│   ├── deploy.sh              # 部署脚本
│   └── test.sh                # 测试脚本
├── 
└── tests/                       # 集成测试
    ├── frontend/               # 前端测试
    ├── backend/               # 后端测试
    └── integration/           # 集成测试
```

## 开发阶段目录（先建这些）
```
Hegelian-AI-Framework/
├── README.md                    # ✅ 已存在
├── .gitignore                   # 📝 需要创建
├── requirements.txt             # 📝 需要创建
├── frontend/                    # 📝 需要创建
├── backend/                     # 📝 需要创建
├── ai_core/                     # 📝 需要创建
├── data/                        # 📝 需要创建
├── docs/                        # 📝 需要创建
└── scripts/                     # 📝 需要创建
```

## 学习优先级
1. **第一周**：熟悉项目结构，设置开发环境
2. **第二周**：学习前端基础（React + TypeScript）
3. **第三周**：学习后端基础（Python Flask）
4. **第四周**：集成前后端，实现第一个功能