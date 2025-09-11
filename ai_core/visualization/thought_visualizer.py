"""
Thought Visualizer - Real-time visualization of AI thinking processes
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

from ..entities.ai_entity import AIEntity, ThoughtProcess

logger = logging.getLogger(__name__)

@dataclass
class VisualizationFrame:
    """Represents a single frame of thought visualization"""
    timestamp: datetime
    entity_id: str
    entity_name: str
    thought_bubbles: List[Dict[str, Any]]
    dialectical_flow: Dict[str, Any]
    emotional_indicators: Dict[str, Any]
    consciousness_state: Dict[str, Any]

class ThoughtVisualizer:
    """
    Visualizes AI thinking processes in real-time
    """
    
    def __init__(self):
        self.active_visualizations: Dict[str, List[VisualizationFrame]] = {}
        self.visualization_settings = {
            "max_frames_per_entity": 50,
            "update_interval": 0.5,  # seconds
            "show_emotional_indicators": True,
            "show_dialectical_flow": True,
            "show_confidence_levels": True
        }
        
        # Visual themes for different thinking stages
        self.stage_themes = {
            "forming": {"color": "#FFE4B5", "icon": "💭", "description": "Forming initial thoughts"},
            "thesis": {"color": "#87CEEB", "icon": "💡", "description": "Establishing position"},
            "antithesis": {"color": "#FFB6C1", "icon": "🤔", "description": "Questioning and challenging"},
            "synthesis": {"color": "#98FB98", "icon": "⚡", "description": "Integrating and resolving"},
            "complete": {"color": "#DDA0DD", "icon": "✨", "description": "Thought completed"}
        }
        
        # Emotional indicators
        self.emotion_indicators = {
            "curious": {"color": "#FFA500", "icon": "🧐", "intensity": "medium"},
            "concerned": {"color": "#FF6347", "icon": "😟", "intensity": "high"},
            "thoughtful": {"color": "#4682B4", "icon": "🤓", "intensity": "medium"},
            "empathetic": {"color": "#FF69B4", "icon": "💝", "intensity": "high"},
            "contemplative": {"color": "#9370DB", "icon": "🧘", "intensity": "low"},
            "adaptive": {"color": "#32CD32", "icon": "🔄", "intensity": "medium"},
            "evolving": {"color": "#FFD700", "icon": "🌱", "intensity": "medium"},
            "peaceful": {"color": "#E6E6FA", "icon": "☮️", "intensity": "low"},
            "aware": {"color": "#00CED1", "icon": "👁️", "intensity": "high"},
            "neutral": {"color": "#D3D3D3", "icon": "😐", "intensity": "low"}
        }
        
        logger.info("Thought Visualizer initialized")
    
    async def start_visualization(self, entity: AIEntity) -> str:
        """Start visualizing an AI entity's thoughts"""
        visualization_id = f"viz_{entity.entity_id}_{datetime.now().timestamp()}"
        self.active_visualizations[visualization_id] = []
        
        # Create initial frame
        initial_frame = await self._create_visualization_frame(entity, visualization_id)
        self.active_visualizations[visualization_id].append(initial_frame)
        
        logger.info(f"Started visualization for entity {entity.config.name}")
        return visualization_id
    
    def stop_visualization(self, visualization_id: str) -> bool:
        """Stop and clean up a visualization"""
        if visualization_id in self.active_visualizations:
            del self.active_visualizations[visualization_id]
            logger.info(f"Stopped visualization {visualization_id}")
            return True
        return False
    
    async def _create_visualization_frame(self, entity: AIEntity, visualization_id: str) -> VisualizationFrame:
        """Create a visualization frame for the current entity state"""
        
        # Get current thoughts
        current_thoughts = entity.consciousness.get_current_thoughts()
        
        # Create thought bubbles
        thought_bubbles = []
        for thought in current_thoughts:
            bubble = self._create_thought_bubble(thought)
            thought_bubbles.append(bubble)
        
        # Create dialectical flow visualization
        dialectical_flow = self._create_dialectical_flow(current_thoughts)
        
        # Create emotional indicators
        emotional_indicators = self._create_emotional_indicators(entity)
        
        # Create consciousness state visualization
        consciousness_state = self._create_consciousness_visualization(entity)
        
        return VisualizationFrame(
            timestamp=datetime.now(),
            entity_id=entity.entity_id,
            entity_name=entity.config.name,
            thought_bubbles=thought_bubbles,
            dialectical_flow=dialectical_flow,
            emotional_indicators=emotional_indicators,
            consciousness_state=consciousness_state
        )
    
    def _create_thought_bubble(self, thought: ThoughtProcess) -> Dict[str, Any]:
        """Create a visual representation of a thought"""
        stage_theme = self.stage_themes.get(thought.stage, self.stage_themes["forming"])
        
        return {
            "thought_id": thought.thought_id,
            "content": thought.content[:100] + "..." if len(thought.content) > 100 else thought.content,
            "full_content": thought.content,
            "stage": thought.stage,
            "confidence": thought.confidence,
            "emotional_tone": thought.emotional_tone,
            "timestamp": thought.timestamp.isoformat(),
            "visual": {
                "color": stage_theme["color"],
                "icon": stage_theme["icon"],
                "description": stage_theme["description"],
                "size": min(max(len(thought.content) / 50, 0.5), 2.0),
                "opacity": min(max(thought.confidence, 0.3), 1.0)
            }
        }
    
    def _create_dialectical_flow(self, thoughts: List[ThoughtProcess]) -> Dict[str, Any]:
        """Create visualization of dialectical reasoning flow"""
        if not thoughts:
            return {"stages": [], "current_stage": "idle", "flow_direction": "none"}
        
        # Find the most recent thought with dialectical stages
        dialectical_thought = None
        for thought in reversed(thoughts):
            if thought.stage in ["thesis", "antithesis", "synthesis"]:
                dialectical_thought = thought
                break
        
        if not dialectical_thought:
            return {"stages": [], "current_stage": "forming", "flow_direction": "none"}
        
        current_stage = dialectical_thought.stage
        
        return {
            "current_stage": current_stage,
            "flow_direction": "forward",
            "thought_id": dialectical_thought.thought_id,
            "confidence": dialectical_thought.confidence
        }
    
    def _create_emotional_indicators(self, entity: AIEntity) -> Dict[str, Any]:
        """Create emotional state indicators"""
        current_emotion = entity.consciousness.emotional_state
        emotion_info = self.emotion_indicators.get(current_emotion, self.emotion_indicators["neutral"])
        
        return {
            "current_emotion": {
                "name": current_emotion,
                "color": emotion_info["color"],
                "icon": emotion_info["icon"],
                "intensity": emotion_info["intensity"]
            },
            "energy_level": entity.consciousness.energy_level,
            "attention_span": entity.consciousness.attention_span
        }
    
    def _create_consciousness_visualization(self, entity: AIEntity) -> Dict[str, Any]:
        """Create visualization of consciousness state"""
        return {
            "current_focus": entity.consciousness.current_focus,
            "active_thought_count": len(entity.consciousness.get_current_thoughts()),
            "total_thoughts": entity.total_thoughts,
            "personality_indicators": {
                "type": entity.config.personality_type.value,
                "thinking_style": entity.config.thinking_style.value,
                "curiosity_level": entity.config.curiosity_level,
                "confidence_threshold": entity.config.confidence_threshold
            }
        }