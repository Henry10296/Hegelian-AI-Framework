"""
Ethical Case Model - Represents an ethical dilemma or case to be processed
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime
import json
import uuid

class CaseType(Enum):
    """Types of ethical cases"""
    MEDICAL = "medical"
    AUTONOMOUS_VEHICLE = "autonomous_vehicle"
    AI_GOVERNANCE = "ai_governance"
    BUSINESS_ETHICS = "business_ethics"
    ENVIRONMENTAL = "environmental"
    SOCIAL_JUSTICE = "social_justice"
    PRIVACY = "privacy"
    RESEARCH_ETHICS = "research_ethics"
    GENERAL = "general"

class ComplexityLevel(Enum):
    """Complexity levels of ethical cases"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"

class CulturalContext(Enum):
    """Cultural context for ethical evaluation"""
    WESTERN = "western"
    EASTERN = "eastern"
    ISLAMIC = "islamic"
    AFRICAN = "african"
    INDIGENOUS = "indigenous"
    MULTICULTURAL = "multicultural"
    UNIVERSAL = "universal"

@dataclass
class Stakeholder:
    """Represents a stakeholder in an ethical case"""
    name: str
    role: str
    interests: List[str]
    power_level: float  # 0.0 to 1.0
    impact_level: float  # 0.0 to 1.0
    ethical_stance: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "interests": self.interests,
            "power_level": self.power_level,
            "impact_level": self.impact_level,
            "ethical_stance": self.ethical_stance
        }

@dataclass
class EthicalDimension:
    """Represents an ethical dimension of a case"""
    name: str
    description: str
    weight: float  # 0.0 to 1.0
    values: List[str]
    conflicts: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "weight": self.weight,
            "values": self.values,
            "conflicts": self.conflicts
        }

@dataclass
class ContextualFactor:
    """Represents contextual factors affecting the case"""
    factor_type: str
    description: str
    influence_level: float  # 0.0 to 1.0
    positive_impact: bool
    related_principles: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "factor_type": self.factor_type,
            "description": self.description,
            "influence_level": self.influence_level,
            "positive_impact": self.positive_impact,
            "related_principles": self.related_principles
        }

@dataclass
class EthicalCase:
    """
    Represents an ethical case or dilemma to be processed by the dialectical engine
    """
    
    # Basic information
    case_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    case_type: CaseType = CaseType.GENERAL
    complexity: ComplexityLevel = ComplexityLevel.MEDIUM
    cultural_context: CulturalContext = CulturalContext.UNIVERSAL
    
    # Stakeholders and dimensions
    stakeholders: List[Stakeholder] = field(default_factory=list)
    ethical_dimensions: List[EthicalDimension] = field(default_factory=list)
    contextual_factors: List[ContextualFactor] = field(default_factory=list)
    
    # Decision options
    available_options: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    
    # Temporal aspects
    time_sensitivity: float = 0.5  # 0.0 to 1.0
    long_term_impact: float = 0.5  # 0.0 to 1.0
    
    # Uncertainty and ambiguity
    uncertainty_level: float = 0.5  # 0.0 to 1.0
    ambiguity_level: float = 0.5   # 0.0 to 1.0
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    related_cases: List[str] = field(default_factory=list)
    
    # Additional data
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_stakeholder(self, stakeholder: Stakeholder):
        """Add a stakeholder to the case"""
        self.stakeholders.append(stakeholder)
    
    def add_ethical_dimension(self, dimension: EthicalDimension):
        """Add an ethical dimension to the case"""
        self.ethical_dimensions.append(dimension)
    
    def add_contextual_factor(self, factor: ContextualFactor):
        """Add a contextual factor to the case"""
        self.contextual_factors.append(factor)
    
    def get_primary_stakeholders(self) -> List[Stakeholder]:
        """Get stakeholders with high power or impact"""
        return [s for s in self.stakeholders if s.power_level > 0.7 or s.impact_level > 0.7]
    
    def get_key_ethical_dimensions(self) -> List[EthicalDimension]:
        """Get ethical dimensions with high weight"""
        return [d for d in self.ethical_dimensions if d.weight > 0.7]
    
    def get_complexity_score(self) -> float:
        """Calculate a complexity score for the case"""
        base_complexity = {
            ComplexityLevel.LOW: 0.25,
            ComplexityLevel.MEDIUM: 0.5,
            ComplexityLevel.HIGH: 0.75,
            ComplexityLevel.EXTREME: 1.0
        }[self.complexity]
        
        # Adjust based on other factors
        stakeholder_complexity = min(len(self.stakeholders) / 10, 1.0)
        dimension_complexity = min(len(self.ethical_dimensions) / 5, 1.0)
        uncertainty_factor = (self.uncertainty_level + self.ambiguity_level) / 2
        
        return min((base_complexity + stakeholder_complexity + dimension_complexity + uncertainty_factor) / 4, 1.0)
    
    def get_ethical_tensions(self) -> List[str]:
        """Identify potential ethical tensions in the case"""
        tensions = []
        
        # Tensions from conflicting stakeholder interests
        for i, stakeholder1 in enumerate(self.stakeholders):
            for stakeholder2 in self.stakeholders[i+1:]:
                common_interests = set(stakeholder1.interests) & set(stakeholder2.interests)
                if not common_interests:
                    tensions.append(f"Conflicting interests between {stakeholder1.name} and {stakeholder2.name}")
        
        # Tensions from conflicting ethical dimensions
        for dimension in self.ethical_dimensions:
            if dimension.conflicts:
                tensions.extend(dimension.conflicts)
        
        return tensions
    
    def validate(self) -> List[str]:
        """Validate the case and return any validation errors"""
        errors = []
        
        if not self.title:
            errors.append("Case title is required")
        
        if not self.description:
            errors.append("Case description is required")
        
        if not self.stakeholders:
            errors.append("At least one stakeholder is required")
        
        if not self.ethical_dimensions:
            errors.append("At least one ethical dimension is required")
        
        if not self.available_options:
            errors.append("At least one available option is required")
        
        # Validate stakeholder data
        for i, stakeholder in enumerate(self.stakeholders):
            if not stakeholder.name:
                errors.append(f"Stakeholder {i+1} name is required")
            if not (0.0 <= stakeholder.power_level <= 1.0):
                errors.append(f"Stakeholder {i+1} power level must be between 0.0 and 1.0")
            if not (0.0 <= stakeholder.impact_level <= 1.0):
                errors.append(f"Stakeholder {i+1} impact level must be between 0.0 and 1.0")
        
        # Validate ethical dimensions
        for i, dimension in enumerate(self.ethical_dimensions):
            if not dimension.name:
                errors.append(f"Ethical dimension {i+1} name is required")
            if not (0.0 <= dimension.weight <= 1.0):
                errors.append(f"Ethical dimension {i+1} weight must be between 0.0 and 1.0")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the case to a dictionary"""
        return {
            "case_id": self.case_id,
            "title": self.title,
            "description": self.description,
            "case_type": self.case_type.value,
            "complexity": self.complexity.value,
            "cultural_context": self.cultural_context.value,
            "stakeholders": [s.to_dict() for s in self.stakeholders],
            "ethical_dimensions": [d.to_dict() for d in self.ethical_dimensions],
            "contextual_factors": [f.to_dict() for f in self.contextual_factors],
            "available_options": self.available_options,
            "constraints": self.constraints,
            "time_sensitivity": self.time_sensitivity,
            "long_term_impact": self.long_term_impact,
            "uncertainty_level": self.uncertainty_level,
            "ambiguity_level": self.ambiguity_level,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "tags": self.tags,
            "related_cases": self.related_cases,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert the case to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EthicalCase':
        """Create an EthicalCase from a dictionary"""
        # Parse basic fields
        case = cls(
            case_id=data.get("case_id", str(uuid.uuid4())),
            title=data.get("title", ""),
            description=data.get("description", ""),
            case_type=CaseType(data.get("case_type", "general")),
            complexity=ComplexityLevel(data.get("complexity", "medium")),
            cultural_context=CulturalContext(data.get("cultural_context", "universal")),
            available_options=data.get("available_options", []),
            constraints=data.get("constraints", []),
            time_sensitivity=data.get("time_sensitivity", 0.5),
            long_term_impact=data.get("long_term_impact", 0.5),
            uncertainty_level=data.get("uncertainty_level", 0.5),
            ambiguity_level=data.get("ambiguity_level", 0.5),
            created_by=data.get("created_by"),
            tags=data.get("tags", []),
            related_cases=data.get("related_cases", []),
            metadata=data.get("metadata", {})
        )
        
        # Parse timestamps
        if "created_at" in data:
            case.created_at = datetime.fromisoformat(data["created_at"])
        
        # Parse stakeholders
        for stakeholder_data in data.get("stakeholders", []):
            stakeholder = Stakeholder(
                name=stakeholder_data["name"],
                role=stakeholder_data["role"],
                interests=stakeholder_data["interests"],
                power_level=stakeholder_data["power_level"],
                impact_level=stakeholder_data["impact_level"],
                ethical_stance=stakeholder_data.get("ethical_stance")
            )
            case.add_stakeholder(stakeholder)
        
        # Parse ethical dimensions
        for dimension_data in data.get("ethical_dimensions", []):
            dimension = EthicalDimension(
                name=dimension_data["name"],
                description=dimension_data["description"],
                weight=dimension_data["weight"],
                values=dimension_data["values"],
                conflicts=dimension_data.get("conflicts", [])
            )
            case.add_ethical_dimension(dimension)
        
        # Parse contextual factors
        for factor_data in data.get("contextual_factors", []):
            factor = ContextualFactor(
                factor_type=factor_data["factor_type"],
                description=factor_data["description"],
                influence_level=factor_data["influence_level"],
                positive_impact=factor_data["positive_impact"],
                related_principles=factor_data.get("related_principles", [])
            )
            case.add_contextual_factor(factor)
        
        return case
    
    @classmethod
    def from_json(cls, json_str: str) -> 'EthicalCase':
        """Create an EthicalCase from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)