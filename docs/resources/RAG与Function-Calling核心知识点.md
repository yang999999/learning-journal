---
title: "RAG 与 Function Calling 核心知识点（面试速查）"
date: 2026-07-06
tags: ["RAG", "Function Calling", "Agent", "面试"]
category: "AI核心知识点"
status: active
---

# 📚 RAG 与 Function Calling 核心知识点

> 两个 AI 应用开发最核心的基础能力，面试必问，必须讲清楚原理、痛点、选型。

---

## 一、RAG（检索增强生成）

### 1. RAG 解决什么问题？为什么不直接用 LLM / 不微调？
LLM 本身有三个致命问题，RAG 针对性解决：
| LLM问题 | RAG怎么解决 |
|---------|------------|
| 知识截止（训练数据有日期，不知道最新的事） | 每次检索最新文档喂给LLM |
| 不知道私有数据（你们直播间的秒杀规则、商卡价格LLM没见过） | 私有文档切片存向量库，按需检索 |
| 幻觉（一本正经胡说八道） | 强制基于检索到的资料回答，不知道说不知道 |

**为什么用RAG不用微调？**
- 微调：成本高、要GPU、更新慢（规则变了要重新训）
- RAG：改文档就行，实时更新，成本低，不需要GPU
- 适用场景：RAG适合**知识频繁更新、需要溯源、成本敏感**场景（知识库/客服/营销助手）；微调适合**风格固定、领域术语注入、复杂推理能力提升**场景，两者不冲突可以结合。

### 2. RAG完整链路（必背）
两阶段：

**【离线阶段】（提前做一次）**
```
文档 → 文档解析（PDF/Word/Markdown/表格）
     → 文档切片（Chunking）
     → Embedding模型转向量
     → 存入向量数据库（Milvus/Pgvector/Chroma）
```

**【在线阶段】（用户提问时）**
```
用户提问 → Query改写（指代消解/多Query/HyDE）
       → Query转向量
       → 向量库检索（Top-K）
       → 可选：BM25关键词检索 → RRF融合
       → Rerank精排（Cross-Encoder取Top-N）
       → 拼接Prompt（System + 检索片段 + 用户问题）
       → LLM生成回答（流式SSE）
       → Guardrails校验（防幻觉/敏感词）
       → 返回给用户（带引用来源）
```

### 3. 切片（Chunking）策略
切片大小直接影响效果：
- **太小**：上下文不全，回答断章取义
- **太大**：引入噪声，无关内容占Prompt，稀释相关性，Token浪费
- **常用策略**：
  - 固定长度+Overlap：512token，overlap 50-100token，最简单但可能切断语义
  - 递归字符切片（RecursiveCharacterTextSplitter）：按段落→句子→字符顺序，优先在自然边界切，效果较好
  - 语义切片：按语义相似度断点切，质量最高但计算成本大
  - **父子文档（Parent-Child Retrieval）**：小块（256token）用于检索精度高，命中后返回父块（1024token）给LLM，兼顾精度和上下文完整性，工业界常用
- 特殊处理：代码按AST（函数/类）切；表格转HTML保留行列结构单独处理；按Markdown标题层级切

### 4. Embedding（向量化）
- **作用**：把文本转成高维稠密向量（如1024维），语义相近的文本向量距离近
- **选型**：
  - 中文/多语言：**BGE-M3**（开源最强，支持长文本/多粒度，可本地部署，数据不出域）
  - 英文：OpenAI text-embedding-3-small / Cohere
  - 轻量：bge-small-zh（速度快，适合小规模）
- **相似度计算**：余弦相似度（cosine similarity），归一化后和点积等价，范围[-1,1]，越接近1越相似

### 5. 混合检索 + RRF融合
**为什么要混合？两种检索各有缺陷：**
| 检索方式 | 擅长 | 不擅长 |
|---------|------|--------|
| BM25关键词检索 | 精确匹配ID/数字/专有名词/代码名 | 不懂语义、同义词、口语 |
| 向量语义检索 | 同义表达、口语、语义匹配 | 精确ID/数字匹配差 |

**RRF（Reciprocal Rank Fusion，倒数排名融合）**：
```
每个文档得分 = Σ 1/(k + rank)
k是常数（默认60）
```
只看排名不看原始分数，避开两种算法量纲不同问题，不用调权重，简单稳定效果好。工业界标准做法。

### 5.5 RAG 工程实现细节（切片/Embedding/Milvus 入参出参）

**离线建库流程：文档 → 切片 → Embedding → Milvus**

1. **切片（Chunking）**：用 `RecursiveCharacterTextSplitter`（LangChain）
   - 入参：原始文档字符串
   - 出参：`List[Document]`，每个Document含 `page_content`（切片文本）+ `metadata`（来源/类型/版本）
   - 关键参数：`chunk_size=512`、`chunk_overlap=50`（10%重叠）、`separators` 按段落→换行→句号优先级切
   - metadata 一定要带source文件名，后续检索回答要能标引用来源

2. **Embedding（向量化）**：用 BAAI/bge-m3（中文开源最强）
   - 入参：单条文本字符串（query）或文本列表（批量documents）
   - 出参：`List[float]`（1024维归一化向量）或 `List[List[float]]`（批量）
   - 注意：必须开启 `normalize_embeddings=True`，这样余弦相似度和点积等价

3. **存入Milvus**：
   - 先建Collection（类似表），字段包含：`id`(INT64自增主键)、`vector`(FLOAT_VECTOR dim=1024)、`content`(VARCHAR存原文)、`source`/`doc_type`(metadata标量字段)
   - 向量字段建 `IVF_FLAT` 索引，`metric_type=COSINE`，`nlist=1024`（百万级向量）
   - 入参：批量entities = [向量列表, content列表, source列表, doc_type列表]，批量插入（batch_size=100）
   - ⚠️ **chunk原文必须存在向量库里**（或主键关联到关系库），否则检索出来只有id和相似度，没法给LLM看

**在线检索流程：用户问题 → 向量化 → Milvus搜索 → （Rerank）→ 拼Prompt**

4. **用户问题Embedding**：和离线完全一样的模型，`embedding_model.embed_query(user_query)` → 1024维向量
5. **Milvus搜索**（`collection.search`）：
   - 入参：
     - `data=[query_vector]`：query向量列表
     - `anns_field="vector"`：向量字段名
     - `param={"metric_type":"COSINE","params":{"nprobe":32}}`：nprobe越大越准越慢
     - `limit=20`：粗排返回Top20
     - `output_fields=["content","source"]`：**必须带content字段**，否则只有id没用
     - `expr="doc_type=='seckill'"`：可选标量过滤（类似WHERE）
   - 出参：`List[Hit]`，每个Hit有 `hit.score`（相似度）、`hit.entity.get('content')`（原文）、`hit.entity.get('source')`（来源）、`hit.id`（主键）
6. **Rerank（可选）**：bge-reranker-v2-m3对(Query, Chunk)对打分，重排序后取Top3-5
7. **拼Prompt**：把Top3的[source+content]拼成上下文，塞进System Prompt给大模型生成回答

**关键参数经验值**：
| 参数 | 推荐值 | 说明 |
|---|---|---|
| chunk_size | 512token | 问答场景；摘要可1024 |
| chunk_overlap | 10%（50token） | 避免在关键信息中间切断 |
| nlist | 1024（百万级） | 经验公式：4*sqrt(总向量数) |
| nprobe | 32 | 精度vs速度平衡，越大越准越慢 |
| 粗排Top-K | 20 | 召回要宽一点 |
| 精排Top-N | 3-5 | 给LLM的上下文不要太多防"Lost in the Middle" |
| metric_type | COSINE | 归一化后等价于IP，语义相似度直观 |

### 6. Rerank（精排）
- **为什么需要Rerank？** 向量/BM25召回Top20是粗排（快），但粗排分数不准确，需要用更精准的模型重新排序，取Top3-5给LLM，减少噪声提升准确率
- **Bi-Encoder vs Cross-Encoder**：
  - Bi-Encoder（双编码器）：Query和Document分别编码→算余弦，速度快，适合粗排（Embedding模型就是这个）
  - Cross-Encoder（交叉编码器）：Query和Document拼在一起过Transformer，Cross-Attention有充分交互，精度高但慢（N次推理），适合精排
- **常用模型**：bge-reranker-v2-m3（开源中文最好），Cohere Rerank

### 7. Query层优化
检索好不好一半在Query：
- **Query Rewrite**：多轮对话指代消解，"它是什么"→"RAG是什么"
- **Multi-Query**：LLM生成3-5个不同角度的Query并行检索，提升召回
- **HyDE（Hypothetical Document Embeddings）**：先让LLM生成一个"假设答案"，用假设答案去检索（假设答案和真实文档语义更接近），提升召回
- **Step-Back Prompting**：先把具体问题抽象到更高层面（"秒杀优惠怎么用"→"电商优惠使用规则"），检索抽象问题，提升通用规则的召回
- **Query路由**：简单FAQ走缓存，实时数据走Tool，规则问题走RAG

### 8. 幻觉治理（核心考点，电商场景价格零幻觉）
**三层防御：**
1. **Prompt层**：强约束"只根据提供的上下文回答，没有依据就回答不知道，禁止编造数字"；要求回答标注引用来源`[来源：文档名#章节]`
2. **工具层**：实时数据（价格/库存/资格/金额）**必须走Function Calling**，不允许RAG/LLM直接回答，工具超时返回兜底
3. **校验层（Guardrails）**：
   - 正则/规则校验答案中的数字是否在工具返回范围内
   - LLM-as-Judge：生成完再用一个LLM校验"每句话是否能在上下文中找到依据"（Faithfulness校验）
   - 用户反馈闭环：👍👎按钮收集bad case，迭代优化
4. **兜底**：不确定时直接说"我查一下稍后回复"或转人工，不硬编

### 9. RAG评估指标
- **检索层**：Recall@K（正确文档是否被召回，最重要）、MRR、NDCG
- **生成层**：
  - Faithfulness（忠实度）：回答是否忠于上下文，反幻觉核心指标
  - Answer Relevancy：答案是否回答了问题
  - Context Precision/Recall：上下文是否相关且充分
- **工具**：RAGAS（自动化评估）、TruLens、人工标注Golden Set
- **线上**：转人工率、用户满意度、bad case分类统计

---

## 二、Function Calling（工具调用）

### 1. 本质是什么？
> **LLM不执行任何工具！它只是按你给的格式，生成一段"要调哪个工具、参数是什么"的JSON文本，真正执行工具的是你写的代码。**

```
用户: "这件秒杀多少钱？"
   ↓
LLM（根据你给的工具描述）决定调用 get_sku_price
   ↓ 生成JSON（不是执行！）
{"name":"get_sku_price", "arguments":{"sku_id":123, "live_room_id":456}}
   ↓
你的Python代码解析JSON，调用真实的商卡价格服务，拿到结果9.9元
   ↓ 把结果塞回消息历史
[{"role":"tool","name":"get_sku_price","content":"{"price":9.9,"original":99,"stock":5}"}]
   ↓
LLM看到结果，生成自然语言回答："这件秒杀价9.9元（原价99元1折），库存剩5件"
```

### 2. 怎么定义工具？
工具定义是一段JSON Schema告诉LLM：
- 工具叫什么（name）
- 工具干嘛用（description，写清楚什么时候用，LLM靠这个判断要不要调）
- 参数有哪些、类型、是否必填、每个参数的含义

```json
{
  "type": "function",
  "function": {
    "name": "get_sku_price",
    "description": "查询直播间商品的实时价格和库存，用户问价格/有没有货/多少钱时必须调用",
    "parameters": {
      "type": "object",
      "properties": {
        "sku_id": {"type": "integer", "description": "商品ID"},
        "live_room_id": {"type": "integer", "description": "直播间ID"}
      },
      "required": ["sku_id", "live_room_id"]
    }
  }
}
```
**关键：description写得好不好决定工具调用准确率**，必须写清楚"什么时候用"。

### 3. Function Calling 完整流程（ReAct循环）
这就是Agent的本质循环：
```
while 没结束:
    1. LLM看对话历史 + 工具列表
    2. 如果要调工具 → 生成工具调用JSON → 代码执行 → 结果加回消息历史 → 回到第1步
    3. 如果不需要调工具 → 生成最终回答 → 结束循环
```
对应到代码里就是while循环，直到LLM返回最终回答不调工具为止。

### 4. 关键设计要点（面试会问）
1. **工具粒度合适**：一个工具干一件事，不要一个万能工具传一堆参数（LLM容易填错）
2. **工具返回结构化**：返回JSON/结构化文本，别返回一坨无格式大文本，LLM好处理
3. **强制调用**：价格/库存等敏感场景，Prompt里明确"必须调用工具，不能自己猜测"
4. **错误处理**：工具报错/超时返回明确错误信息给LLM，让它决定重试还是告诉用户
5. **并行调用**：多个互不依赖的工具OpenAI/多数模型支持并行调用（一次JSON返回多个工具调用），减少轮次降延迟

   **完整并行调用需要三层配合，少一层都不行**：
   - **模型层**：用支持并行调用的模型（GPT-4o/GPT-3.5-turbo-1106+/Gemini 1.5/Qwen2.5+），老模型一次只能返回一个tool_call
   - **Prompt层**：System Prompt里必须明确引导："多个互不依赖的工具调用，请一次性返回，无需逐个串行等待"。否则模型可能保守选串行，白瞎了模型能力
   - **代码层**：拿到工具调用列表后，必须**用asyncio.gather/线程池并行执行**，不能for循环串行逐个await。LangGraph默认ToolNode已经支持并行，不用自己写。

   **常见坑**：模型返回了多个tool_call，但代码串行执行，总延迟还是两个工具相加，根本没起到加速作用。

6. **安全控制**：
   - 工具白名单，只暴露必要接口
   - 危险操作（下单/删除/支付）必须HITL（Human-in-the-loop）人工审批
   - 参数校验（用户输入的ID必须是数字，范围合法）

### 5. Function Calling vs RAG vs 微调 对比
| 方案 | 适用场景 | 实时性 | 成本 |
|------|---------|--------|------|
| 直接LLM回答 | 通用聊天、创意写作 | 无 | 低 |
| RAG | 静态知识问答、规则/文档/FAQ | 分钟级（文档更新即生效） | 中 |
| Function Calling | 实时数据、操作外部系统（查价格、下单、发消息）| 毫秒级（实时）| 中 |
| 微调 | 风格固化、领域术语、复杂推理格式 | 慢（需重训）| 高 |

工业级Agent三个都用：RAG管知识，Tool管实时数据/操作，微调管说话风格和能力。

---

## 三、常考追问总结

**Q1：RAG为什么能减少幻觉？**
> RAG把真实资料塞进上下文，LLM是"开卷考试"，Prompt约束只能按资料回答；加上引用来源和输出校验，幻觉率大幅下降但不可能100%消除。

**Q2：为什么不把所有文档都塞进Prompt？**
> ①Token限制（GPT-4o 128K≈10万字，企业知识库动辄千万字塞不下）；②注意力稀释（Lost in the Middle问题，上下文太长LLM会忽略中间内容）；③成本（Token按输入量计费，全塞非常贵）；检索是为了"找到最相关的几段"，节省Token提升准确率。

**Q3：向量库怎么选？**
> - 开发/小规模：Chroma/FAISS（本地零依赖）
> - 生产中小规模：**Pgvector**（复用PostgreSQL，运维简单）
> - 生产大规模（亿级向量）：Milvus/Qdrant（分布式、水平扩展、GPU加速）
> 我们直播场景文档万级，Pgvector足够，运维成本低。

**Q4：Chunk Size怎么选？**
> 没有标准答案，要实验：通常256-1024token，overlap 10-20%；问答场景小一点（256-512），摘要场景大一点（1024）；父子文档策略避免选择困难。看Recall@K指标调整。

**Q5：Function Calling和MCP什么关系？**
> Function Calling是LLM的**能力**（生成工具调用JSON）；MCP是**工具接入协议**（怎么定义工具、怎么连接工具Server的标准）。MCP Server对外暴露Tools/Resources/Prompts，LLM通过Function Calling去调用MCP提供的工具。两者不是一层东西，不能互相替代：
> - Function Calling = 手机"能打电话"的能力（模型本身的API特性）
> - MCP = USB-C接口标准（所有手机/所有Agent都能用统一方式接工具）
> - 类比：Function Calling是"嘴"（会说话表达要做什么），MCP是"手的接口标准"（用标准方式操作外部工具）

**Q5.1：什么场景用MCP，什么场景直接注册工具？**
> - 工具少（3-5个）、只给自己的Agent用：直接@tool装饰器注册（项目A的做法），10行代码搞定，MCP是过度设计
> - 工具多、来自不同系统（Prometheus/Loki/Jaeger/CMDB）、要给多个Agent/多个客户端复用：用MCP，每个系统封装一个MCP Server，Agent零代码接入，长期受益（项目B的做法）
> - 选型核心：看工具有没有跨系统/跨Agent复用需求。N个工具 × M个客户端 = N×M份适配代码，MCP把它降为N+M。

**Q5.2：MCP是下游Server实现还是模型tools层实现？**
> MCP是Client-Server协议，两边都有角色：
> - **MCP Server（下游系统方实现）**：把自己系统的能力封装成标准工具，对外提供list_tools/call_tool接口，真正执行业务逻辑（比如Prometheus MCP Server、Loki MCP Server）
> - **MCP Client（Agent平台实现）**：①启动时连接所有MCP Server，调用list_tools()拉取工具列表，自动转换成OpenAI Function Calling格式；②模型输出tool_call后，根据工具名路由到对应MCP Server，用call_tool()发请求执行；③拿到结果塞回messages继续循环
> - **大模型本身**：完全不知道MCP存在！模型看到的永远是统一的OpenAI格式tools数组，输出格式也永远一致。MCP Client负责"翻译"和"路由"，对模型完全透明。
>
> 类比：MCP = USB-C，MCP Server = USB-C设备（U盘/显示器），MCP Client = 电脑上的USB-C控制器，大模型 = 使用设备的软件（Word只认磁盘，不知道USB-C是什么协议）。

**Q5.3：下游实现MCP后，上游还要注册tools给模型吗？**
> 必须传tools给模型（模型不知道有哪些工具就没法调用），但**不用手写JSON Schema了**。
>
> 流程是：
> 1. Agent启动时读配置文件，连接所有MCP Server地址
> 2. 对每个Server调用list_tools()拿到工具列表
> 3. Client自动转换成OpenAI格式，合并本地@tool和所有MCP工具，缓存为统一的openai_tools数组
> 4. 每次调用大模型都带着这个tools数组（和本地工具完全一样）
> 5. 模型输出tool_call后，Client根据工具名路由：本地工具→直接调用Python函数；MCP工具→通过call_tool()发JSON-RPC请求给对应Server执行
>
> 新增一个工具？不用改Agent代码，只需要在配置里加一行MCP Server地址，启动时自动发现。工具维护责任从Agent开发者转移到工具所有者（下游团队）。
>
> ```
> # 不用MCP：每个工具都要手写函数+装饰器，新工具改Agent代码
> @tool
> def query_metrics(query: str): ...
>
> # 用MCP：只配地址，自动发现工具
> mcp_servers:
>   - http://prometheus-mcp:8000
>   - http://loki-mcp:8000
> ```

**Q5.4：Skill和给模型注册工具是一个东西吗？**
> 完全不是：
> - 注册工具（Function Calling/MCP Tools）：是给**大模型**看的，告诉LLM"你能调用哪些外部功能"，每次调用模型API时作为tools参数传入
> - Skill（Codex Skill）：是给**Agent助手本身**看的行为规范（SKILL.md），告诉AI助手"你回复用户时要遵守什么规则"（比如"任务被打断必须报告""长输出要截断"），在框架层加载，不传给大模型
>
> 简单说：工具是给模型"用"的（扩展能力边界），Skill是给助手"守规矩"的（约束自身行为）。

**Q6：如果LLM生成了错误的工具参数怎么办？**
> ①参数校验（Pydantic/Schema校验失败直接返回错误给LLM，让它重生成）；②工具描述更清晰，加例子（Few-shot）；③最多重试3次还错就兜底转人工。
