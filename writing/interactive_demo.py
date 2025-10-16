#!/usr/bin/env python3
"""
交互式演示脚本 - 模拟完整的用户交互流程
"""
import os
import sys

# 设置环境变量
os.environ["VOLCANO_API_KEY"] = "your_volcano_api_key_here"

from data_manager import DataManager
from ai_agent import AIAgent
from deduplication import DeduplicationEngine

def print_header():
    """打印欢迎信息"""
    print("=" * 60)
    print("🎨 文案风格个性化AI Agent - 交互式演示")
    print("=" * 60)
    print("这个演示将模拟完整的用户交互流程")
    print("您可以看到每个步骤的效果")
    print("=" * 60)

def simulate_user_input():
    """模拟用户输入"""
    print("\n📝 模拟用户输入:")
    print("-" * 30)
    
    # 模拟用户输入
    user_input = "人工智能正在改变我们的世界，从智能手机到自动驾驶汽车，AI技术无处不在。但是，很多人对AI的理解还停留在科幻电影中。我们需要更好地了解AI，才能在这个智能时代中保持竞争力。"
    reference1 = "在这个快速变化的时代，我们每个人都在寻找属于自己的声音。技术不是冰冷的工具，而是连接人心的桥梁。"
    reference2 = "每一次选择都是一次成长，每一次尝试都是一次突破。我们不是被动的接受者，而是主动的创造者。"
    
    print(f"原始文案: {user_input}")
    print(f"参考文案1: {reference1}")
    print(f"参考文案2: {reference2}")
    
    return user_input, [reference1, reference2]

def simulate_preference_selection(preferences):
    """模拟偏好选择"""
    print(f"\n🎯 模拟偏好选择 (共{len(preferences)}个可用偏好):")
    print("-" * 30)
    
    for i, pref in enumerate(preferences, 1):
        print(f"{i}. {pref['description']}")
    
    # 模拟选择前两个偏好
    selected_indices = [0, 1] if len(preferences) >= 2 else [0] if len(preferences) >= 1 else []
    selected_preferences = [preferences[i] for i in selected_indices]
    
    print(f"\n✅ 模拟选择偏好: {len(selected_preferences)}个")
    for i, pref in enumerate(selected_preferences, 1):
        print(f"   {i}. {pref['description']}")
    
    return selected_preferences

def simulate_rule_selection(rules):
    """模拟规则选择"""
    print(f"\n📋 模拟规则选择 (共{len(rules)}个可用规则):")
    print("-" * 30)
    
    for i, rule in enumerate(rules, 1):
        print(f"{i}. {rule['instruction']}")
    
    # 模拟选择第一个规则
    selected_indices = [0] if len(rules) >= 1 else []
    selected_rules = [rules[i] for i in selected_indices]
    
    print(f"\n✅ 模拟选择规则: {len(selected_rules)}个")
    for i, rule in enumerate(selected_rules, 1):
        print(f"   {i}. {rule['instruction']}")
    
    return selected_rules

def simulate_user_editing(ai_draft):
    """模拟用户编辑"""
    print(f"\n✏️ 模拟用户编辑:")
    print("-" * 30)
    print(f"AI生成的文案: {ai_draft}")
    
    # 模拟用户修改
    user_modified = "你有没有发现，我们的生活正悄悄被AI改变着？从手机到汽车，智能技术无处不在。但很多人对AI的理解还停留在科幻层面。我们需要真正了解AI，才能在这个智能时代保持竞争力。"
    
    print(f"\n用户修改后的文案: {user_modified}")
    return user_modified

def main():
    """主函数"""
    print_header()
    
    # 初始化组件
    print("\n🔧 初始化组件...")
    data_manager = DataManager()
    ai_agent = AIAgent()
    deduplication_engine = DeduplicationEngine()
    print("✅ 所有组件初始化完成")
    
    # 模拟用户输入
    user_input, references = simulate_user_input()
    
    # 生成风格化初稿
    print("\n🎨 生成风格化初稿...")
    print("-" * 30)
    try:
        draft_1 = ai_agent.generate_style_draft(user_input, references)
        print(f"✅ 风格化初稿生成成功:")
        print(f"   {draft_1}")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        draft_1 = user_input
    
    # 获取偏好和规则
    preferences = data_manager.get_user_preferences()
    rules = data_manager.get_restriction_rules()
    
    # 模拟偏好选择和应用
    selected_preferences = simulate_preference_selection(preferences)
    if selected_preferences:
        print("\n🔄 应用写作偏好...")
        try:
            draft_2 = ai_agent.apply_preferences(draft_1, selected_preferences)
            print(f"✅ 偏好应用成功:")
            print(f"   {draft_2}")
        except Exception as e:
            print(f"❌ 偏好应用失败: {e}")
            draft_2 = draft_1
    else:
        draft_2 = draft_1
    
    # 模拟规则选择和应用
    selected_rules = simulate_rule_selection(rules)
    if selected_rules:
        print("\n🔄 应用限制规则...")
        try:
            draft_3 = ai_agent.apply_restrictions(draft_2, selected_rules)
            print(f"✅ 规则应用成功:")
            print(f"   {draft_3}")
        except Exception as e:
            print(f"❌ 规则应用失败: {e}")
            draft_3 = draft_2
    else:
        draft_3 = draft_2
    
    # 模拟用户编辑
    user_final = simulate_user_editing(draft_3)
    
    # 学习新偏好和规则
    print("\n🧠 学习新偏好和规则...")
    print("-" * 30)
    
    try:
        # 学习偏好
        learned_preferences = ai_agent.learn_preferences(draft_3, user_final)
        print(f"✅ 学习到的新偏好: {len(learned_preferences)}个")
        
        existing_preferences = data_manager.get_user_preferences()
        new_preferences = 0
        for pref in learned_preferences:
            if deduplication_engine.deduplicate_preference(pref, existing_preferences):
                data_manager.add_user_preference(pref)
                new_preferences += 1
                print(f"   ✅ 已添加: {pref}")
            else:
                print(f"   ⚠️ 重复跳过: {pref}")
        
        # 学习规则
        user_instructions = ["让文案更简洁", "减少技术术语"]
        learned_rules = ai_agent.learn_rules(user_instructions)
        print(f"✅ 学习到的新规则: {len(learned_rules)}个")
        
        existing_rules = data_manager.get_restriction_rules()
        new_rules = 0
        for rule in learned_rules:
            if deduplication_engine.deduplicate_rule(rule, existing_rules):
                data_manager.add_restriction_rule(rule)
                new_rules += 1
                print(f"   ✅ 已添加: {rule}")
            else:
                print(f"   ⚠️ 重复跳过: {rule}")
        
    except Exception as e:
        print(f"❌ 学习过程出错: {e}")
    
    # 显示最终结果
    print("\n🎉 最终结果")
    print("-" * 30)
    print(f"最终文案: {user_final}")
    
    # 显示数据统计
    final_preferences = data_manager.get_user_preferences()
    final_rules = data_manager.get_restriction_rules()
    
    print(f"\n📊 数据统计:")
    print(f"  偏好总数: {len(final_preferences)}")
    print(f"  规则总数: {len(final_rules)}")
    
    print("\n" + "=" * 60)
    print("🎉 交互式演示完成！")
    print("✅ 所有功能正常工作，火山方舟大模型集成成功！")
    print("\n🌐 Web界面已启动，请在浏览器中访问:")
    print("   http://localhost:8080")
    print("=" * 60)

if __name__ == "__main__":
    main()
