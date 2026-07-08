"""
模拟一个Prometheus指标查询的MCP Server
启动后监听stdio（MCP协议），提供一个query_metrics工具
"""
import sys
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pydantic import BaseModel

# 模拟Prometheus返回的一些数据
MOCK_METRICS = {
    "order_api_p99": 123,  # 毫秒
    "order_api_qps": 3200,
    "live_api_p99": 89,
    "live_api_qps": 5000,
}

class MetricsQueryRequest(BaseModel):
    query: str
    time_range: str = "last_1h"

app = Server("prometheus-mcp-server")

@app.tool()
def query_metrics(query: str, time_range: str = "last_1h") -> dict:
    """查询Prometheus指标，支持:
    - order_api_p99: 订单接口P99延迟
    - order_api_qps: 订单接口QPS
    - live_api_p99: 直播间API P99延迟
    - live_api_qps: 直播间API QPS
    """
    key = query.strip().lower().replace(" ", "_")
    # 简单模糊匹配
    for k, v in MOCK_METRICS.items():
        if key in k:
            return {
                "query": query,
                "time_range": time_range,
                "result": v,
                "unit": "ms" if "p99" in k else "qps",
                "success": True
            }
    return {
        "query": query,
        "time_range": time_range,
        "error": "no metric matched",
        "success": False
    }

async def main():
    async with stdio_server():
        await app.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
