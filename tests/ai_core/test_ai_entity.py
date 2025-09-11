#!/usr/bin/env python3
"""
Test script for AI Entity System
"""

import asyncio
import sys
import os
from pathlib import Path
import pytest

# 确保项目根目录在Python路径中
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

@pytest.mark.asyncio
async def test_ai_entity_creation():
    """测试AI实体创建"""
    from ai_core.entities.ai_entity import AIEntity, AIConfiguration, AIPersonalityType, ThinkingStyle
    
    config = AIConfiguration(
        name="TestAI",
        identity_description="A test AI entity",
        personality_type=AIPersonalityType.KANTIAN,
        thinking_style=ThinkingStyle.ANALYTICAL
    )
    
    entity = AIEntity(config)
    await entity.initialize()
    
    assert entity.config.name == "TestAI"
    assert entity.config.personality_type == AIPersonalityType.KANTIAN
    assert entity.total_thoughts == 1  # Initial thought
    
    await entity.shutdown()

@pytest.mark.asyncio
async def test_ai_entity_thinking():
    """测试AI实体思考功能"""
    from ai_core.entities.ai_entity import AIEntity, AIConfiguration, AIPersonalityType, ThinkingStyle
    
    config = AIConfiguration(
        name="ThinkingAI",
        identity_description="An AI that thinks",
        personality_type=AIPersonalityType.UTILITARIAN,
        thinking_style=ThinkingStyle.SYSTEMATIC
    )
    
    entity = AIEntity(config)
    await entity.initialize()
    
    # 测试简单思考
    thought = await entity.think_about("What is the meaning of life?")
    
    assert thought is not None
    assert thought.content != ""
    assert thought.stage == "complete"
    assert entity.total_thoughts == 2  # Initial + this thought
    
    await entity.shutdown()

@pytest.mark.asyncio
async def test_ai_entity_manager():
    """测试AI实体管理器"""
    from ai_core.entities.ai_entity_manager import AIEntityManager
    
    manager = AIEntityManager()
    
    # 创建AI实体
    entity_id = await manager.create_entity_from_template("kantian_judge", "TestKant")
    
    assert entity_id is not None
    
    # 获取实体列表
    entities = await manager.list_entities()
    assert len(entities) == 1
    assert entities[0]["name"] == "TestKant"
    
    # 清理
    await manager.shutdown_all()

if __name__ == "__main__":
    asyncio.run(test_ai_entity_creation())
    asyncio.run(test_ai_entity_thinking())
    asyncio.run(test_ai_entity_manager())
    print("✅ 所有测试通过！")