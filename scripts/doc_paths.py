"""Resolve historical documentation paths and rewrite local links after the folder move."""
from pathlib import Path
import json,re,os
ROOT=Path(__file__).resolve().parents[1]
MAP_PATH=ROOT/'doc/path-migration.json'
def mapping():return json.loads(MAP_PATH.read_text())['moves']
def target(ref,old_source,new_source):
 if not ref or ref.startswith(('#','/')) or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',ref):return ref
 angled=ref.startswith('<') and ref.endswith('>');raw=ref[1:-1] if angled else ref
 path,mark,frag=raw.partition('#')
 if not path:return ref
 old=(Path(old_source).parent/path).resolve()
 try:key=old.relative_to(ROOT).as_posix()
 except ValueError:return ref
 new_key=mapping().get(key,key);dst=ROOT/new_key
 if key==new_key and not dst.exists():return ref
 result=os.path.relpath(dst,Path(new_source).parent).replace(os.sep,'/')
 if path.endswith('/') and not result.endswith('/'):result+='/'
 result+=mark+frag
 return '<'+result+'>' if angled else result

def rewrite(text,old_source,new_source):
 # Markdown destinations (including images), HTML asset/link attrs, Quarto includes.
 text=re.sub(r'(\]\()([^\n)]*)(\))',lambda m:m[1]+target(m[2],old_source,new_source)+m[3],text)
 text=re.sub(r'''((?:src|href)=["'])([^"']+)(["'])''',lambda m:m[1]+target(m[2],old_source,new_source)+m[3],text)
 text=re.sub(r'(\{\{< include\s+)(\S+)(\s*>\}\})',lambda m:m[1]+target(m[2],old_source,new_source)+m[3],text)
 return text

def full_paths(text):
 for old,new in sorted(mapping().items(),key=lambda kv:-len(kv[0])):text=text.replace(old,new)
 return text
