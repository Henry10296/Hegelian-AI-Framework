# -*- coding: utf-8 -*-
"""
AI Core Models Package

该包定义了AI决策所需的核心数据结构。
"""

# 从其各自的文件中导入所有模型
from .ethical_case import (
    EthicalCase,
    ActionOption,
    Stakeholder,
    CaseType,
    RelationshipType
)
from .moral_genome import MoralGenome

# __all__ 定义了当其他模块使用 'from ai_core.models import *' 时，哪些名称会被导入。
# 这是一个最佳实践，用于明确地声明包的公共API。
__all__ = [
    # from ethical_case
    'EthicalCase',
    'ActionOption',
    'Stakeholder',
    'CaseType',
    'RelationshipType',
    
    # from moral_genome
    'MoralGenome'
]
