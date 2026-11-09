# Generate the nine new card faces, presentation sheets and the gallery from cards/data/beasts.json.
# The two original cards (baize, qilin) keep their hand-built pages; their gallery entries come from the same data file.
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "cards", "data", "beasts.json")
CARDS = os.path.join(ROOT, "cards")
NEW_IDS = ["fenghuang", "xuanwu", "zhuque", "chongming", "baihu", "chenghuang", "qinglong", "pixiu", "jiuweihu"]
ALL_IDS = ["baize", "qilin"] + NEW_IDS

FRONT = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=750">
<title>__NAME__ · 正面</title>
<link rel="stylesheet" href="card.css">
</head>
<body>
<div class="card card--__PALETTE__ front--new">
  <div class="front-media" style="background-image:url('assets/__BG__')"></div>
  <div class="aura aura--new" style="--ax:__AX__px;--ay:__AY__px;--aw:__AW__px;--ah:__AH__px"></div>
  <div class="__CELESTIAL__"></div>

  <img class="beast-art beast-art--glow" src="assets/__BEAST__" alt="" style="--bx:__BX__px;--by:__BY__px;--bw:__BW__px">
  <img class="beast-art" src="assets/__BEAST__" alt="__ALT__" style="--bx:__BX__px;--by:__BY__px;--bw:__BW__px">
  <div class="mist-front"></div>

  <div class="veil"></div>

  <div class="front-head">
    <div class="series">山海异兽录 <span class="dot"></span> <em>__VOLUME__</em></div>
    <div class="rank"><span>__RANK__</span></div>
  </div>

  <div class="title-veil"></div>

  <div class="front-title">
    <div class="eyebrow">No.__NO__ · __SCENE__</div>
    <h1>__NAME__</h1>
    <p class="sub">__SUBTITLE__</p>
    <div class="meta"><span>__M1__</span><i></i><span>__M2__</span><i></i><span>__M3__</span></div>
  </div>

  <div class="seal__SEALCLASS__">__NAME__</div>

  <div class="corner corner--tl"></div>
  <div class="corner corner--tr"></div>
  <div class="corner corner--bl"></div>
  <div class="corner corner--br"></div>
  <div class="frame"></div>
  <div class="grain"></div>
</div>
</body>
</html>
"""

BACK = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=750">
<title>__NAME__ · 背面</title>
<link rel="stylesheet" href="card.css">
</head>
<body>
<div class="card card--__PALETTE__ back back--new">
  <div class="back-watermark"><img src="assets/__BEAST__" alt=""></div>
  <div class="back-inner">
    <div class="back-head">
      <div>
        <div class="back-kicker">山海异兽录 · 神兽图鉴</div>
        <div class="back-name">__NAME__</div>
        <div class="back-en">__EN__ · NO.__NO__ · __METARANK__</div>
      </div>
      <div class="back-seal__SEALCLASS__">__RANK__</div>
    </div>

    <div class="back-divider"></div>

    <div class="stats">
__STATS__
    </div>

    <div class="sections">
      <div class="sec">
        <div class="sec-head"><span class="num">壹</span><h3>分类</h3><span class="en">Classification</span></div>
        <p>__CLASSIFICATION__</p>
      </div>
      <div class="sec">
        <div class="sec-head"><span class="num">贰</span><h3>神兽特点</h3><span class="en">Traits</span></div>
        <p>__TRAITS__</p>
      </div>
      <div class="sec">
        <div class="sec-head"><span class="num">叁</span><h3>功用技能</h3><span class="en">Powers</span></div>
        <p>__POWERS__</p>
      </div>
      <div class="sec">
        <div class="sec-head"><span class="num">肆</span><h3>原型推测</h3><span class="en">Origin</span></div>
        <p>__ORIGIN__</p>
      </div>
    </div>

    <div class="quote">
      <p>__QUOTE__</p>
      <cite>__QUOTESOURCE__</cite>
    </div>

    <div class="back-source">__SOURCE__</div>

    <div class="back-foot">
      <span>正面 · __SCENE__</span>
      <span class="mid">背面 · 神兽图鉴</span>
      <span>NO.__NO__</span>
    </div>
  </div>

  <div class="corner corner--tl"></div>
  <div class="corner corner--tr"></div>
  <div class="corner corner--bl"></div>
  <div class="corner corner--br"></div>
  <div class="frame"></div>
  <div class="grain"></div>
</div>
</body>
</html>
"""

PRESENT = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>__NAME__ · 双面卡牌</title>
<style>
html,body{margin:0;padding:0;width:1760px;height:1260px;overflow:hidden;background:#070b0e;font-family:"Noto Serif SC","SimSun",serif}
.sheet{position:relative;width:1760px;height:1260px;padding:34px 100px 0;box-sizing:border-box;overflow:hidden;
  background:
    radial-gradient(55% 55% at 22% 38%, rgba(50,92,112,.25), rgba(50,92,112,0) 65%),
    radial-gradient(45% 50% at 82% 46%, rgba(34,64,80,.2), rgba(34,64,80,0) 70%),
    radial-gradient(120% 100% at 50% 110%, rgba(0,0,0,.85), rgba(0,0,0,0) 60%),
    linear-gradient(160deg,#0a1117 0%,#060a0d 55%,#05080b 100%)}
.sheet::before{content:"";position:absolute;inset:0;background-image:url('grain.svg');background-size:240px;opacity:.14;mix-blend-mode:overlay;pointer-events:none}
.frame-rule{position:absolute;inset:18px;border:1px solid rgba(201,168,106,.22);pointer-events:none}
.head{position:relative;display:flex;align-items:flex-end;justify-content:space-between;height:64px;border-bottom:1px solid rgba(201,168,106,.28);padding-bottom:12px}
.head .kicker{font-size:10px;letter-spacing:.44em;color:#b99a63}
.head h1{margin:8px 0 0;font-size:28px;line-height:1;font-weight:600;letter-spacing:.16em;color:#f3eee2}
.head h1 span{color:#c9a86a;font-weight:400;font-size:16px;letter-spacing:.22em;margin-left:14px}
.head .meta{text-align:right;font-size:9.5px;line-height:2;letter-spacing:.28em;color:#8d816c}
.cards{position:relative;display:flex;gap:60px;margin-top:18px}
figure{margin:0;width:750px}
figure img{display:block;width:750px;height:1050px;border-radius:12px;border:1px solid rgba(201,168,106,.32);box-shadow:0 34px 80px rgba(0,0,0,.68);background:#0b1116}
figcaption{display:flex;align-items:center;justify-content:space-between;margin-top:12px;font-size:10px;letter-spacing:.3em;color:#a3957b;text-transform:uppercase}
figcaption b{font-weight:500;color:#d8c49a;font-size:11px;letter-spacing:.26em}
.foot{position:relative;display:flex;align-items:center;justify-content:space-between;margin-top:12px;font-size:9px;letter-spacing:.24em;color:#6f6657;text-transform:uppercase}
.foot .mid{display:flex;align-items:center;gap:10px}
.foot .mid::before,.foot .mid::after{content:"";width:28px;height:1px;background:rgba(150,128,90,.45)}
</style>
</head>
<body>
<div class="sheet">
  <div class="frame-rule"></div>
  <div class="head">
    <div>
      <div class="kicker">山海异兽录 · 神兽卡牌</div>
      <h1>__NAME__<span>__SCENE__ · __EN__</span></h1>
    </div>
    <div class="meta">NO.__NO__ / __METARANK__<br>双面卡牌 · 1500 × 2100 PX</div>
  </div>

  <div class="cards">
    <figure>
      <img src="renders/__ID__-front.png" alt="__NAME__卡牌正面">
      <figcaption><b>正面 · FRONT</b><span>__SCENE__ · __SUBTITLE__</span></figcaption>
    </figure>
    <figure>
      <img src="renders/__ID__-back.png" alt="__NAME__卡牌背面">
      <figcaption><b>背面 · BACK</b><span>神兽图鉴 · 分类 / 特点 / 功用 / 原型</span></figcaption>
    </figure>
  </div>

  <div class="foot">
    <span>__SOURCESHORT__</span>
    <span class="mid">山海异兽录 · __VOLUMESHORT__</span>
    <span>MYTHIC BEAST CODEX</span>
  </div>
</div>
</body>
</html>
"""


def fill(template, data):
    out = template
    for k, v in data.items():
        out = out.replace("__" + k + "__", str(v))
    return out


def build_new(beast):
    bid = beast["id"]
    name = beast["name"]
    data = {
        "ID": bid, "NAME": name, "PALETTE": beast["palette"], "BG": beast["bg"],
        "BEAST": beast["beast"], "BX": beast["bx"], "BY": beast["by"], "BW": beast["bw"],
        "AX": beast["ax"], "AY": beast["ay"], "AW": beast["aw"], "AH": beast["ah"],
        "CELESTIAL": beast["celestial"], "VOLUME": beast["volume"], "RANK": beast["rank"],
        "NO": beast["no"], "SCENE": beast["scene"], "SUBTITLE": beast["subtitle"],
        "M1": beast["meta"][0], "M2": beast["meta"][1], "M3": beast["meta"][2],
        "EN": beast["en"], "CLASSIFICATION": beast["classification"], "TRAITS": beast["traits"],
        "POWERS": beast["powers"], "ORIGIN": beast["origin"], "QUOTE": beast["quote"],
        "QUOTESOURCE": beast["quoteSource"], "SOURCE": beast["sourceNote"],
        "SEALCLASS": " seal--long" if len(name) >= 3 else "",
        "METARANK": beast["meta"][0],
        "SOURCESHORT": beast["sourceNote"].replace("｜", " · "),
        "VOLUMESHORT": beast["volume"].split(" · ")[-1],
        "ALT": name + "，" + beast["subtitle"],
    }
    stats = []
    for label, value in beast["stats"].items():
        stats.append(
            '      <div class="stat"><div class="lab">%s</div><div class="row"><div class="bar"><i style="width:%s%%"></i></div><span class="val">%s</span></div></div>'
            % (label, value, value)
        )
    data["STATS"] = "\n".join(stats)
    front = fill(FRONT, data)
    back = fill(BACK, data)
    present = fill(PRESENT, data)
    open(os.path.join(CARDS, bid + "-front.html"), "w", encoding="utf-8").write(front)
    open(os.path.join(CARDS, bid + "-back.html"), "w", encoding="utf-8").write(back)
    open(os.path.join(CARDS, "present-" + bid + ".html"), "w", encoding="utf-8").write(present)


def build_gallery(data):
    items = []
    for bid in ALL_IDS:
        b = data[bid]
        items.append(
            '<a class="cardlink" href="%s-front.html">'
            '<img src="renders/%s-card.png" alt="%s双面卡牌">'
            '<span class="cap"><b>%s</b><em>NO.%s · %s</em><small>%s</small></span></a>'
            % (bid, bid, b["name"], b["name"], b["no"], b["scene"], b["subtitle"])
        )
    cards_html = "\n".join(items)
    html = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>山海异兽录 · 十一张神兽卡牌</title>
<style>
:root{--bg:#080b0e;--panel:#0e1419;--ink:#e9e2d3;--muted:#9a917f;--gold:#c9a86a;--gold-soft:rgba(201,168,106,.35);--red:#a8392b}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:"Noto Serif SC","SimSun",serif}
body{background:radial-gradient(60% 50% at 18% 0%, rgba(50,92,112,.2), transparent 60%),radial-gradient(50% 45% at 86% 4%, rgba(96,82,38,.16), transparent 60%),linear-gradient(#080b0e,#06090c 60%,#05080a)}
.wrap{max-width:1280px;margin:0 auto;padding:56px 32px 40px}
header{border-bottom:1px solid var(--gold-soft);padding-bottom:26px}
.kicker{font-size:11px;letter-spacing:.46em;color:var(--gold);text-transform:uppercase}
h1{font-size:64px;line-height:1.05;margin:16px 0 12px;font-weight:600;letter-spacing:.12em}
h1 em{font-style:normal;color:var(--gold);font-weight:400}
.lede{max-width:900px;margin:0;color:#c7bfae;font-size:17px;line-height:1.85;letter-spacing:.02em}
.factline{display:flex;flex-wrap:wrap;gap:10px 26px;margin-top:20px;font-size:11px;letter-spacing:.22em;color:var(--muted);text-transform:uppercase}
.factline span::before{content:"◆";color:var(--gold);font-size:8px;margin-right:8px;vertical-align:2px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:34px}
.cardlink{display:block;color:inherit;text-decoration:none;background:var(--panel);border:1px solid rgba(201,168,106,.18);border-radius:10px;overflow:hidden;transition:border-color .2s,transform .2s}
.cardlink:hover{border-color:rgba(201,168,106,.55);transform:translateY(-3px)}
.cardlink img{display:block;width:100%;height:auto}
.cap{display:flex;flex-direction:column;gap:4px;padding:14px 16px 16px}
.cap b{font-size:22px;font-weight:600;letter-spacing:.12em}
.cap em{font-style:normal;font-size:10px;letter-spacing:.24em;color:var(--gold);text-transform:uppercase}
.cap small{font-size:12px;letter-spacing:.08em;color:var(--muted)}
footer{margin-top:48px;border-top:1px solid var(--gold-soft);padding-top:22px;font-size:11px;line-height:2;color:#786f60;letter-spacing:.04em}
footer a{color:#a99a7d;text-decoration:none;border-bottom:1px solid rgba(169,154,125,.35)}
.seal{display:inline-flex;width:44px;height:44px;align-items:center;justify-content:center;background:var(--red);color:#f8ece2;font-family:"SimSun";font-size:16px;border-radius:2px;transform:rotate(-3deg);margin-right:14px;vertical-align:middle}
@media (max-width:980px){.grid{grid-template-columns:repeat(2,1fr)}h1{font-size:46px}}
@media (max-width:600px){.grid{grid-template-columns:1fr}.wrap{padding:32px 18px}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="kicker">CaptainDW · 山海异兽录</div>
    <h1>十一神兽 <em>·</em> 图鉴</h1>
    <p class="lede">白泽、麒麟、凤凰、玄武、朱雀、重明鸟、白虎、乘黄、青龙、貔貅、九尾狐。每张卡牌正面为神兽姿态与所居山水，背面为分类、特点、功用技能与原型推测；图像取自公有领域古籍版画与宋元山水，重组为可收藏的双面卡牌。</p>
    <div class="factline">
      <span>01 白泽</span><span>02 麒麟</span><span>03 凤凰</span><span>04 玄武</span><span>05 朱雀</span><span>06 重明鸟</span><span>07 白虎</span><span>08 乘黄</span><span>09 青龙</span><span>10 貔貅</span><span>11 九尾狐</span>
      <span>单面 1500 × 2100 px</span><span>双面 3520 × 2520 px</span>
    </div>
  </header>
  <div class="grid">
__CARDS__
  </div>
  <footer>
    <span class="seal">山海</span>
    图像来源 · 《古今图书集成 · 禽虫典》诸图（公有领域，Wikimedia Commons）<br>
    场景 · 《雪景寒林图》《千里江山图》《早春图》《溪山行旅图》（公有领域）<br>
    卡面设计、排版与渲染 · CaptainDW · 神兽图鉴 · 详见 <a href="../ATTRIBUTION.md">ATTRIBUTION.md</a> 与 <a href="../README.md">README.md</a>
  </footer>
</div>
</body>
</html>
""".replace("__CARDS__", cards_html)
    open(os.path.join(CARDS, "index.html"), "w", encoding="utf-8").write(html)


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    for bid in NEW_IDS:
        build_new(data[bid])
        print("built", bid)
    build_gallery(data)
    print("gallery built")


if __name__ == "__main__":
    main()
