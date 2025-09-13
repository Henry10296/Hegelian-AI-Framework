"""
道德感知NPC行为系统 (Moral-Aware NPC Behavior System)

一个融合康德定言命令和功利主义的可计算道德框架，
使用神经进化算法优化NPC行为，并实现道德传染机制。

主要模块:
- core: 核心NPC智能体和系统管理
- ethics: 康德和功利主义道德计算框架
- neuroevolution: NEAT神经进化算法
- contagion: NPC间道德传染机制
- player_analysis: 玩家行为分析和道德建模
"""

__version__ = "1.0.0"
__author__ = "Moral AI Research Team"

from .core import MoralNPC, NPCManager
from .ethics import KantianEthics, UtilitarianEthics, MoralFramework
from .neuroevolution import NEATEvolution, MoralGenome
from .contagion import MoralContagionNetwork
from .player_analysis import PlayerMoralProfiler

__all__ = [
    "MoralNPC",
    "NPCManager", 
    "KantianEthics",
    "UtilitarianEthics",
    "MoralFramework",
    "NEATEvolution",
    "MoralGenome",
    "MoralContagionNetwork",
    "PlayerMoralProfiler"
]