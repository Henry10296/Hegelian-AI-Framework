# -*- coding: utf-8 -*-
"""
道德演化引擎 (Moral Evolver) - 已升级为包含精英选择和交叉的遗传算法
"""

import copy
import random
from typing import TYPE_CHECKING, List

# 修复ModuleNotFoundError: 从正确的路径导入MoralGenome
from .models.moral_genome import MoralGenome

if TYPE_CHECKING:
    from .ethical_reasoning_framework import EthicalAgent
    from .moral_profiler import MoralProfiler

class MoralEvolver:
    """
    一个实现了精英选择和交叉的、更高级的道德演化器。
    """

    def __init__(self, population_size: int = 20, elite_size: int = 2, mutation_rate: float = 0.1, mutation_strength: float = 0.05, social_learning_rate: float = 0.05):
        self.population_size = population_size
        self.elite_size = elite_size # 精英数量
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.social_learning_rate = social_learning_rate

    def _crossover(self, parent1: MoralGenome, parent2: MoralGenome) -> MoralGenome:
        """(新增) 对两个父代基因组进行单点交叉，创造一个子代。"""
        child_genes = {}
        genes1 = parent1.get_intuitions()
        genes2 = parent2.get_intuitions()
        gene_keys = list(genes1.keys())
        
        crossover_point = random.randint(1, len(gene_keys) - 1)
        
        for i, key in enumerate(gene_keys):
            if i < crossover_point:
                child_genes[key] = genes1[key]
            else:
                child_genes[key] = genes2[key]
                
        return MoralGenome(child_genes)

    def calculate_fitness(self, genome: MoralGenome, player_profile: dict) -> float:
        """适应度函数：计算一个基因组与玩家道德画像的“契合度”。"""
        error = 0.0
        num_genes = 0
        profile_to_gene_map = {
            "harm_care": ["utilitarian", "virtue"],
            "fairness_reciprocity": ["deontological"],
        }
        ai_genes = genome.get_intuitions()
        for profile_key, gene_keys in profile_to_gene_map.items():
            if profile_key in player_profile:
                player_value = player_profile[profile_key]
                for gene_key in gene_keys:
                    if gene_key in ai_genes:
                        ai_value = ai_genes[gene_key]
                        error += (player_value - ai_value) ** 2
                        num_genes += 1
        if num_genes == 0: return 0.0
        mean_squared_error = error / num_genes
        return 1 / (mean_squared_error + 1e-6)

    def evolve_from_population(self, agent: 'EthicalAgent', profiler: 'MoralProfiler'):
        """(已重构) 执行一次“精英选择 + 交叉 + 变异”的演化循环。"""
        player_profile = profiler.get_player_profile()
        current_genome = agent.get_genome()

        population: List[MoralGenome] = [current_genome]
        for _ in range(self.population_size - 1):
            mutant = copy.deepcopy(current_genome)
            mutant.mutate(self.mutation_rate, self.mutation_strength)
            population.append(mutant)
        
        fitness_scores = [(genome, self.calculate_fitness(genome, player_profile)) for genome in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)

        elites = [genome for genome, fitness in fitness_scores[:self.elite_size]]

        new_population = elites
        while len(new_population) < self.population_size:
            parent1 = random.choice(elites)
            parent2 = random.choice(elites)
            child = self._crossover(parent1, parent2)
            child.mutate(self.mutation_rate, self.mutation_strength)
            new_population.append(child)

        final_fitness_scores = [(genome, self.calculate_fitness(genome, player_profile)) for genome in new_population]
        final_fitness_scores.sort(key=lambda x: x[1], reverse=True)
        best_new_genome = final_fitness_scores[0][0]
        
        agent.set_genome(best_new_genome)

    def evolve_towards(self, agent: 'EthicalAgent', target_genome: 'MoralGenome'):
        """让一个AI的基因组，向一个目标基因组进行轻微的“靠拢”（用于道德传染）。"""
        current_genes = agent.get_genome().genes
        target_genes = target_genome.get_intuitions()
        for gene_name, target_value in target_genes.items():
            if gene_name in current_genes:
                current_value = current_genes[gene_name]
                error = target_value - current_value
                adjustment = error * self.social_learning_rate
                new_value = current_value + adjustment
                current_genes[gene_name] = max(0.0, min(1.0, new_value))
        print(f"       - 受社会影响，{agent.name}的基因组发生了微调。")
