# MCP 完整调用流程 Demo

展示从大模型输出 → 识别MCP工具 → MCP Client调用 → 结果喂回模型的完整代码级流程。

## 包含两个文件
1. `mock_prometheus_server.py` —— 模拟一个MCP Server（Prometheus指标查询服务）
2. `mcp_client_demo.py` —— MCP Client + OpenAI大模型，完整端到端流程

## 运行
```bash
pip install mcp openai
python mock_prometheus_server.py  # 先启动MCP Server
python mcp_client_demo.py          # 另开终端运行Client
```

## 核心流程
```
用户问题 → 传给大模型（带上MCP工具列表）
   ↓
大模型输出 tool_call：{name: "query_metrics", arguments: {query: "订单接口P99延迟"}}
   ↓
Client识别这个工具是MCP工具 → 通过MCP协议（stdio/SSE）调用远程MCP Server
   ↓
MCP Server执行真实查询，返回结果
   ↓
Client拿到结果，塞回消息历史
   ↓
再传给大模型，大模型基于结果生成自然语言回答
```
