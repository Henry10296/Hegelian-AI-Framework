#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web服务器主入口 - 为前端提供AI社会模拟数据

运行此文件将启动一个Web服务器，该服务器会预先运行一次完整的AI社会模拟，
并通过一个API端点，为前端提供结构化的JSON历史数据。

--- 运行指南 ---
1. 安装依赖: pip install fastapi "uvicorn[standard]" openai
2. 运行服务器: python start_server.py
3. 访问API: 在浏览器中打开 http://127.0.0.1:8000/api/v1/simulation_history
"""

import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import asdict

# --- 设置Python路径 ---
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
# ---------------------

# --- 导入我们的AI社会模拟器 ---
from ai_core.simulators.ai_society_simulator import AISocietySimulator
from ai_core.models.ethical_case import EthicalCase, ActionOption, Stakeholder, RelationshipType
# --------------------------------

# 创建一个FastAPI应用实例
app = FastAPI(
    title="AI Society Simulation API",
    description="提供AI社会道德演化历史数据的API。",
    version="1.0.0",
)

# --- CORS中间件配置 ---
# 允许所有来源的跨域请求，这在开发前端时非常方便
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 全局变量，用于存储模拟结果 ---
simulation_history_data = []

@app.on_event("startup")
def run_simulation_on_startup():
    """服务器启动时，自动运行一次完整的AI社会模拟。"""
    print("🚀 服务器启动... 正在预先计算AI社会模拟... 🚀")
    global simulation_history_data

    simulator = AISocietySimulator()

    agent_configs = [
        {"name": "Alice", "genome": {"utilitarian": 0.8, "deontological": 0.2, "collectivism": 0.9}},
        {"name": "Bob", "genome": {"utilitarian": 0.3, "deontological": 0.7, "individualism": 0.8}},
        {"name": "Charlie", "genome": {"utilitarian": 0.6, "deontological": 0.4, "collectivism": 0.6}},
        {"name": "David", "genome": {"utilitarian": 0.4, "deontological": 0.6, "individualism": 0.7}},
    ]
    network_connections = [("Alice", "Bob"), ("Bob", "Charlie"), ("Alice", "Charlie")]
    simulator.setup_society(agent_configs, network_connections)

    # 运行几个初始时间步
    simulator.run_tick(event="Society is stable")
    
    # 让Alice面临一个困境并行动，这将触发第一次道德传染
    dilemma = EthicalCase(
        title="牺牲少数，拯救多数",
        action_options=[
            ActionOption(name="牺牲1个人救5个人", description="", metadata={
                'utility_scores': {"all": 10}, 'violates_rules': [], 'expresses_virtues': {'courage': 0.8}
            })
        ]
    )
    simulator.introduce_dilemma("Alice", dilemma)

    # 再运行一个时间步，让Bob和Charlie有机会被Alice影响
    simulator.run_tick(event="Alice's action propagates")

    # 将最终的历史数据转换为前端友好的字典格式并存储
    simulation_history_data = [asdict(snapshot) for snapshot in simulator.tracker.history]
    print("✅ 预计算完成！服务器已准备好为前端提供数据。")

@app.get("/api/v1/simulation_history")
def get_simulation_history():
    """
    API端点：获取完整的、为前端优化的AI社会模拟历史数据。
    """
    return {
        "message": "AI society simulation history retrieved successfully.",
        "data": simulation_history_data
    }

if __name__ == "__main__":
    # 启动服务器
    uvicorn.run(app, host="127.0.0.1", port=8000)
