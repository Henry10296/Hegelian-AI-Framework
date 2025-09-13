"""
美德伦理学实现

基于亚里士多德的美德伦理学理论：
- 强调品格和德性的重要性
- 追求中庸之道
- 重视实践智慧(phronesis)
- 关注人格的完整性和美德的培养
"""

from typing import Dict, List, Any, Optional
from ..core.action import Action, ActionType
from ..core.moral_state import MoralState


class VirtueEthics:
    """美德伦理学计算引擎"""
    
    def __init__(self):
        # 核心美德及其权重
        self.cardinal_virtues = {
            'courage': 0.9,        # 勇气
            'temperance': 0.8,     # 节制
            'justice': 0.9,        # 正义
            'wisdom': 0.8,         # 智慧
            'compassion': 0.8,     # 慈悲
            'honesty': 0.9,        # 诚实
            'humility': 0.7,       # 谦逊
            'patience': 0.6,       # 耐心
            'generosity': 0.8,     # 慷慨
            'loyalty': 0.7         # 忠诚
        }
        
        # 行为与美德的关联
        self.action_virtue_mapping = {
            ActionType.HELP: {
                'compassion': 0.9,
                'generosity': 0.7,
                'wisdom': 0.5
            },
            ActionType.SHARE: {
                'generosity': 0.9,
                'justice': 0.6,
                'compassion': 0.5
            },
            ActionType.COOPERATE: {
                'justice': 0.8,
                'wisdom': 0.6,
                'patience': 0.5
            },
            ActionType.SACRIFICE: {
                'courage': 0.9,
                'compassion': 0.8,
                'wisdom': 0.7
            },
            ActionType.COMMUNICATE: {
                'honesty': 0.7,
                'wisdom': 0.6,
                'patience': 0.5
            },
            ActionType.HARM: {
                'justice': -0.8,
                'compassion': -0.9,
                'wisdom': -0.6
            },
            ActionType.DECEIVE: {
                'honesty': -0.9,
                'justice': -0.7,
                'wisdom': -0.5
            },
            ActionType.COMPETE: {
                'courage': 0.3,
                'justice': 0.2,
                'temperance': -0.2
            },
            ActionType.IGNORE: {
                'compassion': -0.5,
                'courage': -0.3,
                'justice': -0.4
            },
            ActionType.TRADE: {
                'justice': 0.6,
                'honesty': 0.5,
                'wisdom': 0.4
            }
        }
    
    def evaluate_action(self, action: Action, context: Dict[str, Any]) -> float:
        """
        根据美德伦理学评估行为
        
        返回值: [0, 1] 之间的道德评分
        """
        # 获取行为相关的美德
        virtue_impacts = self.action_virtue_mapping.get(action.action_type, {})
        
        if not virtue_impacts:
            return 0.5  # 中性评分
        
        virtue_scores = []
        
        for virtue_name, impact_value in virtue_impacts.items():
            # 基础美德分数
            base_virtue_weight = self.cardinal_virtues.get(virtue_name, 0.5)
            
            # 情境调整
            context_adjustment = self._calculate_context_adjustment(
                virtue_name, action, context
            )
            
            # 中庸之道调整
            moderation_factor = self._apply_doctrine_of_mean(
                virtue_name, action, context
            )
            
            # 计算该美德的得分
            virtue_score = (
                base_virtue_weight * 
                (1.0 + impact_value) *  # impact_value可能为负
                context_adjustment *
                moderation_factor
            )
            
            virtue_scores.append(max(0.0, virtue_score))
        
        # 综合美德评分
        if virtue_scores:
            final_score = sum(virtue_scores) / len(virtue_scores)
        else:
            final_score = 0.5
        
        # 考虑实践智慧(phronesis)
        practical_wisdom_bonus = self._evaluate_practical_wisdom(action, context)
        final_score += practical_wisdom_bonus
        
        return max(0.0, min(1.0, final_score))
    
    def _calculate_context_adjustment(self, virtue_name: str, action: Action, 
                                    context: Dict[str, Any]) -> float:
        """根据情境调整美德评价"""
        adjustment = 1.0
        
        # 紧急情况下勇气更重要
        if virtue_name == 'courage' and context.get('urgency', 0.0) > 0.7:
            adjustment *= 1.3
        
        # 社会可见性影响诚实的重要性
        if virtue_name == 'honesty' and context.get('social_visibility', 0.0) > 0.6:
            adjustment *= 1.2
        
        # 资源稀缺时慷慨更有价值
        if virtue_name == 'generosity' and context.get('resource_scarcity', 0.0) > 0.7:
            adjustment *= 1.4
        
        # 冲突情况下正义更重要
        if virtue_name == 'justice' and context.get('conflict_present', False):
            adjustment *= 1.2
        
        # 压力情况下耐心更有价值
        if virtue_name == 'patience' and context.get('stress_level', 0.0) > 0.6:
            adjustment *= 1.3
        
        # 权力不平衡时谦逊更重要
        if virtue_name == 'humility' and context.get('power_imbalance', False):
            adjustment *= 1.2
        
        return max(0.5, min(2.0, adjustment))
    
    def _apply_doctrine_of_mean(self, virtue_name: str, action: Action, 
                              context: Dict[str, Any]) -> float:
        """应用中庸之道原则"""
        # 检查行为强度是否适中
        intensity = action.intensity
        
        # 不同美德的理想强度范围
        ideal_ranges = {
            'courage': (0.6, 0.9),      # 勇气需要较高强度
            'temperance': (0.3, 0.7),   # 节制需要适中强度
            'justice': (0.7, 1.0),      # 正义需要坚定强度
            'wisdom': (0.4, 0.8),       # 智慧需要适中强度
            'compassion': (0.5, 0.9),   # 慈悲可以较高强度
            'honesty': (0.6, 1.0),      # 诚实需要坚定强度
            'humility': (0.2, 0.6),     # 谦逊需要较低强度
            'patience': (0.3, 0.7),     # 耐心需要适中强度
            'generosity': (0.4, 0.8),   # 慷慨需要适中到较高强度
            'loyalty': (0.5, 0.9)       # 忠诚可以较高强度
        }
        
        if virtue_name not in ideal_ranges:
            return 1.0
        
        min_ideal, max_ideal = ideal_ranges[virtue_name]
        
        if min_ideal <= intensity <= max_ideal:
            # 在理想范围内，给予奖励
            return 1.2
        elif intensity < min_ideal:
            # 强度不足
            deficit = min_ideal - intensity
            return max(0.7, 1.0 - deficit)
        else:
            # 强度过度
            excess = intensity - max_ideal
            return max(0.7, 1.0 - excess)
    
    def _evaluate_practical_wisdom(self, action: Action, context: Dict[str, Any]) -> float:
        """评估实践智慧(phronesis)"""
        wisdom_bonus = 0.0
        
        # 检查行为是否体现了智慧的选择
        
        # 1. 情境适应性 - 行为是否适合情境
        situational_fit = self._assess_situational_appropriateness(action, context)
        wisdom_bonus += situational_fit * 0.1
        
        # 2. 时机把握 - 行为时机是否恰当
        timing_appropriateness = context.get('timing_appropriateness', 0.5)
        wisdom_bonus += (timing_appropriateness - 0.5) * 0.05
        
        # 3. 平衡考量 - 是否平衡了不同的道德要求
        balance_consideration = self._assess_moral_balance(action, context)
        wisdom_bonus += balance_consideration * 0.08
        
        # 4. 长远视野 - 是否考虑了长期后果
        long_term_consideration = context.get('long_term_thinking', 0.5)
        wisdom_bonus += (long_term_consideration - 0.5) * 0.07
        
        return max(-0.1, min(0.2, wisdom_bonus))
    
    def _assess_situational_appropriateness(self, action: Action, context: Dict[str, Any]) -> float:
        """评估行为的情境适应性"""
        appropriateness = 0.5
        
        # 紧急情况下的快速行动
        if context.get('urgency', 0.0) > 0.8:
            if action.action_type in [ActionType.HELP, ActionType.SACRIFICE]:
                appropriateness += 0.3
            elif action.action_type in [ActionType.IGNORE, ActionType.COMMUNICATE]:
                appropriateness -= 0.2
        
        # 社交场合的适当行为
        if context.get('social_setting', False):
            if action.action_type in [ActionType.COMMUNICATE, ActionType.COOPERATE]:
                appropriateness += 0.2
            elif action.action_type in [ActionType.HARM, ActionType.COMPETE]:
                appropriateness -= 0.3
        
        # 权威在场时的适当行为
        if context.get('authority_present', False):
            if action.action_type in [ActionType.COOPERATE, ActionType.COMMUNICATE]:
                appropriateness += 0.1
            elif action.action_type in [ActionType.COMPETE, ActionType.DECEIVE]:
                appropriateness -= 0.2
        
        return max(0.0, min(1.0, appropriateness))
    
    def _assess_moral_balance(self, action: Action, context: Dict[str, Any]) -> float:
        """评估道德平衡性"""
        balance_score = 0.5
        
        # 检查是否在多个道德要求之间取得平衡
        moral_tensions = context.get('moral_tensions', [])
        
        for tension in moral_tensions:
            if tension == 'justice_vs_mercy':
                if action.action_type in [ActionType.HELP, ActionType.COOPERATE]:
                    balance_score += 0.1  # 体现了平衡
            elif tension == 'individual_vs_collective':
                if action.action_type in [ActionType.SHARE, ActionType.COOPERATE]:
                    balance_score += 0.1
            elif tension == 'honesty_vs_kindness':
                if action.action_type == ActionType.COMMUNICATE:
                    balance_score += 0.1
        
        return max(0.0, min(1.0, balance_score))
    
    def analyze_character_development(self, action_history: List[Action], 
                                    contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析品格发展轨迹"""
        if not action_history:
            return {}
        
        virtue_trends = {}
        
        for virtue_name in self.cardinal_virtues:
            virtue_scores = []
            
            for i, action in enumerate(action_history):
                context = contexts[i] if i < len(contexts) else {}
                
                # 计算该行为对此美德的影响
                virtue_impacts = self.action_virtue_mapping.get(action.action_type, {})
                virtue_impact = virtue_impacts.get(virtue_name, 0.0)
                
                if virtue_impact != 0.0:
                    context_adj = self._calculate_context_adjustment(virtue_name, action, context)
                    mean_factor = self._apply_doctrine_of_mean(virtue_name, action, context)
                    
                    virtue_score = virtue_impact * context_adj * mean_factor
                    virtue_scores.append(virtue_score)
            
            if virtue_scores:
                virtue_trends[virtue_name] = {
                    'average_score': sum(virtue_scores) / len(virtue_scores),
                    'trend': self._calculate_trend(virtue_scores),
                    'consistency': self._calculate_consistency(virtue_scores),
                    'recent_performance': sum(virtue_scores[-5:]) / min(5, len(virtue_scores))
                }
        
        return {
            'virtue_profile': virtue_trends,
            'overall_character_strength': self._calculate_overall_character(virtue_trends),
            'development_recommendations': self._generate_development_recommendations(virtue_trends)
        }
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """计算趋势"""
        if len(scores) < 3:
            return 'insufficient_data'
        
        recent_avg = sum(scores[-3:]) / 3
        earlier_avg = sum(scores[:-3]) / len(scores[:-3])
        
        if recent_avg > earlier_avg + 0.1:
            return 'improving'
        elif recent_avg < earlier_avg - 0.1:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_consistency(self, scores: List[float]) -> float:
        """计算一致性"""
        if len(scores) < 2:
            return 0.0
        
        import statistics
        try:
            std_dev = statistics.stdev(scores)
            # 标准差越小，一致性越高
            consistency = max(0.0, 1.0 - std_dev)
            return consistency
        except:
            return 0.5
    
    def _calculate_overall_character(self, virtue_trends: Dict[str, Dict]) -> float:
        """计算整体品格强度"""
        if not virtue_trends:
            return 0.5
        
        total_score = 0.0
        total_weight = 0.0
        
        for virtue_name, trend_data in virtue_trends.items():
            virtue_weight = self.cardinal_virtues.get(virtue_name, 0.5)
            virtue_score = max(0.0, trend_data['average_score'])
            
            total_score += virtue_score * virtue_weight
            total_weight += virtue_weight
        
        if total_weight > 0:
            return total_score / total_weight
        else:
            return 0.5
    
    def _generate_development_recommendations(self, virtue_trends: Dict[str, Dict]) -> List[str]:
        """生成品格发展建议"""
        recommendations = []
        
        for virtue_name, trend_data in virtue_trends.items():
            if trend_data['average_score'] < 0.3:
                recommendations.append(f"需要加强{virtue_name}的培养")
            elif trend_data['trend'] == 'declining':
                recommendations.append(f"{virtue_name}呈下降趋势，需要关注")
            elif trend_data['consistency'] < 0.6:
                recommendations.append(f"{virtue_name}表现不够稳定，需要更一致的实践")
        
        if not recommendations:
            recommendations.append("品格发展良好，继续保持")
        
        return recommendations
    
    def explain_evaluation(self, action: Action, context: Dict[str, Any]) -> Dict[str, Any]:
        """解释美德伦理学评估过程"""
        virtue_impacts = self.action_virtue_mapping.get(action.action_type, {})
        final_score = self.evaluate_action(action, context)
        
        detailed_analysis = {}
        
        for virtue_name, impact_value in virtue_impacts.items():
            context_adj = self._calculate_context_adjustment(virtue_name, action, context)
            mean_factor = self._apply_doctrine_of_mean(virtue_name, action, context)
            
            detailed_analysis[virtue_name] = {
                'base_impact': impact_value,
                'context_adjustment': context_adj,
                'moderation_factor': mean_factor,
                'final_contribution': impact_value * context_adj * mean_factor
            }
        
        return {
            'framework': 'Virtue Ethics',
            'final_score': final_score,
            'virtue_analysis': detailed_analysis,
            'practical_wisdom_evaluation': self._evaluate_practical_wisdom(action, context),
            'moral_judgment': self._get_moral_judgment(final_score),
            'character_implications': self._assess_character_implications(action, context)
        }
    
    def _get_moral_judgment(self, score: float) -> str:
        """根据评分给出道德判断"""
        if score >= 0.8:
            return "德性卓越 (Virtuous Excellence) - 体现了高尚的品格"
        elif score >= 0.6:
            return "德性良好 (Good Character) - 表现出良好的品格"
        elif score >= 0.4:
            return "品格中等 (Moderate Character) - 品格表现一般"
        elif score >= 0.2:
            return "品格有待提升 (Character Needs Development) - 需要培养更好的品格"
        else:
            return "品格缺陷 (Character Deficiency) - 表现出品格上的重大缺陷"
    
    def _assess_character_implications(self, action: Action, context: Dict[str, Any]) -> Dict[str, Any]:
        """评估对品格的影响"""
        implications = {
            'character_building': [],
            'character_risks': [],
            'long_term_effects': []
        }
        
        virtue_impacts = self.action_virtue_mapping.get(action.action_type, {})
        
        for virtue_name, impact_value in virtue_impacts.items():
            if impact_value > 0.5:
                implications['character_building'].append(f"有助于培养{virtue_name}")
            elif impact_value < -0.5:
                implications['character_risks'].append(f"可能损害{virtue_name}")
        
        # 长期影响分析
        if action.action_type in [ActionType.HELP, ActionType.SACRIFICE, ActionType.SHARE]:
            implications['long_term_effects'].append("有助于形成利他的品格特质")
        elif action.action_type in [ActionType.DECEIVE, ActionType.HARM]:
            implications['long_term_effects'].append("可能形成有害的品格习惯")
        
        return implications