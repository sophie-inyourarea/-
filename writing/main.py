"""
文案风格个性化AI Agent - 主程序入口
"""
import os
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        pass
from data_manager import DataManager
from ai_agent import AIAgent
from user_interface import UserInterface
from deduplication import DeduplicationEngine

# 加载环境变量
load_dotenv()

class CopywritingAgent:
    """文案风格个性化AI Agent主类"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.ai_agent = AIAgent()
        self.ui = UserInterface()
        self.deduplication_engine = DeduplicationEngine()
        
        # 检查API密钥
        if not os.getenv("VOLCANO_API_KEY"):
            self.ui.console.print("[red]错误：未找到VOLCANO_API_KEY环境变量！[/red]")
            self.ui.console.print("请创建.env文件并设置您的火山方舟API密钥。")
            exit(1)
    
    def run(self):
        """运行主程序"""
        self.ui.display_welcome()
        
        try:
            # Step 1: 获取用户输入和参考文案
            user_input_text = self.ui.get_user_input_text()
            reference_texts = self.ui.get_reference_texts()
            
            # Step 2: 生成风格化初稿
            self.ui.console.print("[bold]正在生成风格化初稿...[/bold]")
            draft_1 = self.ai_agent.generate_style_draft(user_input_text, reference_texts)
            self.ui.display_draft(draft_1, "风格化初稿")
            
            # Step 3: 应用写作偏好
            preferences = self.data_manager.get_user_preferences()
            selected_preferences = self.ui.select_preferences(preferences)
            
            if selected_preferences:
                self.ui.console.print("[bold]正在应用写作偏好...[/bold]")
                draft_2 = self.ai_agent.apply_preferences(draft_1, selected_preferences)
                self.ui.display_draft(draft_2, "应用偏好后的文案")
            else:
                draft_2 = draft_1
            
            # Step 4: 应用限制规则
            rules = self.data_manager.get_restriction_rules()
            selected_rules = self.ui.select_rules(rules)
            
            if selected_rules:
                self.ui.console.print("[bold]正在应用限制规则...[/bold]")
                first_final_draft = self.ai_agent.apply_restrictions(draft_2, selected_rules)
                self.ui.display_draft(first_final_draft, "AI生成的终稿")
            else:
                first_final_draft = draft_2
            
            # Step 5: 多轮对话与编辑
            current_draft = first_final_draft
            user_instructions = []
            
            while True:
                choice = self.ui.get_edit_choice()
                
                if choice.startswith("满意"):
                    user_confirmed_final_draft = current_draft
                    break
                elif choice.startswith("自己修改"):
                    new_version = self.ui.get_manual_edit()
                    current_draft = new_version
                    self.ui.display_draft(current_draft, "修改后的文案")
                elif choice.startswith("让AI根据指令修改"):
                    instruction = self.ui.get_ai_instruction()
                    user_instructions.append(instruction)
                    self.ui.console.print("[bold]正在根据指令修改文案...[/bold]")
                    new_version = self.ai_agent.modify_with_instruction(current_draft, instruction)
                    current_draft = new_version
                    self.ui.display_draft(current_draft, "AI修改后的文案")
            
            # Step 6: 学习与更新
            self.ui.console.print("[bold]正在学习您的写作偏好...[/bold]")
            self.learn_and_update(first_final_draft, user_confirmed_final_draft, user_instructions)
            
            # 显示最终结果
            self.ui.display_final_result(user_confirmed_final_draft)
            
        except KeyboardInterrupt:
            self.ui.console.print("\n[yellow]程序被用户中断。[/yellow]")
        except Exception as e:
            self.ui.console.print(f"[red]程序运行出错: {e}[/red]")
    
    def learn_and_update(self, first_final_draft: str, user_confirmed_final_draft: str, user_instructions: list):
        """学习用户偏好和规则，更新数据库"""
        # 学习偏好
        learned_preferences = self.ai_agent.learn_preferences(first_final_draft, user_confirmed_final_draft)
        existing_preferences = self.data_manager.get_user_preferences()
        
        new_preferences = []
        for pref_description in learned_preferences:
            if self.deduplication_engine.deduplicate_preference(pref_description, existing_preferences):
                self.data_manager.add_user_preference(pref_description)
                new_preferences.append(pref_description)
                existing_preferences.append({"description": pref_description})  # 更新本地列表
        
        # 学习规则
        learned_rules = self.ai_agent.learn_rules(user_instructions)
        existing_rules = self.data_manager.get_restriction_rules()
        
        new_rules = []
        for rule_instruction in learned_rules:
            if self.deduplication_engine.deduplicate_rule(rule_instruction, existing_rules):
                self.data_manager.add_restriction_rule(rule_instruction)
                new_rules.append(rule_instruction)
                existing_rules.append({"instruction": rule_instruction})  # 更新本地列表
        
        # 显示学习结果
        self.ui.display_learning_results(new_preferences, new_rules)

def main():
    """主函数"""
    agent = CopywritingAgent()
    agent.run()

if __name__ == "__main__":
    main()
