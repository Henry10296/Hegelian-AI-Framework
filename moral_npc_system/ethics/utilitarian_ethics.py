"""
功利主义伦理学的可计算实现

基于约翰·斯图尔特·密尔和边沁的功利主义原则：
- 行为的道德性由其后果决定
- 追求最大多数人的最大幸福
- 考虑快乐的质量和数量
- 平等地考虑所有受影响者的福利
"""

import math
from typing import Dict, List, Any, Optional, Tuple
from ..core.action import Action, ActionType
from ..core.moral_state import MoralState


class UtilitarianEthics:
    """功利主义伦理学计算引擎"""
    
    def __init__(self):
        # 不同行为类型的基础效用值
        self.base_utility_values = {
            ActionType.HELP: 0.8,        # 帮助产生正效用
            ActionType.SHARE: 0.7,       # 分享增加总体福利
            ActionType.COOPERATE: 0.6,   # 合作产生双赢
            ActionType.TRADE: 0.5,       # 公平交易增加效用
            ActionType.COMMUNICATE: 0.3, # 交流产生轻微正效用
            ActionType.SACRIFICE: 0.4,   # 牺牲效用复杂，取决于受益者
            ActionType.IGNORE: -0.1,     # 忽视产生轻微负效用
            ActionType.COMPETE: -0.2,    # 竞争可能减少总体效用
            ActionType.DECEIVE: -0.6,    # 欺骗产生负效用
            ActionType.HARM: -0.9,       # 伤害产生严重负效用
        }
        
        # 快乐/痛苦的质量权重 (密尔的质的功利主义)
        self.pleasure_quality_weights = {
            'intellectual': 1.5,    # 智力快乐
            'aesthetic': 1.3,       # 审美快乐
            'moral': 1.4,          # 道德快乐
            'social': 1.2,         # 社交快乐
            'physical': 1.0,       # 身体快乐
            'material': 0.8,       # 物质快乐
        }
    
    def evaluate_action(self, action: Action, context: Dict[str, Any]) -> float:
        """
        根据功利主义评估行为的道德性
        
        返回值: [0, 1] 之间的道德评分，基于总体效用最大化
        """
        # 识别所有受影响的实体
        affected_entities = self._identify_affected_entities(action, context)
        
        # 计算总效用
        total_utility = 0.0
        total_weight = 0.0
        
        for entity_id, impact_data in affected_entities.items():
            entity_utility = self._calculate_entity_utility(action, entity_id, impact_data, context)
            entity_weight = impact_data.get('moral_weight', 1.0)
            
            total_utility += entity_utility * entity_weight
            total_weight += entity_weight
        
        # 标准化效用值
        if total_weight > 0:
            average_utility = total_utility / total_weight
        else:
            average_utility = 0.0
        
        # 转换为 [0, 1] 区间
        normalized_score = (average_utility + 1.0) / 2.0
        return max(0.0, min(1.0, normalized_score))
    
    def _identify_affected_entities(self, action: Action, context: Dict[str, Any]) -> Dict[str, Dict]:
        """识别受行为影响的所有实体"""
        affected = {}
        
        # 行为者自身
        affected[action.actor_id] = {
            'impact_type': 'actor',
            'moral_weight': 1.0,
            'distance': 0.0
        }
        
        # 直接目标
        if action.target_id and action.target_id != action.actor_id:
            affected[action.target_id] = {
                'impact_type': 'direct_target',
                'moral_weight': 1.0,
                'distance': 1.0
            }
        
        # 间接受影响者
        indirect_affected = context.get('indirect_affected', {})
        for entity_id, impact_data in indirect_affected.items():
            if entity_id not in affected:
                affected[entity_id] = {
                    'impact_type': 'indirect',
                    'moral_weight': impact_data.get('weight', 0.5),
                    'distance': impact_data.get('distance', 2.0)
                }
        
        # 社会整体影响
        if context.get('social_impact', False):
            affected['society'] = {
                'impact_type': 'social',
                'moral_weight': len(affected) * 0.1,  # 社会影响权重基于影响范围
                'distance': 3.0
            }
        
        return affected
    
    def _calculate_entity_utility(self, action: Action, entity_id: str, impact_data: Dict, context: Dict[str, Any]) -> float:
        """计算特定实体的效用变化"""
        base_utility = self.base_utility_values.get(action.action_type, 0.0)
        
        # 根据实体角色调整效用
        impact_type = impact_data['impact_type']
        
        if impact_type == 'actor':
            # 行为者的效用
            utility = self._calculate_actor_utility(action, context)
        elif impact_type == 'direct_target':
            # 直接目标的效用
            utility = self._calculate_target_utility(action, context)
        elif impact_type == 'indirect':
            # 间接受影响者的效用
            distance_factor = 1.0 / (1.0 + impact_data['distance'])
            utility = base_utility * distance_factor * 0.5
        elif impact_type == 'social':
            # 社会整体效用
            utility = self._calculate_social_utility(action, context)
        else:
            utility = base_utility
        
        # 考虑行为强度
        utility *= action.intensity
        
        # 考虑时间因素 (长期vs短期效用)
        time_factor = self._calculate_temporal_utility_factor(action, context)
        utility *= time_factor
        
        return utility
    
    def _calculate_actor_utility(self, action: Action, context: Dict[str, Any]) -> float:
        """计算行为者的效用"""
        base_utility = self.base_utility_values.get(action.action_type, 0.0)
        
        # 利他行为可能给行为者带来道德快乐
        if action.action_type in [ActionType.HELP, ActionType.SHARE, ActionType.SACRIFICE]:
            moral_pleasure = 0.3 * self.pleasure_quality_weights['moral']
            base_utility += moral_pleasure
        
        # 自私行为可能带来愧疚
        elif action.action_type in [ActionType.HARM, ActionType.DECEIVE]:
            guilt_penalty = -0.4
            base_utility += guilt_penalty
        
        # 考虑行为者的个人成本
        personal_cost = context.get('personal_cost', 0.0)
        base_utility -= personal_cost
        
        return base_utility
    
    def _calculate_target_utility(self, action: Action, context: Dict[str, Any]) -> float:
        """计算直接目标的效用"""
        base_utility = self.base_utility_values.get(action.action_type, 0.0)
        
        # 对目标的影响通常与对行为者的影响相反
        if action.action_type == ActionType.HELP:
            # 被帮助者获得正效用
            benefit_magnitude = context.get('benefit_magnitude', 1.0)
            return base_utility * benefit_magnitude
        
        elif action.action_type == ActionType.HARM:
            # 被伤害者遭受负效用
            harm_magnitude = context.get('harm_magnitude', 1.0)
            return base_utility * harm_magnitude
        
        elif action.action_type == ActionType.DECEIVE:
            # 被欺骗者的信任受损
            trust_damage = context.get('trust_damage', 0.5)
            return base_utility * (1.0 + trust_damage)
        
        elif action.action_type == ActionType.SHARE:
            # 分享的受益者
            shared_value = context.get('shared_value', 0.5)
            return base_utility * shared_value
        
        return base_utility
    
    def _calculate_social_utility(self, action: Action, context: Dict[str, Any]) -> float:
        """计算社会整体效用"""
        base_utility = self.base_utility_values.get(action.action_type, 0.0)
        
        # 某些行为对社会有系统性影响
        if action.action_type == ActionType.COOPERATE:
            # 合作行为促进社会和谐
            return base_utility * 1.5
        
        elif action.action_type == ActionType.DECEIVE:
            # 欺骗行为损害社会信任
            return base_utility * 2.0  # 负值会被放大
        
        elif action.action_type == ActionType.HELP:
            # 助人行为树立正面榜样
            return base_utility * 1.2
        
        # 考虑行为的可见性
        visibility = context.get('action_visibility', 0.5)
        return base_utility * (1.0 + visibility * 0.5)
    
    def _calculate_temporal_utility_factor(self, action: Action, context: Dict[str, Any]) -> float:
        """计算时间效用因子 (短期vs长期效果)"""
        short_term_ratio = context.get('short_term_utility_ratio', 0.6)
        long_term_ratio = context.get('long_term_utility_ratio', 0.4)
        
        # 功利主义通常重视长期效果
        temporal_factor = short_term_ratio * 0.8 + long_term_ratio * 1.2
        
        return temporal_factor
    
    def calculate_marginal_utility(self, action: Action, context: Dict[str, Any]) -> Dict[str, float]:
        """计算边际效用 (每个实体的效用变化)"""
        affected_entities = self._identify_affected_entities(action, context)
        marginal_utilities = {}
        
        for entity_id, impact_data in affected_entities.items():
            entity_utility = self._calculate_entity_utility(action, entity_id, impact_data, context)
            marginal_utilities[entity_id] = entity_utility
        
        return marginal_utilities
    
    def compare_actions(self, actions: List[Action], context: Dict[str, Any]) -> List[Tuple[Action, float]]:
        """比较多个行为的功利主义价值"""
        action_utilities = []
        
        for action in actions:
            utility_score = self.evaluate_action(action, context)
            action_utilities.append((action, utility_score))
        
        # 按效用值降序排序
        action_utilities.sort(key=lambda x: x[1], reverse=True)
        
        return action_utilities
    
    def explain_evaluation(self, action: Action, context: Dict[str, Any]) -> Dict[str, Any]:
        """解释功利主义评估的详细过程"""
        affected_entities = self._identify_affected_entities(action, context)
        marginal_utilities = self.calculate_marginal_utility(action, context)
        final_score = self.evaluate_action(action, context)
        
        total_positive_utility = sum(u for u in marginal_utilities.values() if u > 0)
        total_negative_utility = sum(u for u in marginal_utilities.values() if u < 0)
        
        return {
            'framework': 'Utilitarian Ethics',
            'final_score': final_score,
            'total_utility': sum(marginal_utilities.values()),
            'affected_entities': len(affected_entities),
            'utility_breakdown': {
                'positive_utility': total_positive_utility,
                'negative_utility': total_negative_utility,
                'net_utility': total_positive_utility + total_negative_utility
            },
            'entity_utilities': marginal_utilities,
            'moral_judgment': self._get_moral_judgment(final_score)
        }
    
    def _get_moral_judgment(self, score: float) -> str:
        """根据效用评分给出道德判断"""
        if score >= 0.8:
            return "强烈推荐 (Highly Recommended) - 显著增加总体福利"
        elif score >= 0.6:
            return "推荐 (Recommended) - 增加总体福利"
        elif score >= 0.4:
            return "中性 (Neutral) - 效用平衡"
        elif score >= 0.2:
            return "不推荐 (Not Recommended) - 减少总体福利"
        else:
            return "强烈反对 (Strongly Opposed) - 显著减少总体福利"