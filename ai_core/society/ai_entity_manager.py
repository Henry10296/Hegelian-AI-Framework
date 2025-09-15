# -*- coding: utf-8 -*-
"""
AI实体管理器 (AI Entity Manager) - AI社会的“主控制器”

它现在负责创建、管理并连接所有的社会子系统。
"""

from typing import Dict, List
import copy

from ..ethical_reasoning_framework import EthicalAgent
from ..moral_profiler import MoralProfiler
from ..moral_evolver import MoralEvolver
from ..models.ethical_case import ActionOption
from .social_network_manager import SocialNetworkManager
from .moral_contagion_system import MoralContagionSystem
from .moral_message import MoralMessage

class AIEntityManager:
    """
    管理整个AI社会，包括所有智能体和他们之间的交互系统。
    """

    def __init__(self):
        self.agents: Dict[str, EthicalAgent] = {}
        # 管理器现在持有所有社会子系统的实例
        self.network_manager: SocialNetworkManager | None = None
        self.contagion_system: MoralContagionSystem | None = None
        self.evolver = MoralEvolver() # 演化器是通用的，直接创建

    def populate_society(self, agent_configs: List[Dict]) -> List[EthicalAgent]:
        """根据配置列表，批量创建AI并初始化社会。"""
        for config in agent_configs:
            self.create_agent(name=config['name'], initial_genome=config.get('genome'))
        
        all_agents = self.get_all_agents()
        self.network_manager = SocialNetworkManager(all_agents)
        self.contagion_system = MoralContagionSystem(self.network_manager)
        return all_agents

    def create_agent(self, name: str, initial_genome: Dict[str, float] = None) -> EthicalAgent:
        """创建一个新的伦理智能体，并注入对管理器的引用。"""
        if name in self.agents:
            raise ValueError(f"Agent with name '{name}' already exists.")
        
        profiler = MoralProfiler(use_llm=False)
        # 将对自身的引用(self)传递给新创建的agent，使其能够与社会交互
        agent = EthicalAgent(name, profiler, self)

        if initial_genome:
            agent.get_genome().genes = initial_genome
        
        self.agents[name] = agent
        print(f"[社会] 成员 '{name}' 已诞生。")
        return agent

    def create_message_from_action(self, sender: 'EthicalAgent', action: 'ActionOption') -> 'MoralMessage':
        """根据一个AI执行的行动，方便地“包装”出一个道德消息。"""
        return MoralMessage(
            original_sender=sender,
            moral_content=copy.deepcopy(sender.get_genome()), # 附上发送者当前的道德基因组
            text_content=f"I chose to '{action.name}'",
            credibility=0.9 # 亲眼所见的行为，可信度高
        )

    def broadcast_message(self, message: 'MoralMessage'):
        """将一个道德消息广播给发送者的所有邻居。"""
        if not self.network_manager:
            return

        sender_name = message.original_sender.name
        neighbors = self.network_manager.get_neighbors(sender_name)
        print(f"   📬 [广播] '{sender_name}' 的消息正在发送给 {len(neighbors)} 个邻居: {neighbors}")

        for neighbor_name in neighbors:
            neighbor_agent = self.get_agent(neighbor_name)
            if neighbor_agent:
                # 将消息放入邻居的“邮箱”
                neighbor_agent.message_inbox.append(message)

    def get_agent(self, name: str) -> EthicalAgent | None:
        return self.agents.get(name)

    def get_all_agents(self) -> List[EthicalAgent]:
        return list(self.agents.values())

    def tick_all(self):
        """触发所有智能体的主“心跳”。"""
        for agent in self.agents.values():
            agent.tick()
