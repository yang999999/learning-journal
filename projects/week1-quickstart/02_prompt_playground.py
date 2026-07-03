"""
Day 2: Prompt 实验室 —— 对比 Zero-shot / Few-shot / CoT 的效果
目标：直观感受 Prompt 技巧对回答质量的影响
"""
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
import os, json, time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
model = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
console = Console()

def ask(system: str, user: str, label: str) -> str:
    t0 = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0,
    )
    elapsed = time.time() - t0
    answer = resp.choices[0].message.content
    tokens = resp.usage.total_tokens
    console.rule(f"[bold cyan]{label}[/bold cyan]  ⏱ {elapsed:.1f}s  🪙 {tokens} tokens")
    console.print(answer)
    console.print()
    return answer

# 测试问题：一个需要推理的数学/逻辑题
QUESTION = "一个笼子里有鸡和兔，头一共 35 个，脚一共 94 只。请问鸡和兔各多少只？"

console.print(f"[bold yellow]📝 测试问题：{QUESTION}[/bold yellow]\n")

# 1. Zero-shot（直接问）
ask("你是一个数学老师，直接给出答案。",
    QUESTION,
    "Zero-shot（直接问）")

# 2. Zero-shot CoT（加一句"请一步步思考"）
ask("你是一个数学老师，请一步步思考后给出答案。",
    QUESTION,
    "Zero-shot CoT（加'一步步思考'）")

# 3. Few-shot CoT（给一个示例，再问）
FEW_SHOT = """请按示例格式，一步步推理后回答。

示例：
Q: 鸡兔同笼，头共10个，脚共28只，鸡兔各几只？
A: 让我一步步思考。
- 假设全是鸡，则脚有 10×2=20 只
- 实际脚 28 只，多出 8 只
- 每只兔比鸡多 2 只脚，所以兔 = 8/2 = 4 只
- 鸡 = 10-4 = 6 只
答案：鸡6只，兔4只。

现在请回答：
"""
ask("你是一个数学老师。",
    FEW_SHOT + QUESTION,
    "Few-shot CoT（给一个示例）")

console.print("[bold green]✅ Day 2 完成！观察三种 Prompt 方式的回答质量差异。[/bold green]")
console.print("💡 思考：哪种方式最准确？为什么？（提示：引导模型生成中间推理步骤 = CoT 核心思想）")
