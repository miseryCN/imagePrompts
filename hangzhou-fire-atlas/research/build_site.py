from pathlib import Path
import json,base64
r=Path(__file__).resolve().parents[1]
t=(r/'index.template.html').read_text(encoding='utf-8')
data=json.dumps(json.loads((r/'data/places.json').read_text(encoding='utf-8')),ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
svg='data:image/svg+xml;base64,'+base64.b64encode((r/'assets/fire-grill.svg').read_bytes()).decode()
out=t.replace('/*__CSS__*/',(r/'style.css').read_text(encoding='utf-8')).replace('/*__JS__*/',(r/'app.js').read_text(encoding='utf-8')).replace('__GRILL__',svg).replace('__DATA__',data)
(r/'index.html').write_text(out,encoding='utf-8')
(r.parent/'杭州炭火图鉴.html').write_text(out,encoding='utf-8')
print('Built:',len(out.encode()),'bytes')
