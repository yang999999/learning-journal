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
> Function Calling是LLM的**能力**（生成工具调用JSON）；MCP是**工具协议**（怎么定义工具、怎么连接工具Server的标准）。MCP Server对外暴露Tools/Resources/Prompts，LLM通过Function Calling去调用MCP提供的工具。

**Q6：如果LLM生成了错误的工具参数怎么办？**
> ①参数校验（Pydantic/Schema校验失败直接返回错误给LLM，让它重生成）；②工具描述更清晰，加例子（Few-shot）；③最多重试3次还错就兜底转人工。
