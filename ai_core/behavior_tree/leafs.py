# -*- coding: utf-8 -*-
"""
行为树框架 - 叶子节点

定义了行为树的末端执行单元，即行动（Action）和条件（Condition）。
"""

from .node import Node, NodeStatus

class Action(Node):
    """
    行动节点（Action）。
    
    代表一个AI可以执行的具体动作。子类需要重写 on_tick() 方法。
    """
    def tick(self, agent: 'EthicalAgent') -> NodeStatus:
        return self.on_tick(agent)

    def on_tick(self, agent: 'EthicalAgent') -> NodeStatus:
        """子类需要实现这个方法来定义具体的行动逻辑。"""
        raise NotImplementedError("Action subclasses must implement the on_tick() method.")

class Condition(Node):
    """
    条件节点（Condition）。
    
    代表一个对世界状态或AI自身状态的检查。
    如果条件为真，返回SUCCESS；否则返回FAILURE。
    子类需要重写 check() 方法。
    """
    def tick(self, agent: 'EthicalAgent') -> NodeStatus:
        if self.check(agent):
            return NodeStatus.SUCCESS
        else:
            return NodeStatus.FAILURE

    def check(self, agent: 'EthicalAgent') -> bool:
        """子类需要实现这个方法来定义具体的条件检查逻辑。"""
        raise NotImplementedError("Condition subclasses must implement the check() method.")
