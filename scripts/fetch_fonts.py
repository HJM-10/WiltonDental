from urllib.request import urlopen,Request
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
out=root/'dist/assets/fonts';out.mkdir(exist_ok=True)
url='https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=DM+Sans:wght@400;500;600;700&display=swap'
css=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read().decode()
for i,source in enumerate(dict.fromkeys(re.findall(r'url\((https[^)]+)\)',css))):
    file=f'font-{i}.ttf';(out/file).write_bytes(urlopen(source,timeout=40).read());css=css.replace(source,'/assets/fonts/'+file)
(out/'fonts.css').write_text(css,encoding='utf-8')
for name,source in [('Cormorant-OFL.txt','https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/OFL.txt'),('DM-Sans-OFL.txt','https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/OFL.txt')]:
    (out/name).write_bytes(urlopen(source,timeout=40).read())
print('Downloaded local font files and OFL licenses')
