#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ROOT = Path('/home/mifu/openclaw-data')
TESTS_ROOT = ROOT / 'tests' / 'projects'

TEMPLATE = '''"""
项目: {project}
模块: {module}
页面: {page}
功能点: {feature}
类型: {level}
环境: {env}
前置条件:
- 补充账号/登录态
- 补充目标页面路径
断言:
- 页面成功打开
- 关键元素存在
- 无明显报错
"""
from pathlib import Path
import json
import time

TEST_METADATA = {{
    "project": "{project}",
    "module": "{module}",
    "page": "{page}",
    "feature": "{feature}",
    "level": "{level}",
    "status": "todo",
    "summary": "待补充实际自动化步骤",
    "capability": "{capability}",
    "entry": "{entry}",
    "requires_login": {requires_login},
    "assertion_type": {assertion_type}
}}

RESULT = {{
    "project": "{project}",
    "module": "{module}",
    "page": "{page}",
    "feature": "{feature}",
    "level": "{level}",
    "status": "todo",
    "summary": "待补充实际自动化步骤",
    "screenshots": [],
    "assertions": [
        "页面成功打开",
        "关键元素存在",
        "无明显报错"
    ]
}}


def main():
    print(json.dumps(RESULT, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
'''

INDEX_MAP = {
    'L1': '冒烟测试',
    'L2': '页面功能测试',
    'L3': '业务流程测试',
    'L4': '回归测试集',
}

def slug(s: str) -> str:
    s = s.strip().lower().replace('_', '-').replace(' ', '-')
    s = re.sub(r'[^a-z0-9\-]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s or 'unnamed'


def default_filename(level: str, feature: str) -> str:
    if level == 'L1':
        return 'smoke.py'
    return f'{slug(feature)}.py'


def update_index(project, module, page, feature, level, path):
    idx = ROOT / 'tests' / 'TEST_INDEX.md'
    content = idx.read_text(encoding='utf-8') if idx.exists() else '# TEST_INDEX\n\n'
    block = f'- {feature}\n  - 页面：{page}\n  - 脚本：`{path}`\n  - 类型：{INDEX_MAP.get(level, level)}\n'
    if block in content:
        return
    anchor = f'## {project}'
    if anchor not in content:
        content += f'\n## {project}\n\n'
    mod_anchor = f'### {module}'
    project_pos = content.index(anchor)
    tail = content[project_pos:]
    if mod_anchor not in tail:
        insert_pos = project_pos + len(tail)
        content = content[:insert_pos] + f'\n### {module}\n\n' + content[insert_pos:]
        project_pos = content.index(anchor)
        tail = content[project_pos:]
    mod_pos = content.index(mod_anchor, project_pos)
    next_heading = content.find('\n### ', mod_pos + 1)
    next_project = content.find('\n## ', mod_pos + 1)
    candidates = [x for x in [next_heading, next_project] if x != -1]
    insert_pos = min(candidates) if candidates else len(content)
    content = content[:insert_pos] + '\n' + block + content[insert_pos:]
    idx.write_text(content, encoding='utf-8')


def infer_capability(feature: str):
    f = feature.lower()
    if 'upload' in f:
        return 'upload-cover' if 'cover' in f else 'upload'
    if 'default' in f:
        return 'default-cover'
    if 'smoke' in f:
        return 'smoke'
    return f


def infer_entry(module: str, page: str):
    return f'{module}#/{page}'


def infer_assertion_type(feature: str):
    f = feature.lower()
    result = ['dom']
    if 'upload' in f:
        result.append('upload')
        result.append('request')
    if 'smoke' in f:
        result.append('route')
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', required=True)
    ap.add_argument('--module', required=True)
    ap.add_argument('--page', required=True)
    ap.add_argument('--feature', required=True)
    ap.add_argument('--level', default='L2', choices=['L1', 'L2', 'L3', 'L4'])
    ap.add_argument('--env', default='test')
    ap.add_argument('--register-index', action='store_true')
    args = ap.parse_args()

    target_dir = TESTS_ROOT / slug(args.project) / slug(args.module) / slug(args.page)
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / default_filename(args.level, args.feature)
    if file_path.exists():
        print(file_path)
        return
    file_path.write_text(TEMPLATE.format(
        project=args.project,
        module=args.module,
        page=args.page,
        feature=args.feature,
        level=args.level,
        env=args.env,
        capability=infer_capability(args.feature),
        entry=infer_entry(args.module, args.page),
        requires_login='true',
        assertion_type=json.dumps(infer_assertion_type(args.feature), ensure_ascii=False),
    ), encoding='utf-8')
    if args.register_index:
        update_index(args.project, args.module, args.page, args.feature, args.level, file_path)
    print(file_path)


if __name__ == '__main__':
    main()
