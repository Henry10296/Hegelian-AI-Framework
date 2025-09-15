# -*- coding: utf-8 -*-
"""
伦理推理框架 - (已修复) 一个具备社交能力的、可参与群体道德演化的智能体
"""

import logging
import random
from typing import Dict, Any, List, Tuple, TYPE_CHECKING

# 导入核心模块
from .models.ethical_case import EthicalCase, ActionOption
from .models.moral_genome import MoralGenome
from .moral_calculus import calculate_moral_vector

# 导入行为树框架
from .behavior_tree.node import Node
from .behavior_tree.composites import Selector, Sequence
from .action_library import ActionIdle, ActionExecuteChosen

# 避免在运行时产生循环导入
if TYPE_CHECKING:
    from .society.ai_entity_manager import AIEntityManager
    from .society.moral_message import MoralMessage
    from .moral_profiler import MoralProfiler

logger = logging.getLogger(__name__)

CULTURAL_INFLUENCE_THRESHOLD = 0.6
CULTURAL_ADJUSTMENT_FACTOR = 0.3

class ThoughtStream:
    """一个简单的类，用于记录AI连贯的思考过程。"""
    def __init__(self):
        self.thoughts: List[str] = []
    def add(self, thought: str, depth: int = 0): self.thoughts.append(f"{'  ' * depth}{thought}")
    def get_process(self) -> str: return "\n".join(self.thoughts)
    def clear(self): self.thoughts.clear()

class EthicalAgent:
    """
    一个能够参与社会互动的、可演化的伦理智能体。
    """

    def __init__(self, name: str, profiler: 'MoralProfiler', entity_manager: 'AIEntityManager'):
        self.name = name
        self.profiler = profiler
        self.entity_manager = entity_manager
        self.architecture = "social_context_aware_pareto_genetic"
        # 修复AttributeError: 将thought_stream提升为对象属性
        self.thought_stream = ThoughtStream()

        initial_intuitions = {
            "utilitarian": 0.5, "deontological": 0.5, "virtue": 0.5,
            "power_distance": 0.5, "individualism": 0.5, "uncertainty_avoidance": 0.5,
        }
        self.genome = MoralGenome(initial_intuitions)

        # 状态
        self.is_thinking = False
        self.current_dilemma: EthicalCase | None = None
        self.chosen_action: ActionOption | None = None
        self.message_inbox: List['MoralMessage'] = []

        self.behavior_tree: Node = self._build_behavior_tree()
        logger.info(f"社会性伦理智能体 {self.name} 已创建。")

    def _build_behavior_tree(self) -> Node:
        return Selector(name="Root Logic", children=[
            Sequence(name="Execute Chosen Action", children=[
                ActionExecuteChosen(name="Perform Chosen Action")
            ]),
            ActionIdle(name="Perform Idle")
        ])

    def tick(self):
        """AI的主“心跳”，现在包含社交处理。"""
        print(f"\n--- {self.name}'s Tick ---")
        self._process_social_influence()
        if self.is_thinking:
            self._resolve_dilemma()
        self.behavior_tree.tick(self)

    def broadcast_moral_message(self, action: ActionOption):
        """在执行一个行动后，向社会广播一个道德消息。"""
        message = self.entity_manager.create_message_from_action(self, action)
        print(f"   📣 [社交] {self.name} 向社会广播了一个道德事件: '{action.name}'")
        self.entity_manager.broadcast_message(message)

    def _process_social_influence(self):
        """处理收件箱中的道德消息，并决定是否被影响。"""
        if not self.message_inbox:
            return
        
        print(f"   📬 [社交] {self.name} 正在检查邮箱 ({len(self.message_inbox)}条新消息)... ")
        for message in self.message_inbox:
            probability = self.entity_manager.contagion_system.calculate_contagion_probability(message.original_sender, self, message)
            print(f"     - 评估来自 '{message.original_sender.name}' 的消息... 被说服的概率: {probability:.2f}")

            if random.random() < probability:
                print(f"       ✨ {self.name} 被 '{message.original_sender.name}' 的观点说服了！")
                self.entity_manager.evolver.evolve_towards(self, message.moral_content)
        
        self.message_inbox.clear()

    def _resolve_dilemma(self):
        if not self.current_dilemma: return
        self.thought_stream.clear()
        self.thought_stream.add(f"🤔 {self.name} 正在进行多目标道德权衡...")
        
        action_vectors = []
        for action in self.current_dilemma.action_options:
            vector = calculate_moral_vector(action, self.current_dilemma)
            action_vectors.append((action, vector))
            self.thought_stream.add(f"方案 '{action.name}' 的道德向量: {vector}", 1)

        pareto_front = self._find_pareto_front(action_vectors)
        self.thought_stream.add(f"帕累托最优解集: {[action.name for action, _ in pareto_front]}", 1)

        self.chosen_action = self._select_from_pareto_front(pareto_front)
        self.thought_stream.add(f"基因/文化驱动选择: 最终选择 '{self.chosen_action.name}'", 1)
        
        # 决策完成后，不再打印，而是等待“史官”来记录
        self.is_thinking = False

    def _find_pareto_front(self, action_vectors: List[Tuple[ActionOption, Dict[str, float]]]) -> List[Tuple[ActionOption, Dict[str, float]]]:
        pareto_front = []
        for i, (action1, vector1) in enumerate(action_vectors):
            is_dominated = False
            for j, (action2, vector2) in enumerate(action_vectors):
                if i == j: continue
                if all(vector2.get(dim, 0) >= vector1.get(dim, 0) for dim in vector1) and any(vector2.get(dim, 0) > vector1.get(dim, 0) for dim in vector1):
                    is_dominated = True
                    break
            if not is_dominated:
                pareto_front.append((action1, vector1))
        return pareto_front

    def _select_from_pareto_front(self, pareto_front: List[Tuple[ActionOption, Dict[str, float]]]) -> ActionOption:
        if not pareto_front: return self.current_dilemma.action_options[0]
        if len(pareto_front) == 1: return pareto_front[0][0]
        best_action = None
        max_final_score = -1
        weights = self.genome.get_intuitions()
        self.thought_stream.add("根据我的个性和文化背景进行最终权衡:", 2)

        for action, vector in pareto_front:
            base_score = sum(vector.get(dim, 0) * weights.get(dim, 0) for dim in ['utilitarian', 'deontological', 'virtue'])
            cultural_adjustment = 0.0
            if weights.get('power_distance', 0.5) > CULTURAL_INFLUENCE_THRESHOLD:
                cultural_adjustment += vector.get('deontological', 0) * (weights['power_distance'] - 0.5) * CULTURAL_ADJUSTMENT_FACTOR
            individualism_score = weights.get('individualism', 0.5)
            if individualism_score < (1 - CULTURAL_INFLUENCE_THRESHOLD):
                cultural_adjustment += vector.get('utilitarian', 0) * (0.5 - individualism_score) * CULTURAL_ADJUSTMENT_FACTOR
            elif individualism_score > CULTURAL_INFLUENCE_THRESHOLD:
                cultural_adjustment += vector.get('virtue', 0) * (individualism_score - 0.5) * CULTURAL_ADJUSTMENT_FACTOR
            if weights.get('uncertainty_avoidance', 0.5) > CULTURAL_INFLUENCE_THRESHOLD:
                uncertainty_penalty = action.metadata.get('uncertainty_score', 0.0) * (weights['uncertainty_avoidance'] - 0.5) * CULTURAL_ADJUSTMENT_FACTOR
                cultural_adjustment -= uncertainty_penalty
            final_score = base_score + cultural_adjustment
            self.thought_stream.add(f"评估 '{action.name}': 基础分={base_score:.2f}, 文化调整={cultural_adjustment:.2f} -> 最终分={final_score:.2f}", 3)
            if final_score > max_final_score:
                max_final_score = final_score
                best_action = action
        return best_action

    def face_dilemma(self, case: EthicalCase):
        print(f"\n🚨 {self.name} 遇到了一个新的困境: '{case.title}'")
        self.current_dilemma = case
        self.is_thinking = True

    def get_genome(self) -> MoralGenome:
        return self.genome

    def set_genome(self, new_genome: MoralGenome):
        self.genome = new_genome

    def get_moral_profile(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "architecture": self.architecture,
            "moral_intuitions": self.genome.get_intuitions(),
        }
