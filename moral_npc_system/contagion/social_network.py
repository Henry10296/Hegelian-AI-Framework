"""
社交网络结构 - 管理NPC之间的社交关系
"""

import random
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass
from collections import defaultdict
import networkx as nx


@dataclass
class Relationship:
    """关系类"""
    source_id: str
    target_id: str
    relationship_type: str      # 'friendship', 'family', 'colleague', 'rival', etc.
    strength: float = 0.5       # 关系强度 [0-1]
    trust_level: float = 0.5    # 信任程度 [0-1]
    influence_weight: float = 0.5  # 影响权重 [0-1]
    
    # 关系特征
    reciprocal: bool = True     # 是否双向关系
    stable: bool = True         # 关系是否稳定
    
    # 时间信息
    created_time: float = 0.0
    last_interaction: float = 0.0
    interaction_frequency: float = 0.1  # 交互频率
    
    def calculate_influence_factor(self) -> float:
        """计算影响因子"""
        # 基于关系强度、信任和影响权重
        base_influence = (self.strength + self.trust_level + self.influence_weight) / 3.0
        
        # 关系类型修正
        type_modifiers = {
            'family': 1.2,        # 家庭关系影响更强
            'friendship': 1.0,    # 友谊关系标准影响
            'colleague': 0.8,     # 同事关系影响较弱
            'authority': 1.1,     # 权威关系有额外影响
            'rival': -0.3,        # 敌对关系负影响
            'romantic': 1.3,      # 恋爱关系影响很强
            'mentor': 1.1,        # 师生关系正向影响
            'stranger': 0.2       # 陌生人关系影响微弱
        }
        
        modifier = type_modifiers.get(self.relationship_type, 1.0)
        return base_influence * modifier
    
    def update_from_interaction(self, interaction_outcome: float):
        """根据交互结果更新关系"""
        # 正面交互增强关系，负面交互削弱关系
        strength_change = interaction_outcome * 0.1
        trust_change = interaction_outcome * 0.05
        
        self.strength = max(0.0, min(1.0, self.strength + strength_change))
        self.trust_level = max(0.0, min(1.0, self.trust_level + trust_change))
        
        # 更新时间
        import time
        self.last_interaction = time.time()


class SocialNetwork:
    """社交网络管理器"""
    
    def __init__(self):
        # 使用NetworkX图结构
        self.graph = nx.DiGraph()  # 有向图支持非对称关系
        
        # 关系映射
        self.relationships: Dict[Tuple[str, str], Relationship] = {}
        
        # 群体结构
        self.groups: Dict[str, Set[str]] = {}
        self.group_hierarchies: Dict[str, Dict[str, float]] = {}
        
        # 网络统计
        self.network_stats = {
            'density': 0.0,
            'clustering_coefficient': 0.0,
            'average_path_length': 0.0
        }
    
    def add_npc(self, npc_id: str, attributes: Dict[str, Any] = None):
        """添加NPC到网络"""
        if attributes is None:
            attributes = {}
        
        self.graph.add_node(npc_id, **attributes)
    
    def add_relationship(self, source_id: str, target_id: str, 
                        relationship_type: str, **kwargs) -> Relationship:
        """添加关系"""
        # 确保节点存在
        if source_id not in self.graph:
            self.add_npc(source_id)
        if target_id not in self.graph:
            self.add_npc(target_id)
        
        # 创建关系对象
        relationship = Relationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            **kwargs
        )
        
        # 存储关系
        rel_key = (source_id, target_id)
        self.relationships[rel_key] = relationship
        
        # 添加到图中
        self.graph.add_edge(source_id, target_id, 
                           weight=relationship.influence_weight,
                           relationship=relationship)
        
        # 如果是双向关系，添加反向边
        if relationship.reciprocal and source_id != target_id:
            reverse_rel = Relationship(
                source_id=target_id,
                target_id=source_id,
                relationship_type=relationship_type,
                strength=relationship.strength,
                trust_level=relationship.trust_level,
                influence_weight=relationship.influence_weight,
                reciprocal=True
            )
            
            reverse_key = (target_id, source_id)
            self.relationships[reverse_key] = reverse_rel
            
            self.graph.add_edge(target_id, source_id,
                               weight=reverse_rel.influence_weight,
                               relationship=reverse_rel)
        
        return relationship
    
    def get_neighbors(self, npc_id: str, relationship_types: List[str] = None) -> List[str]:
        """获取邻居节点"""
        if npc_id not in self.graph:
            return []
        
        neighbors = []
        for neighbor in self.graph.neighbors(npc_id):
            if relationship_types is None:
                neighbors.append(neighbor)
            else:
                rel_key = (npc_id, neighbor)
                if (rel_key in self.relationships and 
                    self.relationships[rel_key].relationship_type in relationship_types):
                    neighbors.append(neighbor)
        
        return neighbors
    
    def get_relationship(self, source_id: str, target_id: str) -> Optional[Relationship]:
        """获取关系"""
        rel_key = (source_id, target_id)
        return self.relationships.get(rel_key)
    
    def calculate_influence_path(self, source_id: str, target_id: str, 
                               max_depth: int = 3) -> List[Tuple[str, float]]:
        """计算影响路径"""
        if source_id not in self.graph or target_id not in self.graph:
            return []
        
        try:
            # 使用最短路径算法
            path = nx.shortest_path(self.graph, source_id, target_id)
            
            if len(path) > max_depth + 1:  # +1因为路径包括起点
                return []
            
            # 计算路径上的影响衰减
            influence_path = []
            current_influence = 1.0
            
            for i in range(len(path) - 1):
                current_node = path[i]
                next_node = path[i + 1]
                
                rel_key = (current_node, next_node)
                if rel_key in self.relationships:
                    relationship = self.relationships[rel_key]
                    influence_factor = relationship.calculate_influence_factor()
                    current_influence *= abs(influence_factor)
                    
                    influence_path.append((next_node, current_influence))
                else:
                    # 没有直接关系，影响力大幅衰减
                    current_influence *= 0.1
                    influence_path.append((next_node, current_influence))
            
            return influence_path
            
        except nx.NetworkXNoPath:
            return []
    
    def find_influencers(self, target_id: str, influence_threshold: float = 0.3) -> List[Tuple[str, float]]:
        """找到对目标有影响力的NPC"""
        influencers = []
        
        for npc_id in self.graph.nodes():
            if npc_id == target_id:
                continue
            
            influence_path = self.calculate_influence_path(npc_id, target_id)
            if influence_path:
                final_influence = influence_path[-1][1]
                if final_influence >= influence_threshold:
                    influencers.append((npc_id, final_influence))
        
        # 按影响力排序
        influencers.sort(key=lambda x: x[1], reverse=True)
        return influencers
    
    def create_group(self, group_id: str, members: List[str], 
                    hierarchy: Dict[str, float] = None):
        """创建群体"""
        self.groups[group_id] = set(members)
        
        if hierarchy:
            self.group_hierarchies[group_id] = hierarchy
        else:
            # 默认平等层级
            self.group_hierarchies[group_id] = {member: 0.5 for member in members}
        
        # 在群体成员间添加关系
        for i, member1 in enumerate(members):
            for member2 in members[i+1:]:
                if not self.get_relationship(member1, member2):
                    self.add_relationship(member1, member2, 'group_member',
                                        strength=0.4, trust_level=0.4)
    
    def get_group_members(self, group_id: str) -> Set[str]:
        """获取群体成员"""
        return self.groups.get(group_id, set())
    
    def get_npc_groups(self, npc_id: str) -> List[str]:
        """获取NPC所属的群体"""
        groups = []
        for group_id, members in self.groups.items():
            if npc_id in members:
                groups.append(group_id)
        return groups
    
    def calculate_social_distance(self, npc1_id: str, npc2_id: str) -> float:
        """计算社交距离"""
        if npc1_id == npc2_id:
            return 0.0
        
        try:
            path_length = nx.shortest_path_length(self.graph, npc1_id, npc2_id)
            return float(path_length)
        except nx.NetworkXNoPath:
            return float('inf')
    
    def get_network_clusters(self) -> List[Set[str]]:
        """获取网络聚类"""
        # 转换为无向图进行聚类分析
        undirected_graph = self.graph.to_undirected()
        
        # 使用连通分量作为基本聚类
        clusters = list(nx.connected_components(undirected_graph))
        
        return clusters
    
    def calculate_centrality_measures(self) -> Dict[str, Dict[str, float]]:
        """计算中心性指标"""
        centrality_measures = {}
        
        # 度中心性
        degree_centrality = nx.degree_centrality(self.graph)
        
        # 介数中心性
        try:
            betweenness_centrality = nx.betweenness_centrality(self.graph)
        except:
            betweenness_centrality = {node: 0.0 for node in self.graph.nodes()}
        
        # 接近中心性
        try:
            closeness_centrality = nx.closeness_centrality(self.graph)
        except:
            closeness_centrality = {node: 0.0 for node in self.graph.nodes()}
        
        # 特征向量中心性
        try:
            eigenvector_centrality = nx.eigenvector_centrality(self.graph, max_iter=1000)
        except:
            eigenvector_centrality = {node: 0.0 for node in self.graph.nodes()}
        
        for node in self.graph.nodes():
            centrality_measures[node] = {
                'degree': degree_centrality.get(node, 0.0),
                'betweenness': betweenness_centrality.get(node, 0.0),
                'closeness': closeness_centrality.get(node, 0.0),
                'eigenvector': eigenvector_centrality.get(node, 0.0)
            }
        
        return centrality_measures
    
    def update_network_stats(self):
        """更新网络统计信息"""
        if len(self.graph.nodes()) < 2:
            return
        
        # 网络密度
        self.network_stats['density'] = nx.density(self.graph)
        
        # 聚类系数
        try:
            self.network_stats['clustering_coefficient'] = nx.average_clustering(
                self.graph.to_undirected()
            )
        except:
            self.network_stats['clustering_coefficient'] = 0.0
        
        # 平均路径长度
        try:
            undirected = self.graph.to_undirected()
            if nx.is_connected(undirected):
                self.network_stats['average_path_length'] = nx.average_shortest_path_length(undirected)
            else:
                # 对于不连通的图，计算最大连通分量的平均路径长度
                largest_cc = max(nx.connected_components(undirected), key=len)
                subgraph = undirected.subgraph(largest_cc)
                self.network_stats['average_path_length'] = nx.average_shortest_path_length(subgraph)
        except:
            self.network_stats['average_path_length'] = 0.0
    
    def simulate_relationship_evolution(self, time_step: float = 1.0):
        """模拟关系演化"""
        for relationship in self.relationships.values():
            # 关系自然衰减或增强
            if relationship.stable:
                # 稳定关系缓慢向中性值靠拢
                target_strength = 0.5
                change_rate = 0.01 * time_step
                
                if relationship.strength > target_strength:
                    relationship.strength -= change_rate
                elif relationship.strength < target_strength:
                    relationship.strength += change_rate
                
                relationship.strength = max(0.0, min(1.0, relationship.strength))
            else:
                # 不稳定关系随机波动
                change = random.uniform(-0.05, 0.05) * time_step
                relationship.strength = max(0.0, min(1.0, relationship.strength + change))
    
    def export_network_data(self) -> Dict[str, Any]:
        """导出网络数据"""
        return {
            'nodes': list(self.graph.nodes(data=True)),
            'edges': list(self.graph.edges(data=True)),
            'relationships': {
                f"{k[0]}->{k[1]}": {
                    'type': v.relationship_type,
                    'strength': v.strength,
                    'trust': v.trust_level,
                    'influence': v.influence_weight
                } for k, v in self.relationships.items()
            },
            'groups': {k: list(v) for k, v in self.groups.items()},
            'stats': self.network_stats
        }
    
    def get_network_summary(self) -> Dict[str, Any]:
        """获取网络摘要"""
        self.update_network_stats()
        centralities = self.calculate_centrality_measures()
        
        # 找出最有影响力的节点
        most_influential = max(centralities.items(), 
                             key=lambda x: x[1]['eigenvector']) if centralities else (None, None)
        
        return {
            'total_npcs': len(self.graph.nodes()),
            'total_relationships': len(self.relationships),
            'total_groups': len(self.groups),
            'network_density': self.network_stats['density'],
            'clustering_coefficient': self.network_stats['clustering_coefficient'],
            'average_path_length': self.network_stats['average_path_length'],
            'most_influential_npc': most_influential[0] if most_influential[0] else None,
            'influence_score': most_influential[1]['eigenvector'] if most_influential[1] else 0.0
        }