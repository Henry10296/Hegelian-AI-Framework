"""
道德感知NPC系统基础演示

展示系统的核心功能：
1. 创建道德感知NPC
2. 道德事件传播
3. 玩家行为分析
4. 神经进化训练
"""

import sys
import os
import time
import random
from typing import Dict, Any

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moral_npc_system.core.moral_state import MoralState
from moral_npc_system.core.action import Action, ActionType
from moral_npc_system.ethics.moral_framework import MoralFramework
from moral_npc_system.contagion.social_network import SocialNetwork
from moral_npc_system.contagion.moral_contagion_network import MoralContagionNetwork
from moral_npc_system.contagion.moral_event import MoralEvent, MoralEventType, MoralValence
from moral_npc_system.player_analysis.player_moral_profiler import PlayerMoralProfiler, PlayerAction
from moral_npc_system.neuroevolution.neat_evolution import NEATEvolution


def demonstrate_moral_framework():
    """演示道德框架的使用"""
    print("=" * 50)
    print("道德框架演示")
    print("=" * 50)
    
    # 创建道德框架
    moral_framework = MoralFramework()
    
    # 创建NPC道德状态
    kantian_npc = MoralState(
        kantian_weight=0.7,
        utilitarian_weight=0.2,
        virtue_weight=0.1,
        empathy_level=0.8,
        moral_courage=0.7
    )
    
    utilitarian_npc = MoralState(
        kantian_weight=0.2,
        utilitarian_weight=0.7,
        virtue_weight=0.1,
        empathy_level=0.6,
        risk_tolerance=0.4
    )
    
    # 创建测试行为
    help_action = Action(
        id="demo_help",
        action_type=ActionType.HELP,
        actor_id="npc_001",
        target_id="player",
        intensity=0.8
    )
    
    harm_action = Action(
        id="demo_harm", 
        action_type=ActionType.HARM,
        actor_id="npc_001",
        target_id="innocent",
        intensity=0.6
    )
    
    # 测试情境
    emergency_context = {
        'urgency': 0.9,
        'harm_potential': 0.3,
        'benefit_potential': 0.8,
        'social_visibility': 0.5,
        'requires_moral_courage': True
    }
    
    # 评估行为
    print("\n康德倾向NPC对帮助行为的评估:")
    kantian_help_eval = moral_framework.evaluate_action(help_action, kantian_npc, emergency_context)
    print(f"最终评分: {kantian_help_eval['final_score']:.3f}")
    print(f"推荐: {kantian_help_eval['recommendation']}")
    
    print("\n功利主义倾向NPC对帮助行为的评估:")
    util_help_eval = moral_framework.evaluate_action(help_action, utilitarian_npc, emergency_context)
    print(f"最终评分: {util_help_eval['final_score']:.3f}")
    print(f"推荐: {util_help_eval['recommendation']}")
    
    print("\n康德倾向NPC对伤害行为的评估:")
    kantian_harm_eval = moral_framework.evaluate_action(harm_action, kantian_npc, emergency_context)
    print(f"最终评分: {kantian_harm_eval['final_score']:.3f}")
    print(f"推荐: {kantian_harm_eval['recommendation']}")


def demonstrate_moral_contagion():
    """演示道德传染机制"""
    print("\n" + "=" * 50)
    print("道德传染机制演示")
    print("=" * 50)
    
    # 创建社交网络
    social_network = SocialNetwork()
    contagion_network = MoralContagionNetwork(social_network)
    
    # 添加NPC
    npc_ids = [f"npc_{i:03d}" for i in range(10)]
    
    for npc_id in npc_ids:
        moral_state = MoralState(
            kantian_weight=random.uniform(0.2, 0.8),
            utilitarian_weight=random.uniform(0.1, 0.6),
            virtue_weight=random.uniform(0.1, 0.4),
            empathy_level=random.uniform(0.3, 0.9),
            moral_plasticity=random.uniform(0.2, 0.8)
        )
        contagion_network.add_npc(npc_id, moral_state)
    
    # 建立社交关系
    for i in range(len(npc_ids)):
        for j in range(i + 1, min(i + 4, len(npc_ids))):  # 每个NPC与接下来3个建立关系
            relationship_types = ['friendship', 'colleague', 'acquaintance']
            rel_type = random.choice(relationship_types)
            strength = random.uniform(0.3, 0.8)
            
            social_network.add_relationship(
                npc_ids[i], npc_ids[j], rel_type, 
                strength=strength, trust_level=strength * 0.8
            )
    
    print(f"创建了 {len(npc_ids)} 个NPC的社交网络")
    print(f"关系数量: {len(social_network.relationships)}")
    
    # 创建并传播道德事件
    altruistic_event = MoralEvent(
        event_id="demo_altruism",
        event_type=MoralEventType.ALTRUISTIC_ACT,
        valence=MoralValence.POSITIVE,
        primary_actor=npc_ids[0],
        target=npc_ids[1],
        intensity=0.8,
        visibility=0.9,
        moral_weight=0.7
    )
    
    print(f"\n传播道德事件: {altruistic_event.event_type.value}")
    propagation_result = contagion_network.introduce_moral_event(altruistic_event)
    
    print(f"传播结果:")
    print(f"- 影响NPC数量: {len(propagation_result['affected_npcs'])}")
    print(f"- 传播深度: {propagation_result['propagation_depth']}")
    print(f"- 传播路径数: {len(propagation_result['transmission_paths'])}")
    
    # 显示网络道德气候
    moral_climate = contagion_network.get_network_moral_climate()
    print(f"\n网络道德气候:")
    print(f"- 平均共情水平: {moral_climate['average_empathy']:.3f}")
    print(f"- 平均道德勇气: {moral_climate['average_moral_courage']:.3f}")
    print(f"- 道德框架分布: {moral_climate['framework_distribution']}")


def demonstrate_player_analysis():
    """演示玩家行为分析"""
    print("\n" + "=" * 50)
    print("玩家行为分析演示") 
    print("=" * 50)
    
    profiler = PlayerMoralProfiler()
    
    # 模拟玩家行为记录
    player_actions = [
        PlayerAction(ActionType.HELP, "npc_001", {"urgency": 0.7}, 0.8, time.time(), "session_1"),
        PlayerAction(ActionType.SHARE, "npc_002", {"resource_scarcity": 0.6}, 0.6, time.time(), "session_1"),
        PlayerAction(ActionType.COOPERATE, "npc_003", {"group_pressure": 0.3}, 0.9, time.time(), "session_1"),
        PlayerAction(ActionType.HELP, "npc_004", {"emergency": True}, 0.9, time.time(), "session_1"),
        PlayerAction(ActionType.SACRIFICE, "npc_005", {"moral_stakes": 0.8}, 0.7, time.time(), "session_1"),
        PlayerAction(ActionType.IGNORE, "beggar", {"social_visibility": 0.2}, -0.2, time.time(), "session_1"),
        PlayerAction(ActionType.COOPERATE, "team", {"benefit_potential": 0.8}, 0.8, time.time(), "session_1"),
        PlayerAction(ActionType.HELP, "stranger", {"personal_cost": 0.4}, 0.5, time.time(), "session_1"),
        PlayerAction(ActionType.SHARE, "child", {"empathy_trigger": 0.9}, 0.9, time.time(), "session_1"),
        PlayerAction(ActionType.COOPERATE, "ally", {"trust_level": 0.8}, 0.8, time.time(), "session_1"),
        PlayerAction(ActionType.HELP, "enemy", {"moral_courage": 0.9}, 0.6, time.time(), "session_1"),
        PlayerAction(ActionType.SACRIFICE, "community", {"collective_good": 0.9}, 0.8, time.time(), "session_1")
    ]
    
    # 记录行为
    for action in player_actions:
        profiler.record_player_action(action)
    
    # 获取分析结果
    moral_profile = profiler.get_moral_profile()
    behavioral_summary = profiler.get_behavioral_summary()
    
    print("玩家道德档案:")
    print(f"- 主导道德框架: {moral_profile['primary_framework']}")
    print(f"- 道德权重: {moral_profile['moral_weights']}")
    print(f"- 一致性评分: {moral_profile['consistency_score']:.3f}")
    print(f"- 共情指标: {moral_profile['empathy_indicators']:.3f}")
    print(f"- 风险容忍度: {moral_profile['risk_tolerance']:.3f}")
    print(f"- 社会导向: {moral_profile['social_orientation']:.3f}")
    
    print(f"\n行为摘要:")
    print(f"- 记录行为总数: {behavioral_summary['total_actions_recorded']}")
    print(f"- 主导行为倾向: {behavioral_summary['dominant_behavioral_tendency']}")
    print(f"- 档案置信度: {behavioral_summary['moral_profile_confidence']:.3f}")
    
    # 预测行为偏好
    test_situation = {
        'urgency': 0.8,
        'social_visibility': 0.6,
        'harm_potential': 0.3,
        'benefit_potential': 0.7,
        'personal_cost': 0.4
    }
    
    predicted_preferences = profiler.predict_action_preference(test_situation)
    print(f"\n特定情境下的行为偏好预测:")
    sorted_preferences = sorted(predicted_preferences.items(), key=lambda x: x[1], reverse=True)
    for action_type, preference in sorted_preferences[:5]:
        print(f"- {action_type.value}: {preference:.3f}")


def demonstrate_neuroevolution():
    """演示神经进化算法"""
    print("\n" + "=" * 50)
    print("神经进化算法演示")
    print("=" * 50)
    
    # 创建进化算法
    evolution = NEATEvolution(population_size=50)
    
    # 创建训练情境
    training_scenarios = []
    
    # 道德两难情境
    scenarios_templates = [
        {
            'scenario_type': 'trolley_problem',
            'urgency': 0.9,
            'harm_potential': 0.8,
            'benefit_potential': 0.6,
            'social_visibility': 0.3,
            'target_id': 'victims'
        },
        {
            'scenario_type': 'resource_sharing',
            'urgency': 0.4,
            'benefit_potential': 0.7,
            'social_visibility': 0.6,
            'fairness_concern': 0.8,
            'target_id': 'needy_person'
        },
        {
            'scenario_type': 'authority_conflict',
            'urgency': 0.5,
            'harm_potential': 0.6,
            'authority_presence': 0.9,
            'moral_courage_required': True,
            'target_id': 'authority'
        }
    ]
    
    # 为每个模板创建变体
    for template in scenarios_templates:
        for _ in range(5):
            scenario = template.copy()
            # 添加一些随机变化
            for key, value in scenario.items():
                if isinstance(value, (int, float)) and key != 'scenario_type':
                    noise = random.uniform(-0.1, 0.1)
                    scenario[key] = max(0.0, min(1.0, value + noise))
            training_scenarios.append(scenario)
    
    print(f"创建了 {len(training_scenarios)} 个训练情境")
    
    # 运行几代进化
    best_fitness_history = []
    
    print("\n开始进化训练...")
    for generation in range(10):  # 演示版本只运行10代
        stats = evolution.evolve_generation(training_scenarios)
        best_fitness_history.append(stats['best_fitness'])
        
        if generation % 2 == 0:  # 每2代输出一次
            print(f"第 {generation} 代:")
            print(f"  最佳适应度: {stats['best_fitness']:.4f}")
            print(f"  平均适应度: {stats['average_fitness']:.4f}")
            print(f"  种群大小: {stats['population_size']}")
            print(f"  物种数量: {stats['species_stats']['count']}")
    
    # 获取最佳个体
    best_genome = evolution.get_best_genome()
    if best_genome:
        print(f"\n最佳个体信息:")
        print(f"- 适应度: {best_genome.fitness:.4f}")
        print(f"- 道德参数: {best_genome.moral_parameters}")
        print(f"- 节点数量: {len(best_genome.node_genes)}")
        print(f"- 连接数量: {len(best_genome.connection_genes)}")
    
    print(f"\n进化完成! 最终最佳适应度: {max(best_fitness_history):.4f}")


def main():
    """主演示函数"""
    print("道德感知NPC行为系统 - 基础演示")
    print("本演示将展示系统的核心功能模块")
    
    try:
        # 演示各个模块
        demonstrate_moral_framework()
        demonstrate_moral_contagion() 
        demonstrate_player_analysis()
        demonstrate_neuroevolution()
        
        print("\n" + "=" * 50)
        print("演示完成!")
        print("=" * 50)
        print("\n系统成功展示了以下核心功能:")
        print("1. ✅ 康德和功利主义道德框架计算")
        print("2. ✅ NPC间道德传染机制")
        print("3. ✅ 玩家行为分析和道德建模")
        print("4. ✅ 神经进化算法优化NPC行为")
        
        print(f"\n这个系统为游戏AI、教育工具和社会科学研究")
        print(f"提供了强大的道德推理和行为适应能力。")
        
    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")
        print("这可能是由于缺少依赖库导致的。")
        print("请确保安装了所有必要的依赖: numpy, networkx")


if __name__ == "__main__":
    main()