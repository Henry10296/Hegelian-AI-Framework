# -*- coding: utf-8 -*-
"""
道德传染系统 (Moral Contagion System)

该模块实现了基于MAD（动机、注意力、设计）模型的道德传染核心逻辑。
"""

from typing import TYPE_CHECKING

from .moral_message import MoralMessage

# 避免在运行时产生循环导入
if TYPE_CHECKING:
    from ..ethical_reasoning_framework import EthicalAgent
    from .social_network_manager import SocialNetworkManager

class MoralContagionSystem:
    """
    根据MAD模型，计算并处理道德消息在AI社会中的传播。
    """

    def __init__(self, network_manager: 'SocialNetworkManager', motivation_weight: float = 0.4, attention_weight: float = 0.3, design_weight: float = 0.3):
        self.network_manager = network_manager
        self.motivation_weight = motivation_weight
        self.attention_weight = attention_weight
        self.design_weight = design_weight

    def calculate_contagion_probability(self, sender: 'EthicalAgent', receiver: 'EthicalAgent', message: 'MoralMessage') -> float:
        """
        计算一个道德消息从发送者传播到接收者的总概率。

        Returns:
            float: 传播概率 (0.0 to 1.0).
        """
        # 1. 计算动机（Motivation）得分
        motivation_score = self._calculate_motivation(receiver, message)
        
        # 2. 计算注意力（Attention）得分
        attention_score = self._calculate_attention(sender, receiver, message)
        
        # 3. 计算网络设计（Design）得分
        design_score = self._calculate_design_influence(sender, receiver)
        
        # 根据权重将三者合成为最终的传播概率
        total_probability = (
            self.motivation_weight * motivation_score +
            self.attention_weight * attention_score +
            self.design_weight * design_score
        )
        
        # 考虑消息自身的衰减影响
        final_probability = total_probability * message.calculate_decayed_influence()
        return max(0.0, min(1.0, final_probability))

    def _calculate_motivation(self, receiver: 'EthicalAgent', message: 'MoralMessage') -> float:
        """计算接收者的动机得分。"""
        # 内在动机：接收者的价值观与消息内容的相似度
        # 我们使用两个基因组之间的“余弦相似度”来简化计算
        receiver_genes = receiver.get_genome().get_intuitions()
        message_genes = message.moral_content.get_intuitions()
        dot_product = sum(receiver_genes.get(k, 0) * message_genes.get(k, 0) for k in receiver_genes)
        # (此处省略了向量模长的计算以简化，实际应用中应包含)
        intrinsic_motivation = dot_product

        # 外在动机：消息附带的社会奖励价值
        # 假设AI有一个内在的“奖励敏感度”
        reward_sensitivity = receiver.get_genome().genes.get('utilitarian', 0.5) # 功利主义者更在乎奖励
        extrinsic_motivation = message.social_reward * reward_sensitivity
        
        # 简化返回，实际应用中可加入群体认同等更复杂的计算
        return (intrinsic_motivation + extrinsic_motivation) / 2.0

    def _calculate_attention(self, sender: 'EthicalAgent', receiver: 'EthicalAgent', message: 'MoralMessage') -> float:
        """计算消息获得的注意力得分。"""
        # 发送者影响力：简化为发送者的邻居数量（度中心性）
        sender_influence = len(self.network_manager.get_neighbors(sender.name)) / len(self.network_manager.agents)
        
        # 消息情感强度
        emotional_intensity = message.emotional_arousal * (abs(message.emotional_valence) + 0.5)

        # 简化返回，实际应用中可加入接收者认知负荷等
        return (sender_influence + emotional_intensity) / 2.0

    def _calculate_design_influence(self, sender: 'EthicalAgent', receiver: 'EthicalAgent') -> float:
        """计算网络设计对传播的影响得分。"""
        # 关系强度：简化为是否是直接邻居
        is_neighbor = receiver.name in self.network_manager.get_neighbors(sender.name)
        relationship_strength = 1.0 if is_neighbor else 0.2

        # 简化返回，实际应用中可加入网络距离、重复暴露等
        return relationship_strength
