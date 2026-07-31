# -*- coding: utf-8 -*-
"""
Embeds the full novel (book/*.md) INTO the visual novel HTML as a built-in reader
(button '📖 РОМАН' in the header). Output: kobyla_has_waken_up.html (main game file).
"""
import json, re, html as H, glob, os, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def inline(t):
    t = H.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    return t

def md_to_sections(text):
    """Split markdown into sections by top-level '# ' headings."""
    sections = []
    cur = None
    buf = []
    for raw in text.split('\n'):
        line = raw.rstrip()
        if line.startswith('# '):
            if cur is not None:
                sections.append((cur, '\n'.join(buf)))
            cur = inline(line[2:].strip())
            buf = []
        elif cur is not None:
            if line.strip() == '---':
                buf.append('<hr>')
            elif line.startswith('## '):
                buf.append(f'<h2>{inline(line[3:].strip())}</h2>')
            elif line.startswith('### '):
                buf.append(f'<h3>{inline(line[4:].strip())}</h3>')
            elif line.strip() == '':
                buf.append('')
            else:
                buf.append(f'<p>{inline(line.strip())}</p>')
    if cur is not None:
        sections.append((cur, '\n'.join(buf)))
    return sections

def main():
    files = sorted(glob.glob('book/*.md'))
    novel = []
    for f in files:
        txt = open(f, encoding='utf-8').read()
        for title, body in md_to_sections(txt):
            novel.append({'t': title, 'b': body})

    src = 'kobyla_has_waken_up_expanded.html'
    html_doc = open(src, encoding='utf-8').read()

    # 1) header button (before MUSIC button)
    anchor = '<button class="btn-ctrl" id="btn-music"'
    assert anchor in html_doc, 'music button anchor not found'
    novel_btn = '<button class="btn-ctrl" id="btn-novel" onclick="openNovel()">📖 РОМАН</button>\n                '
    html_doc = html_doc.replace(anchor, novel_btn + anchor, 1)

    # 2) novel modal markup before the existing modal
    modal_anchor = '<!-- Modal -->'
    assert modal_anchor in html_doc, 'modal anchor not found'
    novel_modal = '''<!-- Novel Reader Modal -->
    <div class="novel-overlay" id="novel-box">
        <div class="novel-card">
            <div class="novel-head">
                <div class="novel-title">КОБЫЛА ПРОСНУЛАСЬ 2099 — РОМАН. КНИГА ПЕРВАЯ: АНАЛИТИКА ОТЧАЯНИЯ</div>
                <button class="btn-ctrl" onclick="closeNovel()">✕ ЗАКРЫТЬ</button>
            </div>
            <div class="novel-body">
                <div class="novel-nav" id="novel-nav"></div>
                <div class="novel-content" id="novel-content">
                    <div class="novel-intro">Выберите главу в списке слева.<br>Все главы — внутри этой игры. Это тот же текст, что и в сюжете: хлёсткий, публицистический, без воды.</div>
                </div>
            </div>
            <div class="novel-foot">
                <button class="btn-ctrl" id="btn-novel-prev" onclick="novelStep(-1)">◀ ГЛАВА НАЗАД</button>
                <span id="novel-pos"></span>
                <button class="btn-ctrl" id="btn-novel-next" onclick="novelStep(1)">ГЛАВА ВПЕРЁД ▶</button>
            </div>
        </div>
    </div>

'''
    html_doc = html_doc.replace(modal_anchor, novel_modal + modal_anchor, 1)

    # 3) JS: novel data + functions (before window.onload)
    data_js = json.dumps(novel, ensure_ascii=False)
    novel_js = f'''
        // ===== NOVEL READER (РОМАН) =====
        const novelData = {data_js};
        let novelIdx = 0;

        function openNovel() {{
            const box = document.getElementById('novel-box');
            box.classList.add('active');
            renderNovelNav();
            novelShow(0);
        }}

        function closeNovel() {{
            document.getElementById('novel-box').classList.remove('active');
        }}

        function renderNovelNav() {{
            const nav = document.getElementById('novel-nav');
            nav.innerHTML = '';
            novelData.forEach((s, i) => {{
                const item = document.createElement('button');
                item.className = 'novel-nav-item' + (i === novelIdx ? ' active' : '');
                item.innerText = s.t;
                item.onclick = () => novelShow(i);
                nav.appendChild(item);
            }});
        }}

        function novelShow(i) {{
            novelIdx = Math.max(0, Math.min(novelData.length - 1, i));
            const s = novelData[novelIdx];
            document.getElementById('novel-content').innerHTML = '<h1 class="novel-h1">' + s.t + '</h1>' + s.b;
            document.getElementById('novel-content').scrollTop = 0;
            document.getElementById('novel-pos').innerText = (novelIdx + 1) + ' / ' + novelData.length;
            document.querySelectorAll('.novel-nav-item').forEach((el, idx) => {{
                el.classList.toggle('active', idx === novelIdx);
            }});
        }}

        function novelStep(d) {{
            novelShow(novelIdx + d);
        }}
    '''
    onload_anchor = 'window.onload = () => {'
    assert onload_anchor in html_doc, 'onload anchor not found'
    html_doc = html_doc.replace(onload_anchor, novel_js + '\n\n        ' + onload_anchor, 1)

    # 4) CSS for the novel reader before </style>
    css = '''
        .novel-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(4, 2, 6, 0.94); backdrop-filter: blur(6px);
            z-index: 600; display: flex; justify-content: center; align-items: center;
            opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
        }
        .novel-overlay.active { opacity: 1; pointer-events: auto; }
        .novel-card {
            background: #0a0710; border: 2px solid var(--border-red);
            box-shadow: 0 0 40px rgba(220, 20, 60, 0.35);
            width: 96vw; max-width: 1240px; height: 92vh; border-radius: 2px;
            display: flex; flex-direction: column;
        }
        .novel-head {
            display: flex; justify-content: space-between; align-items: center; gap: 10px;
            padding: 12px 16px; border-bottom: 1px solid var(--border-red);
            background: linear-gradient(90deg, rgba(220,20,60,0.18), rgba(0,216,255,0.06));
        }
        .novel-title {
            font-family: var(--font-title); font-weight: 800; font-size: 0.95rem;
            color: #fff; letter-spacing: 0.08em;
        }
        .novel-body { display: flex; flex: 1; min-height: 0; }
        .novel-nav {
            width: 300px; min-width: 300px; overflow-y: auto; padding: 12px;
            border-right: 1px solid rgba(220, 20, 60, 0.4);
            background: rgba(14, 10, 16, 0.85);
        }
        .novel-nav-item {
            display: block; width: 100%; text-align: left;
            background: none; border: none; color: var(--text-light);
            font-family: var(--font-main); font-size: 0.82rem;
            padding: 9px 10px; margin-bottom: 4px; cursor: pointer;
            border-left: 2px solid transparent; line-height: 1.35;
        }
        .novel-nav-item:hover { background: rgba(220, 20, 60, 0.15); color: #fff; }
        .novel-nav-item.active {
            border-left-color: var(--glow-red); background: rgba(220, 20, 60, 0.22);
            color: #fff; font-weight: 700;
        }
        .novel-content {
            flex: 1; overflow-y: auto; padding: 26px 34px 60px;
            line-height: 1.75; font-size: 0.98rem; color: #dfe6e8;
        }
        .novel-content h1.novel-h1 {
            font-family: var(--font-title); font-weight: 900; font-size: 1.6rem;
            color: #fff; letter-spacing: 0.06em; margin: 0 0 18px;
            text-shadow: 0 0 18px rgba(255, 26, 64, 0.5);
            border-bottom: 2px solid var(--border-red); padding-bottom: 12px;
        }
        .novel-content h2 {
            font-weight: 700; font-size: 1.25rem; color: var(--text-gold);
            margin: 28px 0 10px; letter-spacing: 0.04em; font-family: var(--font-title);
        }
        .novel-content h3 {
            font-weight: 700; font-size: 1.0rem; color: var(--neon-cyan);
            margin: 24px 0 8px; letter-spacing: 0.1em; font-family: var(--font-title);
        }
        .novel-content p { margin: 0.55em 0; }
        .novel-content hr {
            border: none; border-top: 1px dashed rgba(255, 26, 64, 0.55);
            margin: 30px auto; width: 60%;
        }
        .novel-content strong { color: #fff; }
        .novel-content em { color: var(--neon-cyan); }
        .novel-content blockquote {
            border-left: 3px solid var(--text-gold); background: rgba(255, 200, 55, 0.06);
            padding: 0.4em 1.1em; margin: 0.8em 0; color: #f3ead2;
        }
        .novel-intro {
            text-align: center; padding: 80px 20px; color: var(--neon-cyan);
            letter-spacing: 0.05em; font-size: 0.95rem; line-height: 1.9;
        }
        .novel-foot {
            display: flex; justify-content: space-between; align-items: center; gap: 10px;
            padding: 10px 16px; border-top: 1px solid var(--border-red);
            background: rgba(14, 10, 16, 0.9);
        }
        #novel-pos { color: var(--text-gold); font-size: 0.85rem; letter-spacing: 0.1em; }
        @media (max-width: 760px) {
            .novel-body { flex-direction: column; }
            .novel-nav { width: 100%; min-width: 0; max-height: 34vh; border-right: none; border-bottom: 1px solid rgba(220,20,60,0.4); }
            .novel-content { padding: 18px 16px 40px; }
        }
    '''
    style_close = html_doc.rfind('</style>')
    assert style_close != -1
    html_doc = html_doc[:style_close] + css + '\n    ' + html_doc[style_close:]

    open('kobyla_has_waken_up.html', 'w', encoding='utf-8').write(html_doc)
    print('OK -> kobyla_has_waken_up.html')
    print('novel sections embedded:', len(novel))
    print('file size:', len(html_doc))


if __name__ == '__main__':
    main()
