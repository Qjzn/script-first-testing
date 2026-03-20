#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path('/home/mifu/openclaw-data')
TESTS_ROOT = ROOT / 'tests' / 'projects'
INDEX_PATH = ROOT / 'tests' / 'TEST_INDEX.md'
CATALOG_PATH = ROOT / 'tests' / 'TEST_CATALOG.json'


def locate(project: str, module: str, page: str, feature: str | None):
    base = TESTS_ROOT / project / module / page
    if not base.exists():
        return None, []
    candidates = sorted(x for x in base.glob('*.py') if x.name != '__init__.py')
    if feature:
        exact = base / f'{feature}.py'
        if exact.exists():
            return exact, candidates
    smoke = base / 'smoke.py'
    if smoke.exists():
        return smoke, candidates
    return (candidates[0] if candidates else None), candidates


def search_catalog(project: str, module: str, page: str, feature: str | None, keyword: str | None):
    if not CATALOG_PATH.exists():
        return []
    data = json.loads(CATALOG_PATH.read_text(encoding='utf-8'))
    hits = []
    for item in data:
        if project and item.get('project') != project:
            continue
        if module and item.get('module') != module:
            continue
        if page and item.get('page') != page:
            continue
        hay = ' '.join([
            item.get('feature', ''),
            item.get('summary', ''),
            item.get('capability', ''),
            item.get('entry', ''),
            ' '.join(item.get('tags', [])),
            ' '.join(item.get('assertion_type', []))
        ]).lower()
        score = 0
        if feature and feature.lower() in hay:
            score += 10
        if keyword and keyword.lower() in hay:
            score += 10
        if feature and item.get('feature', '').lower() == feature.lower():
            score += 20
        if keyword and keyword.lower() == item.get('feature', '').lower():
            score += 20
        if item.get('feature') == 'smoke':
            score -= 5
        if item.get('status') == 'todo' or str(item.get('feature', '')).startswith('manual-'):
            score -= 20
        if keyword and keyword.lower() in item.get('capability', '').lower():
            score += 15
        if feature and feature.lower() in item.get('capability', '').lower():
            score += 15
        if score > 0:
            item = dict(item)
            item['_score'] = score
            hits.append(item)
    hits.sort(key=lambda x: x.get('_score', 0), reverse=True)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', required=True)
    ap.add_argument('--module', required=True)
    ap.add_argument('--page', required=True)
    ap.add_argument('--feature')
    ap.add_argument('--keyword')
    args = ap.parse_args()

    script, candidates = locate(args.project, args.module, args.page, args.feature)
    index_text = INDEX_PATH.read_text(encoding='utf-8') if INDEX_PATH.exists() else ''
    catalog_hits = search_catalog(args.project, args.module, args.page, args.feature, args.keyword)
    preferred = script
    if (args.keyword or args.feature) and catalog_hits:
        preferred = Path(catalog_hits[0]['script_path'])
    result = {
        'project': args.project,
        'module': args.module,
        'page': args.page,
        'feature': args.feature,
        'keyword': args.keyword,
        'script_found': bool(preferred),
        'script_path': str(preferred) if preferred else None,
        'candidate_scripts': [str(x) for x in candidates],
        'catalog_hits': catalog_hits,
        'index_exists': INDEX_PATH.exists(),
        'index_has_project': f'## {args.project}' in index_text,
        'suggestions': []
    }

    if not script and not catalog_hits:
        result['suggestions'] = [
            '先执行真实测试，梳理结构化步骤',
            '再运行 scaffold_test.py 生成模板',
            '补充真实自动化步骤后，用 register_test.py 登记索引'
        ]
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
