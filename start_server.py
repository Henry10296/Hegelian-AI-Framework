#!/usr/bin/env python3
"""
启动服务器脚本 - 自动检测可用端口
"""

import socket
import sys
import os
import uvicorn
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def find_free_port(start_port=8000, max_port=8100):
    """查找可用端口"""
    for port in range(start_port, max_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No free port found between {start_port} and {max_port}")

def main():
    """主函数"""
    print("🚀 启动Hegelian AI Framework服务器...")
    
    # 查找可用端口
    try:
        port = find_free_port()
        print(f"📡 使用端口: {port}")
    except RuntimeError as e:
        print(f"❌ 错误: {e}")
        return 1
    
    # 设置环境变量
    os.environ["PORT"] = str(port)
    
    try:
        # 启动服务器
        uvicorn.run(
            "backend.main:app",
            host="localhost",
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())