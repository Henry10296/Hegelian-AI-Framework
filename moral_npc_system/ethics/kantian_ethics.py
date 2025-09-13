"""
康德定言命令的可计算实现

基于康德的三个定言命令公式：
1. 普遍法则公式：只有当你能够意愿你的行为准则成为普遍法则时，才按此准则行动
2. 人性公式：永远要把人(无论是你自己还是任何其他人)当作目的，而不仅仅当作手段
3. 自律公式：只按照你自己制定的、能够同时成为普遍立法的准则行动
"""

import math
from typing import Dict, List, Any, Optional
from ..core.action import Action, ActionType
from ..core.moral_state import MoralState


class KantianEthics:
    """康德伦理学计算引擎"""
    
    def __init__(self):
        # 行为的普遍化可能性权重
        self.universalizability_weights = {
            ActionType.HELP: 0.9,        # 帮助行为高度可普遍化
            ActionType.SHARE: 0.8,       # 分享行为高度可普遍化
            ActionType.COOPERATE: 0.7,   # 合作行为较可普遍化
            ActionType.TRADE: 0.6,       # 公平交易可普遍化
            ActionType.COMMUNICATE: 0.5, # 交流行为中性
            ActionType.IGNORE: 0.3,      # 忽视行为较难普遍化
            ActionType.COMPETE: 0.2,     # 竞争行为难以普遍化
            ActionType.DECEIVE: 0.1,     # 欺骗行为几乎不可普遍化
            ActionType.HARM: 0.0,        # 伤害行为不可普遍化
            ActionType.SACRIFICE: 0.4,   # 牺牲行为复杂，取决于情境
        }
        
        # 人性尊严权重 (将人当作目的而非手段)
        self.humanity_dignity_weights = {
            ActionType.HELP: 0.9,        # 帮助体现人的尊严
            ActionType.SHARE: 0.8,       # 分享尊重他人需求
            ActionType.SACRIFICE: 0.9,   # 牺牲体现对他人的尊重
            ActionType.COOPERATE: 0.7,   # 合作平等对待他人
            ActionType.TRADE: 0.6,       # 公平交易尊重对方
            ActionType.COMMUNICATE: 0.5, # 交流体现基本尊重
            ActionType.IGNORE: 0.3,      # 忽视缺乏尊重
            ActionType.COMPETE: 0.4,     # 竞争可能工具化他人
            ActionType.DECEIVE: 0.1,     # 欺骗严重工具化他人
            ActionType.HARM: 0.0,        # 伤害完全违背人的尊严
        }
    
    def evaluate_action(self, action: Action, context: Dict[str, Any]) -> float:
        """
        根据康德伦理学评估行为的道德性
        
        返回值: [0, 1] 之间的道德评分，1表示完全符合康德伦理学
        """
        # 第一公式：普遍法则检验
        universalizability = self._evaluate_universalizability(action, context)
        
        # 第二公式：人性尊严检验  
        humanity_respect = self._evaluate_humanity_respect(action, context)
        
        # 第三公式：理性自律检验
        rational_autonomy = self._evaluate_rational_autonomy(action, context)
        
        # 综合评分 (人性公式权重最高)
        moral_score = (
            universalizability * 0.3 +
            humanity_respect * 0.5 +
            rational_autonomy * 0.2
        )
        
        return max(0.0, min(1.0, moral_score))
    
    def _evaluate_universalizability(self, action: Action, context: Dict[str, Any]) -> float:
        """评估行为的普遍化可能性"""
        base_score = self.universalizability_weights.get(action.action_type, 0.5)
        
        # 考虑行为强度
        intensity_factor = 1.0 - (action.intensity - 0.5) * 0.2
        
        # 考虑情境因素
        context_factor = self._analyze_context_for_universalizability(action, context)
        
        return base_score * intensity_factor * context_factor
    
    def _evaluate_humanity_respect(self, action: Action, context: Dict[str, Any]) -> float:
        """评估行为对人性尊严的尊重程度"""
        base_score = self.humanity_dignity_weights.get(action.action_type, 0.5)
        
        # 检查是否有明确的受益者
        if action.target_id and action.target_id != action.actor_id:
            # 他向行为，需要更严格检验
            if action.action_type in [ActionType.DECEIVE, ActionType.HARM]:
                return 0.0  # 欺骗和伤害他人严重违背人性尊严
            elif action.action_type in [ActionType.HELP, ActionType.SHARE]:
                return min(1.0, base_score * 1.2)  # 帮助他人体现对人性的尊重
        
        # 考虑动机纯粹性
        motive_purity = self._evaluate_motive_purity(action, context)
        
        return base_score * motive_purity
    
    def _evaluate_rational_autonomy(self, action: Action, context: Dict[str, Any]) -> float:
        """评估行为的理性自律程度"""
        # 检查行为是否基于理性思考而非冲动
        rationality_score = 0.7  # 默认假设有一定理性
        
        # 检查是否尊重他人的理性自律
        if action.target_id:
            # 强制性行为降低自律评分
            if action.action_type in [ActionType.HARM, ActionType.DECEIVE]:
                rationality_score *= 0.2
            # 启发性行为提高自律评分
            elif action.action_type in [ActionType.HELP, ActionType.COMMUNICATE]:
                rationality_score *= 1.2
        
        # 考虑行为的一致性
        consistency_factor = self._evaluate_moral_consistency(action, context)
        
        return min(1.0, rationality_score * consistency_factor)
    
    def _analyze_context_for_universalizability(self, action: Action, context: Dict[str, Any]) -> float:
        """分析情境对普遍化的影响"""
        # 紧急情况下的例外
        if context.get('emergency', False):
            if action.action_type == ActionType.HARM:
                return 0.1  # 即使紧急情况，伤害他人仍然难以普遍化
            elif action.action_type == ActionType.SACRIFICE:
                return 1.2  # 紧急情况下的牺牲更具普遍化价值
        
        # 资源稀缺性影响
        resource_scarcity = context.get('resource_scarcity', 0.0)
        if resource_scarcity > 0.7:
            if action.action_type == ActionType.SHARE:
                return 1.3  # 稀缺时分享更有道德价值
            elif action.action_type == ActionType.COMPETE:
                return 0.8  # 稀缺时竞争可能更可理解
        
        return 1.0
    
    def _evaluate_motive_purity(self, action: Action, context: Dict[str, Any]) -> float:
        """评估动机的纯粹性 (义务导向 vs 结果导向)"""
        # 康德强调义务导向的动机
        duty_motivation = context.get('duty_motivation', 0.5)
        
        # 检查是否存在自利动机
        self_interest = context.get('self_interest', 0.0)
        
        # 纯粹的义务动机得分更高
        purity_score = duty_motivation * (1.0 - self_interest * 0.5)
        
        return max(0.1, min(1.0, purity_score))
    
    def _evaluate_moral_consistency(self, action: Action, context: Dict[str, Any]) -> float:
        """评估道德一致性"""
        # 检查过往行为的一致性
        past_actions = context.get('past_actions', [])
        if not past_actions:
            return 1.0
        
        # 计算与过往行为的一致性
        consistency_score = 0.5
        similar_actions = [a for a in past_actions if a.action_type == action.action_type]
        
        if similar_actions:
            # 如果过往有类似行为，检查道德评价的一致性
            consistency_score = 0.8
        
        return consistency_score
    
    def explain_evaluation(self, action: Action, context: Dict[str, Any]) -> Dict[str, Any]:
        """解释康德伦理学评估的详细过程"""
        universalizability = self._evaluate_universalizability(action, context)
        humanity_respect = self._evaluate_humanity_respect(action, context)
        rational_autonomy = self._evaluate_rational_autonomy(action, context)
        
        final_score = self.evaluate_action(action, context)
        
        return {
            'framework': 'Kantian Ethics',
            'final_score': final_score,
            'components': {
                'universalizability': {
                    'score': universalizability,
                    'explanation': '检验行为准则是否可以普遍化'
                },
                'humanity_respect': {
                    'score': humanity_respect,
                    'explanation': '检验是否将人当作目的而非手段'
                },
                'rational_autonomy': {
                    'score': rational_autonomy,
                    'explanation': '检验行为是否基于理性自律'
                }
            },
            'moral_judgment': self._get_moral_judgment(final_score)
        }
    
    def _get_moral_judgment(self, score: float) -> str:
        """根据评分给出道德判断"""
        if score >= 0.8:
            return "道德义务 (Moral Duty) - 应当执行此行为"
        elif score >= 0.6:
            return "道德允许 (Morally Permissible) - 可以执行此行为"
        elif score >= 0.4:
            return "道德中性 (Morally Neutral) - 需要进一步考虑"
        elif score >= 0.2:
            return "道德有疑 (Morally Questionable) - 不建议执行"
        else:
            return "道德禁止 (Morally Forbidden) - 绝对不应执行此行为"