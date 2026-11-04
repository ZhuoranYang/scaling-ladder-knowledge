"""Preserve GitHub-style section links when Quarto strips numeric heading prefixes.

Only inserts explicit HTML aliases; imported prose, headings, math and figures stay intact.
"""
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'doc/reading/scientific-scaling-ladder.md'
text = path.read_text()
count = 0


def add_alias(match):
    global count
    heading = match.group(0)
    title = re.sub(r'^#+\s+', '', heading)
    if not re.match(r'(?:\d|A\.|Appendix A\.)', title):
        return heading
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'\s+', '-', slug)
    if f'id="{slug}"' in text:
        return heading
    count += 1
    return f'<!-- Local Quarto navigation alias; imported heading unchanged. -->\n<span id="{slug}"></span>\n\n{heading}'


updated = re.sub(r'^#{2,6} .+$', add_alias, text, flags=re.MULTILINE)
path.write_text(updated)
print(f'Added {count} navigation aliases; imported prose preserved.')
