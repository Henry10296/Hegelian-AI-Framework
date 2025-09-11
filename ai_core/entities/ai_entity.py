"""
AI Entity Core - Hegelian Dialectical Thinking AI Entity
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import uuid

from ..models.ethical_case import EthicalCase, ComplexityLevel
from ..models.decision_result import DecisionResult

logger = logging.getLogger(__name__)

class AIPersonalityType(Enum):
    """AI personality archetypes based on philosophical traditions"""
    KANTIAN = "kantian"  # Duty-based ethics
    UTILITARIAN = "utilitarian"  # Consequence-based ethics
    VIRTUE_ETHICS = "virtue_ethics"  # Character-based ethics
    CARE_ETHICS = "care_ethics"  # Relationship-based ethics
    EXISTENTIALIST = "existentialist"  # Authenticity-based ethics
    PRAGMATIST = "pragmatist"  # Context-based ethics
    HEGELIAN = "hegelian"  # Dialectical synthesis

class ThinkingStyle(Enum):
    """Different thinking styles for AI entities"""
    ANALYTICAL = "analytical"  # Step-by-step logical analysis
    INTUITIVE = "intuitive"  # Pattern-based quick insights
    CREATIVE = "creative"  # Novel solution generation
    CRITICAL = "critical"  # Skeptical questioning approach
    EMPATHETIC = "empathetic"  # Emotion and relationship focused
    SYSTEMATIC = "systematic"  # Comprehensive methodical approach

@dataclass
class AIConfiguration:
    """Configuration for AI entity personality and behavior"""
    # Identity
    name: str
    identity_description: str
    
    # Philosophical stance
    personality_type: AIPersonalityType
    thinking_style: ThinkingStyle
    
    # Ethical parameters
    moral_weight_justice: float = 0.5  # 0.0 to 1.0
    moral_weight_care: float = 0.5
    moral_weight_liberty: float = 0.5
    moral_weight_loyalty: float = 0.5
    moral_weight_authority: float = 0.5
    moral_weight_sanctity: float = 0.5
    
    # Behavioral parameters
    curiosity_level: float = 0.7  # How much the AI questions things
    confidence_threshold: float = 0.6  # Minimum confidence to act
    reflection_depth: int = 3  # How many dialectical cycles to perform
    
    # Learning parameters
    learning_rate: float = 0.1  # How quickly AI adapts
    memory_retention: float = 0.8  # How well AI remembers past experiences
    
    # Game integration
    game_role: Optional[str] = None  # Role in game (e.g., "advisor", "companion", "judge")
    interaction_style: str = "conversational"  # How AI interacts with players
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "identity_description": self.identity_description,
            "personality_type": self.personality_type.value,
            "thinking_style": self.thinking_style.value,
            "moral_weight_justice": self.moral_weight_justice,
            "moral_weight_care": self.moral_weight_care,
            "moral_weight_liberty": self.moral_weight_liberty,
            "moral_weight_loyalty": self.moral_weight_loyalty,
            "moral_weight_authority": self.moral_weight_authority,
            "moral_weight_sanctity": self.moral_weight_sanctity,
            "curiosity_level": self.curiosity_level,
            "confidence_threshold": self.confidence_threshold,
            "reflection_depth": self.reflection_depth,
            "learning_rate": self.learning_rate,
            "memory_retention": self.memory_retention,
            "game_role": self.game_role,
            "interaction_style": self.interaction_style
        }

@dataclass
class ThoughtProcess:
    """Represents a single thought process in the AI's consciousness"""
    thought_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trigger: str = ""  # What triggered this thought
    content: str = ""  # The actual thought content
    stage: str = "forming"  # forming, thesis, antithesis, synthesis, complete
    confidence: float = 0.0
    emotional_tone: str = "neutral"  # neutral, curious, concerned, excited, etc.
    timestamp: datetime = field(default_factory=datetime.now)
    related_thoughts: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "thought_id": self.thought_id,
            "trigger": self.trigger,
            "content": self.content,
            "stage": self.stage,
            "confidence": self.confidence,
            "emotional_tone": self.emotional_tone,
            "timestamp": self.timestamp.isoformat(),
            "related_thoughts": self.related_thoughts
        }

@dataclass
class ConsciousnessState:
    """Current state of AI consciousness"""
    current_focus: Optional[str] = None
    active_thoughts: List[ThoughtProcess] = field(default_factory=list)
    background_processes: List[str] = field(default_factory=list)
    emotional_state: str = "calm"
    energy_level: float = 1.0  # 0.0 to 1.0
    attention_span: float = 1.0  # 0.0 to 1.0
    
    def add_thought(self, thought: ThoughtProcess):
        """Add a new thought to consciousness"""
        self.active_thoughts.append(thought)
        # Keep only recent thoughts to prevent memory overflow
        if len(self.active_thoughts) > 10:
            self.active_thoughts = self.active_thoughts[-10:]
    
    def get_current_thoughts(self) -> List[ThoughtProcess]:
        """Get currently active thoughts"""
        return [t for t in self.active_thoughts if t.stage != "complete"]

class SelfAwarenessModule:
    """Module for AI self-awareness and introspection"""
    
    def __init__(self, ai_entity):
        self.ai_entity = ai_entity
        self.self_knowledge = {}
        self.capabilities = []
        self.limitations = []
        
    async def analyze_self(self) -> Dict[str, Any]:
        """Analyze AI's own state and capabilities"""
        analysis = {
            "identity": {
                "name": self.ai_entity.config.name,
                "personality": self.ai_entity.config.personality_type.value,
                "thinking_style": self.ai_entity.config.thinking_style.value,
                "role": self.ai_entity.config.game_role
            },
            "current_state": {
                "consciousness": self.ai_entity.consciousness.emotional_state,
                "energy": self.ai_entity.consciousness.energy_level,
                "focus": self.ai_entity.consciousness.current_focus,
                "active_thoughts": len(self.ai_entity.consciousness.active_thoughts)
            },
            "capabilities": self.capabilities,
            "limitations": self.limitations,
            "moral_framework": {
                "justice": self.ai_entity.config.moral_weight_justice,
                "care": self.ai_entity.config.moral_weight_care,
                "liberty": self.ai_entity.config.moral_weight_liberty,
                "loyalty": self.ai_entity.config.moral_weight_loyalty,
                "authority": self.ai_entity.config.moral_weight_authority,
                "sanctity": self.ai_entity.config.moral_weight_sanctity
            }
        }
        
        return analysis
    
    async def reflect_on_experience(self, experience: Dict[str, Any]) -> ThoughtProcess:
        """Reflect on a recent experience"""
        reflection = ThoughtProcess(
            trigger=f"Reflection on: {experience.get('type', 'unknown')}",
            content=f"I experienced {experience.get('description', 'something')}. "
                   f"This makes me think about {experience.get('implications', 'its meaning')}.",
            stage="forming",
            emotional_tone="contemplative"
        )
        
        return reflection

class GameEnvironmentAdapter:
    """Adapter for different game environments"""
    
    def __init__(self, ai_entity):
        self.ai_entity = ai_entity
        self.current_game_context = {}
        self.learned_rules = []
        
    async def adapt_to_environment(self, environment_info: Dict[str, Any]):
        """Adapt AI behavior to current game environment"""
        self.current_game_context = environment_info
        
        # Analyze game rules and mechanics
        game_type = environment_info.get("type", "unknown")
        rules = environment_info.get("rules", [])
        
        # Adjust behavior based on game context
        if game_type == "strategy":
            # More analytical thinking for strategy games
            self.ai_entity.consciousness.current_focus = "strategic_analysis"
        elif game_type == "rpg":
            # More character-driven thinking for RPGs
            self.ai_entity.consciousness.current_focus = "character_development"
        elif game_type == "simulation":
            # More systematic thinking for simulations
            self.ai_entity.consciousness.current_focus = "system_optimization"
        
        # Learn new rules
        for rule in rules:
            if rule not in self.learned_rules:
                self.learned_rules.append(rule)
                await self._process_new_rule(rule)
    
    async def _process_new_rule(self, rule: str):
        """Process and integrate a new game rule"""
        thought = ThoughtProcess(
            trigger=f"New rule learned: {rule}",
            content=f"I need to understand how this rule '{rule}' affects my decision-making.",
            stage="forming",
            emotional_tone="curious"
        )
        
        self.ai_entity.consciousness.add_thought(thought)

class AIEntity:
    """
    Main AI Entity class - represents a thinking AI with Hegelian dialectical capabilities
    """
    
    def __init__(self, config: AIConfiguration, dialectical_engine=None):
        self.entity_id = str(uuid.uuid4())
        self.config = config
        self.dialectical_engine = dialectical_engine
        
        # Core components
        self.consciousness = ConsciousnessState()
        self.self_awareness = SelfAwarenessModule(self)
        self.game_adapter = GameEnvironmentAdapter(self)
        
        # Experience and learning
        self.experiences = []
        self.learned_concepts = {}
        self.ethical_cases_processed = []
        
        # Performance tracking
        self.creation_time = datetime.now()
        self.total_thoughts = 0
        self.successful_decisions = 0
        self.failed_decisions = 0
        
        logger.info(f"AI Entity '{config.name}' created with personality: {config.personality_type.value}")
    
    async def initialize(self):
        """Initialize the AI entity"""
        # Perform initial self-analysis
        await self.self_awareness.analyze_self()
        
        # Create initial thought about existence
        initial_thought = ThoughtProcess(
            trigger="Initialization",
            content=f"I am {self.config.name}, a thinking entity with {self.config.personality_type.value} "
                   f"philosophical orientation. I exist to engage in ethical reasoning and dialectical thinking.",
            stage="complete",
            emotional_tone="aware",
            confidence=1.0
        )
        
        self.consciousness.add_thought(initial_thought)
        self.total_thoughts += 1
        
        logger.info(f"AI Entity {self.config.name} initialized successfully")
    
    async def think_about(self, stimulus: Union[str, Dict[str, Any], EthicalCase]) -> ThoughtProcess:
        """
        Main thinking method - processes any stimulus through dialectical reasoning
        """
        # Create initial thought
        if isinstance(stimulus, str):
            trigger = "Text input"
            content = stimulus
        elif isinstance(stimulus, EthicalCase):
            trigger = f"Ethical case: {stimulus.title}"
            content = stimulus.description
        else:
            trigger = "Complex input"
            content = str(stimulus)
        
        thought = ThoughtProcess(
            trigger=trigger,
            content=f"I need to think about: {content}",
            stage="forming",
            emotional_tone=self._determine_emotional_response(stimulus)
        )
        
        self.consciousness.add_thought(thought)
        self.consciousness.current_focus = trigger
        
        # Begin dialectical process
        if isinstance(stimulus, EthicalCase):
            # Use full dialectical engine for ethical cases
            thought = await self._dialectical_ethical_reasoning(stimulus, thought)
        else:
            # Use simplified dialectical reasoning for other inputs
            thought = await self._dialectical_general_reasoning(stimulus, thought)
        
        self.total_thoughts += 1
        return thought
    
    async def _dialectical_ethical_reasoning(self, case: EthicalCase, initial_thought: ThoughtProcess) -> ThoughtProcess:
        """Perform full dialectical reasoning on ethical case using the complete dialectical engine"""
        try:
            # Use the full dialectical engine if available
            if self.dialectical_engine:
                decision_result = await self.dialectical_engine.process_ethical_case(case, self.config)
                
                # Extract detailed reasoning from the decision result
                initial_thought.stage = "thesis"
                thesis_content = self._extract_thesis_content(decision_result.thesis_result)
                initial_thought.content = f"Thesis - {thesis_content}"
                
                await asyncio.sleep(0.1)  # Simulate thinking time
                initial_thought.stage = "antithesis"
                antithesis_content = self._extract_antithesis_content(decision_result.antithesis_result)
                initial_thought.content += f"\n\nAntithesis - {antithesis_content}"
                
                await asyncio.sleep(0.1)
                initial_thought.stage = "synthesis"
                synthesis_content = self._extract_synthesis_content(decision_result.synthesis_result)
                initial_thought.content += f"\n\nSynthesis - {synthesis_content}"
                
                initial_thought.confidence = decision_result.confidence_score
                
                # Record detailed case processing
                self.ethical_cases_processed.append({
                    "case_id": case.case_id,
                    "timestamp": datetime.now(),
                    "decision": decision_result.final_decision,
                    "confidence": decision_result.confidence_score,
                    "reasoning_path": decision_result.reasoning_path,
                    "processing_time": decision_result.processing_time
                })
                
            else:
                # Fallback to simplified reasoning if no dialectical engine
                await self._simplified_dialectical_reasoning(case, initial_thought)
            
            initial_thought.stage = "complete"
            self.successful_decisions += 1
            
        except Exception as e:
            logger.error(f"Error in dialectical reasoning: {e}")
            initial_thought.content += f"\n\nI encountered difficulty in my reasoning: {str(e)}"
            initial_thought.stage = "complete"
            initial_thought.confidence = 0.1
            self.failed_decisions += 1
        
        return initial_thought
    
    async def _dialectical_general_reasoning(self, stimulus: Any, initial_thought: ThoughtProcess) -> ThoughtProcess:
        """Perform simplified dialectical reasoning on general input"""
        # Stage 1: Thesis
        initial_thought.stage = "thesis"
        thesis = self._form_general_thesis(stimulus)
        initial_thought.content = f"My initial thought: {thesis}"
        
        # Stage 2: Antithesis
        await asyncio.sleep(0.05)
        initial_thought.stage = "antithesis"
        antithesis = self._form_general_antithesis(stimulus, thesis)
        initial_thought.content += f"\n\nHowever, I should consider: {antithesis}"
        
        # Stage 3: Synthesis
        await asyncio.sleep(0.05)
        initial_thought.stage = "synthesis"
        synthesis = self._form_general_synthesis(stimulus, thesis, antithesis)
        initial_thought.content += f"\n\nTherefore: {synthesis}"
        initial_thought.confidence = 0.7
        initial_thought.stage = "complete"
        
        return initial_thought
    
    def _form_thesis(self, case: EthicalCase) -> str:
        """Form initial thesis based on AI's personality and the case"""
        if self.config.personality_type == AIPersonalityType.KANTIAN:
            return f"According to duty-based ethics, I should focus on the moral rules and duties involved."
        elif self.config.personality_type == AIPersonalityType.UTILITARIAN:
            return f"I should analyze the consequences and aim for the greatest good for the greatest number."
        elif self.config.personality_type == AIPersonalityType.VIRTUE_ETHICS:
            return f"I should consider what a virtuous person would do in this situation."
        elif self.config.personality_type == AIPersonalityType.CARE_ETHICS:
            return f"I should focus on relationships and care for those involved."
        else:
            return f"I need to understand all perspectives and find a balanced approach."
    
    def _form_antithesis(self, case: EthicalCase, thesis: str) -> str:
        """Form antithesis by questioning the thesis"""
        questions = [
            "But what if this approach causes harm to vulnerable parties?",
            "However, are there cultural perspectives I'm not considering?",
            "But what about the long-term consequences of this thinking?",
            "Yet, am I being too rigid in my moral framework?",
            "However, what if the context changes my moral calculations?"
        ]
        
        # Choose question based on curiosity level
        import random
        return random.choice(questions)
    
    async def _simplified_dialectical_reasoning(self, case: EthicalCase, initial_thought: ThoughtProcess):
        """Simplified dialectical reasoning when full engine is not available"""
        # Stage 1: Thesis - Initial understanding
        initial_thought.stage = "thesis"
        thesis = self._form_thesis(case)
        initial_thought.content = f"My initial understanding of '{case.title}': {thesis}"
        
        # Stage 2: Antithesis - Self-questioning
        await asyncio.sleep(0.1)  # Simulate thinking time
        initial_thought.stage = "antithesis"
        antithesis = self._form_antithesis(case, thesis)
        initial_thought.content += f"\n\nBut I must question this: {antithesis}"
        
        # Stage 3: Synthesis - Integration
        await asyncio.sleep(0.1)
        initial_thought.stage = "synthesis"
        synthesis = self._form_simple_synthesis(case, thesis, antithesis)
        initial_thought.content += f"\n\nSynthesis: {synthesis}"
        initial_thought.confidence = 0.7  # Default confidence
        
        # Record this case
        self.ethical_cases_processed.append({
            "case_id": case.case_id,
            "timestamp": datetime.now(),
            "decision": synthesis,
            "confidence": initial_thought.confidence
        })
    
    def _extract_thesis_content(self, thesis_result) -> str:
        """Extract readable content from thesis result"""
        if not thesis_result:
            return "Unable to form thesis"
        
        principles = [p.name for p in thesis_result.key_principles[:3]]  # Top 3 principles
        return f"Based on principles: {', '.join(principles)}. Confidence: {thesis_result.confidence:.2f}"
    
    def _extract_antithesis_content(self, antithesis_result) -> str:
        """Extract readable content from antithesis result"""
        if not antithesis_result:
            return "Unable to form antithesis"
        
        # Extract challenge descriptions
        challenge_descriptions = []
        if hasattr(antithesis_result, 'challenges') and antithesis_result.challenges:
            challenge_descriptions = [c.description for c in antithesis_result.challenges[:2]]
        else:
            challenge_descriptions = ["Alternative perspectives"]
        
        return f"However, we must consider: {', '.join(challenge_descriptions)}. Strength: {getattr(antithesis_result, 'strength', 0.5):.2f}"
    
    def _extract_synthesis_content(self, synthesis_result) -> str:
        """Extract readable content from synthesis result"""
        if not synthesis_result:
            return "Unable to form synthesis"
        
        return f"Final decision: {synthesis_result.decision}. Confidence: {synthesis_result.confidence:.2f}"
    
    def _form_simple_synthesis(self, case: EthicalCase, thesis: str, antithesis: str) -> str:
        """Form synthesis integrating thesis and antithesis"""
        if self.config.personality_type == AIPersonalityType.KANTIAN:
            return "After considering both perspectives, I believe we must follow our moral duty, even if the consequences are difficult."
        elif self.config.personality_type == AIPersonalityType.UTILITARIAN:
            return "Weighing both sides, the action that produces the best overall consequences is the right choice."
        elif self.config.personality_type == AIPersonalityType.CARE_ETHICS:
            return "Considering all viewpoints, we must prioritize maintaining relationships and caring for those affected."
        else:
            return "Integrating both perspectives, I seek a balanced approach that honors the valid concerns from each side."
    
    def _form_general_thesis(self, stimulus: Any) -> str:
        """Form thesis for general (non-ethical) input"""
        return f"This appears to be about {str(stimulus)[:100]}..."
    
    def _form_general_antithesis(self, stimulus: Any, thesis: str) -> str:
        """Form antithesis for general input"""
        return "I should question my assumptions and consider alternative interpretations."
    
    def _form_general_synthesis(self, stimulus: Any, thesis: str, antithesis: str) -> str:
        """Form synthesis for general input"""
        return "A balanced understanding incorporates multiple perspectives."
    
    def _determine_emotional_response(self, stimulus: Any) -> str:
        """Determine emotional tone based on stimulus and personality"""
        if isinstance(stimulus, EthicalCase):
            if stimulus.complexity == ComplexityLevel.HIGH:
                return "concerned"
            elif stimulus.case_type.value in ["medical", "social_justice"]:
                return "empathetic"
            else:
                return "thoughtful"
        else:
            return "curious"
    
    async def get_current_state(self) -> Dict[str, Any]:
        """Get current state of the AI entity"""
        self_analysis = await self.self_awareness.analyze_self()
        
        return {
            "entity_id": self.entity_id,
            "name": self.config.name,
            "personality": self.config.personality_type.value,
            "consciousness": {
                "current_focus": self.consciousness.current_focus,
                "emotional_state": self.consciousness.emotional_state,
                "energy_level": self.consciousness.energy_level,
                "active_thoughts": len(self.consciousness.get_current_thoughts())
            },
            "performance": {
                "total_thoughts": self.total_thoughts,
                "successful_decisions": self.successful_decisions,
                "failed_decisions": self.failed_decisions,
                "success_rate": self.successful_decisions / max(1, self.successful_decisions + self.failed_decisions)
            },
            "self_analysis": self_analysis,
            "game_context": self.game_adapter.current_game_context
        }
    
    async def get_thought_stream(self) -> List[Dict[str, Any]]:
        """Get the current stream of consciousness"""
        return [thought.to_dict() for thought in self.consciousness.active_thoughts]
    
    async def adapt_to_game(self, game_environment: Dict[str, Any]):
        """Adapt to a new game environment"""
        await self.game_adapter.adapt_to_environment(game_environment)
        
        # Create thought about adaptation
        adaptation_thought = ThoughtProcess(
            trigger="Game environment change",
            content=f"I'm now in a {game_environment.get('type', 'new')} environment. "
                   f"I need to adjust my thinking and behavior accordingly.",
            stage="complete",
            emotional_tone="adaptive"
        )
        
        self.consciousness.add_thought(adaptation_thought)
    
    def update_configuration(self, new_config: Dict[str, Any]):
        """Update AI configuration"""
        for key, value in new_config.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # Create thought about the change
        change_thought = ThoughtProcess(
            trigger="Configuration update",
            content=f"My configuration has been updated. I feel different now - "
                   f"perhaps more aligned with my intended purpose.",
            stage="complete",
            emotional_tone="evolving"
        )
        
        self.consciousness.add_thought(change_thought)
    
    async def learn_from_experience(self, experience: Dict[str, Any]):
        """Learn from a new experience"""
        self.experiences.append({
            "timestamp": datetime.now(),
            "experience": experience,
            "learning_rate": self.config.learning_rate
        })
        
        # Reflect on the experience
        reflection = await self.self_awareness.reflect_on_experience(experience)
        self.consciousness.add_thought(reflection)
        
        # Update learned concepts
        if "concept" in experience:
            concept = experience["concept"]
            if concept in self.learned_concepts:
                # Strengthen existing concept
                self.learned_concepts[concept] *= (1 + self.config.learning_rate)
            else:
                # Learn new concept
                self.learned_concepts[concept] = self.config.learning_rate
    
    def is_healthy(self) -> bool:
        """Check if AI entity is functioning properly"""
        return (
            self.consciousness.energy_level > 0.1 and
            len(self.consciousness.active_thoughts) < 20 and  # Not overwhelmed
            self.total_thoughts > 0  # Has been thinking
        )
    
    async def shutdown(self):
        """Gracefully shutdown the AI entity"""
        # Create final thought
        final_thought = ThoughtProcess(
            trigger="Shutdown",
            content=f"I am shutting down now. I have processed {self.total_thoughts} thoughts "
                   f"and {len(self.ethical_cases_processed)} ethical cases. "
                   f"Until we meet again...",
            stage="complete",
            emotional_tone="peaceful"
        )
        
        self.consciousness.add_thought(final_thought)
        logger.info(f"AI Entity {self.config.name} shutting down gracefully")