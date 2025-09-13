"""
道德基因组 - NEAT算法的基因组实现，专门用于道德决策
"""

import random
import uuid
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class ConnectionGene:
    """连接基因"""
    innovation_id: int
    input_node: int
    output_node: int
    weight: float
    enabled: bool = True
    
    def copy(self) -> 'ConnectionGene':
        return ConnectionGene(
            innovation_id=self.innovation_id,
            input_node=self.input_node,
            output_node=self.output_node,
            weight=self.weight,
            enabled=self.enabled
        )


@dataclass 
class NodeGene:
    """节点基因"""
    node_id: int
    node_type: str  # 'input', 'hidden', 'output'
    activation_function: str = 'sigmoid'
    bias: float = 0.0
    
    def copy(self) -> 'NodeGene':
        return NodeGene(
            node_id=self.node_id,
            node_type=self.node_type,
            activation_function=self.activation_function,
            bias=self.bias
        )


class MoralGenome:
    """道德决策的神经网络基因组"""
    
    def __init__(self, genome_id: str = None):
        self.genome_id = genome_id or str(uuid.uuid4())
        
        # 基因组成
        self.connection_genes: Dict[int, ConnectionGene] = {}
        self.node_genes: Dict[int, NodeGene] = {}
        
        # 道德相关参数
        self.moral_parameters = {
            'kantian_weight': random.uniform(0.1, 0.9),
            'utilitarian_weight': random.uniform(0.1, 0.9),
            'virtue_weight': random.uniform(0.1, 0.9),
            'empathy_sensitivity': random.uniform(0.0, 1.0),
            'risk_aversion': random.uniform(0.0, 1.0),
            'social_conformity': random.uniform(0.0, 1.0)
        }
        
        # 标准化权重
        self._normalize_moral_weights()
        
        # 适应度相关
        self.fitness = 0.0
        self.adjusted_fitness = 0.0
        self.species_id = None
        
        # 网络结构参数
        self.input_size = 12   # 情境输入维度
        self.output_size = 4   # 行为决策输出
        
        # 创新追踪
        self.innovation_tracker = InnovationTracker()
        
        # 初始化基本网络结构
        self._initialize_minimal_network()
    
    def _normalize_moral_weights(self):
        """标准化道德权重"""
        total = (self.moral_parameters['kantian_weight'] + 
                self.moral_parameters['utilitarian_weight'] + 
                self.moral_parameters['virtue_weight'])
        
        if total > 0:
            self.moral_parameters['kantian_weight'] /= total
            self.moral_parameters['utilitarian_weight'] /= total
            self.moral_parameters['virtue_weight'] /= total
    
    def _initialize_minimal_network(self):
        """初始化最小网络结构"""
        # 输入节点
        for i in range(self.input_size):
            self.node_genes[i] = NodeGene(
                node_id=i,
                node_type='input'
            )
        
        # 输出节点
        for i in range(self.output_size):
            output_id = self.input_size + i
            self.node_genes[output_id] = NodeGene(
                node_id=output_id,
                node_type='output',
                activation_function='tanh'
            )
        
        # 创建初始连接 (输入直接连接到输出)
        connection_id = 0
        for input_id in range(self.input_size):
            for output_id in range(self.input_size, self.input_size + self.output_size):
                if random.random() < 0.3:  # 30%概率创建初始连接
                    self.connection_genes[connection_id] = ConnectionGene(
                        innovation_id=connection_id,
                        input_node=input_id,
                        output_node=output_id,
                        weight=random.uniform(-1.0, 1.0)
                    )
                    connection_id += 1
    
    def add_node_mutation(self) -> bool:
        """添加节点变异"""
        if not self.connection_genes:
            return False
        
        # 随机选择一个启用的连接
        enabled_connections = [conn for conn in self.connection_genes.values() if conn.enabled]
        if not enabled_connections:
            return False
        
        old_connection = random.choice(enabled_connections)
        
        # 禁用旧连接
        old_connection.enabled = False
        
        # 创建新节点
        new_node_id = max(self.node_genes.keys()) + 1
        self.node_genes[new_node_id] = NodeGene(
            node_id=new_node_id,
            node_type='hidden',
            activation_function='sigmoid'
        )
        
        # 创建两个新连接
        innovation_id1 = self.innovation_tracker.get_innovation_id(
            old_connection.input_node, new_node_id
        )
        innovation_id2 = self.innovation_tracker.get_innovation_id(
            new_node_id, old_connection.output_node
        )
        
        # 输入到新节点的连接 (权重为1)
        self.connection_genes[innovation_id1] = ConnectionGene(
            innovation_id=innovation_id1,
            input_node=old_connection.input_node,
            output_node=new_node_id,
            weight=1.0
        )
        
        # 新节点到输出的连接 (保持原权重)
        self.connection_genes[innovation_id2] = ConnectionGene(
            innovation_id=innovation_id2,
            input_node=new_node_id,
            output_node=old_connection.output_node,
            weight=old_connection.weight
        )
        
        return True
    
    def add_connection_mutation(self) -> bool:
        """添加连接变异"""
        # 获取所有可能的连接
        possible_connections = []
        
        for input_node in self.node_genes:
            for output_node in self.node_genes:
                # 检查连接合法性
                if (self._can_connect(input_node, output_node) and 
                    not self._connection_exists(input_node, output_node)):
                    possible_connections.append((input_node, output_node))
        
        if not possible_connections:
            return False
        
        # 随机选择一个连接
        input_node, output_node = random.choice(possible_connections)
        
        # 创建新连接
        innovation_id = self.innovation_tracker.get_innovation_id(input_node, output_node)
        
        self.connection_genes[innovation_id] = ConnectionGene(
            innovation_id=innovation_id,
            input_node=input_node,
            output_node=output_node,
            weight=random.uniform(-1.0, 1.0)
        )
        
        return True
    
    def weight_mutation(self, mutation_rate: float = 0.8, perturbation_rate: float = 0.9):
        """权重变异"""
        for connection in self.connection_genes.values():
            if random.random() < mutation_rate:
                if random.random() < perturbation_rate:
                    # 微调权重
                    connection.weight += random.uniform(-0.1, 0.1)
                    connection.weight = max(-5.0, min(5.0, connection.weight))
                else:
                    # 完全随机化权重
                    connection.weight = random.uniform(-1.0, 1.0)
    
    def moral_parameter_mutation(self, mutation_rate: float = 0.1):
        """道德参数变异"""
        for param_name, param_value in self.moral_parameters.items():
            if random.random() < mutation_rate:
                if 'weight' in param_name:
                    # 权重参数需要重新标准化
                    self.moral_parameters[param_name] += random.uniform(-0.1, 0.1)
                    self.moral_parameters[param_name] = max(0.01, min(0.99, self.moral_parameters[param_name]))
                else:
                    # 其他参数直接调整
                    self.moral_parameters[param_name] += random.uniform(-0.05, 0.05)
                    self.moral_parameters[param_name] = max(0.0, min(1.0, self.moral_parameters[param_name]))
        
        self._normalize_moral_weights()
    
    def crossover(self, other: 'MoralGenome') -> 'MoralGenome':
        """基因组交叉"""
        child = MoralGenome()
        
        # 确定更适应的父代
        if self.fitness > other.fitness:
            dominant_parent = self
            recessive_parent = other
        else:
            dominant_parent = other
            recessive_parent = self
        
        # 继承所有主导父代的节点
        for node_id, node in dominant_parent.node_genes.items():
            child.node_genes[node_id] = node.copy()
        
        # 处理连接基因
        all_innovations = set(self.connection_genes.keys()) | set(other.connection_genes.keys())
        
        for innovation_id in all_innovations:
            conn1 = self.connection_genes.get(innovation_id)
            conn2 = other.connection_genes.get(innovation_id)
            
            if conn1 and conn2:
                # 匹配基因，随机选择
                chosen_conn = random.choice([conn1, conn2])
                child.connection_genes[innovation_id] = chosen_conn.copy()
                
                # 如果父母任一方禁用，有75%概率禁用
                if not conn1.enabled or not conn2.enabled:
                    if random.random() < 0.75:
                        child.connection_genes[innovation_id].enabled = False
                        
            elif conn1 and dominant_parent == self:
                # 不匹配基因，来自主导父代
                child.connection_genes[innovation_id] = conn1.copy()
            elif conn2 and dominant_parent == other:
                child.connection_genes[innovation_id] = conn2.copy()
        
        # 交叉道德参数
        for param_name in child.moral_parameters:
            if random.random() < 0.5:
                child.moral_parameters[param_name] = self.moral_parameters[param_name]
            else:
                child.moral_parameters[param_name] = other.moral_parameters[param_name]
        
        child._normalize_moral_weights()
        return child
    
    def _can_connect(self, input_node: int, output_node: int) -> bool:
        """检查两个节点是否可以连接"""
        input_type = self.node_genes[input_node].node_type
        output_type = self.node_genes[output_node].node_type
        
        # 不能自连接
        if input_node == output_node:
            return False
        
        # 输出节点不能作为输入
        if input_type == 'output':
            return False
        
        # 输入节点不能作为输出
        if output_type == 'input':
            return False
        
        # 检查是否会形成循环 (简化版本)
        return True
    
    def _connection_exists(self, input_node: int, output_node: int) -> bool:
        """检查连接是否已存在"""
        for connection in self.connection_genes.values():
            if (connection.input_node == input_node and 
                connection.output_node == output_node):
                return True
        return False
    
    def calculate_compatibility(self, other: 'MoralGenome') -> float:
        """计算与另一个基因组的兼容性距离"""
        # 获取创新编号集合
        innovations1 = set(self.connection_genes.keys())
        innovations2 = set(other.connection_genes.keys())
        
        # 计算不匹配和多余基因
        matching = innovations1 & innovations2
        disjoint1 = innovations1 - innovations2
        disjoint2 = innovations2 - innovations1
        
        # 计算权重差异
        weight_differences = []
        for innovation_id in matching:
            w1 = self.connection_genes[innovation_id].weight
            w2 = other.connection_genes[innovation_id].weight
            weight_differences.append(abs(w1 - w2))
        
        avg_weight_diff = np.mean(weight_differences) if weight_differences else 0
        
        # 基因组大小
        max_genes = max(len(innovations1), len(innovations2))
        if max_genes == 0:
            max_genes = 1
        
        # 兼容性参数
        c1, c2, c3 = 1.0, 1.0, 0.4
        
        # 计算兼容性距离
        compatibility = (
            c1 * len(disjoint1 | disjoint2) / max_genes +
            c2 * len(disjoint1 | disjoint2) / max_genes +
            c3 * avg_weight_diff
        )
        
        # 添加道德参数的兼容性
        moral_distance = self._calculate_moral_parameter_distance(other)
        compatibility += 0.2 * moral_distance
        
        return compatibility
    
    def _calculate_moral_parameter_distance(self, other: 'MoralGenome') -> float:
        """计算道德参数的距离"""
        total_distance = 0.0
        
        for param_name in self.moral_parameters:
            diff = abs(self.moral_parameters[param_name] - other.moral_parameters[param_name])
            total_distance += diff
        
        return total_distance / len(self.moral_parameters)
    
    def copy(self) -> 'MoralGenome':
        """创建基因组的深拷贝"""
        new_genome = MoralGenome(genome_id=str(uuid.uuid4()))
        
        # 复制节点
        for node_id, node in self.node_genes.items():
            new_genome.node_genes[node_id] = node.copy()
        
        # 复制连接
        for conn_id, connection in self.connection_genes.items():
            new_genome.connection_genes[conn_id] = connection.copy()
        
        # 复制道德参数
        new_genome.moral_parameters = self.moral_parameters.copy()
        
        # 复制其他属性
        new_genome.fitness = self.fitness
        new_genome.adjusted_fitness = self.adjusted_fitness
        new_genome.species_id = self.species_id
        
        return new_genome


class InnovationTracker:
    """创新编号追踪器"""
    
    def __init__(self):
        self.innovation_counter = 0
        self.innovation_history: Dict[Tuple[int, int], int] = {}
    
    def get_innovation_id(self, input_node: int, output_node: int) -> int:
        """获取连接的创新编号"""
        connection_key = (input_node, output_node)
        
        if connection_key in self.innovation_history:
            return self.innovation_history[connection_key]
        else:
            self.innovation_counter += 1
            self.innovation_history[connection_key] = self.innovation_counter
            return self.innovation_counter