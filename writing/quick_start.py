#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本 - 文案风格个性化AI Agent
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🎨 文案风格个性化AI Agent                    ║
║                                                              ║
║  基于大语言模型的个性化文案生成系统                              ║
║  支持Web界面和命令行，能够学习用户写作偏好                        ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_requirements():
    """检查依赖是否安装"""
    print("🔍 检查依赖...")
    try:
        import flask
        import volcenginesdkarkruntime
        import numpy
        import sklearn
        import questionary
        import rich
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_env_file():
    """检查环境变量文件"""
    print("🔍 检查环境变量...")
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  未找到 .env 文件")
        print("📝 正在创建 .env 文件...")
        
        # 复制示例文件
        example_file = Path("env_example.txt")
        if example_file.exists():
            with open(example_file, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ 已创建 .env 文件")
            print("⚠️  请编辑 .env 文件，填入您的火山方舟API密钥")
            return False
        else:
            print("❌ 未找到 env_example.txt 文件")
            return False
    else:
        print("✅ .env 文件存在")
        return True

def check_api_key():
    """检查API密钥"""
    print("🔍 检查API密钥...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("VOLCANO_API_KEY")
        if api_key and api_key != "your_volcano_api_key_here":
            print("✅ API密钥已设置")
            return True
        else:
            print("❌ API密钥未设置或使用默认值")
            print("请编辑 .env 文件，设置正确的 VOLCANO_API_KEY")
            return False
    except ImportError:
        print("❌ 无法加载环境变量")
        return False

def create_data_directory():
    """创建数据目录"""
    print("🔍 检查数据目录...")
    data_dir = Path("data")
    if not data_dir.exists():
        print("📁 创建数据目录...")
        data_dir.mkdir()
    
    # 检查用户配置文件
    user_profile = data_dir / "user_profile.json"
    if not user_profile.exists():
        print("📝 创建用户配置文件...")
        # 复制演示配置文件
        demo_profile = data_dir / "demo_profile.json"
        if demo_profile.exists():
            with open(demo_profile, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(user_profile, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ 已创建用户配置文件")
        else:
            # 创建空配置文件
            empty_config = '{"user_preferences": [], "restriction_rules": []}'
            with open(user_profile, 'w', encoding='utf-8') as f:
                f.write(empty_config)
            print("✅ 已创建空用户配置文件")
    else:
        print("✅ 用户配置文件存在")

def show_menu():
    """显示菜单"""
    print("\n🚀 选择启动方式:")
    print("1. 🌐 Web界面 (推荐)")
    print("2. 💻 命令行界面")
    print("3. 🎬 演示模式")
    print("4. 🧪 测试设置")
    print("5. ❌ 退出")
    
    while True:
        try:
            choice = input("\n请输入选择 (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("❌ 请输入有效选择 (1-5)")
        except KeyboardInterrupt:
            print("\n👋 再见!")
            sys.exit(0)

def start_web_interface():
    """启动Web界面"""
    print("\n🌐 启动Web界面...")
    print("📱 请在浏览器中访问: http://localhost:8080")
    print("🛑 按 Ctrl+C 停止服务")
    
    try:
        # 尝试自动打开浏览器
        time.sleep(2)
        webbrowser.open('http://localhost:8080')
    except:
        pass
    
    try:
        subprocess.run([sys.executable, "web_interface.py"])
    except KeyboardInterrupt:
        print("\n👋 Web服务已停止")

def start_cli():
    """启动命令行界面"""
    print("\n💻 启动命令行界面...")
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 命令行界面已退出")

def start_demo():
    """启动演示模式"""
    print("\n🎬 启动演示模式...")
    try:
        subprocess.run([sys.executable, "demo_run.py"])
    except KeyboardInterrupt:
        print("\n👋 演示已结束")

def run_tests():
    """运行测试"""
    print("\n🧪 运行测试...")
    try:
        subprocess.run([sys.executable, "test_setup.py"])
    except KeyboardInterrupt:
        print("\n👋 测试已停止")

def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    if not check_requirements():
        return
    
    if not check_env_file():
        return
    
    if not check_api_key():
        return
    
    create_data_directory()
    
    print("\n✅ 环境检查完成!")
    
    # 显示菜单
    while True:
        choice = show_menu()
        
        if choice == '1':
            start_web_interface()
        elif choice == '2':
            start_cli()
        elif choice == '3':
            start_demo()
        elif choice == '4':
            run_tests()
        elif choice == '5':
            print("👋 再见!")
            break
        
        if choice != '5':
            input("\n按回车键继续...")

if __name__ == "__main__":
    main()
