---
title: "项目B：AI 直播电商 OnCall 助手（智能监控告警根因定位）"
date: 2026-07-05
tags: ["项目", "Agent", "直播电商", "OnCall", "简历", "面试"]
category: "简历项目"
status: planned
---

# 📺 项目 B：AI 直播电商 OnCall 助手（智能监控告警根因定位）

> **定位**：贴合你做的直播电商 C 端业务流量承接 + 告警监控 / 故障排查，天然对口；覆盖 Agent + 工具调用 + HITL 所有考点。
> **可信度**：⭐⭐⭐⭐⭐（每个运维/开发每天都在做，真实度拉满）
> **技术含金量**：⭐⭐⭐⭐⭐（多 Agent + 工具 + MCP + HITL + 安全，覆盖所有 Agent 面试考点）

---

## 📋 一、项目背景（面试30秒开场）

> "我们直播电商业务，大促/秒杀期间告警多，资深 SRE 不够用，新人处理告警慢、错判根因经常延误故障。我引入 AI 做了 OnCall 助手，能自动整合 Prometheus 指标+日志+链路+CMDB，自然语言查询分析根因，新人能快速定位，故障定位平均 MTTR 从 25 分钟降到 8 分钟，减少了大促期间大面积故障。"

**关键数字（根据你的实际改，合理就行）**：
- 覆盖业务：X 场直播（日常+大促），日均 X 次告警定位
- MTTR（平均故障定位时间）：从 25min → 8min
- 大促峰值告警准确率：82%
- 减少人工介入率：减少 40%

---

## 🏛️ 二、系统架构

```
┌───────────────────────────────────────────────────────────────────────┐
│                        用户（SRE / 运营 / 开发）                            │
│                              │
│                              提问自然语言                            │
│                              │ SSE
                              ↓
┌──────────────────────────────────────────────────────────────────────┐
│  API网关层                                                         │
│  ├─ 权限校验 / 限流 / trace透传                                          │
│  └─ 意图识别（Supervisor Agent）                                      │
│         → 分类：通用查询？根因定位？变更查询？                             │
│               ↓
│  通用查询  →  知识库查询（RAG 历史案例 + 当前告警匹配）
│  根因定位  →  多 Worker Agent 并行查指标/日志/变更/CMDB                        │
│                                   ↓
│  结果汇总  →  报告 Agent 生成最终报告                              │
│                                        ↓
│  高危操作 → 人工审批（HITL）                                      │
│                                        ↓
│  执行  →  MCP 工具调用 →  执行命令 →  结果返回                                              │
│                                        ↓
│  持久化  →  Checkpointer 存 State →  全链路 Trace                                        │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 三、核心技术亮点（都是面试可讲的深度）

### 亮点 1：Supervisor-Multiple Worker 架构（LangGraph）

**为什么这么分？**
- Supervisor 负责意图识别+路由+结果汇总，每个具体任务分给专门 Worker Agent，职责清晰，好调试好扩展
- 不同 Worker 可以并行拉数据（指标 + 日志 + 变更 + CMDB），比单 Agent 快
- LangGraph Checkpointer 支持断点续做+人工干预，高危操作必须审批

### 亮点 2：MCP 多工具统一接入

我们业务已经有 Prometheus、Loki、Jaeger、CMDB 都是不同系统，传统集成每个都要改代码适配 Agent；现在我用 MCP 协议把每个系统封装成独立 MCP Server，Agent 框架不用动就能用，新增工具只需要加一个 MCP Server，解耦清晰。

**MCP 协议理解：** 给面试官讲明白"标准化工具接入，降低集成成本，开放生态"就行（之前已经讲过了，这里不用展开太多）

### 亮点 3：Human-in-the-loop（人机协作）安全兜底

- 任何写了变更文件/发布/重启/变更命令，必须**中断执行，推给人工审批**，人工 approve 才能执行
- 结果对不对人做最终决策，Agent 只做辅助定位不做决策，风险可控
- Checkpointer 持久化状态，中断后恢复不丢进度

### 亮点 4：历史故障知识库 RAG
- 过去故障处理完沉淀到知识库，下次遇到相似告警直接检索相似历史故障和根因，新人也能快定位
- 持续收集 bad case 增量更新，越来越准

### 亮点 5：安全分层防御
- 工具白名单（只允许查询类命令，禁止写命令）
- 命令执行沙箱：单独 K8s 命名空间，资源限制，网络隔离
- Prompt Injection 分层防御（标签隔离+检测）
- 全操作审计日志，可回溯

---

## 📊 量化结果

- 处理告警：日均 X 次，准确率 82%
- MTTR 从 25 分钟降到 8 分钟
- 减少资深 SRE 介入次数 45%
- 从未出现过因为 Agent 错误导致的生产故障（所有高危操作必须人工点确定才执行）

---

## 🎤 面试追问 Q&A
### Q0：技术栈怎么选的？为什么不全用Go或全用Python？
> 答：Go+Python分层，gRPC通信，这是大厂AI落地标准架构：①Go接入层扛高并发告警和查询流量（goroutine+Gin天然高并发，公司微服务全是Go，对接方便）；②Python Agent层用LangGraph/MCP生态做编排和RAG，迭代快不用重复造轮子；③AI服务QPS不高（告警已经被Go层聚合过滤），Python完全扛得住；④两边Protobuf定义接口，独立部署扩容，互不干扰。



### Q1：什么情况下需要 AI OnCall？AI 完全取代人不行吗？
> 答：AI 是辅助，不是完全取代人。因为根因定位需要结合业务经验，而且高危操作影响生产，必须人做最终决策；AI 能帮你快速拉数据找相似历史，给出结论建议，缩小排查范围，省时间给人做最终决策，减少 MTTR。

### Q2：多个 Worker Agent 怎么通信？
> 答：通过 LangGraph 共享 State（黑板模式），所有 Agent 读写同一个 State 对象，不用消息队列。Supervisor 路由到不同 Worker，每个 Worker 写结果到 State，然后 Supervisor 汇总。

### Q3：为什么用 Supervisor 不用 Swarm？
> 答：Swarm 是平等对话，适合多个专家平级讨论；Oncall 场景需要一个集中做汇总路由和权限管控，Supervisor 更合适，架构更简单可控。如果是多个专家写论文那种多轮协作，Swarm 更合适，场景不同架构不同。

### Q4：怎么处理不同告警规则频繁变更？
> 答：和项目A一样，告警规则存在哪里？存在规则配置库里，变更后异步更新向量库，版本控制，下线的自动过滤检索不到，和项目A一样的增量更新逻辑。

### Q5：怎么验证模型回答正确？
> 答：① 用户反馈点赞点踩，坏 case 收集回去每周review；② 离线评测：构造历史故障案例测试集，每次调整模型后跑一遍看准确率；③ 上线后持续观察告警处理准确率，逐步迭代。

---

## 🚀 你需要做的最小实操

同样最小改动，能讲清楚就行：

1. 基于 LangGraph 搭 Supervisor + 两个 Mock 工具（Prometheus查询+日志查询）
2. 画架构图
3. 准备一两个完整故障定位故事，说清楚从告警到结论的完整流程
4. 量化指标填进去就行

W10-W12 学多 Agent 的时候再完整搭骨架，现在只要把架构和亮点理清楚。


---

## 🔬 Supervisor-Worker 多Agent 详细设计（面试展开）

### 为什么不用单Agent？
单Agent ReAct循环只能串行：查指标→查日志→查变更→查CMDB，每步等上一步结果，总延迟是四个操作相加。多Agent并行：指标Worker、日志Worker、变更Worker、CMDB Worker同时拉数据，Supervisor等所有结果回来后汇总推理，总延迟等于最慢的那个Worker，快很多。

### LangGraph 状态机设计（黑板模式）

所有Agent共享一个State对象（类似黑板），每个Agent往上面写自己的发现，Supervisor最后汇总。

```python
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END

class OnCallState(TypedDict):
    # 输入
    alert_id: str
    alert_message: str
    
    # 各Worker的结果（并行写入）
    metrics_result: dict | None        # Prometheus Worker写
    logs_result: dict | None          # Loki Worker写
    changes_result: dict | None       # 发布系统Worker写
    cmdb_result: dict | None          # CMDB Worker写
    similar_cases: list[dict] | None  # 历史案例RAG Worker写
    
    # 汇总结果
    root_cause_summary: str | None     # 报告Agent写
    suggested_actions: list[str]       # 报告Agent写
    
    # HITL相关
    pending_approval: bool            # 是否等待人工审批
    approval_result: str | None        # approve/reject
    human_feedback: str | None
```

### 节点定义（每个Agent是一个节点）

```python
# Supervisor节点：意图分类+路由
def supervisor_node(state: OnCallState) -> str:
    # 根据alert类型路由到不同Worker组合
    if "延迟高" in state["alert_message"]:
        return "parallel_investigation"  # 并行拉指标+日志+变更
    elif "错误率" in state["alert_message"]:
        return "parallel_investigation"
    else:
        return "direct_to_report"  # 简单告警直接生成报告

# Worker节点：查Prometheus指标
def metrics_worker(state: OnCallState) -> OnCallState:
    # 通过MCP调用Prometheus Server
    metrics = mcp_client.call_tool("query_metrics", {
        "query": "order_api_p99",
        "time_range": "last_1h"
    })
    state["metrics_result"] = metrics
    return state

# Worker节点：查Loki日志
def logs_worker(state: OnCallState) -> OnCallState:
    logs = mcp_client.call_tool("query_logs", {
        "service": "order_api",
        "keyword": "timeout"
    })
    state["logs_result"] = logs
    return state

# 类似定义changes_worker/cmdb_worker/similar_cases_worker...

# 报告Agent：汇总所有结果生成根因报告
def report_agent(state: OnCallState) -> OnCallState:
    # 把所有Worker结果拼成上下文
    context = f"""
    【Prometheus指标】{state['metrics_result']}
    【Loki日志】{state['logs_result']}
    【近期变更】{state['changes_result']}
    【CMDB信息】{state['cmdb_result']}
    【相似历史故障】{state['similar_cases']}
    """
    
    # 调大模型生成报告
    summary = llm.generate(f"根据以下信息分析根因：{context}")
    state["root_cause_summary"] = summary
    return state
```

### HITL人工审批节点（高危操作必须人点）

```python
def hitl_approval_node(state: OnCallState) -> OnCallState:
    # 判断是否需要人工审批（比如要执行重启命令）
    if "需要重启" in state.get("suggested_actions", []):
        state["pending_approval"] = True
        # ★关键：中断执行，把状态持久化到Checkpointer
        # LangGraph会自动保存，等待人工审批后恢复
        return state  # 返回后LangGraph中断，等resume
    return state

# 人工审批后的恢复节点
def resume_after_approval(state: OnCallState) -> OnCallState:
    if state["approval_result"] == "approve":
        # 执行高危操作
        execute_command(state["suggested_actions"])
    else:
        # 人工拒绝，记录原因
        log("human rejected", state["human_feedback"])
    return state
```

### 边定义（条件路由）

```python
# 建图
graph = StateGraph(OnCallState)

# 添加节点
graph.add_node("supervisor", supervisor_node)
graph.add_node("metrics_worker", metrics_worker)
graph.add_node("logs_worker", logs_worker)
# ... 其他Worker节点
graph.add_node("report_agent", report_agent)
graph.add_node("hitl_approval", hitl_approval_node)
graph.add_node("resume", resume_after_approval)

# 定义边（路由逻辑）
graph.set_entry_point("supervisor")
graph.add_conditional_edges(
    "supervisor",
    {
        "parallel_investigation": "parallel_investigation",
        "direct_to_report": "report_agent"
    }
)

# 并行拉数据：多个Worker同时执行（Fan-out）
graph.add_edge("metrics_worker", "report_agent")
graph.add_edge("logs_worker", "report_agent")
# ... 其他Worker都连到report_agent（Fan-in）

# 报告生成后判断是否需要HITL
graph.add_conditional_edges(
    "report_agent",
    lambda s: "hitl" if s.get("pending_approval") else "end",
    {
        "hitl": "hitl_approval",
        "end": END
    }
)

# HITL审批后恢复
graph.add_edge("hitl_approval", "resume")
graph.add_edge("resume", END)
```

### Checkpointer持久化（支持中断/恢复）

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# SQLite持久化状态（生产用PostgreSQL）
saver = SqliteSaver.from_conn_string(":memory:")

# 编译图时传入checkpointer
app = graph.compile(checkpointer=saver)

# 运行时指定thread_id（每个告警一个thread_id，隔离状态）
config = {"configurable": {"thread_id": "alert_12345"}}

# 运行到HITL节点会自动中断
result = app.invoke(initial_state, config)

# 人工审批后恢复（不用从头跑，从HITL节点继续）
state = app.get_state(config)
state.update({"approval_result": "approve", "human_feedback": "同意重启"})
result = app.invoke(None, config)  # None表示从当前状态继续
```

### 面试讲法（关键点）

> **为什么用Supervisor不用Swarm？** Swarm是平等对话，适合多个专家平级讨论（比如写论文）；OnCall场景需要一个集中做汇总路由和权限管控，Supervisor更简单可控。
>
> **多Agent怎么通信？** 用黑板模式（共享State），每个Worker写结果到State，Supervisor读State汇总，不用消息队列。
>
> **HITL怎么实现？** LangGraph的interrupt机制，节点返回后如果pending_approval=True就中断，Checkpointer自动保存状态。人工审批后调用app.invoke(None, config)从当前状态继续，不用从头跑。
>
> **并行怎么保证不冲突？** Worker只写自己负责的字段（metrics_worker只写metrics_result），不覆盖别人的字段，天然无冲突。如果多个Worker写同一个字段，可以用列表append。

