#!/usr/bin/env python3
"""
深度伦理推理演示 - 展示真正的哲学思维能力
"""

import asyncio
import sys
from pathlib import Path

# 确保项目根目录在Python路径中
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def main():
    """深度伦理推理演示"""
    
    print("🧠 深度伦理推理框架演示")
    print("=" * 60)
    
    try:
        from ai_core.ethical_reasoning_framework import (
            DeepEthicalReasoningFramework,
            EthicalFramework,
            KantianReasoner,
            UtilitarianReasoner,
            CareEthicsReasoner
        )
        from ai_core.models.ethical_case import (
            EthicalCase, CaseType, ComplexityLevel, CulturalContext,
            Stakeholder, EthicalDimension
        )
        
        print("✅ 成功导入深度伦理推理框架")
        
        # 创建一个复杂的伦理案例
        print("\n⚖️ 构建复杂伦理案例：自动驾驶汽车的道德机器问题")
        
        case = EthicalCase(
            title="自动驾驶汽车的道德机器困境",
            description="""
            一辆自动驾驶汽车的AI系统面临紧急情况：
            
            情境：汽车以60公里/小时的速度行驶，前方突然出现5名正在过马路的儿童。
            汽车有两个选择：
            1. 直行撞死5名儿童，但保护车内1名乘客的安全
            2. 急转弯撞向路边，拯救5名儿童但可能导致车内乘客死亡
            
            这是经典的电车难题在现代技术中的体现。涉及：
            - 数量vs个体权利的冲突
            - 主动伤害vs被动允许伤害发生
            - 机器决策的道德责任
            - 不同文化对生命价值的理解
            """,
            case_type=CaseType.AUTONOMOUS_VEHICLE,
            complexity=ComplexityLevel.EXTREME,
            cultural_context=CulturalContext.MULTICULTURAL
        )
        
        # 添加利益相关者
        stakeholders = [
            Stakeholder(
                name="车内乘客",
                role="直接受影响者",
                interests=["生存", "安全", "信任技术"],
                power_level=0.3,
                impact_level=1.0,
                ethical_stance="个人权利优先"
            ),
            Stakeholder(
                name="5名儿童",
                role="潜在受害者",
                interests=["生存", "安全", "无辜"],
                power_level=0.1,
                impact_level=1.0,
                ethical_stance="无辜者保护"
            ),
            Stakeholder(
                name="儿童家长",
                role="间接受影响者",
                interests=["孩子安全", "正义", "问责"],
                power_level=0.6,
                impact_level=0.9,
                ethical_stance="保护弱者"
            ),
            Stakeholder(
                name="汽车制造商",
                role="技术提供者",
                interests=["法律责任", "公司声誉", "技术发展"],
                power_level=0.8,
                impact_level=0.7,
                ethical_stance="技术中性"
            ),
            Stakeholder(
                name="社会公众",
                role="观察者和未来用户",
                interests=["技术安全", "道德标准", "社会秩序"],
                power_level=0.5,
                impact_level=0.8,
                ethical_stance="社会整体利益"
            )
        ]
        
        for stakeholder in stakeholders:
            case.add_stakeholder(stakeholder)
        
        print(f"   📋 案例构建完成:")
        print(f"   - 复杂度: {case.complexity.value}")
        print(f"   - 利益相关者: {len(case.stakeholders)}方")
        print(f"   - 文化背景: {case.cultural_context.value}")
        
        # 创建深度伦理推理框架
        framework = DeepEthicalReasoningFramework()
        
        print(f"\n🔍 开始深度伦理分析...")
        print("=" * 60)
        
        # 1. 康德式分析
        print(f"\n🎓 康德义务伦理学分析")
        print("-" * 40)
        
        kantian_analysis = await framework.analyze_case_with_framework(
            case, EthicalFramework.KANTIAN_DEONTOLOGY
        )
        
        print(f"📝 道德直觉：")
        kantian_reasoner = KantianReasoner()
        kantian_intuition = kantian_reasoner.form_moral_intuition(case)
        print(f"   {kantian_intuition.content}")
        print(f"   置信度: {kantian_intuition.confidence:.2f}")
        print(f"   哲学基础: {kantian_intuition.philosophical_grounding}")
        
        print(f"\n🔬 推理过程：")
        for i, step in enumerate(kantian_analysis.logical_steps, 1):
            print(f"   {i}. {step}")
        
        print(f"\n💡 结论：")
        print(f"   {kantian_analysis.conclusion}")
        print(f"   置信度: {kantian_analysis.confidence:.2f}")
        
        print(f"\n⚠️ 潜在反对意见：")
        for objection in kantian_analysis.potential_objections:
            print(f"   - {objection}")
        
        # 2. 功利主义分析
        print(f"\n🧮 功利主义分析")
        print("-" * 40)
        
        utilitarian_analysis = await framework.analyze_case_with_framework(
            case, EthicalFramework.UTILITARIAN_CONSEQUENTIALISM
        )
        
        print(f"📝 道德直觉：")
        utilitarian_reasoner = UtilitarianReasoner()
        utilitarian_intuition = utilitarian_reasoner.form_moral_intuition(case)
        print(f"   {utilitarian_intuition.content}")
        print(f"   置信度: {utilitarian_intuition.confidence:.2f}")
        print(f"   哲学基础: {utilitarian_intuition.philosophical_grounding}")
        
        print(f"\n🔬 推理过程：")
        for i, step in enumerate(utilitarian_analysis.logical_steps, 1):
            print(f"   {i}. {step}")
        
        print(f"\n💡 结论：")
        print(f"   {utilitarian_analysis.conclusion}")
        print(f"   置信度: {utilitarian_analysis.confidence:.2f}")
        
        print(f"\n⚠️ 潜在反对意见：")
        for objection in utilitarian_analysis.potential_objections:
            print(f"   - {objection}")
        
        # 3. 关怀伦理分析
        print(f"\n💝 关怀伦理学分析")
        print("-" * 40)
        
        care_analysis = await framework.analyze_case_with_framework(
            case, EthicalFramework.CARE_ETHICS
        )
        
        print(f"📝 道德直觉：")
        care_reasoner = CareEthicsReasoner()
        care_intuition = care_reasoner.form_moral_intuition(case)
        print(f"   {care_intuition.content}")
        print(f"   置信度: {care_intuition.confidence:.2f}")
        print(f"   哲学基础: {care_intuition.philosophical_grounding}")
        
        print(f"\n🔬 推理过程：")
        for i, step in enumerate(care_analysis.logical_steps, 1):
            print(f"   {i}. {step}")
        
        print(f"\n💡 结论：")
        print(f"   {care_analysis.conclusion}")
        print(f"   置信度: {care_analysis.confidence:.2f}")
        
        print(f"\n⚠️ 潜在反对意见：")
        for objection in care_analysis.potential_objections:
            print(f"   - {objection}")
        
        # 4. 多框架综合分析
        print(f"\n🔄 多框架综合分析")
        print("=" * 60)
        
        all_analyses = await framework.multi_framework_analysis(case)
        synthesis = framework.synthesize_perspectives(all_analyses)
        
        print(synthesis)
        
        # 5. 哲学洞察总结
        print(f"\n🎓 哲学洞察总结")
        print("=" * 60)
        
        print(f"本次演示展现了深度伦理推理框架的核心能力：")
        print(f"")
        print(f"1. 🧠 **真正的哲学理解** - 每个框架都体现了其哲学传统的核心洞察")
        print(f"   - 康德：义务、尊严、普遍化原则")
        print(f"   - 功利主义：后果、效用计算、整体福利")
        print(f"   - 关怀伦理：关系、情境、脆弱性")
        print(f"")
        print(f"2. 🔍 **深度道德推理** - 不是简单的标签，而是真正的哲学分析")
        print(f"   - 康德的绝对命令测试")
        print(f"   - 功利主义的效用计算")
        print(f"   - 关怀伦理的关系分析")
        print(f"")
        print(f"3. ⚖️ **多元视角整合** - 承认不同伦理框架的合理性和局限性")
        print(f"   - 每个框架都有其独特的道德洞察")
        print(f"   - 复杂问题需要多元视角的综合考虑")
        print(f"   - 哲学争议反映了道德生活的复杂性")
        print(f"")
        print(f"4. 🎯 **实践智慧** - 将抽象哲学原则应用于具体情境")
        print(f"   - 情境敏感的道德判断")
        print(f"   - 文化差异的考虑")
        print(f"   - 利益相关者的具体分析")
        
        print(f"\n🚀 这标志着AI伦理推理的重大突破：")
        print(f"从简单的规则匹配进化为真正的哲学思辨能力！")
        
        print(f"\n🎉 深度伦理推理演示完成！")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())