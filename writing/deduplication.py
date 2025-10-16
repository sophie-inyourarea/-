"""
去重模块 - 使用文本相似度比较，避免重复的偏好和规则
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Any
import os
import re
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class DeduplicationEngine:
    """去重引擎，使用TF-IDF向量化进行相似度比较"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=None,  # 中文文本不使用英文停用词
            ngram_range=(1, 2)  # 使用1-gram和2-gram
        )
    
    def preprocess_text(self, text: str) -> str:
        """预处理文本，提取关键词"""
        # 移除标点符号和特殊字符
        text = re.sub(r'[^\w\s]', ' ', text)
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def get_tfidf_vector(self, text: str) -> np.ndarray:
        """获取文本的TF-IDF向量"""
        try:
            processed_text = self.preprocess_text(text)
            vector = self.vectorizer.fit_transform([processed_text])
            return vector.toarray()[0]
        except Exception as e:
            print(f"获取TF-IDF向量时出错: {e}")
            return np.zeros(1000)  # 默认维度
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """计算两个文本的余弦相似度"""
        # 将两个文本一起向量化以确保维度一致
        texts = [self.preprocess_text(text1), self.preprocess_text(text2)]
        vectors = self.vectorizer.fit_transform(texts)
        
        # 计算余弦相似度
        similarity = cosine_similarity([vectors[0].toarray()[0]], [vectors[1].toarray()[0]])[0][0]
        return float(similarity)
    
    def deduplicate_preference(self, new_description: str, existing_preferences: List[Dict[str, Any]], threshold: float = 0.85) -> bool:
        """
        检查新偏好是否与现有偏好重复
        返回True表示不重复（可以添加），False表示重复（不应添加）
        """
        if not existing_preferences:
            return True
        
        for existing_pref in existing_preferences:
            existing_description = existing_pref.get("description", "")
            similarity = self.calculate_similarity(new_description, existing_description)
            
            if similarity >= threshold:
                print(f"发现相似偏好 (相似度: {similarity:.3f}): {existing_description}")
                return False
        
        return True
    
    def deduplicate_rule(self, new_instruction: str, existing_rules: List[Dict[str, Any]], threshold: float = 0.85) -> bool:
        """
        检查新规则是否与现有规则重复
        返回True表示不重复（可以添加），False表示重复（不应添加）
        """
        if not existing_rules:
            return True
        
        for existing_rule in existing_rules:
            existing_instruction = existing_rule.get("instruction", "")
            similarity = self.calculate_similarity(new_instruction, existing_instruction)
            
            if similarity >= threshold:
                print(f"发现相似规则 (相似度: {similarity:.3f}): {existing_instruction}")
                return False
        
        return True
    
    def deduplicate(self, new_item_text: str, existing_items: List[Dict[str, Any]], threshold: float = 0.85) -> bool:
        """
        通用去重函数
        根据items中的字段自动判断是偏好还是规则
        """
        if not existing_items:
            return True
        
        # 检查第一个item的字段来判断类型
        first_item = existing_items[0]
        if "description" in first_item:
            # 这是偏好列表
            return self.deduplicate_preference(new_item_text, existing_items, threshold)
        elif "instruction" in first_item:
            # 这是规则列表
            return self.deduplicate_rule(new_item_text, existing_items, threshold)
        else:
            # 未知类型，默认允许添加
            return True
