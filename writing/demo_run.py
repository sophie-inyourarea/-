#!/usr/bin/env python3
"""
演示运行脚本 - 展示火山方舟集成的文案风格个性化AI Agent功能
"""
import os
import sys

# 设置环境变量
os.environ["VOLCANO_API_KEY"] = "your_volcano_api_key_here"

from data_manager import DataManager
from ai_agent import AIAgent
from user_interface import UserInterface
from deduplication import DeduplicationEngine

def demo_ai_agent():
    """演示AI Agent功能"""
    print("🤖 AI Agent功能演示")
    print("=" * 50)
    
    try:
        # 初始化AI Agent
        agent = AIAgent()
        print("✓ AI Agent初始化成功")
        
        # 模拟文案生成
        user_input = "这是一个关于人工智能的简单介绍，需要优化成更有吸引力的文案。"
        reference_texts = [
            "在这个快速变化的时代，我们每个人都在寻找属于自己的声音。",
            "技术不是冰冷的工具，而是连接人心的桥梁。"
        ]
        
        print(f"\n📝 原始文案: {user_input}")
        print(f"📚 参考文案: {reference_texts[0]}")
        
        # 生成风格化初稿
        print("\n🔄 正在生成风格化初稿...")
        try:
            draft = agent.generate_style_draft(user_input, reference_texts)
            print(f"✓ 生成成功: {draft[:100]}...")
        except Exception as e:
            print(f"⚠️ 生成失败（可能需要网络连接）: {e}")
            draft = "这是一个关于人工智能的简单介绍，需要优化成更有吸引力的文案。"
        
        # 测试偏好应用
        print("\n🎨 测试偏好应用...")
        preferences = [
            {"description": "立场去权威化：有意识地将表达视角从客观、抽离的第三方评论者，转变为主观、沉浸的第一亲历者，以增强真实感和信任度。"},
            {"description": "沟通导向的对话感：根本目的在于实现有效沟通而非单向输出。因此着力削弱说教感和批判性，营造一种平等、分享式的对话语气，以拉近与读者的心理距离。"}
        ]
        
        try:
            modified_draft = agent.apply_preferences(draft, preferences)
            print(f"✓ 偏好应用成功: {modified_draft[:100]}...")
        except Exception as e:
            print(f"⚠️ 偏好应用失败: {e}")
        
        # 测试规则应用
        print("\n📋 测试规则应用...")
        rules = [
            {"instruction": "不要加入那么多破折号和双引号"}
        ]
        
        try:
            final_draft = agent.apply_restrictions(modified_draft, rules)
            print(f"✓ 规则应用成功: {final_draft[:100]}...")
        except Exception as e:
            print(f"⚠️ 规则应用失败: {e}")
            
    except Exception as e:
        print(f"❌ AI Agent初始化失败: {e}")

def demo_data_manager():
    """演示数据管理器功能"""
    print("\n💾 数据管理器功能演示")
    print("=" * 50)
    
    try:
        dm = DataManager("data/demo_profile.json")
        
        # 添加示例数据
        pref_id = dm.add_user_preference("喜欢使用比喻和修辞手法")
        rule_id = dm.add_restriction_rule("保持文案简洁明了")
        
        print(f"✓ 添加偏好: {pref_id}")
        print(f"✓ 添加规则: {rule_id}")
        
        # 显示数据
        preferences = dm.get_user_preferences()
        rules = dm.get_restriction_rules()
        
        print(f"\n📊 当前数据统计:")
        print(f"  - 偏好数量: {len(preferences)}")
        print(f"  - 规则数量: {len(rules)}")
        
        for i, pref in enumerate(preferences, 1):
            print(f"  {i}. {pref['description']}")
        
        for i, rule in enumerate(rules, 1):
            print(f"  {i}. {rule['instruction']}")
            
    except Exception as e:
        print(f"❌ 数据管理器演示失败: {e}")

def demo_deduplication():
    """演示去重引擎功能"""
    print("\n🔄 去重引擎功能演示")
    print("=" * 50)
    
    try:
        de = DeduplicationEngine()
        
        # 测试相似文本检测
        text1 = "喜欢使用短句，节奏明快"
        text2 = "偏好使用短句，节奏明快"
        text3 = "经常使用比喻和修辞手法"
        
        similarity1 = de.calculate_similarity(text1, text2)
        similarity2 = de.calculate_similarity(text1, text3)
        
        print(f"✓ 文本相似度计算成功")
        print(f"  - '{text1}' vs '{text2}': {similarity1:.3f}")
        print(f"  - '{text1}' vs '{text3}': {similarity2:.3f}")
        
        # 测试去重功能
        existing_preferences = [
            {"description": "喜欢使用短句，节奏明快"}
        ]
        
        is_duplicate1 = not de.deduplicate_preference(text2, existing_preferences)
        is_duplicate2 = not de.deduplicate_preference(text3, existing_preferences)
        
        print(f"\n✓ 去重检测结果:")
        print(f"  - '{text2}' 是否重复: {'是' if is_duplicate1 else '否'}")
        print(f"  - '{text3}' 是否重复: {'是' if is_duplicate2 else '否'}")
        
    except Exception as e:
        print(f"❌ 去重引擎演示失败: {e}")

def demo_user_interface():
    """演示用户界面功能"""
    print("\n🖥️ 用户界面功能演示")
    print("=" * 50)
    
    try:
        ui = UserInterface()
        ui.display_welcome()
        print("✓ 欢迎界面显示正常")
        
        # 模拟显示文案
        sample_draft = "这是一个关于人工智能的简单介绍，需要优化成更有吸引力的文案。"
        ui.display_draft(sample_draft, "示例文案")
        print("✓ 文案显示功能正常")
        
    except Exception as e:
        print(f"❌ 用户界面演示失败: {e}")

def main():
    """主演示函数"""
    print("🚀 文案风格个性化AI Agent - 功能演示")
    print("=" * 60)
    print("使用火山方舟大模型: doubao-seed-1.6-250615")
    print("=" * 60)
    
    # 运行各个模块的演示
    demo_data_manager()
    demo_deduplication()
    demo_user_interface()
    demo_ai_agent()
    
    print("\n" + "=" * 60)
    print("🎉 演示完成！")
    print("\n📋 项目功能总结:")
    print("  ✅ 数据管理 - 本地JSON存储用户偏好和规则")
    print("  ✅ 智能去重 - TF-IDF向量化相似度检测")
    print("  ✅ 用户界面 - 美观的命令行交互界面")
    print("  ✅ AI生成 - 火山方舟大模型文案生成")
    print("  ✅ 学习闭环 - 自动学习用户写作偏好")
    
    print("\n🚀 启动完整程序:")
    print("  python main.py")
    print("  (需要交互式终端环境)")
    
    print("\n📚 更多信息:")
    print("  - README.md: 详细使用说明")
    print("  - VOLCANO_INTEGRATION.md: 火山方舟集成说明")
    print("  - PROJECT_SUMMARY.md: 项目总结")
    print("=" * 60)

if __name__ == "__main__":
    main()
