#!/usr/bin/env python3
"""
测试服务器配置
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试导入"""
    print("🧪 测试导入...")
    
    try:
        from backend.config import Settings
        print("✅ 成功导入 Settings")
        
        settings = Settings()
        print(f"✅ 默认端口: {settings.port}")
        print(f"✅ Neo4j配置: {settings.neo4j_config}")
        
        from ai_core.knowledge_graph import KnowledgeGraphManager
        print("✅ 成功导入 KnowledgeGraphManager")
        
        # 测试知识图谱管理器初始化
        kg_manager = KnowledgeGraphManager(settings.neo4j_config)
        print("✅ 成功创建 KnowledgeGraphManager 实例")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔧 测试服务器配置...")
    
    if test_imports():
        print("\n🎉 所有测试通过！")
        print("💡 现在可以运行: python start_server.py")
        return 0
    else:
        print("\n❌ 测试失败")
        return 1

if __name__ == "__main__":
    exit(main())