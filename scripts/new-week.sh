#!/usr/bin/env bash
# 新建一周学习计划
# 用法: ./scripts/new-week.sh <周数> <主题> [开始日期YYYY-MM-DD]
set -euo pipefail

if [ $# -lt 2 ]; then
    echo "用法: $0 <周数> <主题> [开始日期]"
    echo "示例: $0 2 \"Prompt Engineering深度实践\""
    exit 1
fi

WEEK_NUM="$1"
THEME="$2"
START_DATE="${3:-}"
YEAR=$(date +%Y)

if [ -z "$START_DATE" ]; then
    # 计算本周周一日期 (macOS/Linux兼容)
    if [[ "$(uname)" == "Darwin" ]]; then
        START_DATE=$(date -j -f "%Y-%m-%d" "$(date -v-mon +%Y-%m-%d)" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)
    else
        DOW=$(date +%u)
        START_DATE=$(date -d "today - $((DOW-1)) days" +%Y-%m-%d)
    fi
fi

# 计算结束日期 (start + 6 days)
if [[ "$(uname)" == "Darwin" ]]; then
    END_DATE=$(date -j -f "%Y-%m-%d" -v+6d "${START_DATE}" +%Y-%m-%d)
else
    END_DATE=$(date -d "${START_DATE} +6 days" +%Y-%m-%d)
fi

SAFE_THEME=$(echo "$THEME" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5-]//g' | sed 's/-\+/-/g' | sed 's/^-//;s/-$//')
FILENAME="weekly/W${WEEK_NUM}-${SAFE_THEME}.md"
TEMPLATE="templates/weekly-plan-template.md"

if [ ! -f "$TEMPLATE" ]; then
    echo "错误: 模板文件 $TEMPLATE 不存在"
    exit 1
fi

mkdir -p weekly
sed -e "s/{{week_number}}/${WEEK_NUM}/g" \
    -e "s/{{year}}/${YEAR}/g" \
    -e "s/{{start_date}}/${START_DATE}/g" \
    -e "s/{{end_date}}/${END_DATE}/g" \
    -e "s/{{theme}}/${THEME}/g" \
    "$TEMPLATE" > "$FILENAME"

echo "✅ Week ${WEEK_NUM} 计划已创建: $FILENAME"
echo "   主题: ${THEME}"
echo "   日期: ${START_DATE} ~ ${END_DATE}"

if command -v code &> /dev/null; then
    code "$FILENAME"
fi
