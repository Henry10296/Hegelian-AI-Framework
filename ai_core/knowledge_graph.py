"""
Knowledge Graph Manager for the Hegelian AI Framework
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from datetime import datetime
import json
import uuid

try:
    from neo4j import AsyncGraphDatabase
    from neo4j.exceptions import ServiceUnavailable, TransientError
    NEO4J_AVAILABLE = True
except ImportError:
    # 为了避免类型检查错误，创建虚拟类
    class AsyncGraphDatabase:
        @staticmethod
        def driver(uri: str, auth: tuple):
            return None
    
    class ServiceUnavailable(Exception):
        pass
    
    class TransientError(Exception):
        pass
    
    NEO4J_AVAILABLE = False

from .models.ethical_case import EthicalCase
from .models.decision_result import DecisionResult

logger = logging.getLogger(__name__)

class KnowledgeNode:
    """Represents a node in the knowledge graph"""
    
    def __init__(self, node_id: str, labels: List[str], properties: Dict[str, Any]):
        self.id = node_id
        self.labels = labels
        self.properties = properties
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "labels": self.labels,
            "properties": self.properties
        }

class KnowledgeRelationship:
    """Represents a relationship in the knowledge graph"""
    
    def __init__(self, rel_id: str, start_node: str, end_node: str, rel_type: str, properties: Dict[str, Any]):
        self.id = rel_id
        self.start_node = start_node
        self.end_node = end_node
        self.type = rel_type
        self.properties = properties
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "start_node": self.start_node,
            "end_node": self.end_node,
            "type": self.type,
            "properties": self.properties
        }

class MockKnowledgeGraph:
    """Mock knowledge graph for development without Neo4j"""
    
    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.relationships: Dict[str, KnowledgeRelationship] = {}
        self.node_index: Dict[str, Set[str]] = {}  # label -> set of node_ids
        self.relationship_index: Dict[str, Set[str]] = {}  # type -> set of rel_ids
        
        # Initialize with some sample ethical knowledge
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample ethical principles and concepts"""
        # Add sample ethical principles
        principles = [
            {"name": "Autonomy", "description": "Respect for individual self-determination"},
            {"name": "Beneficence", "description": "Acting in the best interest of others"},
            {"name": "Non-maleficence", "description": "Do no harm"},
            {"name": "Justice", "description": "Fair distribution of benefits and burdens"},
            {"name": "Transparency", "description": "Openness and explainability"},
            {"name": "Accountability", "description": "Responsibility for actions and decisions"},
            {"name": "Privacy", "description": "Protection of personal information"},
            {"name": "Fairness", "description": "Equal treatment and non-discrimination"}
        ]
        
        for principle in principles:
            node_id = str(uuid.uuid4())
            node = KnowledgeNode(
                node_id=node_id,
                labels=["EthicalPrinciple"],
                properties={
                    "name": principle["name"],
                    "description": principle["description"],
                    "weight": 1.0,
                    "cultural_context": "universal",
                    "created_at": datetime.now().isoformat()
                }
            )
            self.nodes[node_id] = node
            
            if "EthicalPrinciple" not in self.node_index:
                self.node_index["EthicalPrinciple"] = set()
            self.node_index["EthicalPrinciple"].add(node_id)
        
        # Add sample conflicts
        conflicts = [
            ("Autonomy", "Beneficence", "Individual choice vs. collective good"),
            ("Privacy", "Transparency", "Information protection vs. openness"),
            ("Justice", "Efficiency", "Fair distribution vs. optimal outcomes")
        ]
        
        for conflict in conflicts:
            # Find nodes by name
            principle1_node = None
            principle2_node = None
            
            for node in self.nodes.values():
                if node.properties.get("name") == conflict[0]:
                    principle1_node = node
                elif node.properties.get("name") == conflict[1]:
                    principle2_node = node
            
            if principle1_node and principle2_node:
                rel_id = str(uuid.uuid4())
                relationship = KnowledgeRelationship(
                    rel_id=rel_id,
                    start_node=principle1_node.id,
                    end_node=principle2_node.id,
                    rel_type="CONFLICTS_WITH",
                    properties={
                        "description": conflict[2],
                        "strength": 0.8,
                        "context": "general",
                        "created_at": datetime.now().isoformat()
                    }
                )
                self.relationships[rel_id] = relationship
                
                if "CONFLICTS_WITH" not in self.relationship_index:
                    self.relationship_index["CONFLICTS_WITH"] = set()
                self.relationship_index["CONFLICTS_WITH"].add(rel_id)
    
    async def query_by_labels(self, labels: List[str]) -> List[KnowledgeNode]:
        """Query nodes by labels"""
        result = []
        for label in labels:
            if label in self.node_index:
                for node_id in self.node_index[label]:
                    result.append(self.nodes[node_id])
        return result
    
    async def query_relationships(self, rel_type: str) -> List[KnowledgeRelationship]:
        """Query relationships by type"""
        result = []
        if rel_type in self.relationship_index:
            for rel_id in self.relationship_index[rel_type]:
                result.append(self.relationships[rel_id])
        return result
    
    async def find_connected_nodes(self, node_id: str, rel_type: Optional[str] = None) -> List[KnowledgeNode]:
        """Find nodes connected to a given node"""
        result = []
        for relationship in self.relationships.values():
            if rel_type and relationship.type != rel_type:
                continue
            
            if relationship.start_node == node_id:
                result.append(self.nodes[relationship.end_node])
            elif relationship.end_node == node_id:
                result.append(self.nodes[relationship.start_node])
        
        return result
    
    async def add_node(self, labels: List[str], properties: Dict[str, Any]) -> str:
        """Add a new node"""
        node_id = str(uuid.uuid4())
        node = KnowledgeNode(node_id, labels, properties)
        self.nodes[node_id] = node
        
        # Update indexes
        for label in labels:
            if label not in self.node_index:
                self.node_index[label] = set()
            self.node_index[label].add(node_id)
        
        return node_id
    
    async def add_relationship(self, start_node: str, end_node: str, rel_type: str, properties: Dict[str, Any]) -> str:
        """Add a new relationship"""
        rel_id = str(uuid.uuid4())
        relationship = KnowledgeRelationship(rel_id, start_node, end_node, rel_type, properties)
        self.relationships[rel_id] = relationship
        
        # Update index
        if rel_type not in self.relationship_index:
            self.relationship_index[rel_type] = set()
        self.relationship_index[rel_type].add(rel_id)
        
        return rel_id

class KnowledgeGraphManager:
    """
    Manager for the knowledge graph system
    """
    
    def __init__(self, neo4j_config: Dict[str, Any]):
        self.neo4j_config = neo4j_config
        self.driver: Optional[Any] = None
        self.mock_graph: Optional[MockKnowledgeGraph] = None
        self.use_mock = not NEO4J_AVAILABLE
        
        if self.use_mock:
            logger.warning("Neo4j not available, using mock knowledge graph")
            self.mock_graph = MockKnowledgeGraph()
        
        self._initialized = False
    
    async def initialize(self):
        """Initialize the knowledge graph connection"""
        try:
            if not self.use_mock:
                self.driver = AsyncGraphDatabase.driver(
                    self.neo4j_config["uri"],
                    auth=(self.neo4j_config["username"], self.neo4j_config["password"])
                )
                
                # Test connection
                await self._test_connection()
                
                # Initialize schema
                await self._initialize_schema()
                
                # Initialize with sample data if empty
                await self._initialize_sample_data_neo4j()
            
            self._initialized = True
            logger.info("Knowledge graph initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize knowledge graph: {e}")
            if not self.use_mock:
                logger.info("Falling back to mock knowledge graph")
                self.use_mock = True
                self.mock_graph = MockKnowledgeGraph()
                self._initialized = True
    
    async def _test_connection(self):
        """Test Neo4j connection"""
        if self.use_mock:
            return
        
        async with self.driver.session() as session:
            result = await session.run("RETURN 1 as test")
            record = await result.single()
            assert record["test"] == 1
    
    async def _initialize_schema(self):
        """Initialize Neo4j schema"""
        if self.use_mock:
            return
        
        schema_queries = [
            "CREATE CONSTRAINT ethical_principle_name IF NOT EXISTS FOR (p:EthicalPrinciple) REQUIRE p.name IS UNIQUE",
            "CREATE CONSTRAINT case_id IF NOT EXISTS FOR (c:EthicalCase) REQUIRE c.case_id IS UNIQUE",
            "CREATE INDEX ethical_principle_cultural_context IF NOT EXISTS FOR (p:EthicalPrinciple) ON (p.cultural_context)",
            "CREATE INDEX case_type IF NOT EXISTS FOR (c:EthicalCase) ON (c.case_type)",
            "CREATE INDEX relationship_type IF NOT EXISTS FOR ()-[r]-() ON (type(r))"
        ]
        
        async with self.driver.session() as session:
            for query in schema_queries:
                try:
                    await session.run(query)
                except Exception as e:
                    logger.warning(f"Schema query failed (may already exist): {e}")
    
    async def _initialize_sample_data_neo4j(self):
        """Initialize Neo4j with sample data"""
        if self.use_mock:
            return
        
        # Check if data already exists
        async with self.driver.session() as session:
            result = await session.run("MATCH (p:EthicalPrinciple) RETURN count(p) as count")
            record = await result.single()
            if record["count"] > 0:
                return  # Data already exists
        
        # Add sample principles
        principles = [
            {"name": "Autonomy", "description": "Respect for individual self-determination"},
            {"name": "Beneficence", "description": "Acting in the best interest of others"},
            {"name": "Non-maleficence", "description": "Do no harm"},
            {"name": "Justice", "description": "Fair distribution of benefits and burdens"},
            {"name": "Transparency", "description": "Openness and explainability"},
            {"name": "Accountability", "description": "Responsibility for actions and decisions"},
            {"name": "Privacy", "description": "Protection of personal information"},
            {"name": "Fairness", "description": "Equal treatment and non-discrimination"}
        ]
        
        async with self.driver.session() as session:
            for principle in principles:
                await session.run(
                    """
                    CREATE (p:EthicalPrinciple {
                        name: $name,
                        description: $description,
                        weight: 1.0,
                        cultural_context: 'universal',
                        created_at: datetime()
                    })
                    """,
                    name=principle["name"],
                    description=principle["description"]
                )
            
            # Add conflicts
            conflicts = [
                ("Autonomy", "Beneficence", "Individual choice vs. collective good"),
                ("Privacy", "Transparency", "Information protection vs. openness"),
                ("Justice", "Efficiency", "Fair distribution vs. optimal outcomes")
            ]
            
            for conflict in conflicts:
                await session.run(
                    """
                    MATCH (p1:EthicalPrinciple {name: $name1})
                    MATCH (p2:EthicalPrinciple {name: $name2})
                    CREATE (p1)-[:CONFLICTS_WITH {
                        description: $description,
                        strength: 0.8,
                        context: 'general',
                        created_at: datetime()
                    }]->(p2)
                    """,
                    name1=conflict[0],
                    name2=conflict[1],
                    description=conflict[2]
                )
    
    async def query(self, case: EthicalCase) -> List[KnowledgeNode]:
        """
        Query the knowledge graph for relevant knowledge
        
        Args:
            case: The ethical case to query for
            
        Returns:
            List of relevant knowledge nodes
        """
        if not self._initialized:
            await self.initialize()
        
        if self.use_mock:
            return await self._query_mock(case)
        else:
            return await self._query_neo4j(case)
    
    async def _query_mock(self, case: EthicalCase) -> List[KnowledgeNode]:
        """Query the mock knowledge graph"""
        # Simple query based on case type and ethical dimensions
        relevant_nodes = []
        
        # Get all ethical principles
        principles = await self.mock_graph.query_by_labels(["EthicalPrinciple"])
        
        # Filter by relevance (simple keyword matching)
        for principle in principles:
            principle_name = principle.properties.get("name", "").lower()
            principle_desc = principle.properties.get("description", "").lower()
            
            # Check if principle is relevant to case
            case_text = f"{case.title} {case.description}".lower()
            if principle_name in case_text or any(keyword in case_text for keyword in principle_desc.split()):
                relevant_nodes.append(principle)
        
        # If no specific matches, return most common principles
        if not relevant_nodes and principles:
            relevant_nodes = principles[:4]  # Return top 4 principles
        
        return relevant_nodes
    
    async def _query_neo4j(self, case: EthicalCase) -> List[KnowledgeNode]:
        """Query Neo4j knowledge graph"""
        # Build query based on case characteristics
        query = """
        MATCH (p:EthicalPrinciple)
        WHERE p.cultural_context = $cultural_context OR p.cultural_context = 'universal'
        RETURN p
        ORDER BY p.weight DESC
        LIMIT 10
        """
        
        async with self.driver.session() as session:
            result = await session.run(
                query,
                cultural_context=case.cultural_context.value
            )
            
            nodes = []
            async for record in result:
                node_data = record["p"]
                node = KnowledgeNode(
                    node_id=str(node_data.id),
                    labels=list(node_data.labels),
                    properties=dict(node_data)
                )
                nodes.append(node)
            
            return nodes
    
    async def add_case_insights(self, case: EthicalCase, decision_result: DecisionResult):
        """
        Add insights from a processed case to the knowledge graph
        
        Args:
            case: The ethical case
            decision_result: The decision result
        """
        if not self._initialized:
            await self.initialize()
        
        if self.use_mock:
            await self._add_case_insights_mock(case, decision_result)
        else:
            await self._add_case_insights_neo4j(case, decision_result)
    
    async def _add_case_insights_mock(self, case: EthicalCase, decision_result: DecisionResult):
        """Add insights to mock knowledge graph"""
        # Add case node
        case_node_id = await self.mock_graph.add_node(
            labels=["EthicalCase"],
            properties={
                "case_id": case.case_id,
                "title": case.title,
                "case_type": case.case_type.value,
                "complexity": case.complexity.value,
                "cultural_context": case.cultural_context.value,
                "final_decision": decision_result.final_decision,
                "confidence": decision_result.confidence_score,
                "created_at": datetime.now().isoformat()
            }
        )
        
        # Link to relevant principles
        for principle in decision_result.thesis_result.key_principles:
            # Find principle node
            principle_node = None
            for node in self.mock_graph.nodes.values():
                if (node.properties.get("name") == principle.name and 
                    "EthicalPrinciple" in node.labels):
                    principle_node = node
                    break
            
            if principle_node:
                await self.mock_graph.add_relationship(
                    start_node=case_node_id,
                    end_node=principle_node.id,
                    rel_type="APPLIES_PRINCIPLE",
                    properties={
                        "relevance": principle.relevance_score,
                        "weight": principle.weight,
                        "context": case.case_type.value
                    }
                )
    
    async def _add_case_insights_neo4j(self, case: EthicalCase, decision_result: DecisionResult):
        """Add insights to Neo4j knowledge graph"""
        async with self.driver.session() as session:
            # Add case node
            await session.run(
                """
                CREATE (c:EthicalCase {
                    case_id: $case_id,
                    title: $title,
                    case_type: $case_type,
                    complexity: $complexity,
                    cultural_context: $cultural_context,
                    final_decision: $final_decision,
                    confidence: $confidence,
                    created_at: datetime()
                })
                """,
                case_id=case.case_id,
                title=case.title,
                case_type=case.case_type.value,
                complexity=case.complexity.value,
                cultural_context=case.cultural_context.value,
                final_decision=decision_result.final_decision,
                confidence=decision_result.confidence_score
            )
            
            # Link to principles
            for principle in decision_result.thesis_result.key_principles:
                await session.run(
                    """
                    MATCH (c:EthicalCase {case_id: $case_id})
                    MATCH (p:EthicalPrinciple {name: $principle_name})
                    CREATE (c)-[:APPLIES_PRINCIPLE {
                        relevance: $relevance,
                        weight: $weight,
                        context: $context
                    }]->(p)
                    """,
                    case_id=case.case_id,
                    principle_name=principle.name,
                    relevance=principle.relevance_score,
                    weight=principle.weight,
                    context=case.case_type.value
                )
    
    async def get_principle_conflicts(self, principle_name: str) -> List[Dict[str, Any]]:
        """
        Get conflicts for a specific principle
        
        Args:
            principle_name: Name of the principle
            
        Returns:
            List of conflicts
        """
        if not self._initialized:
            await self.initialize()
        
        if self.use_mock:
            return await self._get_principle_conflicts_mock(principle_name)
        else:
            return await self._get_principle_conflicts_neo4j(principle_name)
    
    async def _get_principle_conflicts_mock(self, principle_name: str) -> List[Dict[str, Any]]:
        """Get principle conflicts from mock graph"""
        conflicts = []
        
        # Find the principle node
        principle_node = None
        for node in self.mock_graph.nodes.values():
            if (node.properties.get("name") == principle_name and 
                "EthicalPrinciple" in node.labels):
                principle_node = node
                break
        
        if not principle_node:
            return conflicts
        
        # Find conflict relationships
        for relationship in self.mock_graph.relationships.values():
            if relationship.type == "CONFLICTS_WITH":
                if relationship.start_node == principle_node.id:
                    conflicting_node = self.mock_graph.nodes[relationship.end_node]
                    conflicts.append({
                        "principle": conflicting_node.properties.get("name"),
                        "description": relationship.properties.get("description"),
                        "strength": relationship.properties.get("strength")
                    })
                elif relationship.end_node == principle_node.id:
                    conflicting_node = self.mock_graph.nodes[relationship.start_node]
                    conflicts.append({
                        "principle": conflicting_node.properties.get("name"),
                        "description": relationship.properties.get("description"),
                        "strength": relationship.properties.get("strength")
                    })
        
        return conflicts
    
    async def _get_principle_conflicts_neo4j(self, principle_name: str) -> List[Dict[str, Any]]:
        """Get principle conflicts from Neo4j"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (p1:EthicalPrinciple {name: $principle_name})
                MATCH (p1)-[r:CONFLICTS_WITH]-(p2:EthicalPrinciple)
                RETURN p2.name as principle, r.description as description, r.strength as strength
                """,
                principle_name=principle_name
            )
            
            conflicts = []
            async for record in result:
                conflicts.append({
                    "principle": record["principle"],
                    "description": record["description"],
                    "strength": record["strength"]
                })
            
            return conflicts
    
    async def check_health(self) -> bool:
        """
        Check knowledge graph health
        
        Returns:
            True if healthy
        """
        try:
            if not self._initialized:
                return False
            
            if self.use_mock:
                return len(self.mock_graph.nodes) > 0
            else:
                async with self.driver.session() as session:
                    result = await session.run("RETURN 1 as test")
                    record = await result.single()
                    return record["test"] == 1
                    
        except Exception as e:
            logger.error(f"Knowledge graph health check failed: {e}")
            return False
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get knowledge graph statistics
        
        Returns:
            Statistics dictionary
        """
        if not self._initialized:
            await self.initialize()
        
        if self.use_mock:
            return {
                "total_nodes": len(self.mock_graph.nodes),
                "total_relationships": len(self.mock_graph.relationships),
                "node_types": list(self.mock_graph.node_index.keys()),
                "relationship_types": list(self.mock_graph.relationship_index.keys()),
                "type": "mock"
            }
        else:
            async with self.driver.session() as session:
                # Get node counts
                result = await session.run("MATCH (n) RETURN count(n) as total_nodes")
                total_nodes = (await result.single())["total_nodes"]
                
                # Get relationship counts
                result = await session.run("MATCH ()-[r]-() RETURN count(r) as total_relationships")
                total_relationships = (await result.single())["total_relationships"]
                
                # Get node types
                result = await session.run("MATCH (n) RETURN DISTINCT labels(n) as labels")
                node_types = []
                async for record in result:
                    node_types.extend(record["labels"])
                node_types = list(set(node_types))
                
                # Get relationship types
                result = await session.run("MATCH ()-[r]-() RETURN DISTINCT type(r) as rel_type")
                relationship_types = []
                async for record in result:
                    relationship_types.append(record["rel_type"])
                
                return {
                    "total_nodes": total_nodes,
                    "total_relationships": total_relationships,
                    "node_types": node_types,
                    "relationship_types": relationship_types,
                    "type": "neo4j"
                }
    
    async def shutdown(self):
        """Shutdown the knowledge graph connection"""
        try:
            if self.driver:
                await self.driver.close()
            logger.info("Knowledge graph connection closed")
        except Exception as e:
            logger.error(f"Error shutting down knowledge graph: {e}")
            raise