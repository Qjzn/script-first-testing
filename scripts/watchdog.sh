#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/mifu/openclaw-data"
SKILL_DIR="$ROOT/skills/script-first-testing"
OUT_DIR="$SKILL_DIR/output"
STATE_DIR="$SKILL_DIR/runtime"
mkdir -p "$OUT_DIR" "$STATE_DIR"
TS="$(date '+%Y-%m-%d %H:%M:%S')"
REPORT="$OUT_DIR/watchdog-latest.md"
QUEUE="$SKILL_DIR/tasks/QUEUE.md"
CATALOG="$ROOT/tests/TEST_CATALOG.json"
INDEX="$ROOT/tests/TEST_INDEX.md"
STATE_JSON="$STATE_DIR/promoter-state.json"
WATCHDOG_LOG="$STATE_DIR/watchdog.log"
PROMOTER="$SKILL_DIR/scripts/promoter.sh"
NEEDS_WAKE=0

if [ ! -f "$STATE_JSON" ]; then
  NEEDS_WAKE=1
else
  AGE=$(python3 - <<'PY'
import json, time
from pathlib import Path
p=Path('/home/mifu/openclaw-data/skills/script-first-testing/runtime/promoter-state.json')
try:
    data=json.loads(p.read_text(encoding='utf-8'))
    ts=data.get('last_seen','')
    now=time.time()
    last=time.mktime(time.strptime(ts, '%Y-%m-%d %H:%M:%S'))
    print(int(now-last))
except Exception:
    print(999999)
PY
)
  if [ "$AGE" -gt 900 ]; then
    NEEDS_WAKE=1
  fi
fi

if [ "$NEEDS_WAKE" -eq 1 ]; then
  bash "$PROMOTER" || true
  echo "[$TS] promoter awakened" >> "$WATCHDOG_LOG"
else
  echo "[$TS] promoter healthy" >> "$WATCHDOG_LOG"
fi

{
  echo "# Script First Testing Watchdog"
  echo
  echo "时间: $TS"
  echo
  echo "## Promoter 状态"
  if [ -f "$STATE_JSON" ]; then
    cat "$STATE_JSON"
  else
    echo "promoter-state.json 不存在"
  fi
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
  echo "## 守护动作"
  if [ "$NEEDS_WAKE" -eq 1 ]; then
    echo "promoter 已唤醒"
  else
    echo "promoter 运行正常"
  fi
} > "$REPORT"

echo "$REPORT"
