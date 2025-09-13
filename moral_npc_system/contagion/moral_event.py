"""
道德事件类 - 定义可传播的道德事件
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import uuid
import time


class MoralEventType(Enum):
    """道德事件类型"""
    ALTRUISTIC_ACT = "altruistic_act"       # 利他行为
    SELFISH_ACT = "selfish_act"             # 自私行为
    COOPERATION = "cooperation"              # 合作行为
    BETRAYAL = "betrayal"                   # 背叛行为
    JUSTICE_ACTION = "justice_action"       # 正义行为
    CORRUPTION = "corruption"               # 腐败行为
    SACRIFICE = "sacrifice"                 # 牺牲行为
    EXPLOITATION = "exploitation"           # 剥削行为
    FORGIVENESS = "forgiveness"             # 宽恕行为
    REVENGE = "revenge"                     # 报复行为


class MoralValence(Enum):
    """道德价值倾向"""
    POSITIVE = "positive"     # 正面道德影响
    NEGATIVE = "negative"     # 负面道德影响
    NEUTRAL = "neutral"       # 中性影响
    AMBIGUOUS = "ambiguous"   # 模糊/复杂的道德影响


@dataclass
class MoralEvent:
    """道德事件"""
    
    event_id: str
    event_type: MoralEventType
    valence: MoralValence
    
    # 事件参与者
    primary_actor: str
    target: Optional[str] = None
    witnesses: List[str] = None
    
    # 事件特征
    intensity: float = 1.0          # 事件强度 [0-1]
    visibility: float = 1.0         # 可见性 [0-1]
    moral_weight: float = 1.0       # 道德权重 [0-1]
    
    # 情境信息
    context: Dict[str, Any] = None
    consequences: List[str] = None
    
    # 时间信息
    timestamp: float = 0.0
    duration: float = 0.0
    
    # 传播参数
    initial_influence_strength: float = 1.0
    decay_rate: float = 0.1
    max_propagation_distance: int = 3
    
    def __post_init__(self):
        if self.event_id is None:
            self.event_id = str(uuid.uuid4())
        if self.witnesses is None:
            self.witnesses = []
        if self.context is None:
            self.context = {}
        if self.consequences is None:
            self.consequences = []
        if self.timestamp == 0.0:
            self.timestamp = time.time()
    
    @property
    def moral_impact_score(self) -> float:
        """计算道德影响分数"""
        base_score = self.intensity * self.moral_weight
        
        # 根据价值倾向调整
        if self.valence == MoralValence.POSITIVE:
            return base_score
        elif self.valence == MoralValence.NEGATIVE:
            return -base_score
        elif self.valence == MoralValence.AMBIGUOUS:
            return base_score * 0.5  # 模糊事件影响减半
        else:  # NEUTRAL
            return 0.0
    
    @property
    def propagation_strength(self) -> float:
        """计算传播强度"""
        visibility_factor = self.visibility
        intensity_factor = self.intensity
        moral_factor = abs(self.moral_impact_score)
        
        return (visibility_factor * intensity_factor * moral_factor) ** 0.5
    
    def get_influence_on_moral_dimension(self, dimension: str) -> float:
        """获取对特定道德维度的影响"""
        base_influence = self.moral_impact_score
        
        # 不同事件类型对不同道德维度的影响程度不同
        dimension_weights = self._get_dimension_weights()
        
        weight = dimension_weights.get(dimension, 0.5)
        return base_influence * weight
    
    def _get_dimension_weights(self) -> Dict[str, float]:
        """获取事件类型对各道德维度的影响权重"""
        weights_map = {
            MoralEventType.ALTRUISTIC_ACT: {
                'empathy': 0.9,
                'compassion': 0.8,
                'cooperation': 0.7,
                'fairness': 0.6
            },
            MoralEventType.SELFISH_ACT: {
                'empathy': -0.6,
                'self_interest': 0.8,
                'competition': 0.7,
                'individualism': 0.9
            },
            MoralEventType.COOPERATION: {
                'cooperation': 0.9,
                'trust': 0.8,
                'social_harmony': 0.7,
                'collective_good': 0.8
            },
            MoralEventType.BETRAYAL: {
                'trust': -0.9,
                'cooperation': -0.7,
                'cynicism': 0.6,
                'self_protection': 0.5
            },
            MoralEventType.JUSTICE_ACTION: {
                'fairness': 0.9,
                'righteousness': 0.8,
                'rule_adherence': 0.7,
                'moral_courage': 0.6
            },
            MoralEventType.CORRUPTION: {
                'fairness': -0.8,
                'trust': -0.7,
                'cynicism': 0.6,
                'power_abuse': 0.8
            },
            MoralEventType.SACRIFICE: {
                'altruism': 0.9,
                'moral_courage': 0.8,
                'selflessness': 0.9,
                'duty': 0.7
            },
            MoralEventType.EXPLOITATION: {
                'fairness': -0.8,
                'empathy': -0.6,
                'power_abuse': 0.7,
                'dominance': 0.6
            },
            MoralEventType.FORGIVENESS: {
                'compassion': 0.8,
                'healing': 0.7,
                'reconciliation': 0.9,
                'mercy': 0.8
            },
            MoralEventType.REVENGE: {
                'justice': 0.5,
                'anger': 0.8,
                'retribution': 0.9,
                'cycle_of_harm': -0.6
            }
        }
        
        return weights_map.get(self.event_type, {})
    
    def calculate_time_decay(self, current_time: float) -> float:
        """计算时间衰减因子"""
        time_elapsed = current_time - self.timestamp
        if time_elapsed <= 0:
            return 1.0
        
        # 指数衰减
        decay_factor = np.exp(-self.decay_rate * time_elapsed)
        return max(0.0, decay_factor)
    
    def is_similar_to(self, other_event: 'MoralEvent', threshold: float = 0.7) -> bool:
        """判断与另一个事件是否相似"""
        if self.event_type != other_event.event_type:
            return False
        
        if self.valence != other_event.valence:
            return False
        
        # 检查参与者重叠
        actor_similarity = 1.0 if self.primary_actor == other_event.primary_actor else 0.0
        target_similarity = 1.0 if self.target == other_event.target else 0.0
        
        # 检查情境相似性
        context_similarity = self._calculate_context_similarity(other_event)
        
        overall_similarity = (actor_similarity + target_similarity + context_similarity) / 3.0
        
        return overall_similarity >= threshold
    
    def _calculate_context_similarity(self, other_event: 'MoralEvent') -> float:
        """计算情境相似性"""
        if not self.context or not other_event.context:
            return 0.5
        
        common_keys = set(self.context.keys()) & set(other_event.context.keys())
        if not common_keys:
            return 0.0
        
        similarities = []
        for key in common_keys:
            val1 = self.context[key]
            val2 = other_event.context[key]
            
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # 数值比较
                max_val = max(abs(val1), abs(val2), 1.0)
                similarity = 1.0 - abs(val1 - val2) / max_val
            elif val1 == val2:
                # 相等比较
                similarity = 1.0
            else:
                similarity = 0.0
            
            similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 0.0
    
    def create_follow_up_event(self, new_actor: str, response_type: str) -> 'MoralEvent':
        """创建后续反应事件"""
        response_event_types = {
            'inspired': MoralEventType.ALTRUISTIC_ACT,
            'emulated': self.event_type,
            'opposed': self._get_opposite_event_type(),
            'retaliated': MoralEventType.REVENGE
        }
        
        new_event_type = response_event_types.get(response_type, self.event_type)
        
        return MoralEvent(
            event_id=str(uuid.uuid4()),
            event_type=new_event_type,
            valence=self._get_response_valence(response_type),
            primary_actor=new_actor,
            target=self.primary_actor,
            intensity=self.intensity * 0.8,  # 略微减弱
            visibility=self.visibility * 0.7,
            moral_weight=self.moral_weight,
            context={
                'triggered_by': self.event_id,
                'response_type': response_type,
                **self.context
            }
        )
    
    def _get_opposite_event_type(self) -> MoralEventType:
        """获取相反的事件类型"""
        opposites = {
            MoralEventType.ALTRUISTIC_ACT: MoralEventType.SELFISH_ACT,
            MoralEventType.SELFISH_ACT: MoralEventType.ALTRUISTIC_ACT,
            MoralEventType.COOPERATION: MoralEventType.BETRAYAL,
            MoralEventType.BETRAYAL: MoralEventType.COOPERATION,
            MoralEventType.JUSTICE_ACTION: MoralEventType.CORRUPTION,
            MoralEventType.CORRUPTION: MoralEventType.JUSTICE_ACTION,
            MoralEventType.SACRIFICE: MoralEventType.EXPLOITATION,
            MoralEventType.EXPLOITATION: MoralEventType.SACRIFICE,
            MoralEventType.FORGIVENESS: MoralEventType.REVENGE,
            MoralEventType.REVENGE: MoralEventType.FORGIVENESS
        }
        
        return opposites.get(self.event_type, self.event_type)
    
    def _get_response_valence(self, response_type: str) -> MoralValence:
        """获取回应事件的价值倾向"""
        if response_type in ['inspired', 'emulated']:
            return self.valence
        elif response_type == 'opposed':
            valence_opposites = {
                MoralValence.POSITIVE: MoralValence.NEGATIVE,
                MoralValence.NEGATIVE: MoralValence.POSITIVE,
                MoralValence.NEUTRAL: MoralValence.NEUTRAL,
                MoralValence.AMBIGUOUS: MoralValence.AMBIGUOUS
            }
            return valence_opposites.get(self.valence, MoralValence.NEUTRAL)
        else:
            return MoralValence.AMBIGUOUS
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type.value,
            'valence': self.valence.value,
            'primary_actor': self.primary_actor,
            'target': self.target,
            'witnesses': self.witnesses,
            'intensity': self.intensity,
            'visibility': self.visibility,
            'moral_weight': self.moral_weight,
            'context': self.context,
            'consequences': self.consequences,
            'timestamp': self.timestamp,
            'duration': self.duration,
            'moral_impact_score': self.moral_impact_score,
            'propagation_strength': self.propagation_strength
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MoralEvent':
        """从字典创建事件"""
        return cls(
            event_id=data['event_id'],
            event_type=MoralEventType(data['event_type']),
            valence=MoralValence(data['valence']),
            primary_actor=data['primary_actor'],
            target=data.get('target'),
            witnesses=data.get('witnesses', []),
            intensity=data.get('intensity', 1.0),
            visibility=data.get('visibility', 1.0),
            moral_weight=data.get('moral_weight', 1.0),
            context=data.get('context', {}),
            consequences=data.get('consequences', []),
            timestamp=data.get('timestamp', time.time()),
            duration=data.get('duration', 0.0)
        )


# 导入numpy，如果没有则使用math
try:
    import numpy as np
except ImportError:
    import math
    class np:
        @staticmethod
        def exp(x):
            return math.exp(x)
        
        @staticmethod
        def mean(values):
            return sum(values) / len(values) if values else 0.0