#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/mifu/openclaw-data')
INDEX_PATH = ROOT / 'tests' / 'TEST_INDEX.md'
BUILD_CATALOG = ROOT / 'skills' / 'script-first-testing' / 'scripts' / 'build_test_catalog.py'
INDEX_MAP = {
    'L1': '冒烟测试',
    'L2': '页面功能测试',
    'L3': '业务流程测试',
    'L4': '回归测试集',
}


def ensure_module_section(content: str, project: str, module: str):
    anchor = f'## {project}'
    if anchor not in content:
        content += f'\n## {project}\n\n'
    project_pos = content.index(anchor)
    tail = content[project_pos:]
    mod_anchor = f'### {module}'
    if mod_anchor not in tail:
        insert_pos = project_pos + len(tail)
        content = content[:insert_pos] + f'\n### {module}\n\n' + content[insert_pos:]
    return content


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', required=True)
    ap.add_argument('--module', required=True)
    ap.add_argument('--page', required=True)
    ap.add_argument('--feature', required=True)
    ap.add_argument('--level', default='L2')
    ap.add_argument('--script-path', required=True)
    args = ap.parse_args()

    content = INDEX_PATH.read_text(encoding='utf-8') if INDEX_PATH.exists() else '# TEST_INDEX\n\n'
    content = ensure_module_section(content, args.project, args.module)
    block = f'- {args.feature}\n  - 页面：{args.page}\n  - 脚本：`{args.script_path}`\n  - 类型：{INDEX_MAP.get(args.level, args.level)}\n'
    if block not in content:
        mod_anchor = f'### {args.module}'
        mod_pos = content.index(mod_anchor, content.index(f'## {args.project}'))
        next_heading = content.find('\n### ', mod_pos + 1)
        next_project = content.find('\n## ', mod_pos + 1)
        candidates = [x for x in [next_heading, next_project] if x != -1]
        insert_pos = min(candidates) if candidates else len(content)
        content = content[:insert_pos] + '\n' + block + content[insert_pos:]
        INDEX_PATH.write_text(content, encoding='utf-8')

    subprocess.run([sys.executable, str(BUILD_CATALOG)], check=False)

    print(json.dumps({
        'status': 'ok',
        'project': args.project,
        'module': args.module,
        'page': args.page,
        'feature': args.feature,
        'script_path': args.script_path,
        'index_path': str(INDEX_PATH),
        'catalog_refreshed': True,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
