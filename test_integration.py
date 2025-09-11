#!/usr/bin/env python3
"""
Integration test for the dialectical engine
"""

import asyncio
import sys
from pathlib import Path

# 确保项目根目录在Python路径中
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_dialectical_engine():
    """Test the complete dialectical engine integration"""
    
    print("🧪 测试辩证决策引擎集成...")
    
    try:
        from ai_core.entities.ai_entity_manager import AIEntityManager
        from ai_core.models.ethical_case import EthicalCase, CaseType, ComplexityLevel
        
        # 创建AI实体管理器
        print("📋 创建AI实体管理器...")
        manager = AIEntityManager(enable_full_dialectical_engine=True)
        await manager.initialize()
        
        # 创建一个AI实体
        print("🤖 创建AI实体...")
        entity_id = await manager.create_entity_from_template("kantian_judge", "测试康德")
        entity = await manager.get_entity(entity_id)
        
        # 创建一个简单的伦理案例
        print("⚖️ 创建伦理案例...")
        case = EthicalCase(
            title="简单测试案例",
            description="这是一个用于测试辩证决策引擎的简单案例",
            case_type=CaseType.GENERAL,
            complexity=ComplexityLevel.LOW
        )
        
        # 让AI思考这个案例
        print("💭 AI开始思考...")
        thought = await entity.think_about(case)
        
        print(f"✅ 思考完成!")
        print(f"   阶段: {thought.stage}")
        print(f"   置信度: {thought.confidence:.2f}")
        print(f"   内容长度: {len(thought.content)} 字符")
        
        # 检查是否使用了完整的辩证引擎
        if entity.dialectical_engine:
            print("✅ 使用了完整的辩证决策引擎")
        else:
            print("⚠️ 使用了简化的推理模式")
        
        # 获取AI状态
        state = await entity.get_current_state()
        print(f"📊 AI状态:")
        print(f"   成功率: {state['performance']['success_rate']:.2%}")
        print(f"   总思考次数: {state['performance']['total_thoughts']}")
        
        # 清理
        await manager.shutdown_all()
        
        print("🎉 测试完成!")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_dialectical_engine())
    sys.exit(0 if success else 1)