#!/usr/bin/env python3
"""Generate navigation, counts and declared input compatibility; --check never writes."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def block(text,name,body):
    start=f'<!-- BEGIN {name} -->';end=f'<!-- END {name} -->'
    replacement=start+'\n'+body+'\n'+end
    if start in text:return re.sub(re.escape(start)+'.*?'+re.escape(end),lambda m:replacement,text,flags=re.S)
    return text.split('\n',1)[0]+'\n\n'+replacement+'\n'+text.split('\n',1)[1]
def outputs():
    cat=read('data/catalog.json');exp=read('data/prompts.json');assets=read('assets/manifest.json')['assets'];loc=read('data/readme-locales.json')['versions']
    n=len(exp['core'])+len(exp['localized']);packs=len(cat['packs'])+1
    out={};access=[]
    exceptions={'P015':2,'P023':2,'P058':3,'P082':2,'P085':2}
    for r in exp['core']+exp['localized']:
        prompts=r['prompt'] if isinstance(r['prompt'],dict) else {r['language']:r['prompt']}
        refs=exceptions.get(r['id'],1 if r.get('mode')=='edit' else 0)
        flags=[]
        if refs>1:flags.append('Multiple references / 多图输入')
        if r['id'] in ['P024','P083']:flags.append('Verify transparent output / 需核对透明输出')
        lengths={k:len(v) for k,v in prompts.items()}
        for lang,size in lengths.items():
            if size>2000:flags.append(f'{lang}: {size} characters; exceeds 2000 / 超出字数限制')
        access.append(dict(id=r['id'],references=refs,prompt_characters=lengths,checks=flags,status='needs-check' if flags else 'within-declared-input-limits',platform_tested=False))
    out['data/recipe-access.json']=json.dumps({'checked':'2026-09-21','basis':'Free page DOM: one reference, 2000-character textarea. Input fit is not a successful generation test.','recipes':access},ensure_ascii=False,indent=2)+'\n'
    lines=['# Recipe input guide · 配方输入说明','','[Free Flyne tool](https://flyne.ai/free-gpt-image-2-5/) · [Access and test records](flyne-access.md)','','Checked 2026-09-21: one reference image and 2,000 characters per submission. Entries below describe input requirements, not verified generation quality. Several-reference recipes need another compatible tool. Transparent output needs a separate check.','','免费入口最多一张参考图、提示词最多 2,000 字符。符合输入限制不等于已实测成功。不要直接截断长提示词；应先精简并保留必需条件。','','| Recipe | Reference images / 参考图 | Input check / 输入检查 |','| --- | --- | --- |']
    byid={r['id']:r for r in exp['core']}
    for a in access:
        slug=byid.get(a['id'],{}).get('pack','11-multilingual')
        status='; '.join(a['checks']) or 'Within declared limits; not tested / 符合已公布输入限制，未实测'
        lines.append(f'| [{a["id"]}](../prompts/{slug}.md#{a["id"].lower()}) | {a["references"]} | {status} |')
    out['docs/recipe-access.md']='\n'.join(lines)+'\n'
    ctas=read('data/entry-copy.json')
    for v in loc:
        path=v['path'];text=(ROOT/path).read_text();copy=ctas[v['locale']]
        body=f'**[{copy["cta"]}](https://flyne.ai/free-gpt-image-2-5/)**\n\n'+copy['limits']+' [→](docs/flyne-access.md)\n\n'+copy['stats'].format(total=n,packs=packs,images=len(assets),bilingual=sum('zh' in r['brief'] for r in exp['core']),english=sum('zh' not in r['brief'] for r in exp['core']),localized=len(exp['localized']))
        text=block(text,'FLYNE ENTRY',body)
        if v['locale'] in ['en','zh-Hans']:
            zh=v['locale']=='zh-Hans';rows=['| 场景包 | 数量 |' if zh else '| Collection | Recipes |','| --- | --- |']
            allpacks=[(p['slug'],p['title']['zh' if zh else 'en'],len(p['recipes'])) for p in cat['packs']]+[('11-multilingual','多语言配方' if zh else 'Multilingual recipes',len(exp['localized']))]
            for slug,title,count in sorted(allpacks):rows.append(f'| [{title}](prompts/{slug}.md) | {count} |')
            body='\n'.join(rows)
            if '<!-- BEGIN PACK TABLE -->' not in text:
                heading='## 按实际工作选场景' if zh else '## Prompt library'
                if heading not in text: raise ValueError(heading)
                start=text.index('|',text.index(heading));end=text.find('\n\n',start)
                text=text[:start]+'<!-- BEGIN PACK TABLE -->\n'+body+'\n<!-- END PACK TABLE -->'+text[end:]
            else:text=block(text,'PACK TABLE',body)
        out[path]=text
    return out

def check_assets():
    rows=read('assets/previews.json')['previews'];assets=read('assets/manifest.json')['assets']
    assert {r['source'] for r in rows}=={a['path'] for a in assets},'Preview coverage mismatch'
    assert len(rows)==len({r['path'] for r in rows}), 'Duplicate previews'
    assert {r['path'] for r in rows}=={str(p.relative_to(ROOT)) for p in (ROOT/'assets/previews').glob('*.jpg')},'Unrecorded preview'
    for r in rows:
        assert hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest()==r['source_sha256'],'Stale preview source'
        data=(ROOT/r['path']).read_bytes()
        assert data[:2]==b'\xff\xd8' and len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'],'Invalid preview'
        assert max(r['width'],r['height'])<=720,'Oversized preview'

def main():
    check='--check' in sys.argv
    for path,content in outputs().items():
        if check:assert (ROOT/path).read_text()==content,f'Stale generated section: {path}'
        else:(ROOT/path).write_text(content)
    check_assets()
    print('PASS: generated entry pages, complete pack tables, input requirements and preview integrity')
if __name__=='__main__':main()
