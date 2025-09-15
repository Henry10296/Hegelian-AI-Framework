# -*- coding: utf-8 -*-
"""
道德基因组 (Moral Genome)

该模块定义了AI的道德基因组，它是神经进化过程中的基本遗传单位。
每个基因组都包含了一套完整的道德价值观，并且能够进行变异。
"""

import random
from typing import Dict

class MoralGenome:
    """
    代表一个AI的道德基因组。
    它封装了AI的道德直觉，并提供了变异（mutation）的方法。
    """

    def __init__(self, initial_intuitions: Dict[str, float]):
        """
        初始化基因组。

        Args:
            initial_intuitions (Dict[str, float]): 初始的道德直觉字典。
        """
        self.genes: Dict[str, float] = initial_intuitions.copy()

    def mutate(self, mutation_rate: float, mutation_strength: float):
        """
        对基因组进行变异。

        以一定的概率（mutation_rate）对基因组中的某个基因（道德直觉）
        进行一次微小的、随机的调整（调整幅度由mutation_strength决定）。

        Args:
            mutation_rate (float): 每个基因发生突变的概率 (0.0 to 1.0)。
            mutation_strength (float): 突变发生时，基因值的最大变化量。
        """
        # print(f"   🧬 [基因突变] 开始进行，突变率: {mutation_rate}, 突变强度: {mutation_strength}")
        for gene_name in self.genes.keys():
            if random.random() < mutation_rate:
                current_value = self.genes[gene_name]
                change = random.uniform(-mutation_strength, mutation_strength)
                new_value = current_value + change
                self.genes[gene_name] = max(0.0, min(1.0, new_value))
                # print(f"     - 基因 '{gene_name}' 发生突变: {current_value:.2f} -> {self.genes[gene_name]:.2f}")

    def get_intuitions(self) -> Dict[str, float]:
        """
        获取当前基因组所代表的道德直觉。
        """
        return self.genes

    def __repr__(self) -> str:
        return f"MoralGenome(Genes={self.genes})"
