# -*- coding: utf-8 -*-
"""
道德演化追踪器 (Moral Evolution Tracker) - (已升级) 包含社会宏观指标计算
"""

import json
import random
import numpy as np
from typing import Dict, List, Any
import time
from dataclasses import dataclass, asdict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ai_entity_manager import AIEntityManager
    from ..ethical_reasoning_framework import EthicalAgent

# --- 前端数据传输对象 (DTOs) ---

@dataclass
class AgentSnapshot:
    id: str
    position: Dict[str, float]
    moral_genome: Dict[str, float]
    last_thought: str = ""

@dataclass
class LinkSnapshot:
    source: str
    target: str

@dataclass
class SocietySnapshot:
    """(已升级) 整个社会在某个时间点的状态快照，现在包含宏观社会指标。"""
    tick: int
    event: str
    agents: List[AgentSnapshot]
    links: List[LinkSnapshot]
    network_polarization: float # 新增：社会极化度
    average_moral_diversity: float # 新增：道德多样性

# -------------------------------------

class MoralEvolutionTracker:
    """
    记录并导出AI社会道德演化历史的“史官”。
    """

    def __init__(self, entity_manager: 'AIEntityManager'):
        self.entity_manager = entity_manager
        self.history: List[SocietySnapshot] = []
        self._agent_positions = {agent.name: {"x": random.random() * 100, "y": random.random() * 100} for agent in entity_manager.get_all_agents()}

    def _calculate_network_polarization(self, agents: List['EthicalAgent']) -> float:
        """计算社会极化度：所有agent之间道德基因组的平均距离。"""
        if len(agents) < 2:
            return 0.0
        
        total_distance = 0.0
        num_comparisons = 0
        genomes = [np.array(list(agent.get_genome().get_intuitions().values())) for agent in agents]

        for i in range(len(genomes)):
            for j in range(i + 1, len(genomes)):
                # 使用欧氏距离计算两个基因组向量之间的距离
                distance = np.linalg.norm(genomes[i] - genomes[j])
                total_distance += distance
                num_comparisons += 1
        
        return total_distance / num_comparisons if num_comparisons > 0 else 0.0

    def _calculate_moral_diversity(self, agents: List['EthicalAgent']) -> float:
        """计算道德多样性：所有道德基因维度上的平均标准差。"""
        if not agents:
            return 0.0

        genomes_by_dim = {key: [] for key in agents[0].get_genome().get_intuitions().keys()}
        for agent in agents:
            for key, value in agent.get_genome().get_intuitions().items():
                genomes_by_dim[key].append(value)

        total_std_dev = 0.0
        for dim_values in genomes_by_dim.values():
            total_std_dev += np.std(dim_values)
        
        return total_std_dev / len(genomes_by_dim) if genomes_by_dim else 0.0

    def record_snapshot(self, tick_num: int, event: str = "tick"):
        """(已升级) 记录快照，现在包含计算和存储宏观指标。"""
        print(f"[记录官] 正在记录时间点 {tick_num} 的社会状态快照 (事件: {event})...")
        
        all_agents = self.entity_manager.get_all_agents()
        
        agent_snapshots = []
        for agent in all_agents:
            snapshot = AgentSnapshot(
                id=agent.name,
                position=self._agent_positions.get(agent.name, {"x": 0, "y": 0}),
                moral_genome=agent.get_genome().get_intuitions(),
                last_thought=agent.thought_stream.get_process() # 统一导出思考过程
            )
            agent_snapshots.append(snapshot)

        link_snapshots = []
        if self.entity_manager.network_manager:
            for agent_name, neighbors in self.entity_manager.network_manager.adjacency_list.items():
                if agent_name < neighbor_name:
                    link_snapshots.append(LinkSnapshot(source=agent_name, target=neighbor_name))

        society_snapshot = SocietySnapshot(
            tick=tick_num,
            event=event,
            agents=agent_snapshots,
            links=link_snapshots,
            network_polarization=self._calculate_network_polarization(all_agents),
            average_moral_diversity=self._calculate_moral_diversity(all_agents)
        )
        self.history.append(society_snapshot)

    def export_to_json(self, file_path: str):
        print(f"\n[记录官] 正在将前端友好的演化历史导出到: {file_path}")
        history_as_dicts = [asdict(snapshot) for snapshot in self.history]
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(history_as_dicts, f, ensure_ascii=False, indent=4)
            print(f"✅ 导出成功！")
        except IOError as e:
            print(f"❌ 导出失败: {e}")
