#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path('/home/mifu/openclaw-data')
TESTS_ROOT = ROOT / 'tests' / 'projects'
CATALOG_PATH = ROOT / 'tests' / 'TEST_CATALOG.json'


def infer_tags(path: Path, text: str):
    tags = set()
    whole = f'{path.as_posix().lower()}\n{text.lower()}'
    for token in ['upload', 'cover', 'default-cover', 'default', 'course', 'manage', 'learning', 'smoke']:
        if token in whole:
            tags.add(token)
    return sorted(tags)


def infer_capability(feature: str, tags: list[str]):
    f = (feature or '').lower()
    if 'upload' in f or 'upload' in tags:
        return 'upload-cover' if 'cover' in f or 'cover' in tags else 'upload'
    if 'default' in f or 'default-cover' in tags:
        return 'default-cover'
    if 'smoke' in f:
        return 'smoke'
    if 'create' in f and 'course' in f:
        return 'create-course'
    return f or 'unknown'


def infer_entry(text: str, module: str):
    lower = text.lower()
    if '/course/add' in lower:
        return 'learning#/course/add'
    if '/dashboard/course-manage' in lower:
        return 'manage#/dashboard/course-manage'
    return f'{module}#unknown'


def infer_assertion_type(text: str, tags: list[str]):
    lower = text.lower()
    result = []
    if 'url' in lower or 'route' in lower or '/dashboard/' in lower or '/course/add' in lower:
        result.append('route')
    if 'imgcount' in lower or 'dialog' in lower or 'queryselector' in lower:
        result.append('dom')
    if 'gettoken_200' in lower or 'put_200' in lower or 'geturl_200' in lower:
        result.append('request')
    if 'upload' in tags or 'uploadtriggered' in lower:
        result.append('upload')
    if 'default-cover' in tags or 'dialog' in lower:
        result.append('dialog')
    return sorted(set(result))


def extract_json_fields(text: str):
    fields = {}
    for key in ['project', 'module', 'page', 'feature', 'level', 'summary', 'status', 'capability', 'entry']:
        m = re.search(rf'"{key}"\s*:\s*"([^"]+)"', text)
        if m:
            fields[key] = m.group(1)
    m = re.search(r'"requires_login"\s*:\s*(true|false)', text, re.I)
    if m:
        fields['requires_login'] = m.group(1).lower() == 'true'
    m = re.search(r'"assertion_type"\s*:\s*\[(.*?)\]', text, re.S)
    if m:
        fields['assertion_type'] = re.findall(r'"([^"]+)"', m.group(1))
    return fields


def main():
    entries = []
    for path in sorted(TESTS_ROOT.rglob('*.py')):
        if path.name == '__init__.py':
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        fields = extract_json_fields(text)
        rel = path.relative_to(ROOT)
        parts = rel.parts
        project = fields.get('project') or (parts[2] if len(parts) > 2 else '')
        module = fields.get('module') or (parts[3] if len(parts) > 3 else '')
        page = fields.get('page') or (parts[4] if len(parts) > 4 else '')
        feature = fields.get('feature') or path.stem
        summary = fields.get('summary') or ''
        tags = infer_tags(path, text)
        entries.append({
            'script_path': str(path),
            'project': project,
            'module': module,
            'page': page,
            'feature': feature,
            'summary': summary,
            'status': fields.get('status', ''),
            'tags': tags,
            'capability': fields.get('capability') or infer_capability(feature, tags),
            'entry': fields.get('entry') or infer_entry(text, module),
            'requires_login': fields.get('requires_login') if 'requires_login' in fields else ('15212120027' in text or 'a1111111' in text or '登录' in text),
            'assertion_type': fields.get('assertion_type') or infer_assertion_type(text, tags),
        })
    CATALOG_PATH.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': 'ok', 'catalog_path': str(CATALOG_PATH), 'count': len(entries)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
