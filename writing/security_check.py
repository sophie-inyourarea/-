#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全检查脚本 - 确保没有敏感信息被提交到GitHub
"""

import os
import re
from pathlib import Path

def check_sensitive_files():
    """检查敏感文件"""
    print("🔍 检查敏感文件...")
    
    sensitive_files = ['.env', 'data/user_profile.json']
    all_safe = True
    
    for file_path in sensitive_files:
        if Path(file_path).exists():
            print(f"⚠️  发现敏感文件: {file_path}")
            print(f"   请确保此文件在 .gitignore 中")
            all_safe = False
        else:
            print(f"✅ 敏感文件不存在: {file_path}")
    
    return all_safe

def check_api_keys():
    """检查代码中是否有硬编码的API密钥"""
    print("\n🔍 检查硬编码API密钥...")
    
    # 检查Python文件
    python_files = [
        'web_interface.py', 'main.py', 'ai_agent.py', 
        'data_manager.py', 'deduplication.py', 'user_interface.py',
        'demo_run.py', 'interactive_demo.py', 'test_setup.py',
        'start.py', 'quick_start.py'
    ]
    
    api_key_patterns = [
        r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}',  # 真实API密钥格式
        r'api_key\s*=\s*["\'][^"\']+["\']',  # 硬编码API密钥模式
        r'VOLCANO_API_KEY\s*=\s*["\'][^"\']+["\']',  # 环境变量硬编码
    ]
    
    all_safe = True
    
    for file_path in python_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern in api_key_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        print(f"❌ 在 {file_path} 中发现可能的API密钥: {matches}")
                        all_safe = False
                    else:
                        print(f"✅ {file_path} 没有硬编码API密钥")
            except Exception as e:
                print(f"⚠️  无法检查 {file_path}: {e}")
    
    return all_safe

def check_gitignore():
    """检查.gitignore配置"""
    print("\n🔍 检查.gitignore配置...")
    
    if not Path('.gitignore').exists():
        print("❌ .gitignore 文件不存在")
        return False
    
    try:
        with open('.gitignore', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_patterns = ['.env', 'data/user_profile.json', '__pycache__/', '*.pyc']
        all_present = True
        
        for pattern in required_patterns:
            if pattern in content:
                print(f"✅ .gitignore 包含: {pattern}")
            else:
                print(f"❌ .gitignore 缺少: {pattern}")
                all_present = False
        
        return all_present
    except Exception as e:
        print(f"❌ 无法读取 .gitignore: {e}")
        return False

def check_env_example():
    """检查env_example.txt是否安全"""
    print("\n🔍 检查env_example.txt...")
    
    if not Path('env_example.txt').exists():
        print("❌ env_example.txt 文件不存在")
        return False
    
    try:
        with open('env_example.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含真实API密钥（这里应该检查是否有真实的API密钥格式）
        if re.search(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', content):
            print("❌ env_example.txt 包含真实API密钥格式")
            return False
        
        if 'your_volcano_api_key_here' in content:
            print("✅ env_example.txt 使用占位符API密钥")
            return True
        else:
            print("⚠️  env_example.txt 可能包含真实API密钥")
            return False
    except Exception as e:
        print(f"❌ 无法读取 env_example.txt: {e}")
        return False

def main():
    """主检查函数"""
    print("🔒 开始安全检查...")
    print("=" * 50)
    
    all_safe = True
    
    # 检查各项
    if not check_sensitive_files():
        all_safe = False
    
    if not check_api_keys():
        all_safe = False
    
    if not check_gitignore():
        all_safe = False
    
    if not check_env_example():
        all_safe = False
    
    print("\n" + "=" * 50)
    if all_safe:
        print("🎉 安全检查通过！可以安全部署到GitHub")
        print("\n📋 安全部署步骤:")
        print("1. git init")
        print("2. git add .")
        print("3. git commit -m 'Initial commit'")
        print("4. git remote add origin <your-repo-url>")
        print("5. git push -u origin main")
    else:
        print("❌ 安全检查失败！请修复安全问题后再部署")
        print("\n🔧 修复建议:")
        print("1. 确保 .env 文件在 .gitignore 中")
        print("2. 确保 env_example.txt 使用占位符API密钥")
        print("3. 检查代码中是否有硬编码的API密钥")
        print("4. 确保 data/user_profile.json 在 .gitignore 中")
    
    return all_safe

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
