"""
Day 4: 流式对话 CLI —— 打字机效果的聊天机器人
目标：掌握 SSE 流式输出 + 多轮记忆 + 用户交互
"""
import os
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
model = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
console = Console()

def streaming_chat():
    messages = [
        {"role": "system", "content": "你是一个友好的AI助手，回答简洁有帮助。使用中文回答。"},
    ]

    console.print("[bold cyan]🤖 流式对话机器人已启动（输入 exit/quit 退出）[/bold cyan]\n")

    while True:
        user_input = console.input("[bold blue]👤 你:[/bold blue] ")
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            console.print("[bold]👋 再见！[/bold]")
            break

        messages.append({"role": "user", "content": user_input})
        console.print("[bold green]🤖 AI:[/bold green] ", end="")

        # 流式调用
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=0.7,
        )

        full_response = []
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                full_response.append(text)
                console.print(text, end="", markup=False)

        console.print("\n")  # 换行
        messages.append({"role": "assistant", "content": "".join(full_response)})
        console.print(f"[dim]💬 当前已对话 {len([m for m in messages if m['role']=='user'])} 轮[/dim]\n")

if __name__ == "__main__":
    streaming_chat()
