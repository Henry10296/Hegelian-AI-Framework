"""
Hegelian AI Framework - AI Core Module

This module provides the core AI functionality for dialectical reasoning
and ethical decision making using Hegelian dialectics.
"""

# Core AI Entity System
from .entities import (
    AIEntity,
    AIConfiguration,
    AIPersonalityType,
    ThinkingStyle,
    ThoughtProcess,
    ConsciousnessState,
    SelfAwarenessModule,
    AIEntityManager
)

# Thought Visualization
from .visualization import (
    ThoughtVisualizer,
    VisualizationFrame
)

# Dialectical Engine
from .dialectical_engine import (
    DialecticalEngine,
    DialecticalStage,
    DialecticalProcess
)

# Models
from .models import (
    EthicalCase,
    DecisionResult,
    ThesisResult,
    AntithesisResult,
    SynthesisResult
)

__all__ = [
    # AI Entity System
    'AIEntity',
    'AIConfiguration',
    'AIPersonalityType',
    'ThinkingStyle',
    'ThoughtProcess',
    'ConsciousnessState',
    'SelfAwarenessModule',
    'AIEntityManager',
    
    # Visualization
    'ThoughtVisualizer',
    'VisualizationFrame',
    
    # Dialectical Engine
    'DialecticalEngine',
    'DialecticalStage',
    'DialecticalProcess',
    
    # Models
    'EthicalCase',
    'DecisionResult', 
    'ThesisResult',
    'AntithesisResult',
    'SynthesisResult'
]