# 📚 持续学习仓库

> 记录学习资料、笔记与复盘总结，保持终身学习的习惯。

## 📂 目录结构

```
learning-journal/
├── docs/
│   ├── notes/          # 学习笔记（按主题/日期组织）
│   ├── summaries/      # 复盘总结（周/月/季度/年复盘）
│   └── resources/      # 学习资源整理（书单、课程、文章等）
├── templates/          # 笔记和复盘模板
├── scripts/            # 实用脚本
└── README.md
```

## 🔄 周迭代学习模式

本仓库采用**敏捷周迭代**方式推进学习：
- **每周一定计划**：明确 3-5 个可交付目标
- **周内每天推进**：有问题随时找 AI 助教讨论、Debug、出题
- **周日做复盘**：总结收获、更新能力矩阵、调整下周方向
- 每周计划见 `weekly/` 目录，当前周：[W1 · Hello AI 入门启动周](weekly/W1-Hello-AI-入门启动周.md)
- 协作方式见 [周迭代SOP](docs/resources/周迭代学习SOP.md)

## 🚀 快速开始

### 新建一篇学习笔记

```bash
./scripts/new-note.sh "主题名称"
```

### 新建一次复盘总结

```bash
./scripts/new-summary.sh weekly    # 周复盘
./scripts/new-summary.sh monthly   # 月复盘
./scripts/new-summary.sh quarterly # 季度复盘
./scripts/new-summary.sh yearly    # 年复盘
```

### 面试刷题（后端+AI高频题随机抽）

```bash
./scripts/quiz.sh              # 随机抽5题
./scripts/quiz.sh mysql 3      # 抽3道MySQL题
./scripts/quiz.sh rag 5        # 抽5道RAG题
# 支持模块: mysql/redis/kafka/分布式/事务/Docker/LLM基础/RAG/微调/Agent
```

### 新建一周学习计划

```bash
./scripts/new-week.sh 2 "LangGraph深度实践"
```

## 📝 笔记规范

- 文件名格式：`YYYY-MM-DD-主题.md`，例如 `2026-07-02-Python异步编程.md`
- 使用 Markdown 格式书写
- 每篇笔记建议包含：学习目标、核心要点、实践示例、疑问与思考
- 善用标签（tags）分类，便于后续检索

## 🔄 复盘框架

复盘采用 **GRAI 方法**（Goal - Result - Analysis - Insight）：

1. **Goal（目标回顾）**：当初设定的目标是什么？
2. **Result（结果对比）**：实际结果如何？哪些做得好？哪些有待改进？
3. **Analysis（原因分析）**：成功/失败的根本原因是什么？
4. **Insight（规律总结）**：学到了什么？下次如何改进？

## 📊 学习状态

| 周期    | 笔记数 | 复盘数 | 关键收获 |
|---------|--------|--------|----------|
| 2026 Q3 | 2      | 0      | AI Agent 转型知识体系搭建完成 |

## 🔥 AI Agent 转型专题

> 🎯 面向后端工程师转型 AI Agent 方向的体系化学习资料

| 文档 | 说明 | 链接 |
|------|------|------|
| 📘 体系化技术知识手册 | 7 大模块（MySQL/MQ/Redis/分布式/事务/Docker/AI Agent）三段式（知识点→原理→面试题） | [查看](docs/notes/2026-07-02-AI-Agent技术知识手册.md) |
| 🗺️ 五段式学习路线 | 基础地基→LangChain/LangGraph→RAG→微调→Agent工程化，18周计划 | [查看](docs/resources/AI-Agent转型学习路线.md) |
| 🧠 学习方法论执行手册 | 费曼技巧+项目驱动+刻意练习，避坑指南+每日/每周节奏+资深能力标准 | [查看](docs/resources/学习方法论执行手册.md) |
| 📊 能力自检矩阵 | 13大类80+能力项，5分制打分，月度追踪成长进度 | [查看](docs/resources/能力自检矩阵.md) |
| 🚀 Week1 启动包 | 7天可运行代码脚手架（Hello AI→Prompt→Function Calling→流式对话→手写RAG） | [查看](projects/week1-quickstart/) |
| 📚 项目A：企业级 RAG 智能知识库 | 全链路优化+工程化，覆盖 RAG 面试考点 | [查看](projects/project-A-RAG智能知识库.md) |
| 🤖 项目B：AI 智能运维 Copilot | 多Agent + MCP + HITL，Agent 架构面试全覆盖 | [查看](projects/project-B-AI运维Copilot.md) |
| 📕 后端面试满分速查 | MySQL/Redis/MQ/分布式/事务/Docker 高频面试题满分答案 | [查看](docs/resources/后端面试满分速查.md) |
| 🤖 AI Agent面试满分速查 | Transformer/RAG/微调/Agent 面试题+实战项目对应 | [查看](docs/resources/AI-Agent面试满分速查.md) |
| 📋 每日学习执行指南 | **每天照着做**：学→验→练→记四步，面试满分导向 | [查看](docs/resources/每日学习执行指南.md) |
| 🎲 面试抽题脚本 | 随机抽题自测，`./scripts/quiz.sh [模块] [数量]` | 见下 |

## 🛠 工具推荐

- **笔记**：Markdown + VS Code / Obsidian
- **思维导图**：XMind / Mermaid
- **闪卡复习**：Anki
- **阅读管理**：Zotero / Pocket

## 📜 License

MIT
