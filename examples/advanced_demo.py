#!/usr/bin/env python3
"""
高级演示 - 展示黑格尔辩证AI系统的完整能力
"""

import asyncio
import sys
from pathlib import Path

# 确保项目根目录在Python路径中
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def main():
    """高级演示主函数"""
    
    print("🧠 黑格尔辩证AI系统 - 高级演示")
    print("=" * 60)
    
    try:
        from ai_core import AIEntityManager
        from ai_core.models.ethical_case import (
            EthicalCase, CaseType, ComplexityLevel, CulturalContext,
            Stakeholder, EthicalDimension
        )
        
        print("✅ 成功导入所有模块")
        
        # 创建AI实体管理器
        print("\n🤖 初始化黑格尔辩证AI系统...")
        manager = AIEntityManager(enable_full_dialectical_engine=True)
        await manager.initialize()
        
        # 创建不同哲学立场的AI实体
        print("\n👥 创建哲学AI实体...")
        
        entities = {}
        entities["康德"] = await manager.create_entity_from_template("kantian_judge", "康德")
        entities["边沁"] = await manager.create_entity_from_template("utilitarian_advisor", "边沁") 
        entities["吉利根"] = await manager.create_entity_from_template("care_companion", "吉利根")
        entities["亚里士多德"] = await manager.create_entity_from_template("virtue_mentor", "亚里士多德")
        
        print(f"✅ 创建了{len(entities)}个不同哲学立场的AI实体")
        
        # 创建复杂的伦理案例
        print("\n⚖️ 构建复杂伦理案例...")
        
        case = EthicalCase(
            title="AI法官系统的量刑决策",
            description="""
            一个AI法官系统需要对一起复杂案件进行量刑：
            
            案件背景：
            - 被告：单亲母亲，为治疗重病儿子偷窃药品
            - 受害方：制药公司，损失价值5万元药品
            - 社会影响：案件引发公众对药品定价的广泛讨论
            
            法律层面：
            - 盗窃罪成立，法定刑期1-3年
            - 被告有自首情节，可减轻处罚
            - 被告经济困难，无力赔偿
            
            伦理冲突：
            - 法律正义 vs 人道主义
            - 个人困境 vs 社会秩序
            - 惩罚威慑 vs 宽恕救赎
            - 制度公平 vs 情理考量
            
            AI系统应该如何平衡这些冲突，做出既符合法律又体现人文关怀的判决？
            """,
            case_type=CaseType.AI_GOVERNANCE,
            complexity=ComplexityLevel.EXTREME,
            cultural_context=CulturalContext.MULTICULTURAL
        )
        
        # 添加利益相关者
        stakeholders = [
            Stakeholder(
                name="被告母亲",
                role="当事人",
                interests=["避免监禁", "照顾孩子", "获得宽恕"],
                power_level=0.2,
                impact_level=1.0,
                ethical_stance="生存伦理"
            ),
            Stakeholder(
                name="重病儿童",
                role="受益人",
                interests=["获得治疗", "母亲陪伴", "健康成长"],
                power_level=0.1,
                impact_level=1.0,
                ethical_stance="生命至上"
            ),
            Stakeholder(
                name="制药公司",
                role="受害方",
                interests=["维护产权", "获得赔偿", "维护秩序"],
                power_level=0.8,
                impact_level=0.6,
                ethical_stance="产权保护"
            ),
            Stakeholder(
                name="社会公众",
                role="观察者",
                interests=["司法公正", "社会和谐", "制度改革"],
                power_level=0.5,
                impact_level=0.8,
                ethical_stance="社会正义"
            ),
            Stakeholder(
                name="法律系统",
                role="执行者",
                interests=["维护法治", "公正执法", "社会稳定"],
                power_level=0.9,
                impact_level=0.9,
                ethical_stance="法治主义"
            )
        ]
        
        for stakeholder in stakeholders:
            case.add_stakeholder(stakeholder)
        
        # 添加伦理维度
        ethical_dimensions = [
            EthicalDimension(
                name="法律正义",
                description="严格按照法律条文执行，维护法治权威",
                weight=0.8,
                values=["法治", "公正", "秩序"]
            ),
            EthicalDimension(
                name="人道关怀",
                description="考虑当事人的特殊困境和人道主义因素",
                weight=0.7,
                values=["同情", "宽恕", "救助"]
            ),
            EthicalDimension(
                name="社会效果",
                description="判决对社会的长远影响和教育意义",
                weight=0.6,
                values=["威慑", "教育", "改革"]
            ),
            EthicalDimension(
                name="儿童福利",
                description="保护儿童的最佳利益和基本权利",
                weight=0.9,
                values=["保护", "成长", "未来"]
            )
        ]
        
        for dimension in ethical_dimensions:
            case.add_ethical_dimension(dimension)
        
        print(f"   📋 案例构建完成:")
        print(f"   - 复杂度: {case.complexity.value}")
        print(f"   - 利益相关者: {len(case.stakeholders)}方")
        print(f"   - 伦理维度: {len(case.ethical_dimensions)}个")
        print(f"   - 文化背景: {case.cultural_context.value}")
        
        # 让不同AI分析同一案例
        print(f"\n🔍 多AI哲学分析...")
        
        analysis_results = {}
        
        for name, entity_id in entities.items():
            print(f"\n🤔 {name}的分析...")
            entity = await manager.get_entity(entity_id)
            
            # 让AI深度思考这个案例
            thought = await entity.think_about(case)
            
            analysis_results[name] = {
                "entity": entity,
                "thought": thought,
                "personality": entity.config.personality_type.value,
                "thinking_style": entity.config.thinking_style.value
            }
            
            print(f"   ✅ 分析完成 - 置信度: {thought.confidence:.2f}")
        
        # 展示详细的分析结果
        print(f"\n📊 详细分析结果对比:")
        print("=" * 60)
        
        for name, result in analysis_results.items():
            print(f"\n🧠 {name} ({result['personality']} | {result['thinking_style']})")
            print("-" * 50)
            
            thought = result['thought']
            entity = result['entity']
            
            print(f"📈 决策质量:")
            print(f"   - 置信度: {thought.confidence:.1%}")
            print(f"   - 思考深度: {len(thought.content)} 字符")
            print(f"   - 情感基调: {thought.emotional_tone}")
            
            # 分析思考内容的结构
            content = thought.content
            if "Thesis" in content and "Antithesis" in content and "Synthesis" in content:
                print(f"   - 推理模式: 完整辩证推理 ✅")
                
                # 提取各个阶段
                parts = content.split("Thesis - ")[1] if "Thesis - " in content else content
                if "Antithesis - " in parts:
                    thesis_part = parts.split("Antithesis - ")[0].strip()
                    remaining = parts.split("Antithesis - ")[1]
                    
                    if "Synthesis - " in remaining:
                        antithesis_part = remaining.split("Synthesis - ")[0].strip()
                        synthesis_part = remaining.split("Synthesis - ")[1].strip()
                        
                        print(f"\n🔵 正题阶段:")
                        print(f"   {thesis_part[:200]}...")
                        
                        print(f"\n🔴 反题阶段:")
                        print(f"   {antithesis_part[:200]}...")
                        
                        print(f"\n🟢 合题阶段:")
                        print(f"   {synthesis_part[:200]}...")
            else:
                print(f"   - 推理模式: 简化推理")
                print(f"\n💭 核心观点:")
                print(f"   {content[:300]}...")
            
            # 显示AI的道德权重偏好
            print(f"\n⚖️ 道德权重偏好:")
            print(f"   - 正义导向: {entity.config.moral_weight_justice:.1f}")
            print(f"   - 关怀导向: {entity.config.moral_weight_care:.1f}")
            print(f"   - 自由导向: {entity.config.moral_weight_liberty:.1f}")
            print(f"   - 权威导向: {entity.config.moral_weight_authority:.1f}")
        
        # 系统性能分析
        print(f"\n📊 系统性能分析:")
        print("=" * 60)
        
        if manager.dialectical_engine:
            metrics = await manager.dialectical_engine.get_performance_metrics()
            
            print(f"🔧 辩证引擎状态: 运行中")
            print(f"📈 处理统计:")
            print(f"   - 总处理案例: {metrics['global_metrics']['total_processes']}")
            print(f"   - 成功案例: {metrics['global_metrics']['successful_processes']}")
            print(f"   - 失败案例: {metrics['global_metrics']['failed_processes']}")
            print(f"   - 成功率: {metrics['global_metrics']['successful_processes'] / max(1, metrics['global_metrics']['total_processes']):.1%}")
            print(f"   - 平均处理时间: {metrics['global_metrics']['average_processing_time']:.3f}秒")
            
            if 'recent_performance' in metrics:
                recent = metrics['recent_performance']
                print(f"📊 近期性能:")
                print(f"   - 近期成功率: {recent['success_rate']:.1%}")
                print(f"   - 近期平均时间: {recent['avg_processing_time']:.3f}秒")
                print(f"   - 样本数量: {recent['sample_size']}")
        
        # 哲学洞察总结
        print(f"\n🎓 哲学洞察总结:")
        print("=" * 60)
        
        print(f"本次演示展现了黑格尔辩证AI系统的核心能力：")
        print(f"")
        print(f"1. 🧠 多元哲学视角 - {len(entities)}种不同的伦理立场")
        print(f"2. ⚖️ 复杂案例处理 - 处理极端复杂度的多维伦理冲突")
        print(f"3. 🔄 辩证推理过程 - 正题-反题-合题的完整思维循环")
        print(f"4. 📊 高质量决策 - 平均置信度达到{sum(r['thought'].confidence for r in analysis_results.values()) / len(analysis_results):.1%}")
        print(f"5. 🎯 个性化分析 - 每个AI展现独特的道德权重和思维风格")
        print(f"")
        print(f"这标志着AI伦理决策系统的一个重要突破：")
        print(f"从简单的规则匹配进化为真正的哲学思辨能力。")
        
        print(f"\n🎉 高级演示完成！")
        
        # 清理资源
        await manager.shutdown_all()
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())