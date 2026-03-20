#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/mifu/openclaw-data"
SKILL_DIR="$ROOT/skills/script-first-testing"
STATE_DIR="$SKILL_DIR/runtime"
QUEUE="$SKILL_DIR/tasks/QUEUE.md"
LOG="$STATE_DIR/promoter.log"
STATE_JSON="$STATE_DIR/promoter-state.json"
mkdir -p "$STATE_DIR"
TS="$(date '+%Y-%m-%d %H:%M:%S')"
PID="$$"

echo "[$TS] promoter start pid=$PID" >> "$LOG"
python3 "$SKILL_DIR/scripts/next_actions.py" > "$STATE_DIR/next-actions.json"

python3 - <<'PY'
import json
from pathlib import Path
root=Path('/home/mifu/openclaw-data/skills/script-first-testing')
queue=root/'tasks'/'QUEUE.md'
state=root/'runtime'/'promoter-state.json'
ready=[]
if queue.exists():
    lines=queue.read_text(encoding='utf-8').splitlines()
    in_ready=False
    for line in lines:
        if line.startswith('## Ready'):
            in_ready=True
            continue
        if line.startswith('## ') and not line.startswith('## Ready'):
            in_ready=False
        if in_ready and line.startswith('- [ ] '):
            ready.append(line[6:])
state.write_text(json.dumps({
    'status':'idle',
    'last_seen':'$TS',
    'pid':'$PID',
    'ready_count':len(ready),
    'top_ready':ready[:3]
}, ensure_ascii=False, indent=2), encoding='utf-8')
PY

echo "[$TS] promoter heartbeat written" >> "$LOG"
