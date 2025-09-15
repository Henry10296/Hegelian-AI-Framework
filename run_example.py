#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目最终运行入口 - 数据驱动的AI社会模拟器

该脚本从 `config.json` 文件中读取所有实验设置，并运行模拟。
这是与AI社会交互的最终、也是唯一的推荐入口。
"""

import os
import sys
import json
from pathlib import Path

# --- 设置Python路径 ---
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
# ---------------------

# --- 导入最终的模拟器和数据模型 ---
from ai_core.simulators.ai_society_simulator import AISocietySimulator
from ai_core.models.ethical_case import EthicalCase, Stakeholder, RelationshipType

# 导入LLM客户端（如果可用）
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

def load_config(config_path: str) -> dict:
    """从JSON文件加载配置。"""
    print(f"[主控] 正在从 '{config_path}' 加载实验配置...")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    """根据配置文件，运行一个完整的、数据驱动的AI社会模拟。"""
    
    # 1. 加载配置
    config = load_config("config.json")
    
    # 2. 初始化LLM客户端（如果配置了API密钥）
    llm_client = None
    if OpenAI and os.getenv("DEEPSEEK_API_KEY"):
        print("[主控] 检测到DeepSeek API密钥，正在激活LLM...")
        llm_client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )
    else:
        print("[主控] 未检测到LLM API密钥，部分功能（如动态生成困境）将受限。")

    # 3. 创建并设置模拟器
    simulator = AISocietySimulator(llm_client=llm_client)
    simulator.setup_society(
        agent_configs=config['society']['agents'],
        network_connections=config['society']['network']
    )

    # 4. 循环执行模拟剧本中的所有事件
    print("\n[主控] 开始执行模拟剧本...")
    for event in config['script']:
        action = event.get("action")
        parameters = event.get("parameters", {})
        
        if action == "run_tick":
            simulator.run_tick(event=event.get("event", "tick"))
        
        elif action == "introduce_dilemma":
            dilemma_config = parameters.get("dilemma", {})
            # 动态生成或创建困境
            if dilemma_config.get("core_concept") and llm_client:
                dilemma = simulator.generate_dilemma_with_llm(
                    core_concept=dilemma_config["core_concept"],
                    stakeholder_configs=dilemma_config.get("stakeholders", [])
                )
            else: # 如果没有LLM或核心概念，则使用预设值
                dilemma = EthicalCase(**dilemma_config) # 简化创建
            
            simulator.introduce_dilemma(parameters.get("agent_name"), dilemma)

        elif action == "introduce_external_shock":
            simulator.introduce_external_shock(
                shock_type=parameters.get("shock_type"),
                parameters=parameters
            )

    # 5. 导出最终的模拟历史
    export_path = config.get("settings", {}).get("export_file_path", "simulation_results.json")
    simulator.export_history(export_path)

    print(f"\n🎉 模拟完成！所有历史记录已保存到 '{export_path}'。")
    print("您现在可以将这份JSON文件用于您的前端可视化项目。")

if __name__ == "__main__":
    main()
