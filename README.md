# 🎨 文案风格个性化AI Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![火山方舟](https://img.shields.io/badge/火山方舟-API-orange.svg)](https://www.volcengine.com)

一个基于大语言模型的个性化文案生成系统，能够学习用户的写作偏好和限制规则，生成符合个人风格的文案。

## ✨ 功能特点

- 🎯 **风格学习**：从参考文案中学习写作风格
- 🎨 **偏好应用**：应用历史学习到的写作偏好
- 📋 **规则限制**：应用用户设定的限制规则
- ✏️ **多轮编辑**：支持多轮对话和编辑
- 🧠 **持续学习**：从每次交互中学习新的偏好和规则

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/writing-ai-agent.git
cd writing-ai-agent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `env_example.txt` 为 `.env` 并填入您的API密钥：

```bash
cp env_example.txt .env
```

编辑 `.env` 文件：
```
VOLCANO_API_KEY=your_volcano_api_key_here
```

### 4. 运行项目

#### 🌐 Web界面（推荐）
```bash
python web_interface.py
```
然后在浏览器中访问 http://localhost:8080

#### 💻 命令行界面
```bash
python main.py
```

#### 🎬 演示模式
```bash
python demo_run.py
```

## 📁 项目结构

```
writing-ai-agent/
├── 🌐 web_interface.py      # Web界面（Flask）
├── 💻 main.py              # 命令行主程序
├── 🤖 ai_agent.py          # AI代理核心逻辑
├── 📊 data_manager.py      # 数据管理
├── 🔄 deduplication.py     # 去重引擎
├── 🎨 user_interface.py    # 用户界面工具
├── 🎬 demo_run.py          # 演示脚本
├── 🎮 interactive_demo.py  # 交互式演示
├── 🧪 test_setup.py        # 测试脚本
├── ⚡ start.py             # 快速启动脚本
├── 📦 requirements.txt     # 依赖列表
├── 🔧 env_example.txt      # 环境变量示例
├── 📁 data/                # 数据目录
│   ├── user_profile.json    # 用户配置文件
│   └── demo_profile.json    # 演示配置文件
├── 📖 README.md            # 项目说明
├── 📄 LICENSE              # 许可证
├── 🚫 .gitignore           # Git忽略文件
└── 📚 docs/                # 文档目录
    ├── WEB_USAGE_GUIDE.md   # Web使用指南
    ├── UI_UX_DESIGN.md      # UI/UX设计说明
    ├── VOLCANO_INTEGRATION.md # 火山方舟集成说明
    └── PROJECT_SUMMARY.md   # 项目总结
```

## 🎯 使用说明

### Web界面使用流程

1. **📝 风格化初稿生成**：输入原始文案和参考文案，生成风格化初稿
2. **🎯 应用写作偏好**：选择历史偏好，应用到文案中
3. **📋 应用限制性规定**：选择限制规则，生成AI终稿
4. **✏️ 编辑**：在AI终稿基础上进行多轮修改
5. **🧠 偏好更新**：学习新的偏好和规则，更新数据库

### 命令行使用

运行 `python main.py` 后按照提示操作：

1. 输入原始文案
2. 提供参考文案
3. 选择要应用的偏好
4. 选择要应用的规则
5. 进行多轮编辑
6. 完成学习更新

## 🔌 API接口

### Web API端点

- `GET /` - 主页面
- `GET /api/preferences` - 获取偏好列表
- `GET /api/rules` - 获取规则列表
- `POST /api/generate-draft` - 生成风格化初稿
- `POST /api/apply-preferences` - 应用偏好
- `POST /api/apply-rules` - 应用规则
- `POST /api/ai-edit` - AI编辑
- `POST /api/learn` - 学习更新

## ⚙️ 配置说明

### 用户配置文件 (data/user_profile.json)

```json
{
  "user_preferences": [
    {
      "id": "pref_1_xxx",
      "description": "偏好描述",
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "restriction_rules": [
    {
      "id": "rule_1_xxx", 
      "instruction": "规则描述",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

## 🛠️ 开发说明

### 添加新的AI服务

1. 修改 `ai_agent.py` 中的客户端初始化
2. 更新API调用方法
3. 修改环境变量配置

### 自定义去重算法

修改 `deduplication.py` 中的相似度计算方法。

### 扩展Web界面

在 `web_interface.py` 中添加新的路由和前端逻辑。

## 🔧 故障排除

### 常见问题

1. **API密钥错误**：检查 `.env` 文件中的 `VOLCANO_API_KEY`
2. **端口占用**：修改 `web_interface.py` 中的端口号
3. **依赖安装失败**：使用 `pip install --upgrade pip` 升级pip

### 调试模式

设置环境变量启用调试：
```bash
export FLASK_DEBUG=1
python web_interface.py
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。



**⚠️ 注意**：使用前请确保已获得火山方舟API的访问权限，并正确配置API密钥。

**⭐ 如果这个项目对您有帮助，请给个Star支持一下！**
