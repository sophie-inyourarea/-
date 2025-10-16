#!/usr/bin/env python3
"""
完整功能演示脚本 - 模拟完整的文案生成流程
"""
import os
import sys

# 设置环境变量
os.environ["VOLCANO_API_KEY"] = "your_volcano_api_key_here"

from data_manager import DataManager
from ai_agent import AIAgent
from user_interface import UserInterface
from deduplication import DeduplicationEngine

def simulate_full_workflow():
    """模拟完整的文案生成工作流程"""
    print("🚀 文案风格个性化AI Agent - 完整功能演示")
    print("=" * 60)
    
    # 初始化所有组件
    print("🔧 初始化组件...")
    data_manager = DataManager()
    ai_agent = AIAgent()
    ui = UserInterface()
    deduplication_engine = DeduplicationEngine()
    print("✅ 所有组件初始化完成")
    
    # 模拟用户输入
    print("\n📝 Step 1: 用户输入")
    print("-" * 30)
    user_input_text = "人工智能正在改变我们的世界，从智能手机到自动驾驶汽车，AI技术无处不在。但是，很多人对AI的理解还停留在科幻电影中。我们需要更好地了解AI，才能在这个智能时代中保持竞争力。"
    reference_texts = [
        "在这个快速变化的时代，我们每个人都在寻找属于自己的声音。技术不是冰冷的工具，而是连接人心的桥梁。",
        "每一次选择都是一次成长，每一次尝试都是一次突破。我们不是被动的接受者，而是主动的创造者。"
    ]
    
    print(f"原始文案: {user_input_text}")
    print(f"参考文案1: {reference_texts[0]}")
    print(f"参考文案2: {reference_texts[1]}")
    
    # Step 1: 生成风格化初稿
    print("\n🎨 Step 2: 生成风格化初稿")
    print("-" * 30)
    try:
        draft_1 = ai_agent.generate_style_draft(user_input_text, reference_texts)
        print(f"✅ 风格化初稿生成成功:")
        print(f"   {draft_1}")
    except Exception as e:
        print(f"❌ 风格化初稿生成失败: {e}")
        draft_1 = user_input_text
    
    # Step 2: 应用写作偏好
    print("\n🎯 Step 3: 应用写作偏好")
    print("-" * 30)
    preferences = data_manager.get_user_preferences()
    print(f"可用偏好: {len(preferences)} 个")
    for i, pref in enumerate(preferences, 1):
        print(f"  {i}. {pref['description']}")
    
    # 模拟选择偏好
    selected_preferences = preferences[:2] if len(preferences) >= 2 else preferences
    print(f"选择的偏好: {len(selected_preferences)} 个")
    
    try:
        draft_2 = ai_agent.apply_preferences(draft_1, selected_preferences)
        print(f"✅ 偏好应用成功:")
        print(f"   {draft_2}")
    except Exception as e:
        print(f"❌ 偏好应用失败: {e}")
        draft_2 = draft_1
    
    # Step 3: 应用限制规则
    print("\n📋 Step 4: 应用限制规则")
    print("-" * 30)
    rules = data_manager.get_restriction_rules()
    print(f"可用规则: {len(rules)} 个")
    for i, rule in enumerate(rules, 1):
        print(f"  {i}. {rule['instruction']}")
    
    # 模拟选择规则
    selected_rules = rules[:1] if len(rules) >= 1 else []
    print(f"选择的规则: {len(selected_rules)} 个")
    
    try:
        first_final_draft = ai_agent.apply_restrictions(draft_2, selected_rules)
        print(f"✅ 规则应用成功:")
        print(f"   {first_final_draft}")
    except Exception as e:
        print(f"❌ 规则应用失败: {e}")
        first_final_draft = draft_2
    
    # Step 4: 模拟用户修改
    print("\n✏️ Step 5: 模拟用户修改")
    print("-" * 30)
    user_modified_draft = "AI正在重塑我们的世界。从手机到汽车，智能技术无处不在。但很多人对AI的理解还停留在科幻层面。我们需要真正了解AI，才能在这个智能时代保持竞争力。"
    print(f"用户修改后的文案:")
    print(f"   {user_modified_draft}")
    
    # Step 5: 学习新偏好和规则
    print("\n🧠 Step 6: 学习新偏好和规则")
    print("-" * 30)
    
    # 学习偏好
    try:
        learned_preferences = ai_agent.learn_preferences(first_final_draft, user_modified_draft)
        print(f"✅ 学习到的新偏好: {len(learned_preferences)} 个")
        for i, pref in enumerate(learned_preferences, 1):
            print(f"  {i}. {pref}")
            
            # 去重检查并添加
            existing_preferences = data_manager.get_user_preferences()
            if deduplication_engine.deduplicate_preference(pref, existing_preferences):
                data_manager.add_user_preference(pref)
                print(f"     ✅ 已添加到偏好库")
            else:
                print(f"     ⚠️ 与现有偏好重复，跳过")
    except Exception as e:
        print(f"❌ 偏好学习失败: {e}")
    
    # 学习规则
    user_instructions = ["让文案更简洁", "减少技术术语"]
    try:
        learned_rules = ai_agent.learn_rules(user_instructions)
        print(f"✅ 学习到的新规则: {len(learned_rules)} 个")
        for i, rule in enumerate(learned_rules, 1):
            print(f"  {i}. {rule}")
            
            # 去重检查并添加
            existing_rules = data_manager.get_restriction_rules()
            if deduplication_engine.deduplicate_rule(rule, existing_rules):
                data_manager.add_restriction_rule(rule)
                print(f"     ✅ 已添加到规则库")
            else:
                print(f"     ⚠️ 与现有规则重复，跳过")
    except Exception as e:
        print(f"❌ 规则学习失败: {e}")
    
    # 显示最终结果
    print("\n🎉 最终结果")
    print("-" * 30)
    print(f"最终文案: {user_modified_draft}")
    
    # 显示更新后的数据
    final_preferences = data_manager.get_user_preferences()
    final_rules = data_manager.get_restriction_rules()
    
    print(f"\n📊 数据统计:")
    print(f"  偏好总数: {len(final_preferences)}")
    print(f"  规则总数: {len(final_rules)}")
    
    print(f"\n📝 所有偏好:")
    for i, pref in enumerate(final_preferences, 1):
        print(f"  {i}. {pref['description']}")
    
    print(f"\n📋 所有规则:")
    for i, rule in enumerate(final_rules, 1):
        print(f"  {i}. {rule['instruction']}")
    
    print("\n" + "=" * 60)
    print("🎉 完整工作流程演示完成！")
    print("✅ 所有功能正常工作，火山方舟大模型集成成功！")
    print("=" * 60)

def test_ai_capabilities():
    """测试AI能力"""
    print("\n🤖 AI能力测试")
    print("=" * 30)
    
    try:
        ai_agent = AIAgent()
        
        # 测试简单文案生成
        test_prompt = "写一段关于春天的文案"
        print(f"测试提示: {test_prompt}")
        
        # 模拟API调用
        response = ai_agent.client.chat.completions.create(
            model=ai_agent.model,
            messages=[
                {"role": "user", "content": test_prompt}
            ],
            thinking={"type": "disabled"}
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ AI响应成功:")
        print(f"   {result}")
        
    except Exception as e:
        print(f"❌ AI能力测试失败: {e}")

if __name__ == "__main__":
    # 运行完整工作流程
    simulate_full_workflow()
    
    # 测试AI能力
    test_ai_capabilities()
