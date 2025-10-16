#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署检查脚本 - 确保项目可以成功部署到GitHub
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - 文件不存在")
        return False

def check_file_content(file_path, required_content, description):
    """检查文件内容"""
    if not Path(file_path).exists():
        print(f"❌ {description}: {file_path} - 文件不存在")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if required_content in content:
            print(f"✅ {description}: {file_path}")
            return True
        else:
            print(f"❌ {description}: {file_path} - 缺少必要内容")
            return False
    except Exception as e:
        print(f"❌ {description}: {file_path} - 读取错误: {e}")
        return False

def check_json_file(file_path, description):
    """检查JSON文件格式"""
    if not Path(file_path).exists():
        print(f"❌ {description}: {file_path} - 文件不存在")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✅ {description}: {file_path}")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {description}: {file_path} - JSON格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ {description}: {file_path} - 读取错误: {e}")
        return False

def main():
    """主检查函数"""
    print("🔍 开始部署检查...")
    print("=" * 50)
    
    all_passed = True
    
    # 检查核心文件
    print("\n📁 检查核心文件:")
    core_files = [
        ("README.md", "项目说明文档"),
        ("LICENSE", "许可证文件"),
        (".gitignore", "Git忽略文件"),
        ("requirements.txt", "依赖列表"),
        ("env_example.txt", "环境变量示例"),
    ]
    
    for file_path, description in core_files:
        if not check_file_exists(file_path, description):
            all_passed = False
    
    # 检查Python文件
    print("\n🐍 检查Python文件:")
    python_files = [
        ("web_interface.py", "Web界面"),
        ("main.py", "命令行主程序"),
        ("ai_agent.py", "AI代理核心"),
        ("data_manager.py", "数据管理"),
        ("deduplication.py", "去重引擎"),
        ("user_interface.py", "用户界面工具"),
        ("demo_run.py", "演示脚本"),
        ("interactive_demo.py", "交互式演示"),
        ("test_setup.py", "测试脚本"),
        ("start.py", "快速启动脚本"),
        ("quick_start.py", "一键启动脚本"),
    ]
    
    for file_path, description in python_files:
        if not check_file_exists(file_path, description):
            all_passed = False
    
    # 检查数据目录
    print("\n📊 检查数据目录:")
    if not check_file_exists("data", "数据目录"):
        all_passed = False
    
    if not check_json_file("data/demo_profile.json", "演示配置文件"):
        all_passed = False
    
    # 检查文档文件
    print("\n📚 检查文档文件:")
    doc_files = [
        ("WEB_USAGE_GUIDE.md", "Web使用指南"),
        ("UI_UX_DESIGN.md", "UI/UX设计说明"),
        ("VOLCANO_INTEGRATION.md", "火山方舟集成说明"),
        ("GITHUB_DEPLOYMENT.md", "GitHub部署指南"),
        ("PROJECT_OVERVIEW.md", "项目总览"),
    ]
    
    for file_path, description in doc_files:
        if not check_file_exists(file_path, description):
            all_passed = False
    
    # 检查README内容
    print("\n📖 检查README内容:")
    readme_checks = [
        ("# 🎨 文案风格个性化AI Agent", "项目标题"),
        ("## ✨ 功能特点", "功能特点章节"),
        ("## 🚀 快速开始", "快速开始章节"),
        ("## 📁 项目结构", "项目结构章节"),
        ("## 🔌 API接口", "API接口章节"),
        ("## ⚙️ 配置说明", "配置说明章节"),
        ("## 🤝 贡献指南", "贡献指南章节"),
        ("## 📄 许可证", "许可证章节"),
    ]
    
    for content, description in readme_checks:
        if not check_file_content("README.md", content, description):
            all_passed = False
    
    # 检查requirements.txt内容
    print("\n📦 检查依赖文件:")
    required_packages = [
        "volcengine-python-sdk[ark]",
        "questionary",
        "rich",
        "numpy",
        "scikit-learn",
        "python-dotenv",
        "flask",
    ]
    
    for package in required_packages:
        if not check_file_content("requirements.txt", package, f"依赖包: {package}"):
            all_passed = False
    
    # 检查.gitignore内容
    print("\n🚫 检查Git忽略文件:")
    gitignore_checks = [
        "__pycache__/",
        "*.pyc",
        ".env",
        "*.log",
        "data/user_profile.json",
    ]
    
    for content in gitignore_checks:
        if not check_file_content(".gitignore", content, f"忽略规则: {content}"):
            all_passed = False
    
    # 检查环境变量示例
    print("\n🔧 检查环境变量示例:")
    if not check_file_content("env_example.txt", "VOLCANO_API_KEY", "API密钥配置"):
        all_passed = False
    
    # 检查许可证
    print("\n📄 检查许可证:")
    if not check_file_content("LICENSE", "MIT License", "MIT许可证"):
        all_passed = False
    
    # 总结
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查通过！项目可以安全部署到GitHub")
        print("\n📋 部署步骤:")
        print("1. git init")
        print("2. git add .")
        print("3. git commit -m 'Initial commit'")
        print("4. git remote add origin <your-repo-url>")
        print("5. git push -u origin main")
        print("\n⚠️  注意事项:")
        print("- 确保不要提交 .env 文件")
        print("- 确保不要提交包含真实API密钥的文件")
        print("- 建议先创建 .env 文件并测试项目运行")
    else:
        print("❌ 部分检查失败，请修复后再部署")
        print("\n🔧 修复建议:")
        print("- 检查缺失的文件")
        print("- 检查文件内容是否完整")
        print("- 确保所有依赖都已安装")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
