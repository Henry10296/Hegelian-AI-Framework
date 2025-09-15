# -*- coding: utf-8 -*-
"""
AI社会模拟器 (已升级为“虚拟社会实验室”)

该模拟器现在拥有动态生成困境、引入外部冲击和完全自定义的能力。
"""

import json
from typing import List, Dict

# 导入所有核心模块
from ..society.ai_entity_manager import AIEntityManager
from ..society.moral_evolution_tracker import MoralEvolutionTracker
from ..models.ethical_case import EthicalCase, ActionOption, Stakeholder
from ..models.moral_genome import MoralGenome
from ..society.moral_message import MoralMessage

# 导入LLM客户端（如果可用）
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class AISocietySimulator:
    """
    一个高级模拟器，封装了创建、运行和记录可自定义的AI社会实验的所有复杂性。
    """

    def __init__(self, llm_client: 'OpenAI' = None):
        print("🚀 初始化AI社会模拟器...")
        self.entity_manager = AIEntityManager()
        self.tracker: MoralEvolutionTracker | None = None
        self.llm_client = llm_client
        self.current_tick = 0

    def setup_society(self, agent_configs: List[Dict], network_connections: List[tuple]):
        print("[模拟器] 正在设置社会...")
        self.entity_manager.populate_society(agent_configs)
        self.tracker = MoralEvolutionTracker(self.entity_manager)
        for agent1_name, agent2_name in network_connections:
            self.entity_manager.network_manager.add_connection(agent1_name, agent2_name)
        print("[模拟器] 社会设置完毕。")

    def introduce_external_shock(self, shock_type: str, parameters: Dict):
        """(新增) 向社会引入一次“外部冲击”。"""
        print(f"\n⚡️ [外部冲击] 正在向社会施加一次 '{shock_type}' 冲击...")
        event_description = f"External Shock: {shock_type}"
        
        if shock_type == "IDEOLOGICAL_BOMB":
            # 向社会中的每一个AI广播一个统一的、强烈的道德消息
            genome_data = parameters.get("genome", {})
            message_genome = MoralGenome(genome_data)
            # 创建一个没有“原始发送者”的、来自“外部”的消息
            ideological_message = MoralMessage(moral_content=message_genome, original_sender=None, text_content=parameters.get("text", "A new idea has arrived."))
            
            for agent in self.entity_manager.get_all_agents():
                agent.message_inbox.append(ideological_message)
            event_description += f" with content {genome_data}"

        elif shock_type == "RESOURCE_SQUEEZE":
            # 直接调整社会中每个AI的某个基因的权重
            gene_to_change = parameters.get("gene", "utilitarian")
            factor = parameters.get("factor", 1.0)
            for agent in self.entity_manager.get_all_agents():
                current_value = agent.get_genome().genes.get(gene_to_change, 0.5)
                new_value = max(0.0, min(1.0, current_value * factor))
                agent.get_genome().genes[gene_to_change] = new_value
            event_description += f" on {gene_to_change} by factor {factor}"
        
        # 在施加冲击后，立即运行一个特殊的时间步来观察其直接效果
        self.run_tick(event=event_description)

    def generate_dilemma_with_llm(self, core_concept: str, stakeholder_configs: List[Dict]) -> EthicalCase | None:
        if not self.llm_client: return None
        # ... (LLM生成困境的逻辑保持不变) ...
        return None # 简化演示

    def run_tick(self, event: str = "tick"):
        self.current_tick += 1
        print(f"\n================== 模拟时间步: {self.current_tick} (事件: {event}) ==================")
        self.entity_manager.tick_all()
        if self.tracker: self.tracker.record_snapshot(self.current_tick, event)

    def introduce_dilemma(self, agent_name: str, dilemma: EthicalCase):
        agent = self.entity_manager.get_agent(agent_name)
        if agent and dilemma:
            agent.face_dilemma(dilemma)
        elif not agent:
            print(f"⚠️ [模拟器] 警告: 无法找到名为 '{agent_name}' 的AI。")

    def export_history(self, file_path: str):
        if self.tracker: self.tracker.export_to_json(file_path)
