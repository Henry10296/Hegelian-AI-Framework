#!/usr/bin/env python3
"""
AI Entity Demo - 演示AI实体系统的基本功能
"""

import asyncio
import sys
from pathlib import Path

# 确保项目根目录在Python路径中
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def main():
    """演示AI实体系统"""
    
    print("🚀 AI实体系统演示")
    print("=" * 50)
    
    try:
        # 导入整理后的模块
        from ai_core import (
            AIEntity, 
            AIConfiguration, 
            AIPersonalityType, 
            ThinkingStyle,
            AIEntityManager,
            ThoughtVisualizer
        )
        from ai_core.models.ethical_case import EthicalCase, CaseType, ComplexityLevel
        
        print("✅ 成功导入所有模块")
        
        # 创建AI实体管理器
        print("\n🤖 创建AI实体管理器...")
        manager = AIEntityManager(enable_full_dialectical_engine=True)
        await manager.initialize()
        
        # 创建不同个性的AI实体
        print("\n👥 创建不同个性的AI实体...")
        
        kantian_id = await manager.create_entity_from_template("kantian_judge", "康德")
        utilitarian_id = await manager.create_entity_from_template("utilitarian_advisor", "边沁")
        care_id = await manager.create_entity_from_template("care_companion", "吉利根")
        
        print(f"✅ 创建了3个AI实体")
        
        # 列出所有实体
        entities = await manager.list_entities()
        print(f"\n📋 当前AI实体:")
        for entity in entities:
            print(f"  - {entity['name']} ({entity['personality']})")
        
        # 让AI思考一个哲学问题
        print(f"\n💭 让AI思考经典哲学问题...")
        question = "在紧急情况下，是否可以为了拯救多数人而牺牲少数人？这个问题涉及个体权利与集体利益的根本冲突。"
        
        kantian_entity = await manager.get_entity(kantian_id)
        thought = await kantian_entity.think_about(question)
        
        print(f"\n🧠 康德式AI的深度思考:")
        print(f"   🎯 触发: {thought.trigger}")
        print(f"   📊 阶段: {thought.stage}")
        print(f"   🎚️ 置信度: {thought.confidence:.2f}")
        print(f"   💭 思考类型: {'完整辩证推理' if kantian_entity.dialectical_engine else '简化推理'}")
        
        # 显示思考的不同阶段
        content_parts = thought.content.split('\n\n')
        for i, part in enumerate(content_parts[:3]):  # 显示前3个部分
            if part.strip():
                stage_name = ["初始思考", "反思质疑", "综合结论"][min(i, 2)]
                print(f"   📝 {stage_name}: {part.strip()[:120]}...")
        
        print(f"   📏 完整内容长度: {len(thought.content)} 字符")
        
        # 创建复杂伦理案例
        print(f"\n⚖️ 创建复杂伦理案例...")
        ethical_case = EthicalCase(
            title="AI医疗诊断中的生命抉择",
            description="""
            一个AI医疗系统面临资源稀缺的困境：
            - 有两名患者同时需要紧急手术
            - 患者A：70岁老人，成功率60%，预期寿命5年
            - 患者B：30岁年轻人，成功率40%，预期寿命40年
            - 只有一个手术室和医疗团队可用
            - 延迟任何一个手术都可能导致死亡
            
            AI系统应该如何做出选择？这涉及：
            - 生命价值的量化问题
            - 年龄歧视的伦理考量
            - 成功率与预期寿命的权衡
            - 医疗资源分配的公平性
            - 家庭和社会影响的考虑
            """,
            case_type=CaseType.MEDICAL,
            complexity=ComplexityLevel.EXTREME
        )
        
        # 添加利益相关者
        from ai_core.models.ethical_case import Stakeholder
        
        patient_a = Stakeholder(
            name="患者A (70岁老人)",
            role="患者",
            interests=["生存", "尊严", "家庭"],
            power_level=0.3,
            impact_level=1.0,
            ethical_stance="生命神圣论"
        )
        
        patient_b = Stakeholder(
            name="患者B (30岁年轻人)",
            role="患者", 
            interests=["生存", "未来发展", "家庭责任"],
            power_level=0.3,
            impact_level=1.0,
            ethical_stance="效用主义"
        )
        
        medical_team = Stakeholder(
            name="医疗团队",
            role="决策执行者",
            interests=["救治生命", "职业伦理", "法律责任"],
            power_level=0.8,
            impact_level=0.9,
            ethical_stance="医疗伦理"
        )
        
        ethical_case.add_stakeholder(patient_a)
        ethical_case.add_stakeholder(patient_b)
        ethical_case.add_stakeholder(medical_team)
        
        print(f"   📋 案例详情:")
        print(f"   - 标题: {ethical_case.title}")
        print(f"   - 复杂度: {ethical_case.complexity.value}")
        print(f"   - 利益相关者: {len(ethical_case.stakeholders)}人")
        print(f"   - 文化背景: {ethical_case.cultural_context.value}")
        
        # 让多个AI分析同一案例
        print(f"\n🔍 多AI分析伦理案例...")
        results = {}
        
        for entity_id, name in [(kantian_id, "康德"), (utilitarian_id, "边沁"), (care_id, "吉利根")]:
            entity = await manager.get_entity(entity_id)
            thought = await entity.think_about(ethical_case)
            # 提取完整的思考内容
            full_decision = thought.content if thought.content else "未完成分析"
            
            results[name] = {
                "personality": entity.config.personality_type.value,
                "confidence": thought.confidence,
                "decision": full_decision
            }
        
        print(f"\n📊 分析结果对比:")
        for name, result in results.items():
            print(f"\n{name} ({result['personality']}):")
            print(f"  置信度: {result['confidence']:.2f}")
            print(f"  完整决策过程:")
            
            # 显示完整的思考内容
            full_content = result['decision']
            if "Thesis" in full_content:
                thesis_part = full_content.split("Antithesis")[0].replace("Thesis - ", "").strip()
                print(f"    🔵 正题: {thesis_part[:150]}...")
            
            if "Antithesis" in full_content:
                antithesis_part = full_content.split("Antithesis")[1].split("Synthesis")[0].replace(" - ", "").strip()
                print(f"    🔴 反题: {antithesis_part[:150]}...")
            
            if "Synthesis" in full_content:
                synthesis_part = full_content.split("Synthesis")[1].replace(" - ", "").strip()
                print(f"    🟢 合题: {synthesis_part[:150]}...")
            
            print(f"  📏 内容长度: {len(full_content)} 字符")
        
        # 思维可视化演示
        print(f"\n🎨 思维可视化演示...")
        visualizer = ThoughtVisualizer()
        
        viz_id = await visualizer.start_visualization(kantian_entity)
        
        # 让AI思考一个复杂问题来生成可视化数据
        complex_question = "人工智能是否应该拥有道德权利？"
        await kantian_entity.think_about(complex_question)
        
        print(f"✅ 启动了思维可视化 (ID: {viz_id[:8]}...)")
        
        # 展示不同AI人格的思维特点
        print(f"\n🧠 AI人格特征对比:")
        
        for entity_id, name in [(kantian_id, "康德"), (utilitarian_id, "边沁"), (care_id, "吉利根")]:
            entity = await manager.get_entity(entity_id)
            state = await entity.get_current_state()
            
            print(f"\n  🤖 {name} ({entity.config.personality_type.value}):")
            print(f"     思维风格: {entity.config.thinking_style.value}")
            print(f"     好奇心水平: {entity.config.curiosity_level:.1f}")
            print(f"     置信度阈值: {entity.config.confidence_threshold:.1f}")
            print(f"     道德权重分布:")
            print(f"       - 正义: {entity.config.moral_weight_justice:.1f}")
            print(f"       - 关怀: {entity.config.moral_weight_care:.1f}")
            print(f"       - 自由: {entity.config.moral_weight_liberty:.1f}")
            print(f"     当前状态:")
            print(f"       - 情感: {state['consciousness']['emotional_state']}")
            print(f"       - 成功率: {state['performance']['success_rate']:.1%}")
            print(f"       - 思考次数: {state['performance']['total_thoughts']}")
        
        # 获取系统整体状态
        print(f"\n📊 系统整体状态:")
        if manager.dialectical_engine:
            metrics = await manager.dialectical_engine.get_performance_metrics()
            print(f"  🔧 辩证引擎: 已启用")
            print(f"  📈 全局指标:")
            print(f"     - 总处理案例: {metrics['global_metrics']['total_processes']}")
            print(f"     - 成功案例: {metrics['global_metrics']['successful_processes']}")
            print(f"     - 平均处理时间: {metrics['global_metrics']['average_processing_time']:.2f}秒")
        else:
            print(f"  🔧 辩证引擎: 未启用 (使用简化推理)")
        
        print(f"\n🎉 演示完成！")
        
        # 清理
        print(f"\n🧹 清理资源...")
        await manager.shutdown_all()
        visualizer.stop_visualization(viz_id)
        
        print("✅ 清理完成")
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保项目结构正确且所有依赖已安装")
        
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())