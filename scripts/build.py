"""Usage: python3 build.py <film-folder> <slug> "<Title>". Writes <slug>-film.html (16:9) and <slug>-reel.html (9:16) from src.html."""
import base64, os, sys
if len(sys.argv) < 4: sys.exit('usage: build.py <film-folder> <slug> "<Title>"')
d, slug, title = sys.argv[1:4]
src = open(os.path.join(d, 'src.html'), encoding='utf-8').read()
a = os.path.join(d, 'page-audio.m4a')
audio = 'data:audio/mp4;base64,' + base64.b64encode(open(a, 'rb').read()).decode() if os.path.exists(a) else ''
for name, label, flag in [(f'{slug}-film.html', title + ' Film', ''), (f'{slug}-reel.html', title + ' Reel', "document.documentElement.classList.add('reel')")]:
    open(os.path.join(d, name), 'w', encoding='utf-8').write(src.replace('{{AUDIO}}', audio).replace('{{TITLE}}', label).replace('{{REELFLAG}}', flag))
print('built', slug, len(src) // 1024, 'KB source')
