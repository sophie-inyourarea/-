#!/usr/bin/env python3
"""
快速启动脚本 - 检查环境并启动文案风格个性化AI Agent
"""
import os
import sys

def check_environment():
    """检查运行环境"""
    print("正在检查运行环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 错误：需要Python 3.8或更高版本")
        print(f"   当前版本：{sys.version}")
        return False
    
    print(f"✓ Python版本：{sys.version.split()[0]}")
    
    # 检查依赖包
    required_packages = ['openai', 'questionary', 'rich', 'numpy', 'sklearn', 'dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                import sklearn
            elif package == 'dotenv':
                import dotenv
            else:
                __import__(package)
            print(f"✓ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print(f"\n请安装缺失的依赖包：")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    # 检查API密钥
    api_key = os.getenv("VOLCANO_API_KEY")
    if not api_key or api_key == "your_volcano_api_key_here":
        print("\n⚠️  警告：未设置火山方舟API密钥")
        print("请创建 .env 文件并设置您的API密钥：")
        print("VOLCANO_API_KEY=your_actual_api_key")
        print("\n或者设置环境变量：")
        print("export VOLCANO_API_KEY=your_actual_api_key")
        return False
    
    print("✓ 火山方舟API密钥已设置")
    
    # 检查数据目录
    if not os.path.exists("data"):
        os.makedirs("data")
        print("✓ 创建数据目录")
    
    if not os.path.exists("data/user_profile.json"):
        with open("data/user_profile.json", "w", encoding="utf-8") as f:
            import json
            json.dump({"user_preferences": [], "restriction_rules": []}, f, ensure_ascii=False, indent=2)
        print("✓ 创建用户配置文件")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("文案风格个性化AI Agent - 启动检查")
    print("=" * 60)
    
    if not check_environment():
        print("\n❌ 环境检查失败，请解决上述问题后重试")
        sys.exit(1)
    
    print("\n✅ 环境检查通过！")
    print("\n正在启动程序...")
    print("=" * 60)
    
    # 启动主程序
    try:
        from main import main as run_main
        run_main()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，再见！")
    except Exception as e:
        print(f"\n❌ 程序运行出错：{e}")
        print("请检查错误信息并重试")
        sys.exit(1)

if __name__ == "__main__":
    main()
