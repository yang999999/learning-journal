"""
Day 5-7: 手写迷你 RAG（不依赖 LangChain，理解原理）
目标：完整实现文档加载→切片→Embedding→向量检索→生成回答

需要先安装: uv pip install faiss-cpu sentence-transformers
（如果装不了 sentence-transformers，会自动回退到 OpenAI Embedding API）
"""
import os, json, math
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
chat_model = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
console = Console()

# ========== 1. 准备知识库（几篇小文档）==========
DOCUMENTS = [
    {
        "title": "什么是 RAG",
        "content": "RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合"
                   "信息检索和大语言模型生成的技术框架。它的核心思想是：在回答用户问题前，"
                   "先从外部知识库中检索相关文档，再把文档内容作为上下文喂给大模型，让模型"
                   "基于检索到的真实内容生成回答，从而减少幻觉、让模型具备访问私有/最新知识的能力。"
    },
    {
        "title": "RAG 的三个核心步骤",
        "content": "RAG 主要分三步：1) 索引阶段：将文档切片后用 Embedding 模型转成向量存入向量数据库；"
                   "2) 检索阶段：用户提问时，将问题也转成向量，在向量库中通过余弦相似度找最相关的 Top-K 片段；"
                   "3) 生成阶段：将检索到的片段拼接到 Prompt 中，让大模型基于这些上下文生成回答。"
    },
    {
        "title": "Chunk 策略",
        "content": "文档切片（Chunking）是 RAG 效果的关键环节。常见策略包括："
                   "固定长度切片（如每512个token，重叠50个token，实现简单但可能切断语义）；"
                   "递归切片（按段落→句子→字符顺序优先在自然边界切，效果较好）；"
                   "语义切片（按语义相似度断点切，质量最高但计算成本大）；"
                   "父子文档（小块检索、大块返回，兼顾检索精度和上下文完整性）。"
                   "切片太小会丢失上下文，太大会引入噪声、稀释相关性，通常256-1024 tokens 需要根据场景实验。"
    },
    {
        "title": "向量嵌入 Embedding",
        "content": "Embedding 模型把文本转换成高维稠密向量（如768维或1024维），"
                   "语义相近的文本在向量空间中距离更近。常用开源模型包括 BGE-M3（多语言、多任务）、"
                   "M3E（中文优秀）、bce-embedding；闭源如 OpenAI text-embedding-3-small。"
                   "衡量两个向量相似度的方法主要是余弦相似度（cosine similarity），"
                   "值越接近1表示越相似。"
    },
    {
        "title": "混合检索与 Rerank",
        "content": "单纯向量检索容易漏掉关键词精确匹配的内容，工业级 RAG 通常使用混合检索："
                   "把向量检索（稠密，擅长语义匹配）和 BM25 关键词检索（稀疏，擅长精确词匹配）结合，"
                   "用 RRF（Reciprocal Rank Fusion）算法融合两路排序结果。"
                   "多路召回后通常还要经过 Rerank 模型（如 bge-reranker）进行精排，"
                   "Cross-Encoder 类 Rerank 会把 query 和 document 拼在一起重新计算相关度，"
                   "虽然慢但精度高，能显著提升最终回答质量。"
    },
    {
        "title": "RAG 幻觉问题",
        "content": "RAG 虽然能大幅减少幻觉，但不能完全消除。常见策略："
                   "1) Prompt 中明确指示只能依据上下文回答，不能编造；"
                   "2) 要求模型在答案中引用来源段落；"
                   "3) 生成后用 Faithfulness 指标或 LLM-as-Judge 做事实校验；"
                   "4) 对检索结果做相关性过滤，不相关的上下文不给模型；"
                   "5) 超出知识范围的问题显式回答'不知道'。"
    },
]

# ========== 2. 切片：这里简化为按文档标题对应的内容整体作为一个 chunk ==========
def chunk_documents(docs, chunk_size=200, overlap=30):
    """简化版切片：按字符长度切（生产环境用 token 级切片+递归）"""
    chunks = []
    for doc in docs:
        text = f"【{doc['title']}】{doc['content']}"
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append({"text": text[start:end], "source": doc["title"]})
            if end == len(text):
                break
            start = end - overlap
    return chunks

# ========== 3. Embedding ==========
# 优先使用 OpenAI Embedding API（无需本地模型，开箱即用）
def get_embeddings(texts: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(
        model="text-embedding-3-small",  # 或你用的服务商的 embedding 模型
        input=texts,
    )
    return [item.embedding for item in resp.data]

# ========== 4. 简易向量存储（用 numpy 做余弦相似度，无需 FAISS）==========
def cosine_sim(a: list[float], b: list[float]) -> float:
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    return dot / (na * nb + 1e-10)

class SimpleVectorStore:
    def __init__(self):
        self.chunks: list[dict] = []
        self.vectors: list[list[float]] = []

    def add(self, chunks, vectors):
        self.chunks.extend(chunks)
        self.vectors.extend(vectors)

    def search(self, query_vector, top_k=3) -> list[tuple[dict, float]]:
        scored = [(c, cosine_sim(query_vector, v)) for c, v in zip(self.chunks, self.vectors)]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

# ========== 5. RAG 主流程 ==========
def build_index():
    console.print("[bold]📚 正在构建索引（切片 + Embedding）...[/bold]")
    chunks = chunk_documents(DOCUMENTS)
    console.print(f"   共切成 {len(chunks)} 个片段")
    vectors = get_embeddings([c["text"] for c in chunks])
    store = SimpleVectorStore()
    store.add(chunks, vectors)
    console.print("[green]✅ 索引构建完成[/green]\n")
    return store

def rag_qa(store: SimpleVectorStore, query: str, top_k: int = 3):
    # 检索
    q_vec = get_embeddings([query])[0]
    results = store.search(q_vec, top_k=top_k)

    console.print(Panel(f"🔍 检索到 Top {top_k} 相关片段:", style="cyan"))
    context_parts = []
    for i, (c, score) in enumerate(results, 1):
        context_parts.append(f"[片段{i}](来源:{c['source']}, 相关度:{score:.3f})\n{c['text']}")
        console.print(f"  [dim]#{i} score={score:.3f} | {c['source']} | {c['text'][:60]}...[/dim]")
    context = "\n\n".join(context_parts)

    # 生成
    prompt = f"""请基于以下检索到的资料回答用户的问题。
要求：
1. 只根据提供的资料回答，不要编造资料外的内容；
2. 如果资料中没有答案，请明确说"根据现有资料无法回答"；
3. 回答简洁清晰，分点作答。

【检索资料】
{context}

【用户问题】
{query}"""

    console.print("\n[bold]🤖 正在生成回答...[/bold]\n")
    stream = client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": "你是一个严谨的知识库问答助手。"},
            {"role": "user", "content": prompt},
        ],
        stream=True,
        temperature=0.3,
    )
    answer = []
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            t = chunk.choices[0].delta.content
            answer.append(t)
            console.print(t, end="", markup=False)
    console.print("\n")
    return "".join(answer)

# ========== 主入口 ==========
if __name__ == "__main__":
    store = build_index()

    console.print("[bold yellow]💡 迷你 RAG 问答（输入 exit 退出）[/bold yellow]")
    console.print("示例问题：什么是RAG？/ Chunk大小怎么选？/ 怎么减少幻觉？\n")

    while True:
        q = console.input("[bold blue]❓ 你的问题:[/bold blue] ")
        if q.lower() in ("exit", "quit", "q"):
            break
        if q.strip():
            rag_qa(store, q)
            console.print("─" * 60)

    console.print("[green]✅ Week1 完成！你已经手写了完整的 RAG 系统 🎉[/green]")
    console.print("[dim]下一步：对比有 RAG 和无 RAG（直接问模型）的回答差异[/dim]")
