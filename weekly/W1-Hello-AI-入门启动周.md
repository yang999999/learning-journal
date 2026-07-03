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

## 🎯 本周目标（适配要求：后端刷题 + AI实战）

- [x] **G0**：仓库机制 + 面试速查 + 抽题脚本搭建完成
- [ ] **G1**：跑通 AI 实战（Hello AI → Prompt → Function Calling → 流式对话 → 手写RAG）
- [ ] **G2**：刷 8 道后端高频题（MySQL/Redis/Kafka），自我校验
- [ ] **G3**：写第一篇 AI 笔记 + 第一次周复盘

---

## 📓 每日进展

### 周五 7/3（启动日，1-2h）
- [x] **仓库环境**（已完成）
- [ ] 进入 `projects/week1-quickstart/`
- [ ] `pip install openai python-dotenv rich`（如已装跳过）
- [ ] 复制 `.env.example` 为 `.env`，填入 API Key
- [ ] 跑通 `python 01_hello_ai.py`，看到 AI 回答
- [ ] **后端热身**：运行 `./scripts/quiz.sh mysql 3`，自测3道MySQL题（答完看后端速查手册校对）
- [ ] 成功后告诉我："Day1 跑通了！"

**今日产出**：AI第一跑 + 3道MySQL题自测
**要点**：后端你日常在用，所以只做面试刷题，不重复实战

### 周六 7/4（AI核心实战 + 后端刷题，2-3h）
- [ ] **AI实战 Day2**：跑 `02_prompt_playground.py`，对比 Zero-shot/Few-shot/CoT 效果
- [ ] 用你自己的问题测试 CoT，感受 Prompt 对输出的影响
- [ ] **AI实战 Day3**：跑 `03_function_calling.py`，**重点读代码理解 ReAct 循环**
- [ ] 试着加一个自己的工具（比如"查询当前时间"/"查询IP"）
- [ ] **AI实战 Day4**：跑 `04_streaming_chat.py`，体验多轮记忆+打字机流式输出
- [ ] **后端刷题**：`./scripts/quiz.sh redis 3`，自测3道Redis题校对

**今日产出**：手写 ReAct 循环 + 流式聊天机器人 + 3道Redis题
**里程碑**：理解「Agent 本质 = LLM决策 + 工具执行 + 循环」

### 周日 7/5（RAG 实战 + 复盘，3h）
- [ ] **AI实战 Day5**：跑 `05_mini_rag.py`（手写完整RAG）
- [ ] 给 DOCUMENTS 数组加一篇你自己的文章，问相关问题 → 感受"给AI喂私有知识"
- [ ] **后端刷题**：`./scripts/quiz.sh kafka 2`，自测2道MQ题
- [ ] **写第一篇AI笔记**：`./scripts/new-note.sh "Week1总结-我的AI第一周" "week1,入门"`
- [ ] **第一次周复盘**：`./scripts/new-summary.sh weekly`，对照能力矩阵打第一次分
- [ ] git commit + push → 告诉我"W1 完成了，我最大的感受是XXX"

**今日产出**：手写RAG跑通 + 5道MQ题 + 第一篇笔记 + 第一次复盘
**里程碑**：🏁 从"想学AI"变成"能写AI应用的人"

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
