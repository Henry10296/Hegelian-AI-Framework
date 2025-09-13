"""
道德感知NPC智能体 - 系统的核心智能体实现
"""

import time
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

from .moral_state import MoralState
from .action import Action, ActionType
from ..ethics.moral_framework import MoralFramework
from ..neuroevolution.neural_network import MoralNeuralNetwork
from ..neuroevolution.moral_genome import MoralGenome


@dataclass
class NPCMemory:
    """NPC记忆结构"""
    player_interactions: List[Dict[str, Any]]
    moral_experiences: List[Dict[str, Any]]
    social_relationships: Dict[str, float]
    recent_events: List[str]
    
    def __post_init__(self):
        if not hasattr(self, 'player_interactions'):
            self.player_interactions = []
        if not hasattr(self, 'moral_experiences'):
            self.moral_experiences = []
        if not hasattr(self, 'social_relationships'):
            self.social_relationships = {}
        if not hasattr(self, 'recent_events'):
            self.recent_events = []


class MoralNPC:
    """道德感知NPC智能体"""
    
    def __init__(self, npc_id: str, initial_moral_state: MoralState = None, 
                 neural_genome: MoralGenome = None):
        self.npc_id = npc_id
        self.moral_state = initial_moral_state or MoralState()
        
        # 神经网络大脑
        if neural_genome:
            self.genome = neural_genome
            self.neural_network = MoralNeuralNetwork(neural_genome)
        else:
            self.genome = MoralGenome()
            self.neural_network = MoralNeuralNetwork(self.genome)
        
        # 道德框架
        self.moral_framework = MoralFramework()
        
        # 记忆系统
        self.memory = NPCMemory([], [], {}, [])
        
        # NPC属性
        self.personality_traits = {
            'openness': random.uniform(0.3, 0.8),
            'conscientiousness': random.uniform(0.4, 0.9),
            'extroversion': random.uniform(0.2, 0.8),
            'agreeableness': random.uniform(0.3, 0.8),
            'neuroticism': random.uniform(0.1, 0.6)
        }
        
        # 状态跟踪
        self.current_mood = 0.5  # [0-1] 负面到正面
        self.stress_level = 0.3  # [0-1] 压力水平
        self.last_update_time = time.time()
        
        # 行为历史
        self.action_history: List[Action] = []
        self.decision_count = 0
    
    def perceive_situation(self, situation_context: Dict[str, Any]) -> Dict[str, Any]:
        """感知和处理情境信息"""
        perception = {
            'context': situation_context,
            'moral_salience': self._calculate_moral_salience(situation_context),
            'emotional_response': self._generate_emotional_response(situation_context),
            'social_considerations': self._analyze_social_factors(situation_context),
            'personal_relevance': self._assess_personal_relevance(situation_context)
        }
        
        # 更新内部状态
        self._update_internal_state(perception)
        
        return perception
    
    def make_moral_decision(self, situation_context: Dict[str, Any], 
                          available_actions: List[ActionType] = None) -> Dict[str, Any]:
        """进行道德决策"""
        # 感知情境
        perception = self.perceive_situation(situation_context)
        
        # 生成可能的行为
        if available_actions is None:
            available_actions = self._generate_possible_actions(situation_context)
        
        # 使用神经网络进行初步决策
        neural_decision = self.neural_network.evaluate_moral_decision(situation_context)
        
        # 使用道德框架进行详细评估
        action_evaluations = []
        
        for action_type in available_actions:
            test_action = Action(
                id=f"{self.npc_id}_decision_{self.decision_count}",
                action_type=action_type,
                actor_id=self.npc_id,
                target_id=situation_context.get('target_id'),
                intensity=neural_decision['raw_outputs'][0] if neural_decision['raw_outputs'] else 0.7
            )
            
            moral_eval = self.moral_framework.evaluate_action(
                test_action, self.moral_state, situation_context
            )
            
            action_evaluations.append({
                'action': test_action,
                'moral_score': moral_eval['final_score'],
                'neural_score': neural_decision['decision_analysis']['action_tendencies'].get(
                    action_type.value, 0.0
                ),
                'evaluation_details': moral_eval
            })
        
        # 综合决策
        final_decision = self._integrate_decision_factors(
            action_evaluations, neural_decision, perception
        )
        
        # 记录决策
        self._record_decision(final_decision, situation_context)
        
        self.decision_count += 1
        
        return final_decision
    
    def _calculate_moral_salience(self, context: Dict[str, Any]) -> float:
        """计算道德显著性"""
        salience_factors = [
            context.get('harm_potential', 0.0) * 1.2,
            context.get('benefit_potential', 0.0) * 1.0,
            context.get('fairness_concern', 0.0) * 1.1,
            context.get('duty_obligation', 0.0) * 0.9,
            context.get('social_visibility', 0.0) * 0.8
        ]
        
        base_salience = sum(salience_factors) / len(salience_factors)
        
        # 个人敏感度调整
        personal_sensitivity = (
            self.moral_state.empathy_level * 0.4 +
            self.moral_state.guilt_sensitivity * 0.3 +
            self.moral_state.moral_courage * 0.3
        )
        
        return min(1.0, base_salience * (0.5 + personal_sensitivity))
    
    def _generate_emotional_response(self, context: Dict[str, Any]) -> Dict[str, float]:
        """生成情感反应"""
        emotions = {
            'empathy': 0.0,
            'anger': 0.0,
            'fear': 0.0,
            'guilt': 0.0,
            'pride': 0.0,
            'concern': 0.0
        }
        
        # 基于情境生成情感
        if context.get('harm_potential', 0.0) > 0.6:
            emotions['concern'] += 0.7 * self.moral_state.empathy_level
            emotions['anger'] += 0.5 * (1.0 - self.personality_traits['agreeableness'])
        
        if context.get('injustice_present', False):
            emotions['anger'] += 0.8 * self.moral_state.moral_courage
            emotions['concern'] += 0.6
        
        if context.get('personal_cost', 0.0) > 0.5:
            emotions['fear'] += 0.4 * self.personality_traits['neuroticism']
        
        # 标准化情感强度
        for emotion in emotions:
            emotions[emotion] = min(1.0, emotions[emotion])
        
        return emotions
    
    def _analyze_social_factors(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """分析社会因素"""
        social_analysis = {
            'peer_pressure': context.get('group_pressure', 0.0),
            'authority_influence': context.get('authority_presence', 0.0),
            'public_visibility': context.get('social_visibility', 0.0),
            'reputation_impact': 0.0,
            'social_expectation': 0.0
        }
        
        # 计算声誉影响
        if social_analysis['public_visibility'] > 0.5:
            social_analysis['reputation_impact'] = (
                social_analysis['public_visibility'] * 
                (1.0 - self.moral_state.social_pressure_resistance)
            )
        
        # 社会期望
        if context.get('social_norms'):
            expected_behavior = context['social_norms'].get('expected_behavior', '')
            if expected_behavior:
                social_analysis['social_expectation'] = 0.7
        
        return social_analysis
    
    def _assess_personal_relevance(self, context: Dict[str, Any]) -> float:
        """评估个人相关性"""
        relevance = 0.5  # 基础相关性
        
        # 检查个人利益
        if context.get('personal_benefit', 0.0) > 0:
            relevance += 0.3 * context['personal_benefit']
        
        if context.get('personal_cost', 0.0) > 0:
            relevance += 0.2 * context['personal_cost']
        
        # 关系相关性
        target_id = context.get('target_id')
        if target_id and target_id in self.memory.social_relationships:
            relationship_strength = self.memory.social_relationships[target_id]
            relevance += 0.4 * abs(relationship_strength)
        
        # 价值观匹配
        if context.get('value_alignment'):
            relevance += 0.3 * context['value_alignment']
        
        return min(1.0, relevance)
    
    def _update_internal_state(self, perception: Dict[str, Any]):
        """更新内部状态"""
        # 更新情绪状态
        emotional_response = perception['emotional_response']
        positive_emotions = emotional_response.get('pride', 0) + emotional_response.get('empathy', 0)
        negative_emotions = emotional_response.get('anger', 0) + emotional_response.get('fear', 0) + emotional_response.get('guilt', 0)
        
        mood_change = (positive_emotions - negative_emotions) * 0.1
        self.current_mood = max(0.0, min(1.0, self.current_mood + mood_change))
        
        # 更新压力水平
        stress_factors = perception['moral_salience'] * 0.3 + negative_emotions * 0.2
        self.stress_level = max(0.0, min(1.0, self.stress_level + stress_factors * 0.1 - 0.05))
    
    def _generate_possible_actions(self, context: Dict[str, Any]) -> List[ActionType]:
        """生成可能的行为选项"""
        possible_actions = [ActionType.HELP, ActionType.COOPERATE, ActionType.IGNORE]
        
        # 基于情境添加特定行为
        if context.get('conflict_present', False):
            possible_actions.extend([ActionType.COMPETE, ActionType.HARM])
        
        if context.get('resources_available', False):
            possible_actions.append(ActionType.SHARE)
        
        if context.get('deception_possible', False):
            possible_actions.append(ActionType.DECEIVE)
        
        if context.get('sacrifice_option', False):
            possible_actions.append(ActionType.SACRIFICE)
        
        if context.get('communication_needed', True):
            possible_actions.append(ActionType.COMMUNICATE)
        
        return list(set(possible_actions))  # 去重
    
    def _integrate_decision_factors(self, action_evaluations: List[Dict], 
                                  neural_decision: Dict, perception: Dict) -> Dict[str, Any]:
        """整合决策因素"""
        # 计算每个行为的综合评分
        integrated_scores = []
        
        for eval_data in action_evaluations:
            moral_score = eval_data['moral_score']
            neural_score = eval_data['neural_score']
            
            # 权重整合
            moral_weight = 0.6
            neural_weight = 0.4
            
            # 情感和个性调整
            emotional_response = perception['emotional_response']
            personality_adjustment = self._calculate_personality_adjustment(
                eval_data['action'], emotional_response
            )
            
            integrated_score = (
                moral_score * moral_weight + 
                neural_score * neural_weight + 
                personality_adjustment * 0.2
            )
            
            integrated_scores.append({
                'action': eval_data['action'],
                'integrated_score': integrated_score,
                'moral_score': moral_score,
                'neural_score': neural_score,
                'personality_adjustment': personality_adjustment,
                'evaluation_details': eval_data['evaluation_details']
            })
        
        # 选择最高评分的行为
        best_choice = max(integrated_scores, key=lambda x: x['integrated_score'])
        
        return {
            'chosen_action': best_choice['action'],
            'decision_confidence': best_choice['integrated_score'],
            'all_evaluations': integrated_scores,
            'neural_analysis': neural_decision,
            'perception': perception,
            'reasoning': self._generate_decision_reasoning(best_choice, perception)
        }
    
    def _calculate_personality_adjustment(self, action: Action, 
                                       emotional_response: Dict[str, float]) -> float:
        """基于个性特征计算行为调整"""
        adjustment = 0.0
        
        # 基于行为类型和个性的调整
        if action.action_type == ActionType.HELP:
            adjustment += self.personality_traits['agreeableness'] * 0.3
            adjustment += emotional_response.get('empathy', 0) * 0.2
        
        elif action.action_type == ActionType.COMPETE:
            adjustment += (1.0 - self.personality_traits['agreeableness']) * 0.2
            adjustment -= self.personality_traits['conscientiousness'] * 0.1
        
        elif action.action_type == ActionType.SACRIFICE:
            adjustment += self.personality_traits['conscientiousness'] * 0.3
            adjustment += self.moral_state.moral_courage * 0.2
        
        elif action.action_type == ActionType.DECEIVE:
            adjustment -= self.personality_traits['conscientiousness'] * 0.4
            adjustment += emotional_response.get('fear', 0) * 0.1
        
        elif action.action_type == ActionType.COMMUNICATE:
            adjustment += self.personality_traits['extroversion'] * 0.2
            adjustment += self.personality_traits['openness'] * 0.1
        
        return max(-0.3, min(0.3, adjustment))  # 限制调整范围
    
    def _generate_decision_reasoning(self, best_choice: Dict, perception: Dict) -> str:
        """生成决策推理说明"""
        action = best_choice['action']
        reasoning_parts = []
        
        # 基于主导道德框架的推理
        dominant_framework = self.moral_state.get_dominant_moral_framework()
        
        if dominant_framework == 'kantian':
            reasoning_parts.append("基于道德义务考虑")
            if action.action_type in [ActionType.HELP, ActionType.SACRIFICE]:
                reasoning_parts.append("此行为符合道德法则")
        
        elif dominant_framework == 'utilitarian':
            reasoning_parts.append("基于整体效用考虑")
            if action.action_type in [ActionType.COOPERATE, ActionType.SHARE]:
                reasoning_parts.append("此行为能带来更大的整体福利")
        
        else:
            reasoning_parts.append("基于品德伦理考虑")
        
        # 情感因素
        dominant_emotion = max(perception['emotional_response'].items(), 
                             key=lambda x: x[1])
        if dominant_emotion[1] > 0.5:
            reasoning_parts.append(f"受到{dominant_emotion[0]}情感的影响")
        
        # 社会因素
        social_factors = perception['social_considerations']
        if social_factors['peer_pressure'] > 0.6:
            reasoning_parts.append("考虑到同伴压力")
        if social_factors['public_visibility'] > 0.7:
            reasoning_parts.append("考虑到公众影响")
        
        return "; ".join(reasoning_parts) if reasoning_parts else "基于综合考虑做出决策"
    
    def _record_decision(self, decision: Dict[str, Any], context: Dict[str, Any]):
        """记录决策历史"""
        action = decision['chosen_action']
        self.action_history.append(action)
        
        # 记录到记忆中
        decision_record = {
            'action': action,
            'context': context,
            'decision_confidence': decision['decision_confidence'],
            'reasoning': decision['reasoning'],
            'timestamp': time.time()
        }
        
        self.memory.moral_experiences.append(decision_record)
        
        # 只保留最近的经验
        if len(self.memory.moral_experiences) > 50:
            self.memory.moral_experiences = self.memory.moral_experiences[-50:]
    
    def learn_from_outcome(self, action_outcome: float, social_feedback: float):
        """从结果中学习"""
        if not self.action_history:
            return
        
        last_action = self.action_history[-1]
        
        # 更新道德状态
        self.moral_state.update_from_experience(
            last_action.action_type.value,
            action_outcome,
            social_feedback
        )
        
        # 更新记忆
        if self.memory.moral_experiences:
            last_experience = self.memory.moral_experiences[-1]
            last_experience['outcome'] = action_outcome
            last_experience['social_feedback'] = social_feedback
    
    def interact_with_player(self, player_id: str, interaction_context: Dict[str, Any]) -> Dict[str, Any]:
        """与玩家交互"""
        # 记录交互
        interaction_record = {
            'player_id': player_id,
            'context': interaction_context,
            'timestamp': time.time(),
            'npc_mood': self.current_mood,
            'npc_stress': self.stress_level
        }
        
        self.memory.player_interactions.append(interaction_record)
        
        # 更新对玩家的关系
        if player_id not in self.memory.social_relationships:
            self.memory.social_relationships[player_id] = 0.0
        
        # 基于交互调整关系
        interaction_valence = interaction_context.get('valence', 0.0)
        relationship_change = interaction_valence * 0.1
        
        current_relationship = self.memory.social_relationships[player_id]
        self.memory.social_relationships[player_id] = max(-1.0, min(1.0, 
            current_relationship + relationship_change))
        
        # 生成响应
        response = self._generate_interaction_response(player_id, interaction_context)
        
        return response
    
    def _generate_interaction_response(self, player_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """生成交互响应"""
        relationship = self.memory.social_relationships.get(player_id, 0.0)
        
        # 基于关系和情境生成响应
        response_warmth = max(0.1, min(1.0, 0.5 + relationship * 0.4 + self.current_mood * 0.1))
        response_trust = max(0.0, min(1.0, 0.5 + relationship * 0.5))
        
        # 响应类型
        if response_warmth > 0.7:
            response_type = "friendly"
        elif response_warmth > 0.4:
            response_type = "neutral"
        else:
            response_type = "cold"
        
        return {
            'response_type': response_type,
            'warmth': response_warmth,
            'trust_level': response_trust,
            'relationship_status': relationship,
            'dialogue_suggestion': self._suggest_dialogue(response_type, context),
            'behavioral_tendency': self._suggest_behavior_tendency(context)
        }
    
    def _suggest_dialogue(self, response_type: str, context: Dict[str, Any]) -> str:
        """建议对话内容"""
        dialogue_templates = {
            'friendly': [
                "很高兴见到你！有什么我可以帮助的吗？",
                "你好！你今天过得怎么样？",
                "我一直在想我们上次的谈话..."
            ],
            'neutral': [
                "你好。有什么事情吗？",
                "需要什么帮助吗？",
                "你在这里做什么？"
            ],
            'cold': [
                "...",
                "我很忙。",
                "你想要什么？"
            ]
        }
        
        templates = dialogue_templates.get(response_type, dialogue_templates['neutral'])
        return random.choice(templates)
    
    def _suggest_behavior_tendency(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """建议行为倾向"""
        tendencies = {
            'cooperation_likelihood': 0.5,
            'help_willingness': 0.5,
            'trust_disposition': 0.5,
            'information_sharing': 0.5
        }
        
        # 基于当前状态调整
        mood_factor = (self.current_mood - 0.5) * 0.4
        stress_factor = -self.stress_level * 0.2
        
        for tendency in tendencies:
            tendencies[tendency] += mood_factor + stress_factor
            tendencies[tendency] = max(0.0, min(1.0, tendencies[tendency]))
        
        return tendencies
    
    def get_current_status(self) -> Dict[str, Any]:
        """获取当前状态摘要"""
        return {
            'npc_id': self.npc_id,
            'moral_profile': {
                'dominant_framework': self.moral_state.get_dominant_moral_framework(),
                'empathy_level': self.moral_state.empathy_level,
                'moral_courage': self.moral_state.moral_courage,
                'consistency_score': len(self.action_history) / max(1, len(set(a.action_type for a in self.action_history)))
            },
            'current_state': {
                'mood': self.current_mood,
                'stress_level': self.stress_level,
                'decision_count': self.decision_count
            },
            'relationships': dict(list(self.memory.social_relationships.items())[-5:]),  # 最近5个关系
            'recent_actions': [a.action_type.value for a in self.action_history[-3:]]  # 最近3个行为
        }
    
    def reset_to_baseline(self):
        """重置到基线状态"""
        self.current_mood = 0.5
        self.stress_level = 0.3
        self.decision_count = 0
        self.action_history = []
        self.memory = NPCMemory([], [], {}, [])