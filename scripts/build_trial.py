# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown-it-py==4.0.0"]
# ///
"""Render a trial's frozen Markdown under sources/<trial>/ into web/trials/<trial>.json.

Usage: uv run scripts/build_trial.py TRIAL
Open it at http://127.0.0.1:8767/?trial=TRIAL.
"""
from pathlib import Path
import json
import re
import sys
from urllib.parse import urljoin
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
md = MarkdownIt('commonmark', {'html': False}).enable('table')

def render(text, base):
    tokens = md.parse(text)
    for token in tokens:
        for child in token.children or []:
            if child.type == 'link_open':
                child.attrSet('href', urljoin(base, child.attrGet('href') or ''))
                child.attrSet('target', '_blank')
                child.attrSet('rel', 'noopener noreferrer')
    return md.renderer.render(tokens, md.options, {})

trial = sys.argv[1]
if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,80}', trial):
    sys.exit('Trial names use lowercase letters, digits and dashes')
meta = json.loads((ROOT / 'sources' / trial / 'manifest.json').read_text())
projects = []
for project_id, title in meta['projects'].items():
    project = {'id': project_id, 'title': title, 'versions': {}, 'differences': []}
    for arm in ['a', 'b']:
        run = next(r for r in meta['runs'] if r['project'] == project_id and r['arm'] == arm)
        # Result commits exist only in the saved outputs, so links resolve against the starting commit.
        base = f"https://github.com/{run['repository']}/blob/{run['base_commit']}/"
        docs = {}
        for doc in run['docs']:
            original = (ROOT / 'sources' / trial / run['id'] / doc['file']).read_text()
            body = re.sub(r'^# [^\n]+\n+', '', original, count=1)
            url = urljoin(base, doc['path'])
            docs[doc['id']] = {'label': doc['label'], 'url': '', 'html': render(body, url),
                               'opening': render(body.split('\n## ', 1)[0], url)}
        project['versions'][arm] = {'label': arm.upper(), 'commit': run['result_commit'], 'repo': run['repository'], 'docs': docs}
    projects.append(project)
out = ROOT / 'web' / 'trials' / f'{trial}.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({'id': trial, 'title': meta['title'], 'projects': projects, 'sourceManifest': meta},
                          ensure_ascii=False, indent=2) + '\n')
print(f'Wrote {out.relative_to(ROOT)}')
