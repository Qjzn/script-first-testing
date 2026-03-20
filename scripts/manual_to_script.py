#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/mifu/openclaw-data')
TESTS_ROOT = ROOT / 'tests' / 'projects'
BUILD_CATALOG = ROOT / 'skills' / 'script-first-testing' / 'scripts' / 'build_test_catalog.py'

TEMPLATE = '''#!/usr/bin/env python3
"""
由真实测试记录自动生成的脚本骨架
项目: {project}
模块: {module}
页面: {page}
功能点: {feature}
类型: {level}
"""
import json
import sys
from pathlib import Path
ROOT = Path('/home/mifu/openclaw-data')
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TEST_METADATA = {{
    "project": "{project}",
    "module": "{module}",
    "page": "{page}",
    "feature": "{feature}",
    "level": "{level}",
    "status": "todo",
    "summary": "待补充基于真实测试记录的自动化步骤",
    "capability": "{capability}",
    "entry": "{entry}",
    "requires_login": true,
    "assertion_type": {assertion_type}
}}

RESULT = {{
    "project": "{project}",
    "module": "{module}",
    "page": "{page}",
    "feature": "{feature}",
    "level": "{level}",
    "status": "todo",
    "summary": "待补充基于真实测试记录的自动化步骤",
    "manual_source": "{manual_source}",
    "preconditions": {preconditions},
    "steps": {steps},
    "assertions": {assertions}
}}


def main():
    print(json.dumps(RESULT, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
'''


def slug(s: str) -> str:
    import re
    s = s.strip().lower().replace('_', '-').replace(' ', '-')
    s = re.sub(r'[^a-z0-9\-]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s or 'unnamed'


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
        result.extend(['upload', 'request'])
    return sorted(set(result))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True, help='真实测试记录 JSON 文件')
    ap.add_argument('--project', required=True)
    ap.add_argument('--module', required=True)
    ap.add_argument('--page', required=True)
    ap.add_argument('--feature', required=True)
    ap.add_argument('--level', default='L2')
    args = ap.parse_args()

    source = Path(args.input)
    data = json.loads(source.read_text(encoding='utf-8'))
    preconditions = data.get('preconditions', [])
    steps = data.get('steps', [])
    assertions = data.get('assertions', [])

    target_dir = TESTS_ROOT / slug(args.project) / slug(args.module) / slug(args.page)
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = 'smoke.py' if args.level == 'L1' else f'{slug(args.feature)}.py'
    target = target_dir / filename
    target.write_text(TEMPLATE.format(
        project=args.project,
        module=args.module,
        page=args.page,
        feature=args.feature,
        level=args.level,
        capability=infer_capability(args.feature),
        entry=infer_entry(args.module, args.page),
        assertion_type=json.dumps(infer_assertion_type(args.feature), ensure_ascii=False),
        manual_source=str(source),
        preconditions=json.dumps(preconditions, ensure_ascii=False, indent=4),
        steps=json.dumps(steps, ensure_ascii=False, indent=4),
        assertions=json.dumps(assertions, ensure_ascii=False, indent=4),
    ), encoding='utf-8')

    subprocess.run([sys.executable, str(BUILD_CATALOG)], check=False)

    print(json.dumps({
        'status': 'ok',
        'script_path': str(target),
        'manual_source': str(source),
        'catalog_refreshed': True,
        'next_steps': [
            '补充真实自动化实现',
            '运行 register_test.py 登记到 TEST_INDEX.md',
            '再用 run_test.py 验证结果语义'
        ]
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
