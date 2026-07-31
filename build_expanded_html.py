# -*- coding: utf-8 -*-
"""
Builds kobyla_has_waken_up_expanded.html from the original kobyla_has_waken_up.html.

WHAT CHANGES (everything else stays byte-identical):
  1. storyData is replaced with the massively expanded bilingual script.
  2. New music tracks are added to the Web Audio engine (stalk / war / void / ascension / finale).
  3. New sound effects are added (explosion / alarm / whisper / chant / melt / glass / scream).
  4. Ending nodes now render a clear GAME OVER screen: banner, ending tag, route,
     final stats recap, epilogue, analytical takeaway, restart button.
  5. The portrait image (base64) is taken verbatim from the original file.
"""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from story_part1 import NODES_A
from story_part2 import NODES_B
from story_part3 import NODES_C
from story_part4 import NODES_D
from story_part5 import NODES_E

story = {}
for part in (NODES_A, NODES_B, NODES_C, NODES_D, NODES_E):
    story.update(part)

# Map a few nodes to the new ambient tracks for variety.
TRACK_OVERRIDES = {
    "HACK_SNEAK": "stalk",
    "HACK_DIVE": "void",
    "BURN_DARK": "void",
    "BURN_ENTRY": "war",
    "BURN_CHARGE": "battle",
    "BURN_EMP": "battle",
    "BURN_STAMPEDE": "horror",
    "HACK_VAULT": "horror",
    "AUDIT_HALLWAY2": "horror",
    "ENDING_UPLOAD": "ascension",
    "ENDING_CHAOS": "finale",
}
for k, t in TRACK_OVERRIDES.items():
    if k in story:
        story[k]["music_track"] = t

# Fix any leftover "effect": null -> "-" (original used "-")
for k, v in story.items():
    if v.get("effect") is None:
        v["effect"] = "-"

NEW_TRACKS_JS = r'''                    stalk: {
                        name_ru: 'ТРЕК 7: ПУЛЬС В ТУМАНЕ (65 BPM)',
                        name_en: 'TRACK 7: PULSE IN THE FOG (65 BPM)',
                        tempo: 65,
                        bass: [36.7, 36.7, 32.7, 36.7, 29.1, 32.7, 27.5, 32.7],
                        arp: [110, 116.54, 103.83, 98],
                        waveform: 'sine',
                        kickInterval: 16
                    },
                    war: {
                        name_ru: 'ТРЕК 8: ВОЙНА БУНКЕРА (170 BPM)',
                        name_en: 'TRACK 8: BUNKER WAR (170 BPM)',
                        tempo: 170,
                        bass: [87.3, 87.3, 98, 87.3, 110, 87.3, 98, 130.8],
                        arp: [440, 523.25, 659.25, 880, 659.25, 523.25],
                        waveform: 'square',
                        kickInterval: 1
                    },
                    void: {
                        name_ru: 'ТРЕК 9: БЕЗДНА НЕЙРОНОВ (55 BPM)',
                        name_en: 'TRACK 9: THE NEURAL VOID (55 BPM)',
                        tempo: 55,
                        bass: [27.5, 24.5, 22.0, 18.35],
                        arp: [73.42, 69.3, 65.41, 61.74],
                        waveform: 'sine',
                        kickInterval: 32
                    },
                    ascension: {
                        name_ru: 'ТРЕК 10: ВОЗНЕСЕНИЕ (78 BPM)',
                        name_en: 'TRACK 10: ASCENSION (78 BPM)',
                        tempo: 78,
                        bass: [55, 55, 65.4, 55, 73.4, 65.4, 49, 55],
                        arp: [329.63, 392, 493.88, 587.33, 493.88, 392],
                        waveform: 'triangle',
                        kickInterval: 8
                    },
                    finale: {
                        name_ru: 'ТРЕК 11: ПОСЛЕ СИГНАЛА (72 BPM)',
                        name_en: 'TRACK 11: AFTER THE SIGNAL (72 BPM)',
                        tempo: 72,
                        bass: [43.65, 43.65, 36.71, 43.65, 32.7, 36.71],
                        arp: [196, 261.63, 329.63, 392],
                        waveform: 'sine',
                        kickInterval: 16
                    }'''

NEW_SFX_JS = r'''            else if (type === 'explosion') {
                const bufferSize = ctx.sampleRate * 0.8;
                const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
                const data = buffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) {
                    data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufferSize, 1.5);
                }
                const noise = ctx.createBufferSource();
                noise.buffer = buffer;
                const g = ctx.createGain();
                g.gain.setValueAtTime(0.5, now);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
                const lp = ctx.createBiquadFilter();
                lp.type = 'lowpass';
                lp.frequency.setValueAtTime(400, now);
                lp.frequency.exponentialRampToValueAtTime(40, now + 0.7);
                noise.connect(lp); lp.connect(g); g.connect(ctx.destination);
                noise.start(now); noise.stop(now + 0.85);
                const boom = ctx.createOscillator();
                const bg = ctx.createGain();
                boom.type = 'sine';
                boom.frequency.setValueAtTime(90, now);
                boom.frequency.exponentialRampToValueAtTime(25, now + 0.6);
                bg.gain.setValueAtTime(0.6, now);
                bg.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
                boom.connect(bg); bg.connect(ctx.destination);
                boom.start(now); boom.stop(now + 0.65);
            }
            else if (type === 'alarm') {
                for (let rep = 0; rep < 3; rep++) {
                    const t0 = now + rep * 0.4;
                    const osc = ctx.createOscillator();
                    const g = ctx.createGain();
                    osc.type = 'square';
                    osc.frequency.setValueAtTime(rep % 2 === 0 ? 660 : 520, t0);
                    g.gain.setValueAtTime(0.12, t0);
                    g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.35);
                    osc.connect(g); g.connect(ctx.destination);
                    osc.start(t0); osc.stop(t0 + 0.38);
                }
            }
            else if (type === 'whisper') {
                const bufferSize = ctx.sampleRate * 0.5;
                const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
                const data = buffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) {
                    data[i] = (Math.random() * 2 - 1) * (0.4 + 0.6 * Math.sin(i / 800));
                }
                const noise = ctx.createBufferSource();
                noise.buffer = buffer;
                const g = ctx.createGain();
                g.gain.setValueAtTime(0.0001, now);
                g.gain.linearRampToValueAtTime(0.22, now + 0.3);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
                const bp = ctx.createBiquadFilter();
                bp.type = 'bandpass';
                bp.frequency.setValueAtTime(900, now);
                bp.Q.setValueAtTime(6, now);
                noise.connect(bp); bp.connect(g); g.connect(ctx.destination);
                noise.start(now); noise.stop(now + 0.55);
            }
            else if (type === 'chant') {
                [82.41, 87.31, 98, 110].forEach((f, i) => {
                    const osc = ctx.createOscillator();
                    const g = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(f, now + i * 0.02);
                    osc.detune.setValueAtTime(i * 4, now);
                    g.gain.setValueAtTime(0.0001, now + i * 0.02);
                    g.gain.linearRampToValueAtTime(0.09, now + i * 0.02 + 0.4);
                    g.gain.exponentialRampToValueAtTime(0.001, now + 1.4);
                    osc.connect(g); g.connect(ctx.destination);
                    osc.start(now + i * 0.02); osc.stop(now + 1.5);
                });
            }
            else if (type === 'melt') {
                const osc = ctx.createOscillator();
                const g = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(1400, now);
                osc.frequency.linearRampToValueAtTime(120, now + 0.6);
                const vib = ctx.createOscillator();
                const vg = ctx.createGain();
                vib.frequency.setValueAtTime(22, now);
                vg.gain.setValueAtTime(60, now);
                vib.connect(vg); vg.connect(osc.frequency);
                g.gain.setValueAtTime(0.16, now);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
                osc.connect(g); g.connect(ctx.destination);
                osc.start(now); osc.stop(now + 0.65);
                vib.start(now); vib.stop(now + 0.65);
            }
            else if (type === 'glass') {
                const osc = ctx.createOscillator();
                const g = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(2400, now);
                osc.frequency.linearRampToValueAtTime(1500, now + 0.25);
                g.gain.setValueAtTime(0.18, now);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
                osc.connect(g); g.connect(ctx.destination);
                osc.start(now); osc.stop(now + 0.32);
            }
            else if (type === 'scream') {
                const osc = ctx.createOscillator();
                const g = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(300, now);
                osc.frequency.linearRampToValueAtTime(1800, now + 0.3);
                osc.frequency.linearRampToValueAtTime(200, now + 0.7);
                g.gain.setValueAtTime(0.25, now);
                g.gain.exponentialRampToValueAtTime(0.001, now + 0.75);
                const vib = ctx.createOscillator();
                const vg = ctx.createGain();
                vib.frequency.setValueAtTime(35, now);
                vg.gain.setValueAtTime(80, now);
                vib.connect(vg); vg.connect(osc.frequency);
                osc.connect(g); g.connect(ctx.destination);
                osc.start(now); osc.stop(now + 0.8);
                vib.start(now); vib.stop(now + 0.8);
            }'''

ENDING_RENDER_JS = r'''            document.getElementById('chapter-title').innerText = titleText;
            document.getElementById('speaker-name').innerText = speakerText;
            if (node.is_ending) {
                const overT = currentLang === 'ru' ? 'ИГРА ОКОНЧЕНА' : 'GAME OVER';
                const tag = currentLang === 'ru' ? node.ending_tag_ru : node.ending_tag_en;
                const route = currentLang === 'ru' ? node.route_ru : node.route_en;
                const take = currentLang === 'ru' ? node.takeaway_ru : node.takeaway_en;
                const lblSanity = currentLang === 'ru' ? 'Нейро-Рассудок' : 'Cyber-Sanity';
                const lblWill = currentLang === 'ru' ? 'Воля' : 'Willpower';
                const lblBlood = currentLang === 'ru' ? 'Инфекция' : 'Infection';
                document.getElementById('story-text').innerHTML =
                    '<div class="ending-banner"><span class="ending-over">' + overT + '</span>' +
                    '<span class="ending-tag">' + tag + '</span>' +
                    '<span class="ending-route">' + route + '</span></div>' +
                    '<div class="ending-stats">' +
                    '<span>' + lblSanity + ': ' + stats.sanity + '%</span>' +
                    '<span>' + lblWill + ': ' + stats.willpower + '</span>' +
                    '<span>' + lblBlood + ': ' + stats.blood + '</span>' +
                    '</div>' +
                    '<div class="ending-epilogue">' + bodyText.split('\n\n').map(function(p){return '<p>' + p + '</p>';}).join('') + '</div>' +
                    '<div class="ending-takeaway"><strong>' + (currentLang === 'ru' ? '📊 АНАЛИТИЧЕСКИЙ ВЫВОД:' : '📊 ANALYTICAL TAKEAWAY:') + '</strong> ' + take + '</div>';
            } else {
                document.getElementById('story-text').innerText = bodyText;
            }'''

ENDING_CHOICES_JS = r'''            if (node.is_ending) {
                const note = document.createElement('div');
                note.className = 'ending-restart-note';
                note.innerText = currentLang === 'ru' ? 'Вы достигли конца прохождения. Выберите другой вектор, чтобы увидеть другие исходы.' : 'You have reached the end of this playthrough. Choose a different vector to see other outcomes.';
                choicesBox.appendChild(note);
                const restartBtn = document.createElement('button');
                restartBtn.className = 'btn-choice';
                restartBtn.innerText = currentLang === 'ru' ? '↻ Перезапустить публицистическую новеллу' : '↻ Restart Publicist Visual Novel';
                restartBtn.onclick = () => restartGame();
                choicesBox.appendChild(restartBtn);
                return;
            }'''

ENDING_CSS = r'''        .ending-banner {
            border: 2px solid var(--glow-red);
            background: linear-gradient(180deg, rgba(220,20,60,0.25) 0%, rgba(8,6,8,0.95) 100%);
            padding: 16px 18px;
            margin-bottom: 14px;
            text-align: center;
            box-shadow: 0 0 24px rgba(220,20,60,0.35);
            animation: endpulse 2.2s ease-in-out infinite;
        }
        .ending-over {
            display: block;
            font-family: var(--font-title);
            font-weight: 900;
            font-size: 1.7rem;
            letter-spacing: 0.35em;
            color: var(--glow-red);
            text-shadow: 0 0 14px rgba(255,26,64,0.8);
        }
        .ending-tag {
            display: block;
            margin-top: 6px;
            font-weight: 700;
            font-size: 1.05rem;
            color: var(--text-gold);
            letter-spacing: 0.12em;
        }
        .ending-route {
            display: block;
            margin-top: 4px;
            font-size: 0.78rem;
            color: var(--neon-cyan);
            letter-spacing: 0.08em;
        }
        .ending-stats {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
            justify-content: center;
            margin: 12px 0;
            padding: 10px 12px;
            border: 1px solid rgba(0,216,255,0.35);
            background: rgba(0,216,255,0.06);
            font-size: 0.82rem;
            letter-spacing: 0.06em;
        }
        .ending-stats span {
            white-space: nowrap;
        }
        .ending-epilogue p {
            margin-bottom: 10px;
            line-height: 1.6;
        }
        .ending-takeaway {
            margin-top: 14px;
            padding: 12px 14px;
            border-left: 3px solid var(--text-gold);
            background: rgba(255,200,55,0.07);
            font-size: 0.86rem;
            line-height: 1.6;
            color: #f3ead2;
        }
        .ending-restart-note {
            font-size: 0.75rem;
            color: var(--neon-cyan);
            opacity: 0.85;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
            text-align: center;
        }
        @keyframes endpulse {
            0%,100% { box-shadow: 0 0 18px rgba(220,20,60,0.25); }
            50% { box-shadow: 0 0 34px rgba(220,20,60,0.6); }
        }'''


def main():
    src_path = "kobyla_has_waken_up.html"
    out_path = "kobyla_has_waken_up_expanded.html"
    html = open(src_path, encoding="utf-8").read()

    # 1) Replace storyData
    start_marker = "const storyData = {"
    start = html.find(start_marker)
    assert start != -1, "storyData marker not found"
    close = html.find("};", start)
    assert close != -1, "storyData close not found"
    new_json = json.dumps(story, ensure_ascii=False, indent=2)
    html = html[:start] + "const storyData = " + new_json + ";" + html[close + 2:]

    # 2) Add new music tracks
    anchor = "kickInterval: 1\n                    }\n                };"
    assert anchor in html, "tracks anchor not found"
    html = html.replace(anchor, "kickInterval: 1\n                    },\n" + NEW_TRACKS_JS + "\n                };", 1)

    # 3) Add new SFX branches
    sfx_anchor = "noise.stop(now + 0.2);\n            }\n        }"
    assert sfx_anchor in html, "sfx anchor not found"
    html = html.replace(sfx_anchor, "noise.stop(now + 0.2);\n            }\n" + NEW_SFX_JS + "\n        }", 1)

    # 4) Rich ending render for story-text
    text_anchor = "            document.getElementById('story-text').innerText = bodyText;"
    assert text_anchor in html, "story-text anchor not found"
    html = html.replace(text_anchor, ENDING_RENDER_JS, 1)

    # 5) Richer ending choices block
    ch_anchor = """            if (node.is_ending) {
                const restartBtn = document.createElement('button');
                restartBtn.className = 'btn-choice';
                restartBtn.innerText = currentLang === 'ru' ? ' Перезапустить публицистическую новеллу' : ' Restart Publicist Visual Novel';
                restartBtn.onclick = () => restartGame();
                choicesBox.appendChild(restartBtn);
                return;
            }"""
    assert ch_anchor in html, "ending choices anchor not found"
    html = html.replace(ch_anchor, ENDING_CHOICES_JS, 1)

    # 6) Ending CSS before </style>
    style_close = html.rfind("</style>")
    assert style_close != -1
    html = html[:style_close] + ENDING_CSS + "\n    " + html[style_close:]

    open(out_path, "w", encoding="utf-8").write(html)

    # Report
    ru = sum(len(v.get("text_ru", "")) for v in story.values())
    en = sum(len(v.get("text_en", "")) for v in story.values())
    print("OK ->", out_path)
    print("nodes:", len(story))
    print("text_ru chars:", ru, "| text_en chars:", en, "| total:", ru + en)
    print("endings:", sum(1 for v in story.values() if v.get("is_ending")))
    print("file size:", len(html))


if __name__ == "__main__":
    main()
