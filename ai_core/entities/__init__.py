"""
AI Entities Package - Contains AI entity related classes
"""

from .ai_entity import (
    AIEntity,
    AIConfiguration,
    AIPersonalityType,
    ThinkingStyle,
    ThoughtProcess,
    ConsciousnessState,
    SelfAwarenessModule
)

from .ai_entity_manager import AIEntityManager

__all__ = [
    'AIEntity',
    'AIConfiguration', 
    'AIPersonalityType',
    'ThinkingStyle',
    'ThoughtProcess',
    'ConsciousnessState',
    'SelfAwarenessModule',
    'AIEntityManager'
]