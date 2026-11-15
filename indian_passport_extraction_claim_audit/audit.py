"""Read-only documentation and AST analysis."""
import ast
import os
from pathlib import Path
import re
from .phrases import INDIANPASSPORTEXTRACTION, NOINDIANPASSPORTEXTRACTION, GENERIC_NAMES


def normalize(text):
    return ' '.join(text.lower().replace('’', "'").replace("n't", ' not').replace('-', ' ').split())


def prose(text):
    fence = None
    lines = []
    for line in text.splitlines():
        match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
            lines.append('')
        elif match:
            fence = match[1]
            lines.append('')
        else:
            lines.append(line)
    return '\n'.join(lines)


def matches(text, phrases):
    pattern = r'\b(?:' + '|'.join(re.escape(x) for x in sorted(phrases, key=lambda x: (-len(x), x))) + r')\b'
    return list(re.finditer(pattern, text))


def claims_in(text, path):
    result = []
    for paragraph in re.split(r'\n\s*\n', prose(text)):
        normalized = normalize(paragraph)
        denials = matches(normalized, NOINDIANPASSPORTEXTRACTION)
        masked = list(normalized)
        for m in denials:
            masked[m.start():m.end()] = ' ' * (m.end()-m.start())
        for family, found in [('NOINDIANPASSPORTEXTRACTION', denials), ('INDIANPASSPORTEXTRACTION', matches(''.join(masked), INDIANPASSPORTEXTRACTION))]:
            result.extend(dict(family=family, phrase=m[0], path=path) for m in found)
    return result


def module_evidence(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    aliases, bound, definitions = {}, set(), set()
    imported_mindee = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                aliases[a.asname or a.name.split('.')[0]] = a.name if a.asname else a.name.split('.')[0]
                imported_mindee |= a.name.split('.')[0] == 'mindee'
        elif isinstance(node, ast.ImportFrom):
            imported_mindee |= (node.module or '').split('.')[0] == 'mindee'
            for a in node.names:
                aliases[a.asname or a.name] = (node.module or '') + '.' + a.name
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.With, ast.AsyncWith)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else [i.optional_vars for i in node.items if i.optional_vars]
            for target in targets:
                bound.update(n.id for n in ast.walk(target) if isinstance(n, ast.Name))
    shadow = bound | definitions

    def clear(node):
        if isinstance(node, ast.Name):
            return node.id not in definitions and not (node.id in bound and (node.id in aliases or node.id in {'mindee', 'IndianPassportV1'}))
        if isinstance(node, ast.Attribute):
            return node.attr not in definitions and clear(node.value)
        # A call result is a legitimate base, including Client().parse().
        return True

    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    generic = []
    client = False
    parses = []
    for call in calls:
        f = call.func
        if isinstance(f, ast.Name) and clear(f):
            resolved = aliases.get(f.id, '')
            if resolved.rsplit('.', 1)[-1] in GENERIC_NAMES and resolved:
                generic.append(('generic', call.lineno))
            if resolved == 'mindee.Client':
                client = True
        elif isinstance(f, ast.Attribute):
            if f.attr in GENERIC_NAMES and clear(f):
                generic.append(('generic', call.lineno))
            if f.attr == 'Client' and isinstance(f.value, ast.Name) and f.value.id == 'mindee' and clear(f):
                client = True
            if f.attr == 'parse' and clear(f):
                args = call.args + [k.value for k in call.keywords]
                if any(((isinstance(a, ast.Name) and a.id == 'IndianPassportV1') or (isinstance(a, ast.Attribute) and a.attr == 'IndianPassportV1')) and clear(a) for a in args):
                    parses.append(('mindee', call.lineno))
    return generic + (parses if imported_mindee and client else [])


def audit(root='.', ignore=()):
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise OSError('repository must be a non-symlink directory')
    claims, evidence, sources = [], [], []
    prefixes = [str(x).replace('\\', '/').rstrip('/') for x in ignore]
    def ignored(rel):
        return any(rel == p or rel.startswith(p + '/') for p in prefixes)
    def walk_error(error):
        raise error
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        dirs[:] = sorted(d for d in dirs if not (Path(directory)/d).is_symlink() and not ignored((Path(directory)/d).relative_to(root).as_posix()))
        for name in sorted(files):
            path = Path(directory)/name
            rel = path.relative_to(root)
            label = rel.as_posix()
            if path.is_symlink() or ignored(label):
                continue
            doc = label == 'README.md' or (path.suffix == '.md' and 'docs' in rel.parts[:-1])
            if doc:
                claims.extend(claims_in(path.read_text(encoding='utf-8'), label))
            if path.suffix != '.py':
                continue
            sources.append(label)
            if set(rel.parts[:-1]) & {'fixtures', 'docs', 'examples'}:
                continue
            test = 'tests' in rel.parts[:-1] or name.startswith('test_') or name.endswith('_test.py')
            for route, line in module_evidence(path.read_text(encoding='utf-8')):
                evidence.append(dict(path=label, line=line, route=route, test=test))
    production = any(not e['test'] for e in evidence)
    findings = []
    for family, rule in [('INDIANPASSPORTEXTRACTION', 'documented-indian-passport-extraction-claim-false'), ('NOINDIANPASSPORTEXTRACTION', 'documented-no-indian-passport-extraction-claim-false')]:
        selected = [c for c in claims if c['family'] == family]
        if selected and ((family == 'INDIANPASSPORTEXTRACTION' and not production) or (family == 'NOINDIANPASSPORTEXTRACTION' and production)):
            severity = 'MEDIUM' if family == 'INDIANPASSPORTEXTRACTION' and evidence else 'HIGH'
            findings.append(dict(rule=rule, severity=severity, message='Documented claim contradicts static source evidence.', claims=selected))
    return dict(verdict='FAIL' if findings else 'PASS', findings=findings, claims=claims, evidence=evidence, source_files=sources)
