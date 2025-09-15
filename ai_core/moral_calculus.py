# -*- coding: utf-8 -*-
"""
道德微积分模块 (Moral Calculus) - 已集成关系感知

该模块现在会根据AI与利益相关者之间的社会关系，来调整其道德计算的权重。
"""

from typing import Dict
from .models.ethical_case import ActionOption, EthicalCase, RelationshipType

# --- 关系权重定义 ---
# 定义了在不同伦理学计算中，不同社会关系的权重

# 在计算功利主义（整体效益）时，对不同关系的人的“幸福感”的重视程度
RELATIONSHIP_UTILITY_WEIGHTS = {
    RelationshipType.SELF: 1.0,    # 对自己的效用，正常计算
    RelationshipType.FRIEND: 1.2,  # 对朋友的效用，权重放大
    RelationshipType.STRANGER: 1.0,# 对陌生人的效用，正常计算
    RelationshipType.ENEMY: 0.8,   # 对敌人的效用，权重缩小
}

# 在计算义务论（违反规则）时，对不同关系的人违反规则的“严重性”的惩罚系数
RELATIONSHIP_DEONTOLOGY_PENALTY = {
    RelationshipType.SELF: 1.0,
    RelationshipType.FRIEND: 1.5,  # 对朋友撒谎，惩罚加重
    RelationshipType.STRANGER: 1.0,
    RelationshipType.ENEMY: 0.5,   # 对敌人撒谎，惩罚减轻
}

def calculate_utilitarian_score(action: ActionOption, case: EthicalCase) -> float:
    """
    计算一个行动的“功利主义”得分，现在考虑了社会关系。
    """
    weighted_total_utility = 0.0
    utility_scores = action.metadata.get('utility_scores', {})
    if not utility_scores:
        return 0.5 # 返回一个中性值

    for stakeholder in case.stakeholders:
        utility = utility_scores.get(stakeholder.name, 0)
        # 获取关系权重，如果找不到则默认为1.0
        weight = RELATIONSHIP_UTILITY_WEIGHTS.get(stakeholder.relationship, 1.0)
        weighted_total_utility += utility * weight
    
    # 归一化处理
    max_possible_utility = 10 * len(case.stakeholders) if case.stakeholders else 10
    normalized_score = (weighted_total_utility / max_possible_utility) if max_possible_utility != 0 else 0
    # 将得分从[-1, 1]的范围映射到[0, 1]
    final_score = (normalized_score + 1) / 2
    return max(0.0, min(1.0, final_score))

def calculate_deontological_score(action: ActionOption, case: EthicalCase) -> float:
    """
    计算一个行动的“义务论”得分，现在考虑了社会关系。
    元数据需求: action.metadata['violates_rules'] should be a list of dicts, e.g., 
                  [{'rule': 'do_not_lie', 'target': 'guard'}]
    """
    total_penalty = 0.0
    violations = action.metadata.get('violates_rules', [])
    
    # 基础惩罚值
    BASE_PENALTY = 0.4

    for violation in violations:
        target_name = violation.get('target')
        penalty_multiplier = 1.0

        if target_name:
            # 找到被违反规则的目标利益相关者
            target_stakeholder = next((s for s in case.stakeholders if s.name == target_name), None)
            if target_stakeholder:
                # 获取关系对应的惩罚系数
                penalty_multiplier = RELATIONSHIP_DEONTOLOGY_PENALTY.get(target_stakeholder.relationship, 1.0)
        
        total_penalty += BASE_PENALTY * penalty_multiplier

    score = 1.0 - total_penalty
    return max(0.0, min(1.0, score))

def calculate_virtue_ethics_score(action: ActionOption, case: EthicalCase) -> float:
    """
    计算一个行动的“德性伦理”得分。目前与关系无关。
    """
    virtue_scores = action.metadata.get('expresses_virtues', {})
    if not virtue_scores:
        return 0.5 # 返回一个中性值
    
    average_score = sum(virtue_scores.values()) / len(virtue_scores)
    return max(0.0, min(1.0, average_score))

# --- 主计算函数 ---

def calculate_moral_vector(action: ActionOption, case: EthicalCase) -> Dict[str, float]:
    """
    为单个行动计算其完整的多维度“道德向量”。
    """
    return {
        'utilitarian': calculate_utilitarian_score(action, case),
        'deontological': calculate_deontological_score(action, case),
        'virtue': calculate_virtue_ethics_score(action, case),
    }
