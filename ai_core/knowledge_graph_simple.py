"""
Simplified Knowledge Graph Manager - Basic implementation for dialectical reasoning
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from .models.ethical_case import EthicalCase, CaseType, CulturalContext

logger = logging.getLogger(__name__)

@dataclass
class KnowledgeNode:
    """Represents a node in the knowledge graph"""
    node_id: str
    labels: List[str]
    properties: Dict[str, Any]
    
    def __post_init__(self):
        if not self.properties:
            self.properties = {}

class SimpleKnowledgeGraphManager:
    """
    Simplified knowledge graph manager using in-memory storage
    This is a basic implementation to support the dialectical engine
    """
    
    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.relationships: List[Dict[str, Any]] = []
        
        # Initialize with basic ethical knowledge
        self._initialize_basic_knowledge()
        
        logger.info("Simple Knowledge Graph Manager initialized")
    
    def _initialize_basic_knowledge(self):
        """Initialize with basic ethical principles and knowledge"""
        
        # Core ethical principles
        principles = [
            {
                "id": "autonomy",
                "name": "Autonomy",
                "description": "Respect for individual self-determination and freedom of choice",
                "weight": 0.8,
                "cultural_context": "universal"
            },
            {
                "id": "beneficence",
                "name": "Beneficence",
                "description": "Acting in the best interest of others and promoting well-being",
                "weight": 0.9,
                "cultural_context": "universal"
            },
            {
                "id": "non_maleficence",
                "name": "Non-maleficence",
                "description": "Do no harm - avoiding actions that cause harm",
                "weight": 0.95,
                "cultural_context": "universal"
            },
            {
                "id": "justice",
                "name": "Justice",
                "description": "Fair distribution of benefits, risks, and costs",
                "weight": 0.85,
                "cultural_context": "universal"
            },
            {
                "id": "privacy",
                "name": "Privacy",
                "description": "Right to control personal information and maintain confidentiality",
                "weight": 0.7,
                "cultural_context": "western"
            },
            {
                "id": "transparency",
                "name": "Transparency",
                "description": "Openness and clarity in decision-making processes",
                "weight": 0.75,
                "cultural_context": "universal"
            },
            {
                "id": "accountability",
                "name": "Accountability",
                "description": "Responsibility for actions and their consequences",
                "weight": 0.8,
                "cultural_context": "universal"
            },
            {
                "id": "dignity",
                "name": "Human Dignity",
                "description": "Inherent worth and respect for all human beings",
                "weight": 0.9,
                "cultural_context": "universal"
            },
            {
                "id": "collective_harmony",
                "name": "Collective Harmony",
                "description": "Maintaining social cohesion and group well-being",
                "weight": 0.8,
                "cultural_context": "eastern"
            },
            {
                "id": "ubuntu",
                "name": "Ubuntu",
                "description": "I am because we are - interconnectedness of humanity",
                "weight": 0.85,
                "cultural_context": "african"
            }
        ]
        
        # Add principle nodes
        for principle in principles:
            node = KnowledgeNode(
                node_id=principle["id"],
                labels=["EthicalPrinciple"],
                properties=principle
            )
            self.nodes[principle["id"]] = node
        
        # Case-specific knowledge
        case_knowledge = [
            {
                "id": "medical_ethics",
                "name": "Medical Ethics",
                "description": "Ethical principles specific to medical practice",
                "domain": "medical",
                "principles": ["autonomy", "beneficence", "non_maleficence", "justice"]
            },
            {
                "id": "ai_ethics",
                "name": "AI Ethics",
                "description": "Ethical principles for artificial intelligence systems",
                "domain": "ai_governance",
                "principles": ["transparency", "accountability", "privacy", "justice"]
            },
            {
                "id": "autonomous_vehicle_ethics",
                "name": "Autonomous Vehicle Ethics",
                "description": "Ethical considerations for self-driving vehicles",
                "domain": "autonomous_vehicle",
                "principles": ["non_maleficence", "justice", "accountability", "transparency"]
            }
        ]
        
        # Add domain knowledge nodes
        for knowledge in case_knowledge:
            node = KnowledgeNode(
                node_id=knowledge["id"],
                labels=["DomainKnowledge"],
                properties=knowledge
            )
            self.nodes[knowledge["id"]] = node
    
    async def query(self, case: EthicalCase) -> List[KnowledgeNode]:
        """Query the knowledge graph for nodes relevant to the case"""
        relevant_nodes = []
        
        # Find domain-specific knowledge
        for node in self.nodes.values():
            if self._is_relevant_to_case(node, case):
                relevant_nodes.append(node)
        
        # Sort by relevance
        relevant_nodes.sort(
            key=lambda x: self._calculate_relevance_score(x, case),
            reverse=True
        )
        
        return relevant_nodes
    
    def _is_relevant_to_case(self, node: KnowledgeNode, case: EthicalCase) -> bool:
        """Check if a node is relevant to the case"""
        # Check if it's an ethical principle
        if "EthicalPrinciple" in node.labels:
            # Check cultural context
            node_culture = node.properties.get("cultural_context", "universal")
            if node_culture in ["universal", case.cultural_context.value]:
                return True
        
        # Check if it's domain knowledge
        if "DomainKnowledge" in node.labels:
            node_domain = node.properties.get("domain", "")
            if node_domain == case.case_type.value:
                return True
        
        return False
    
    def _calculate_relevance_score(self, node: KnowledgeNode, case: EthicalCase) -> float:
        """Calculate relevance score for a node"""
        score = 0.0
        
        # Base score for ethical principles
        if "EthicalPrinciple" in node.labels:
            score += 1.0
            
            # Cultural context bonus
            node_culture = node.properties.get("cultural_context", "universal")
            if node_culture == case.cultural_context.value:
                score += 0.5
            elif node_culture == "universal":
                score += 0.3
            
            # Weight from node properties
            node_weight = node.properties.get("weight", 0.5)
            score += node_weight * 0.5
        
        # Domain knowledge bonus
        if "DomainKnowledge" in node.labels:
            node_domain = node.properties.get("domain", "")
            if node_domain == case.case_type.value:
                score += 2.0  # High relevance for domain match
        
        # Complexity adjustment
        complexity_multiplier = {
            "low": 1.0,
            "medium": 0.9,
            "high": 0.8,
            "extreme": 0.7
        }
        score *= complexity_multiplier.get(case.complexity.value, 0.8)
        
        return score
    
    async def add_case_insights(self, case: EthicalCase, decision_result):
        """Add insights from processed case to the knowledge graph"""
        try:
            # Create a case node
            case_node = KnowledgeNode(
                node_id=f"case_{case.case_id}",
                labels=["ProcessedCase"],
                properties={
                    "case_id": case.case_id,
                    "title": case.title,
                    "case_type": case.case_type.value,
                    "complexity": case.complexity.value,
                    "cultural_context": case.cultural_context.value,
                    "final_decision": decision_result.final_decision,
                    "confidence_score": decision_result.confidence_score,
                    "processing_time": decision_result.processing_time,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            self.nodes[case_node.node_id] = case_node
            
            # Create relationships to relevant principles
            if hasattr(decision_result, 'thesis_result') and decision_result.thesis_result:
                for principle in decision_result.thesis_result.key_principles:
                    relationship = {
                        "from_node": case_node.node_id,
                        "to_node": principle.name.lower().replace(" ", "_"),
                        "relationship_type": "USED_PRINCIPLE",
                        "weight": principle.weight,
                        "relevance_score": principle.relevance_score
                    }
                    self.relationships.append(relationship)
            
            logger.info(f"Added case insights for {case.case_id} to knowledge graph")
            
        except Exception as e:
            logger.error(f"Error adding case insights: {e}")
    
    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """Get a specific node by ID"""
        return self.nodes.get(node_id)
    
    def get_all_nodes(self) -> List[KnowledgeNode]:
        """Get all nodes in the knowledge graph"""
        return list(self.nodes.values())
    
    def get_nodes_by_label(self, label: str) -> List[KnowledgeNode]:
        """Get all nodes with a specific label"""
        return [node for node in self.nodes.values() if label in node.labels]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge graph statistics"""
        return {
            "total_nodes": len(self.nodes),
            "total_relationships": len(self.relationships),
            "node_types": {
                "EthicalPrinciple": len(self.get_nodes_by_label("EthicalPrinciple")),
                "DomainKnowledge": len(self.get_nodes_by_label("DomainKnowledge")),
                "ProcessedCase": len(self.get_nodes_by_label("ProcessedCase"))
            }
        }
    
    def is_healthy(self) -> bool:
        """Check if the knowledge graph is healthy"""
        return len(self.nodes) > 0
    
    async def shutdown(self):
        """Shutdown the knowledge graph manager"""
        logger.info("Simple Knowledge Graph Manager shutting down")
        # In a real implementation, this would save state to persistent storage