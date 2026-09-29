# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown-it-py==4.0.0"]
# ///
"""Render frozen Markdown snapshots for the review interface."""
from pathlib import Path
import json
import re
from urllib.parse import urljoin
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
md = MarkdownIt('commonmark', {'html': False}).enable('table')
meta = json.loads((ROOT / 'sources/manifest.json').read_text())

def render(text, url):
    tokens = md.parse(text)
    for token in tokens:
        for child in token.children or []:
            if child.type == 'link_open':
                href = child.attrGet('href') or ''
                child.attrSet('href', urljoin(url, href))
                child.attrSet('target', '_blank')
                child.attrSet('rel', 'noopener noreferrer')
    return md.renderer.render(tokens, md.options, {})

def para(text, needle):
    blocks = text.split('\n\n')
    matches = [b for b in blocks if needle in b]
    if not matches:
        raise ValueError(f'Missing quote: {needle}')
    return matches[0]

projects = []
for case, title in [('morning','Morning reader'),('writing','Writing checks')]:
    project = {'id': case, 'title': title, 'versions': {}, 'differences': []}
    texts = {}
    for arm in ['a','b']:
        run = next(r for r in meta['runs'] if r['id'] == case + '-' + arm)
        v = {'label': arm.upper(), 'commit': run['result_commit'], 'repo': run['repository'], 'docs': {}}
        for path in sorted((ROOT / 'sources' / (case + '-' + arm)).glob('*.md')):
            name = path.stem
            original = path.read_text()
            body = re.sub(r'^# [^\n]+\n+', '', original, count=1)
            github_path = 'README.md' if name == 'readme' else 'docs/setup.md'
            url = f"https://github.com/{run['repository']}/blob/{run['result_commit']}/{github_path}"
            v['docs'][name] = {'label': 'README' if name == 'readme' else 'Setup guide', 'url': url, 'html': render(body,url), 'opening': render(body.split('\n## ',1)[0],url)}
            texts[(arm,name)] = body
        project['versions'][arm] = v
    def add(id,title,question,a,b):
        item={'id':id,'title':title,'question':question,'evidence':{}}
        for arm,spec in [('a',a),('b',b)]:
            doc, needles = spec
            text='\n\n'.join(para(texts[(arm,doc)],n) for n in needles)
            url=project['versions'][arm]['docs'][doc]['url']
            item['evidence'][arm]={'doc':doc,'html':render(text,url) if text else '<p class="absence">No corresponding passage in this README.</p>','url':url}
        project['differences'].append(item)
    if case == 'morning':
        add('cost','Cost guidance','Which cost guidance would you keep?',('readme',['As checked on 2026-09-29']),('readme',['The configured model is']))
        add('first-step','Before paying for API access','Which starting path would you keep?',('setup',['Start with the build before paying']),('readme',['Create your local configuration']))
        add('limits','Reading and feed limits','Which explanation of the limits would you keep?',('readme',['Passages aim for 5–15']),('readme',['Preparation normally aims','Background checks are scheduled']))
        add('recovery','Recovering a failed transfer','Which recovery instruction would you keep?',('setup',['A pack was written but pushing failed']),('readme',['A pack was built but transfer failed']))
        add('verification','What was verified','Which verification note would you keep?',('setup',['Documentation review on 2026-09-29']),('readme',[]))
    else:
        add('example','Concrete example','Which example would you keep?',('readme',['For example, the bundled sentence','L6 [19]']),('readme',['For example, find guides']))
        add('scores','Explaining the result','Which explanation of the scores would you keep?',('readme',['**Exit code 1 is expected']),('readme',['[Save a draft]','This writes `scripts/explorer.local.html`']))
        add('privacy','Sharing a generated report','Which sharing guidance would you keep?',('readme',['Generated pages embed']),('readme',['The generated `scripts/explorer.local.html`']))
        add('verification','Tests and evidence','Which account of verification would you keep?',('readme',['The 14 automated tests']),('readme',['The tests cover rule behavior']))
    projects.append(project)
(ROOT/'web/data.json').write_text(json.dumps({'id':'prepare-to-share-2026-09-29','projects':projects,'sourceManifest':meta},ensure_ascii=False,indent=2)+'\n')
