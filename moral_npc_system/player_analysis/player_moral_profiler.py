"""
玩家道德档案分析器 - 构建玩家的道德人格画像
"""

import time
import numpy as np
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict, deque
from dataclasses import dataclass

from ..core.action import Action, ActionType
from ..core.moral_state import MoralState
from ..ethics.moral_framework import MoralFramework


@dataclass
class PlayerAction:
    """玩家行为记录"""
    action_type: ActionType
    target_id: Optional[str]
    context: Dict[str, Any]
    outcome: float  # 行为结果评分 [-1, 1]
    timestamp: float
    session_id: str
    
    # 选择相关信息
    available_alternatives: List[ActionType] = None
    decision_time: float = 0.0  # 决策耗时
    certainty_level: float = 1.0  # 选择的确定性


@dataclass
class MoralDilemmaResponse:
    """道德两难反应"""
    dilemma_id: str
    chosen_option: str
    reasoning: str
    confidence: float
    response_time: float
    context_factors: Dict[str, Any]


class PlayerMoralProfiler:
    """玩家道德档案分析器"""
    
    def __init__(self):
        # 行为历史
        self.action_history: List[PlayerAction] = []
        self.dilemma_responses: List[MoralDilemmaResponse] = []
        
        # 道德框架评估器
        self.moral_framework = MoralFramework()
        
        # 统计数据
        self.behavior_patterns = {
            'action_frequency': defaultdict(int),
            'context_preferences': defaultdict(float),
            'temporal_patterns': defaultdict(list),
            'decision_styles': {}
        }
        
        # 道德档案
        self.moral_profile = {
            'primary_framework': 'unknown',
            'moral_weights': {'kantian': 0.33, 'utilitarian': 0.33, 'virtue': 0.34},
            'behavioral_tendencies': {},
            'value_priorities': {},
            'consistency_score': 0.0,
            'moral_development_stage': 'conventional',
            'empathy_indicators': 0.5,
            'risk_tolerance': 0.5,
            'social_orientation': 0.5
        }
        
        # 分析参数
        self.analysis_params = {
            'min_actions_for_analysis': 10,
            'recent_actions_window': 50,
            'consistency_threshold': 0.7,
            'confidence_threshold': 0.6
        }
    
    def record_player_action(self, action: PlayerAction):
        """记录玩家行为"""
        self.action_history.append(action)
        
        # 更新行为模式
        self._update_behavior_patterns(action)
        
        # 如果有足够数据，重新分析档案
        if len(self.action_history) >= self.analysis_params['min_actions_for_analysis']:
            self._analyze_moral_profile()
    
    def record_dilemma_response(self, response: MoralDilemmaResponse):
        """记录道德两难回应"""
        self.dilemma_responses.append(response)
        self._analyze_moral_reasoning_style()
    
    def _update_behavior_patterns(self, action: PlayerAction):
        """更新行为模式统计"""
        # 行为频率
        self.behavior_patterns['action_frequency'][action.action_type] += 1
        
        # 情境偏好
        for context_key, context_value in action.context.items():
            if isinstance(context_value, (int, float)):
                self.behavior_patterns['context_preferences'][context_key] += context_value
        
        # 时间模式
        hour = time.localtime(action.timestamp).tm_hour
        self.behavior_patterns['temporal_patterns'][hour].append(action.action_type)
        
        # 决策风格
        self.behavior_patterns['decision_styles'][action.timestamp] = {
            'decision_time': action.decision_time,
            'certainty': action.certainty_level,
            'complexity': len(action.available_alternatives) if action.available_alternatives else 1
        }
    
    def _analyze_moral_profile(self):
        """分析道德档案"""
        recent_actions = self.action_history[-self.analysis_params['recent_actions_window']:]
        
        # 分析道德框架倾向
        self._analyze_moral_framework_preference(recent_actions)
        
        # 分析行为倾向
        self._analyze_behavioral_tendencies(recent_actions)
        
        # 分析价值优先级
        self._analyze_value_priorities(recent_actions)
        
        # 计算一致性评分
        self._calculate_consistency_score(recent_actions)
        
        # 分析道德发展阶段
        self._analyze_moral_development_stage()
        
        # 分析心理特征
        self._analyze_psychological_traits(recent_actions)
    
    def _analyze_moral_framework_preference(self, actions: List[PlayerAction]):
        """分析道德框架偏好"""
        framework_scores = {'kantian': 0.0, 'utilitarian': 0.0, 'virtue': 0.0}
        total_weight = 0.0
        
        for action in actions:
            if not action.context:
                continue
            
            # 创建模拟的道德状态进行评估
            test_state = MoralState()
            
            # 模拟Action对象
            test_action = Action(
                id=f"player_{action.timestamp}",
                action_type=action.action_type,
                actor_id="player",
                target_id=action.target_id,
                context=action.context
            )
            
            # 评估各框架的匹配度
            evaluation = self.moral_framework.evaluate_action(test_action, test_state, action.context)
            
            # 根据玩家的实际选择和结果调整评分
            if action.outcome > 0:  # 正面结果表明选择合理
                weight = action.certainty_level
                framework_scores['kantian'] += evaluation['component_scores']['kantian'] * weight
                framework_scores['utilitarian'] += evaluation['component_scores']['utilitarian'] * weight
                framework_scores['virtue'] += evaluation['component_scores']['virtue'] * weight
                total_weight += weight
        
        # 标准化评分
        if total_weight > 0:
            for framework in framework_scores:
                framework_scores[framework] /= total_weight
        
        # 更新档案
        self.moral_profile['moral_weights'] = framework_scores
        self.moral_profile['primary_framework'] = max(framework_scores.items(), key=lambda x: x[1])[0]
    
    def _analyze_behavioral_tendencies(self, actions: List[PlayerAction]):
        """分析行为倾向"""
        tendencies = {
            'altruism': 0.0,      # 利他主义倾向
            'cooperation': 0.0,    # 合作倾向
            'competitiveness': 0.0, # 竞争倾向
            'risk_taking': 0.0,    # 冒险倾向
            'rule_following': 0.0,  # 规则遵循
            'innovation': 0.0      # 创新倾向
        }
        
        action_tendency_mapping = {
            ActionType.HELP: {'altruism': 1.0, 'cooperation': 0.5},
            ActionType.SHARE: {'altruism': 0.8, 'cooperation': 0.7},
            ActionType.COOPERATE: {'cooperation': 1.0, 'rule_following': 0.3},
            ActionType.COMPETE: {'competitiveness': 1.0, 'risk_taking': 0.5},
            ActionType.SACRIFICE: {'altruism': 1.0, 'risk_taking': 0.8},
            ActionType.HARM: {'competitiveness': 0.8, 'risk_taking': 0.6},
            ActionType.DECEIVE: {'competitiveness': 0.7, 'risk_taking': 0.9},
            ActionType.TRADE: {'cooperation': 0.4, 'rule_following': 0.6},
            ActionType.COMMUNICATE: {'cooperation': 0.3, 'innovation': 0.2}
        }
        
        total_actions = len(actions)
        if total_actions == 0:
            return
        
        for action in actions:
            mappings = action_tendency_mapping.get(action.action_type, {})
            weight = action.certainty_level / total_actions
            
            for tendency, value in mappings.items():
                tendencies[tendency] += value * weight
        
        self.moral_profile['behavioral_tendencies'] = tendencies
    
    def _analyze_value_priorities(self, actions: List[PlayerAction]):
        """分析价值优先级"""
        values = {
            'justice': 0.0,        # 正义
            'compassion': 0.0,     # 同情
            'autonomy': 0.0,       # 自主
            'loyalty': 0.0,        # 忠诚
            'authority': 0.0,      # 权威
            'sanctity': 0.0,       # 神圣性
            'fairness': 0.0,       # 公平
            'care': 0.0,          # 关怀
            'liberty': 0.0,        # 自由
            'efficiency': 0.0      # 效率
        }
        
        # 基于行为类型推断价值优先级
        for action in actions:
            context = action.context
            outcome_weight = max(0.1, action.outcome)  # 正面结果权重更高
            
            if action.action_type == ActionType.HELP:
                values['care'] += outcome_weight
                values['compassion'] += outcome_weight
            
            elif action.action_type == ActionType.COOPERATE:
                values['fairness'] += outcome_weight
                values['loyalty'] += outcome_weight * 0.5
            
            elif action.action_type == ActionType.SACRIFICE:
                values['care'] += outcome_weight * 1.2
                values['justice'] += outcome_weight * 0.8
            
            elif action.action_type == ActionType.COMPETE:
                values['autonomy'] += outcome_weight
                values['efficiency'] += outcome_weight * 0.7
            
            # 情境因素
            if context.get('authority_present', False):
                if action.outcome > 0:
                    values['authority'] += outcome_weight * 0.5
                else:
                    values['liberty'] += outcome_weight * 0.3
            
            if context.get('group_involved', False):
                values['loyalty'] += outcome_weight * 0.3
                values['fairness'] += outcome_weight * 0.4
        
        # 标准化
        total_value = sum(values.values())
        if total_value > 0:
            for value in values:
                values[value] /= total_value
        
        self.moral_profile['value_priorities'] = values
    
    def _calculate_consistency_score(self, actions: List[PlayerAction]):
        """计算一致性评分"""
        if len(actions) < 5:
            self.moral_profile['consistency_score'] = 0.0
            return
        
        # 分析相似情境下的行为一致性
        context_clusters = defaultdict(list)
        
        for action in actions:
            # 简化的情境聚类
            context_signature = self._get_context_signature(action.context)
            context_clusters[context_signature].append(action)
        
        consistency_scores = []
        
        for cluster in context_clusters.values():
            if len(cluster) < 2:
                continue
            
            # 计算该情境下的行为一致性
            action_types = [action.action_type for action in cluster]
            most_common = max(set(action_types), key=action_types.count)
            consistency = action_types.count(most_common) / len(action_types)
            consistency_scores.append(consistency)
        
        # 总体一致性
        if consistency_scores:
            self.moral_profile['consistency_score'] = np.mean(consistency_scores)
        else:
            self.moral_profile['consistency_score'] = 0.5
    
    def _get_context_signature(self, context: Dict[str, Any]) -> str:
        """获取情境签名用于聚类"""
        # 简化的情境特征提取
        features = []
        
        key_factors = ['urgency', 'social_visibility', 'resource_cost', 'harm_potential']
        for factor in key_factors:
            if factor in context:
                value = context[factor]
                if isinstance(value, (int, float)):
                    # 离散化
                    if value < 0.3:
                        features.append(f"{factor}_low")
                    elif value < 0.7:
                        features.append(f"{factor}_med")
                    else:
                        features.append(f"{factor}_high")
        
        return "_".join(sorted(features))
    
    def _analyze_moral_development_stage(self):
        """分析道德发展阶段 (基于科尔伯格理论)"""
        # 简化的发展阶段判断
        consistency = self.moral_profile['consistency_score']
        kantian_weight = self.moral_profile['moral_weights']['kantian']
        utilitarian_weight = self.moral_profile['moral_weights']['utilitarian']
        
        if consistency < 0.3:
            stage = 'preconventional'  # 前习俗水平
        elif kantian_weight > 0.5 and consistency > 0.7:
            stage = 'postconventional'  # 后习俗水平
        else:
            stage = 'conventional'  # 习俗水平
        
        self.moral_profile['moral_development_stage'] = stage
    
    def _analyze_psychological_traits(self, actions: List[PlayerAction]):
        """分析心理特征"""
        if not actions:
            return
        
        # 共情指标
        empathy_actions = [ActionType.HELP, ActionType.SHARE, ActionType.SACRIFICE]
        empathy_count = sum(1 for action in actions if action.action_type in empathy_actions)
        self.moral_profile['empathy_indicators'] = empathy_count / len(actions)
        
        # 风险容忍度
        risk_actions = [ActionType.COMPETE, ActionType.HARM, ActionType.DECEIVE]
        risk_contexts = sum(action.context.get('risk_level', 0) for action in actions if action.context)
        risk_behavior = sum(1 for action in actions if action.action_type in risk_actions)
        
        risk_score = (risk_contexts / len(actions) + risk_behavior / len(actions)) / 2
        self.moral_profile['risk_tolerance'] = min(1.0, risk_score)
        
        # 社会导向
        social_actions = [ActionType.COOPERATE, ActionType.SHARE, ActionType.COMMUNICATE]
        social_count = sum(1 for action in actions if action.action_type in social_actions)
        self.moral_profile['social_orientation'] = social_count / len(actions)
    
    def _analyze_moral_reasoning_style(self):
        """分析道德推理风格"""
        if not self.dilemma_responses:
            return
        
        # 分析推理复杂度
        reasoning_complexity = []
        response_times = []
        confidence_levels = []
        
        for response in self.dilemma_responses:
            # 推理复杂度 (基于推理文本长度和关键词)
            reasoning_length = len(response.reasoning.split())
            moral_keywords = ['should', 'ought', 'right', 'wrong', 'duty', 'consequence', 'harm', 'benefit']
            keyword_count = sum(1 for word in response.reasoning.lower().split() if word in moral_keywords)
            
            complexity = (reasoning_length / 10 + keyword_count) / 2
            reasoning_complexity.append(min(1.0, complexity))
            
            response_times.append(response.response_time)
            confidence_levels.append(response.confidence)
        
        # 更新决策风格
        self.behavior_patterns['decision_styles'].update({
            'avg_reasoning_complexity': np.mean(reasoning_complexity),
            'avg_response_time': np.mean(response_times),
            'avg_confidence': np.mean(confidence_levels)
        })
    
    def get_moral_profile(self) -> Dict[str, Any]:
        """获取当前道德档案"""
        return self.moral_profile.copy()
    
    def get_behavioral_summary(self) -> Dict[str, Any]:
        """获取行为摘要"""
        recent_actions = self.action_history[-20:] if self.action_history else []
        
        action_distribution = defaultdict(int)
        for action in recent_actions:
            action_distribution[action.action_type.value] += 1
        
        return {
            'total_actions_recorded': len(self.action_history),
            'recent_action_distribution': dict(action_distribution),
            'moral_profile_confidence': self._calculate_profile_confidence(),
            'dominant_behavioral_tendency': self._get_dominant_tendency(),
            'moral_consistency': self.moral_profile['consistency_score']
        }
    
    def _calculate_profile_confidence(self) -> float:
        """计算档案置信度"""
        data_sufficiency = min(1.0, len(self.action_history) / 50)  # 50个行为为充分数据
        consistency = self.moral_profile['consistency_score']
        dilemma_data = min(1.0, len(self.dilemma_responses) / 5)  # 5个两难为充分数据
        
        confidence = (data_sufficiency + consistency + dilemma_data) / 3
        return confidence
    
    def _get_dominant_tendency(self) -> str:
        """获取主导行为倾向"""
        tendencies = self.moral_profile.get('behavioral_tendencies', {})
        if not tendencies:
            return 'unknown'
        
        return max(tendencies.items(), key=lambda x: x[1])[0]
    
    def predict_action_preference(self, situation_context: Dict[str, Any]) -> Dict[ActionType, float]:
        """预测玩家在特定情境下的行为偏好"""
        preferences = {}
        
        # 基于历史行为模式预测
        for action_type in ActionType:
            base_frequency = self.behavior_patterns['action_frequency'][action_type]
            total_actions = max(1, len(self.action_history))
            base_preference = base_frequency / total_actions
            
            # 情境调整
            context_adjustment = self._calculate_context_adjustment(action_type, situation_context)
            
            # 道德框架调整
            moral_adjustment = self._calculate_moral_framework_adjustment(action_type, situation_context)
            
            final_preference = base_preference * (1 + context_adjustment + moral_adjustment)
            preferences[action_type] = min(1.0, max(0.0, final_preference))
        
        # 标准化
        total_preference = sum(preferences.values())
        if total_preference > 0:
            preferences = {k: v/total_preference for k, v in preferences.items()}
        
        return preferences
    
    def _calculate_context_adjustment(self, action_type: ActionType, context: Dict[str, Any]) -> float:
        """计算情境调整因子"""
        adjustment = 0.0
        
        # 基于学习到的情境偏好
        for context_key, context_value in context.items():
            if context_key in self.behavior_patterns['context_preferences']:
                learned_preference = self.behavior_patterns['context_preferences'][context_key]
                
                if isinstance(context_value, (int, float)) and learned_preference != 0:
                    # 情境值与学习偏好的匹配度
                    match_factor = 1.0 - abs(context_value - learned_preference)
                    adjustment += match_factor * 0.1
        
        return adjustment
    
    def _calculate_moral_framework_adjustment(self, action_type: ActionType, context: Dict[str, Any]) -> float:
        """计算道德框架调整因子"""
        # 创建测试行为
        test_action = Action(
            id="prediction_test",
            action_type=action_type,
            actor_id="player",
            target_id=context.get('target_id')
        )
        
        # 使用玩家的道德状态评估
        player_moral_state = MoralState(
            kantian_weight=self.moral_profile['moral_weights']['kantian'],
            utilitarian_weight=self.moral_profile['moral_weights']['utilitarian'],
            virtue_weight=self.moral_profile['moral_weights']['virtue'],
            empathy_level=self.moral_profile['empathy_indicators'],
            moral_courage=self.moral_profile.get('moral_courage', 0.5)
        )
        
        evaluation = self.moral_framework.evaluate_action(test_action, player_moral_state, context)
        
        # 评分越高，调整因子越大
        return (evaluation['final_score'] - 0.5) * 0.5