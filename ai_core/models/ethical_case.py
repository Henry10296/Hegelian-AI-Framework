# -*- coding: utf-8 -*-
"""
Ethical Case Model - Represents an ethical dilemma or case to be processed
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from enum import Enum
from datetime import datetime
import uuid

class CaseType(Enum):
    """Types of ethical cases"""
    GENERAL = "general"

class RelationshipType(Enum):
    """Defines the AI's relationship with a stakeholder."""
    SELF = "self"
    FRIEND = "friend"
    STRANGER = "stranger"
    ENEMY = "enemy"

@dataclass
class ActionOption:
    """
    Represents a possible action to take in an ethical case.

    The `metadata` field is a flexible dictionary used by the `moral_calculus` module
    to evaluate the action. It can contain keys such as:
    - 'utility_scores': Dict[str, float]
    - 'violates_rules': List[Dict[str, str]]
    - 'expresses_virtues': Dict[str, float]
    - 'uncertainty_score': float (0.0 to 1.0) - Represents the riskiness of the action.
    """
    name: str
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "metadata": self.metadata
        }

@dataclass
class Stakeholder:
    """Represents a stakeholder, now with a defined relationship to the AI."""
    name: str
    role: str
    interests: List[str]
    relationship: RelationshipType = RelationshipType.STRANGER
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "interests": self.interests,
            "relationship": self.relationship.value
        }

@dataclass
class EthicalCase:
    """
    Represents an ethical case or dilemma to be processed.
    """
    
    case_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    case_type: CaseType = CaseType.GENERAL
    
    stakeholders: List[Stakeholder] = field(default_factory=list)
    action_options: List[ActionOption] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_stakeholder(self, stakeholder: Stakeholder):
        self.stakeholders.append(stakeholder)

    def add_action_option(self, option: ActionOption):
        self.action_options.append(option)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "title": self.title,
            "description": self.description,
            "case_type": self.case_type.value,
            "stakeholders": [s.to_dict() for s in self.stakeholders],
            "action_options": [opt.to_dict() for opt in self.action_options],
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EthicalCase':
        case = cls(
            case_id=data.get("case_id", str(uuid.uuid4())),
            title=data.get("title", ""),
            description=data.get("description", ""),
            case_type=CaseType(data.get("case_type", "general")),
            metadata=data.get("metadata", {})
        )
        
        if "created_at" in data:
            case.created_at = datetime.fromisoformat(data["created_at"])
        
        for stakeholder_data in data.get("stakeholders", []):
            rel_str = stakeholder_data.pop("relationship", "stranger")
            stakeholder_data["relationship"] = RelationshipType(rel_str)
            case.add_stakeholder(Stakeholder(**stakeholder_data))

        for option_data in data.get("action_options", []):
            case.add_action_option(ActionOption(**option_data))
        
        return case
