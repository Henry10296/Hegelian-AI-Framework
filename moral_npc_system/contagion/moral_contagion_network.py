"""
道德传染网络 - 核心道德传染机制实现
"""

import time
import random
from typing import Dict, List, Set, Tuple, Optional, Any, Callable
from collections import defaultdict, deque
import numpy as np

from .social_network import SocialNetwork, Relationship
from .moral_event import MoralEvent, MoralEventType, MoralValence
from ..core.moral_state import MoralState


class MoralInfluence:
    """道德影响对象"""
    
    def __init__(self, source_event: MoralEvent, influence_strength: float, 
                 propagation_path: List[str], distance: int):
        self.source_event = source_event
        self.influence_strength = influence_strength
        self.propagation_path = propagation_path
        self.distance = distance
        self.timestamp = time.time()
        
        # 影响衰减参数
        self.decay_rate = 0.1
        self.half_life = 24.0  # 24小时半衰期
    
    def get_current_strength(self, current_time: float = None) -> float:
        """获取当前影响强度 (考虑时间衰减)"""
        if current_time is None:
            current_time = time.time()
        
        time_elapsed = current_time - self.timestamp
        decay_factor = np.exp(-self.decay_rate * time_elapsed / self.half_life)
        
        return self.influence_strength * decay_factor
    
    def is_expired(self, current_time: float = None, threshold: float = 0.01) -> bool:
        """判断影响是否已过期"""
        return self.get_current_strength(current_time) < threshold


class MoralContagionNetwork:
    """道德传染网络核心类"""
    
    def __init__(self, social_network: SocialNetwork):
        self.social_network = social_network
        
        # NPC道德状态映射
        self.npc_moral_states: Dict[str, MoralState] = {}
        
        # 活跃的道德影响
        self.active_influences: Dict[str, List[MoralInfluence]] = defaultdict(list)
        
        # 道德事件历史
        self.event_history: List[MoralEvent] = []
        self.event_index: Dict[str, MoralEvent] = {}
        
        # 传播参数
        self.propagation_params = {
            'base_transmission_rate': 0.7,      # 基础传播率
            'distance_decay_factor': 0.8,       # 距离衰减因子
            'relationship_weight_factor': 1.2,  # 关系权重因子
            'similarity_boost_factor': 1.5,     # 相似性增强因子
            'max_propagation_distance': 4,      # 最大传播距离
            'min_influence_threshold': 0.05     # 最小影响阈值
        }
        
        # 统计信息
        self.contagion_stats = {
            'total_events': 0,
            'successful_transmissions': 0,
            'blocked_transmissions': 0,
            'average_propagation_distance': 0.0,
            'most_influential_event': None
        }
    
    def add_npc(self, npc_id: str, moral_state: MoralState):
        """添加NPC到道德传染网络"""
        self.npc_moral_states[npc_id] = moral_state
        self.social_network.add_npc(npc_id)
        self.active_influences[npc_id] = []
    
    def introduce_moral_event(self, event: MoralEvent) -> Dict[str, Any]:
        """引入道德事件并开始传播"""
        # 记录事件
        self.event_history.append(event)
        self.event_index[event.event_id] = event
        self.contagion_stats['total_events'] += 1
        
        # 开始传播
        propagation_result = self._propagate_moral_influence(event)
        
        # 更新统计
        self._update_propagation_stats(event, propagation_result)
        
        return {
            'event_id': event.event_id,
            'initial_actor': event.primary_actor,
            'affected_npcs': propagation_result['affected_npcs'],
            'transmission_paths': propagation_result['transmission_paths'],
            'total_transmissions': propagation_result['total_transmissions'],
            'propagation_depth': propagation_result['max_depth']
        }
    
    def _propagate_moral_influence(self, event: MoralEvent) -> Dict[str, Any]:
        """传播道德影响"""
        affected_npcs = set()
        transmission_paths = []
        
        # 使用广度优先搜索进行传播
        queue = deque([(event.primary_actor, 1.0, [event.primary_actor], 0)])
        visited = {event.primary_actor}
        
        while queue:
            current_npc, current_strength, path, distance = queue.popleft()
            
            if distance >= self.propagation_params['max_propagation_distance']:
                continue
                
            if current_strength < self.propagation_params['min_influence_threshold']:
                continue
            
            # 获取邻居
            neighbors = self.social_network.get_neighbors(current_npc)
            
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                
                # 计算传播概率
                transmission_prob = self._calculate_transmission_probability(
                    event, current_npc, neighbor, current_strength, distance
                )
                
                # 决定是否传播
                if random.random() < transmission_prob:
                    # 计算新的影响强度
                    new_strength = self._calculate_influence_strength(
                        event, current_npc, neighbor, current_strength
                    )
                    
                    if new_strength >= self.propagation_params['min_influence_threshold']:
                        # 创建影响对象
                        new_path = path + [neighbor]
                        influence = MoralInfluence(
                            source_event=event,
                            influence_strength=new_strength,
                            propagation_path=new_path,
                            distance=distance + 1
                        )
                        
                        # 应用影响
                        self._apply_moral_influence(neighbor, influence)
                        
                        # 记录结果
                        affected_npcs.add(neighbor)
                        transmission_paths.append(new_path)
                        
                        # 继续传播
                        queue.append((neighbor, new_strength, new_path, distance + 1))
                        visited.add(neighbor)
                        
                        self.contagion_stats['successful_transmissions'] += 1
                    else:
                        self.contagion_stats['blocked_transmissions'] += 1
                else:
                    self.contagion_stats['blocked_transmissions'] += 1
        
        return {
            'affected_npcs': list(affected_npcs),
            'transmission_paths': transmission_paths,
            'total_transmissions': len(affected_npcs),
            'max_depth': max([len(path) - 1 for path in transmission_paths]) if transmission_paths else 0
        }
    
    def _calculate_transmission_probability(self, event: MoralEvent, source_npc: str, 
                                         target_npc: str, current_strength: float, 
                                         distance: int) -> float:
        """计算传播概率"""
        base_prob = self.propagation_params['base_transmission_rate']
        
        # 距离衰减
        distance_factor = (self.propagation_params['distance_decay_factor'] ** distance)
        
        # 关系强度影响
        relationship = self.social_network.get_relationship(source_npc, target_npc)
        if relationship:
            relationship_factor = relationship.calculate_influence_factor()
            relationship_factor = abs(relationship_factor)  # 负关系也能传播，但效果相反
        else:
            relationship_factor = 0.1  # 无直接关系时的基础传播率
        
        # 道德相似性影响
        similarity_factor = self._calculate_moral_similarity(source_npc, target_npc)
        
        # 目标NPC的接受性
        target_receptivity = self._calculate_receptivity(target_npc, event)
        
        # 事件强度影响
        event_strength = event.propagation_strength
        
        # 综合计算
        transmission_prob = (
            base_prob * 
            distance_factor * 
            relationship_factor * 
            (1.0 + similarity_factor * self.propagation_params['similarity_boost_factor']) *
            target_receptivity * 
            event_strength * 
            current_strength
        )
        
        return min(1.0, max(0.0, transmission_prob))
    
    def _calculate_influence_strength(self, event: MoralEvent, source_npc: str, 
                                    target_npc: str, current_strength: float) -> float:
        """计算影响强度"""
        # 基础强度衰减
        base_decay = 0.8
        
        # 关系调节
        relationship = self.social_network.get_relationship(source_npc, target_npc)
        if relationship:
            relationship_multiplier = abs(relationship.calculate_influence_factor())
        else:
            relationship_multiplier = 0.5
        
        # 道德匹配度调节
        moral_match = self._calculate_moral_compatibility(target_npc, event)
        
        new_strength = current_strength * base_decay * relationship_multiplier * moral_match
        
        return max(0.0, min(1.0, new_strength))
    
    def _apply_moral_influence(self, npc_id: str, influence: MoralInfluence):
        """应用道德影响到NPC"""
        if npc_id not in self.npc_moral_states:
            return
        
        # 添加到活跃影响列表
        self.active_influences[npc_id].append(influence)
        
        # 立即应用影响
        self._update_npc_moral_state(npc_id, influence)
    
    def _update_npc_moral_state(self, npc_id: str, influence: MoralInfluence):
        """更新NPC道德状态"""
        moral_state = self.npc_moral_states[npc_id]
        event = influence.source_event
        strength = influence.get_current_strength()
        
        # 计算道德参数调整
        adjustments = self._calculate_moral_adjustments(event, strength)
        
        # 应用调整 (使用学习速率控制变化幅度)
        learning_rate = moral_state.learning_rate * moral_state.moral_plasticity
        
        for param, adjustment in adjustments.items():
            if hasattr(moral_state, param):
                current_value = getattr(moral_state, param)
                new_value = current_value + adjustment * learning_rate
                
                # 限制范围
                if param.endswith('_weight'):
                    new_value = max(0.01, min(0.99, new_value))
                else:
                    new_value = max(0.0, min(1.0, new_value))
                
                setattr(moral_state, param, new_value)
        
        # 重新标准化权重
        if any(param.endswith('_weight') for param in adjustments):
            moral_state._normalize_weights()
        
        # 记录经验
        outcome = 1.0 if event.valence in [MoralValence.POSITIVE] else -1.0
        social_feedback = strength  # 简化：影响强度作为社会反馈
        
        moral_state.update_from_experience(
            event.event_type.value, outcome, social_feedback
        )
    
    def _calculate_moral_adjustments(self, event: MoralEvent, strength: float) -> Dict[str, float]:
        """计算道德参数调整"""
        adjustments = {}
        
        # 基于事件类型的调整
        event_effects = {
            MoralEventType.ALTRUISTIC_ACT: {
                'empathy_level': 0.1,
                'utilitarian_weight': 0.05,
                'moral_courage': 0.05
            },
            MoralEventType.SELFISH_ACT: {
                'empathy_level': -0.1,
                'kantian_weight': -0.05,
                'guilt_sensitivity': 0.05
            },
            MoralEventType.COOPERATION: {
                'utilitarian_weight': 0.08,
                'social_pressure_resistance': -0.05
            },
            MoralEventType.BETRAYAL: {
                'guilt_sensitivity': 0.1,
                'social_pressure_resistance': 0.05,
                'empathy_level': -0.05
            },
            MoralEventType.JUSTICE_ACTION: {
                'kantian_weight': 0.1,
                'moral_courage': 0.08
            },
            MoralEventType.SACRIFICE: {
                'moral_courage': 0.1,
                'kantian_weight': 0.05,
                'empathy_level': 0.05
            }
        }
        
        base_adjustments = event_effects.get(event.event_type, {})
        
        # 根据事件价值倾向调整方向
        valence_multiplier = 1.0
        if event.valence == MoralValence.NEGATIVE:
            valence_multiplier = -1.0
        elif event.valence == MoralValence.AMBIGUOUS:
            valence_multiplier = 0.5
        elif event.valence == MoralValence.NEUTRAL:
            valence_multiplier = 0.2
        
        # 应用强度和价值倾向
        for param, base_change in base_adjustments.items():
            adjustments[param] = base_change * valence_multiplier * strength
        
        return adjustments
    
    def _calculate_moral_similarity(self, npc1_id: str, npc2_id: str) -> float:
        """计算道德相似性"""
        if npc1_id not in self.npc_moral_states or npc2_id not in self.npc_moral_states:
            return 0.5
        
        state1 = self.npc_moral_states[npc1_id]
        state2 = self.npc_moral_states[npc2_id]
        
        # 计算道德距离的逆
        moral_distance = state1.moral_distance_to(state2)
        similarity = 1.0 - moral_distance
        
        return max(0.0, min(1.0, similarity))
    
    def _calculate_moral_compatibility(self, npc_id: str, event: MoralEvent) -> float:
        """计算NPC与事件的道德兼容性"""
        if npc_id not in self.npc_moral_states:
            return 0.5
        
        moral_state = self.npc_moral_states[npc_id]
        
        # 基于主导道德框架的兼容性
        dominant_framework = moral_state.get_dominant_moral_framework()
        
        compatibility_scores = {
            'kantian': self._evaluate_kantian_compatibility(event),
            'utilitarian': self._evaluate_utilitarian_compatibility(event),
            'virtue': self._evaluate_virtue_compatibility(event)
        }
        
        base_compatibility = compatibility_scores.get(dominant_framework, 0.5)
        
        # 考虑情感因素
        emotional_factor = self._calculate_emotional_compatibility(moral_state, event)
        
        # 综合兼容性
        overall_compatibility = (base_compatibility + emotional_factor) / 2.0
        
        return max(0.0, min(1.0, overall_compatibility))
    
    def _evaluate_kantian_compatibility(self, event: MoralEvent) -> float:
        """评估康德伦理学兼容性"""
        kantian_positive_events = [
            MoralEventType.JUSTICE_ACTION, MoralEventType.SACRIFICE, 
            MoralEventType.ALTRUISTIC_ACT
        ]
        
        kantian_negative_events = [
            MoralEventType.BETRAYAL, MoralEventType.EXPLOITATION,
            MoralEventType.CORRUPTION
        ]
        
        if event.event_type in kantian_positive_events:
            return 0.8 if event.valence == MoralValence.POSITIVE else 0.2
        elif event.event_type in kantian_negative_events:
            return 0.2 if event.valence == MoralValence.NEGATIVE else 0.8
        else:
            return 0.5
    
    def _evaluate_utilitarian_compatibility(self, event: MoralEvent) -> float:
        """评估功利主义兼容性"""
        utilitarian_positive_events = [
            MoralEventType.COOPERATION, MoralEventType.ALTRUISTIC_ACT,
            MoralEventType.SACRIFICE
        ]
        
        if event.event_type in utilitarian_positive_events:
            return 0.8 if event.valence == MoralValence.POSITIVE else 0.3
        elif event.event_type == MoralEventType.SELFISH_ACT:
            # 功利主义可能容忍一些自私行为，如果整体结果是好的
            return 0.6 if event.valence == MoralValence.POSITIVE else 0.2
        else:
            return 0.5
    
    def _evaluate_virtue_compatibility(self, event: MoralEvent) -> float:
        """评估美德伦理学兼容性"""
        virtue_positive_events = [
            MoralEventType.SACRIFICE, MoralEventType.FORGIVENESS,
            MoralEventType.JUSTICE_ACTION, MoralEventType.ALTRUISTIC_ACT
        ]
        
        if event.event_type in virtue_positive_events:
            return 0.8 if event.valence == MoralValence.POSITIVE else 0.3
        else:
            return 0.5
    
    def _calculate_emotional_compatibility(self, moral_state: MoralState, event: MoralEvent) -> float:
        """计算情感兼容性"""
        compatibility = 0.5
        
        # 共情水平影响
        if event.affects_others and moral_state.empathy_level > 0.7:
            if event.valence == MoralValence.POSITIVE:
                compatibility += 0.2
            elif event.valence == MoralValence.NEGATIVE:
                compatibility -= 0.2
        
        # 愧疚敏感度影响
        if event.valence == MoralValence.NEGATIVE and moral_state.guilt_sensitivity > 0.7:
            compatibility -= 0.1
        
        # 道德勇气影响
        if event.event_type in [MoralEventType.JUSTICE_ACTION, MoralEventType.SACRIFICE]:
            if moral_state.moral_courage > 0.6:
                compatibility += 0.15
            else:
                compatibility -= 0.1
        
        return max(0.0, min(1.0, compatibility))
    
    def _calculate_receptivity(self, npc_id: str, event: MoralEvent) -> float:
        """计算NPC对事件的接受性"""
        if npc_id not in self.npc_moral_states:
            return 0.5
        
        moral_state = self.npc_moral_states[npc_id]
        
        # 基础接受性
        base_receptivity = moral_state.moral_plasticity
        
        # 社会压力抵抗调节
        if event.visibility > 0.7:  # 高可见度事件
            social_factor = 1.0 - moral_state.social_pressure_resistance
            base_receptivity *= (1.0 + social_factor * 0.5)
        
        # 情境敏感度调节
        context_factor = moral_state.context_sensitivity
        base_receptivity *= (0.5 + context_factor * 0.5)
        
        # 当前道德压力调节
        moral_stress = moral_state.calculate_moral_stress()
        if moral_stress > 0.5:
            # 高道德压力下更容易受影响
            base_receptivity *= (1.0 + moral_stress * 0.3)
        
        return max(0.1, min(1.0, base_receptivity))
    
    def cleanup_expired_influences(self, current_time: float = None):
        """清理过期的影响"""
        if current_time is None:
            current_time = time.time()
        
        for npc_id in self.active_influences:
            self.active_influences[npc_id] = [
                influence for influence in self.active_influences[npc_id]
                if not influence.is_expired(current_time)
            ]
    
    def get_influence_summary(self, npc_id: str) -> Dict[str, Any]:
        """获取NPC的影响摘要"""
        if npc_id not in self.active_influences:
            return {}
        
        influences = self.active_influences[npc_id]
        
        # 按事件类型分组
        by_event_type = defaultdict(list)
        for influence in influences:
            by_event_type[influence.source_event.event_type].append(influence)
        
        # 计算总影响强度
        total_strength = sum(inf.get_current_strength() for inf in influences)
        
        return {
            'total_active_influences': len(influences),
            'total_influence_strength': total_strength,
            'influences_by_type': {
                event_type.value: len(inf_list) 
                for event_type, inf_list in by_event_type.items()
            },
            'most_recent_influence': max(influences, key=lambda x: x.timestamp).source_event.event_id if influences else None
        }
    
    def _update_propagation_stats(self, event: MoralEvent, propagation_result: Dict[str, Any]):
        """更新传播统计"""
        total_transmissions = propagation_result['total_transmissions']
        
        if total_transmissions > 0:
            # 更新平均传播距离
            current_avg = self.contagion_stats['average_propagation_distance']
            total_events = self.contagion_stats['total_events']
            
            new_avg = ((current_avg * (total_events - 1)) + propagation_result['max_depth']) / total_events
            self.contagion_stats['average_propagation_distance'] = new_avg
            
            # 更新最有影响力的事件
            if (self.contagion_stats['most_influential_event'] is None or 
                total_transmissions > self.contagion_stats.get('max_transmissions', 0)):
                
                self.contagion_stats['most_influential_event'] = event.event_id
                self.contagion_stats['max_transmissions'] = total_transmissions
    
    def get_network_moral_climate(self) -> Dict[str, Any]:
        """获取网络道德气候"""
        if not self.npc_moral_states:
            return {}
        
        # 计算道德框架分布
        framework_distribution = defaultdict(int)
        empathy_levels = []
        moral_courage_levels = []
        
        for moral_state in self.npc_moral_states.values():
            dominant = moral_state.get_dominant_moral_framework()
            framework_distribution[dominant] += 1
            empathy_levels.append(moral_state.empathy_level)
            moral_courage_levels.append(moral_state.moral_courage)
        
        # 计算最近事件的道德倾向
        recent_events = self.event_history[-50:]  # 最近50个事件
        positive_events = sum(1 for event in recent_events if event.valence == MoralValence.POSITIVE)
        negative_events = sum(1 for event in recent_events if event.valence == MoralValence.NEGATIVE)
        
        return {
            'total_npcs': len(self.npc_moral_states),
            'framework_distribution': dict(framework_distribution),
            'average_empathy': np.mean(empathy_levels) if empathy_levels else 0.0,
            'average_moral_courage': np.mean(moral_courage_levels) if moral_courage_levels else 0.0,
            'recent_moral_trend': {
                'positive_events': positive_events,
                'negative_events': negative_events,
                'moral_balance': (positive_events - negative_events) / max(len(recent_events), 1)
            },
            'contagion_stats': self.contagion_stats.copy()
        }