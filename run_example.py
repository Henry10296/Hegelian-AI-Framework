#!/usr/bin/env python3
"""
示例运行脚本 - 在PyCharm中运行此文件
"""

import sys
import os
from pathlib import Path

# 确保项目根目录在Python路径中
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """主函数 - 演示如何使用AI核心模块"""
    
    print("🚀 启动Hegelian AI框架示例...")
    
    try:
        # 导入模型
        from ai_core.models import (
            EthicalCase, 
            DecisionResult, 
            Stakeholder, 
            EthicalDimension,
            CaseType,
            ComplexityLevel
        )
        
        print("✅ 成功导入所有模型")
        
        # 创建一个示例伦理案例
        case = EthicalCase(
            title="自动驾驶汽车道德决策",
            description="自动驾驶汽车在紧急情况下应该如何选择保护乘客还是行人？",
            case_type=CaseType.AUTONOMOUS_VEHICLE,
            complexity=ComplexityLevel.HIGH
        )
        
        # 添加利益相关者
        passenger = Stakeholder(
            name="乘客",
            role="车内人员",
            interests=["安全", "生存"],
            power_level=0.3,
            impact_level=0.9
        )
        
        pedestrian = Stakeholder(
            name="行人",
            role="道路使用者",
            interests=["安全", "生存"],
            power_level=0.1,
            impact_level=0.9
        )
        
        case.add_stakeholder(passenger)
        case.add_stakeholder(pedestrian)
        
        # 添加伦理维度
        safety_dimension = EthicalDimension(
            name="安全原则",
            description="保护生命安全的道德义务",
            weight=0.9,
            values=["生命价值", "伤害最小化"]
        )
        
        case.add_ethical_dimension(safety_dimension)
        
        print(f"\n📋 创建的伦理案例:")
        print(f"   标题: {case.title}")
        print(f"   类型: {case.case_type.value}")
        print(f"   复杂度: {case.complexity.value}")
        print(f"   利益相关者数量: {len(case.stakeholders)}")
        print(f"   伦理维度数量: {len(case.ethical_dimensions)}")
        
        # 验证案例
        validation_errors = case.validate()
        if validation_errors:
            print(f"\n⚠️ 验证错误: {validation_errors}")
        else:
            print("\n✅ 案例验证通过")
        
        # 显示复杂度分数
        complexity_score = case.get_complexity_score()
        print(f"\n📊 复杂度分数: {complexity_score:.2f}")
        
        # 显示伦理冲突
        tensions = case.get_ethical_tensions()
        if tensions:
            print(f"\n⚡ 发现的伦理冲突:")
            for tension in tensions:
                print(f"   - {tension}")
        
        print("\n🎉 示例运行成功！")
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("\n💡 解决方案:")
        print("1. 确保在PyCharm中打开了正确的项目根目录")
        print("2. 检查Python解释器配置")
        print("3. 右键点击项目根目录 -> Mark Directory as -> Sources Root")
        
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()