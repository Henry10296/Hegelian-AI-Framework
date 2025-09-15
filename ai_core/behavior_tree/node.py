# -*- coding: utf-8 -*-
"""
行为树框架 - 节点基类

定义了所有行为树节点（Node）的通用接口和状态。
"""

from enum import Enum

class NodeStatus(Enum):
    """定义了行为树节点的执行状态"""
    SUCCESS = 1  # 成功
    FAILURE = 2  # 失败
    RUNNING = 3  # 运行中

class Node:
    """
    所有行为树节点的抽象基类。
    """
    def __init__(self, name: str):
        self.name = name

    def tick(self, agent: 'EthicalAgent') -> NodeStatus:
        """
        每个节点都必须实现的主要方法。
        它包含了节点的执行逻辑，并在每个“心跳”中被调用。

        Args:
            agent: 执行此行为树的AI智能体。

        Returns:
            节点的执行状态 (SUCCESS, FAILURE, RUNNING)。
        """
        raise NotImplementedError("Subclasses must implement the tick() method.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}')"
