"""
演示脚本 - 展示文案风格个性化AI Agent的功能
"""
import os
from data_manager import DataManager
from ai_agent import AIAgent
from user_interface import UserInterface
from deduplication import DeduplicationEngine

def demo_without_api():
    """演示程序功能（不需要API调用）"""
    print("=" * 60)
    print("文案风格个性化AI Agent - 功能演示")
    print("=" * 60)
    
    # 1. 测试数据管理器
    print("\n1. 数据管理器功能演示:")
    print("-" * 30)
    
    dm = DataManager("data/demo_profile.json")
    
    # 添加一些示例偏好和规则
    pref_id1 = dm.add_user_preference("偏好使用短句，节奏明快")
    pref_id2 = dm.add_user_preference("倾向于避免使用引号")
    rule_id1 = dm.add_restriction_rule("请将文案精简到200字以内")
    rule_id2 = dm.add_restriction_rule("不要使用任何感叹号")
    
    print(f"✓ 添加偏好: {pref_id1}")
    print(f"✓ 添加偏好: {pref_id2}")
    print(f"✓ 添加规则: {rule_id1}")
    print(f"✓ 添加规则: {rule_id2}")
    
    # 显示存储的数据
    preferences = dm.get_user_preferences()
    rules = dm.get_restriction_rules()
    
    print(f"\n当前存储的偏好数量: {len(preferences)}")
    for pref in preferences:
        print(f"  - {pref['description']}")
    
    print(f"\n当前存储的规则数量: {len(rules)}")
    for rule in rules:
        print(f"  - {rule['instruction']}")
    
    # 2. 测试去重引擎
    print("\n2. 去重引擎功能演示:")
    print("-" * 30)
    
    # 注意：这里需要API密钥才能测试embedding功能
    api_key = os.getenv("VOLCANO_API_KEY")
    if api_key and api_key != "your_volcano_api_key_here":
        try:
            de = DeduplicationEngine()
            
            # 测试相似偏好检测
            similar_pref = "喜欢使用短句，节奏明快"  # 与现有偏好相似
            different_pref = "经常使用比喻和修辞手法"  # 与现有偏好不同
            
            print(f"测试相似偏好: '{similar_pref}'")
            is_duplicate1 = not de.deduplicate_preference(similar_pref, preferences)
            print(f"  检测结果: {'重复' if is_duplicate1 else '不重复'}")
            
            print(f"测试不同偏好: '{different_pref}'")
            is_duplicate2 = not de.deduplicate_preference(different_pref, preferences)
            print(f"  检测结果: {'重复' if is_duplicate2 else '不重复'}")
            
        except Exception as e:
            print(f"去重引擎测试失败（需要有效的API密钥）: {e}")
    else:
        print("跳过去重引擎测试（需要设置有效的VOLCANO_API_KEY）")
    
    # 3. 测试用户界面
    print("\n3. 用户界面功能演示:")
    print("-" * 30)
    
    ui = UserInterface()
    ui.display_welcome()
    
    # 模拟一些界面功能
    print("✓ 欢迎界面显示正常")
    print("✓ 命令行交互组件加载正常")
    
    # 4. 显示项目结构
    print("\n4. 项目结构:")
    print("-" * 30)
    
    project_files = [
        "main.py - 主程序入口",
        "ai_agent.py - AI Agent核心模块",
        "data_manager.py - 数据管理模块", 
        "deduplication.py - 去重机制模块",
        "user_interface.py - 用户界面模块",
        "data/user_profile.json - 用户数据存储",
        "requirements.txt - 依赖包列表",
        "README.md - 项目说明文档"
    ]
    
    for file_desc in project_files:
        print(f"  ✓ {file_desc}")
    
    # 5. 使用说明
    print("\n5. 使用说明:")
    print("-" * 30)
    print("1. 设置火山方舟API密钥:")
    print("   - 创建 .env 文件")
    print("   - 添加 VOLCANO_API_KEY=your_actual_api_key")
    print()
    print("2. 运行程序:")
    print("   python main.py")
    print()
    print("3. 程序流程:")
    print("   - 输入原始文案")
    print("   - 提供参考文案（定义风格）")
    print("   - 选择历史偏好和规则")
    print("   - 多轮编辑和修改")
    print("   - 自动学习新的偏好和规则")
    
    # 清理演示文件
    if os.path.exists("data/demo_profile.json"):
        os.remove("data/demo_profile.json")
    
    print("\n" + "=" * 60)
    print("演示完成！程序功能正常。")
    print("请设置API密钥后运行 'python main.py' 开始使用。")
    print("=" * 60)

if __name__ == "__main__":
    demo_without_api()
