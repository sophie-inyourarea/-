#!/usr/bin/env python3
"""
Web界面版本 - 在浏览器中使用文案风格个性化AI Agent
"""
import os
import json
from flask import Flask, render_template_string, request, jsonify
from data_manager import DataManager
from ai_agent import AIAgent
from deduplication import DeduplicationEngine

# 设置环境变量
os.environ["VOLCANO_API_KEY"] = "your_volcano_api_key_here"

app = Flask(__name__)

# 初始化组件
data_manager = DataManager()
ai_agent = AIAgent()
deduplication_engine = DeduplicationEngine()

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文案风格个性化AI Agent</title>
    <style>
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            line-height: 1.6;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid transparent;
            background: linear-gradient(90deg, #667eea, #764ba2) bottom/100% 3px no-repeat;
        }
        
        .header h1 {
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            font-size: 2.5rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        .header p {
            color: #6b7280;
            font-size: 1.1rem;
            margin: 0;
        }
        
        .step {
            margin-bottom: 30px;
            padding: 30px;
            border: 2px solid transparent;
            border-radius: 16px;
            background: linear-gradient(white, white) padding-box,
                        linear-gradient(135deg, #e5e7eb, #f3f4f6) border-box;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .step::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #e5e7eb, #f3f4f6);
            transition: all 0.3s ease;
        }
        
        .step.active {
            border-color: #667eea;
            background: linear-gradient(white, white) padding-box,
                        linear-gradient(135deg, #667eea, #764ba2) border-box;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
        }
        
        .step.active::before {
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .step.completed {
            border-color: #10b981;
            background: linear-gradient(white, white) padding-box,
                        linear-gradient(135deg, #10b981, #059669) border-box;
        }
        
        .step.completed::before {
            background: linear-gradient(90deg, #10b981, #059669);
        }
        
        .step h3 {
            color: #1f2937;
            margin-top: 0;
            margin-bottom: 20px;
            font-size: 1.4rem;
            font-weight: 600;
            display: flex;
            align-items: center;
        }
        
        .step p {
            color: #6b7280;
            margin-bottom: 20px;
            font-size: 0.95rem;
        }
        
        .step-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            text-align: center;
            line-height: 1;
            margin-right: 15px;
            font-weight: 600;
            font-size: 0.9rem;
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
        }
        
        .step.completed .step-number {
            background: linear-gradient(135deg, #10b981, #059669);
            box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
        }
        
        textarea, input[type="text"] {
            width: 100%;
            padding: 16px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
            transition: all 0.3s ease;
            background: #fafafa;
        }
        
        textarea:focus, input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        textarea {
            min-height: 100px;
        }
        
        .reference-textarea {
            margin-bottom: 15px;
        }
        
        button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            margin-right: 12px;
            margin-bottom: 12px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        button:hover::before {
            left: 100%;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        button:disabled {
            background: #d1d5db;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        button:disabled::before {
            display: none;
        }
        
        .result {
            background: linear-gradient(135deg, #f8fafc, #f1f5f9);
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 12px 12px 0;
            white-space: pre-wrap;
            font-size: 14px;
            line-height: 1.6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .preference-item, .rule-item {
            background: white;
            padding: 16px;
            margin: 12px 0;
            border-radius: 12px;
            border: 2px solid #e5e7eb;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .preference-item:hover, .rule-item:hover {
            background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
            border-color: #667eea;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        }
        
        .preference-item.selected, .rule-item.selected {
            background: linear-gradient(135deg, #e0f2fe, #bae6fd);
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        
        .checkbox {
            margin-right: 15px;
            width: 20px;
            height: 20px;
            accent-color: #667eea;
            cursor: pointer;
        }
        
        .item-text {
            flex: 1;
            font-size: 14px;
            line-height: 1.5;
            color: #374151;
        }
        
        .loading {
            text-align: center;
            color: #6b7280;
            font-style: italic;
            padding: 30px;
            font-size: 14px;
            position: relative;
        }
        
        .loading::after {
            content: '';
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid #e5e7eb;
            border-radius: 50%;
            border-top-color: #667eea;
            animation: spin 1s ease-in-out infinite;
            margin-left: 10px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .error {
            color: #dc2626;
            background: linear-gradient(135deg, #fef2f2, #fee2e2);
            padding: 16px;
            border-radius: 12px;
            margin: 15px 0;
            border-left: 4px solid #dc2626;
            font-size: 14px;
        }
        
        .success {
            color: #059669;
            background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            padding: 16px;
            border-radius: 12px;
            margin: 15px 0;
            border-left: 4px solid #059669;
            font-size: 14px;
        }
        
        .edit-options {
            display: flex;
            gap: 15px;
            margin: 20px 0;
        }
        
        .edit-options button {
            flex: 1;
            font-size: 13px;
            padding: 12px 20px;
        }
        
        .instruction-input {
            margin-top: 15px;
        }
        
        .hidden {
            display: none;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: linear-gradient(90deg, #e5e7eb, #f3f4f6);
            border-radius: 4px;
            margin-bottom: 30px;
            overflow: hidden;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 4px;
            transition: width 0.5s ease;
            position: relative;
        }
        
        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #374151;
            font-size: 14px;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .container {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .step {
                padding: 20px;
            }
            
            .edit-options {
                flex-direction: column;
            }
        }
        
        /* 滚动条美化 */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a67d8, #6b46c1);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 文案风格个性化AI Agent</h1>
            <p>根据您的写作风格生成个性化文案 - 按照5步工作流程</p>
        </div>

        <div class="progress-bar">
            <div class="progress-fill" id="progressFill" style="width: 0%"></div>
        </div>

        <!-- Step 1: 风格化初稿生成 -->
        <div class="step" id="step1">
            <h3><span class="step-number">1</span>📝 风格化初稿生成</h3>
            <p>根据用户输入的混乱观点和参考文案，生成一篇风格化的初稿</p>
            
            <div>
                <label><strong>原始文案：</strong></label>
                <textarea id="userInput" placeholder="请输入您要优化的原始混乱文案..."></textarea>
            </div>
            
            <div>
                <label><strong>参考文案1（必填）：</strong></label>
                <textarea id="reference1" class="reference-textarea" placeholder="用于定义风格的参考文案..."></textarea>
            </div>
            
            <div>
                <label><strong>参考文案2（可选）：</strong></label>
                <textarea id="reference2" class="reference-textarea" placeholder="第二个参考文案..."></textarea>
            </div>
            
            <button onclick="generateDraft()" id="generateBtn">生成风格化初稿</button>
            <div id="draftResult"></div>
        </div>

        <!-- Step 2: 交互式应用写作偏好 -->
        <div class="step" id="step2">
            <h3><span class="step-number">2</span>🎯 应用写作偏好</h3>
            <p>选择适用的历史写作偏好，并生成修改后的稿件</p>
            
            <div id="preferencesList">
                <div class="loading">加载偏好中...</div>
            </div>
            
            <button onclick="applyPreferences()" id="applyPrefBtn" disabled>应用选中的偏好</button>
            <div id="preferenceResult"></div>
        </div>

        <!-- Step 3: 交互式应用限制性规定 -->
        <div class="step" id="step3">
            <h3><span class="step-number">3</span>📋 应用限制性规定</h3>
            <p>选择适用的历史限制规则，生成AI的首次终稿</p>
            
            <div id="rulesList">
                <div class="loading">加载规则中...</div>
            </div>
            
            <button onclick="applyRules()" id="applyRuleBtn" disabled>应用选中的规则</button>
            <div id="ruleResult"></div>
        </div>

        <!-- Step 4: 多轮对话与编辑 -->
        <div class="step" id="step4">
            <h3><span class="step-number">4</span>✏️ 编辑</h3>
            <p>在AI生成的终稿基础上进行多轮修改，直到满意为止</p>
            
            <div id="currentDraftDisplay">
                <label><strong>当前文案：</strong></label>
                <div id="currentDraftText" class="result">请先完成前面的步骤</div>
            </div>
            
            <div class="edit-options">
                <button onclick="markSatisfied()" id="satisfiedBtn" disabled>满意 (y)</button>
                <button onclick="enableManualEdit()" id="manualEditBtn" disabled>自己修改 (e)</button>
                <button onclick="enableAIEdit()" id="aiEditBtn" disabled>让AI根据指令修改 (i)</button>
            </div>
            
            <div id="manualEditArea" class="hidden">
                <label><strong>手动编辑：</strong></label>
                <textarea id="manualEditText" placeholder="在这里编辑文案..."></textarea>
                <button onclick="confirmManualEdit()">确认修改</button>
            </div>
            
            <div id="aiEditArea" class="hidden">
                <label><strong>AI修改指令：</strong></label>
                <input type="text" id="aiInstruction" placeholder="请输入修改指令...">
                <button onclick="confirmAIEdit()">确认AI修改</button>
            </div>
            
            <div id="editResult"></div>
        </div>

        <!-- Step 5: 录入与学习 -->
        <div class="step" id="step5">
            <h3><span class="step-number">5</span>🧠 偏好更新 </h3>
            <p>从本次会话中学习新的偏好和规则，更新本地数据库</p>
            
            <div>
                <label><strong>AI生成的终稿：</strong></label>
                <div id="aiFinalDraft" class="result">请先完成前面的步骤</div>
            </div>
            
            <div>
                <label><strong>用户最终版本：</strong></label>
                <div id="userFinalDraft" class="result">请先完成前面的步骤</div>
            </div>
            
            <button onclick="learnFromSession()" id="learnBtn" disabled>开始学习</button>
            <div id="learnResult"></div>
        </div>
    </div>

    <script>
        let currentStep = 1;
        let selectedPreferences = [];
        let selectedRules = [];
        let currentDraft = '';
        let aiFinalDraft = '';
        let userFinalDraft = '';
        let userInstructions = [];

        // 更新进度条
        function updateProgress() {
            const progress = (currentStep / 5) * 100;
            document.getElementById('progressFill').style.width = progress + '%';
        }

        // 标记步骤完成
        function markStepCompleted(stepNum) {
            const step = document.getElementById('step' + stepNum);
            step.classList.add('completed');
            step.classList.remove('active');
        }

        // 激活步骤
        function activateStep(stepNum) {
            const step = document.getElementById('step' + stepNum);
            step.classList.add('active');
        }

        // 加载偏好和规则
        async function loadPreferences() {
            try {
                const response = await fetch('/api/preferences');
                const data = await response.json();
                
                const container = document.getElementById('preferencesList');
                container.innerHTML = '';
                
                if (data.preferences.length === 0) {
                    container.innerHTML = '<div class="loading">暂无可用偏好</div>';
                    return;
                }
                
                data.preferences.forEach((pref, index) => {
                    const div = document.createElement('div');
                    div.className = 'preference-item';
                    div.innerHTML = `
                        <input type="checkbox" class="checkbox" id="pref_${index}" onchange="togglePreference(${index})">
                        <div class="item-text">${pref.description}</div>
                    `;
                    container.appendChild(div);
                });
            } catch (error) {
                document.getElementById('preferencesList').innerHTML = '<div class="error">加载偏好失败</div>';
            }
        }

        async function loadRules() {
            try {
                const response = await fetch('/api/rules');
                const data = await response.json();
                
                const container = document.getElementById('rulesList');
                container.innerHTML = '';
                
                if (data.rules.length === 0) {
                    container.innerHTML = '<div class="loading">暂无可用规则</div>';
                    return;
                }
                
                data.rules.forEach((rule, index) => {
                    const div = document.createElement('div');
                    div.className = 'rule-item';
                    div.innerHTML = `
                        <input type="checkbox" class="checkbox" id="rule_${index}" onchange="toggleRule(${index})">
                        <div class="item-text">${rule.instruction}</div>
                    `;
                    container.appendChild(div);
                });
            } catch (error) {
                document.getElementById('rulesList').innerHTML = '<div class="error">加载规则失败</div>';
            }
        }

        function togglePreference(index) {
            const checkbox = document.getElementById('pref_' + index);
            if (checkbox.checked) {
                if (!selectedPreferences.includes(index)) {
                    selectedPreferences.push(index);
                }
            } else {
                selectedPreferences = selectedPreferences.filter(i => i !== index);
            }
            updatePreferenceButton();
        }

        function toggleRule(index) {
            const checkbox = document.getElementById('rule_' + index);
            if (checkbox.checked) {
                if (!selectedRules.includes(index)) {
                    selectedRules.push(index);
                }
            } else {
                selectedRules = selectedRules.filter(i => i !== index);
            }
            updateRuleButton();
        }

        function updatePreferenceButton() {
            const btn = document.getElementById('applyPrefBtn');
            btn.disabled = selectedPreferences.length === 0;
        }

        function updateRuleButton() {
            const btn = document.getElementById('applyRuleBtn');
            btn.disabled = selectedRules.length === 0;
        }

        // Step 1: 生成风格化初稿
        async function generateDraft() {
            const userInput = document.getElementById('userInput').value;
            const reference1 = document.getElementById('reference1').value;
            const reference2 = document.getElementById('reference2').value;
            
            if (!userInput || !reference1) {
                alert('请填写原始文案和至少一个参考文案');
                return;
            }

            const references = [reference1];
            if (reference2) references.push(reference2);

            // 显示加载状态
            const btn = document.getElementById('generateBtn');
            const originalText = btn.textContent;
            btn.textContent = '🔄 生成中...';
            btn.disabled = true;
            btn.classList.add('pulse');

            try {
                const response = await fetch('/api/generate-draft', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        user_input: userInput,
                        references: references
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    currentDraft = data.draft;
                    document.getElementById('draftResult').innerHTML = 
                        `<div class="result"><strong>✨ 风格化初稿：</strong><br>${data.draft}</div>`;
                    
                    // 进入下一步
                    markStepCompleted(1);
                    currentStep = 2;
                    activateStep(2);
                    updateProgress();
                } else {
                    document.getElementById('draftResult').innerHTML = 
                        `<div class="error">❌ 生成失败：${data.error}</div>`;
                }
            } catch (error) {
                document.getElementById('draftResult').innerHTML = 
                    `<div class="error">❌ 请求失败：${error.message}</div>`;
            } finally {
                // 恢复按钮状态
                btn.textContent = originalText;
                btn.disabled = false;
                btn.classList.remove('pulse');
            }
        }

        // Step 2: 应用偏好
        async function applyPreferences() {
            if (!currentDraft) {
                alert('请先生成初稿');
                return;
            }

            // 显示加载状态
            const btn = document.getElementById('applyPrefBtn');
            const originalText = btn.textContent;
            btn.textContent = '🔄 应用中...';
            btn.disabled = true;
            btn.classList.add('pulse');

            try {
                const response = await fetch('/api/apply-preferences', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        draft: currentDraft,
                        preference_indices: selectedPreferences
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    currentDraft = data.draft;
                    document.getElementById('preferenceResult').innerHTML = 
                        `<div class="result"><strong>🎯 应用偏好后：</strong><br>${data.draft}</div>`;
                    
                    // 进入下一步
                    markStepCompleted(2);
                    currentStep = 3;
                    activateStep(3);
                    updateProgress();
                } else {
                    document.getElementById('preferenceResult').innerHTML = 
                        `<div class="error">❌ 应用失败：${data.error}</div>`;
                }
            } catch (error) {
                document.getElementById('preferenceResult').innerHTML = 
                    `<div class="error">❌ 请求失败：${error.message}</div>`;
            } finally {
                // 恢复按钮状态
                btn.textContent = originalText;
                btn.disabled = false;
                btn.classList.remove('pulse');
            }
        }

        // Step 3: 应用规则
        async function applyRules() {
            if (!currentDraft) {
                alert('请先生成初稿');
                return;
            }

            try {
                const response = await fetch('/api/apply-rules', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        draft: currentDraft,
                        rule_indices: selectedRules
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    aiFinalDraft = data.draft;
                    currentDraft = data.draft;
                    document.getElementById('ruleResult').innerHTML = 
                        `<div class="result"><strong>应用规则后（AI终稿）：</strong><br>${data.draft}</div>`;
                    
                    // 更新显示
                    document.getElementById('currentDraftText').textContent = data.draft;
                    document.getElementById('aiFinalDraft').textContent = data.draft;
                    
                    // 进入下一步
                    markStepCompleted(3);
                    currentStep = 4;
                    activateStep(4);
                    updateProgress();
                    
                    // 启用编辑按钮
                    document.getElementById('satisfiedBtn').disabled = false;
                    document.getElementById('manualEditBtn').disabled = false;
                    document.getElementById('aiEditBtn').disabled = false;
                } else {
                    document.getElementById('ruleResult').innerHTML = 
                        `<div class="error">应用失败：${data.error}</div>`;
                }
            } catch (error) {
                document.getElementById('ruleResult').innerHTML = 
                    `<div class="error">请求失败：${error.message}</div>`;
            }
        }

        // Step 4: 多轮编辑
        function markSatisfied() {
            userFinalDraft = currentDraft;
            document.getElementById('userFinalDraft').textContent = userFinalDraft;
            
            markStepCompleted(4);
            currentStep = 5;
            activateStep(5);
            updateProgress();
            
            document.getElementById('learnBtn').disabled = false;
            
            document.getElementById('editResult').innerHTML = 
                '<div class="success">用户满意，进入学习阶段</div>';
        }

        function enableManualEdit() {
            document.getElementById('manualEditArea').classList.remove('hidden');
            document.getElementById('aiEditArea').classList.add('hidden');
            document.getElementById('manualEditText').value = currentDraft;
        }

        function confirmManualEdit() {
            const newDraft = document.getElementById('manualEditText').value;
            currentDraft = newDraft;
            document.getElementById('currentDraftText').textContent = newDraft;
            document.getElementById('manualEditArea').classList.add('hidden');
            
            document.getElementById('editResult').innerHTML = 
                '<div class="success">手动修改完成</div>';
        }

        function enableAIEdit() {
            document.getElementById('aiEditArea').classList.remove('hidden');
            document.getElementById('manualEditArea').classList.add('hidden');
        }

        async function confirmAIEdit() {
            const instruction = document.getElementById('aiInstruction').value;
            if (!instruction) {
                alert('请输入修改指令');
                return;
            }

            try {
                const response = await fetch('/api/ai-edit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        draft: currentDraft,
                        instruction: instruction
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    currentDraft = data.draft;
                    userInstructions.push(instruction);
                    document.getElementById('currentDraftText').textContent = data.draft;
                    document.getElementById('aiEditArea').classList.add('hidden');
                    document.getElementById('aiInstruction').value = '';
                    
                    document.getElementById('editResult').innerHTML = 
                        '<div class="success">AI修改完成</div>';
                } else {
                    document.getElementById('editResult').innerHTML = 
                        `<div class="error">AI修改失败：${data.error}</div>`;
                }
            } catch (error) {
                document.getElementById('editResult').innerHTML = 
                    `<div class="error">请求失败：${error.message}</div>`;
            }
        }

        // Step 5: 学习
        async function learnFromSession() {
            if (!aiFinalDraft || !userFinalDraft) {
                alert('请先完成前面的步骤');
                return;
            }

            try {
                const response = await fetch('/api/learn', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        ai_final_draft: aiFinalDraft,
                        user_final_draft: userFinalDraft,
                        user_instructions: userInstructions
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    document.getElementById('learnResult').innerHTML = 
                        `<div class="success">学习完成！新增 ${data.new_preferences} 个偏好，${data.new_rules} 个规则</div>`;
                    
                    markStepCompleted(5);
                    updateProgress();
                    
                    // 重新加载偏好和规则
                    loadPreferences();
                    loadRules();
                } else {
                    document.getElementById('learnResult').innerHTML = 
                        `<div class="error">学习失败：${data.error}</div>`;
                }
            } catch (error) {
                document.getElementById('learnResult').innerHTML = 
                    `<div class="error">请求失败：${error.message}</div>`;
            }
        }

        // 页面加载时初始化
        window.onload = function() {
            loadPreferences();
            loadRules();
            activateStep(1);
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/preferences')
def get_preferences():
    preferences = data_manager.get_user_preferences()
    return jsonify({'preferences': preferences})

@app.route('/api/rules')
def get_rules():
    rules = data_manager.get_restriction_rules()
    return jsonify({'rules': rules})

@app.route('/api/generate-draft', methods=['POST'])
def generate_draft():
    try:
        data = request.json
        user_input = data['user_input']
        references = data['references']
        
        draft = ai_agent.generate_style_draft(user_input, references)
        return jsonify({'success': True, 'draft': draft})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/apply-preferences', methods=['POST'])
def apply_preferences():
    try:
        data = request.json
        draft = data['draft']
        preference_indices = data['preference_indices']
        
        preferences = data_manager.get_user_preferences()
        selected_preferences = [preferences[i] for i in preference_indices]
        
        modified_draft = ai_agent.apply_preferences(draft, selected_preferences)
        return jsonify({'success': True, 'draft': modified_draft})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/apply-rules', methods=['POST'])
def apply_rules():
    try:
        data = request.json
        draft = data['draft']
        rule_indices = data['rule_indices']
        
        rules = data_manager.get_restriction_rules()
        selected_rules = [rules[i] for i in rule_indices]
        
        modified_draft = ai_agent.apply_restrictions(draft, selected_rules)
        return jsonify({'success': True, 'draft': modified_draft})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ai-edit', methods=['POST'])
def ai_edit():
    try:
        data = request.json
        draft = data['draft']
        instruction = data['instruction']
        
        modified_draft = ai_agent.modify_with_instruction(draft, instruction)
        return jsonify({'success': True, 'draft': modified_draft})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/learn', methods=['POST'])
def learn_from_edit():
    try:
        data = request.json
        ai_final_draft = data['ai_final_draft']
        user_final_draft = data['user_final_draft']
        user_instructions = data.get('user_instructions', [])
        
        # 学习偏好
        learned_preferences = ai_agent.learn_preferences(ai_final_draft, user_final_draft)
        existing_preferences = data_manager.get_user_preferences()
        
        new_preferences = 0
        for pref in learned_preferences:
            if deduplication_engine.deduplicate_preference(pref, existing_preferences):
                data_manager.add_user_preference(pref)
                new_preferences += 1
                existing_preferences.append({"description": pref})
        
        # 学习规则
        learned_rules = ai_agent.learn_rules(user_instructions)
        existing_rules = data_manager.get_restriction_rules()
        
        new_rules = 0
        for rule in learned_rules:
            if deduplication_engine.deduplicate_rule(rule, existing_rules):
                data_manager.add_restriction_rule(rule)
                new_rules += 1
                existing_rules.append({"instruction": rule})
        
        return jsonify({
            'success': True, 
            'new_preferences': new_preferences,
            'new_rules': new_rules
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🌐 启动Web界面...")
    print("📱 请在浏览器中访问: http://localhost:8080")
    print("🛑 按 Ctrl+C 停止服务")
    app.run(debug=True, host='0.0.0.0', port=8080)
