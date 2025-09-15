# -*- coding: utf-8 -*-
"""
社交网络管理器 (Social Network Manager)

负责生成和管理AI社会中的社交网络结构。
"""

import random
from typing import Dict, List, Set
from ..ethical_reasoning_framework import EthicalAgent

class SocialNetworkManager:
    """
    管理AI个体之间的社交关系图谱。
    """

    def __init__(self, agents: List[EthicalAgent]):
        self.agents = agents
        # 使用邻接表来表示社交图谱，每个agent都映射到一个其“朋友”的集合
        self.adjacency_list: Dict[str, Set[str]] = {agent.name: set() for agent in agents}

    def get_neighbors(self, agent_name: str) -> List[str]:
        """获取一个AI的所有邻居（朋友）。"""
        return list(self.adjacency_list.get(agent_name, set()))

    def add_connection(self, agent1_name: str, agent2_name: str):
        """建立一个双向的社交连接。"""
        if agent1_name in self.adjacency_list and agent2_name in self.adjacency_list:
            self.adjacency_list[agent1_name].add(agent2_name)
            self.adjacency_list[agent2_name].add(agent1_name)

    def generate_small_world_network(self, k_neighbors: int, rewiring_prob: float):
        """
        生成一个Watts-Strogatz小世界网络。

        Args:
            k_neighbors (int): 每个节点连接的最近邻居数量（必须是偶数）。
            rewiring_prob (float): 随机重连的概率。
        """
        print(f"[社会] 正在生成小世界网络 (k={k_neighbors}, p={rewiring_prob})...")
        agent_names = list(self.adjacency_list.keys())
        n = len(agent_names)
        if n < k_neighbors + 1:
            print("⚠️ 警告: Agent数量过少，无法生成指定的小世界网络。")
            return

        # 1. 创建一个规则的环形网络
        for i in range(n):
            for j in range(1, k_neighbors // 2 + 1):
                neighbor_index = (i + j) % n
                self.add_connection(agent_names[i], agent_names[neighbor_index])

        # 2. 随机重连
        for i in range(n):
            agent_name = agent_names[i]
            neighbors_to_rewire = list(self.adjacency_list[agent_name])
            for neighbor_name in neighbors_to_rewire:
                if random.random() < rewiring_prob:
                    # 选择一个新的、不重复的、非自身的节点进行连接
                    possible_new_neighbors = [name for name in agent_names if name != agent_name and name not in self.adjacency_list[agent_name]]
                    if possible_new_neighbors:
                        new_neighbor = random.choice(possible_new_neighbors)
                        # 断开旧连接，建立新连接
                        self.adjacency_list[agent_name].remove(neighbor_name)
                        self.adjacency_list[neighbor_name].remove(agent_name)
                        self.add_connection(agent_name, new_neighbor)
        print("[社会] 社交网络已生成。")

    def __repr__(self) -> str:
        return f"SocialNetworkManager(NodeCount={len(self.agents)})"
