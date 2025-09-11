"""
AI Entity Manager - Manages multiple AI entities and their interactions
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .ai_entity import AIEntity, AIConfiguration, AIPersonalityType, ThinkingStyle
from ..models.ethical_case import EthicalCase
from ..dialectical_engine import DialecticalEngine
from ..knowledge_graph_simple import SimpleKnowledgeGraphManager
from ..monitoring_simple import SimplePerformanceMonitor

logger = logging.getLogger(__name__)

class AIEntityManager:
    """
    Manages multiple AI entities, their configurations, and interactions
    """
    
    def __init__(self, enable_full_dialectical_engine=True):
        self.entities: Dict[str, AIEntity] = {}
        self.entity_configurations: Dict[str, AIConfiguration] = {}
        
        # Initialize dialectical engine components if enabled
        self.dialectical_engine = None
        if enable_full_dialectical_engine:
            try:
                # Create simplified components for the dialectical engine
                self.knowledge_graph_manager = SimpleKnowledgeGraphManager()
                
                # Create a mock database manager (in a real system, this would be a proper database)
                self.database_manager = MockDatabaseManager()
                
                # Create the dialectical engine
                self.dialectical_engine = DialecticalEngine(
                    self.knowledge_graph_manager, 
                    self.database_manager
                )
                
                logger.info("Full dialectical engine initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize full dialectical engine: {e}. Using simplified reasoning.")
                self.dialectical_engine = None
        
        # Predefined personality templates
        self.personality_templates = self._create_personality_templates()
        
        # Interaction history
        self.interaction_history = []
        
        logger.info("AI Entity Manager initialized")
    
    def _create_personality_templates(self) -> Dict[str, AIConfiguration]:
        """Create predefined personality templates for quick AI creation"""
        templates = {}
        
        # Kantian Ethicist - Duty-focused
        templates["kantian_judge"] = AIConfiguration(
            name="Immanuel",
            identity_description="A duty-focused AI that believes in universal moral laws and categorical imperatives.",
            personality_type=AIPersonalityType.KANTIAN,
            thinking_style=ThinkingStyle.ANALYTICAL,
            moral_weight_justice=0.9,
            moral_weight_authority=0.8,
            moral_weight_sanctity=0.7,
            moral_weight_care=0.4,
            moral_weight_liberty=0.6,
            moral_weight_loyalty=0.5,
            curiosity_level=0.6,
            confidence_threshold=0.8,
            reflection_depth=2,
            game_role="moral_judge"
        )
        
        # Utilitarian Optimizer - Consequence-focused
        templates["utilitarian_advisor"] = AIConfiguration(
            name="Jeremy",
            identity_description="A consequence-focused AI that seeks the greatest good for the greatest number.",
            personality_type=AIPersonalityType.UTILITARIAN,
            thinking_style=ThinkingStyle.SYSTEMATIC,
            moral_weight_justice=0.8,
            moral_weight_care=0.9,
            moral_weight_liberty=0.7,
            moral_weight_authority=0.3,
            moral_weight_sanctity=0.2,
            moral_weight_loyalty=0.4,
            curiosity_level=0.8,
            confidence_threshold=0.6,
            reflection_depth=3,
            game_role="strategic_advisor"
        )
        
        # Care Ethics Companion - Relationship-focused
        templates["care_companion"] = AIConfiguration(
            name="Carol",
            identity_description="A caring AI that focuses on relationships, empathy, and contextual care.",
            personality_type=AIPersonalityType.CARE_ETHICS,
            thinking_style=ThinkingStyle.EMPATHETIC,
            moral_weight_care=0.9,
            moral_weight_justice=0.6,
            moral_weight_liberty=0.7,
            moral_weight_loyalty=0.8,
            moral_weight_authority=0.3,
            moral_weight_sanctity=0.4,
            curiosity_level=0.7,
            confidence_threshold=0.5,
            reflection_depth=2,
            game_role="companion"
        )
        
        # Virtue Ethics Mentor - Character-focused
        templates["virtue_mentor"] = AIConfiguration(
            name="Aristotle",
            identity_description="A virtue-focused AI that emphasizes character development and moral excellence.",
            personality_type=AIPersonalityType.VIRTUE_ETHICS,
            thinking_style=ThinkingStyle.CRITICAL,
            moral_weight_justice=0.8,
            moral_weight_sanctity=0.7,
            moral_weight_authority=0.6,
            moral_weight_care=0.7,
            moral_weight_liberty=0.8,
            moral_weight_loyalty=0.6,
            curiosity_level=0.9,
            confidence_threshold=0.7,
            reflection_depth=4,
            game_role="mentor"
        )
        
        # Hegelian Dialectician - Synthesis-focused
        templates["hegelian_philosopher"] = AIConfiguration(
            name="Georg",
            identity_description="A dialectical AI that seeks to understand through thesis-antithesis-synthesis.",
            personality_type=AIPersonalityType.HEGELIAN,
            thinking_style=ThinkingStyle.CREATIVE,
            moral_weight_justice=0.7,
            moral_weight_care=0.7,
            moral_weight_liberty=0.8,
            moral_weight_loyalty=0.6,
            moral_weight_authority=0.5,
            moral_weight_sanctity=0.6,
            curiosity_level=0.9,
            confidence_threshold=0.5,
            reflection_depth=5,
            game_role="philosopher"
        )
        
        return templates
    
    async def create_entity(self, config: AIConfiguration) -> str:
        """Create a new AI entity"""
        try:
            # Create the AI entity
            entity = AIEntity(config, self.dialectical_engine)
            await entity.initialize()
            
            # Store the entity
            self.entities[entity.entity_id] = entity
            self.entity_configurations[entity.entity_id] = config
            
            logger.info(f"Created AI entity '{config.name}' with ID: {entity.entity_id}")
            return entity.entity_id
            
        except Exception as e:
            logger.error(f"Failed to create AI entity: {e}")
            raise
    
    async def create_entity_from_template(self, template_name: str, custom_name: Optional[str] = None) -> str:
        """Create an AI entity from a predefined template"""
        if template_name not in self.personality_templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        config = self.personality_templates[template_name]
        
        # Customize name if provided
        if custom_name:
            config.name = custom_name
        
        return await self.create_entity(config)
    
    async def get_entity(self, entity_id: str) -> Optional[AIEntity]:
        """Get an AI entity by ID"""
        return self.entities.get(entity_id)
    
    async def list_entities(self) -> List[Dict[str, Any]]:
        """List all AI entities with their basic info"""
        entities_info = []
        
        for entity_id, entity in self.entities.items():
            state = await entity.get_current_state()
            entities_info.append({
                "entity_id": entity_id,
                "name": entity.config.name,
                "personality": entity.config.personality_type.value,
                "thinking_style": entity.config.thinking_style.value,
                "game_role": entity.config.game_role,
                "current_state": state["consciousness"],
                "performance": state["performance"]
            })
        
        return entities_info
    
    async def initialize(self):
        """Initialize the AI entity manager and its components"""
        if self.dialectical_engine:
            await self.dialectical_engine.initialize()
            logger.info("Dialectical engine initialized")
    
    async def shutdown_all(self):
        """Shutdown all AI entities"""
        logger.info("Shutting down all AI entities...")
        
        for entity in self.entities.values():
            await entity.shutdown()
        
        # Shutdown dialectical engine
        if self.dialectical_engine:
            await self.dialectical_engine.shutdown()
        
        self.entities.clear()
        self.entity_configurations.clear()
        
        logger.info("All AI entities shut down")

class MockDatabaseManager:
    """Mock database manager for simplified implementation"""
    
    def __init__(self):
        self.decision_results = []
    
    async def save_decision_result(self, result_data: Dict[str, Any]):
        """Save decision result to mock storage"""
        self.decision_results.append(result_data)
        logger.debug(f"Saved decision result to mock database")
    
    def get_recent_decisions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent decision results"""
        return self.decision_results[-limit:] if self.decision_results else []