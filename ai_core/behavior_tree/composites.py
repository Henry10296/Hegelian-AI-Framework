# -*- coding: utf-8 -*-
"""
行为树框架 - 组合节点

定义了用于控制行为流程的组合节点，如序列（Sequence）和选择器（Selector）。
"""

from typing import List
from .node import Node, NodeStatus

class Composite(Node):
    """组合节点的基类，可以包含多个子节点。"""
    def __init__(self, name: str, children: List[Node]):
        super().__init__(name)
        self.children = children

class Sequence(Composite):
    """
    序列节点（Sequence）。

    按顺序执行其子节点。只要有一个子节点返回FAILURE，它就立刻返回FAILURE。
    只有当所有子节点都返回SUCCESS时，它才返回SUCCESS。
    如果一个子节点返回RUNNING，它也会立刻返回RUNNING，并在下一个心跳周期从该子节点继续。
    """
    def tick(self, agent: 'EthicalAgent') -> NodeStatus:
        for child in self.children:
            status = child.tick(agent)
            if status != NodeStatus.SUCCESS:
                # 如果子节点失败或正在运行，则序列节点也返回该状态
                return status
        # 所有子节点都成功了
        return NodeStatus.SUCCESS

class Selector(Composite):
    """
    选择器节点（Selector）。

    按顺序执行其子节点。只要有一个子节点返回SUCCESS，它就立刻返回SUCCESS。
    只有当所有子节点都返回FAILURE时，它才返回FAILURE。
    如果一个子节点返回RUNNING，它也会立刻返回RUNNING，并在下一个心跳周期从该子节点继续。
    """
    def tick(self, agent: 'EthicalAgent') -> NodeStatus:
        for child in self.children:
            status = child.tick(agent)
            if status != NodeStatus.FAILURE:
                # 如果子节点成功或正在运行，则选择器节点也返回该状态
                return status
        # 所有子节点都失败了
        return NodeStatus.FAILURE
