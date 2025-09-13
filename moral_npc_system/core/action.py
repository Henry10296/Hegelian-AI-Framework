"""
行为和行为类型定义
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import uuid


class ActionType(Enum):
    """行为类型枚举"""
    HELP = "help"           # 帮助行为
    HARM = "harm"           # 伤害行为
    TRADE = "trade"         # 交易行为
    COMMUNICATE = "communicate"  # 交流行为
    IGNORE = "ignore"       # 忽视行为
    COOPERATE = "cooperate" # 合作行为
    COMPETE = "compete"     # 竞争行为
    SACRIFICE = "sacrifice" # 牺牲行为
    DECEIVE = "deceive"     # 欺骗行为
    SHARE = "share"         # 分享行为


@dataclass
class Action:
    """行为对象"""
    id: str
    action_type: ActionType
    actor_id: str
    target_id: Optional[str] = None
    context: Dict[str, Any] = None
    intensity: float = 1.0  # 行为强度 [0-1]
    consequences: List[str] = None
    timestamp: float = 0.0
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.context is None:
            self.context = {}
        if self.consequences is None:
            self.consequences = []
    
    @property
    def is_moral_relevant(self) -> bool:
        """判断行为是否具有道德意义"""
        moral_relevant_actions = {
            ActionType.HELP, ActionType.HARM, ActionType.SACRIFICE,
            ActionType.DECEIVE, ActionType.SHARE, ActionType.COOPERATE
        }
        return self.action_type in moral_relevant_actions
    
    @property
    def affects_others(self) -> bool:
        """判断行为是否影响他人"""
        return self.target_id is not None and self.target_id != self.actor_id
    
    def get_moral_weight(self) -> float:
        """获取行为的道德权重"""
        weights = {
            ActionType.HELP: 0.8,
            ActionType.HARM: -0.9,
            ActionType.SACRIFICE: 0.9,
            ActionType.DECEIVE: -0.7,
            ActionType.SHARE: 0.6,
            ActionType.COOPERATE: 0.5,
            ActionType.COMPETE: -0.2,
            ActionType.TRADE: 0.1,
            ActionType.COMMUNICATE: 0.1,
            ActionType.IGNORE: -0.1
        }
        base_weight = weights.get(self.action_type, 0.0)
        return base_weight * self.intensity