"""Refresh the public content evidence and original practice imagery."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import urlopen, Request
from concurrent.futures import ThreadPoolExecutor
import json, re, io
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/sources'
ASSETS = ROOT / 'dist/assets'
SOURCE.mkdir(parents=True, exist_ok=True)
class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.images=[]; self.text=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('script','style'): self.skip+=1
        if tag=='img': self.images.append(a)
    def handle_endtag(self,tag):
        if tag in ('script','style'): self.skip=max(0,self.skip-1)
    def handle_data(self,data):
        if not self.skip and data.strip(): self.text.append(data.strip())
def fetch(url):
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r: return r.read()
def page(slug):
    url='https://wiltondental.co.uk/'+(slug+'/' if slug!='home' else '')
    raw=fetch(url).decode(); (SOURCE/(slug+'.html')).write_text(raw,encoding='utf-8')
    p=Parser();p.feed(raw)
    (SOURCE/(slug+'.json')).write_text(json.dumps({'url':url,'retrieved':'2026-09-26','images':p.images,'text':p.text},indent=2),encoding='utf-8')
    return slug,p
pages=dict(ThreadPoolExecutor(6).map(page,['home','contact','whitening','imaging','implants','microdermabrasion','dr-wale-towolawi']))
mapping={'white-fillings':'White-Composite','dental-implants':'Dental-Implants','invisible-braces':'Invisalign2','root-canal':'Endo-','dental-hygiene':'i7ym90','wisdom-teeth':'Wisdom-tooth','sedation':'Woman-in-chair','smile-makeovers':'Veneers-','facial-aesthetics':'Derm-Chick','stress-therapy':'Cliquedental-psychology','wale-towolawi':'Dr-Wale','namitha-shibu':'Dr-Namitha','shruti-pawar':'Shruti-1','steffeena-mathews':'Ms-Stef-Mathew-1-r','tinu-oloyede':'Ms-Tinu','sanju-balami':'Sanju-'}
manifest=[]
def asset(entry):
    name,needle=entry
    img=next(i for i in pages['home'].images if needle in i.get('src',''))
    url=img['src']; raw=fetch(url); im=Image.open(io.BytesIO(raw)); im.thumbnail((1000,1000)); dest=ASSETS/(name+'.webp'); im.save(dest,'WEBP',quality=88)
    return {'file':dest.relative_to(ROOT).as_posix(),'source':url,'sourcePage':'https://wiltondental.co.uk/','size':list(im.size),'rights':'Existing practice website asset; retained for redesign review. Practice to confirm publication rights.'}
manifest=list(ThreadPoolExecutor(8).map(asset,mapping.items()))
logo=next(i for i in pages['home'].images if 'custom-logo' in i.get('class',''))
url=logo['srcset'].split(',')[-1].strip().split(' ')[0]
(ASSETS/'wilton-original-logo.png').write_bytes(fetch(url))
manifest.append({'file':'dist/assets/wilton-original-logo.png','source':url,'rights':'Existing Wilton Dental identity; unmodified.'})
for slug in ['imaging','whitening']:
    candidates=[i for i in pages[slug].images if 'custom-logo' not in i.get('class','')]
    for n,img in enumerate(candidates):
        try:
            im=Image.open(io.BytesIO(fetch(img['src'])));im.thumbnail((1100,900));dest=ASSETS/f'{slug}-{n}.webp';im.save(dest,'WEBP',quality=85)
            manifest.append({'file':dest.relative_to(ROOT).as_posix(),'source':img['src'],'size':list(im.size),'rights':'Existing practice website asset.'})
        except Exception as e: print('Skipped image',slug,n,str(e))
(SOURCE/'assets.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'pages':list(pages),'assets':len(manifest),'profile':pages['dr-wale-towolawi'].text},indent=2))
