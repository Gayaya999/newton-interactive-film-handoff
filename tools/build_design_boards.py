"""Generate four static planning boards from existing film stills. Python 3 only."""
from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / 'design'


def image(path):
    mime = 'image/png' if path.suffix == '.png' else 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def text(x, y, words, size=24, fill='#F1EBDD', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" {extra}>{words}</text>'


def line(x1,y1,x2,y2,stroke='#C4A875',width=1,extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def board(filename, source, content):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<title>{filename} · 静态布局结构示意，待视觉确认</title>
<defs>
  <linearGradient id="filmShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111411" stop-opacity="0"/><stop offset="1" stop-color="#111411" stop-opacity="0.85"/></linearGradient>
  <filter id="paperShadow" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="9" stdDeviation="10" flood-color="#000" flood-opacity="0.28"/></filter>
</defs>
<image href="{image(source)}" x="0" y="0" width="1280" height="720"/>
<g font-family="PingFang SC,Microsoft YaHei,sans-serif" font-weight="400">{content}</g>
</svg>'''
    (DESIGN / filename).write_text(svg, encoding='utf-8')


speed = '<rect width="1280" height="64" fill="#111411"/><rect y="656" width="1280" height="64" fill="#111411"/>'
speed += text(64,43,'调整速度，让小球绕过地面。',28,extra='font-family="Songti SC,STSong,serif"')
speed += text(64,694,'同一起点，只改变向前的速度。',18,'#B5B3A5')
speed += line(575,686,855,686,'#6C7165',1)
for x,label in [(595,'Ⅰ'),(715,'Ⅱ'),(835,'Ⅲ')]:
    speed += line(x,678,x,694,'#B5B3A5',2) + text(x,674,label,17,'#D4CFBF',extra='text-anchor="middle"')
speed += '<rect x="1010" y="665" width="128" height="44" rx="2" fill="none" stroke="#6C7165"/>'
speed += text(1074,695,'发射',22,'#85897F',extra='text-anchor="middle"')
board('01_三档速度.svg',ROOT / 'assets/stills/speed.jpg',speed)

dialogue = '<rect width="1280" height="64" fill="#111411"/><rect y="650" width="1280" height="70" fill="#111411"/>'
dialogue += text(64,43,'距离，会改变吸引吗？',28,extra='font-family="Songti SC,STSong,serif"')
dialogue += line(73,686,96,686,'#C4A875',2)
dialogue += text(112,694,'也许远近并不影响吸引。',23,'#F1EBDD')
dialogue += line(112,706,430,706,'#C4A875',1)
dialogue += line(670,686,683,686,'#7A8175',1)
dialogue += text(700,694,'也许越远，吸引就越弱。',23,'#B5B3A5')
board('02_对白选择.svg',ROOT / 'assets/stills/hypothesis.jpg',dialogue)

desk = DESIGN / 'source-research-108s.png'
notebook = '<rect width="1280" height="720" fill="#111411" opacity="0.23"/><rect width="1280" height="64" fill="#111411"/>'
notebook += text(64,43,'拖动观察窗，找出差异。',28,extra='font-family="Songti SC,STSong,serif"')
notebook += '<path d="M223 137 L1058 146 L1081 601 L211 617 L203 582 L216 163 Z" fill="#DCCDAA" filter="url(#paperShadow)"/>'
notebook += '<path d="M238 155 L1043 163 L1061 584 L233 599 Z" fill="none" stroke="#BDAE90" stroke-width="1" opacity="0.7"/>'
notebook += text(276,196,'把预测留在纸上，再逐处核对。',22,'#393C32',extra='font-family="Songti SC,STSong,serif"')
notebook += line(775,190,811,190,'#393C32',2)+text(821,196,'预测',16,'#393C32')
notebook += line(903,190,939,190,'#6B6856',2,'stroke-dasharray="4 5"')+text(949,196,'参考',16,'#6B6856')
notebook += line(332,239,332,525,'#78725E')+line(332,525,985,525,'#78725E')
notebook += text(283,261,'强',18,'#6B6856')+text(283,510,'弱',18,'#6B6856')
notebook += '<rect x="648" y="228" width="96" height="307" fill="#F1EBDD" fill-opacity="0.30" stroke="#8C826A" stroke-width="1"/>'
notebook += '<path d="M361 270 L960 270" stroke="#393C32" stroke-width="2.5" fill="none"/>'
notebook += '<path d="M361 270 C491 393 628 438 696 458 S867 489 960 493" stroke="#6B6856" stroke-width="2.5" stroke-dasharray="5 6" fill="none"/>'
for x,label in [(361,'近'),(696,'中'),(960,'远')]:
    notebook += line(x,519,x,531,'#78725E')+text(x,553,label,18,'#393C32',extra='text-anchor="middle"')
notebook += line(696,282,696,444,'#9C7560',1.5)+line(688,282,704,282,'#9C7560')+line(688,444,704,444,'#9C7560')
notebook += '<path d="M266 219 h14 m-7 -7 v14 M1001 219 h14 m-7 -7 v14" stroke="#92856D" stroke-width="1.5"/>'
notebook += text(276,584,'这里的预测高于参考。',19,'#675547')
notebook += '<rect x="0" y="638" width="1280" height="82" fill="url(#filmShade)"/>'
notebook += text(64,684,'模型推演示意，非牛顿原始观测记录。',15,'#D4CFBF')
notebook += line(1010,682,1035,682,'#C4A875',2)+text(1050,690,'记下这里',22,'#F1EBDD')
board('03_手稿小游戏.svg',desk,notebook)

ending = '<rect width="1280" height="720" fill="#111411" opacity="0.66"/>'
ending += text(143,160,'留在手稿里的发现',19,'#C4A875',extra='letter-spacing="3"')
for y,words in [(264,'向前运动，也在下落。'),(352,'距离变远，吸引减弱。'),(440,'地球与苹果，相互吸引。')]:
    ending += text(143,y,words,42,'#F1EBDD',extra='font-family="Songti SC,STSong,serif"')
ending += line(145,490,190,490,'#C4A875',1)
ending += text(145,542,'一个问题，连接起大地与星空。',19,'#B5B3A5')
ending += text(145,626,'再走一次',22,'#F1EBDD')+line(145,638,233,638,'#C4A875',1)
ending += text(315,626,'返回入口',20,'#B5B3A5')
board('04_结尾发现.svg',desk,ending)
print('Created four 1280×720 static SVG planning boards.')
