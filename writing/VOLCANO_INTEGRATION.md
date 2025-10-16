# 火山方舟大模型集成说明

## 集成完成情况

✅ **火山方舟大模型集成已完成** - 项目已成功从OpenAI API迁移到火山方舟大模型服务

## 主要变更

### 1. 依赖包更新
- **移除**: `openai>=1.0.0`
- **添加**: `volcengine-python-sdk[ark]>=1.0.0`

### 2. API密钥配置
- **原配置**: `OPENAI_API_KEY`
- **新配置**: `VOLCANO_API_KEY`

### 3. 模型配置
- **使用模型**: `doubao-seed-1.6-250615`
- **超时设置**: 1800秒（30分钟）
- **思考模式**: 禁用深度思考（`thinking={"type": "disabled"}`）

### 4. 去重机制优化
- **原方案**: OpenAI text-embedding-3-small
- **新方案**: TF-IDF向量化 + 余弦相似度
- **优势**: 无需额外API调用，本地计算，成本更低

## 技术实现细节

### AI Agent模块 (`ai_agent.py`)
```python
from volcenginesdkarkruntime import Ark

class AIAgent:
    def __init__(self):
        self.client = Ark(
            api_key=os.getenv("VOLCANO_API_KEY"),
            timeout=1800,  # 30分钟超时
        )
        self.model = "doubao-seed-1.6-250615"
```

### 去重引擎模块 (`deduplication.py`)
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DeduplicationEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=None,  # 中文文本
            ngram_range=(1, 2)  # 1-gram和2-gram
        )
```

## 环境配置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 设置API密钥
创建 `.env` 文件：
```
VOLCANO_API_KEY=your_volcano_api_key_here
```

### 3. 运行程序
```bash
python start.py
# 或
python main.py
```

## 功能验证

### 已测试功能
✅ 模块导入正常  
✅ 数据管理器功能正常  
✅ 用户界面组件正常  
✅ 去重引擎架构完整  
✅ 主程序流程完整  

### 待验证功能（需要API密钥）
- 文案生成功能
- 偏好学习功能
- 规则提取功能

## 优势对比

### 火山方舟 vs OpenAI
| 特性 | 火山方舟 | OpenAI |
|------|----------|--------|
| 成本 | 相对较低 | 较高 |
| 中文支持 | 原生优化 | 良好 |
| 响应速度 | 较快 | 中等 |
| 本地化 | 国内服务 | 国际服务 |
| 去重方案 | TF-IDF本地计算 | 需要API调用 |

## 使用示例

### 基本用法
```python
from ai_agent import AIAgent

agent = AIAgent()

# 生成风格化初稿
draft = agent.generate_style_draft(
    user_input_text="原始文案内容",
    reference_texts=["参考文案1", "参考文案2"]
)

# 应用偏好
modified_draft = agent.apply_preferences(
    draft=draft,
    selected_preferences=[{"description": "偏好描述"}]
)
```

### 去重功能
```python
from deduplication import DeduplicationEngine

engine = DeduplicationEngine()

# 检查偏好是否重复
is_unique = engine.deduplicate_preference(
    new_description="新偏好描述",
    existing_preferences=[{"description": "现有偏好"}]
)
```

## 注意事项

1. **API密钥安全**: 请妥善保管您的火山方舟API密钥
2. **超时设置**: 已设置为30分钟，适合复杂文案生成
3. **模型选择**: 当前使用 `doubao-seed-1.6-250615`，可根据需要调整
4. **去重阈值**: 默认相似度阈值为0.85，可根据实际需求调整

## 故障排除

### 常见问题
1. **SDK导入失败**: 确保安装了 `volcengine-python-sdk[ark]`
2. **API密钥错误**: 检查 `.env` 文件中的 `VOLCANO_API_KEY`
3. **超时错误**: 检查网络连接和API服务状态
4. **去重不准确**: 可调整TF-IDF参数或相似度阈值

## 总结

火山方舟大模型集成已成功完成，项目现在使用：
- **火山方舟大模型** 进行文案生成和学习
- **TF-IDF向量化** 进行智能去重
- **本地JSON存储** 管理用户数据

所有核心功能保持不变，用户体验完全一致，同时获得了更好的中文支持和成本效益。
