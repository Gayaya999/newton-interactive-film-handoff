"""Run with Python 3, from any directory. Verifies handoff integrity, not gameplay."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def verify():
    root = Path(__file__).resolve().parent.parent
    manifest = json.loads((root / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    errors = []
    declared = set()
    for entry in manifest['files']:
        relative = PurePosixPath(entry['path'])
        if relative.is_absolute() or '..' in relative.parts or entry['path'] in declared:
            errors.append('Invalid or duplicate path: ' + entry['path'])
            continue
        declared.add(entry['path'])
        path = root.joinpath(*relative.parts)
        if not path.is_file() or path.is_symlink():
            errors.append('Missing/invalid file: ' + entry['path'])
        elif path.stat().st_size != entry['bytes'] or sha256(path) != entry['sha256']:
            errors.append('Changed file: ' + entry['path'])
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
              if p.is_file() and p.name != 'PACKAGE_MANIFEST.json'
              and p.name != '.DS_Store' and '__pycache__' not in p.parts}
    errors.extend('Unlisted file: ' + p for p in sorted(actual - declared))
    edits = json.loads((root / 'content/edit-list.json').read_text(encoding='utf-8'))
    graph = json.loads((root / 'content/story-graph.json').read_text(encoding='utf-8'))
    ids = {item['id'] for item in edits['clips']}
    required_ids = {'opening','orbit','moon-question','research','distance','confirmation',
                    'reciprocal-explanation','ending','low','high','accept','relation-question',
                    'oneway-feedback','mutual-feedback'}
    if ids != required_ids or len(edits['clips']) != 14:
        errors.append('Expected 14 specific movie cuts.')
    for item in edits['clips']:
        path = root / item['path']
        if not path.is_file() or sha256(path) != item['sha256']:
            errors.append('Cut provenance mismatch: ' + item['id'])
        if item['end'] <= item['start']:
            errors.append('Invalid cut range: ' + item['id'])
    for key,item in edits['sources'].items():
        path = root / item['path']
        if not path.is_file() or sha256(path) != item['sha256']:
            errors.append('Original provenance mismatch: ' + key)
    for node_id, node in graph['nodes'].items():
        targets = list(node.get('choices',{}).values())
        targets += [node[k] for k in ['on_ended','on_start','on_retry','on_valid_commit','on_restart'] if k in node]
        for target in targets:
            if target not in graph['nodes']:
                errors.append(f'Unknown transition: {node_id} -> {target}')
        if node.get('kind') == 'video' and node.get('media') not in ids:
            errors.append('Missing video node media: ' + node_id)
    for name in ['00_先读这里.md','01_交给Claude的完整提示词.md','02_美术排版与UI设计方案.md',
                 '03_剧情交互与小游戏.md','04_动效与声音设计.md','05_实现计划与验收.md','06_镜头剪辑与科学修正.md',
                 'design/index.html','content/asset-index.json']:
        if not (root/name).is_file():
            errors.append('Missing promised document: ' + name)
    if manifest['file_count'] != len(declared):
        errors.append('Manifest file_count mismatch.')
    if errors:
        print(json.dumps({'status':'FAIL','errors':errors},ensure_ascii=False,indent=2))
        return 1
    print(json.dumps({'status':'PASS','checked_files':len(declared),'video_cuts':14,
                      'original_videos':len(edits['sources']),'scope':'handoff integrity and graph references; not final game validation'},ensure_ascii=False,indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(verify())
