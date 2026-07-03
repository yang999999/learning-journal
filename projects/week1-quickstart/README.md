# 🚀 Week 1 启动包：7 天跑通 LLM 应用开发

> 第一周目标：**从"会调 API"到"理解 Agent 本质"**。7 个可运行脚本，每天一个，每步 30-60 分钟。

## 📦 环境准备（Day 0，30 分钟）

```bash
# 1. 进入项目目录
cd projects/week1-quickstart

# 2. 用 uv 建虚拟环境（推荐，快）
uv venv && source .venv/bin/activate
uv pip install -e .

# 或者用 pip
python3 -m venv .venv && source .venv/bin/activate
pip install openai python-dotenv rich

# 3. 配置 API Key
cp .env.example .env
# 编辑 .env，填入你的 OPENAI_API_KEY 和 OPENAI_BASE_URL
# （推荐国内用 DeepSeek/通义/智谱 的 OpenAI 兼容接口，价格便宜）
```

## 📅 7 天计划

| 天 | 脚本 | 目标 | 产出 |
|----|------|------|------|
| Day 1 | `01_hello_ai.py` | 第一次调用 LLM API，理解 messages 结构、token 用量 | 成功打印 AI 回答 |
| Day 2 | `02_prompt_playground.py` | 对比 Zero-shot/Few-shot/CoT，感受 Prompt 威力 | 理解 CoT 为什么有效 |
| Day 3 | `03_function_calling.py` | **手写 ReAct 循环**：LLM决策→调工具→观察→继续 | 理解 Agent 本质就是循环 |
| Day 4 | `04_streaming_chat.py` | 实现流式 CLI 聊天机器人（打字机效果+多轮记忆） | 掌握 stream=True 和消息历史 |
| Day 5-7 | `05_mini_rag.py` | **手写 RAG**（切片→Embedding→向量检索→生成） | 不依赖框架理解 RAG 全链路 |

## 🚀 运行方式

```bash
# 激活环境后
python 01_hello_ai.py
python 02_prompt_playground.py
python 03_function_calling.py
python 04_streaming_chat.py
python 05_mini_rag.py
```

## 🎯 一周后你应该能回答的问题

- [ ] LLM API 调用的 messages 结构里 system/user/assistant 各是什么角色？
- [ ] temperature 设 0 和 1 有什么区别？
- [ ] CoT（思维链）为什么能提升推理效果？
- [ ] Function Calling 是怎么让模型"用工具"的？（本质还是生成文本）
- [ ] Agent 为什么本质是个循环？循环怎么终止？
- [ ] 流式输出的 SSE 是什么原理？
- [ ] RAG 的完整链路是哪几步？Embedding 向量为什么能做检索？
- [ ] 余弦相似度怎么计算？为什么要归一化？

## ✅ Day 7 收尾任务

1. 运行 `./scripts/new-note.sh "Week1总结-我的AI入门周" "week1,入门"`，写一篇笔记
2. 运行 `./scripts/new-summary.sh weekly`，做第一次周复盘
3. 给自己在能力矩阵上打第一次分
4. git add + commit + push，记录你的第一个 AI 学习里程碑
