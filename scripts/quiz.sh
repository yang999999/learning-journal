#!/usr/bin/env bash
# 面试抽题脚本：随机抽题自测（不显示答案，答案在对应速查手册里）
# 用法:
#   ./scripts/quiz.sh              # 从所有模块随机抽5题
#   ./scripts/quiz.sh mysql        # 只抽MySQL题
#   ./scripts/quiz.sh all 10       # 抽10题
set -euo pipefail

DIR="$(cd "$(dirname "$0")/.." && pwd)"
BANK="$DIR/interview/questions-bank.json"

MODULE="${1:-all}"
COUNT="${2:-5}"

python3 - "$BANK" "$MODULE" "$COUNT" << 'PYEOF'
import json, sys, random

bank_file, module, count = sys.argv[1], sys.argv[2], int(sys.argv[3])
with open(bank_file, encoding="utf-8") as f:
    bank = json.load(f)

if module == "all":
    pool = []
    for cat, qs in bank.items():
        for q in qs:
            pool.append((cat, q))
else:
    cat_map = {k.lower(): k for k in bank}
    if module.lower() not in cat_map:
        print(f"❌ 未知模块: {module}")
        print(f"可选模块: {', '.join(bank.keys())}, all")
        sys.exit(1)
    cat = cat_map[module.lower()]
    pool = [(cat, q) for q in bank[cat]]

picked = random.sample(pool, min(count, len(pool)))

print(f"\n🎯 面试抽题（{len(picked)} 题）\n")
print("=" * 60)
for i, (cat, q) in enumerate(picked, 1):
    print(f"\n【Q{i}】[{cat}·{q['k']}]")
    print(f"  {q['q']}")
    print()
    input("  (按 Enter 看下一题)")
print("=" * 60)
print("\n📖 参考答案位置：")
print("  后端 → docs/resources/后端面试满分速查.md")
print("  AI  → docs/resources/AI-Agent面试满分速查.md")
PYEOF
