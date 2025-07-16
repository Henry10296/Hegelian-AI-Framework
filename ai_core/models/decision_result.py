"""
Decision Result Models - Represents the results of dialectical reasoning
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime
import json

class DecisionType(Enum):
    """Types of decisions"""
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"
    DEFER = "defer"
    ESCALATE = "escalate"

class ConfidenceLevel(Enum):
    """Confidence levels for decisions"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class EthicalPrinciple:
    """Represents an ethical principle"""
    name: str
    description: str
    weight: float
    relevance_score: float
    cultural_adaptation: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "weight": self.weight,
            "relevance_score": self.relevance_score,
            "cultural_adaptation": self.cultural_adaptation
        }

@dataclass
class ReasoningStep:
    """Represents a step in the reasoning process"""
    step_number: int
    description: str
    inputs: List[str]
    outputs: List[str]
    confidence: float
    reasoning_type: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_number": self.step_number,
            "description": self.description,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "confidence": self.confidence,
            "reasoning_type": self.reasoning_type
        }

@dataclass
class ThesisResult:
    """
    Result of the thesis stage - analysis of current ethical norms
    """
    case_id: str
    key_principles: List[EthicalPrinciple]
    applicable_norms: List[str]
    precedent_cases: List[str]
    confidence: float
    reasoning_path: List[ReasoningStep]
    cultural_considerations: List[str] = field(default_factory=list)
    temporal_factors: List[str] = field(default_factory=list)
    stakeholder_analysis: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "key_principles": [p.to_dict() for p in self.key_principles],
            "applicable_norms": self.applicable_norms,
            "precedent_cases": self.precedent_cases,
            "confidence": self.confidence,
            "reasoning_path": [r.to_dict() for r in self.reasoning_path],
            "cultural_considerations": self.cultural_considerations,
            "temporal_factors": self.temporal_factors,
            "stakeholder_analysis": self.stakeholder_analysis
        }

@dataclass
class EthicalChallenge:
    """Represents an ethical challenge or opposition"""
    challenge_type: str
    description: str
    strength: float
    counter_arguments: List[str]
    affected_stakeholders: List[str]
    cultural_source: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "challenge_type": self.challenge_type,
            "description": self.description,
            "strength": self.strength,
            "counter_arguments": self.counter_arguments,
            "affected_stakeholders": self.affected_stakeholders,
            "cultural_source": self.cultural_source
        }

@dataclass
class ConflictScenario:
    """Represents a conflict scenario"""
    scenario_id: str
    description: str
    conflicting_values: List[str]
    potential_outcomes: List[str]
    likelihood: float
    impact_severity: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "description": self.description,
            "conflicting_values": self.conflicting_values,
            "potential_outcomes": self.potential_outcomes,
            "likelihood": self.likelihood,
            "impact_severity": self.impact_severity
        }

@dataclass
class AntithesisResult:
    """
    Result of the antithesis stage - opposing viewpoints and challenges
    """
    case_id: str
    challenges: List[EthicalChallenge]
    alternative_perspectives: List[str]
    conflicts: List[ConflictScenario]
    devil_advocate_arguments: List[str]
    strength: float
    cultural_variations: Dict[str, List[str]] = field(default_factory=dict)
    minority_positions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "challenges": [c.to_dict() for c in self.challenges],
            "alternative_perspectives": self.alternative_perspectives,
            "conflicts": [c.to_dict() for c in self.conflicts],
            "devil_advocate_arguments": self.devil_advocate_arguments,
            "strength": self.strength,
            "cultural_variations": self.cultural_variations,
            "minority_positions": self.minority_positions
        }

@dataclass
class ResolutionStrategy:
    """Represents a strategy for resolving dialectical tension"""
    strategy_type: str
    description: str
    steps: List[str]
    expected_outcomes: List[str]
    success_probability: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy_type": self.strategy_type,
            "description": self.description,
            "steps": self.steps,
            "expected_outcomes": self.expected_outcomes,
            "success_probability": self.success_probability
        }

@dataclass
class IntegratedPrinciple:
    """Represents an integrated ethical principle from synthesis"""
    name: str
    description: str
    source_principles: List[str]
    integration_method: str
    weight: float
    consensus_level: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "source_principles": self.source_principles,
            "integration_method": self.integration_method,
            "weight": self.weight,
            "consensus_level": self.consensus_level
        }

@dataclass
class SynthesisResult:
    """
    Result of the synthesis stage - integration and resolution
    """
    case_id: str
    decision: str
    integrated_principles: List[IntegratedPrinciple]
    resolution_strategy: ResolutionStrategy
    confidence: float
    consensus_score: float
    trade_offs: List[str]
    implementation_guidelines: List[str]
    monitoring_requirements: List[str] = field(default_factory=list)
    fallback_options: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "decision": self.decision,
            "integrated_principles": [p.to_dict() for p in self.integrated_principles],
            "resolution_strategy": self.resolution_strategy.to_dict(),
            "confidence": self.confidence,
            "consensus_score": self.consensus_score,
            "trade_offs": self.trade_offs,
            "implementation_guidelines": self.implementation_guidelines,
            "monitoring_requirements": self.monitoring_requirements,
            "fallback_options": self.fallback_options
        }

@dataclass
class DecisionResult:
    """
    Final result of the dialectical decision process
    """
    case_id: str
    thesis_result: ThesisResult
    antithesis_result: AntithesisResult
    synthesis_result: SynthesisResult
    final_decision: str
    confidence_score: float
    reasoning_path: List[Dict[str, Any]]
    processing_time: float
    decision_type: DecisionType = DecisionType.APPROVE
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Additional analysis
    ethical_impact_assessment: Dict[str, Any] = field(default_factory=dict)
    stakeholder_impact_analysis: Dict[str, Any] = field(default_factory=dict)
    risk_assessment: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_confidence_level(self) -> ConfidenceLevel:
        """Get confidence level based on confidence score"""
        if self.confidence_score >= 0.9:
            return ConfidenceLevel.VERY_HIGH
        elif self.confidence_score >= 0.7:
            return ConfidenceLevel.HIGH
        elif self.confidence_score >= 0.5:
            return ConfidenceLevel.MEDIUM
        elif self.confidence_score >= 0.3:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the decision result"""
        return {
            "case_id": self.case_id,
            "final_decision": self.final_decision,
            "decision_type": self.decision_type.value,
            "confidence_score": self.confidence_score,
            "confidence_level": self.get_confidence_level().value,
            "processing_time": self.processing_time,
            "key_principles": [p.name for p in self.thesis_result.key_principles],
            "main_challenges": [c.challenge_type for c in self.antithesis_result.challenges],
            "resolution_strategy": self.synthesis_result.resolution_strategy.strategy_type,
            "consensus_score": self.synthesis_result.consensus_score,
            "timestamp": self.timestamp.isoformat()
        }
    
    def get_explainability_report(self) -> Dict[str, Any]:
        """Generate an explainability report"""
        return {
            "case_id": self.case_id,
            "decision_overview": {
                "final_decision": self.final_decision,
                "confidence": self.confidence_score,
                "processing_time": self.processing_time
            },
            "reasoning_process": {
                "thesis_stage": {
                    "key_principles": [p.name for p in self.thesis_result.key_principles],
                    "confidence": self.thesis_result.confidence,
                    "reasoning_steps": len(self.thesis_result.reasoning_path)
                },
                "antithesis_stage": {
                    "challenges_identified": len(self.antithesis_result.challenges),
                    "strength": self.antithesis_result.strength,
                    "conflicts": len(self.antithesis_result.conflicts)
                },
                "synthesis_stage": {
                    "integrated_principles": len(self.synthesis_result.integrated_principles),
                    "consensus_score": self.synthesis_result.consensus_score,
                    "resolution_strategy": self.synthesis_result.resolution_strategy.strategy_type
                }
            },
            "detailed_reasoning": self.reasoning_path,
            "impact_assessment": {
                "ethical_impact": self.ethical_impact_assessment,
                "stakeholder_impact": self.stakeholder_impact_analysis,
                "risk_assessment": self.risk_assessment
            },
            "implementation": {
                "guidelines": self.synthesis_result.implementation_guidelines,
                "monitoring": self.synthesis_result.monitoring_requirements,
                "fallback_options": self.synthesis_result.fallback_options
            }
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "case_id": self.case_id,
            "thesis_result": self.thesis_result.to_dict(),
            "antithesis_result": self.antithesis_result.to_dict(),
            "synthesis_result": self.synthesis_result.to_dict(),
            "final_decision": self.final_decision,
            "confidence_score": self.confidence_score,
            "reasoning_path": self.reasoning_path,
            "processing_time": self.processing_time,
            "decision_type": self.decision_type.value,
            "timestamp": self.timestamp.isoformat(),
            "ethical_impact_assessment": self.ethical_impact_assessment,
            "stakeholder_impact_analysis": self.stakeholder_impact_analysis,
            "risk_assessment": self.risk_assessment,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DecisionResult':
        """Create from dictionary"""
        # Parse thesis result
        thesis_data = data["thesis_result"]
        thesis_result = ThesisResult(
            case_id=thesis_data["case_id"],
            key_principles=[EthicalPrinciple(**p) for p in thesis_data["key_principles"]],
            applicable_norms=thesis_data["applicable_norms"],
            precedent_cases=thesis_data["precedent_cases"],
            confidence=thesis_data["confidence"],
            reasoning_path=[ReasoningStep(**r) for r in thesis_data["reasoning_path"]],
            cultural_considerations=thesis_data.get("cultural_considerations", []),
            temporal_factors=thesis_data.get("temporal_factors", []),
            stakeholder_analysis=thesis_data.get("stakeholder_analysis", {})
        )
        
        # Parse antithesis result
        antithesis_data = data["antithesis_result"]
        antithesis_result = AntithesisResult(
            case_id=antithesis_data["case_id"],
            challenges=[EthicalChallenge(**c) for c in antithesis_data["challenges"]],
            alternative_perspectives=antithesis_data["alternative_perspectives"],
            conflicts=[ConflictScenario(**c) for c in antithesis_data["conflicts"]],
            devil_advocate_arguments=antithesis_data["devil_advocate_arguments"],
            strength=antithesis_data["strength"],
            cultural_variations=antithesis_data.get("cultural_variations", {}),
            minority_positions=antithesis_data.get("minority_positions", [])
        )
        
        # Parse synthesis result
        synthesis_data = data["synthesis_result"]
        synthesis_result = SynthesisResult(
            case_id=synthesis_data["case_id"],
            decision=synthesis_data["decision"],
            integrated_principles=[IntegratedPrinciple(**p) for p in synthesis_data["integrated_principles"]],
            resolution_strategy=ResolutionStrategy(**synthesis_data["resolution_strategy"]),
            confidence=synthesis_data["confidence"],
            consensus_score=synthesis_data["consensus_score"],
            trade_offs=synthesis_data["trade_offs"],
            implementation_guidelines=synthesis_data["implementation_guidelines"],
            monitoring_requirements=synthesis_data.get("monitoring_requirements", []),
            fallback_options=synthesis_data.get("fallback_options", [])
        )
        
        # Create decision result
        result = cls(
            case_id=data["case_id"],
            thesis_result=thesis_result,
            antithesis_result=antithesis_result,
            synthesis_result=synthesis_result,
            final_decision=data["final_decision"],
            confidence_score=data["confidence_score"],
            reasoning_path=data["reasoning_path"],
            processing_time=data["processing_time"],
            decision_type=DecisionType(data.get("decision_type", "approve")),
            ethical_impact_assessment=data.get("ethical_impact_assessment", {}),
            stakeholder_impact_analysis=data.get("stakeholder_impact_analysis", {}),
            risk_assessment=data.get("risk_assessment", {}),
            metadata=data.get("metadata", {})
        )
        
        # Parse timestamp
        if "timestamp" in data:
            result.timestamp = datetime.fromisoformat(data["timestamp"])
        
        return result
    
    @classmethod
    def from_json(cls, json_str: str) -> 'DecisionResult':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)