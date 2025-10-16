"""
数据管理模块 - 处理用户偏好和规则的数据存储
"""
import json
import os
from typing import List, Dict, Any
from datetime import datetime


class DataManager:
    """管理用户偏好和规则的数据存储"""
    
    def __init__(self, data_file_path: str = "data/user_profile.json"):
        self.data_file_path = data_file_path
        self.ensure_data_file_exists()
    
    def ensure_data_file_exists(self):
        """确保数据文件存在，如果不存在则创建"""
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        if not os.path.exists(self.data_file_path):
            initial_data = {
                "user_preferences": [],
                "restriction_rules": []
            }
            self.save_data(initial_data)
    
    def load_data(self) -> Dict[str, Any]:
        """加载用户数据"""
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"user_preferences": [], "restriction_rules": []}
    
    def save_data(self, data: Dict[str, Any]):
        """保存用户数据"""
        with open(self.data_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_user_preferences(self) -> List[Dict[str, Any]]:
        """获取用户偏好列表"""
        data = self.load_data()
        return data.get("user_preferences", [])
    
    def get_restriction_rules(self) -> List[Dict[str, Any]]:
        """获取限制规则列表"""
        data = self.load_data()
        return data.get("restriction_rules", [])
    
    def add_user_preference(self, description: str) -> str:
        """添加新的用户偏好"""
        data = self.load_data()
        preference_id = f"pref_{len(data['user_preferences']) + 1}_{int(datetime.now().timestamp())}"
        
        new_preference = {
            "id": preference_id,
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        
        data["user_preferences"].append(new_preference)
        self.save_data(data)
        return preference_id
    
    def add_restriction_rule(self, instruction: str) -> str:
        """添加新的限制规则"""
        data = self.load_data()
        rule_id = f"rule_{len(data['restriction_rules']) + 1}_{int(datetime.now().timestamp())}"
        
        new_rule = {
            "id": rule_id,
            "instruction": instruction,
            "created_at": datetime.now().isoformat()
        }
        
        data["restriction_rules"].append(new_rule)
        self.save_data(data)
        return rule_id
    
    def get_preference_by_id(self, preference_id: str) -> Dict[str, Any]:
        """根据ID获取偏好"""
        preferences = self.get_user_preferences()
        for pref in preferences:
            if pref["id"] == preference_id:
                return pref
        return {}
    
    def get_rule_by_id(self, rule_id: str) -> Dict[str, Any]:
        """根据ID获取规则"""
        rules = self.get_restriction_rules()
        for rule in rules:
            if rule["id"] == rule_id:
                return rule
        return {}
