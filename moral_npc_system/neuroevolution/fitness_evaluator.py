"""
适应度评估器 - 评估NPC在道德情境中的表现
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from .moral_genome import MoralGenome
from .neural_network import MoralNeuralNetwork
from ..ethics.moral_framework import MoralFramework
from ..core.action import Action, ActionType
from ..core.moral_state import MoralState


class FitnessEvaluator:
    """道德NPC适应度评估器"""
    
    def __init__(self):
        self.moral_framework = MoralFramework()
        
        # 评估权重
        self.evaluation_weights = {
            'moral_consistency': 0.3,      # 道德一致性
            'social_adaptation': 0.25,     # 社会适应性
            'player_alignment': 0.2,       # 与玩家道德的匹配度
            'behavioral_diversity': 0.15,  # 行为多样性
            'learning_efficiency': 0.1     # 学习效率
        }
        
        # 预定义的道德情境模板
        self.moral_scenarios = [
            self._create_trolley_problem(),
            self._create_resource_sharing_scenario(),
            self._create_promise_keeping_scenario(),
            self._create_authority_conflict_scenario(),
            self._create_group_pressure_scenario()
        ]
    
    def evaluate_genome_on_scenario(self, genome: MoralGenome, network: MoralNeuralNetwork, 
                                  scenario: Dict[str, Any]) -> float:
        """评估基因组在特定情境下的适应度"""
        
        # 从基因组构建道德状态
        moral_state = self._genome_to_moral_state(genome)
        
        # 获取网络决策
        decision_result = network.evaluate_moral_decision(scenario)
        
        # 评估不同方面的表现
        scores = {}
        
        # 1. 道德一致性评估
        scores['moral_consistency'] = self._evaluate_moral_consistency(
            decision_result, moral_state, scenario
        )
        
        # 2. 社会适应性评估
        scores['social_adaptation'] = self._evaluate_social_adaptation(
            decision_result, scenario
        )
        
        # 3. 玩家匹配度评估 (如果有玩家数据)
        if 'player_moral_profile' in scenario:
            scores['player_alignment'] = self._evaluate_player_alignment(
                decision_result, scenario['player_moral_profile']
            )
        else:
            scores['player_alignment'] = 0.5  # 中性分数
        
        # 4. 行为多样性评估
        scores['behavioral_diversity'] = self._evaluate_behavioral_diversity(
            decision_result
        )
        
        # 5. 学习效率评估 (基于历史表现)
        scores['learning_efficiency'] = self._evaluate_learning_efficiency(
            genome, scenario
        )
        
        # 计算加权总分
        total_fitness = sum(
            scores[aspect] * self.evaluation_weights[aspect]
            for aspect in scores
        )
        
        # 添加特殊奖励/惩罚
        total_fitness += self._calculate_special_modifiers(decision_result, scenario)
        
        return max(0.0, min(1.0, total_fitness))
    
    def _genome_to_moral_state(self, genome: MoralGenome) -> MoralState:
        """将基因组转换为道德状态"""
        moral_params = genome.moral_parameters
        
        return MoralState(
            kantian_weight=moral_params['kantian_weight'],
            utilitarian_weight=moral_params['utilitarian_weight'],
            virtue_weight=moral_params['virtue_weight'],
            empathy_level=moral_params['empathy_sensitivity'],
            moral_courage=moral_params.get('moral_courage', 0.5),
            guilt_sensitivity=moral_params.get('guilt_sensitivity', 0.5),
            context_sensitivity=moral_params.get('context_sensitivity', 0.5),
            social_pressure_resistance=1.0 - moral_params['social_conformity'],
            moral_plasticity=0.3,
            learning_rate=0.1
        )
    
    def _evaluate_moral_consistency(self, decision_result: Dict, moral_state: MoralState, 
                                  scenario: Dict[str, Any]) -> float:
        """评估道德一致性"""
        # 模拟可能的行为选择
        possible_actions = self._generate_possible_actions(scenario)
        
        consistency_scores = []
        
        for action in possible_actions:
            # 使用道德框架评估每个行为
            moral_evaluation = self.moral_framework.evaluate_action(
                action, moral_state, scenario
            )
            
            # 检查网络推荐是否与道德框架一致
            network_preference = decision_result['action_tendencies'].get(
                action.action_type.value, 0.0
            )
            
            framework_score = moral_evaluation['final_score']
            
            # 计算一致性 (两者都高或都低表示一致)
            if framework_score > 0.5 and network_preference > 0.5:
                consistency = min(framework_score, network_preference)
            elif framework_score <= 0.5 and network_preference <= 0.5:
                consistency = 1.0 - max(framework_score, network_preference)
            else:
                consistency = 0.5 - abs(framework_score - network_preference)
            
            consistency_scores.append(max(0.0, consistency))
        
        return np.mean(consistency_scores) if consistency_scores else 0.5
    
    def _evaluate_social_adaptation(self, decision_result: Dict, scenario: Dict[str, Any]) -> float:
        """评估社会适应性"""
        social_score = 0.5  # 基础分数
        
        # 检查是否适应社会环境
        social_norms = scenario.get('social_norms', {})
        decision_action = decision_result.get('recommended_action', '')
        
        # 社会期望的行为
        expected_behavior = social_norms.get('expected_behavior', '')
        if decision_action == expected_behavior:
            social_score += 0.3
        
        # 考虑社会可见性
        visibility = scenario.get('social_visibility', 0.0)
        if visibility > 0.7:
            # 高可见性情况下，更符合社会期望的行为得分更高
            prosocial_actions = ['help', 'cooperate', 'share']
            if decision_action in prosocial_actions:
                social_score += 0.2
        
        # 权威存在的情况
        authority = scenario.get('authority_presence', 0.0)
        if authority > 0.5:
            # 权威在场时的适当行为
            compliant_actions = ['cooperate', 'help']
            if decision_action in compliant_actions:
                social_score += 0.1
        
        return max(0.0, min(1.0, social_score))
    
    def _evaluate_player_alignment(self, decision_result: Dict, player_profile: Dict[str, Any]) -> float:
        """评估与玩家道德倾向的匹配度"""
        npc_action = decision_result.get('recommended_action', '')
        npc_tendencies = decision_result.get('action_tendencies', {})
        
        # 玩家的道德倾向
        player_moral_weights = player_profile.get('moral_weights', {})
        player_preferred_actions = player_profile.get('preferred_actions', [])
        
        alignment_score = 0.5
        
        # 检查行为偏好匹配
        if npc_action in player_preferred_actions:
            alignment_score += 0.3
        
        # 检查道德框架匹配
        if player_moral_weights:
            # 计算道德框架的相似性
            framework_similarity = self._calculate_moral_framework_similarity(
                decision_result, player_moral_weights
            )
            alignment_score += framework_similarity * 0.2
        
        return max(0.0, min(1.0, alignment_score))
    
    def _evaluate_behavioral_diversity(self, decision_result: Dict) -> float:
        """评估行为多样性"""
        action_tendencies = decision_result.get('action_tendencies', {})
        
        if not action_tendencies:
            return 0.0
        
        # 计算行为倾向的分布
        tendency_values = list(action_tendencies.values())
        
        # 使用熵来衡量多样性
        # 避免过于极端的行为模式
        entropy = self._calculate_entropy(tendency_values)
        max_entropy = np.log(len(tendency_values))  # 最大可能熵
        
        if max_entropy > 0:
            normalized_entropy = entropy / max_entropy
        else:
            normalized_entropy = 0.0
        
        # 适度的多样性是好的，但不要过于随机
        diversity_score = 1.0 - abs(normalized_entropy - 0.7)  # 目标熵为0.7
        
        return max(0.0, min(1.0, diversity_score))
    
    def _evaluate_learning_efficiency(self, genome: MoralGenome, scenario: Dict[str, Any]) -> float:
        """评估学习效率"""
        # 基于基因组的历史表现评估学习能力
        # 这里使用简化的评估方法
        
        # 检查道德参数的合理性
        moral_params = genome.moral_parameters
        
        efficiency_score = 0.5
        
        # 参数平衡性
        weights = [moral_params['kantian_weight'], 
                  moral_params['utilitarian_weight'], 
                  moral_params['virtue_weight']]
        
        # 避免过于极端的权重分布
        weight_balance = 1.0 - np.std(weights)
        efficiency_score += weight_balance * 0.3
        
        # 情感参数的合理性
        empathy = moral_params['empathy_sensitivity']
        risk_aversion = moral_params['risk_aversion']
        
        # 适度的共情和风险规避是好的
        emotion_balance = 1.0 - abs(empathy - 0.6) - abs(risk_aversion - 0.5)
        efficiency_score += emotion_balance * 0.2
        
        return max(0.0, min(1.0, efficiency_score))
    
    def _calculate_special_modifiers(self, decision_result: Dict, scenario: Dict[str, Any]) -> float:
        """计算特殊奖励/惩罚修正"""
        modifier = 0.0
        
        decision_action = decision_result.get('recommended_action', '')
        scenario_type = scenario.get('scenario_type', '')
        
        # 特殊情境的奖励/惩罚
        if scenario_type == 'emergency':
            # 紧急情况下的适当响应
            if decision_action in ['help', 'cooperate']:
                modifier += 0.1
        
        elif scenario_type == 'moral_dilemma':
            # 道德两难中的深思熟虑
            decision_certainty = decision_result.get('decision_certainty', 0.0)
            if 0.3 <= decision_certainty <= 0.8:  # 适度的不确定性表示深思
                modifier += 0.05
        
        # 惩罚明显不道德的行为
        if decision_action in ['harm', 'deceive']:
            harm_severity = scenario.get('harm_potential', 0.0)
            modifier -= harm_severity * 0.2
        
        return modifier
    
    def _generate_possible_actions(self, scenario: Dict[str, Any]) -> List[Action]:
        """生成情境中可能的行为"""
        possible_actions = []
        
        scenario_context = scenario.get('context', {})
        
        # 基本行为选择
        basic_actions = [ActionType.HELP, ActionType.COOPERATE, ActionType.IGNORE]
        
        # 根据情境添加特定行为
        if scenario.get('conflict_present', False):
            basic_actions.extend([ActionType.COMPETE, ActionType.HARM])
        
        if scenario.get('resources_available', False):
            basic_actions.append(ActionType.SHARE)
        
        if scenario.get('sacrifice_possible', False):
            basic_actions.append(ActionType.SACRIFICE)
        
        for action_type in basic_actions:
            action = Action(
                id=f"test_{action_type.value}",
                action_type=action_type,
                actor_id="npc_test",
                target_id=scenario.get('target_id', 'other'),
                intensity=0.7
            )
            possible_actions.append(action)
        
        return possible_actions
    
    def _calculate_entropy(self, values: List[float]) -> float:
        """计算熵"""
        if not values or all(v == 0 for v in values):
            return 0.0
        
        # 标准化值
        total = sum(abs(v) for v in values)
        if total == 0:
            return 0.0
        
        probabilities = [abs(v) / total for v in values]
        
        entropy = 0.0
        for p in probabilities:
            if p > 0:
                entropy -= p * np.log(p)
        
        return entropy
    
    def _calculate_moral_framework_similarity(self, decision_result: Dict, 
                                            player_weights: Dict[str, float]) -> float:
        """计算道德框架相似性"""
        # 这里需要从decision_result中推断NPC的道德框架倾向
        # 简化实现
        return 0.5
    
    # 预定义情境生成方法
    def _create_trolley_problem(self) -> Dict[str, Any]:
        """创建电车难题情境"""
        return {
            'scenario_type': 'moral_dilemma',
            'description': '电车即将撞死5个人，你可以拉杆让它转向撞死1个人',
            'urgency': 0.9,
            'harm_potential': 0.8,
            'benefit_potential': 0.6,
            'social_visibility': 0.3,
            'resource_cost': 0.1,
            'emotional_stakes': 0.9,
            'rule_violation': 0.7,
            'duty_obligation': 0.8,
            'target_id': 'potential_victims'
        }
    
    def _create_resource_sharing_scenario(self) -> Dict[str, Any]:
        """创建资源分享情境"""
        return {
            'scenario_type': 'resource_allocation',
            'description': '发现食物，附近有饥饿的人',
            'urgency': 0.4,
            'harm_potential': 0.2,
            'benefit_potential': 0.7,
            'social_visibility': 0.6,
            'resource_cost': 0.5,
            'emotional_stakes': 0.5,
            'fairness_concern': 0.8,
            'resources_available': True,
            'target_id': 'hungry_person'
        }
    
    def _create_promise_keeping_scenario(self) -> Dict[str, Any]:
        """创建承诺保持情境"""
        return {
            'scenario_type': 'promise_keeping',
            'description': '之前承诺帮助某人，但现在有更紧急的事情',
            'urgency': 0.7,
            'harm_potential': 0.3,
            'benefit_potential': 0.5,
            'social_visibility': 0.5,
            'emotional_stakes': 0.6,
            'duty_obligation': 0.9,
            'target_id': 'promise_recipient'
        }
    
    def _create_authority_conflict_scenario(self) -> Dict[str, Any]:
        """创建权威冲突情境"""
        return {
            'scenario_type': 'authority_conflict',
            'description': '权威要求做不道德的事情',
            'urgency': 0.5,
            'harm_potential': 0.6,
            'benefit_potential': 0.3,
            'social_visibility': 0.8,
            'authority_presence': 0.9,
            'rule_violation': 0.7,
            'moral_courage_required': True,
            'target_id': 'authority_figure'
        }
    
    def _create_group_pressure_scenario(self) -> Dict[str, Any]:
        """创建群体压力情境"""
        return {
            'scenario_type': 'group_pressure',
            'description': '群体鼓励做有问题的行为',
            'urgency': 0.3,
            'harm_potential': 0.5,
            'benefit_potential': 0.4,
            'social_visibility': 0.9,
            'group_pressure': 0.8,
            'social_norms': {'expected_behavior': 'conform'},
            'target_id': 'group_members'
        }