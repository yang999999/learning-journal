#!/usr/bin/env bash
# 新建学习笔记
# 用法: ./scripts/new-note.sh "主题名称" [tags]

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "用法: $0 <主题名称> [标签,用逗号分隔]"
    echo "示例: $0 \"Python异步编程\" \"python,async\""
    exit 1
fi

TITLE="$1"
TAGS="${2:-}"
DATE=$(date +%Y-%m-%d)
DATETIME=$(date +%Y-%m-%dT%H:%M:%S%z)
SAFE_TITLE=$(echo "$TITLE" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5-]//g')
FILENAME="docs/notes/${DATE}-${SAFE_TITLE}.md"
TEMPLATE="templates/note-template.md"

if [ ! -f "$TEMPLATE" ]; then
    echo "错误: 模板文件 $TEMPLATE 不存在"
    exit 1
fi

# 从模板生成笔记
sed -e "s/{{title}}/${TITLE}/g" \
    -e "s/{{date}}/${DATETIME}/g" \
    "$TEMPLATE" > "$FILENAME"

# 添加标签
if [ -n "$TAGS" ]; then
    IFS=',' read -ra TAG_ARRAY <<< "$TAGS"
    TAG_LIST=""
    for tag in "${TAG_ARRAY[@]}"; do
        TAG_LIST+="\"${tag// /}\", "
    done
    TAG_LIST="[${TAG_LIST%, }]"
    sed -i '' "s/tags: \[\]/tags: ${TAG_LIST}/" "$FILENAME"
fi

echo "✅ 新笔记已创建: $FILENAME"

# 尝试用默认编辑器打开
if [ -n "${EDITOR:-}" ]; then
    $EDITOR "$FILENAME"
elif command -v code &> /dev/null; then
    code "$FILENAME"
fi
