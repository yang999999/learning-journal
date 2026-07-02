#!/usr/bin/env bash
# 新建复盘总结
# 用法: ./scripts/new-summary.sh <weekly|monthly|quarterly|yearly>

set -euo pipefail

TYPE="${1:-weekly}"
DATE=$(date +%Y-%m-%d)
DATETIME=$(date +%Y-%m-%dT%H:%M:%S%z)
TEMPLATE="templates/summary-template.md"

case "$TYPE" in
    weekly)
        # 获取本周的周一日期
        WEEK_NUM=$(date +%V)
        YEAR=$(date +%Y)
        PERIOD="${YEAR}年第${WEEK_NUM}周"
        TITLE="第${WEEK_NUM}周"
        FILENAME="docs/summaries/${DATE}-weekly-${YEAR}-W${WEEK_NUM}.md"
        ;;
    monthly)
        MONTH=$(date +%m)
        YEAR=$(date +%Y)
        PERIOD="${YEAR}年${MONTH}月"
        TITLE="${YEAR}年${MONTH}月"
        FILENAME="docs/summaries/${DATE}-monthly-${YEAR}-${MONTH}.md"
        ;;
    quarterly)
        MONTH=$(date +%m)
        QUARTER=$(( (10#$MONTH - 1) / 3 + 1 ))
        YEAR=$(date +%Y)
        PERIOD="${YEAR}年Q${QUARTER}"
        TITLE="${YEAR}年Q${QUARTER}"
        FILENAME="docs/summaries/${DATE}-quarterly-${YEAR}-Q${QUARTER}.md"
        ;;
    yearly)
        YEAR=$(date +%Y)
        PERIOD="${YEAR}年"
        TITLE="${YEAR}年"
        FILENAME="docs/summaries/${DATE}-yearly-${YEAR}.md"
        ;;
    *)
        echo "错误: 不支持的复盘类型 '$TYPE'"
        echo "支持的类型: weekly, monthly, quarterly, yearly"
        exit 1
        ;;
esac

if [ ! -f "$TEMPLATE" ]; then
    echo "错误: 模板文件 $TEMPLATE 不存在"
    exit 1
fi

sed -e "s/{{title}}/${TITLE}/g" \
    -e "s/{{period}}/${PERIOD}/g" \
    -e "s/{{date}}/${DATETIME}/g" \
    -e "s/{{type}}/${TYPE}/g" \
    "$TEMPLATE" > "$FILENAME"

echo "✅ ${PERIOD}复盘已创建: $FILENAME"

if [ -n "${EDITOR:-}" ]; then
    $EDITOR "$FILENAME"
elif command -v code &> /dev/null; then
    code "$FILENAME"
fi
