---
week: W1
year: 2026
dates: 2026-07-03 ~ 2026-07-05
theme: "Hello AI：跑通第一个AI程序，建立环境与信心"
status: in-progress
---

# 🗓️ Week 1 · Hello AI：跑通第一个AI程序，建立环境与信心

> 本周是启动周，只有 3 天（周五到周日），目标只有一个：**跑通代码、建立正反馈、跑起来**。
> 不追求学多少东西，追求"我真的能让 AI 听我指挥"的感觉。

---

## 🎯 本周目标（3个，不贪多）

- [x] **G0**：环境配置完成（Python/API Key/依赖安装）
- [ ] **G1**：跑通 Day1-Day4 脚本（Hello AI → Prompt → Function Calling → 流式对话）
- [ ] **G2**：跑通 Day5 迷你 RAG，体验"给 AI 喂私有知识"
- [ ] **G3（加分）**：写第一篇学习笔记，做第一次周复盘

---

## 📓 每日进展

### 周五 7/3（启动日，1-2h）
- [ ] 读这份周计划
- [ ] 进入 `projects/week1-quickstart/`
- [ ] `pip install openai python-dotenv rich`
- [ ] 复制 `.env.example` 为 `.env`，填入 API Key
- [ ] 跑通 `python 01_hello_ai.py`，看到 AI 回答
- [ ] 成功后告诉我："Day1 跑通了！" → 我给你 Day2 讲解

**今日产出**：AI 在终端里回你一句话 🎉
**可能遇到的问题**：API Key 填错、网络不通、包安装失败 → 直接把错误信息发给我

### 周六 7/4（核心日，2-3h）
- [ ] Day2：跑 `02_prompt_playground.py`，观察 Zero-shot/Few-shot/CoT 的差异
- [ ] 试试修改问题，用你自己的问题测试 CoT 效果
- [ ] Day3：跑 `03_function_calling.py`，**重点读代码理解 ReAct 循环**
- [ ] 试着加一个自己的工具（比如"查询当前时间"）
- [ ] Day4：跑 `04_streaming_chat.py`，体验多轮对话+流式输出

**今日产出**：能和自己写的 AI 助手流畅聊天，理解"Agent 就是循环"
**关键概念**：CoT、Function Calling、ReAct 循环、流式输出

### 周日 7/5（RAG 日 + 复盘，2-3h）
- [ ] Day5-7：跑 `05_mini_rag.py`（需要 openai embedding 权限，用OpenAI/DeepSeek都可）
- [ ] 试着给 DOCUMENTS 数组里加你自己的文章，问相关问题
- [ ] **写下第一篇笔记**：用 `./scripts/new-note.sh "Week1总结-我的AI第一周"`
- [ ] **做第一次周复盘**：用 `./scripts/new-summary.sh weekly`
- [ ] git commit + push，记录你的第一个里程碑
- [ ] 回来告诉我"W1 完成了，我的感受是XXX"

**今日产出**：手写 RAG 跑通 + 第一篇笔记 + 第一次复盘
**里程碑**：🏁 从"想学AI"变成"写过AI代码的人"

---

## 🔍 本周学习笔记

- （周内逐步添加链接）

---

## 💡 本周重点理解的 5 个概念

1. **消息结构**：`messages = [system, user, assistant, user, assistant...]` 就是对话历史
2. **Token**：LLM 处理文本的基本单位，中文约 1 字 = 1-2 tokens，费用按 token 算
3. **Temperature**：0 = 确定性回答，1 = 创造性回答，根据场景调
4. **Function Calling**：LLM 不直接执行操作，而是"决定要调什么工具+生成参数"，你写代码执行
5. **RAG 本质**：检索相关文档拼到 Prompt 里，让 LLM 基于给定文本回答，不是什么魔法

---

## 🤔 思考题（周日答）

1. 为什么 LLM 能"理解"工具定义的 JSON Schema？这是真的理解还是模式匹配？
2. 流式输出在工程上是怎么实现的？（SSE / WebSocket 有什么区别？）
3. Mini RAG 里余弦相似度的取值范围是多少？为什么要归一化？
4. 如果让你给 Mini RAG 加一个"记忆对话历史"功能，你会怎么设计？
5. 下周想深入哪个方向？Prompt？Agent？RAG？

---

## 🔄 周日复盘（周日晚上填）

### ✅ 完成了
-

### ❌ 未完成，原因是
-

### 💡 最大收获/新认知
1.
2.
3.

### 🚩 下周方向预判
根据 W1 的感受我们周一定 W2 计划，候选方向：
- **A 线（推荐）**：Transformer/Self-Attention 原理 + nanoGPT 手撸 → 夯实基础
- **B 线**：Prompt 深度练习 + 更复杂的 Agent（多工具/多轮记忆） → 应用导向
- **C 线**：LangChain/LangGraph 框架入门 → 快速上手生产框架
