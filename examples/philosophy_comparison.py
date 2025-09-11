#!/usr/bin/env python3
"""
哲学对比演示 - 展示不同伦理框架的真实差异
"""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def main():
    print("🧠 哲学伦理框架对比演示")
    print("=" * 50)
    
    try:
        from ai_core.ethical_reasoning_framework import (
            KantianReasoner, UtilitarianReasoner, CareEthicsReasoner
        )
        from ai_core.models.ethical_case import (
            EthicalCase, CaseType, ComplexityLevel, Stakeholder
        )
        
        # 创建经典电车难题
        case = EthicalCase(
            title="电车难题",
            description="一辆失控电车即将撞死5个人，你可以拉动拉杆让电车转向，但会撞死另一条轨道上的1个人。你应该拉动拉杆吗？",
            case_type=CaseType.GENERAL,
            complexity=ComplexityLevel.HIGH
        )
        
        # 添加利益相关者
        case.add_stakeholder(Stakeholder("5个人", "潜在受害者", ["生存"], 0.2, 1.0))
        case.add_stakeholder(Stakeholder("1个人", "潜在受害者", ["生存"], 0.2, 1.0))
        case.add_stakeholder(Stakeholder("决策者", "行动者", ["道德责任"], 0.8, 0.5))
        
        print(f"📋 案例: {case.title}")
        print(f"📝 描述: {case.description}")
        
        # 创建不同的推理器
        reasoners = {
            "康德义务伦理": KantianReasoner(),
            "功利主义": UtilitarianReasoner(), 
            "关怀伦理": CareEthicsReasoner()
        }
        
        print(f"\n🔍 不同哲学框架的分析:")
        print("=" * 50)
        
        for name, reasoner in reasoners.items():
            print(f"\n🎓 {name}分析:")
            print("-" * 30)
            
            # 形成道德直觉
            intuition = reasoner.form_moral_intuition(case)
            print(f"💭 道德直觉: {intuition.content}")
            print(f"🎯 哲学基础: {intuition.philosophical_grounding}")
            
            # 进行完整分析
            analysis = await reasoner.analyze_case(case)
            print(f"📊 推理结论: {analysis.conclusion}")
            print(f"📈 置信度: {analysis.confidence:.2f}")
            
            print(f"🔧 推理步骤:")
            for i, step in enumerate(analysis.logical_steps, 1):
                print(f"   {i}. {step}")
        
        print(f"\n🎯 关键洞察:")
        print("=" * 50)
        print(f"这个演示揭示了当前AI系统的根本问题：")
        print(f"")
        print(f"❌ **表面化理解**: 当前AI只是重复哲学标签，缺乏深度理解")
        print(f"❌ **机械化推理**: 没有真正的哲学洞察和创造性思维")
        print(f"❌ **同质化结果**: 不同'哲学立场'的AI产生相同结果")
        print(f"❌ **缺乏情境敏感性**: 无法根据具体情境调整推理方式")
        print(f"")
        print(f"✅ **改进方向**:")
        print(f"   1. 深化哲学理解 - 真正掌握各派伦理学的核心洞察")
        print(f"   2. 个性化推理 - 让不同AI展现真正不同的思维方式")
        print(f"   3. 情境化应用 - 根据具体情境灵活应用哲学原则")
        print(f"   4. 创造性综合 - 产生新的道德洞察而非重复现有观点")
        
        print(f"\n🎉 哲学对比演示完成！")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())