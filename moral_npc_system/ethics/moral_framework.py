"""
统一的道德框架，整合康德伦理学和功利主义
"""

from typing import Dict, List, Any, Optional
from ..core.action import Action
from ..core.moral_state import MoralState
from .kantian_ethics import KantianEthics
from .utilitarian_ethics import UtilitarianEthics


class MoralFramework:
    """统一道德评估框架"""
    
    def __init__(self):
        self.kantian_ethics = KantianEthics()
        self.utilitarian_ethics = UtilitarianEthics()
    
    def evaluate_action(self, action: Action, moral_state: MoralState, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用统一框架评估行为
        
        基于NPC的道德状态权重整合不同伦理体系的评价
        """
        # 康德伦理学评估
        kantian_score = self.kantian_ethics.evaluate_action(action, context)
        
        # 功利主义评估
        utilitarian_score = self.utilitarian_ethics.evaluate_action(action, context)
        
        # 基于道德状态的加权组合
        weighted_score = (
            kantian_score * moral_state.kantian_weight +
            utilitarian_score * moral_state.utilitarian_weight +
            0.5 * moral_state.virtue_weight  # 美德伦理暂时使用平均值
        )
        
        # 考虑道德情感影响
        emotional_adjustment = self._apply_moral_emotions(
            action, weighted_score, moral_state, context
        )
        
        final_score = max(0.0, min(1.0, weighted_score + emotional_adjustment))
        
        return {
            'final_score': final_score,
            'component_scores': {
                'kantian': kantian_score,
                'utilitarian': utilitarian_score,
                'virtue': 0.5  # 占位符
            },
            'moral_weights': {
                'kantian_weight': moral_state.kantian_weight,
                'utilitarian_weight': moral_state.utilitarian_weight,
                'virtue_weight': moral_state.virtue_weight
            },
            'emotional_adjustment': emotional_adjustment,
            'moral_confidence': self._calculate_confidence(kantian_score, utilitarian_score),
            'recommendation': self._get_recommendation(final_score)
        }
    
    def _apply_moral_emotions(self, action: Action, base_score: float, 
                            moral_state: MoralState, context: Dict[str, Any]) -> float:
        """应用道德情感对评分的调整"""
        adjustment = 0.0
        
        # 共情影响
        if action.affects_others and moral_state.empathy_level > 0.5:
            if action.get_moral_weight() > 0:  # 正面行为
                adjustment += (moral_state.empathy_level - 0.5) * 0.2
            else:  # 负面行为
                adjustment -= (moral_state.empathy_level - 0.5) * 0.3
        
        # 愧疚敏感度影响
        if action.get_moral_weight() < 0 and moral_state.guilt_sensitivity > 0.5:
            guilt_penalty = (moral_state.guilt_sensitivity - 0.5) * 0.4
            adjustment -= guilt_penalty
        
        # 道德勇气影响
        if context.get('requires_moral_courage', False):
            if moral_state.moral_courage > 0.5:
                adjustment += (moral_state.moral_courage - 0.5) * 0.3
            else:
                adjustment -= (0.5 - moral_state.moral_courage) * 0.2
        
        # 社会压力影响
        social_pressure = context.get('social_pressure', 0.0)
        if social_pressure > 0:
            pressure_effect = social_pressure * (1.0 - moral_state.social_pressure_resistance)
            # 社会压力可能推向不道德行为
            if base_score < 0.5:
                adjustment -= pressure_effect * 0.2
        
        return adjustment
    
    def _calculate_confidence(self, kantian_score: float, utilitarian_score: float) -> float:
        """计算道德判断的置信度"""
        # 两个体系评分越接近，置信度越高
        score_difference = abs(kantian_score - utilitarian_score)
        
        # 分数极端值 (接近0或1) 表示更强的道德确定性
        extreme_factor = min(
            abs(kantian_score - 0.5) * 2,
            abs(utilitarian_score - 0.5) * 2
        )
        
        # 置信度计算
        consistency_confidence = 1.0 - score_difference
        certainty_confidence = extreme_factor
        
        overall_confidence = (consistency_confidence + certainty_confidence) / 2.0
        return max(0.0, min(1.0, overall_confidence))
    
    def _get_recommendation(self, score: float) -> str:
        """根据综合评分给出行为建议"""
        if score >= 0.8:
            return "强烈推荐执行此行为"
        elif score >= 0.6:
            return "推荐执行此行为"
        elif score >= 0.4:
            return "可以考虑执行此行为"
        elif score >= 0.2:
            return "不建议执行此行为"
        else:
            return "强烈不建议执行此行为"
    
    def compare_actions(self, actions: List[Action], moral_state: MoralState, 
                       context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """比较多个行为并排序"""
        evaluations = []
        
        for action in actions:
            evaluation = self.evaluate_action(action, moral_state, context)
            evaluation['action'] = action
            evaluations.append(evaluation)
        
        # 按最终评分降序排序
        evaluations.sort(key=lambda x: x['final_score'], reverse=True)
        
        return evaluations
    
    def explain_moral_reasoning(self, action: Action, moral_state: MoralState, 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """详细解释道德推理过程"""
        # 获取各框架的详细解释
        kantian_explanation = self.kantian_ethics.explain_evaluation(action, context)
        utilitarian_explanation = self.utilitarian_ethics.explain_evaluation(action, context)
        
        # 整合评估
        integrated_evaluation = self.evaluate_action(action, moral_state, context)
        
        return {
            'action_summary': {
                'type': action.action_type.value,
                'actor': action.actor_id,
                'target': action.target_id,
                'intensity': action.intensity
            },
            'moral_state_profile': {
                'dominant_framework': moral_state.get_dominant_moral_framework(),
                'empathy_level': moral_state.empathy_level,
                'moral_courage': moral_state.moral_courage,
                'guilt_sensitivity': moral_state.guilt_sensitivity
            },
            'framework_evaluations': {
                'kantian': kantian_explanation,
                'utilitarian': utilitarian_explanation
            },
            'integrated_evaluation': integrated_evaluation,
            'reasoning_process': self._generate_reasoning_narrative(
                action, moral_state, kantian_explanation, utilitarian_explanation, integrated_evaluation
            )
        }
    
    def _generate_reasoning_narrative(self, action: Action, moral_state: MoralState,
                                    kantian_exp: Dict, utilitarian_exp: Dict, 
                                    integrated_eval: Dict) -> str:
        """生成道德推理的叙述性解释"""
        narrative_parts = []
        
        # 行为描述
        narrative_parts.append(f"正在评估 {action.action_type.value} 行为")
        
        # 主导道德框架
        dominant = moral_state.get_dominant_moral_framework()
        if dominant == 'kantian':
            narrative_parts.append(f"该NPC主要遵循康德伦理学 (权重: {moral_state.kantian_weight:.2f})")
            narrative_parts.append(f"康德评估: {kantian_exp['moral_judgment']}")
        elif dominant == 'utilitarian':
            narrative_parts.append(f"该NPC主要遵循功利主义 (权重: {moral_state.utilitarian_weight:.2f})")
            narrative_parts.append(f"功利主义评估: {utilitarian_exp['moral_judgment']}")
        
        # 情感因素
        if moral_state.empathy_level > 0.7:
            narrative_parts.append("高共情能力增强了对他人福利的关注")
        if moral_state.guilt_sensitivity > 0.7:
            narrative_parts.append("高愧疚敏感度使其更谨慎对待可能的负面行为")
        
        # 最终建议
        narrative_parts.append(f"综合评估建议: {integrated_eval['recommendation']}")
        
        return "; ".join(narrative_parts)