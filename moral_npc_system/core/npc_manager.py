"""
NPC管理器 - 管理多个道德感知NPC的系统
"""

import time
import random
from typing import Dict, List, Set, Any, Optional, Tuple
from collections import defaultdict

from .moral_npc import MoralNPC
from .moral_state import MoralState
from ..neuroevolution.moral_genome import MoralGenome
from ..contagion.social_network import SocialNetwork
from ..contagion.moral_contagion_network import MoralContagionNetwork


class NPCManager:
    """NPC系统管理器"""
    
    def __init__(self):
        # NPC实例管理
        self.npcs: Dict[str, MoralNPC] = {}
        
        # 社交网络和传染系统
        self.social_network = SocialNetwork()
        self.contagion_network = MoralContagionNetwork(self.social_network)
        
        # 系统状态
        self.active = True
        self.last_update_time = time.time()
        
        # 管理参数
        self.max_npcs = 1000
        self.update_interval = 1.0  # 秒
        
        # 统计信息
        self.stats = {
            'total_npcs_created': 0,
            'total_decisions_made': 0,
            'total_interactions': 0,
            'moral_events_processed': 0
        }
        
        # 预设的道德偏向模板
        self.moral_templates = {
            'kantian': MoralState(
                kantian_weight=0.7, utilitarian_weight=0.2, virtue_weight=0.1,
                empathy_level=0.8, moral_courage=0.7, guilt_sensitivity=0.8
            ),
            'utilitarian': MoralState(
                kantian_weight=0.2, utilitarian_weight=0.7, virtue_weight=0.1,
                empathy_level=0.6, moral_courage=0.5, guilt_sensitivity=0.5
            ),
            'virtue_ethics': MoralState(
                kantian_weight=0.2, utilitarian_weight=0.2, virtue_weight=0.6,
                empathy_level=0.7, moral_courage=0.8, guilt_sensitivity=0.6
            ),
            'balanced': MoralState(
                kantian_weight=0.33, utilitarian_weight=0.33, virtue_weight=0.34,
                empathy_level=0.6, moral_courage=0.6, guilt_sensitivity=0.6
            ),
            'pragmatic': MoralState(
                kantian_weight=0.3, utilitarian_weight=0.5, virtue_weight=0.2,
                empathy_level=0.5, moral_courage=0.4, guilt_sensitivity=0.4
            ),
            'idealistic': MoralState(
                kantian_weight=0.5, utilitarian_weight=0.2, virtue_weight=0.3,
                empathy_level=0.8, moral_courage=0.9, guilt_sensitivity=0.7
            )
        }
    
    def create_npc(self, npc_id: str, moral_bias: str = 'balanced', 
                   custom_moral_state: MoralState = None,
                   custom_genome: MoralGenome = None,
                   npc_attributes: Dict[str, Any] = None) -> MoralNPC:
        """创建新的道德感知NPC"""
        
        if len(self.npcs) >= self.max_npcs:
            raise ValueError(f"已达到最大NPC数量限制: {self.max_npcs}")
        
        if npc_id in self.npcs:
            raise ValueError(f"NPC ID '{npc_id}' 已存在")
        
        # 确定道德状态
        if custom_moral_state:
            moral_state = custom_moral_state
        elif moral_bias in self.moral_templates:
            # 使用模板并添加少量随机变化
            template = self.moral_templates[moral_bias]
            moral_state = self._add_personality_variation(template.copy())
        else:
            # 默认平衡型
            moral_state = self.moral_templates['balanced'].copy()
        
        # 创建NPC
        npc = MoralNPC(
            npc_id=npc_id,
            initial_moral_state=moral_state,
            neural_genome=custom_genome
        )
        
        # 添加自定义属性
        if npc_attributes:
            for key, value in npc_attributes.items():
                if hasattr(npc, key):
                    setattr(npc, key, value)
        
        # 注册到系统
        self.npcs[npc_id] = npc
        self.social_network.add_npc(npc_id, npc_attributes or {})
        self.contagion_network.add_npc(npc_id, moral_state)
        
        # 更新统计
        self.stats['total_npcs_created'] += 1
        
        return npc
    
    def _add_personality_variation(self, template_state: MoralState) -> MoralState:
        """为模板道德状态添加个性变化"""
        variation_range = 0.1
        
        # 随机调整道德权重
        template_state.kantian_weight += random.uniform(-variation_range, variation_range)
        template_state.utilitarian_weight += random.uniform(-variation_range, variation_range)
        template_state.virtue_weight += random.uniform(-variation_range, variation_range)
        
        # 重新标准化
        template_state._normalize_weights()
        
        # 调整情感参数
        template_state.empathy_level = max(0.1, min(0.9, 
            template_state.empathy_level + random.uniform(-variation_range, variation_range)))
        template_state.moral_courage = max(0.1, min(0.9,
            template_state.moral_courage + random.uniform(-variation_range, variation_range)))
        template_state.guilt_sensitivity = max(0.1, min(0.9,
            template_state.guilt_sensitivity + random.uniform(-variation_range, variation_range)))
        
        return template_state
    
    def remove_npc(self, npc_id: str) -> bool:
        """移除NPC"""
        if npc_id not in self.npcs:
            return False
        
        # 从各个系统中移除
        del self.npcs[npc_id]
        
        # 从社交网络中移除 (包括所有关系)
        if npc_id in self.social_network.graph:
            # 移除所有相关关系
            relationships_to_remove = [
                (source, target) for source, target in self.social_network.relationships.keys()
                if source == npc_id or target == npc_id
            ]
            
            for source, target in relationships_to_remove:
                if (source, target) in self.social_network.relationships:
                    del self.social_network.relationships[(source, target)]
            
            self.social_network.graph.remove_node(npc_id)
        
        # 从传染网络中移除
        if npc_id in self.contagion_network.npc_moral_states:
            del self.contagion_network.npc_moral_states[npc_id]
        if npc_id in self.contagion_network.active_influences:
            del self.contagion_network.active_influences[npc_id]
        
        return True
    
    def get_npc(self, npc_id: str) -> Optional[MoralNPC]:
        """获取指定NPC"""
        return self.npcs.get(npc_id)
    
    def list_npcs(self, filter_criteria: Dict[str, Any] = None) -> List[str]:
        """列出NPC (可选过滤)"""
        npc_ids = list(self.npcs.keys())
        
        if not filter_criteria:
            return npc_ids
        
        filtered_ids = []
        for npc_id in npc_ids:
            npc = self.npcs[npc_id]
            match = True
            
            # 道德框架过滤
            if 'moral_framework' in filter_criteria:
                expected_framework = filter_criteria['moral_framework']
                actual_framework = npc.moral_state.get_dominant_moral_framework()
                if actual_framework != expected_framework:
                    match = False
            
            # 情感特征过滤
            if 'min_empathy' in filter_criteria:
                if npc.moral_state.empathy_level < filter_criteria['min_empathy']:
                    match = False
            
            if 'min_courage' in filter_criteria:
                if npc.moral_state.moral_courage < filter_criteria['min_courage']:
                    match = False
            
            # 状态过滤
            if 'min_mood' in filter_criteria:
                if npc.current_mood < filter_criteria['min_mood']:
                    match = False
            
            if match:
                filtered_ids.append(npc_id)
        
        return filtered_ids
    
    def create_relationship(self, npc1_id: str, npc2_id: str, 
                          relationship_type: str, **relationship_params) -> bool:
        """创建NPC之间的关系"""
        if npc1_id not in self.npcs or npc2_id not in self.npcs:
            return False
        
        self.social_network.add_relationship(
            npc1_id, npc2_id, relationship_type, **relationship_params
        )
        
        return True
    
    def batch_decision_making(self, shared_situation: Dict[str, Any], 
                            npc_ids: List[str] = None) -> Dict[str, Dict[str, Any]]:
        """批量NPC决策"""
        if npc_ids is None:
            npc_ids = list(self.npcs.keys())
        
        decisions = {}
        
        for npc_id in npc_ids:
            if npc_id in self.npcs:
                npc = self.npcs[npc_id]
                
                # 为每个NPC定制情境
                personalized_situation = shared_situation.copy()
                personalized_situation['target_id'] = personalized_situation.get('target_id', 'unknown')
                
                decision = npc.make_moral_decision(personalized_situation)
                decisions[npc_id] = decision
                
                self.stats['total_decisions_made'] += 1
        
        return decisions
    
    def simulate_social_interaction(self, npc_ids: List[str], 
                                  interaction_context: Dict[str, Any]) -> Dict[str, Any]:
        """模拟NPC间社交互动"""
        if len(npc_ids) < 2:
            return {'error': 'Need at least 2 NPCs for interaction'}
        
        interaction_results = {}
        
        # 两两互动
        for i in range(len(npc_ids)):
            for j in range(i + 1, len(npc_ids)):
                npc1_id, npc2_id = npc_ids[i], npc_ids[j]
                
                if npc1_id in self.npcs and npc2_id in self.npcs:
                    npc1, npc2 = self.npcs[npc1_id], self.npcs[npc2_id]
                    
                    # NPC1对NPC2的反应
                    response1 = npc1.interact_with_player(npc2_id, interaction_context)
                    
                    # NPC2对NPC1的反应
                    response2 = npc2.interact_with_player(npc1_id, interaction_context)
                    
                    interaction_results[f"{npc1_id}->{npc2_id}"] = response1
                    interaction_results[f"{npc2_id}->{npc1_id}"] = response2
                    
                    self.stats['total_interactions'] += 2
        
        return interaction_results
    
    def introduce_moral_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """向系统引入道德事件"""
        from ..contagion.moral_event import MoralEvent, MoralEventType, MoralValence
        
        # 创建道德事件
        event = MoralEvent(
            event_id=event_data.get('event_id', f"event_{time.time()}"),
            event_type=MoralEventType(event_data['event_type']),
            valence=MoralValence(event_data['valence']),
            primary_actor=event_data['primary_actor'],
            target=event_data.get('target'),
            intensity=event_data.get('intensity', 0.7),
            visibility=event_data.get('visibility', 0.5),
            moral_weight=event_data.get('moral_weight', 0.6),
            context=event_data.get('context', {})
        )
        
        # 传播事件
        propagation_result = self.contagion_network.introduce_moral_event(event)
        
        self.stats['moral_events_processed'] += 1
        
        return propagation_result
    
    def get_network_analysis(self) -> Dict[str, Any]:
        """获取网络分析"""
        # 社交网络分析
        network_summary = self.social_network.get_network_summary()
        
        # 道德气候分析
        moral_climate = self.contagion_network.get_network_moral_climate()
        
        # NPC状态统计
        npc_stats = self._calculate_npc_statistics()
        
        return {
            'network_structure': network_summary,
            'moral_climate': moral_climate,
            'npc_statistics': npc_stats,
            'system_stats': self.stats
        }
    
    def _calculate_npc_statistics(self) -> Dict[str, Any]:
        """计算NPC统计信息"""
        if not self.npcs:
            return {}
        
        # 道德框架分布
        framework_distribution = defaultdict(int)
        empathy_levels = []
        moral_courage_levels = []
        mood_levels = []
        stress_levels = []
        
        for npc in self.npcs.values():
            framework = npc.moral_state.get_dominant_moral_framework()
            framework_distribution[framework] += 1
            
            empathy_levels.append(npc.moral_state.empathy_level)
            moral_courage_levels.append(npc.moral_state.moral_courage)
            mood_levels.append(npc.current_mood)
            stress_levels.append(npc.stress_level)
        
        return {
            'total_npcs': len(self.npcs),
            'framework_distribution': dict(framework_distribution),
            'average_empathy': sum(empathy_levels) / len(empathy_levels),
            'average_moral_courage': sum(moral_courage_levels) / len(moral_courage_levels),
            'average_mood': sum(mood_levels) / len(mood_levels),
            'average_stress': sum(stress_levels) / len(stress_levels),
            'most_active_npc': max(self.npcs.items(), 
                                 key=lambda x: x[1].decision_count)[0] if self.npcs else None
        }
    
    def run_system_update(self):
        """运行系统更新"""
        current_time = time.time()
        
        # 清理过期的道德影响
        self.contagion_network.cleanup_expired_influences(current_time)
        
        # 更新网络统计
        self.social_network.update_network_stats()
        
        # 模拟关系演化
        self.social_network.simulate_relationship_evolution(
            current_time - self.last_update_time
        )
        
        self.last_update_time = current_time
    
    def save_system_state(self, filepath: str):
        """保存系统状态"""
        import json
        
        system_state = {
            'timestamp': time.time(),
            'stats': self.stats,
            'npc_count': len(self.npcs),
            'npc_summaries': {
                npc_id: npc.get_current_status() 
                for npc_id, npc in self.npcs.items()
            },
            'network_analysis': self.get_network_analysis()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(system_state, f, indent=2, ensure_ascii=False)
    
    def create_npc_group(self, group_name: str, npc_count: int, 
                        moral_bias: str = 'balanced',
                        relationship_density: float = 0.3) -> List[str]:
        """创建NPC群体"""
        npc_ids = []
        
        # 创建NPC
        for i in range(npc_count):
            npc_id = f"{group_name}_{i:03d}"
            try:
                npc = self.create_npc(npc_id, moral_bias)
                npc_ids.append(npc_id)
            except ValueError:
                break  # 达到最大数量限制
        
        # 建立群体内关系
        for i in range(len(npc_ids)):
            for j in range(i + 1, len(npc_ids)):
                if random.random() < relationship_density:
                    relationship_types = ['colleague', 'acquaintance', 'friend']
                    rel_type = random.choice(relationship_types)
                    strength = random.uniform(0.3, 0.7)
                    
                    self.create_relationship(
                        npc_ids[i], npc_ids[j], rel_type,
                        strength=strength, trust_level=strength * 0.8
                    )
        
        # 创建群体
        self.social_network.create_group(group_name, npc_ids)
        
        return npc_ids
    
    def get_system_health(self) -> Dict[str, Any]:
        """获取系统健康状态"""
        return {
            'active': self.active,
            'npc_count': len(self.npcs),
            'max_capacity_usage': len(self.npcs) / self.max_npcs,
            'relationship_count': len(self.social_network.relationships),
            'active_influences': sum(len(influences) for influences 
                                   in self.contagion_network.active_influences.values()),
            'last_update': self.last_update_time,
            'uptime': time.time() - self.last_update_time if hasattr(self, 'start_time') else 0
        }
    
    def shutdown(self):
        """关闭系统"""
        self.active = False
        
        # 清理资源
        self.npcs.clear()
        self.social_network = SocialNetwork()
        self.contagion_network = MoralContagionNetwork(self.social_network)