#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path('/home/mifu/openclaw-data')
RECORDS_DIR = ROOT / 'tests' / 'drafts' / 'manual-records'


def slug(s: str) -> str:
    import re
    s = s.strip().lower().replace('_', '-').replace(' ', '-')
    s = re.sub(r'[^a-z0-9\-]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s or 'unnamed'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', required=True)
    ap.add_argument('--module', required=True)
    ap.add_argument('--page', required=True)
    ap.add_argument('--feature', required=True)
    ap.add_argument('--env', default='test')
    args = ap.parse_args()

    RECORDS_DIR.mkdir(parents=True, exist_ok=True)
    path = RECORDS_DIR / f"{slug(args.project)}-{slug(args.module)}-{slug(args.page)}-{slug(args.feature)}.json"
    payload = {
        'meta': {
            'project': args.project,
            'module': args.module,
            'page': args.page,
            'feature': args.feature,
            'env': args.env,
            'source': '真实手测'
        },
        'preconditions': [
            '补充前置条件1',
            '补充前置条件2'
        ],
        'steps': [
            '补充步骤1',
            '补充步骤2'
        ],
        'assertions': [
            '补充断言1',
            '补充断言2'
        ],
        'artifacts': [],
        'notes': []
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({
        'status': 'ok',
        'record_path': str(path),
        'next_steps': [
            '补充真实测试步骤与断言',
            '再运行 manual_to_script.py 生成脚本骨架'
        ]
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
