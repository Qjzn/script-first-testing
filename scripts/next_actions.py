#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path('/home/mifu/openclaw-data')
QUEUE = ROOT / 'skills' / 'script-first-testing' / 'tasks' / 'QUEUE.md'
CATALOG = ROOT / 'tests' / 'TEST_CATALOG.json'


def ready_items():
    if not QUEUE.exists():
        return []
    lines = QUEUE.read_text(encoding='utf-8').splitlines()
    in_ready = False
    items = []
    for line in lines:
        if line.startswith('## Ready'):
            in_ready = True
            continue
        if line.startswith('## ') and not line.startswith('## Ready'):
            in_ready = False
        if in_ready and line.startswith('- [ ] '):
            items.append(line[6:])
    return items


def catalog_stats():
    if not CATALOG.exists():
        return {'count': 0, 'todo': 0}
    data = json.loads(CATALOG.read_text(encoding='utf-8'))
    return {
        'count': len(data),
        'todo': sum(1 for x in data if x.get('status') == 'todo')
    }


def main():
    stats = catalog_stats()
    items = ready_items()[:5]
    print(json.dumps({
        'catalog': stats,
        'next_actions': items,
        'recommended_acceptance': 'python3 /home/mifu/openclaw-data/tests/run_test.py --project fzyc --module learning --page home --keyword upload',
        'promoter_policy': '持续推进 script-first-testing 技能；若 15 分钟无心跳，看门狗自动唤醒；cron 每 10 分钟轮询一次'
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
