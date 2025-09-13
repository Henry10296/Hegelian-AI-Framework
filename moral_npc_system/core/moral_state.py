"""
NPC道德状态管理
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np


@dataclass
class MoralState:
    """NPC的道德状态"""
    
    # 道德倾向权重 (总和为1.0)
    kantian_weight: float = 0.33      # 康德道德权重
    utilitarian_weight: float = 0.33  # 功利主义权重
    virtue_weight: float = 0.34       # 美德伦理权重
    
    # 道德情感参数
    empathy_level: float = 0.5        # 共情能力 [0-1]
    guilt_sensitivity: float = 0.5    # 愧疚敏感度 [0-1]
    moral_courage: float = 0.5        # 道德勇气 [0-1]
    
    # 环境敏感度
    context_sensitivity: float = 0.5  # 情境敏感度 [0-1]
    social_pressure_resistance: float = 0.5  # 社会压力抵抗 [0-1]
    
    # 学习参数
    moral_plasticity: float = 0.3     # 道德可塑性 [0-1]
    learning_rate: float = 0.1        # 学习速率
    
    # 历史记录
    moral_experiences: List[Dict] = None
    
    def __post_init__(self):
        if self.moral_experiences is None:
            self.moral_experiences = []
        self._normalize_weights()
    
    def _normalize_weights(self):
        """标准化道德权重，确保总和为1.0"""
        total = self.kantian_weight + self.utilitarian_weight + self.virtue_weight
        if total > 0:
            self.kantian_weight /= total
            self.utilitarian_weight /= total
            self.virtue_weight /= total
    
    def get_dominant_moral_framework(self) -> str:
        """获取主导的道德框架"""
        weights = {
            'kantian': self.kantian_weight,
            'utilitarian': self.utilitarian_weight,
            'virtue': self.virtue_weight
        }
        return max(weights.items(), key=lambda x: x[1])[0]
    
    def update_from_experience(self, action_type: str, outcome: float, social_feedback: float):
        """根据经验更新道德状态"""
        experience = {
            'action': action_type,
            'outcome': outcome,
            'social_feedback': social_feedback,
            'timestamp': len(self.moral_experiences)
        }
        self.moral_experiences.append(experience)
        
        # 基于经验调整道德参数
        if outcome > 0 and social_feedback > 0:
            # 正面经验增强相应的道德倾向
            adjustment = self.learning_rate * self.moral_plasticity
            
            if 'help' in action_type or 'share' in action_type:
                self.empathy_level = min(1.0, self.empathy_level + adjustment)
            
            if 'sacrifice' in action_type:
                self.moral_courage = min(1.0, self.moral_courage + adjustment)
        
        elif outcome < 0 or social_feedback < 0:
            # 负面经验增强愧疚感
            adjustment = self.learning_rate * self.moral_plasticity
            self.guilt_sensitivity = min(1.0, self.guilt_sensitivity + adjustment)
    
    def calculate_moral_stress(self) -> float:
        """计算当前的道德压力水平"""
        recent_negative_exp = sum(1 for exp in self.moral_experiences[-10:] 
                                if exp['outcome'] < 0 or exp['social_feedback'] < 0)
        
        base_stress = recent_negative_exp / 10.0
        guilt_factor = self.guilt_sensitivity * 0.5
        
        return min(1.0, base_stress + guilt_factor)
    
    def moral_distance_to(self, other: 'MoralState') -> float:
        """计算与另一个道德状态的距离"""
        weight_diff = abs(self.kantian_weight - other.kantian_weight) + \
                     abs(self.utilitarian_weight - other.utilitarian_weight) + \
                     abs(self.virtue_weight - other.virtue_weight)
        
        emotion_diff = abs(self.empathy_level - other.empathy_level) + \
                      abs(self.guilt_sensitivity - other.guilt_sensitivity) + \
                      abs(self.moral_courage - other.moral_courage)
        
        return (weight_diff + emotion_diff) / 2.0
    
    def copy(self) -> 'MoralState':
        """创建道德状态的副本"""
        return MoralState(
            kantian_weight=self.kantian_weight,
            utilitarian_weight=self.utilitarian_weight,
            virtue_weight=self.virtue_weight,
            empathy_level=self.empathy_level,
            guilt_sensitivity=self.guilt_sensitivity,
            moral_courage=self.moral_courage,
            context_sensitivity=self.context_sensitivity,
            social_pressure_resistance=self.social_pressure_resistance,
            moral_plasticity=self.moral_plasticity,
            learning_rate=self.learning_rate,
            moral_experiences=self.moral_experiences.copy()
        )