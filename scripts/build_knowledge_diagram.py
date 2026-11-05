"""Build the static wiki navigation SVG using the installed Quarto Mermaid runtime."""
import asyncio
import hashlib
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]


async def main():
    source=ROOT/'wiki/assets/pretraining-workflow.mmd'
    runtime=ROOT/'_site/site_libs/quarto-diagram/mermaid.min.js'
    target=source.with_suffix('.svg')
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        try:
            page=await browser.new_page()
            await page.set_content('<html><body></body></html>')
            await page.add_script_tag(path=str(runtime))
            svg=await page.evaluate('''async text => {
              mermaid.initialize({startOnLoad:false,theme:'neutral',fontFamily:'Arial',flowchart:{htmlLabels:false}});
              return (await mermaid.render('pretraining-workflow',text)).svg;
            }''',source.read_text())
            target.write_text(svg+'\n')
        finally:
            await browser.close()
    files=[source,runtime,target]
    receipt={'mode':'derived navigation figure; not a measured training result',
             'generator':'scripts/build_knowledge_diagram.py',
             'files':[{'path':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]}
    (ROOT/'knowledge/diagram-provenance.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(target.relative_to(ROOT))


if __name__=='__main__':asyncio.run(main())
