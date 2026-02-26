#!/usr/bin/env python3
"""
BMSG Dashboard Generator
毎日Claude APIで最新情報を取得し、HTMLを生成する
"""

import anthropic
import json
import os
from datetime import datetime, timezone, timedelta

# 日本時間
JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
today_str = now.strftime("%Y年%-m月%-d日")
today_iso = now.strftime("%Y-%m-%d")

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

print(f"[{today_str}] BMSG情報を取得中...")

# ① Claude + Web検索で最新情報を取得
search_response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=4096,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    system="""あなたはBMSG（Be My Self Group）の最新情報を収集するアシスタントです。
以下のアーティストの情報を収集してください：
BE:FIRST, MAZZEL, HANA, SKY-HI, Novel Core, Aile The Shota, STARGLOW, REIKO

収集する情報カテゴリ：
1. ライブ・イベント（今後の公演、ツアー日程）
2. FC・会員先行申し込み（締切日付き）
3. グッズ販売情報
4. 新曲・リリース情報

必ず以下のJSON形式のみで返してください（マークダウンなし）：
{
  "updated": "YYYY-MM-DD",
  "urgent": [
    {"text": "緊急告知テキスト（締切間近の情報）"}
  ],
  "live": [
    {
      "artist": "アーティスト名",
      "artistKey": "befirst|mazzel|hana|skyhi|novelcore|aile|starglow|reiko|bmsg",
      "title": "イベントタイトル",
      "date": "日程テキスト",
      "venue": "会場",
      "ticket": "チケット情報",
      "tags": ["fc"|"general"|"release"|"goods"|"ended"],
      "url": "公式URL",
      "ended": true|false
    }
  ],
  "fc": [
    {
      "artist": "アーティスト名",
      "artistKey": "befirst|mazzel|hana|skyhi|novelcore|aile|starglow|bmsg",
      "fcName": "FC名",
      "fee": "月額",
      "status": "active|pending",
      "benefit": "特典内容"
    }
  ],
  "release": [
    {
      "artist": "アーティスト名",
      "artistKey": "befirst|mazzel|hana|skyhi|novelcore|aile|starglow|bmsg",
      "title": "タイトル",
      "date": "発売日",
      "type": "album|single|video|streaming",
      "note": "補足情報",
      "url": "URL"
    }
  ],
  "goods": [
    {
      "artist": "アーティスト名",
      "artistKey": "befirst|mazzel|hana|skyhi|novelcore|aile|starglow|bmsg",
      "title": "グッズ名・販売名",
      "date": "販売期間・日程",
      "note": "補足",
      "url": "URL"
    }
  ]
}""",
    messages=[{
        "role": "user",
        "content": f"今日は{today_str}です。BMSGアーティスト全員の最新情報をweb検索して収集し、JSON形式で返してください。特に今後のライブ、現在受付中のFC先行、直近のリリース情報を重点的に調べてください。"
    }]
)

# レスポンスからテキストを抽出
raw_text = ""
for block in search_response.content:
    if block.type == "text":
        raw_text += block.text

# JSON部分を抽出
import re
json_match = re.search(r'\{[\s\S]*\}', raw_text)
if not json_match:
    print("ERROR: JSONが見つかりませんでした")
    print(raw_text[:500])
    exit(1)

try:
    data = json.loads(json_match.group())
    print(f"✅ データ取得成功: live={len(data.get('live',[]))}, fc={len(data.get('fc',[]))}, release={len(data.get('release',[]))}")
except json.JSONDecodeError as e:
    print(f"ERROR: JSON解析失敗: {e}")
    exit(1)

# ② HTMLを生成
HTML = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:title" content="BMSG FAN DASHBOARD">
<meta property="og:description" content="BE:FIRST / MAZZEL / HANA / SKY-HIほか最新情報まとめ">
<title>BMSG FAN DASHBOARD</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Noto+Sans+JP:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
  :root {{
    --black: #0a0a0a; --white: #f0f0f0; --gold: #d4a843; --gold-dim: #8a6a1f;
    --red: #e03030; --blue: #2a6fd4; --purple: #8b3ec8; --teal: #1eb89a;
    --pink: #e84f9a; --orange: #e8852a; --card-bg: #141414; --border: #2a2a2a;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--black); color:var(--white); font-family:'Noto Sans JP',sans-serif; min-height:100vh; overflow-x:hidden; }}
  header {{ position:relative; padding:40px 24px 32px; border-bottom:1px solid var(--border); background:linear-gradient(180deg,#111 0%,var(--black) 100%); overflow:hidden; }}
  header::before {{ content:'BMSG'; position:absolute; right:-20px; top:-10px; font-family:'Bebas Neue',cursive; font-size:160px; color:rgba(212,168,67,0.04); pointer-events:none; letter-spacing:-4px; }}
  .header-inner {{ max-width:1100px; margin:0 auto; display:flex; align-items:flex-end; justify-content:space-between; flex-wrap:wrap; gap:16px; }}
  .logo-area h1 {{ font-family:'Bebas Neue',cursive; font-size:clamp(42px,6vw,72px); letter-spacing:4px; line-height:1; background:linear-gradient(135deg,var(--gold) 0%,#fff8e0 50%,var(--gold) 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }}
  .logo-area p {{ font-size:11px; letter-spacing:3px; color:rgba(255,255,255,0.35); text-transform:uppercase; margin-top:4px; }}
  .header-date {{ font-size:13px; color:rgba(255,255,255,0.4); letter-spacing:1px; }}
  .header-date span {{ color:var(--gold); font-weight:700; }}
  .tabs {{ display:flex; gap:4px; padding:16px 24px; max-width:1100px; margin:0 auto; overflow-x:auto; }}
  .tab {{ padding:8px 20px; border-radius:2px; font-size:12px; letter-spacing:2px; text-transform:uppercase; cursor:pointer; border:1px solid var(--border); background:transparent; color:rgba(255,255,255,0.4); transition:all 0.2s; white-space:nowrap; }}
  .tab.active,.tab:hover {{ background:var(--gold); color:var(--black); border-color:var(--gold); font-weight:700; }}
  main {{ max-width:1100px; margin:0 auto; padding:0 24px 60px; }}
  .section {{ display:none; }}
  .section.active {{ display:block; animation:fadeIn 0.3s ease; }}
  @keyframes fadeIn {{ from {{ opacity:0; transform:translateY(8px); }} to {{ opacity:1; transform:none; }} }}
  .section-header {{ display:flex; align-items:center; gap:14px; margin:32px 0 20px; }}
  .section-header h2 {{ font-family:'Bebas Neue',cursive; font-size:28px; letter-spacing:3px; }}
  .section-header .line {{ flex:1; height:1px; background:linear-gradient(90deg,var(--gold-dim),transparent); }}
  .grid {{ display:grid; gap:14px; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); }}
  .grid-3 {{ grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); }}
  .event-card {{ background:var(--card-bg); border:1px solid var(--border); border-radius:4px; padding:20px; position:relative; overflow:hidden; transition:border-color 0.2s,transform 0.2s; }}
  .event-card:hover {{ border-color:rgba(212,168,67,0.4); transform:translateY(-2px); }}
  .event-card::before {{ content:''; position:absolute; left:0; top:0; bottom:0; width:3px; }}
  .event-card.befirst::before {{ background:var(--blue); }}
  .event-card.mazzel::before {{ background:var(--purple); }}
  .event-card.hana::before {{ background:var(--pink); }}
  .event-card.skyhi::before {{ background:var(--gold); }}
  .event-card.novelcore::before {{ background:var(--red); }}
  .event-card.aile::before {{ background:var(--teal); }}
  .event-card.starglow::before {{ background:var(--orange); }}
  .event-card.reiko::before {{ background:#a0d0f0; }}
  .event-card.bmsg::before {{ background:linear-gradient(180deg,var(--gold),var(--blue)); }}
  .artist-badge {{ display:inline-block; font-size:10px; letter-spacing:2px; text-transform:uppercase; padding:3px 10px; border-radius:2px; margin-bottom:10px; font-weight:700; }}
  .befirst .artist-badge {{ background:rgba(42,111,212,0.2); color:#6fa8ea; border:1px solid rgba(42,111,212,0.3); }}
  .mazzel .artist-badge {{ background:rgba(139,62,200,0.2); color:#c08af0; border:1px solid rgba(139,62,200,0.3); }}
  .hana .artist-badge {{ background:rgba(232,79,154,0.2); color:#f087c4; border:1px solid rgba(232,79,154,0.3); }}
  .skyhi .artist-badge {{ background:rgba(212,168,67,0.15); color:var(--gold); border:1px solid rgba(212,168,67,0.3); }}
  .novelcore .artist-badge {{ background:rgba(224,48,48,0.2); color:#f07070; border:1px solid rgba(224,48,48,0.3); }}
  .aile .artist-badge {{ background:rgba(30,184,154,0.2); color:#60d8c0; border:1px solid rgba(30,184,154,0.3); }}
  .starglow .artist-badge {{ background:rgba(232,133,42,0.2); color:#f0a870; border:1px solid rgba(232,133,42,0.3); }}
  .reiko .artist-badge {{ background:rgba(160,208,240,0.2); color:#a0d0f0; border:1px solid rgba(160,208,240,0.3); }}
  .bmsg .artist-badge {{ background:rgba(212,168,67,0.15); color:var(--gold); border:1px solid rgba(212,168,67,0.3); }}
  .event-title {{ font-size:15px; font-weight:700; line-height:1.4; margin-bottom:10px; }}
  .event-meta {{ display:flex; flex-direction:column; gap:5px; font-size:12px; color:rgba(255,255,255,0.5); }}
  .event-meta .icon {{ margin-right:6px; }}
  .event-meta .date-val {{ color:rgba(255,255,255,0.85); font-weight:700; }}
  .tag {{ display:inline-block; font-size:10px; padding:2px 8px; border-radius:2px; margin-top:10px; margin-right:4px; letter-spacing:1px; }}
  .tag.fc {{ background:rgba(212,168,67,0.15); color:var(--gold); }}
  .tag.general {{ background:rgba(255,255,255,0.08); color:rgba(255,255,255,0.5); }}
  .tag.release {{ background:rgba(30,184,154,0.15); color:var(--teal); }}
  .tag.goods {{ background:rgba(232,79,154,0.15); color:var(--pink); }}
  .tag.ended {{ background:rgba(255,255,255,0.05); color:rgba(255,255,255,0.25); }}
  .link-btn {{ display:inline-block; margin-top:14px; font-size:11px; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,0.35); text-decoration:none; border-bottom:1px solid rgba(255,255,255,0.15); padding-bottom:2px; transition:color 0.2s,border-color 0.2s; }}
  .link-btn:hover {{ color:var(--gold); border-color:var(--gold); }}
  .urgent {{ background:linear-gradient(135deg,rgba(224,48,48,0.12),rgba(224,48,48,0.05)); border:1px solid rgba(224,48,48,0.3); border-radius:4px; padding:16px 20px; margin-bottom:20px; display:flex; align-items:center; gap:12px; }}
  .urgent-dot {{ width:8px; height:8px; background:var(--red); border-radius:50%; animation:pulse 1.5s infinite; flex-shrink:0; }}
  @keyframes pulse {{ 0%,100% {{ opacity:1; transform:scale(1); }} 50% {{ opacity:0.4; transform:scale(0.7); }} }}
  .urgent p {{ font-size:13px; color:rgba(255,255,255,0.75); }}
  .urgent strong {{ color:#f07070; }}
  .notice {{ background:rgba(212,168,67,0.07); border:1px solid rgba(212,168,67,0.2); border-radius:4px; padding:14px 18px; font-size:12px; color:rgba(255,255,255,0.5); margin-bottom:20px; line-height:1.7; }}
  .notice a {{ color:var(--gold); text-decoration:none; }}
  .fc-table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  .fc-table th {{ text-align:left; padding:10px 14px; background:rgba(255,255,255,0.04); color:rgba(255,255,255,0.4); font-size:11px; letter-spacing:1px; text-transform:uppercase; font-weight:400; border-bottom:1px solid var(--border); }}
  .fc-table td {{ padding:13px 14px; border-bottom:1px solid rgba(255,255,255,0.05); vertical-align:middle; }}
  .fc-table tr:hover td {{ background:rgba(255,255,255,0.02); }}
  .fc-name {{ font-weight:700; font-size:13px; }}
  .fc-fee {{ color:var(--gold); font-weight:700; }}
  .status-dot {{ display:inline-block; width:6px; height:6px; border-radius:50%; margin-right:6px; }}
  .status-dot.active {{ background:var(--teal); }}
  .status-dot.pending {{ background:var(--orange); }}
  .update-badge {{ position:fixed; bottom:20px; right:20px; background:rgba(20,20,20,0.95); border:1px solid var(--border); border-radius:4px; padding:10px 16px; font-size:11px; color:rgba(255,255,255,0.35); letter-spacing:1px; z-index:100; }}
  .update-badge span {{ color:var(--gold); }}
  @media(max-width:600px) {{ .grid,.grid-3 {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body>

<header>
  <div class="header-inner">
    <div class="logo-area">
      <h1>BMSG DASHBOARD</h1>
      <p>Be My Self Group — Fan Info Hub</p>
    </div>
    <div class="header-date">最終更新 <span>{today_str}</span></div>
  </div>
</header>

<div style="max-width:1100px;margin:0 auto;">
  <div class="tabs">
    <button class="tab active" onclick="showTab('live',this)">🎤 ライブ・イベント</button>
    <button class="tab" onclick="showTab('fc',this)">🏷 FC先行・申込</button>
    <button class="tab" onclick="showTab('release',this)">💿 新曲・リリース</button>
    <button class="tab" onclick="showTab('goods',this)">🛍 グッズ</button>
  </div>
</div>

<main>

<!-- LIVE -->
<section id="live" class="section active">
  <div class="section-header"><h2>ライブ・イベント</h2><div class="line"></div></div>
  {''.join(f'<div class="urgent"><div class="urgent-dot"></div><p><strong>直近情報</strong>　{u["text"]}</p></div>' for u in data.get('urgent', []))}
  <div class="grid">
  {''.join(f"""
    <div class="event-card {item.get('artistKey','bmsg')}{' ' if item.get('ended') else ''}">
      <div class="artist-badge">{item['artist']}</div>
      <div class="event-title">{item['title']}</div>
      <div class="event-meta">
        {'<div><span class="icon">📅</span><span class="date-val">' + item['date'] + '</span></div>' if item.get('date') else ''}
        {'<div><span class="icon">📍</span>' + item['venue'] + '</div>' if item.get('venue') else ''}
        {'<div><span class="icon">🎫</span>' + item['ticket'] + '</div>' if item.get('ticket') else ''}
      </div>
      {''.join(f'<span class="tag {t}">{"⭐ FC先行" if t=="fc" else "一般" if t=="general" else "リリース" if t=="release" else "グッズ" if t=="goods" else "終了" if t=="ended" else t}</span>' for t in item.get('tags',[]))}
      {'<br><a href="' + item['url'] + '" target="_blank" class="link-btn">詳細を見る →</a>' if item.get('url') else ''}
    </div>""" for item in data.get('live', []))}
  </div>
</section>

<!-- FC -->
<section id="fc" class="section">
  <div class="section-header"><h2>FC先行・申込情報</h2><div class="line"></div></div>
  <div class="notice">
    ⚡ <strong>B-Town（B with U）</strong> はBMSGのオンラインサロン。ArchitectまたはResidentプランに入会すると、ほぼ全アーティストのFC先行にまとめてアクセス可能。
    → <a href="https://bmsg.shop/pages/b-town" target="_blank">B-Town公式</a>
  </div>
  <table class="fc-table">
    <thead><tr><th>アーティスト</th><th>FC名</th><th>月額</th><th>状態</th><th>特典</th></tr></thead>
    <tbody>
    {''.join(f"""<tr>
      <td><div class="fc-name">{item['artist']}</div></td>
      <td>{item.get('fcName','—')}</td>
      <td class="fc-fee">{item.get('fee','—')}</td>
      <td><span class="status-dot {item.get('status','active')}"></span>{'受付中' if item.get('status')=='active' else '詳細待ち'}</td>
      <td>{item.get('benefit','—')}</td>
    </tr>""" for item in data.get('fc', []))}
    </tbody>
  </table>
</section>

<!-- RELEASE -->
<section id="release" class="section">
  <div class="section-header"><h2>新曲・リリース情報</h2><div class="line"></div></div>
  <div class="grid grid-3">
  {''.join(f"""
    <div class="event-card {item.get('artistKey','bmsg')}">
      <div class="artist-badge">{item['artist']}</div>
      <div class="event-title">{item['title']}</div>
      <div class="event-meta">
        {'<div><span class="icon">📅</span><span class="date-val">' + item['date'] + '</span></div>' if item.get('date') else ''}
        {'<div><span class="icon">📝</span>' + item['note'] + '</div>' if item.get('note') else ''}
      </div>
      <span class="tag release">{'📀 アルバム' if item.get('type')=='album' else '🎵 シングル' if item.get('type')=='single' else '🎬 映像作品' if item.get('type')=='video' else '🎵 配信'}</span>
      {'<br><a href="' + item['url'] + '" target="_blank" class="link-btn">詳細 →</a>' if item.get('url') else ''}
    </div>""" for item in data.get('release', []))}
  </div>
</section>

<!-- GOODS -->
<section id="goods" class="section">
  <div class="section-header"><h2>グッズ・販売情報</h2><div class="line"></div></div>
  <div class="grid">
  {''.join(f"""
    <div class="event-card {item.get('artistKey','bmsg')}">
      <div class="artist-badge">{item['artist']}</div>
      <div class="event-title">{item['title']}</div>
      <div class="event-meta">
        {'<div><span class="icon">📅</span><span class="date-val">' + item['date'] + '</span></div>' if item.get('date') else ''}
        {'<div><span class="icon">🛒</span>' + item['note'] + '</div>' if item.get('note') else ''}
      </div>
      <span class="tag goods">グッズ</span>
      {'<br><a href="' + item['url'] + '" target="_blank" class="link-btn">詳細 →</a>' if item.get('url') else ''}
    </div>""" for item in data.get('goods', []))}
  </div>
</section>

</main>

<div class="update-badge">🔄 毎日自動更新 / 最終更新: <span>{today_str}</span></div>

<script>
function showTab(id, el) {{
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  el.classList.add('active');
}}
</script>
</body>
</html>"""

# ③ index.htmlとして保存
output_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"✅ index.html を生成しました ({today_str})")
