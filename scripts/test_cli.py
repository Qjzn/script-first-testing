#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/mifu/openclaw-data')
SCRIPTS = ROOT / 'skills' / 'script-first-testing' / 'scripts'
REFS = ROOT / 'skills' / 'script-first-testing' / 'references'
CONFIGS = ROOT / 'skills' / 'script-first-testing' / 'configs'
TESTS_ROOT = ROOT / 'tests' / 'projects'
RUNNER = ROOT / 'tests' / 'run_test.py'
TEMPLATE_PATH = REFS / 'project-config-template.json'

REQUIRED_TOP_LEVEL = ['project', 'env', 'baseUrl', 'routeMode', 'login', 'selectors', 'routes']
REQUIRED_LOGIN = ['required', 'url', 'usernameSelector', 'passwordSelector', 'submitSelector']
REQUIRED_SELECTORS = ['upload']
REQUIRED_ROUTES = ['home']

SMOKE_TEMPLATE = '''#!/usr/bin/env python3
import json
import sys
from pathlib import Path
ROOT = Path('/home/mifu/openclaw-data')
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tests.shared.project_config import load_project_config

CFG = load_project_config('{project}')
LOGIN = CFG['login']
ROUTES = CFG['routes']


def main():
    result = {{
        "project": "{project}",
        "module": "{module}",
        "page": "{page}",
        "feature": "smoke",
        "level": "L1",
        "status": "todo",
        "summary": "配置驱动 smoke 模板已生成，待补真实自动化步骤",
        "config_snapshot": {{
            "baseUrl": CFG.get("baseUrl"),
            "loginRequired": LOGIN.get("required"),
            "loginUrl": LOGIN.get("url"),
            "targetRoute": ROUTES.get("{page_route_key}", ROUTES.get("home", "/"))
        }}
    }}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(3)


if __name__ == '__main__':
    main()
'''

FEATURE_TEMPLATE = '''#!/usr/bin/env python3
import json
import sys
from pathlib import Path
ROOT = Path('/home/mifu/openclaw-data')
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tests.shared.project_config import load_project_config

CFG = load_project_config('{project}')
LOGIN = CFG['login']
SELECTORS = CFG['selectors']
ROUTES = CFG['routes']


def main():
    result = {{
        "project": "{project}",
        "module": "{module}",
        "page": "{page}",
        "feature": "{feature}",
        "level": "L2",
        "status": "todo",
        "summary": "配置驱动 {feature_cn} 模板已生成，待补真实自动化步骤",
        "config_snapshot": {{
            "baseUrl": CFG.get("baseUrl"),
            "loginRequired": LOGIN.get("required"),
            "loginUrl": LOGIN.get("url"),
            "targetRoute": ROUTES.get("{page_route_key}", ROUTES.get("home", "/")),
            "uploadSelector": SELECTORS.get("upload"),
            "defaultCoverButton": SELECTORS.get("defaultCoverButton")
        }}
    }}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(3)


if __name__ == '__main__':
    main()
'''


def run(cmd):
    proc = subprocess.run(cmd)
    raise SystemExit(proc.returncode)


def load_template():
    return json.loads(TEMPLATE_PATH.read_text(encoding='utf-8'))


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def validate_config_data(data: dict):
    errors = []
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f'缺少顶层字段: {key}')
    login = data.get('login', {})
    selectors = data.get('selectors', {})
    routes = data.get('routes', {})
    for key in REQUIRED_LOGIN:
        if key not in login:
            errors.append(f'缺少 login 字段: {key}')
    for key in REQUIRED_SELECTORS:
        if key not in selectors:
            errors.append(f'缺少 selectors 字段: {key}')
    for key in REQUIRED_ROUTES:
        if key not in routes:
            errors.append(f'缺少 routes 字段: {key}')
    return errors


def cmd_init_project(args):
    data = load_template()
    data['project'] = args.project
    data['env'] = args.env
    data['baseUrl'] = args.base_url
    data['login']['url'] = args.login_url or f"{args.base_url.rstrip('/')}/login"
    config_path = CONFIGS / f'{args.project}.json'
    if config_path.exists() and not args.force:
        print(json.dumps({'status': 'exists', 'config_path': str(config_path), 'summary': '项目配置已存在，如需覆盖请加 --force'}, ensure_ascii=False, indent=2))
        return
    save_json(config_path, data)
    project_root = TESTS_ROOT / args.project / args.module / args.page
    project_root.mkdir(parents=True, exist_ok=True)
    print(json.dumps({
        'status': 'ok',
        'summary': '项目骨架已初始化',
        'config_path': str(config_path),
        'project_root': str(project_root),
    }, ensure_ascii=False, indent=2))


def cmd_validate_config(args):
    path = Path(args.config) if args.config else CONFIGS / f'{args.project}.json'
    if not path.exists():
        print(json.dumps({'status': 'fail', 'summary': '配置文件不存在', 'config_path': str(path)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    data = json.loads(path.read_text(encoding='utf-8'))
    errors = validate_config_data(data)
    project_root = TESTS_ROOT / data['project']
    result = {
        'status': 'pass' if not errors else 'fail',
        'config_path': str(path),
        'project': data.get('project'),
        'project_root_exists': project_root.exists(),
        'errors': errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


def write_force(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def cmd_scaffold_from_config(args):
    path = Path(args.config) if args.config else CONFIGS / f'{args.project}.json'
    if not path.exists():
        print(json.dumps({'status': 'fail', 'summary': '配置文件不存在', 'config_path': str(path)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    data = json.loads(path.read_text(encoding='utf-8'))
    errors = validate_config_data(data)
    if errors:
        print(json.dumps({'status': 'fail', 'summary': '配置校验失败', 'errors': errors}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    project = data['project']
    module = args.module
    page = args.page
    target = TESTS_ROOT / project / module / page
    write_force(target / 'smoke.py', SMOKE_TEMPLATE.format(
        project=project,
        module=module,
        page=page,
        page_route_key=page,
    ))
    write_force(target / 'default-cover.py', FEATURE_TEMPLATE.format(
        project=project,
        module=module,
        page=page,
        page_route_key=page,
        feature='default-cover',
        feature_cn='默认封面',
    ))
    write_force(target / 'upload-cover.py', FEATURE_TEMPLATE.format(
        project=project,
        module=module,
        page=page,
        page_route_key=page,
        feature='upload-cover',
        feature_cn='上传封面',
    ))
    print(json.dumps({
        'status': 'ok',
        'summary': '已按配置生成可运行配置驱动模板',
        'target': str(target),
        'files': [
            str(target / 'smoke.py'),
            str(target / 'default-cover.py'),
            str(target / 'upload-cover.py'),
        ]
    }, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description='Script First Testing CLI')
    sub = ap.add_subparsers(dest='command', required=True)

    p_find = sub.add_parser('find')
    p_find.add_argument('--project', required=True)
    p_find.add_argument('--module', required=True)
    p_find.add_argument('--page', required=True)
    p_find.add_argument('--feature')
    p_find.add_argument('--keyword')

    p_run = sub.add_parser('run')
    p_run.add_argument('--project', required=True)
    p_run.add_argument('--module', required=True)
    p_run.add_argument('--page', required=True)
    p_run.add_argument('--feature')
    p_run.add_argument('--keyword')

    p_record = sub.add_parser('record-template')
    p_record.add_argument('--project', required=True)
    p_record.add_argument('--module', required=True)
    p_record.add_argument('--page', required=True)
    p_record.add_argument('--feature', required=True)
    p_record.add_argument('--env', default='test')

    p_generate = sub.add_parser('generate-from-record')
    p_generate.add_argument('--input', required=True)
    p_generate.add_argument('--project', required=True)
    p_generate.add_argument('--module', required=True)
    p_generate.add_argument('--page', required=True)
    p_generate.add_argument('--feature', required=True)
    p_generate.add_argument('--level', default='L2')

    p_register = sub.add_parser('register')
    p_register.add_argument('--project', required=True)
    p_register.add_argument('--module', required=True)
    p_register.add_argument('--page', required=True)
    p_register.add_argument('--feature', required=True)
    p_register.add_argument('--level', default='L2')
    p_register.add_argument('--script-path', required=True)

    sub.add_parser('build-catalog')

    p_init = sub.add_parser('init-project')
    p_init.add_argument('--project', required=True)
    p_init.add_argument('--env', default='test')
    p_init.add_argument('--base-url', required=True)
    p_init.add_argument('--login-url')
    p_init.add_argument('--module', default='home')
    p_init.add_argument('--page', default='index')
    p_init.add_argument('--force', action='store_true')

    p_validate = sub.add_parser('validate-config')
    p_validate.add_argument('--project')
    p_validate.add_argument('--config')

    p_scaffold = sub.add_parser('scaffold-from-config')
    p_scaffold.add_argument('--project')
    p_scaffold.add_argument('--config')
    p_scaffold.add_argument('--module', default='home')
    p_scaffold.add_argument('--page', default='index')

    args = ap.parse_args()

    if args.command == 'find':
        run([sys.executable, str(SCRIPTS / 'locate_test.py'), '--project', args.project, '--module', args.module, '--page', args.page, *(['--feature', args.feature] if args.feature else []), *(['--keyword', args.keyword] if args.keyword else [])])
    elif args.command == 'run':
        run([sys.executable, str(RUNNER), '--project', args.project, '--module', args.module, '--page', args.page, *(['--feature', args.feature] if args.feature else []), *(['--keyword', args.keyword] if args.keyword else [])])
    elif args.command == 'record-template':
        run([sys.executable, str(SCRIPTS / 'create_manual_record.py'), '--project', args.project, '--module', args.module, '--page', args.page, '--feature', args.feature, '--env', args.env])
    elif args.command == 'generate-from-record':
        run([sys.executable, str(SCRIPTS / 'manual_to_script.py'), '--input', args.input, '--project', args.project, '--module', args.module, '--page', args.page, '--feature', args.feature, '--level', args.level])
    elif args.command == 'register':
        run([sys.executable, str(SCRIPTS / 'register_test.py'), '--project', args.project, '--module', args.module, '--page', args.page, '--feature', args.feature, '--level', args.level, '--script-path', args.script_path])
    elif args.command == 'build-catalog':
        run([sys.executable, str(SCRIPTS / 'build_test_catalog.py')])
    elif args.command == 'init-project':
        cmd_init_project(args)
    elif args.command == 'validate-config':
        cmd_validate_config(args)
    elif args.command == 'scaffold-from-config':
        cmd_scaffold_from_config(args)


if __name__ == '__main__':
    main()
