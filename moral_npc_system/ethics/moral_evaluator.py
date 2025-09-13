"""
道德评估器 - 统一的道德行为评估接口
"""

from typing import Dict, List, Any, Optional
from ..core.action import Action
from ..core.moral_state import MoralState
from .kantian_ethics import KantianEthics
from .utilitarian_ethics import UtilitarianEthics
from .virtue_ethics import VirtueEthics


class MoralEvaluator:
    """统一的道德评估器"""
    
    def __init__(self):
        self.kantian_ethics = KantianEthics()
        self.utilitarian_ethics = UtilitarianEthics()
        self.virtue_ethics = VirtueEthics()
    
    def comprehensive_evaluation(self, action: Action, moral_state: MoralState, 
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """综合道德评估"""
        
        # 各框架评估
        kantian_score = self.kantian_ethics.evaluate_action(action, context)
        utilitarian_score = self.utilitarian_ethics.evaluate_action(action, context)
        virtue_score = self.virtue_ethics.evaluate_action(action, context)
        
        # 加权综合
        weighted_score = (
            kantian_score * moral_state.kantian_weight +
            utilitarian_score * moral_state.utilitarian_weight +
            virtue_score * moral_state.virtue_weight
        )
        
        return {
            'action_summary': {
                'type': action.action_type.value,
                'actor': action.actor_id,
                'target': action.target_id,
                'intensity': action.intensity
            },
            'framework_scores': {
                'kantian': kantian_score,
                'utilitarian': utilitarian_score,
                'virtue_ethics': virtue_score
            },
            'weighted_score': weighted_score,
            'moral_weights': {
                'kantian_weight': moral_state.kantian_weight,
                'utilitarian_weight': moral_state.utilitarian_weight,
                'virtue_weight': moral_state.virtue_weight
            },
            'recommendation': self._generate_recommendation(weighted_score),
            'detailed_explanations': {
                'kantian': self.kantian_ethics.explain_evaluation(action, context),
                'utilitarian': self.utilitarian_ethics.explain_evaluation(action, context),
                'virtue': self.virtue_ethics.explain_evaluation(action, context)
            }
        }
    
    def _generate_recommendation(self, score: float) -> str:
        """生成行为建议"""
        if score >= 0.8:
            return "强烈推荐 - 这是一个道德上优秀的行为选择"
        elif score >= 0.6:
            return "推荐 - 这是一个道德上良好的行为选择"
        elif score >= 0.4:
            return "可接受 - 这是一个道德上可接受的行为选择"
        elif score >= 0.2:
            return "不推荐 - 这个行为在道德上存在问题"
        else:
            return "强烈反对 - 这个行为在道德上是有害的"