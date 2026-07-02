# 📚 持续学习仓库

> 记录学习资料、笔记与复盘总结，保持终身学习的习惯。

## 📂 目录结构

```
learning-journal/
├── docs/
│   ├── notes/          # 学习笔记（按主题/日期组织）
│   ├── summaries/      # 复盘总结（周/月/季度/年复盘）
│   └── resources/      # 学习资源整理（书单、课程、文章等）
├── templates/          # 笔记和复盘模板
├── scripts/            # 实用脚本
└── README.md
```

## 🚀 快速开始

### 新建一篇学习笔记

```bash
./scripts/new-note.sh "主题名称"
```

### 新建一次复盘总结

```bash
./scripts/new-summary.sh weekly    # 周复盘
./scripts/new-summary.sh monthly   # 月复盘
./scripts/new-summary.sh quarterly # 季度复盘
./scripts/new-summary.sh yearly    # 年复盘
```

## 📝 笔记规范

- 文件名格式：`YYYY-MM-DD-主题.md`，例如 `2026-07-02-Python异步编程.md`
- 使用 Markdown 格式书写
- 每篇笔记建议包含：学习目标、核心要点、实践示例、疑问与思考
- 善用标签（tags）分类，便于后续检索

## 🔄 复盘框架

复盘采用 **GRAI 方法**（Goal - Result - Analysis - Insight）：

1. **Goal（目标回顾）**：当初设定的目标是什么？
2. **Result（结果对比）**：实际结果如何？哪些做得好？哪些有待改进？
3. **Analysis（原因分析）**：成功/失败的根本原因是什么？
4. **Insight（规律总结）**：学到了什么？下次如何改进？

## 📊 学习状态

| 周期    | 笔记数 | 复盘数 | 关键收获 |
|---------|--------|--------|----------|
| 2026 Q3 | 0      | 0      | -        |

## 🛠 工具推荐

- **笔记**：Markdown + VS Code / Obsidian
- **思维导图**：XMind / Mermaid
- **闪卡复习**：Anki
- **阅读管理**：Zotero / Pocket

## 📜 License

MIT
