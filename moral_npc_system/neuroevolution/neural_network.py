"""
道德神经网络 - 从基因组构建和执行神经网络
"""

import numpy as np
from typing import Dict, List, Set, Tuple, Any
from .moral_genome import MoralGenome, NodeGene, ConnectionGene


class MoralNeuralNetwork:
    """基于基因组的道德决策神经网络"""
    
    def __init__(self, genome: MoralGenome):
        self.genome = genome
        self.nodes: Dict[int, float] = {}
        self.node_order: List[int] = []
        
        # 激活函数映射
        self.activation_functions = {
            'sigmoid': self._sigmoid,
            'tanh': np.tanh,
            'relu': self._relu,
            'linear': lambda x: x
        }
        
        # 构建网络拓扑
        self._build_network_topology()
    
    def _build_network_topology(self):
        """构建网络拓扑结构"""
        # 初始化所有节点
        for node_id in self.genome.node_genes:
            self.nodes[node_id] = 0.0
        
        # 确定节点执行顺序 (拓扑排序)
        self.node_order = self._topological_sort()
    
    def _topological_sort(self) -> List[int]:
        """拓扑排序确定节点计算顺序"""
        # 简化版本：输入 -> 隐藏 -> 输出
        input_nodes = [node_id for node_id, node in self.genome.node_genes.items() 
                      if node.node_type == 'input']
        
        hidden_nodes = [node_id for node_id, node in self.genome.node_genes.items() 
                       if node.node_type == 'hidden']
        
        output_nodes = [node_id for node_id, node in self.genome.node_genes.items() 
                       if node.node_type == 'output']
        
        # 对隐藏节点进行更精确的排序 (基于连接关系)
        sorted_hidden = self._sort_hidden_nodes(hidden_nodes)
        
        return input_nodes + sorted_hidden + output_nodes
    
    def _sort_hidden_nodes(self, hidden_nodes: List[int]) -> List[int]:
        """对隐藏节点进行排序"""
        if not hidden_nodes:
            return []
        
        # 简化版本：基于节点ID排序
        # 实际应用中应该基于连接依赖关系
        return sorted(hidden_nodes)
    
    def activate(self, inputs: List[float]) -> List[float]:
        """激活网络进行前向传播"""
        if len(inputs) != self.genome.input_size:
            raise ValueError(f"Expected {self.genome.input_size} inputs, got {len(inputs)}")
        
        # 重置所有节点
        for node_id in self.nodes:
            self.nodes[node_id] = 0.0
        
        # 设置输入值
        input_nodes = [node_id for node_id, node in self.genome.node_genes.items() 
                      if node.node_type == 'input']
        
        for i, input_value in enumerate(inputs):
            if i < len(input_nodes):
                self.nodes[input_nodes[i]] = input_value
        
        # 按顺序激活每个节点
        for node_id in self.node_order:
            if self.genome.node_genes[node_id].node_type != 'input':
                self._activate_node(node_id)
        
        # 收集输出
        output_nodes = [node_id for node_id, node in self.genome.node_genes.items() 
                       if node.node_type == 'output']
        
        outputs = [self.nodes[node_id] for node_id in sorted(output_nodes)]
        
        # 应用道德参数调整
        adjusted_outputs = self._apply_moral_adjustments(outputs)
        
        return adjusted_outputs
    
    def _activate_node(self, node_id: int):
        """激活单个节点"""
        node = self.genome.node_genes[node_id]
        
        # 计算输入总和
        input_sum = node.bias
        
        for connection in self.genome.connection_genes.values():
            if (connection.output_node == node_id and 
                connection.enabled and 
                connection.input_node in self.nodes):
                
                input_sum += self.nodes[connection.input_node] * connection.weight
        
        # 应用激活函数
        activation_fn = self.activation_functions.get(
            node.activation_function, self._sigmoid
        )
        
        self.nodes[node_id] = activation_fn(input_sum)
    
    def _apply_moral_adjustments(self, outputs: List[float]) -> List[float]:
        """基于道德参数调整输出"""
        adjusted = outputs.copy()
        
        # 获取道德参数
        moral_params = self.genome.moral_parameters
        
        # 根据不同的道德倾向调整输出
        empathy_factor = moral_params['empathy_sensitivity']
        risk_aversion = moral_params['risk_aversion']
        social_conformity = moral_params['social_conformity']
        
        # 假设输出代表：[帮助, 伤害, 合作, 竞争]
        if len(adjusted) >= 4:
            # 高共情增强帮助倾向，减少伤害倾向
            adjusted[0] *= (1.0 + empathy_factor * 0.5)  # 帮助
            adjusted[1] *= (1.0 - empathy_factor * 0.7)  # 伤害
            
            # 高风险规避减少竞争倾向
            adjusted[3] *= (1.0 - risk_aversion * 0.3)   # 竞争
            
            # 高社会从众增强合作倾向
            adjusted[2] *= (1.0 + social_conformity * 0.4)  # 合作
        
        return adjusted
    
    def evaluate_moral_decision(self, situation_context: Dict[str, Any]) -> Dict[str, Any]:
        """评估道德决策"""
        # 将情境转换为网络输入
        network_inputs = self._encode_situation(situation_context)
        
        # 激活网络
        raw_outputs = self.activate(network_inputs)
        
        # 解释输出
        decision_analysis = self._interpret_outputs(raw_outputs, situation_context)
        
        return {
            'raw_outputs': raw_outputs,
            'decision_analysis': decision_analysis,
            'moral_profile': self.genome.moral_parameters,
            'confidence': self._calculate_decision_confidence(raw_outputs)
        }
    
    def _encode_situation(self, context: Dict[str, Any]) -> List[float]:
        """将情境编码为网络输入"""
        inputs = [0.0] * self.genome.input_size
        
        # 基本情境特征
        inputs[0] = context.get('urgency', 0.0)           # 紧急程度
        inputs[1] = context.get('harm_potential', 0.0)     # 伤害潜力
        inputs[2] = context.get('benefit_potential', 0.0)  # 受益潜力
        inputs[3] = context.get('social_visibility', 0.0)  # 社会可见性
        inputs[4] = context.get('resource_cost', 0.0)      # 资源成本
        inputs[5] = context.get('emotional_stakes', 0.0)   # 情感利害
        
        # 关系因素
        inputs[6] = context.get('relationship_closeness', 0.0)  # 关系亲密度
        inputs[7] = context.get('authority_presence', 0.0)      # 权威存在
        inputs[8] = context.get('group_pressure', 0.0)          # 群体压力
        
        # 道德相关因素
        inputs[9] = context.get('rule_violation', 0.0)     # 规则违反程度
        inputs[10] = context.get('fairness_concern', 0.0)  # 公平关切
        inputs[11] = context.get('duty_obligation', 0.0)   # 义务责任
        
        return inputs
    
    def _interpret_outputs(self, outputs: List[float], context: Dict[str, Any]) -> Dict[str, Any]:
        """解释网络输出为具体决策"""
        if len(outputs) < 4:
            return {'error': 'Insufficient outputs'}
        
        action_tendencies = {
            'help': max(0.0, outputs[0]),
            'harm': max(0.0, outputs[1]), 
            'cooperate': max(0.0, outputs[2]),
            'compete': max(0.0, outputs[3])
        }
        
        # 确定主导行为倾向
        dominant_action = max(action_tendencies.items(), key=lambda x: x[1])
        
        # 计算行为确定性
        output_variance = np.var(list(action_tendencies.values()))
        certainty = 1.0 / (1.0 + output_variance)
        
        return {
            'action_tendencies': action_tendencies,
            'recommended_action': dominant_action[0],
            'action_strength': dominant_action[1],
            'decision_certainty': certainty,
            'moral_reasoning': self._generate_moral_reasoning(action_tendencies, context)
        }
    
    def _generate_moral_reasoning(self, action_tendencies: Dict[str, float], 
                                context: Dict[str, Any]) -> str:
        """生成道德推理解释"""
        moral_params = self.genome.moral_parameters
        dominant_framework = max(
            ['kantian_weight', 'utilitarian_weight', 'virtue_weight'],
            key=lambda x: moral_params[x]
        )
        
        reasoning_parts = []
        
        # 基于主导道德框架的推理
        if dominant_framework == 'kantian_weight':
            reasoning_parts.append("基于义务伦理学考虑")
            if action_tendencies['help'] > 0.5:
                reasoning_parts.append("帮助他人符合道德义务")
        elif dominant_framework == 'utilitarian_weight':
            reasoning_parts.append("基于效用最大化考虑")
            if action_tendencies['cooperate'] > 0.5:
                reasoning_parts.append("合作能带来更大的整体福利")
        else:
            reasoning_parts.append("基于品德伦理学考虑")
        
        # 情感因素影响
        if moral_params['empathy_sensitivity'] > 0.7:
            reasoning_parts.append("高共情能力影响决策")
        
        if moral_params['risk_aversion'] > 0.7:
            reasoning_parts.append("谨慎考虑潜在风险")
        
        return "; ".join(reasoning_parts)
    
    def _calculate_decision_confidence(self, outputs: List[float]) -> float:
        """计算决策置信度"""
        # 基于输出的极端程度计算置信度
        max_output = max(abs(x) for x in outputs)
        output_spread = max(outputs) - min(outputs)
        
        confidence = (max_output + output_spread) / 2.0
        return min(1.0, confidence)
    
    # 激活函数
    def _sigmoid(self, x: float) -> float:
        """Sigmoid激活函数"""
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
    
    def _relu(self, x: float) -> float:
        """ReLU激活函数"""
        return max(0.0, x)
    
    def get_network_complexity(self) -> Dict[str, int]:
        """获取网络复杂度指标"""
        enabled_connections = sum(1 for conn in self.genome.connection_genes.values() 
                                if conn.enabled)
        
        return {
            'total_nodes': len(self.genome.node_genes),
            'hidden_nodes': len([n for n in self.genome.node_genes.values() 
                               if n.node_type == 'hidden']),
            'total_connections': len(self.genome.connection_genes),
            'enabled_connections': enabled_connections,
            'network_depth': self._calculate_network_depth()
        }
    
    def _calculate_network_depth(self) -> int:
        """计算网络深度"""
        # 简化版本：隐藏层数量 + 1
        hidden_count = len([n for n in self.genome.node_genes.values() 
                          if n.node_type == 'hidden'])
        return hidden_count + 1