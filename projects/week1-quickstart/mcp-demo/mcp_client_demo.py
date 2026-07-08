"""
完整的 MCP Client + 大模型 调用流程Demo
演示从模型输出tool_call → 识别是MCP工具 → 调用MCP Server → 结果喂回模型
"""
import asyncio
import json
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

client = AsyncOpenAI()  # 需要设置OPENAI_API_KEY环境变量

async def run():
    # ==========================================
    # 第一步：连接MCP Server，获取工具列表
    # ==========================================
    server_params = StdioServerParameters(
        command="python",
        args=["mock_prometheus_server.py"],  # 启动子进程
    )
    
    print("=" * 60)
    print("🔌 连接 MCP Server (Prometheus)...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 获取MCP Server提供的所有工具
            mcp_tools = await session.list_tools()
            
            print(f"✅ MCP Server 提供了 {len(mcp_tools.tools)} 个工具：")
            for t in mcp_tools.tools:
                print(f"  - {t.name}: {t.description[:80]}...")
            
            # ==========================================
            # 第二步：把MCP工具转成OpenAI Function Calling格式
            # ==========================================
            # 这一步就是关键！模型看到的tools数组和本地注册工具一模一样
            # 模型根本不知道这工具背后是本地函数还是MCP Server
            
            openai_tools = []
            for tool in mcp_tools.tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            "type": "object",
                            "properties": {
                                p: {"type": "string"} for p in tool.inputSchema.get("properties", {}).keys()
                            },
                            "required": tool.inputSchema.get("required", []),
                        }
                    }
                })
            
            print(f"\n📋 转化后的OpenAI tools格式（共{len(openai_tools)}个工具）：")
            print(json.dumps(openai_tools, ensure_ascii=False, indent=2)[:500] + "...")
            
            # ==========================================
            # 第三步：构建对话，调用大模型
            # ==========================================
            user_query = "订单接口的P99延迟现在是多少？"
            messages = [
                {"role": "system", "content": "你是运维助手，查询指标必须调用query_metrics工具。"},
                {"role": "user", "content": user_query}
            ]
            
            print(f"\n💬 用户提问：{user_query}")
            print("🤖 第一次调用大模型，等待决策...")
            
            # 调用大模型——ReAct循环
            while True:
                response = await client.chat.completions.create(
                    model="gpt-4o-mini",  # 用mini便宜，演示用
                    messages=messages,
                    tools=openai_tools,
                    tool_choice="auto",
                )
                
                msg = response.choices[0].message
                
                # 模型没有要调工具 → 直接出最终回答
                if not msg.tool_calls:
                    print(f"\n✅ 模型最终回答：{msg.content}")
                    break
                
                # 模型要调工具 → 执行（通过MCP协议）
                print(f"\n🔧 模型决定调用 {len(msg.tool_calls)} 个工具:")
                for tc in msg.tool_calls:
                    print(f"  → 工具名: {tc.function.name}")
                    print(f"  → 参数: {tc.function.arguments}")
                
                # 把模型的tool_call消息加回历史（OpenAI要求）
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                        } for tc in msg.tool_calls
                    ]
                })
                
                # ==========================================
                # 第四步：通过MCP协议调用工具（关键！）
                # ==========================================
                for tc in msg.tool_calls:
                    tool_name = tc.function.name
                    tool_args = json.loads(tc.function.arguments)
                    
                    print(f"\n🌐 【MCP协议调用】调用 {tool_name}, 参数={tool_args}")
                    
                    # ★ 这一行就是MCP的核心：通过MCP协议发送调用请求
                    # 底层是JSON-RPC 2.0 消息通过stdio/SSE传输
                    # Server收到请求，执行真实逻辑，返回结果
                    result = await session.call_tool(tool_name, tool_args)
                    
                    # 提取返回文本
                    result_text = result.content[0].text
                    print(f"📥 MCP Server 返回结果：{result_text}")
                    
                    # 把工具结果加回消息历史，喂回给模型
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result_text,
                    })
                
                # 循环回去，让模型看结果继续决策（可能再调工具，可能出回答）
                print("\n🔄 工具结果已返回，继续让大模型决策...\n")
                print("-" * 40)

if __name__ == "__main__":
    asyncio.run(run())
