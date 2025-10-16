"""
用户界面模块 - 处理命令行交互和用户输入
"""
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import List, Dict, Any, Optional

console = Console()

class UserInterface:
    """用户界面管理器"""
    
    def __init__(self):
        self.console = console
    
    def display_welcome(self):
        """显示欢迎信息"""
        welcome_text = Text("文案风格个性化AI Agent", style="bold blue")
        subtitle = Text("根据您的写作风格生成个性化文案", style="italic")
        
        panel = Panel.fit(
            f"{welcome_text}\n\n{subtitle}",
            title="欢迎使用",
            border_style="blue"
        )
        self.console.print(panel)
        self.console.print()
    
    def get_user_input_text(self) -> str:
        """获取用户输入的原始文案"""
        self.console.print("[bold]请输入您要优化的原始文案：[/bold]")
        return questionary.text("文案内容", multiline=True).ask()
    
    def get_reference_texts(self) -> List[str]:
        """获取参考文案"""
        self.console.print("[bold]请输入参考文案（用于定义风格）：[/bold]")
        reference_texts = []
        
        for i in range(3):
            if i == 0:
                text = questionary.text(f"参考文案 {i+1}（必填）", multiline=True).ask()
            else:
                text = questionary.text(f"参考文案 {i+1}（可选，直接回车跳过）", multiline=True).ask()
            
            if text and text.strip():
                reference_texts.append(text.strip())
            elif i == 0:
                # 第一个是必填的
                self.console.print("[red]第一个参考文案是必填的！[/red]")
                i -= 1
                continue
            else:
                # 后续是可选的
                break
        
        return reference_texts
    
    def display_draft(self, draft: str, title: str = "当前文案"):
        """显示文案草稿"""
        panel = Panel(
            draft,
            title=title,
            border_style="green"
        )
        self.console.print(panel)
        self.console.print()
    
    def select_preferences(self, preferences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """让用户选择要应用的偏好"""
        if not preferences:
            self.console.print("[yellow]暂无可用的写作偏好。[/yellow]")
            return []
        
        self.console.print("[bold]请选择要应用的写作偏好：[/bold]")
        
        # 创建选择列表
        choices = []
        for i, pref in enumerate(preferences, 1):
            choices.append(f"{i}. {pref['description']}")
        
        choices.append("跳过此步骤")
        
        selected_indices = questionary.checkbox(
            "选择偏好（可多选）",
            choices=choices
        ).ask()
        
        if "跳过此步骤" in selected_indices:
            return []
        
        # 解析选择的偏好
        selected_preferences = []
        for choice in selected_indices:
            try:
                index = int(choice.split('.')[0]) - 1
                if 0 <= index < len(preferences):
                    selected_preferences.append(preferences[index])
            except (ValueError, IndexError):
                continue
        
        return selected_preferences
    
    def select_rules(self, rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """让用户选择要应用的规则"""
        if not rules:
            self.console.print("[yellow]暂无可用的限制规则。[/yellow]")
            return []
        
        self.console.print("[bold]请选择要应用的限制规则：[/bold]")
        
        # 创建选择列表
        choices = []
        for i, rule in enumerate(rules, 1):
            choices.append(f"{i}. {rule['instruction']}")
        
        choices.append("跳过此步骤")
        
        selected_indices = questionary.checkbox(
            "选择规则（可多选）",
            choices=choices
        ).ask()
        
        if "跳过此步骤" in selected_indices:
            return []
        
        # 解析选择的规则
        selected_rules = []
        for choice in selected_indices:
            try:
                index = int(choice.split('.')[0]) - 1
                if 0 <= index < len(rules):
                    selected_rules.append(rules[index])
            except (ValueError, IndexError):
                continue
        
        return selected_rules
    
    def get_edit_choice(self) -> str:
        """获取用户编辑选择"""
        return questionary.select(
            "您对当前文案满意吗？",
            choices=[
                "满意 (y) - 完成编辑",
                "自己修改 (e) - 手动编辑文案",
                "让AI根据指令修改 (i) - 提供修改指令"
            ]
        ).ask()
    
    def get_manual_edit(self) -> str:
        """获取用户手动编辑的文案"""
        self.console.print("[bold]请输入修改后的文案：[/bold]")
        return questionary.text("修改后的文案", multiline=True).ask()
    
    def get_ai_instruction(self) -> str:
        """获取用户给AI的修改指令"""
        self.console.print("[bold]请提供修改指令：[/bold]")
        return questionary.text("修改指令", multiline=True).ask()
    
    def display_learning_results(self, new_preferences: List[str], new_rules: List[str]):
        """显示学习结果"""
        if new_preferences or new_rules:
            self.console.print("[bold green]学习到的新内容：[/bold green]")
            
            if new_preferences:
                self.console.print("[bold]新增偏好：[/bold]")
                for i, pref in enumerate(new_preferences, 1):
                    self.console.print(f"  {i}. {pref}")
                self.console.print()
            
            if new_rules:
                self.console.print("[bold]新增规则：[/bold]")
                for i, rule in enumerate(new_rules, 1):
                    self.console.print(f"  {i}. {rule}")
                self.console.print()
        else:
            self.console.print("[yellow]本次会话未学习到新的偏好或规则。[/yellow]")
    
    def display_final_result(self, final_draft: str):
        """显示最终结果"""
        panel = Panel(
            final_draft,
            title="[bold green]最终文案[/bold green]",
            border_style="green"
        )
        self.console.print(panel)
        self.console.print()
        self.console.print("[bold green]文案生成完成！[/bold green]")
