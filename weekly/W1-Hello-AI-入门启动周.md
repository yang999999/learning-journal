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
- [ ] **G2**：刷 3(MySQL)+3(Redis)+2(Kafka) = **8 道后端高频题**
- [ ] **G3**：写第一篇 AI 笔记 + 第一次周复盘 + 更新能力矩阵
- [ ] **G4**：完成 W1 所有 Day 任务，和助教确认开始 W2

---

## 📓 每日进展（按步骤打勾）

> 详细任务指引见：[每日学习执行指南](../../docs/resources/每日学习执行指南.md)

### 📅 周五 7/3 Day 1（启动日，约 1.5h）

□ **Step 1 学（20min）**
- [ ] 快速翻看后端面试速查 MySQL Q1-Q3（B+Tree/聚簇索引/MVCC）
- [ ] 理解 Prompt/Token/Temperature 三个概念（不懂就问助教）

□ **Step 2 验（5min）**
- [ ] 跑 `./scripts/quiz.sh mysql 2` 抽 2 道题口述答，对照速查，卡壳标★

□ **Step 3 练（60min）**
- [ ] cd projects/week1-quickstart/
- [ ] pip install openai python-dotenv rich
- [ ] cp .env.example .env → 填 API Key/Base URL
- [ ] 跑 python 01_hello_ai.py → 看到 AI 回答就是成功
- [ ] 试试改 system prompt 让它用古诗回答

□ **Step 4 记（5min）**
- [ ] 勾完成项，写一句话收获/卡点
- [ ] 告诉助教："Day1 完成"

---

### 📅 周六 7/4 Day 2（约 2.5h）

□ **Step 1 学（25min）**
- [ ] 后端：看 Redis Q1-Q3（为什么快/缓存三问题/分布式锁）
- [ ] AI：看 02/03 脚本开头注释，理解 CoT 和 Function Calling

□ **Step 2 验（10min）**
- [ ] `./scripts/quiz.sh redis 3` 口述答
- [ ] `./scripts/quiz.sh llm基础 1` 抽一道 LLM 题

□ **Step 3 练（100min）**
- [ ] 跑 python 02_prompt_playground.py，对比 Zero-shot/Few-shot/CoT
- [ ] 换你自己的业务问题测试 CoT
- [ ] 跑 python 03_function_calling.py，读代码理解 ReAct 循环
- [ ] [加分] 加一个你自己的工具（如查询当前时间）
- [ ] 跑 python 04_streaming_chat.py，和 AI 聊几句

□ **Step 4 记（15min）**
- [ ] 勾完成项，写一句话收获
- [ ] 思考题："Agent 本质是循环吗？怎么终止？"写下你的理解

---

### 📅 周日 7/5 Day 3（约 3h，里程碑日）

□ **Step 1 学（25min）**
- [ ] 后端：看 Kafka Q1-Q3（高吞吐/可靠性/顺序）
- [ ] AI：看 05_mini_rag.py 开头注释，理解 RAG 链路

□ **Step 2 验（10min）**
- [ ] `./scripts/quiz.sh kafka 2` 口述答
- [ ] `./scripts/quiz.sh rag 1` 抽一道 RAG 题

□ **Step 3 练（120min）—— 手写 RAG 大日子**
- [ ] 跑 python 05_mini_rag.py → 体验手写 RAG
- [ ] 动手：给 DOCUMENTS 数组加你自己的知识，问相关问题
- [ ] 思考：问一个文档里没有答案的问题，AI 会怎么答？会幻觉吗？

□ **Step 4 记 + 复盘（25min）**
- [ ] `./scripts/new-note.sh "Week1总结-我的AI第一周" "week1"` 写笔记
- [ ] 打开能力自检矩阵给自己第一次打分
- [ ] `./scripts/new-summary.sh weekly` 写第一次周复盘
- [ ] git add -A && git commit -m "完成W1" && git push
- [ ] 告诉助教："W1 完成，感受是___"

**🏁 W1 里程碑：从"想学AI"变成"能写AI应用的人"**

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
