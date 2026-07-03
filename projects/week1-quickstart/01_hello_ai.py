"""
Day 1: Hello AI World —— 第一次调用大模型 API
目标：成功发送一条消息并打印回复，验证环境配置
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)
model = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")

# ---------- 1. 最简单的调用 ----------
print("=" * 60)
print(f"🤖 使用模型: {model}")
print("=" * 60)

response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "你是一个友好的 AI 助教，回答简洁。"},
        {"role": "user", "content": "用一句话解释什么是大语言模型。"},
    ],
    temperature=0.7,
)
print("回答:", response.choices[0].message.content)
print(f"📊 Token 用量: prompt={response.usage.prompt_tokens}, "
      f"completion={response.usage.completion_tokens}, "
      f"total={response.usage.total_tokens}")

# ---------- 2. 多轮对话 ----------
print("\n" + "=" * 60)
print("💬 多轮对话（带历史）")
print("=" * 60)

messages = [
    {"role": "system", "content": "你是一个 AI 助手。"}
]

# 模拟多轮
questions = [
    "我叫小明，是个后端工程师。",
    "我叫什么名字？我是做什么的？",
]
for q in questions:
    messages.append({"role": "user", "content": q})
    resp = client.chat.completions.create(model=model, messages=messages, temperature=0)
    answer = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    print(f"👤 我: {q}")
    print(f"🤖 AI: {answer}\n")

print("✅ Day 1 完成！你已经成功调用了大模型 API。")
