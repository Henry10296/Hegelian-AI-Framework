"""
AI Core Models Package
"""

from .ethical_case import (
    EthicalCase,
    Stakeholder,
    EthicalDimension,
    ContextualFactor,
    CaseType,
    ComplexityLevel,
    CulturalContext
)

from .decision_result import (
    DecisionResult,
    ThesisResult,
    AntithesisResult,
    SynthesisResult,
    EthicalPrinciple,
    ReasoningStep,
    EthicalChallenge,
    ConflictScenario,
    ResolutionStrategy,
    IntegratedPrinciple,
    DecisionType,
    ConfidenceLevel
)

__all__ = [
    # Main classes
    'EthicalCase',
    'DecisionResult',
    'ThesisResult',
    'AntithesisResult',
    'SynthesisResult',
    
    # Ethical case components
    'Stakeholder',
    'EthicalDimension',
    'ContextualFactor',
    
    # Enums
    'CaseType',
    'ComplexityLevel',
    'CulturalContext',
    'DecisionType',
    'ConfidenceLevel',
    
    # Decision result components
    'EthicalPrinciple',
    'ReasoningStep',
    'EthicalChallenge',
    'ConflictScenario',
    'ResolutionStrategy',
    'IntegratedPrinciple'
]