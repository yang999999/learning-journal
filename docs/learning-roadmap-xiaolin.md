# 📚 学习路线图：以小林两个站为主教材

> 教材来源：
> - **AI 方向**（Agent/RAG/LLM/ClaudeCode）：https://xiaolinnote.com
> - **后端方向**（MySQL/Redis/Go/OS/面经）：https://www.xiaolincoding.com
>
> 策略：优先系统学习小林图解系列 → 学懂后在此基础上扩展（结合我们业务/AI项目写进速查文档）→ 每个技术栈知识点都能映射进《直播电商智能助手》项目。

---

## 一、MySQL 专题（xiaolincoding /mysql/）
> 用户重点：索引、存储引擎、事务、MVCC、锁、日志、BufferPool

| 小林章节 | 链接 | 我们已有进度 | 待补 |
|---|---|---|---|
| 架构 + select 流程 | /mysql/architecture/mysql_architecture.html、/mysql/base/how_select.html | Q7 SQL执行链路✅ | 存储引擎对比(InnoDB/MyISAM) |
| 行格式 row_format | /mysql/base/row_format.html | - | ❌ 补 |
| Buffer Pool | /mysql/buffer_pool/buffer_pool.html | 脏页/刷盘提过 | ❌ 重点补 BufferPool 管理 |
| 索引为什么 B+Tree | /mysql/index/why_index_chose_bpuls_tree.html | Q1✅ | - |
| 索引失效 | /mysql/index/index_lose.html | Q8✅ | 对照补 |
| 索引面试题 | /mysql/index/index_interview.html | - | ❌ 补 |
| MVCC | /mysql/transaction/mvcc.html | Q3✅ | - |
| 幻读 | /mysql/transaction/phantom.html、/mysql/lock/lock_phantom.html | Q4✅ | - |
| 锁 | /mysql/lock/mysql_lock.html 等 | Q4✅ | - |
| 两阶段提交/Redo | /mysql/log/redolog.html、/mysql/log/how_update.html | Q5✅ | 对照补 |
| 死锁 | /mysql/lock/deadlock.html | Q4提过 | 补死锁排查 |

## 二、Redis 专题（xiaolincoding /redis/）
> 用户重点：数据结构、持久化、缓存淘汰、高可用、缓存数据一致性

| 小林章节 | 链接 | 我们已有进度 | 待补 |
|---|---|---|---|
| 为什么快 | /redis/base/wath_is_redis.html | Q1✅ | - |
| 数据结构 | /redis/data_struct/data_struct.html | 提过 | ❌ 重点补底层(SDS/ziplist/skiplist) |
| 缓存一致性 | /redis/architecture/mysql_redis_consistency.html | Q9✅ | 对照补 |
| 缓存三灾 | /redis/cluster/cache_problem.html | Q2✅ | - |
| 分布式锁/Redlock | /redis/module/setnx.html、/redis/cluster/redlock.html | Q3✅ | 对照补 |
| 持久化 RDB/AOF | /redis/storage/rdb.html、/redis/storage/aof.html | 提过 | ❌ 重点补 |
| 淘汰策略 | /redis/module/strategy.html | Q5✅ | 对照补 |
| 主从/哨兵/Cluster | /redis/cluster/master_slave_replication.html、sentinel.html、cluster.html | - | ❌ 重点补高可用 |

## 三、Agent 专题（xiaolinnote）
> 用户重点：Agent架构、OpenClaw、GraphRAG、Harness工程 + AI Agent面试八股

| 小林章节 | 链接 | 我们已有进度 | 待补 |
|---|---|---|---|
| Agent 是什么/组件 | /ai/agent/1_whatisagent.html、2_components.html | 概念提过 | 系统补 |
| ReAct | /ai/agent/5_react.html | ✅ | - |
| 记忆机制 | /ai/agent/8_memory.html、9_memory_storage.html | 提过 | 重点补 |
| 多Agent | /ai/agent/10_multiagent.html、11_single_multi.html | Supervisor-Worker✅ | 对照补 |
| 上下文压缩 | /ai/agent/12_memcompress.html | - | ❌ 重点补(面试热点) |
| 规划/反思/协作 | /ai/agent/14_planning.html、15_reflection.html、16_collab.html | - | 补 |
| Agent概念(OpenClaw) | /agent/concept/agent.html、openclaw.html | - | ❌ 补 |
| Harness工程 | /agent/engineering/harness-engineering.html | - | ❌ 重点补 |
| GraphRAG | /agent/rag/graphrag-lightrag.html | - | ❌ 重点补 |
| LangGraph | /ai/langchain/*.html | B端设计✅ | 对照补 |

## 四、RAG 专题（xiaolinnote /ai/rag/，20篇）
> 用户重点：RAG高频知识

| 小林章节 | 链接 | 我们已有进度 | 待补 |
|---|---|---|---|
| RAG是什么/问题 | 1_whatisrag.html、2_rag_problems.html | ✅ | - |
| RAG vs 微调 | 3_rag_vs_finetune.html | - | 补 |
| 切片 | 4_chunking.html、5_semantic_cuts.html | ✅ | 对照补 |
| Embedding | 6_embedding.html、7_embedding_algos.html | BGE-M3✅ | 补原理 |
| 向量库 | 8_vectordb.html、9_vectordb_practice.html | Milvus✅ | 对照补 |
| 检索优化 | 11_retrieval_types.html、14_retrieval_opt.html | RRF✅ | 补 |
| Query改写 | 12_query_rewrite.html | - | 补 |
| 多路召回 | 13_multi_retrieval.html | ✅ | - |
| 图数据库 | 16_graph_db.html | - | 补 |
| 幻觉 | 17_hallucination.html | 三层防幻觉✅ | 对照补 |
| 评估 | 18_evaluation.html | RAGAS✅ | 对照补 |
| 动态更新 | 19_dynamic_update.html | - | 补 |

## 五、LLM 专题（xiaolinnote /ai/llm/）
> 用户重点：AI Agent面试八股里的LLM部分

| 小林章节 | 链接 | 我们已有进度 | 待补 |
|---|---|---|---|
| Transformer | transformer_architecture.html | Self-Attention✅ | 补整体架构 |
| KV Cache | kv_cache_prompt_caching.html | ✅ | 对照补 |
| MHA/MQA/GQA/FlashAttention | mha_mqa_gqa_flash_attention.html | GQA✅ | 补FlashAttention |
| LoRA | lora.html、finetuning.html | 概念讲过 | 落文档 |
| DPO vs PPO | dpo_vs_ppo.html | - | 补 |
| 量化 | quantization.html | QLoRA提过 | 补 |
| MoE | moe.html | - | 补 |
| 位置编码 | position_encoding.html | RoPE✅ | 对照补 |
| Tokenizer | tokenizer.html | - | 补 |
| 部署框架 | deployment_frameworks.html | vLLM提过 | 补 |

## 六、Tools/MCP 专题（xiaolinnote /ai/tools/，16篇）
> 用户重点：Function Calling、MCP、SSE、Agent工具

| 小林章节 | 链接 | 我们已有进度 | 待补 |
|---|---|---|---|
| Function Calling | 1_function_calling.html | ✅ | - |
| MCP | 4_what_is_mcp.html、6_mcp_vs_fc.html | ✅ | 对照补 |
| Skill | 9_skill.html | - | 补 |
| MCP vs Skill | 10_mcp_vs_skill.html | - | ❌ 重点补 |
| SSE vs WebSocket | 14_sse_vs_websocket.html | ✅ | - |
| A2A协议 | 12_a2a_protocol.html | - | 补 |

## 七、ClaudeCode 专题（xiaolinnote /claudecode/）
> 用户重点：主循环、上下文压缩、记忆机制、多Agent

| 小林章节 | 链接 | 说明 |
|---|---|---|
| 主循环 | /claudecode/source/cc_query_loop.html | ❌ 重点补 |
| 上下文压缩 | /claudecode/source/cc_compact.html | ❌ 重点补 |
| 记忆机制 | /claudecode/source/cc_memory.html | ❌ 重点补 |
| 多Agent | /claudecode/source/cc_multi_agent.html | ❌ 重点补 |
| Skill机制 | /claudecode/source/cc_skill.html、/claudecode/playbook/cc_skills.html | 我们有skill实操✅ |
| CLAUDE.md | /claudecode/playbook/cc_claude_md.html | 对照AGENTS.md |
| grep/工程 | /claudecode/source/cc_grep.html | - |

## 八、Golang 专题（xiaolincoding /interview/golang.html + os）
> 用户重点：Go基础、Channel、Slice、Map、Sync、GMP、垃圾回收、内存管理

| 主题 | 链接 | 说明 |
|---|---|---|
| Go基础/Channel/Slice/Map/Sync | /interview/golang.html | ❌ 全部待学 |
| GMP调度 | /os/4_process/*.html、goroutine 调度 | ❌ 重点补 |
| 垃圾回收 | GC 相关 | ❌ 重点补 |
| 内存管理 | /os/3_memory/*.html | 补 |
| Go并发模型 | Channel/Goroutine | ❌ 重点补 |

## 九、大厂后端面经（xiaolincoding /backend_interview/）
> 用户重点：大厂/中厂/手机厂/通信厂/新能源/银行面试题

| 类型 | 链接 | 说明 |
|---|---|---|
| 互联网大厂 | /backend_interview/internet_giants/*.html（字节/腾讯/阿里/美团/京东/快手等） | ❌ 补字节/腾讯重点 |
| 互联网中厂 | /backend_interview/internet_medium/*.html | 选看 |
| 手机厂 | /backend_interview/mobile/*.html（小米/OPPO/vivo） | 选看 |
| 通信厂 | /backend_interview/telecommunication/*.html（华为） | 选看 |
| 新能源 | /backend_interview/new_energy/*.html（比亚迪/极氪） | 选看 |
| 银行 | /backend_interview/bank/*.html | 选看 |

---

## 学习顺序建议（串行推进，每节学完落到速查文档+映射进项目）
> 优先级按用户最新指令调整：**Go 语言优先**（最不熟、面试最高频），MySQL/Redis 放最后（最熟悉、查漏补缺即可）。

1. **Golang 优先**：Go基础/Channel/Slice/Map/Sync → GMP调度 → 垃圾回收/内存管理（后端方向 xiaolincoding）
2. **AI 深化**：Agent体系(记忆/压缩/多Agent/Harness/OpenClaw/GraphRAG) → RAG深化 → LLM(FlashAttention/量化/MoE/DPO) → Tools(MCP vs Skill/A2A)
3. **ClaudeCode 源码**：结合我们实际用的 Codex 理解主循环/上下文压缩/记忆（AI Agent 面试加分点）
4. **MySQL/Redis 最后**：最熟悉，只补 BufferPool/存储引擎/数据结构底层/持久化/高可用等高频盲区
5. **大厂面经**：字节/腾讯优先，作为最终查漏补缺

> 项目始终用我们包装的《直播电商智能助手》，每个知识点学完都问"这个技术在我项目里怎么用/面试怎么结合项目讲"，避免学完忘。

## 参考包装项目（小林给的两个项目，看面试重点让包装更真实可深挖）
> 出处：https://xiaolincoding.com/project/
- **智能OnCall Agent**（/project/aioncallagent.html）：三个核心Agent（知识库/对话/运维）串起 RAG、Function Calling、ReAct、Plan-Execute-Replan、Multi-Agent、SSE 等整套 AI Agent 技术栈；**有 Java/Go/Python 三版本**（我们是 Go 后端，直接对齐 Go 版）——和我们包装的项目几乎一致，验证方向正确。附 60 道项目面试题，用于打磨我们项目的深挖细节。
- **MewCode Agent 项目**（/project/mewcode.html）：仿 Claude Code 的 CLI Coding Agent，Java/Go/Python/TS 四版本（我们是 Go 后端看 Go 版）。**5 层架构**：交互层(TUI/Slash/Skill) → 引擎层(Agent Loop/LLM/SubAgent) → 工具层(内置6工具/MCP/Hook) → 记忆层(上下文压缩/跨会话记忆) → 安全层(权限/Worktree隔离)。**面试亮点全是 Agent 岗位必考点**：Agent Loop 主循环终止条件(看模型返回有无 tool_use)、工具系统设计、System Prompt 工程、权限系统、MCP、Skill、上下文压缩与注入、记忆分层(短期/长期/项目级)、多Agent协作(SubAgent/Worktree/Agent Teams)。50+ 项目面试题。→ 用于对照，把我们的《直播电商智能助手》包装得真实、能深挖这些设计决策。
