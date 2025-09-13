"""
道德伦理计算框架

实现康德定言命令和功利主义的可计算版本。
"""

from .kantian_ethics import KantianEthics
from .utilitarian_ethics import UtilitarianEthics
from .virtue_ethics import VirtueEthics
from .moral_framework import MoralFramework
from .moral_evaluator import MoralEvaluator

__all__ = [
    "KantianEthics",
    "UtilitarianEthics", 
    "VirtueEthics",
    "MoralFramework",
    "MoralEvaluator"
]