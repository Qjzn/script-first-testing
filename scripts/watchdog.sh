#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/mifu/openclaw-data"
SKILL_DIR="$ROOT/skills/script-first-testing"
OUT_DIR="$SKILL_DIR/output"
mkdir -p "$OUT_DIR"
TS="$(date '+%Y-%m-%d %H:%M:%S')"
REPORT="$OUT_DIR/watchdog-latest.md"
QUEUE="$SKILL_DIR/tasks/QUEUE.md"
CATALOG="$ROOT/tests/TEST_CATALOG.json"
INDEX="$ROOT/tests/TEST_INDEX.md"

{
  echo "# Script First Testing Watchdog"
  echo
  echo "时间: $TS"
  echo
  echo "## Git 状态"
  git -C "$SKILL_DIR" status --short || true
  echo
  echo "## Queue 摘要"
  if [ -f "$QUEUE" ]; then
    grep -E '^## |^- \[' "$QUEUE" || true
  else
    echo "QUEUE.md 不存在"
  fi
  echo
  echo "## Catalog 状态"
  if [ -f "$CATALOG" ]; then
    python3 - <<'PY'
import json
p='/home/mifu/openclaw-data/tests/TEST_CATALOG.json'
try:
    data=json.load(open(p))
    todo=sum(1 for x in data if x.get('status')=='todo')
    print(f'count={len(data)} todo={todo}')
except Exception as e:
    print(f'catalog_error={e}')
PY
  else
    echo "TEST_CATALOG.json 不存在"
  fi
  echo
  echo "## Index 状态"
  if [ -f "$INDEX" ]; then
    wc -l "$INDEX"
  else
    echo "TEST_INDEX.md 不存在"
  fi
  echo
  echo "## 建议下一步"
  echo "1. 先做 Ready 第一项"
  echo "2. 每次 register/manual_to_script 后确认 catalog 自动刷新"
  echo "3. 每次大改后用 fzyc learning upload 做真实验收"
} > "$REPORT"

echo "$REPORT"
