#!/usr/bin/env python3
"""Print every configured Quarto HTML page to a checked, linked PDF collection.

Run quarto render first. Requires playwright, PyYAML and pypdf, plus Chromium.
No training jobs or external publication are performed by this script.
"""
import argparse
import asyncio
from datetime import datetime, timezone
import functools
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading

from playwright.async_api import async_playwright
from pypdf import PdfReader
import yaml

ROOT = Path(__file__).resolve().parents[1]
GITHUB = 'https://github.com/ZhuoranYang/scaling-ladder-knowledge/blob/main/'
DEPENDENCIES = json.loads((ROOT/'configs/industry/source-pins.json').read_text())['repositories']
PRINT_CSS = '''
@page { size: A4; }
#quarto-header, #quarto-sidebar, #quarto-margin-sidebar, .quarto-secondary-nav,
.quarto-navigation-tool, .quarto-title-meta, .nav-footer, .code-copy-button,
.anchorjs-link, .quarto-alternate-formats, .quarto-title-breadcrumbs,
.header-section-number { display:none!important; }
html, body { background:white!important; color:#16202b!important; font-size:10pt!important; }
body { line-height:1.45!important; margin:0!important; padding:0!important; }
#quarto-content { display:block!important; padding:0!important; margin:0!important; }
main.content { width:100%!important; max-width:none!important; margin:0!important; padding:0!important; }
.page-columns, .column-body, .column-page { display:block!important; width:100%!important; }
h1 { font-size:22pt!important; } h2 { font-size:16pt!important; }
h3 { font-size:12pt!important; } h4,h5,h6 { font-size:10.5pt!important; }
h1,h2,h3,h4,h5,h6 { break-after:avoid-page; }
p { orphans:3; widows:3; }
a { color:#245a81!important; text-decoration:none!important; }
a[href]:after { content:none!important; }
table { width:100%!important; font-size:8pt!important; table-layout:auto!important; }
th,td { overflow-wrap:anywhere!important; padding:4px!important; }
tr { break-inside:avoid; }
thead { display:table-header-group; }
pre,code { font-size:7.6pt!important; white-space:pre-wrap!important; overflow-wrap:anywhere!important; }
pre, div.sourceCode { overflow:visible!important; max-height:none!important; }
.table-responsive, .cell-output-display { overflow:visible!important; }
img,svg { max-width:100%!important; height:auto; }
figure,.mermaid,.mermaid-js { break-inside:avoid; }
.math.display { overflow:visible!important; }
.quarto-title-block { margin-bottom:1.5em!important; }
'''


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def sources():
    config = yaml.safe_load((ROOT/'_quarto.yml').read_text())
    return list(dict.fromkeys(p for pattern in config['project']['render']
                             for p in sorted(ROOT.glob(pattern))))


async def render_one(browser, source, base_url, semaphore):
    async with semaphore:
        relative = source.relative_to(ROOT)
        html = relative.with_suffix('.html')
        target = ROOT/'pdf'/relative.with_suffix('.pdf')
        if not (ROOT/'_site'/html).is_file():
            raise FileNotFoundError(f'Render Quarto first: {html}')
        expected_diagrams = (ROOT/'_site'/html).read_text().count('<pre class="mermaid')
        page = await browser.new_page(viewport={'width':1440, 'height':1000},
                                      device_scale_factor=1, ignore_https_errors=True)
        try:
            await page.goto(f'{base_url}/{html.as_posix()}', wait_until='load', timeout=90000)
            await page.evaluate('''async () => {
              document.querySelectorAll('img').forEach(i => i.loading='eager');
              await document.fonts.ready;
              await Promise.all(Array.from(document.images).map(i => i.complete ? Promise.resolve() :
                new Promise(resolve => {i.onload=resolve; i.onerror=resolve;})));
            }''')
            math_count = await page.locator('.math').count()
            if math_count:
                await page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.promise', timeout=45000)
                await page.evaluate('async () => { await MathJax.startup.promise; await MathJax.typesetPromise(); }')
                if not await page.locator('mjx-container').count():
                    raise RuntimeError(f'MathJax did not render: {relative}')
                if await page.locator('mjx-merror, [data-mjx-error]').count():
                    raise RuntimeError(f'MathJax error: {relative}')
            if expected_diagrams:
                await page.wait_for_function("n => document.querySelectorAll('svg.mermaid-js').length===n", arg=expected_diagrams, timeout=45000)
            diagram_count = await page.locator('svg.mermaid-js').count()
            broken = await page.evaluate("Array.from(document.images).filter(i => !i.complete || i.naturalWidth===0).map(i=>i.src)")
            if broken:
                raise RuntimeError(f'Broken figures in {relative}: {broken}')
            title = await page.locator('h1').first.inner_text()
            columns = await page.evaluate("Math.max(0,...Array.from(document.querySelectorAll('table tr')).map(r=>r.children.length))")
            # Preserve readable dense configuration tables without shrinking every prose page.
            landscape = columns >= 8
            await page.add_style_tag(content=PRINT_CSS.replace('@page { size: A4; }', '@page { size: A4 landscape; }' if landscape else '@page { size: A4; }'))
            # Quarto's diagram SVGs can be much taller than a physical page.
            # Set both dimensions from the viewBox so Chromium keeps one vector
            # diagram together instead of splitting/clipping it across pages.
            await page.evaluate('''({maxWidth,maxHeight}) => {
              document.querySelectorAll('svg.mermaid-js').forEach(svg => {
                const box=svg.viewBox.baseVal;
                const factor=Math.min(maxWidth/box.width,maxHeight/box.height);
                svg.style.setProperty('width',`${box.width*factor}px`,'important');
                svg.style.setProperty('height',`${box.height*factor}px`,'important');
                svg.style.setProperty('display','block','important');
                svg.style.setProperty('margin','0 auto','important');
              });
              document.querySelectorAll('img').forEach(img => {
                img.style.setProperty('max-height',`${maxHeight}px`,'important');
                img.style.setProperty('object-fit','contain','important');
              });
            }''', {'maxWidth':(271 if landscape else 184)*96/25.4,
                   'maxHeight':(150 if landscape else 230)*96/25.4})
            await page.evaluate('''({root, github, dependencies}) => {
              document.querySelectorAll('a[href]').forEach(a => {
                const href=a.getAttribute('href'); if(href.startsWith('#')) return;
                const u=new URL(href, location.href); if(u.origin!==root) return;
                const path=decodeURIComponent(u.pathname).replace(/^\\//,'');
                const dependency=dependencies.find(d => path.startsWith(d.checkout+'/'));
                if(dependency) {
                  a.href=dependency.repository+'/blob/'+dependency.revision+'/'+path.slice(dependency.checkout.length+1)+u.hash;
                  return;
                }
                a.href=github+(path.endsWith('.html') ? 'pdf/'+path.replace(/\\.html$/,'.pdf') : path)+u.hash;
              });
            }''', {'root':base_url, 'github':GITHUB, 'dependencies':DEPENDENCIES})
            await page.emulate_media(media='print')
            target.parent.mkdir(parents=True, exist_ok=True)
            await page.pdf(path=str(target), format='A4', landscape=landscape,
                           print_background=True, prefer_css_page_size=True,
                           margin={'top':'16mm','bottom':'17mm','left':'13mm','right':'13mm'},
                           display_header_footer=True, header_template='<span></span>',
                           footer_template='<div style="font-size:8px;color:#666;width:100%;text-align:center">Scaling Ladder Knowledge · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                           tagged=True, outline=True)
            pdf = PdfReader(target)
            text = ''.join(p.extract_text() or '' for p in pdf.pages)
            if len(text.strip()) < 80:
                raise RuntimeError(f'Empty or image-only PDF: {relative}')
            result = {'title':title,'source':relative.as_posix(),
                      'pdf':target.relative_to(ROOT).as_posix(),'pages':len(pdf.pages),
                      'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                      'math_elements':math_count,'mermaid_diagrams':diagram_count,
                      'landscape':landscape}
            print(f"OK {result['pdf']} ({result['pages']} pages)", flush=True)
            return result
        finally:
            await page.close()


def write_index(records):
    lines = ['# Read the rendered PDFs', '',
             'These PDFs are printed from the Quarto HTML pages, including rendered equations, figures and flowcharts. Click a title to open GitHub’s PDF viewer; use **Download raw file** to save it.', '',
             '**Suggested starting points:** [Jiaxuan reading guide](doc/reading/jiaxuan-reading-guide.pdf), [Marin data pipeline](doc/data/marin-artifact-lineage.pdf), [Marin evaluation](doc/evaluation/marin-evaluation.pdf), [mid/post-training](doc/training/marin-midtraining-posttraining.pdf), and [96-H100 plan](doc/plans/plan-96-h100.pdf).', '',
             f"**{len(records)} documents · {sum(r['pages'] for r in records)} PDF pages.** Each PDF mirrors its source path. Dense tables use landscape pages. Source files and the original references remain in the main repository.", '',
             '| Document | PDF pages | Editable source |', '|---|---:|---|']
    for r in records:
        lines.append(f"| [{r['title'].replace('|','/')}](<{r['pdf'][4:]}>) | {r['pages']} | [Source](<../{r['source']}>) |")
    lines += ['', '## Regenerate', '', 'Install Quarto and the Python/browser dependencies, then run from the repository root:', '',
              '```bash', 'python -m venv tmp/pdf-tools', 'tmp/pdf-tools/bin/pip install -r scripts/requirements-pdf.txt',
              'PLAYWRIGHT_BROWSERS_PATH="$PWD/tmp/pdf-browser" tmp/pdf-tools/bin/python -m playwright install --with-deps chromium --only-shell',
              'quarto render', 'PLAYWRIGHT_BROWSERS_PATH="$PWD/tmp/pdf-browser" tmp/pdf-tools/bin/python scripts/render_pdfs.py', '```', '',
              'The exporter checks that equations, diagrams and figures render, verifies readable PDF text, and records page counts and SHA-256 hashes in [manifest.json](manifest.json). Internet access is needed for the HTML’s MathJax and web-font resources. No model weights or training text are downloaded.', '']
    (ROOT/'pdf/README.md').write_text('\n'.join(lines))


async def main(args):
    selected = sources()
    if args.only:
        selected = [s for s in selected if s.relative_to(ROOT).as_posix() in args.only]
        if not selected:
            raise ValueError('No matching source pages')
    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT/'_site')))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            try:
                semaphore = asyncio.Semaphore(args.workers)
                records = await asyncio.gather(*(render_one(browser,s,f'http://127.0.0.1:{server.server_port}',semaphore) for s in selected))
            finally:
                await browser.close()
        if not args.only:
            manifest = {'generated_at':datetime.now(timezone.utc).isoformat(), 'renderer':'Playwright Chromium print-to-PDF',
                        'documents':records,'document_count':len(records),'page_count':sum(r['pages'] for r in records)}
            (ROOT/'pdf/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
            write_index(records)
        print(f"Rendered {len(records)} PDFs",flush=True)
    finally:
        server.shutdown()


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only',action='append',help='One source path, relative to repo root; repeatable')
    parser.add_argument('--workers',type=int,default=3)
    asyncio.run(main(parser.parse_args()))
