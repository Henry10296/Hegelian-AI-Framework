"""
NEAT进化算法主引擎
"""

import random
import numpy as np
from typing import Dict, List, Set, Tuple, Optional, Callable
from collections import defaultdict
from .moral_genome import MoralGenome
from .neural_network import MoralNeuralNetwork
from .fitness_evaluator import FitnessEvaluator


class Species:
    """物种类"""
    
    def __init__(self, species_id: int, representative: MoralGenome):
        self.species_id = species_id
        self.representative = representative
        self.members: List[MoralGenome] = []
        self.best_fitness = 0.0
        self.average_fitness = 0.0
        self.generations_without_improvement = 0
        self.offspring_count = 0
    
    def add_member(self, genome: MoralGenome):
        """添加成员到物种"""
        genome.species_id = self.species_id
        self.members.append(genome)
    
    def calculate_average_fitness(self):
        """计算平均适应度"""
        if not self.members:
            self.average_fitness = 0.0
            return
        
        total_fitness = sum(member.adjusted_fitness for member in self.members)
        self.average_fitness = total_fitness / len(self.members)
        
        # 更新最佳适应度
        current_best = max(member.fitness for member in self.members)
        if current_best > self.best_fitness:
            self.best_fitness = current_best
            self.generations_without_improvement = 0
        else:
            self.generations_without_improvement += 1
    
    def remove_weakest(self, survival_rate: float = 0.5):
        """移除最弱的个体"""
        if not self.members:
            return
        
        self.members.sort(key=lambda x: x.adjusted_fitness, reverse=True)
        survivors_count = max(1, int(len(self.members) * survival_rate))
        self.members = self.members[:survivors_count]


class NEATEvolution:
    """NEAT进化算法"""
    
    def __init__(self, population_size: int = 150):
        self.population_size = population_size
        self.population: List[MoralGenome] = []
        self.species: Dict[int, Species] = {}
        self.generation = 0
        self.species_counter = 0
        
        # 进化参数
        self.compatibility_threshold = 3.0
        self.survival_rate = 0.2
        self.mutation_rates = {
            'add_node': 0.03,
            'add_connection': 0.05,
            'weight_mutation': 0.8,
            'moral_parameter_mutation': 0.1
        }
        
        # 适应度评估器
        self.fitness_evaluator = FitnessEvaluator()
        
        # 统计信息
        self.best_genome: Optional[MoralGenome] = None
        self.best_fitness = 0.0
        self.fitness_history: List[float] = []
        
        # 初始化种群
        self._initialize_population()
    
    def _initialize_population(self):
        """初始化种群"""
        self.population = []
        
        for i in range(self.population_size):
            genome = MoralGenome(genome_id=f"gen0_individual_{i}")
            
            # 为每个个体添加一些随机变异
            if random.random() < 0.5:
                genome.add_connection_mutation()
            if random.random() < 0.1:
                genome.add_node_mutation()
            
            genome.weight_mutation()
            genome.moral_parameter_mutation()
            
            self.population.append(genome)
    
    def evolve_generation(self, scenario_batch: List[Dict]) -> Dict[str, any]:
        """进化一代"""
        self.generation += 1
        
        # 评估适应度
        self._evaluate_population(scenario_batch)
        
        # 物种分类
        self._speciate_population()
        
        # 计算调整适应度
        self._calculate_adjusted_fitness()
        
        # 选择和繁殖
        new_population = self._reproduce_population()
        
        # 应用变异
        self._mutate_population(new_population)
        
        # 更新种群
        self.population = new_population
        
        # 更新统计信息
        generation_stats = self._update_statistics()
        
        # 清理物种
        self._cleanup_species()
        
        return generation_stats
    
    def _evaluate_population(self, scenario_batch: List[Dict]):
        """评估种群适应度"""
        for genome in self.population:
            network = MoralNeuralNetwork(genome)
            fitness_scores = []
            
            for scenario in scenario_batch:
                fitness = self.fitness_evaluator.evaluate_genome_on_scenario(
                    genome, network, scenario
                )
                fitness_scores.append(fitness)
            
            # 综合适应度
            genome.fitness = np.mean(fitness_scores)
    
    def _speciate_population(self):
        """将种群分类到物种"""
        # 清空现有物种成员
        for species in self.species.values():
            species.members.clear()
        
        unassigned_genomes = self.population.copy()
        
        # 尝试将每个基因组分配到现有物种
        for genome in self.population:
            assigned = False
            
            for species in self.species.values():
                compatibility = genome.calculate_compatibility(species.representative)
                
                if compatibility < self.compatibility_threshold:
                    species.add_member(genome)
                    assigned = True
                    break
            
            # 如果无法分配到现有物种，创建新物种
            if not assigned:
                self.species_counter += 1
                new_species = Species(self.species_counter, genome)
                new_species.add_member(genome)
                self.species[self.species_counter] = new_species
        
        # 移除空物种
        empty_species = [sid for sid, species in self.species.items() if not species.members]
        for sid in empty_species:
            del self.species[sid]
    
    def _calculate_adjusted_fitness(self):
        """计算调整适应度 (共享适应度)"""
        for species in self.species.values():
            species.calculate_average_fitness()
            
            # 共享适应度：个体适应度除以物种大小
            for member in species.members:
                member.adjusted_fitness = member.fitness / len(species.members)
    
    def _reproduce_population(self) -> List[MoralGenome]:
        """繁殖新种群"""
        new_population = []
        
        # 计算每个物种的后代数量
        total_adjusted_fitness = sum(species.average_fitness for species in self.species.values())
        
        if total_adjusted_fitness == 0:
            # 如果总适应度为0，平均分配
            for species in self.species.values():
                species.offspring_count = self.population_size // len(self.species)
        else:
            for species in self.species.values():
                species.offspring_count = int(
                    (species.average_fitness / total_adjusted_fitness) * self.population_size
                )
        
        # 确保总后代数等于种群大小
        total_offspring = sum(species.offspring_count for species in self.species.values())
        if total_offspring < self.population_size:
            # 给最佳物种额外的后代
            best_species = max(self.species.values(), key=lambda s: s.average_fitness)
            best_species.offspring_count += self.population_size - total_offspring
        
        # 为每个物种生成后代
        for species in self.species.values():
            # 保留最佳个体 (精英主义)
            if species.members:
                best_member = max(species.members, key=lambda x: x.fitness)
                new_population.append(best_member.copy())
                
                # 生成其他后代
                for _ in range(species.offspring_count - 1):
                    if len(species.members) >= 2:
                        # 交叉繁殖
                        parent1 = self._tournament_selection(species.members)
                        parent2 = self._tournament_selection(species.members)
                        child = parent1.crossover(parent2)
                    else:
                        # 无性繁殖
                        parent = species.members[0]
                        child = parent.copy()
                    
                    new_population.append(child)
        
        # 填充到目标种群大小
        while len(new_population) < self.population_size:
            # 从最佳个体中随机复制
            if self.population:
                best_genome = max(self.population, key=lambda x: x.fitness)
                new_population.append(best_genome.copy())
            else:
                new_population.append(MoralGenome())
        
        return new_population[:self.population_size]
    
    def _tournament_selection(self, population: List[MoralGenome], 
                            tournament_size: int = 3) -> MoralGenome:
        """锦标赛选择"""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda x: x.adjusted_fitness)
    
    def _mutate_population(self, population: List[MoralGenome]):
        """对种群应用变异"""
        for genome in population[1:]:  # 跳过精英个体
            # 结构变异
            if random.random() < self.mutation_rates['add_node']:
                genome.add_node_mutation()
            
            if random.random() < self.mutation_rates['add_connection']:
                genome.add_connection_mutation()
            
            # 权重变异
            if random.random() < self.mutation_rates['weight_mutation']:
                genome.weight_mutation()
            
            # 道德参数变异
            if random.random() < self.mutation_rates['moral_parameter_mutation']:
                genome.moral_parameter_mutation()
    
    def _update_statistics(self) -> Dict[str, any]:
        """更新统计信息"""
        if not self.population:
            return {}
        
        # 当前代最佳适应度
        current_best = max(self.population, key=lambda x: x.fitness)
        current_best_fitness = current_best.fitness
        
        # 更新全局最佳
        if current_best_fitness > self.best_fitness:
            self.best_fitness = current_best_fitness
            self.best_genome = current_best.copy()
        
        # 计算统计信息
        fitnesses = [genome.fitness for genome in self.population]
        avg_fitness = np.mean(fitnesses)
        self.fitness_history.append(avg_fitness)
        
        # 物种统计
        species_stats = {
            'count': len(self.species),
            'sizes': [len(species.members) for species in self.species.values()],
            'avg_fitness': [species.average_fitness for species in self.species.values()]
        }
        
        return {
            'generation': self.generation,
            'best_fitness': current_best_fitness,
            'average_fitness': avg_fitness,
            'population_size': len(self.population),
            'species_stats': species_stats,
            'complexity_stats': self._calculate_complexity_stats()
        }
    
    def _calculate_complexity_stats(self) -> Dict[str, float]:
        """计算种群复杂度统计"""
        if not self.population:
            return {}
        
        node_counts = []
        connection_counts = []
        
        for genome in self.population:
            node_counts.append(len(genome.node_genes))
            enabled_connections = sum(1 for conn in genome.connection_genes.values() 
                                    if conn.enabled)
            connection_counts.append(enabled_connections)
        
        return {
            'avg_nodes': np.mean(node_counts),
            'avg_connections': np.mean(connection_counts),
            'max_nodes': max(node_counts),
            'max_connections': max(connection_counts)
        }
    
    def _cleanup_species(self):
        """清理停滞的物种"""
        stagnation_threshold = 15
        
        species_to_remove = []
        for species_id, species in self.species.items():
            if species.generations_without_improvement > stagnation_threshold:
                species_to_remove.append(species_id)
        
        for species_id in species_to_remove:
            del self.species[species_id]
    
    def get_best_genome(self) -> Optional[MoralGenome]:
        """获取最佳基因组"""
        return self.best_genome
    
    def get_population_diversity(self) -> float:
        """计算种群多样性"""
        if len(self.population) < 2:
            return 0.0
        
        diversity_sum = 0.0
        comparison_count = 0
        
        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):
                diversity = self.population[i].calculate_compatibility(self.population[j])
                diversity_sum += diversity
                comparison_count += 1
        
        return diversity_sum / comparison_count if comparison_count > 0 else 0.0
    
    def save_checkpoint(self, filepath: str):
        """保存进化检查点"""
        checkpoint_data = {
            'generation': self.generation,
            'population': [genome.__dict__ for genome in self.population],
            'best_fitness': self.best_fitness,
            'fitness_history': self.fitness_history,
            'species_counter': self.species_counter
        }
        
        import json
        with open(filepath, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
    
    def load_checkpoint(self, filepath: str):
        """加载进化检查点"""
        import json
        with open(filepath, 'r') as f:
            checkpoint_data = json.load(f)
        
        self.generation = checkpoint_data['generation']
        self.best_fitness = checkpoint_data['best_fitness']
        self.fitness_history = checkpoint_data['fitness_history']
        self.species_counter = checkpoint_data['species_counter']
        
        # 重建种群 (简化版本)
        # 实际应用中需要完整的序列化/反序列化逻辑