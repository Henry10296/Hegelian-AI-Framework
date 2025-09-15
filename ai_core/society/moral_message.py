# -*- coding: utf-8 -*-
"""
道德消息 (Moral Message)

定义了在AI社会中传播的“道德事件”或“道德消息”的数据结构。
这是道德传染过程中的基本信息单位。
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import time

# 避免在运行时产生循环导入，但在类型检查时提供智能提示
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..ethical_reasoning_framework import EthicalAgent
    # 修复ModuleNotFoundError: 从正确的路径导入MoralGenome
    from ..models.moral_genome import MoralGenome

@dataclass
class MoralMessage:
    """
    一个结构化的道德消息，包含了传播所需的所有要素。
    """
    # --- 必需参数（没有默认值），必须放在最前面 ---
    moral_content: 'MoralGenome'
    original_sender: 'EthicalAgent'

    # --- 可选参数（有默认值） ---
    text_content: str = ""
    emotional_valence: float = 0.0
    emotional_arousal: float = 0.5
    social_reward: float = 0.1
    group_relevance: float = 0.1
    urgency: float = 0.5
    credibility: float = 0.8
    
    # --- 自动生成的元数据 ---
    transmission_path: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self):
        # 自动将原始发送者添加到传播路径中
        if self.original_sender and self.original_sender.name not in self.transmission_path:
            self.transmission_path.append(self.original_sender.name)

    def calculate_decayed_influence(self) -> float:
        """
        计算消息因时间和传播距离而产生的衰减影响。
        """
        time_decay = 0.5 ** ((time.time() - self.timestamp) / 7.0)
        distance_decay = 1.0 / (1.0 + len(self.transmission_path))
        return self.credibility * time_decay * distance_decay

    def __repr__(self) -> str:
        return f"MoralMessage(from='{self.original_sender.name}', path_len={len(self.transmission_path)})"
