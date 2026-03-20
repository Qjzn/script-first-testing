#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/mifu/openclaw-data"
SKILL_DIR="$ROOT/skills/script-first-testing"
CRON_LINE="*/10 * * * * bash $SKILL_DIR/scripts/watchdog.sh >> $SKILL_DIR/runtime/cron.log 2>&1"
TMP=$(mktemp)
crontab -l 2>/dev/null | grep -v "script-first-testing/scripts/watchdog.sh" > "$TMP" || true
echo "$CRON_LINE" >> "$TMP"
crontab "$TMP"
rm -f "$TMP"
echo "$CRON_LINE"
