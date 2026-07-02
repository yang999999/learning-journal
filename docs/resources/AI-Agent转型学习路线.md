---
title: "后端转 AI Agent：五段式系统学习清单"
date: 2026-07-02
tags: ["AI-Agent", "学习路线", "后端转型", "面试"]
category: "学习规划"
status: in-progress
---

# 🗺️ 后端工程师 → AI Agent 开发：五段式系统学习清单

> 面向有后端基础（3年+）、想系统转型 AI Agent 方向的工程师。按 **基础地基 → LangChain/LangGraph → RAG → 微调 → Agent 工程化** 五段推进，每个模块拆到工作落地和面试追问的粒度。
>
> **核心策略**：先打通**应用开发线**（LangChain + RAG + Agent 工程化）就能胜任绝大多数 Agent 开发岗；微调作为进阶分水岭。基础地基不可跳过——Transformer/Self-Attention/Prompt 是所有追问的落点，90%+ 岗位面试先问大模型基础。
>
> **面试趋势（2026）**：重心已从"大模型基础"转向"AI 应用落地"，Agent 架构、RAG 全链路、工程化能力是社招/校招必刷方向。

---

## 📊 学习路线总览

```
阶段1            阶段2              阶段3            阶段4           阶段5
基础地基    →  LangChain/     →   RAG 全链路  →   大模型微调  →   Agent 工程化
(4周)           LangGraph(3周)     (4周)            (3周，进阶)      (3周)
                                                                    ↓
                                                          完整项目+面试冲刺(2周)
═══════════════════════════════════════════════════════════════════════════════
总计：约 17-19 周（4-5个月）可面试就绪（每天2-3小时）
```

| 阶段 | 模块 | 目标 | 产出物 |
|------|------|------|--------|
| **P1** | 基础地基 | 理解 LLM 原理+Prompt 工程+Python 生态 | 实现一个 GPT 从零训练（tiny 级）+ Prompt 库 |
| **P2** | LangChain/LangGraph | 熟练 Agent 框架，能快速搭建 ReAct Agent | 3个 demo Agent + LangGraph 状态机项目 |
| **P3** | RAG 全链路 | 独立设计生产级 RAG 系统 | 完整 RAG 系统（含评估）+ RAG 优化报告 |
| **P4** | 大模型微调 | 掌握 LoRA/QLoRA/SFT/DPO 全流程 | 微调一个垂直领域 7B 模型+评测报告 |
| **P5** | Agent 工程化 | 可观测/部署/安全/性能/多 Agent | 完整 Agent 服务（可观测+部署+安全） |
| **P6** | 项目+面试 | 整合输出，准备面试 | GitHub 项目 + 简历 + 模拟面试 |

---

## P1 · 基础地基（约 4 周）

> 不可跳过！90%+ AI 岗位面试前 15 分钟必问 LLM 基础。不要跳过原理直接调 API。

### 1.1 Transformer 与大模型原理（1.5 周）

**✅ 学完要能说清**

- [ ] Self-Attention 数学公式 + 为什么要除以 √d_k + Multi-Head 的意义
- [ ] Encoder 和 Decoder 的结构差异（BERT vs GPT 的根本区别）
- [ ] Positional Encoding（正余弦位置编码 vs RoPE）
- [ ] LayerNorm 为什么比 BatchNorm 在 NLP 中更好；Pre-Norm vs Post-Norm
- [ ] GPT-2/3/4 的关键演进（规模法则 / InstructGPT 三阶段 / RLHF）
- [ ] LLaMA 系列的关键设计（RMSNorm / SwiGLU / RoPE / GQA）
- [ ] Tokenization：BPE 算法原理、中文分词坑点、Token 长度计算
- [ ] 采样策略：Greedy / Beam Search / Temperature / Top-K / Top-P / Repetition Penalty

**🎬 学习资源**
- 视频：李沐《动手学深度学习》Transformer 章节；3Blue1Brown Attention 可视化
- 论文：《Attention Is All You Need》（必读原文，精读 3 遍）、《GPT-3》、《LLaMA》
- 代码：[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)（自己跑一遍，理解训练流程）、[Andrej Karpathy Let's Build GPT 视频](https://www.youtube.com/watch?v=kCc8FmEb1nY)

**💻 动手任务**
1. 用 PyTorch 手撸一个迷你 GPT（nanoGPT 级别），在 Shakespeare 数据集上训练，能生成文本
2. 手动实现 Self-Attention、Multi-Head Attention、RoPE（用纯 NumPy/PyTorch）
3. 阅读 HuggingFace Transformers 中 LLaMA 的 modeling_llama.py 源码（重点是 Attention 和 MLP）

**🔥 面试追问落点**
- Q: 为什么 Self-Attention 是 O(n²) 复杂度？长上下文怎么优化？（FlashAttention/Sliding Window/Linear Attention）
- Q: KV Cache 是什么？训练和推理为什么不一样？（训练并行计算所有 token，推理自回归，缓存 K/V 减少重复计算）
- Q: MHA / MQA / GQA 区别？为什么 LLaMA-2/3 用 GQA？（MQA 快但质量略降，GQA 分组折中）

### 1.2 Prompt Engineering（1 周）

**✅ 学完要能说清**

- [ ] Zero-shot / Few-shot / CoT（Chain-of-Thought）/ Self-Consistency 区别与适用场景
- [ ] ReAct 范式（Reasoning + Acting 交替）
- [ ] System Prompt 设计原则（角色设定/输出格式/约束/示例）
- [ ] 结构化输出：JSON Mode / Function Calling 原理与使用
- [ ] Prompt 防注入基础、Prompt 模板管理

**🎬 学习资源**
- OpenAI / Anthropic 官方 Prompt Engineering Guide
- 论文：《Chain-of-Thought Prompting》、《ReAct: Synergizing Reasoning and Acting》
- 实践：[OpenAI Cookbook](https://github.com/openai/openai-cookbook)、[Prompt Engineering Guide](https://www.promptingguide.ai/)

**💻 动手任务**
1. 构建个人 Prompt 库（角色/写作/代码/分析/抽取等 5+ 类模板）
2. 用 Few-shot + CoT 解决一个具体业务问题（如从文本抽取结构化信息），对比 zero-shot 效果
3. 实现一个 Function Calling demo：让模型选择工具+提取参数+执行

**🔥 面试追问落点**
- Q: 为什么 CoT 能提升推理能力？什么时候 CoT 无效？（简单任务不需要/小模型不具备推理能力）
- Q: 怎么设计一个稳定的 JSON 输出 Prompt？（Schema 定义+示例+重试+正则兜底）

### 1.3 Python AI 生态与基础工具（1.5 周）

**✅ 学完要能说清**

- [ ] Python 异步编程（asyncio / aiohttp / async/await）—— Agent 大量用异步
- [ ] FastAPI / Pydantic v2（构建 AI 服务的标配）
- [ ] HuggingFace 三件套：Transformers / Datasets / Tokenizers
- [ ] 向量基础：numpy 余弦相似度、归一化、相似度检索手写实现
- [ ] 开发环境：Conda/UV、Jupyter、WSL/Linux 基础、Git 规范
- [ ] （可选）CUDA 基础：PyTorch 张量操作、GPU 张量放置、显存查看

**🎬 学习资源**
- FastAPI 官方教程（1天快速过）
- HuggingFace NLP Course（免费）
- Python asyncio 官方文档

**💻 动手任务**
1. 用 FastAPI 搭一个 OpenAI API 兼容的聊天服务（支持流式 SSE）
2. 用 Datasets 库加载一个开源数据集并做数据清洗
3. 手写一个暴力余弦相似度检索（1000 条文档，对 Query 查 Top-10）

---

## P2 · LangChain / LangGraph（约 3 周）

> LangGraph 已经成为 2026 年 Agent 开发的事实标准，LangChain 传统 Agent 了解即可，**重点放 LangGraph**。

### 2.1 LangChain 核心组件（1 周）

**✅ 学完要能说清**

- [ ] 核心抽象：ChatModel / PromptTemplate / OutputParser / Retriever / Tool / Chain
- [ ] LCEL（LangChain Expression Language）：管道符 `|` 组合、Runnable 接口、流式/批/异步
- [ ] Tool 定义与 Function Calling 绑定
- [ ] Memory 类型：ConversationBuffer/Summary/VectorStore/Entity
- [ ] 传统 Agent：ZeroShotAgent / ReAct Agent / AgentExecutor 运行机制
- [ ] LangChain 生态：LangSmith 可观测、文档加载器（PyPDF/Unstructured/BeautifulSoup）

**💻 动手任务**
1. 实现一个"论文阅读助手"：加载 PDF → 切片存向量 → 用户提问 → 检索+回答
2. 实现一个"多工具助手"：能调用搜索（Tavily API）、计算器、天气查询三个工具
3. 对比 LCEL 管道 vs 手写调用 LLM 的代码量和灵活性

### 2.2 LangGraph 深度掌握（2 周）🔥 重点

**✅ 学完要能说清**

- [ ] LangGraph 核心抽象：StateGraph / Node / Edge / Conditional Edge / END
- [ ] State 设计：TypedDict / Pydantic 状态、Reducer（注解合并列表/追加消息）
- [ ] 图模式：线性图、分支路由、循环（ReAct 循环）、并行节点（Send）
- [ ] Checkpointer：Sqlite/Postgres/Redis 持久化、断点/恢复/时间旅行/人工审批（Human-in-the-loop）
- [ ] ToolNode + 条件边实现自动 ReAct 循环
- [ ] Subgraph（子图嵌套）实现复杂 Agent 架构
- [ ] Streaming：流式输出（token 流/消息流/更新流）

**🎬 学习资源**
- LangGraph 官方文档 Tutorials（全过一遍）
- LangGraph Academy / YouTube 官方教程
- 源码阅读：langgraph/graph/state.py

**💻 动手任务**
1. **必做**：手写 ReAct Agent（不用预构建 create_react_agent）：自己实现 agent 节点 + tools 节点 + 条件边
2. **必做**：在 ReAct 基础上加人工审批节点（调用敏感工具前暂停等确认）
3. 实现 Supervisor-Worker 多 Agent 架构：Supervisor 根据任务派发给 Researcher/Coder/Writer 三个 Worker
4. 给 Agent 加 Sqlite Checkpointer，支持跨会话记忆
5. 实现流式输出（SSE）+ LangSmith 可观测

**🔥 面试追问落点**
- Q: LangGraph vs 传统 LangChain Agent 本质区别？（显式状态机 vs 黑盒 LLM 循环）
- Q: Checkpointer 怎么实现的？怎么支持多轮对话记忆？（每个 superstep 保存状态快照，thread_id 隔离）
- Q: 怎么在 Agent 里处理工具调用失败/格式错误？（OutputParser 重试/约束 LLM 输出 JSON schema）
- Q: 如何设计一个多 Agent 协作系统？（Supervisor 路由/Swarm 平等/GDAN 等架构对比）

---

## P3 · RAG 全链路（约 4 周）🔥 面试最重

> 2026 年 AI 应用落地最成熟的方向，面试必考。**RAG 优化是 RAG 工程师的核心竞争力**。

### 3.1 RAG 基础流程（1 周）

**✅ 学完要能说清**

- [ ] 完整链路：文档加载 → 切片 → Embedding → 向量存储 → 检索 → Rerank → Prompt 组装 → LLM 生成
- [ ] 文档切片策略：
  - 固定长度 + Overlap（256/512/1024 tokens，overlap 10-20%）
  - 递归字符切片（RecursiveCharacterTextSplitter，按段落→句子→字符递归）
  - 语义切片（Semantic Chunking，按语义相似度断点）
  - 结构化切片（Markdown 按标题层级/代码单独切）
  - 父子文档（Parent-Child Retrieval：存小 chunks 用于检索，返回大 chunks 用于生成）
- [ ] Embedding 模型选型：OpenAI text-embedding-3-small/large、BGE-M3（多语言+长文本）、M3E（中文）、bce-embedding
- [ ] 向量数据库选型与对比：
  - 轻量本地：Chroma / FAISS / LanceDB（开发测试）
  - 生产级：Milvus / Qdrant / Weaviate / Pgvector（PostgreSQL 扩展）
  - 云服务：Pinecone
- [ ] HNSW 近似最近邻索引原理（分层导航小世界，构建/查询流程，ef_construction/M 影响）
- [ ] 距离度量：余弦相似度 vs 欧氏距离 vs 点积（归一化后余弦=点积）

**💻 动手任务**
1. 不用 LangChain，手写完整 RAG：用 PyPDF 读 PDF → 递归切片 → BGE-M3 Embedding → FAISS 存储→余弦相似度检索 → 拼 Prompt 调用 Qwen 生成回答
2. 对比不同 chunk_size（256/512/1024/2048）对检索效果的影响，用 10 个问题做定性评估

### 3.2 RAG 进阶优化（2 周）

**✅ 学完要能说清**

- [ ] **Query 层优化**：
  - HyDE（Hypothetical Document Embeddings）：先生成假设答案再用答案检索
  - Multi-Query：LLM 生成多个角度的查询并行检索
  - Step-Back Prompting：先抽象问题再检索
  - Query Rewrite：用 LLM 改写/扩展/分解用户问题
  - Sub-Query：复杂问题拆成子问题分别检索
- [ ] **检索层优化**：
  - 混合检索（Hybrid Search）：BM25（稀疏）+ 向量（稠密），RRF 融合排序
  - Metadata 过滤（时间/来源/权限/分类）
  - 多路召回（向量+关键词+知识图谱）
  - MMR（Maximal Marginal Relevance）：提升结果多样性
- [ ] **排序层优化**：
  - Reranker 模型：bge-reranker / Cohere Rerank / cross-encoder
  - 为什么 Cross-Encoder 比 Bi-Encoder 准但慢（无嵌入缓存、查询-文档交叉计算注意力）
- [ ] **上下文层优化**：
  - Context Compression（LLMLingua 压缩/LLM Extract）
  - 引用标注（每段标来源，答案带引用）
  - 长上下文策略：Map-Reduce / Refine / Parent-Document
- [ ] **Graph RAG**：微软 GraphRAG（知识图谱抽取+社区摘要+全局/本地查询）
- [ ] **Agentic RAG**：Agent 自主决定何时检索、用什么策略检索、是否需要多轮检索

**🎬 学习资源**
- 论文：《Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks》（RAG 原始论文）
- 博客：LlamaIndex Advanced RAG Guide、RAGAS 文档
- 代码：[microsoft/graphrag](https://github.com/microsoft/graphrag)、[run-llama/llama_index](https://github.com/run-llama/llama_index)（看 advanced 部分）

**💻 动手任务**
1. 在基础 RAG 上叠加：Query Rewrite + 混合检索（BM25+BGE）+ BGE Rerank，对比优化前后效果
2. 实现 Parent-Child 检索：小 chunks 检索，返回父文档段落
3. 实现 Agentic RAG：Agent 可以决定检索→评估相关性→不够就改写再检索→最终回答

### 3.3 RAG 评估与调优（1 周）

**✅ 学完要能说清**

- [ ] RAG 评估指标体系：
  - 检索指标：Recall@K / Precision@K / MRR / NDCG
  - 生成指标：Faithfulness（忠实度/反幻觉）/ Answer Relevancy / Context Precision / Context Recall
- [ ] 评估框架：RAGAS / TruLens / DeepEval
- [ ] Golden Dataset 构建：人工标注 / LLM-as-Judge 辅助 / 合成数据生成
- [ ] Bad Case 分析方法论：分类（漏检/误检/上下文足够但答不对/幻觉）→ 针对性优化
- [ ] A/B 测试框架：线上如何验证 RAG 优化效果

**💻 动手任务**
1. 构造 50+ 问题的评测集（自己业务/技术文档场景）
2. 用 RAGAS 评估你的 RAG 系统（Faithfulness/Relevancy 等指标）
3. 针对 bad case 做一轮定向优化，量化指标提升
4. 输出一份 RAG 优化报告（问题→方法→指标变化）

**🔥 面试高频追问**
- Q: RAG 中 Chunk Size 怎么选？（取决于 Embedding 模型最佳长度+文档类型+查询类型，需要实验对比）
- Q: 混合检索中 BM25 和向量怎么融合？（RRF 最常用：score=1/(k+rank)，k 通常取60；或加权分数）
- Q: 怎么解决 RAG 中的幻觉？（Prompt约束+引用来源+Faithfulness评估+兜底"不知道"+Fact Check）
- Q: 表格/代码/图片怎么处理？（表格：HTML/markdown 保留结构/TableSummary；代码：按函数/类切；图片：多模态VLM+图片描述）
- Q: 多轮对话 RAG 怎么做？（需要先做 Query Rewrite 把指代消解，如"它是什么"→"Python GIL 是什么"）

---

## P4 · 大模型微调（约 3 周，进阶分水岭）

> 应用开发岗面试高频但不一定要求实操，能讲清原理即可；**算法/模型岗**需要真实微调经验。但 2026 年"微调+应用"复合人才非常抢手。

### 4.1 微调理论基础（1 周）

**✅ 学完要能说清**

- [ ] 为什么要微调？（通用模型→垂直领域/特定风格/特定格式/工具调用能力注入）
- [ ] 微调范式对比：
  - **Full Fine-Tuning**：全参微调，效果好但显存需求大（7B 模型 fp16 约 140GB 显存）
  - **LoRA**：低秩适配，只训旁路矩阵，参数约原模型的 0.1%-1%，单卡可训
  - **QLoRA**：4bit 量化基础模型+LoRA，24GB 卡可训 70B，效果接近 LoRA
  - **P-Tuning v2 / Prefix-Tuning**：只在输入端加可训练前缀
  - **Prompt Tuning**：Soft Prompt，最简单
  - **DoRA / AdaLoRA / LoRA+**：LoRA 的改进变体
- [ ] LoRA 数学原理：W = W₀ + BA，B∈R^{d×r}, A∈R^{k×r}，秩 r、alpha（缩放系数=alpha/r）
- [ ] LoRA 训练细节：target_modules 选择（q_proj/v_proj 还是所有线性层）、dropout、merge 推理
- [ ] 微调数据格式：Alpaca 格式（instruction/input/output）、ShareGPT 格式（messages 多轮对话）
- [ ] SFT（Supervised Fine-Tuning）：指令微调，教模型"按指令格式回答"

**🎬 学习资源**
- 论文：《LoRA: Low-Rank Adaptation of Large Language Models》
- 论文：《QLoRA: Efficient Finetuning of Quantized LLMs》
- Huatuo-Llama-Med-Chinese / Alpaca-LoRA 源码（看数据格式）

### 4.2 微调实操（1.5 周）

**✅ 学完要能说清**

- [ ] 框架选择：
  - **Llama-Factory**：开箱即用，支持 100+ 模型，Web UI，强烈推荐入门
  - **Unsloth**：训练速度快 2-5 倍，显存省 50%+
  - **TRL (Transformers Reinforcement Learning)**：HuggingFace 官方，SFT/DPO/PPO 全栈
  - **DeepSpeed**：ZeRO 1/2/3 显存优化（训练大模型必备）
- [ ] 数据工程：
  - 数据清洗：去重（MinHash/SimHash）、去毒、过滤低质（perplexity 过滤/规则过滤）
  - 数据构造：真实业务数据 > GPT-4 蒸馏 > Self-Instruct > Evol-Instruct（进化指令）
  - 数据格式统一、多样性覆盖、质量 >> 数量（1 万条高质量 > 100 万条低质量）
  - 数据比例：通用对话:专业任务:工具调用 ≈ 3:5:2（Agent 场景）
- [ ] 训练超参：
  - batch_size / gradient_accumulation / learning_rate（LoRA 通常 1e-4~2e-4）/ epoch（2-5）
  - warmup / lr_scheduler（cosine）/ max_seq_length / weight_decay
- [ ] 常见问题：过拟合（loss 曲线/loss 反弹）、灾难性遗忘（混入通用数据）、Loss NaN（降 LR/检查数据）
- [ ] 模型合并与导出：LoRA merge 到原模型、导出 GGUF（llama.cpp 推理）/ AWQ/GPTQ 量化

**💻 动手任务**
1. 用 Llama-Factory + QLoRA 在一张 GPU（Google Colab A100/本地 3090/4090）上微调 Qwen2.5-7B-Instruct 或 LLaMA-3-8B
2. 准备自己的数据集（可从公开 Alpaca/COIG 等中文数据集裁剪 5000 条）
3. 训练完成用 vLLM/Ollama 部署，对比微调前后的回答质量
4. 做一组消融实验：对比 r=8/16/64、target_modules 不同选择的效果差异

### 4.3 对齐与评测（0.5 周）

**✅ 学完要能说清**

- [ ] 对齐技术演进：SFT → RLHF（PPO） → DPO → ORPO / KTO / SimPO
- [ ] RLHF 三阶段：SFT → Reward Model 训练 → PPO 强化学习（工程复杂，奖励黑客问题）
- [ ] DPO（Direct Preference Optimization）：跳过 RM，直接用偏好对优化策略，数学等价 RLHF 最优解，训练稳定简单
- [ ] 评测体系：
  - 通用知识：MMLU / C-Eval / CMMLU
  - 对话能力：MT-Bench / AlpacaEval
  - 代码：HumanEval / MBPP
  - 业务评测：自建 Golden Set（最重要）
- [ ] 过拟合评测集：训练集/测试集严格隔离

**🔥 面试高频追问**
- Q: LoRA 和 Full Fine-Tuning 效果差距多大？什么情况必须 Full FT？（LoRA 通常达全参 95%+；大规模数据/领域偏移极大/预训练阶段注入新知识时考虑全参）
- Q: QLoRA 的 4bit 量化为什么几乎不损失效果？（NF4 量化 + 双量化 + 分页优化器，量化误差在训练中被 LoRA 吸收）
- Q: SFT 数据量多少合适？（看任务复杂度：格式注入几百条；领域适应 1-5 万条；复杂能力可能 10 万+；关键是数据质量）
- Q: DPO 为什么能跳过 Reward Model？（通过偏好对 (chosen, rejected) 的损失函数直接优化策略，利用 Bradley-Terry 模型隐式表示奖励）
- Q: 微调后模型能力下降（灾难性遗忘）怎么办？（混合 5-10% 通用数据、降低 LR、加 LoRA dropout、EWC 正则化）

---

## P5 · Agent 工程化（约 3 周）🔥 后端优势变现点

> **这是后端工程师的主场**，也是从 Demo 到生产的关键壁垒。前端/算法同学通常在这块薄弱。

### 5.1 可观测性（0.5 周）

**✅ 学完要能说清**

- [ ] LangSmith / Langfuse / Helicone / Phoenix 对比选型
- [ ] Trace 全链路：每次调用的 Prompt/输出/Tool 使用/Latency/Cost/Tokens 全记录
- [ ] 日志规范：结构化日志、TraceID 串联、敏感信息脱敏
- [ ] 指标监控：QPS/Tokens 速率/响应延迟 P99/错误率/成本/Token 缓存命中率
- [ ] 告警：错误率超阈值、成本异常、模型服务延迟飙升、幻觉投诉率

**💻 动手任务**
1. 为 P2 的 Agent 项目接入 Langfuse 自建（开源）或 LangSmith
2. 配置 Grafana 监控面板（Prometheus + FastAPI metrics + Token/Cost 统计）

### 5.2 性能优化与并发（0.5 周）

**✅ 学完要能说清**

- [ ] 异步编程：asyncio + aiohttp + 异步 LLM 调用，并发调用多个工具/LLM
- [ ] 缓存策略：
  - 精确缓存（Prompt+模型参数完全一致）：Redis
  - 语义缓存（Semantic Cache，GPTCache）：相似问题命中缓存
- [ ] Token 优化：Prompt 压缩（LLMLingua）、Token 计数、上下文窗口管理
- [ ] 模型路由（Model Routing）：简单问题用小模型（Qwen2.5-7B）省成本，复杂问题用大模型（GPT-4/Claude）
- [ ] 批处理：Embedding 批量调用、批量评估
- [ ] 推理加速：vLLM（PagedAttention）/ TGI / SGLang 部署模型，吞吐量提升 10-20 倍

### 5.3 部署与运维（1 周）

**✅ 学完要能说清**

- [ ] 模型服务化：
  - 闭源 API：OpenAI/Anthropic SDK + 代理（代理池/负载均衡/失败重试/Fallback）
  - 开源模型本地部署：vLLM / Ollama（开发）/ Xinference / llama.cpp
  - 推理优化：量化（AWQ/GPTQ/GGUF）、Continuous Batching、PagedAttention
- [ ] 服务架构：FastAPI/Gunicorn/Uvicorn 部署、Nginx 反向代理、K8s 部署
- [ ] 流式响应：SSE（Server-Sent Events）/ WebSocket、Token 级流式输出实现
- [ ] 扩缩容：HPA 基于 QPS/GPU 利用率自动扩缩 Pod；模型预热
- [ ] 高可用：多副本、健康检查、熔断降级（Circuit Breaker）、Fallback 到小模型

**💻 动手任务**
1. 用 vLLM 部署 Qwen2.5-7B-Instruct（OpenAI API 兼容），对比 Transformers 推理吞吐量
2. 用 Docker 打包你的 Agent 服务，写 Docker Compose（Agent服务 + Redis + Milvus + Langfuse）
3. 实现流式 SSE 输出（客户端打字机效果）

### 5.4 安全与护栏（0.5 周）

**✅ 学完要能说清**

- [ ] Prompt Injection 防御：
  - 直接注入（用户输入中含忽略指令）：输入层过滤+System Prompt 强化+分隔符隔离
  - 间接注入（外部数据/工具返回中含指令）：工具返回可信标记+独立 LLM 审查
- [ ] Guardrails：输入校验（敏感词/PII 检测/主题限制）、输出校验（幻觉检测/格式校验/有害内容过滤）
- [ ] 工具安全：工具白名单、参数校验、危险操作（删除/支付）需人工审批
- [ ] 数据安全：训练数据脱敏、对话数据加密、知识库权限隔离（多租户）
- [ ] 合规：内容审核（网信办要求）、日志留存、模型备案

### 5.5 多租户与生产功能（0.5 周）

**✅ 学完要能说清**

- [ ] 多租户隔离：用户级速率限制、知识库隔离、会话隔离、API Key 管理
- [ ] 会话管理：Session 持久化、历史消息截断策略（Sliding Window/Summary）
- [ ] 知识库管理：文档上传→切片→向量化的异步流水线、增量更新、文档权限
- [ ] 成本管控：Token 预算、按用户计费、成本监控告警
- [ ] A/B 测试框架：新 Prompt/新模型/新 RAG 策略的线上小流量验证

**🔥 面试高频追问**
- Q: 线上 Agent 服务 P99 延迟很高，怎么排查？（Trace 找瓶颈：是 LLM 推理慢/工具调用慢/检索慢；LLM 慢→换更快模型/流式/缓存；工具慢→并行/异步/超时）
- Q: 怎么控制 Agent 的成本？（模型路由/缓存/压缩Prompt/限制最大步数/Token预算）
- Q: Prompt Injection 怎么防？（分层防御：输入过滤+Prompt结构+外部数据隔离+输出审查+人工审批关键操作，没有银弹）
- Q: 如何处理大模型服务的抖动和限流？（指数退避重试+多 API Key 轮询+Fallback 模型+熔断降级）
- Q: 一个生产级 RAG/Agent 服务，怎么设计架构？（网关层→鉴权限流→Agent 编排层→工具层→模型服务层→向量库/数据库→可观测层）

---

## P6 · 完整项目 + 面试冲刺（约 2 周）

### 推荐综合项目（选 1-2 个做深）

**项目 1：企业知识库问答系统（RAG 主方向）**
- 功能：多格式文档上传（PDF/Word/Markdown）→ 自动切片向量化 → 多轮对话问答 → 引用来源 → 反馈收集
- 技术栈：FastAPI + LangGraph + BGE-M3 + Milvus/Pgvector + BGE Rerank + Qwen/GPT + Langfuse
- 加分项：Hybrid Search + Agentic RAG + 权限控制 + 流式输出 + Docker/K8s 部署
- 面试价值：展示 RAG 全链路能力 + 工程化能力（后端优势）

**项目 2：代码 Agent / 开发助手（Agent 主方向）**
- 功能：代码仓库理解 + 代码生成/修改 + 测试运行 + Git 操作 + 代码解释
- 技术栈：LangGraph + Tree-sitter 代码解析 + Aider/OpenHands 参考 + Docker 沙箱执行
- 加分项：多 Agent（规划者/执行者/审查者）、沙箱安全、长上下文仓库索引
- 面试价值：展示 Agent 设计 + 工程化 + 工具使用能力

**项目 3：垂直领域 Agent（结合个人工作经验最佳）**
- 例如：运维 Agent（接 Prometheus 自动排障）/ 数据分析 Agent（接数据库自然语言查询+图表生成）/ 客服 Agent（接工单系统）
- 关键：体现领域理解 + 业务落地能力，比通用 demo 有说服力 10 倍

### 简历要点

- **量化结果**：不要写"使用 RAG 构建问答系统"，写"基于 BGE-M3+Rerank 构建企业知识库 RAG 系统，Faithfulness 达 0.92，Top-5 Recall 0.87，P99 延迟 <3s，服务 XX 用户"
- **体现深度**：写出你做的优化（如"引入 Parent-Child 检索+Query 改写，将漏检率降低 35%"）
- **后端优势**：强调架构设计、高并发、可观测、部署运维经验（这些是纯算法同学没有的）

### 面试准备清单

**自我介绍模板（3分钟）**
1. 背景：X 年后端经验，做过什么核心系统（量化）
2. 转型：为什么转 AI Agent（动机+已有准备）
3. 能力：LLM 基础/RAG/Agent/微调/工程化 各掌握到什么程度
4. 项目：1-2 个代表项目，突出技术难点和成果
5. 意愿：为什么适合这个岗位

**高频题速查清单**
- LLM 基础：Self-Attention/KV Cache/位置编码/RoPE/GQA/采样策略/Tokenizer
- RAG：全链路/Chunk策略/混合检索/Rerank/幻觉处理/评估指标/Graph RAG
- Agent：ReAct/LangGraph 状态机/多Agent/MCP/工具调用/记忆机制
- 微调：LoRA/QLoRA/SFT/DPO/数据工程/显存优化
- 工程化：流式/异步/缓存/可观测/部署/Prompt Injection防护
- 后端基础：MySQL（索引+事务）/Redis（缓存问题+锁）/MQ（可靠性+幂等）/分布式（CAP/Raft/事务）

**模拟面试建议**
1. 把每个高频题录音回答 3 遍，找朋友或 AI 当面试官
2. 项目要能扛住"为什么这么设计→遇到什么问题→怎么解决→还有什么优化空间"的追问链
3. 准备 2-3 个"我做的最有技术挑战的事"的故事（STAR-R 框架）

---

## 📅 推荐学习节奏（18周计划）

| 周次 | 内容 | 每日投入 |
|------|------|----------|
| W1-W2 | P1.1 Transformer 原理 + nanoGPT 实战 | 2-3h |
| W3 | P1.2 Prompt Engineering 实战 | 2h |
| W4 | P1.3 Python 生态（FastAPI/HF/异步） | 2h |
| W5 | P2.1 LangChain 核心 | 2-3h |
| W6-W7 | P2.2 LangGraph 深度 + 多 Agent | 3h |
| W8 | P3.1 RAG 基础流程 + 手写 RAG | 3h |
| W9-W10 | P3.2 RAG 进阶优化（混合检索/Graph RAG/Agentic RAG） | 3h |
| W11 | P3.3 RAG 评估 + bad case 优化 | 2-3h |
| W12 | P4.1 微调理论（LoRA/QLoRA/SFT/DPO） | 2h |
| W13-W14 | P4.2 微调实操（Llama-Factory 微调 + 消融实验） | 3h |
| W15 | P5 工程化（可观测/性能/部署/安全） | 3h |
| W16-W17 | P6 综合项目开发 | 周末集中 |
| W18 | 简历 + 模拟面试 + 投简历 | 2h |

---

## 🛠️ 推荐工具链速查

| 类别 | 推荐工具 |
|------|----------|
| LLM API | OpenAI GPT-4o / Claude 3.5/4 Sonnet / DeepSeek / Qwen-Max / 豆包 |
| 开源模型 | Qwen2.5 系列 / LLaMA-3.1 / GLM-4 / Mistral / Yi |
| 本地推理 | Ollama（开发）、vLLM（生产）、llama.cpp（边缘） |
| Embedding | BGE-M3（开源首选）、text-embedding-3-small（OpenAI） |
| Rerank | bge-reranker-v2-m3、Cohere Rerank |
| Agent 框架 | LangGraph（⭐首选）、LlamaIndex Agents、CrewAI（快速原型） |
| 向量数据库 | Milvus（生产）、Pgvector（Postgres）、Qdrant、Chroma（开发） |
| 微调框架 | Llama-Factory（入门）、Unsloth（快）、TRL（HuggingFace 官方） |
| 可观测 | Langfuse（⭐开源首选）、LangSmith（官方）、Helicone、Phoenix |
| 评估 | RAGAS、DeepEval、TruLens |
| 部署 | FastAPI + Docker + K8s、BentoML |
| MCP | MCP 官方 SDK、FastMCP |
| UI | Gradio / Streamlit（快速 demo）、Next.js（生产前端） |

---

## 💡 学习心法

1. **项目驱动，不要只看视频**：每学完一个模块立刻动手做东西，"看懂"和"做出来"之间差 10 倍
2. **写学习笔记**：用费曼技巧，学完一个知识点用自己的话写出来，放到本仓库 `docs/notes/`
3. **保持复盘节奏**：每周日用 `./scripts/new-summary.sh weekly` 做一次周复盘
4. **跟进前沿但不焦虑**：AI 领域每周都有新东西，抓主线（RAG/Agent/微调），热点按需了解
5. **后端优势别丢**：你的并发/架构/工程化经验是差异化竞争力，把 AI 组件当成新的"中间件"来掌握
6. **造轮子与用轮子平衡**：学习阶段造轮子（手写 RAG/手写 ReAct）理解原理；工作阶段用成熟框架（LangGraph/Milvus）提效
7. **社区参与**：关注 GitHub Trending、X(Twitter) AI 圈、Paper With Code、加入技术社群

---

## 📚 核心论文清单（建议顺序阅读）

1. [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Transformer 开山之作
2. [GPT-3 Paper](https://arxiv.org/abs/2005.14165) - 规模法则与 Few-shot
3. [InstructGPT / Training language models to follow instructions](https://arxiv.org/abs/2203.02155) - SFT+RLHF 三阶段
4. [LoRA](https://arxiv.org/abs/2106.09685) - 低秩适配
5. [QLoRA](https://arxiv.org/abs/2305.14314) - 4bit 微调
6. [ReAct](https://arxiv.org/abs/2210.03629) - 推理+行动范式
7. [Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401) - RAG 原始论文
8. [DPO](https://arxiv.org/abs/2305.18290) - 直接偏好优化
9. [FlashAttention](https://arxiv.org/abs/2205.14135) - IO 感知注意力
10. [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) - CoT
11. [From Tools to Agents (Survey)](https://arxiv.org/abs/2308.11432) - Agent 综述
12. [Graph RAG (Microsoft)](https://arxiv.org/abs/2404.16130) - 图增强 RAG

---

> 🎯 **最后一句**：后端转 AI Agent 不是"丢掉后端重新学"，而是**把你的工程能力叠加到 LLM 应用开发上**。先做出来（P1-P3），再做深（P4），再做好（P5）。保持节奏，5 个月后你会感谢现在开始的自己。
