"""
AI Agent模块 - 处理与火山方舟大模型的交互和文案生成
"""
import os
import re
from typing import List, Dict, Any
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from volcenginesdkarkruntime import Ark
except ImportError:
    print("请安装火山方舟SDK: pip install -U 'volcengine-python-sdk[ark]'")
    raise

class AIAgent:
    """AI Agent，负责与火山方舟大模型API交互"""
    
    def __init__(self):
        self.client = Ark(
            api_key=os.getenv("VOLCANO_API_KEY"),
            timeout=1800,  # 30分钟超时
        )
        self.model = "doubao-seed-1.6-250615"  # 您提供的模型ID
    
    def generate_style_draft(self, user_input_text: str, reference_texts: List[str]) -> str:
        """
        Step 1: 根据参考文案生成风格化初稿
        """
        reference_texts_str = "\n\n".join(reference_texts)
        
        prompt = f"""请结合示例的整体节奏、语气，优化所给文案。

文案：{user_input_text}

示例：{reference_texts_str}

请生成一篇风格化的初稿，保持示例的写作风格和语调。"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的文案优化助手，擅长学习和模仿不同的写作风格。"},
                    {"role": "user", "content": prompt}
                ],
                thinking={"type": "disabled"}  # 不使用深度思考能力
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"生成风格化初稿时出错: {e}")
            return user_input_text
    
    def apply_preferences(self, draft: str, selected_preferences: List[Dict[str, Any]]) -> str:
        """
        Step 2: 应用用户选择的写作偏好
        """
        if not selected_preferences:
            return draft
        
        preferences_text = "\n".join([f"- {pref['description']}" for pref in selected_preferences])
        
        prompt = f"""根据文本修改要求，帮我修改所给文案。

文案：{draft}

文本修改要求：
{preferences_text}

请根据这些要求修改文案，保持内容的完整性。"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的文案修改助手，能够根据用户的写作偏好调整文案风格。"},
                    {"role": "user", "content": prompt}
                ],
                thinking={"type": "disabled"}
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"应用偏好时出错: {e}")
            return draft
    
    def apply_restrictions(self, draft: str, selected_rules: List[Dict[str, Any]]) -> str:
        """
        Step 3: 应用用户选择的限制规则
        """
        if not selected_rules:
            return draft
        
        rules_text = "\n".join([f"- {rule['instruction']}" for rule in selected_rules])
        
        prompt = f"""根据要求，帮我修改所给文案。

文案：{draft}

要求：
{rules_text}

请严格按照这些要求修改文案。"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的文案修改助手，能够严格按照用户的要求调整文案。"},
                    {"role": "user", "content": prompt}
                ],
                thinking={"type": "disabled"}
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"应用限制规则时出错: {e}")
            return draft
    
    def modify_with_instruction(self, draft: str, instruction: str) -> str:
        """
        Step 4: 根据用户指令修改文案
        """
        prompt = f"""请根据以下指令修改文案：

文案：{draft}

指令：{instruction}

请根据指令修改文案。"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的文案修改助手，能够根据用户的详细指令调整文案。"},
                    {"role": "user", "content": prompt}
                ],
                thinking={"type": "disabled"}
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"根据指令修改文案时出错: {e}")
            return draft
    
    def learn_preferences(self, original_draft: str, user_modified_draft: str) -> List[str]:
        """
        Step 5: 学习用户的写作偏好
        """
        prompt = f"""分析"原文本"和"作者改动后的文本"的差异。

请总结出1-3条作者的写作风格偏好。你的输出必须是清晰的序号分点列表（如：1. ... 2. ...）。每一条都应是独立、可执行的描述。

原文本：{original_draft}

作者改动后的文本：{user_modified_draft}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的写作风格分析师，能够从文本修改中识别出作者的写作偏好。"},
                    {"role": "user", "content": prompt}
                ],
                thinking={"type": "disabled"}
            )
            
            # 解析输出，提取偏好描述
            content = response.choices[0].message.content.strip()
            preferences = self._extract_preferences(content)
            return preferences
        except Exception as e:
            print(f"学习偏好时出错: {e}")
            return []
    
    def learn_rules(self, user_instructions: List[str]) -> List[str]:
        """
        Step 5: 学习用户的通用规则
        """
        if not user_instructions:
            return []
        
        instructions_text = "\n".join([f"- {instruction}" for instruction in user_instructions])
        
        prompt = f"""以下是用户对文案的修改意见。判断其中哪些是通用规则，而非对内容细节的意见。总结并分点输出其中通用规则，要求语言精简。

用户意见：
{instructions_text}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的规则提取器，能够从用户的修改意见中识别出通用的写作规则。"},
                    {"role": "user", "content": prompt}
                ],
                thinking={"type": "disabled"}
            )
            
            # 解析输出，提取规则描述
            content = response.choices[0].message.content.strip()
            rules = self._extract_rules(content)
            return rules
        except Exception as e:
            print(f"学习规则时出错: {e}")
            return []
    
    def _extract_preferences(self, content: str) -> List[str]:
        """从AI输出中提取偏好描述"""
        # 使用正则表达式提取序号列表
        pattern = r'\d+\.\s*(.+?)(?=\n\d+\.|\n\n|$)'
        matches = re.findall(pattern, content, re.DOTALL)
        return [match.strip() for match in matches if match.strip()]
    
    def _extract_rules(self, content: str) -> List[str]:
        """从AI输出中提取规则描述"""
        # 使用正则表达式提取序号列表
        pattern = r'\d+\.\s*(.+?)(?=\n\d+\.|\n\n|$)'
        matches = re.findall(pattern, content, re.DOTALL)
        return [match.strip() for match in matches if match.strip()]
