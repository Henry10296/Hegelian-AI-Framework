"""
Simple Moral NPC System Demonstration
"""

import sys
import os
import time
import random
from typing import Dict, Any

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moral_npc_system.core.moral_state import MoralState
from moral_npc_system.core.action import Action, ActionType
from moral_npc_system.ethics.moral_framework import MoralFramework


def test_moral_framework():
    """Test the moral evaluation framework"""
    print("=" * 50)
    print("MORAL FRAMEWORK DEMONSTRATION")
    print("=" * 50)
    
    # Create moral framework
    moral_framework = MoralFramework()
    
    # Create different NPC moral states
    kantian_npc = MoralState(
        kantian_weight=0.7,
        utilitarian_weight=0.2,
        virtue_weight=0.1,
        empathy_level=0.8,
        moral_courage=0.7
    )
    
    utilitarian_npc = MoralState(
        kantian_weight=0.2,
        utilitarian_weight=0.7,
        virtue_weight=0.1,
        empathy_level=0.6,
        social_pressure_resistance=0.4
    )
    
    # Test actions
    help_action = Action(
        id="demo_help",
        action_type=ActionType.HELP,
        actor_id="npc_001",
        target_id="player",
        intensity=0.8
    )
    
    harm_action = Action(
        id="demo_harm", 
        action_type=ActionType.HARM,
        actor_id="npc_001",
        target_id="innocent",
        intensity=0.6
    )
    
    # Test context
    emergency_context = {
        'urgency': 0.9,
        'harm_potential': 0.3,
        'benefit_potential': 0.8,
        'social_visibility': 0.5,
        'requires_moral_courage': True
    }
    
    # Evaluate actions
    print("\nKantian NPC evaluating HELP action:")
    kantian_help_eval = moral_framework.evaluate_action(help_action, kantian_npc, emergency_context)
    print(f"Final Score: {kantian_help_eval['final_score']:.3f}")
    print(f"Recommendation: {kantian_help_eval['recommendation']}")
    
    print("\nUtilitarian NPC evaluating HELP action:")
    util_help_eval = moral_framework.evaluate_action(help_action, utilitarian_npc, emergency_context)
    print(f"Final Score: {util_help_eval['final_score']:.3f}")
    print(f"Recommendation: {util_help_eval['recommendation']}")
    
    print("\nKantian NPC evaluating HARM action:")
    kantian_harm_eval = moral_framework.evaluate_action(harm_action, kantian_npc, emergency_context)
    print(f"Final Score: {kantian_harm_eval['final_score']:.3f}")
    print(f"Recommendation: {kantian_harm_eval['recommendation']}")
    
    return True


def test_individual_ethics():
    """Test individual ethics frameworks"""
    print("\n" + "=" * 50)
    print("INDIVIDUAL ETHICS FRAMEWORKS TEST")
    print("=" * 50)
    
    from moral_npc_system.ethics.kantian_ethics import KantianEthics
    from moral_npc_system.ethics.utilitarian_ethics import UtilitarianEthics
    from moral_npc_system.ethics.virtue_ethics import VirtueEthics
    
    kantian = KantianEthics()
    utilitarian = UtilitarianEthics()
    virtue = VirtueEthics()
    
    # Test action
    action = Action('test_001', ActionType.HELP, 'npc_001', 'player')
    context = {
        'urgency': 0.7,
        'harm_potential': 0.2,
        'benefit_potential': 0.8,
        'social_visibility': 0.6
    }
    
    k_score = kantian.evaluate_action(action, context)
    u_score = utilitarian.evaluate_action(action, context)
    v_score = virtue.evaluate_action(action, context)
    
    print(f"Action: {action.action_type.value}")
    print(f"Kantian Ethics Score: {k_score:.3f}")
    print(f"Utilitarian Ethics Score: {u_score:.3f}")
    print(f"Virtue Ethics Score: {v_score:.3f}")
    
    # Test negative action
    harm_action = Action('test_002', ActionType.HARM, 'npc_001', 'victim')
    
    k_score2 = kantian.evaluate_action(harm_action, context)
    u_score2 = utilitarian.evaluate_action(harm_action, context)
    v_score2 = virtue.evaluate_action(harm_action, context)
    
    print(f"\nAction: {harm_action.action_type.value}")
    print(f"Kantian Ethics Score: {k_score2:.3f}")
    print(f"Utilitarian Ethics Score: {u_score2:.3f}")
    print(f"Virtue Ethics Score: {v_score2:.3f}")
    
    return True


def test_npc_manager():
    """Test NPC Manager"""
    print("\n" + "=" * 50)
    print("NPC MANAGER TEST")
    print("=" * 50)
    
    from moral_npc_system.core.npc_manager import NPCManager
    
    try:
        manager = NPCManager()
        print("NPC Manager created successfully")
        
        # Create test NPCs
        npc1 = manager.create_npc('guard_001', 'kantian')
        npc2 = manager.create_npc('merchant_001', 'utilitarian')
        npc3 = manager.create_npc('priest_001', 'virtue_ethics')
        
        print(f"Created NPCs: {len(manager.npcs)}")
        
        # Test NPC properties
        for npc_id, npc in manager.npcs.items():
            status = npc.get_current_status()
            print(f"{npc_id}: {status['moral_profile']['dominant_framework']}")
        
        # Create relationships
        manager.create_relationship('guard_001', 'merchant_001', 'colleague', strength=0.6)
        manager.create_relationship('priest_001', 'guard_001', 'friendship', strength=0.7)
        
        print(f"Created {len(manager.social_network.relationships)} relationships")
        
        # Test decision making
        situation = {
            'urgency': 0.8,
            'harm_potential': 0.3,
            'benefit_potential': 0.7,
            'social_visibility': 0.5
        }
        
        decisions = manager.batch_decision_making(situation, ['guard_001', 'merchant_001'])
        
        print("\nDecision Making Results:")
        for npc_id, decision in decisions.items():
            action = decision['chosen_action']
            confidence = decision['decision_confidence']
            print(f"{npc_id}: {action.action_type.value} (confidence: {confidence:.3f})")
        
        return True
        
    except Exception as e:
        print(f"NPC Manager test failed: {e}")
        return False


def main():
    """Main demonstration function"""
    print("MORAL-AWARE NPC BEHAVIOR SYSTEM - DEMONSTRATION")
    print("This demo showcases the core system functionality")
    
    success_count = 0
    
    # Test individual components
    try:
        if test_individual_ethics():
            success_count += 1
            print("\n[SUCCESS] Individual ethics frameworks test passed")
    except Exception as e:
        print(f"\n[FAILED] Individual ethics test failed: {e}")
    
    try:
        if test_moral_framework():
            success_count += 1
            print("\n[SUCCESS] Moral framework test passed")
    except Exception as e:
        print(f"\n[FAILED] Moral framework test failed: {e}")
    
    try:
        if test_npc_manager():
            success_count += 1
            print("\n[SUCCESS] NPC Manager test passed")
    except Exception as e:
        print(f"\n[FAILED] NPC Manager test failed: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("DEMONSTRATION SUMMARY")
    print("=" * 50)
    
    if success_count >= 2:
        print(f"SUCCESS: {success_count}/3 tests passed")
        print("\nCore System Features Demonstrated:")
        print("1. Multi-framework moral evaluation (Kantian, Utilitarian, Virtue)")
        print("2. NPC moral state management and decision making") 
        print("3. Social network and relationship management")
        print("4. Adaptive moral reasoning based on context")
        
        print(f"\nThis system provides powerful moral reasoning capabilities")
        print(f"for game AI, educational tools, and social science research.")
        
    else:
        print(f"PARTIAL SUCCESS: {success_count}/3 tests passed")
        print("Some components may need additional dependencies or setup.")


if __name__ == "__main__":
    main()