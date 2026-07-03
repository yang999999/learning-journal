"""
Day 3: Function Calling —— 让模型学会用工具
目标：理解 Tool Use 机制（Agent 的核心能力）
"""
import json, os, time
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
model = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
console = Console()

# ---------- 1. 定义工具（给模型看的 Schema）----------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的实时天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称，如：北京、上海"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，支持 +-*/ 和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expr": {"type": "string", "description": "数学表达式，如：(3+5)*2"},
                },
                "required": ["expr"],
            },
        },
    },
]

# ---------- 2. 工具实现（本地执行）----------
def get_weather(city: str) -> str:
    """模拟天气 API"""
    fake_data = {
        "北京": "晴，28°C，微风",
        "上海": "多云，26°C，东南风3级",
        "深圳": "雷阵雨，30°C，湿度85%",
    }
    return fake_data.get(city, f"{city}：暂无天气数据（模拟）")

def calculator(expr: str) -> str:
    """安全计算器"""
    allowed = set("0123456789+-*/().e ")
    if not all(c in allowed for c in expr):
        return "错误：表达式包含非法字符"
    try:
        return f"计算结果：{expr} = {eval(expr)}"
    except Exception as e:
        return f"计算错误：{e}"

tool_map = {"get_weather": get_weather, "calculator": calculator}

# ---------- 3. ReAct 循环：思考 → 调用工具 → 观察 → 继续 ----------
def run_agent(user_input: str, max_steps: int = 5):
    messages = [
        {"role": "system", "content": "你是一个智能助手，可以使用工具回答问题。请根据需要调用工具，得到结果后用中文回答用户。"},
        {"role": "user", "content": user_input},
    ]

    for step in range(1, max_steps + 1):
        console.print(Panel(f"Step {step}/{max_steps}", style="bold blue"))

        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0,
        )
        msg = resp.choices[0].message
        messages.append(msg)

        # 如果模型没调工具，说明它直接回答了 → 结束
        if not msg.tool_calls:
            console.print(Panel(msg.content, title="🤖 最终回答", border_style="green"))
            return

        # 模型决定调用工具 → 执行
        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = json.loads(tc.function.arguments)
            console.print(f"🔧 调用工具: [bold]{fn_name}[/bold]({fn_args})")

            # 执行工具
            result = tool_map[fn_name](**fn_args)
            console.print(f"📋 工具返回: {result}\n")

            # 把工具结果加回消息历史
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "name": fn_name,
                "content": result,
            })

    console.print("[yellow]⚠️ 达到最大步数，停止循环[/yellow]")

# ---------- 测试 ----------
if __name__ == "__main__":
    tests = [
        "北京今天天气怎么样？",
        "37乘以43再加128等于多少？",
        "我明天要去上海出差，上海现在天气如何？顺便帮我算一下出差3天，每天预算500元，总共需要多少钱？",
    ]
    for i, q in enumerate(tests, 1):
        console.rule(f"[bold]问题 {i}: {q}[/bold]")
        run_agent(q)
        console.print()

    console.print("[bold green]✅ Day 3 完成！你已经手写了一个 ReAct Agent 循环。[/bold green]")
    console.print("💡 这就是 Agent 的本质：LLM 决策 + 工具执行 + 循环直到回答。LangGraph 就是帮你把这个循环显式管理起来。")
