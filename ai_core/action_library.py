# -*- coding: utf-8 -*-
"""
AI行动库 (已为社会交互重构)

这个库现在包含一个能够在行动后广播“道德事件”的核心执行器。
"""

from .behavior_tree.leafs import Action
from .behavior_tree.node import NodeStatus
from typing import TYPE_CHECKING

# 避免循环导入
if TYPE_CHECKING:
    from .ethical_reasoning_framework import EthicalAgent

class ActionExecuteChosen(Action):
    """
    行动：执行由核心决策系统最终选定的行动，并在之后广播一个道德消息。
    """
    def on_tick(self, agent: 'EthicalAgent') -> NodeStatus:
        if agent.chosen_action:
            action_to_execute = agent.chosen_action
            print(f"   ⚡️ [行动执行] {agent.name} 根据其道德权衡，决定执行: '{action_to_execute.name}'")
            
            # 执行完毕后，清空已选定的行动
            agent.chosen_action = None
            
            # UPGRADED: 行动之后，向社会广播一个道德消息
            agent.broadcast_moral_message(action_to_execute)

            return NodeStatus.SUCCESS
        else:
            # 如果当前没有已选定的行动，则此节点无事可做
            return NodeStatus.FAILURE

class ActionIdle(Action):
    """
    行动：原地待命。
    """
    def on_tick(self, agent: 'EthicalAgent') -> NodeStatus:
        print(f"   [行动执行] {agent.name} 正在原地待命，观察四周。")
        return NodeStatus.SUCCESS
