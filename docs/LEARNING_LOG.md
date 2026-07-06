# 📖 学习日志（归档）

> 按日期记录每天完成的学习内容，用于回顾。新会话不必读本文件。

---

## 2026-07-02 ~ 07-06（W1 启动周）

### 后端 MySQL 知识点
- **Q1 B+Tree 索引**：补充磁盘预读、内存连续、与跳表/B树/红黑树对比
- **Q2 Redo/Undo 日志**：物理逻辑日志区分，事务回滚与崩溃恢复
- **Q3 MVCC 幻读**：快照读 vs 当前读，隐藏字段、ReadView、Next-Key Lock
- 全部整理于 `docs/resources/后端面试满分速查.md`

### AI Agent 基础
- Prompt / Token / Temperature 核心概念
- RAG 完整知识点：向量化、检索、混合检索（BM25+向量）、Chunk策略、Rerank
- Function Calling：函数注册、参数填充、工具调用循环、安全校验
- 全部整理于 `docs/resources/AI面试速查.md`

### 简历项目包装
- **项目A：直播电商AI营销助手**（可信度⭐⭐⭐⭐⭐）
  - 结合现有业务：商卡营销价格/秒杀/竞拍/直播间召回
  - 融入用户行为存储（观看时长/下单/购买/点击）
  - 亮点：RAG防幻觉、个性化回答、自然语言运营取数、高并发、流式输出
  - 文件：`projects/project-A-直播电商AI营销助手.md`
- **项目B：AI运维Copilot**（可信度⭐⭐⭐⭐⭐）
  - 多Agent(LangGraph) + MCP Server + 故障根因分析
  - 文件：`projects/project-B-AI运维Copilot.md`
  - 计划 W10-W12 工程化骨架

### 工程约定
- 新增 `~/.codex/skills/task-status-report/SKILL.md`：任务中断必须报告
- 新建 `AGENTS.md` + `CURRENT_PROGRESS.md`：跨会话上下文持久化
