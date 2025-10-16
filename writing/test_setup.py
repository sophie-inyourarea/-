"""
测试脚本 - 验证项目设置是否正确
"""
import os
import sys

def test_imports():
    """测试所有模块是否能正确导入"""
    try:
        from data_manager import DataManager
        print("✓ DataManager 导入成功")
    except ImportError as e:
        print(f"✗ DataManager 导入失败: {e}")
        return False
    
    try:
        from ai_agent import AIAgent
        print("✓ AIAgent 导入成功")
    except ImportError as e:
        print(f"✗ AIAgent 导入失败: {e}")
        return False
    
    try:
        from user_interface import UserInterface
        print("✓ UserInterface 导入成功")
    except ImportError as e:
        print(f"✗ UserInterface 导入失败: {e}")
        return False
    
    try:
        from deduplication import DeduplicationEngine
        print("✓ DeduplicationEngine 导入成功")
    except ImportError as e:
        print(f"✗ DeduplicationEngine 导入失败: {e}")
        return False
    
    return True

def test_data_manager():
    """测试数据管理器"""
    try:
        from data_manager import DataManager
        dm = DataManager("data/test_user_profile.json")
        
        # 测试基本功能
        data = dm.load_data()
        assert "user_preferences" in data
        assert "restriction_rules" in data
        print("✓ DataManager 基本功能正常")
        
        # 清理测试文件
        if os.path.exists("data/test_user_profile.json"):
            os.remove("data/test_user_profile.json")
        
        return True
    except Exception as e:
        print(f"✗ DataManager 测试失败: {e}")
        return False

def test_api_key():
    """测试API密钥设置"""
    api_key = os.getenv("VOLCANO_API_KEY")
    if api_key and api_key != "your_volcano_api_key_here":
        print("✓ 火山方舟API密钥已设置")
        return True
    else:
        print("✗ 火山方舟API密钥未设置")
        print("  请创建 .env 文件并设置 VOLCANO_API_KEY")
        return False

def main():
    """运行所有测试"""
    print("开始测试项目设置...")
    print("=" * 50)
    
    all_passed = True
    
    # 测试导入
    print("\n1. 测试模块导入:")
    if not test_imports():
        all_passed = False
    
    # 测试数据管理器
    print("\n2. 测试数据管理器:")
    if not test_data_manager():
        all_passed = False
    
    # 测试API密钥
    print("\n3. 测试API密钥:")
    if not test_api_key():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ 所有测试通过！项目设置正确。")
        print("\n可以运行以下命令启动程序:")
        print("python main.py")
    else:
        print("✗ 部分测试失败，请检查上述错误信息。")
        sys.exit(1)

if __name__ == "__main__":
    main()
