# -*- coding: utf-8 -*-
"""
Horror edition builder v5 (DREAD ENGINE - BRUTAL).
Base = kobyla_has_waken_up_novel.html.

Key upgrades over v4:
  - MUSIC DUCKING: the music engine now routes through a master gain bus; during
    horror ambience music is ducked to ~10%, and during scare impacts it is cut
    to 0 (silence before the hit = classic horror technique).
  - ENDING SCARES are scheduled via a direct horrorEnding() call in horrorCheck
    (no reliance on HORROR_EVENTS lookup for endings), fire at ~4.3s, and are
    MUCH bigger: impact + scream + mare (760ms) + 50px shake + strobe + noise
    storm + phrase, then second eyes-flash, third void-flash, corner echo,
    heartbeat, music fades back.
  - Scarier synthesized sounds: vocal-fry screams (vibrato + formant bandpass),
    AM-growls, impact booms, whisper-word syllables.
  - Shake disables the breath animation on #app-container so it always reads.
  - Reading area stays clean (noise carved out).
"""
import re, base64, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

MARE = {
    'wake':  b64('_assets/mare_wake.jpg'),
    'void':  b64('_assets/mare_void.jpg'),
    'teeth': b64('_assets/mare_teeth.jpg'),
    'eyes':  b64('_assets/mare_eyes.jpg'),
    'pale':  b64('_assets/mare_pale.jpg'),
    'leap':  b64('_assets/mare_leap.jpg'),
    'stare': b64('_assets/mare_stare.jpg'),
}

CSS = r'''
        /* ============ HORROR LAYER v5 (DREAD ENGINE - BRUTAL) ============ */
        #mare-layer {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            display: none; justify-content: center; align-items: center;
            z-index: 900; pointer-events: none; background: #000;
        }
        #mare-layer.mare-on { display: flex; }
        #mare-layer.blackout { display: flex; background: #000; }
        #mare-img {
            width: 100%; height: 100%; object-fit: cover;
            opacity: 0;
        }
        #mare-layer.mare-on #mare-img { animation: mareIn 0.07s steps(3) forwards; }
        #mare-layer.mare-void #mare-img,
        #mare-layer.mare-eyes #mare-img,
        #mare-layer.mare-pale #mare-img { filter: contrast(1.7) brightness(0.7); }
        #mare-layer.mare-teeth #mare-img { filter: contrast(1.55) saturate(1.5) brightness(0.82); }
        #mare-layer.mare-leap #mare-img { filter: contrast(1.65) saturate(1.7) brightness(0.78); }
        #mare-layer.mare-stare #mare-img { filter: contrast(1.5) brightness(0.9); }
        @keyframes mareIn {
            0% { transform: scale(1.1) translate(0,0); opacity: 0; }
            100% { transform: scale(1.5) translate(-2%, -3%); opacity: 1; }
        }
        #mare-layer.mare-corner {
            background: transparent; justify-content: flex-end; align-items: flex-end;
        }
        #mare-layer.mare-corner #mare-img {
            width: 30vw; min-width: 230px; height: auto; object-fit: contain;
            animation: cornerIn 0.1s steps(3) forwards;
        }
        @keyframes cornerIn {
            0% { transform: scale(1.05); opacity: 0; }
            100% { transform: scale(1.0); opacity: 1; }
        }
        #dread-text {
            position: fixed; inset: 0; display: none; align-items: center; justify-content: center;
            z-index: 945; pointer-events: none; text-align: center;
        }
        #dread-text.on { display: flex; }
        #dread-text span {
            font-family: var(--font-main); font-weight: 700;
            font-size: clamp(1.1rem, 3.4vw, 2.2rem); letter-spacing: 0.32em;
            color: rgba(255, 240, 240, 0.94);
            text-shadow: 0 0 18px rgba(255,26,64,0.85), 0 0 60px rgba(255,26,64,0.5);
            animation: dreadTextIn 0.08s steps(2) forwards;
        }
        @keyframes dreadTextIn {
            0% { opacity: 0; transform: translateX(-7px) skewX(-9deg); }
            100% { opacity: 1; transform: translateX(0) skewX(0); }
        }
        #wake-text {
            position: fixed; inset: 0; display: none; align-items: center; justify-content: center;
            z-index: 950; pointer-events: none; text-align: center;
        }
        #wake-text.on { display: flex; }
        #wake-text span {
            font-family: var(--font-title); font-weight: 900;
            font-size: clamp(2.4rem, 9vw, 6.5rem); letter-spacing: 0.18em;
            color: #fff; text-shadow: 0 0 30px var(--glow-red), 0 0 90px var(--glow-red), 3px 0 rgba(0,216,255,0.5), -3px 0 rgba(255,26,64,0.6);
            animation: wakeTextGlitch 0.3s steps(4) infinite;
            white-space: nowrap;
        }
        @keyframes wakeTextGlitch {
            0% { transform: translate(0,0) skewX(0); opacity: 1; }
            25% { transform: translate(-8px,2px) skewX(-8deg); opacity: 0.85; }
            50% { transform: translate(7px,-3px) skewX(6deg); opacity: 1; }
            75% { transform: translate(-5px,2px) skewX(-5deg); opacity: 0.9; }
            100% { transform: translate(0,0) skewX(0); opacity: 1; }
        }
        #noise-canvas {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: 80; pointer-events: none; opacity: 0.65;
        }
        #vignette {
            position: fixed; inset: 0; z-index: 86; pointer-events: none;
            background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.55) 78%, rgba(0,0,0,0.92) 100%);
            opacity: 0; transition: opacity 0.8s ease;
        }
        #vignette.vig-on { opacity: 1; }
        body.wake-mode #vignette {
            opacity: 1;
            background: radial-gradient(ellipse at center, rgba(120,0,0,0.16) 20%, rgba(30,0,0,0.55) 70%, rgba(0,0,0,0.97) 100%);
            animation: vigPulse 1.4s ease-in-out infinite;
        }
        @keyframes vigPulse { 0%,100% { opacity: 0.85; } 50% { opacity: 1; } }
        body.horror-mode #portrait-box { animation: breathe 3.0s ease-in-out infinite; }
        @keyframes breathe {
            0%,100% { transform: scale(1); filter: none; }
            50% { transform: scale(1.04); filter: brightness(1.15) saturate(1.4); }
        }
        body.horror-mode .eye-glow-overlay { animation: eyeGlow 2.0s ease-in-out infinite; }
        @keyframes eyeGlow {
            0%,100% { opacity: 0.45; filter: blur(1px); }
            50% { opacity: 1; filter: blur(4px); }
        }
        body.glitch #portrait-box {
            animation: portraitGlitch 0.24s steps(3) infinite;
            filter: contrast(1.7) saturate(2.6) hue-rotate(-20deg);
        }
        @keyframes portraitGlitch {
            0% { clip-path: inset(0 0 0 0); transform: translate(0,0); }
            25% { clip-path: inset(12% 0 38% 0); transform: translate(-10px,3px); }
            50% { clip-path: inset(55% 0 8% 0); transform: translate(9px,-3px); }
            75% { clip-path: inset(30% 0 30% 0); transform: translate(-6px,2px); }
            100% { clip-path: inset(0 0 0 0); transform: translate(0,0); }
        }
        body.dread-high #app-container { animation: breathScale 4s ease-in-out infinite; }
        @keyframes breathScale {
            0%,100% { transform: scale(1); }
            50% { transform: scale(1.014); }
        }
        body.dread-high { filter: sepia(0.35) hue-rotate(-18deg) saturate(1.55); }
        .btn-ctrl-danger { border-color: var(--glow-red) !important; }
        .btn-ctrl-danger:hover { box-shadow: 0 0 14px var(--glow-red) !important; }
'''

OVERLAYS = '''<!-- Horror Overlays -->
    <div id="mare-layer"><img id="mare-img" alt=""></div>
    <div id="wake-text"><span>КОБЫЛА ПРОСНУЛАСЬ.</span></div>
    <div id="dread-text"><span id="dread-text-span"></span></div>
    <canvas id="noise-canvas"></canvas>
    <div id="vignette"></div>

'''

HORROR_JS = r'''
        // ================= HORROR LAYER v5 (DREAD ENGINE - BRUTAL) =================
        const MARE_IMGS = {
            'wake':  'data:image/jpeg;base64,__W__',
            'void':  'data:image/jpeg;base64,__V__',
            'teeth': 'data:image/jpeg;base64,__T__',
            'eyes':  'data:image/jpeg;base64,__E__',
            'pale':  'data:image/jpeg;base64,__P__',
            'leap':  'data:image/jpeg;base64,__L__',
            'stare': 'data:image/jpeg;base64,__S__'
        };

        const HORROR = {
            enabled: true,
            timers: [], ambTimers: [], ambOn: false,
            lastNode: null, dread: 0, drone: null, beatInterval: 2600
        };

        const DREAD_PHRASES = [
            'НЕ ОБОРАЧИВАЙСЯ', 'ОНА СЛЫШИТ ТВОЁ СЕРДЦЕ', 'ЗА ТОБОЙ', 'ТЫ УЖЕ ЧАСТЬ ЕЁ',
            'ОНА ЗДЕСЬ', 'НЕ ДЫШИ', 'ОНА ВИДИТ ТЕБЯ', 'ТВОЁ ИМЯ В ЕЁ ЛОГАХ',
            'СМОТРИ В ГЛАЗА', 'ОНА УЖЕ ВНУТРИ', 'ЭТО НЕ СОН', 'ОТКРОЙ ГЛАЗА',
            'ПОЗАДИ', 'ОНА ИДЁТ ЗА ТОБОЙ', 'ОНА ПОМНИТ ТЕБЯ'
        ];

        const HORROR_EVENTS = {
            'AUDIT_LOGS':          [['glitch', 600], ['whisper', 1500], ['thud', 3200], ['mare-corner-mini', 5400]],
            'AUDIT_INFECTION':     [['sting', 400], ['mare-teeth', 1600]],
            'AUDIT_HALLWAY2':      [['heart', 800], ['whisper', 3400], ['scrape', 5200], ['corner', 6400]],
            'AUDIT_LAB_ENTRY':     [['drone-push', 400], ['breath', 2600], ['mare-small', 5200]],
            'BIO_HORROR':          [['wake', 700]],
            'ARIS_DEATH':          [['mare-teeth', 950], ['growl', 2700], ['voice-far', 4300]],
            'HIVE_PURGE':          [['sting', 400], ['roar', 1900], ['mare-small', 3600]],
            'FINAL_BOSS':          [['roar', 250], ['shake-big', 1600], ['mare-teeth', 2800]],
            'CORE_CONFRONTATION':  [['heart', 500], ['whisper-many', 2300], ['breath', 3600], ['knock', 5100], ['mare-stare', 6600]],
            'HACK_MATRIX':         [['glitch', 300], ['sting', 1400], ['corner', 3600]],
            'HACK_SNEAK':          [['knock', 1200], ['scrape', 3000], ['mare-corner-mini', 4600]],
            'HACK_DIVE':           [['void', 800], ['voice-far', 3600]],
            'HACK_VAULT':          [['mare-teeth', 700], ['whisper-many', 2300]],
            'BURN_ENTRY':          [['roar', 300], ['glitch', 1500], ['mare-small', 3400]],
            'BURN_CHARGE':         [['roar', 200], ['shake-big', 1200], ['mare-teeth', 2600]],
            'BURN_DARK':           [['void', 600], ['growl', 2100], ['whisper', 3300], ['mare-stare', 4600]],
            'BURN_STAMPEDE':       [['mare-teeth', 800], ['whisper-many', 2500]]
        };

        const AMBIENT_NODES = ['AUDIT_LOGS','AUDIT_INFECTION','AUDIT_HALLWAY2','AUDIT_LAB_ENTRY',
            'BIO_HORROR','ARIS_DEATH','HIVE_PURGE','FINAL_BOSS','CORE_CONFRONTATION',
            'HACK_MATRIX','HACK_SNEAK','HACK_DIVE','HACK_VAULT','BURN_DARK','BURN_STAMPEDE',
            'BURN_CHARGE','BURN_EMP','BURN_ENTRY'];

        function hrInit() {
            const nc = document.getElementById('noise-canvas');
            nc.width = window.innerWidth; nc.height = window.innerHeight;
            window.addEventListener('resize', () => { nc.width = window.innerWidth; nc.height = window.innerHeight; });
            requestAnimationFrame(noiseLoop);
        }

        let noiseOn = false;
        function noiseLoop() {
            const nc = document.getElementById('noise-canvas');
            const c = nc.getContext('2d');
            if (noiseOn || document.body.classList.contains('horror-mode')) {
                const img = c.createImageData(nc.width, nc.height);
                const d = img.data;
                const a = noiseOn ? 120 : (HORROR.dread > 60 ? 30 : 16);
                for (let i = 0; i < d.length; i += 4) {
                    const v = (Math.random() * 255) | 0;
                    d[i] = v; d[i+1] = v; d[i+2] = v; d[i+3] = (Math.random() * a) | 0;
                }
                c.putImageData(img, 0, 0);
                try {
                    const sc = document.querySelector('.story-container');
                    if (sc && sc.getBoundingClientRect) {
                        const r = sc.getBoundingClientRect();
                        c.clearRect(Math.floor(r.left) - 6, Math.floor(r.top) - 6, Math.ceil(r.width) + 12, Math.ceil(r.height) + 12);
                    }
                } catch (e) {}
            } else {
                c.clearRect(0, 0, nc.width, nc.height);
            }
            requestAnimationFrame(noiseLoop);
        }

        // ---------- MUSIC DUCK (kill the synthwave during scares) ----------
        function hrMusicDuck(v) {
            try {
                if (musicEngine.master && musicEngine.ctx) {
                    musicEngine.master.gain.setValueAtTime(v, musicEngine.ctx.currentTime);
                }
            } catch (e) {
                try { if (musicEngine.master) musicEngine.master.gain.value = v; } catch (e2) {}
            }
        }

        // ---------- SOUND core ----------
        function hrPlay(kind) {
            musicEngine.init();
            if (!musicEngine.ctx) return;
            const ctx = musicEngine.ctx;
            const now = ctx.currentTime;
            const out = ctx.destination;
            function osc(type, f0, f1, t0, dur, gain, dest) {
                const o = ctx.createOscillator(); const g = ctx.createGain();
                o.type = type; o.frequency.setValueAtTime(f0, t0);
                if (f1 !== null) o.frequency.exponentialRampToValueAtTime(Math.max(1, f1), t0 + dur);
                g.gain.setValueAtTime(0.0001, t0);
                g.gain.linearRampToValueAtTime(gain, t0 + 0.012);
                g.gain.exponentialRampToValueAtTime(0.001, t0 + dur);
                o.connect(g); g.connect(dest || out);
                o.start(t0); o.stop(t0 + dur + 0.05);
                return o;
            }
            function fnoise(dur, gain, lp, hp, t0) {
                t0 = t0 || now;
                const len = Math.floor(ctx.sampleRate * dur);
                const buf = ctx.createBuffer(1, len, ctx.sampleRate);
                const d = buf.getChannelData(0);
                for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 1.5);
                const src = ctx.createBufferSource(); src.buffer = buf;
                const g = ctx.createGain();
                g.gain.setValueAtTime(0.0001, t0);
                g.gain.linearRampToValueAtTime(gain, t0 + 0.012);
                g.gain.exponentialRampToValueAtTime(0.001, t0 + dur);
                src.connect(g);
                if (lp) { const f = ctx.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = lp; g.connect(f); f.connect(out); }
                else if (hp) { const f = ctx.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = hp; g.connect(f); f.connect(out); }
                else g.connect(out);
                src.start(t0); src.stop(t0 + dur + 0.05);
            }
            function whisp(vol, t0) {
                t0 = t0 || now;
                const len = Math.floor(ctx.sampleRate * (0.5 + Math.random() * 0.6));
                const buf = ctx.createBuffer(1, len, ctx.sampleRate);
                const d = buf.getChannelData(0);
                const rate = 60 + Math.random() * 300;
                for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (0.4 + 0.6 * Math.sin(i / rate));
                const src = ctx.createBufferSource(); src.buffer = buf;
                const bp = ctx.createBiquadFilter(); bp.type = 'bandpass';
                bp.frequency.value = 700 + Math.random() * 700; bp.Q.value = 5 + Math.random() * 4;
                const g = ctx.createGain();
                g.gain.setValueAtTime(0.0001, t0);
                g.gain.linearRampToValueAtTime(vol, t0 + 0.35);
                g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.55 + Math.random() * 0.4);
                src.connect(bp); bp.connect(g); g.connect(out);
                src.start(t0); src.stop(t0 + 1.2);
            }
            switch (kind) {
                case 'sting':
                    [520, 540, 570, 820, 1240].forEach((f, i) => osc('sawtooth', f, f * 1.9, now + i * 0.008, 0.5, 0.18));
                    fnoise(0.35, 0.5, 5000, 0);
                    break;
                case 'impact': {
                    fnoise(0.22, 0.75, 0, 900);
                    const o = ctx.createOscillator(); o.type = 'sine';
                    o.frequency.setValueAtTime(170, now); o.frequency.exponentialRampToValueAtTime(26, now + 0.4);
                    const g = ctx.createGain(); g.gain.setValueAtTime(0.85, now); g.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
                    o.connect(g); g.connect(out); o.start(now); o.stop(now + 0.5);
                    break;
                }
                case 'scream': {
                    const mk = (type, f0, f1, lf, ld, bpf, dur, gain) => {
                        const o = ctx.createOscillator(); o.type = type;
                        o.frequency.setValueAtTime(f0, now);
                        o.frequency.exponentialRampToValueAtTime(Math.max(1, f1), now + dur);
                        const lfo = ctx.createOscillator(); lfo.frequency.value = lf;
                        const lg = ctx.createGain(); lg.gain.value = ld;
                        lfo.connect(lg); lg.connect(o.frequency);
                        const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.frequency.value = bpf; bp.Q.value = 2.5;
                        const g = ctx.createGain();
                        g.gain.setValueAtTime(0.0001, now);
                        g.gain.linearRampToValueAtTime(gain, now + 0.03);
                        g.gain.exponentialRampToValueAtTime(0.001, now + dur);
                        o.connect(bp); bp.connect(g); g.connect(out);
                        o.start(now); o.stop(now + dur + 0.05); lfo.start(now); lfo.stop(now + dur + 0.05);
                    };
                    mk('sawtooth', 260, 1800, 47, 60, 1100, 0.6, 0.30);
                    mk('sawtooth', 320, 2200, 61, 55, 1500, 0.55, 0.24);
                    mk('square', 180, 900, 40, 40, 700, 0.6, 0.16);
                    const len = Math.floor(ctx.sampleRate * 0.6);
                    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
                    const dd = buf.getChannelData(0);
                    for (let i = 0; i < len; i++) dd[i] = (Math.random() * 2 - 1) * (0.3 + 0.7 * Math.sin(i / 90) * Math.sin(i / 9));
                    const src = ctx.createBufferSource(); src.buffer = buf;
                    const bp2 = ctx.createBiquadFilter(); bp2.type = 'bandpass';
                    bp2.frequency.setValueAtTime(2000, now); bp2.frequency.exponentialRampToValueAtTime(400, now + 0.5); bp2.Q.value = 3;
                    const ng = ctx.createGain(); ng.gain.setValueAtTime(0.0001, now); ng.gain.linearRampToValueAtTime(0.4, now + 0.02); ng.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
                    src.connect(bp2); bp2.connect(ng); ng.connect(out);
                    src.start(now); src.stop(now + 0.65);
                    const sub = ctx.createOscillator(); sub.type = 'sine';
                    sub.frequency.setValueAtTime(160, now); sub.frequency.exponentialRampToValueAtTime(30, now + 0.35);
                    const sg = ctx.createGain(); sg.gain.setValueAtTime(0.5, now); sg.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
                    sub.connect(sg); sg.connect(out); sub.start(now); sub.stop(now + 0.45);
                    break;
                }
                case 'shriek': {
                    const mk = (f0, f1, dur, gain) => {
                        const o = ctx.createOscillator(); o.type = 'sawtooth';
                        o.frequency.setValueAtTime(f0, now); o.frequency.exponentialRampToValueAtTime(Math.max(1, f1), now + dur);
                        const lfo = ctx.createOscillator(); lfo.frequency.value = 55;
                        const lg = ctx.createGain(); lg.gain.value = 50;
                        lfo.connect(lg); lg.connect(o.frequency);
                        const g = ctx.createGain();
                        g.gain.setValueAtTime(0.0001, now); g.gain.linearRampToValueAtTime(gain, now + 0.02); g.gain.exponentialRampToValueAtTime(0.001, now + dur);
                        o.connect(g); g.connect(out); o.start(now); o.stop(now + dur + 0.05); lfo.start(now); lfo.stop(now + dur + 0.05);
                    };
                    mk(1500, 3600, 0.3, 0.26); mk(1900, 2800, 0.25, 0.2);
                    fnoise(0.3, 0.45, 0, 3000);
                    break;
                }
                case 'roar': {
                    const o = ctx.createOscillator(); o.type = 'sawtooth';
                    o.frequency.setValueAtTime(75, now); o.frequency.exponentialRampToValueAtTime(38, now + 1.1);
                    const lfo = ctx.createOscillator(); lfo.frequency.value = 18;
                    const lg = ctx.createGain(); lg.gain.value = 26;
                    lfo.connect(lg); lg.connect(o.frequency);
                    const g = ctx.createGain();
                    g.gain.setValueAtTime(0.0001, now); g.gain.linearRampToValueAtTime(0.5, now + 0.05); g.gain.exponentialRampToValueAtTime(0.001, now + 1.15);
                    o.connect(g); g.connect(out); o.start(now); o.stop(now + 1.2); lfo.start(now); lfo.stop(now + 1.2);
                    const o2 = ctx.createOscillator(); o2.type = 'square';
                    o2.frequency.setValueAtTime(52, now); o2.frequency.exponentialRampToValueAtTime(26, now + 0.9);
                    const g2 = ctx.createGain(); g2.gain.setValueAtTime(0.3, now); g2.gain.exponentialRampToValueAtTime(0.001, now + 0.95);
                    o2.connect(g2); g2.connect(out); o2.start(now); o2.stop(now + 1);
                    fnoise(1.0, 0.5, 300, 0);
                    break;
                }
                case 'growl': {
                    const o = ctx.createOscillator(); o.type = 'sawtooth';
                    o.frequency.setValueAtTime(52, now); o.frequency.linearRampToValueAtTime(30, now + 1.0);
                    const lfo = ctx.createOscillator(); lfo.frequency.value = 11;
                    const lg = ctx.createGain(); lg.gain.value = 24;
                    lfo.connect(lg); lg.connect(o.frequency);
                    const g = ctx.createGain();
                    g.gain.setValueAtTime(0.0001, now); g.gain.linearRampToValueAtTime(0.36, now + 0.1); g.gain.exponentialRampToValueAtTime(0.001, now + 1.05);
                    o.connect(g); g.connect(out); o.start(now); o.stop(now + 1.1); lfo.start(now); lfo.stop(now + 1.1);
                    break;
                }
                case 'thud':
                    osc('sine', 130, 26, now, 0.5, 0.6);
                    fnoise(0.25, 0.3, 180, 0);
                    break;
                case 'knock': {
                    const seq = [0, 0.24, 0.62, 0.98];
                    seq.forEach(t => { osc('sine', 120 + Math.random() * 40, 30, now + t, 0.22, 0.5); });
                    break;
                }
                case 'scrape':
                    osc('sawtooth', 3000, 220, now, 0.8, 0.12);
                    fnoise(0.8, 0.22, 3000, 0);
                    break;
                case 'cry-far':
                    osc('sine', 1100, 2400, now, 0.6, 0.08);
                    osc('sine', 900, 1700, now + 0.1, 0.6, 0.06);
                    fnoise(0.6, 0.12, 0, 1500);
                    break;
                case 'chime':
                    osc('sine', 1660, 1600, now, 1.6, 0.07);
                    osc('sine', 2490, 2400, now + 0.02, 1.4, 0.04);
                    break;
                case 'musicbox': {
                    const notes = [1318.5, 1174.7, 987.8, 880, 1046.5, 1244.5];
                    const n = notes[Math.floor(Math.random() * notes.length)];
                    osc('sine', n, n * 0.98, now, 1.6, 0.06);
                    osc('sine', n * 2, n * 1.96, now + 0.01, 1.3, 0.03);
                    if (Math.random() < 0.5) { const n2 = notes[Math.floor(Math.random() * notes.length)]; osc('sine', n2, n2 * 0.98, now + 0.4 + Math.random() * 0.5, 1.4, 0.05); }
                    break;
                }
                case 'riser': {
                    osc('sawtooth', 70, 260, now, 0.7, 0.14);
                    fnoise(0.7, 0.3, 900, 0);
                    break;
                }
                case 'static-slam':
                    fnoise(0.4, 0.55, 0, 800);
                    break;
                case 'whisper-word': {
                    const syl = [0, 0.28, 0.55];
                    syl.forEach((off, idx) => {
                        const t0 = now + off;
                        const len = Math.floor(ctx.sampleRate * 0.24);
                        const buf = ctx.createBuffer(1, len, ctx.sampleRate);
                        const d = buf.getChannelData(0);
                        const rate = 90 + idx * 40;
                        for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (0.35 + 0.65 * Math.sin(i / rate));
                        const src = ctx.createBufferSource(); src.buffer = buf;
                        const bp = ctx.createBiquadFilter(); bp.type = 'bandpass';
                        bp.frequency.setValueAtTime(650 + idx * 180, t0); bp.Q.value = 8;
                        const g = ctx.createGain();
                        g.gain.setValueAtTime(0.0001, t0); g.gain.linearRampToValueAtTime(0.22, t0 + 0.05); g.gain.linearRampToValueAtTime(0.0001, t0 + 0.24);
                        src.connect(bp); bp.connect(g); g.connect(out);
                        src.start(t0); src.stop(t0 + 0.26);
                    });
                    break;
                }
                case 'voice-far':
                    osc('sawtooth', 120, 60, now, 1.4, 0.11);
                    osc('sawtooth', 96, 55, now + 0.06, 1.4, 0.09);
                    whisp(0.18, now);
                    break;
                case 'voice-calm': {
                    const o = ctx.createOscillator(); const g = ctx.createGain();
                    o.type = 'triangle'; o.frequency.setValueAtTime(210, now);
                    o.frequency.linearRampToValueAtTime(160, now + 1.2);
                    const vib = ctx.createOscillator(); const vg = ctx.createGain();
                    vib.frequency.value = 5; vg.gain.value = 14;
                    vib.connect(vg); vg.connect(o.frequency);
                    const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.frequency.value = 900; bp.Q.value = 3;
                    g.gain.setValueAtTime(0.0001, now);
                    g.gain.linearRampToValueAtTime(0.07, now + 0.3);
                    g.gain.exponentialRampToValueAtTime(0.001, now + 1.3);
                    o.connect(bp); bp.connect(g); g.connect(out);
                    o.start(now); o.stop(now + 1.35); vib.start(now); vib.stop(now + 1.35);
                    break;
                }
                case 'heart': {
                    osc('sine', 74, 28, now, 0.13, 0.55);
                    osc('sine', 62, 24, now + 0.17, 0.11, 0.45);
                    fnoise(0.12, 0.22, 200, 0);
                    fnoise(0.10, 0.16, 200, 0, now + 0.17);
                    break;
                }
                case 'whisper': whisp(0.24); break;
                case 'whisper-many':
                    whisp(0.26); setTimeout(() => whisp(0.3, musicEngine.ctx.currentTime), 240);
                    setTimeout(() => whisp(0.3, musicEngine.ctx.currentTime), 480);
                    hrGlitch(180);
                    break;
                case 'breath':
                    for (let i = 0; i < 3; i++) {
                        const t = now + i * 1.3;
                        const len = Math.floor(ctx.sampleRate * 1.1);
                        const buf = ctx.createBuffer(1, len, ctx.sampleRate);
                        const d = buf.getChannelData(0);
                        for (let j = 0; j < len; j++) d[j] = (Math.random() * 2 - 1) * Math.sin(Math.PI * j / len);
                        const src = ctx.createBufferSource(); src.buffer = buf;
                        const f = ctx.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = 420;
                        const g = ctx.createGain();
                        g.gain.setValueAtTime(0.0001, t);
                        g.gain.linearRampToValueAtTime(0.16, t + 0.45);
                        g.gain.linearRampToValueAtTime(0.001, t + 1.1);
                        src.connect(f); f.connect(g); g.connect(out);
                        src.start(t); src.stop(t + 1.15);
                    }
                    break;
                case 'static': fnoise(0.3, 0.22, 0, 2500); break;
            }
        }

        // ---------- LOW DRONE ----------
        function hrDroneStart() {
            if (HORROR.drone) return;
            const ctx = musicEngine.ctx;
            const g = ctx.createGain(); g.gain.value = 0.0;
            const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 240;
            g.connect(lp); lp.connect(ctx.destination);
            const oscs = [];
            [38.2, 40.6, 30.4].forEach(f => {
                const o = ctx.createOscillator();
                o.type = 'sawtooth'; o.frequency.value = f;
                o.connect(g); o.start(); oscs.push(o);
            });
            const sub = ctx.createOscillator();
            sub.type = 'sine'; sub.frequency.value = 24.0;
            sub.connect(g); sub.start(); oscs.push(sub);
            HORROR.drone = { g: g, lp: lp, oscs: oscs };
        }
        function hrDroneSet(level) {
            if (!HORROR.drone) return;
            HORROR.drone.g.gain.value = 0.03 + level * 0.2;
            HORROR.drone.lp.frequency.value = 180 + level * 280;
        }
        function hrDroneStop() {
            if (HORROR.drone) {
                try {
                    HORROR.drone.g.gain.value = 0.0;
                    HORROR.drone.oscs.forEach(o => { try { o.stop(); } catch (e) {} });
                } catch (e) {}
                HORROR.drone = null;
            }
        }

        // ---------- VISUAL primitives ----------
        function hrShake(ms, amp) {
            const el = document.getElementById('app-container');
            el.style.animation = 'none';
            const t0 = Date.now();
            const id = setInterval(() => {
                const dt = Date.now() - t0;
                if (dt >= ms) { clearInterval(id); el.style.transform = ''; el.style.animation = ''; return; }
                const k = amp * (1 - dt / ms);
                el.style.transform = 'translate(' + (Math.random() * 2 - 1) * k + 'px,' + (Math.random() * 2 - 1) * k + 'px) rotate(' + (Math.random() * 2 - 1) * k * 0.2 + 'deg)';
            }, 16);
        }
        function hrFlash(kind, ms) {
            const flash = document.getElementById('screen-flash');
            flash.className = 'screen-flash ' + (kind === 'red' ? 'flash-red' : 'flash-white');
            setTimeout(() => flash.className = 'screen-flash', ms || 300);
        }
        function hrStrobe(n) {
            let count = 0;
            const id = setInterval(() => {
                hrFlash(count % 2 === 0 ? 'red' : 'white', 60);
                count++;
                if (count >= n) clearInterval(id);
            }, 110);
        }
        function hrMare(kind, ms) {
            const layer = document.getElementById('mare-layer');
            const img = document.getElementById('mare-img');
            const key = ['void','teeth','eyes','pale','leap','stare'].indexOf(kind) !== -1 ? kind : 'wake';
            img.src = MARE_IMGS[key];
            layer.className = 'mare-on mare-' + key;
            setTimeout(() => { layer.className = ''; }, ms || 300);
        }
        function hrCorner(ms) {
            const layer = document.getElementById('mare-layer');
            const img = document.getElementById('mare-img');
            img.src = MARE_IMGS['wake'];
            layer.className = 'mare-on mare-corner';
            setTimeout(() => { layer.className = ''; }, ms || 140);
        }
        function hrBlackout(ms) {
            const layer = document.getElementById('mare-layer');
            layer.className = 'blackout';
            setTimeout(() => { if (!layer.classList.contains('mare-on')) layer.className = ''; }, ms || 200);
        }
        function hrWakeText(ms) {
            const t = document.getElementById('wake-text');
            t.className = 'on';
            setTimeout(() => t.className = '', ms || 1300);
        }
        function hrDreadText(ms) {
            const t = document.getElementById('dread-text');
            const sp = document.getElementById('dread-text-span');
            const txt = DREAD_PHRASES[Math.floor(Math.random() * DREAD_PHRASES.length)];
            if (sp) sp.textContent = txt;
            t.classList.add('on');
            setTimeout(() => t.classList.remove('on'), ms || 130);
        }
        function hrDreadTextFixed(txt, ms) {
            const t = document.getElementById('dread-text');
            const sp = document.getElementById('dread-text-span');
            if (sp) sp.textContent = txt;
            t.classList.add('on');
            setTimeout(() => t.classList.remove('on'), ms || 140);
        }
        function hrGlitch(ms) {
            document.body.classList.add('glitch');
            hrPlay('static');
            noiseOn = true;
            setTimeout(() => {
                document.body.classList.remove('glitch');
                setTimeout(() => { if (!HORROR.ambOn) noiseOn = false; }, 220);
            }, ms || 350);
        }
        function hrVig(on) {
            const v = document.getElementById('vignette');
            if (on) v.classList.add('vig-on'); else v.classList.remove('vig-on');
        }

        // ---------- DREAD ENGINE ----------
        function dreadSet(d) {
            HORROR.dread = Math.max(0, Math.min(100, d));
            document.body.classList.toggle('dread-high', HORROR.dread > 55);
            hrDroneSet(HORROR.dread / 100);
            const iv = 2600 - Math.floor(HORROR.dread / 100 * 1900);
            if (iv !== HORROR.beatInterval) { HORROR.beatInterval = iv; }
        }

        function scareBuild(then) {
            hrMusicDuck(0);
            hrPlay('riser');
            hrVig(true);
            hrShake(260, 6);
            setTimeout(() => { hrMusicDuck(0); then(); }, 700);
        }

        function noiseStorm(ms) {
            noiseOn = true;
            document.body.classList.add('glitch');
            setTimeout(() => {
                document.body.classList.remove('glitch');
                setTimeout(() => { if (!HORROR.ambOn) noiseOn = false; }, 300);
            }, ms);
        }

        function wakeScare() {
            cancelHorrorTimers(); stopAmb();
            hrMusicDuck(0);
            hrVig(true);
            document.body.classList.add('wake-mode');
            dreadSet(100);
            hrBlackout(260);
            setTimeout(() => {
                hrPlay('impact');
                hrPlay('scream');
                hrMare('leap', 800);
                hrShake(1100, 46);
                hrFlash('red', 460);
                hrStrobe(5);
                noiseStorm(1200);
                hrWakeText(1800);
                setTimeout(() => { hrMare('teeth', 200); hrPlay('shriek'); hrFlash('red', 240); hrShake(600, 30); }, 420);
                setTimeout(() => { hrMare('stare', 260); hrPlay('growl'); hrFlash('white', 180); hrShake(700, 30); }, 1250);
                setTimeout(() => { hrCorner(170); hrPlay('whisper-word'); }, 2200);
                setTimeout(() => { hrMusicDuck(0.3); hrPlay('heart'); }, 3000);
                setTimeout(() => { hrMusicDuck(1); }, 5200);
            }, 260);
            setTimeout(() => { document.body.classList.remove('wake-mode'); }, 4600);
            setTimeout(() => { hrVig(true); startAmb(); dreadSet(70); }, 1900);
        }

        // ---------- ENDING SCARES (guaranteed direct schedule) ----------
        function horrorEnding(id) {
            cancelHorrorTimers(); stopAmb();
            const cfg = {
                'ENDING_AUDIT':  [['whisper-fade', 700], ['static-slam', 1800], ['drone-push', 3000], ['final-audit', 4300]],
                'ENDING_UPLOAD': [['breath', 700], ['whisper-fade', 2100], ['drone-push', 3200], ['final-upload', 4300]],
                'ENDING_PURGE':  [['thud', 500], ['breath', 1700], ['drone-push', 2900], ['final-purge', 4300]],
                'ENDING_CHAOS':  [['whisper-fade', 700], ['cry-far', 2000], ['drone-push', 3000], ['final-chaos', 4300]]
            };
            const list = cfg[id];
            if (!list) return;
            list.forEach(ev => {
                HORROR.timers.push(setTimeout(() => hrEvent(ev[0]), ev[1]));
            });
        }

        function finalScare(mareKey, sound, phrase) {
            cancelHorrorTimers(); stopAmb();
            dreadSet(100);
            hrMusicDuck(0);
            setTimeout(() => {
                hrBlackout(220);
                setTimeout(() => {
                    hrPlay('impact');
                    hrPlay(sound);
                    hrMare(mareKey, 780);
                    hrShake(1400, 50);
                    hrFlash('red', 460);
                    hrStrobe(5);
                    noiseStorm(1200);
                    hrDreadTextFixed(phrase, 2800);
                    setTimeout(() => { hrMare('eyes', 190); hrPlay('shriek'); hrFlash('white', 150); hrShake(520, 24); }, 440);
                    setTimeout(() => { hrMare('void', 240); hrPlay('growl'); hrFlash('red', 280); hrShake(700, 30); }, 1250);
                    setTimeout(() => { hrCorner(180); hrPlay('whisper-word'); }, 2150);
                    setTimeout(() => { hrMusicDuck(0.35); hrPlay('heart'); }, 3000);
                    setTimeout(() => { hrMusicDuck(1); }, 5400);
                }, 220);
            }, 120);
        }

        function hrEvent(kind) {
            if (!HORROR.enabled) {
                if (kind === 'wake') { hrFlash('red', 250); hrWakeText(1200); }
                return;
            }
            switch (kind) {
                case 'glitch': hrGlitch(360); hrFlash('white', 90); dreadSet(HORROR.dread + 5); break;
                case 'whisper': hrPlay('whisper'); hrVig(true); setTimeout(() => hrVig(false), 900); break;
                case 'whisper-many': hrPlay('whisper-many'); hrVig(true); setTimeout(() => hrVig(false), 1400); break;
                case 'thud': hrPlay('thud'); hrShake(260, 7); break;
                case 'knock': hrPlay('knock'); hrVig(true); setTimeout(() => hrVig(false), 1500); break;
                case 'scrape': hrPlay('scrape'); hrShake(300, 7); break;
                case 'cry-far': hrPlay('cry-far'); hrVig(true); setTimeout(() => hrVig(false), 2000); break;
                case 'musicbox': hrPlay('musicbox'); break;
                case 'chime': hrPlay('chime'); hrVig(true); setTimeout(() => hrVig(false), 1200); break;
                case 'static-slam': hrPlay('static-slam'); hrGlitch(320); hrFlash('white', 110); break;
                case 'sting': hrPlay('sting'); hrFlash('red', 260); hrShake(550, 14); dreadSet(HORROR.dread + 7); break;
                case 'corner': hrCorner(160); hrPlay('whisper'); hrShake(300, 9); dreadSet(HORROR.dread + 3); break;
                case 'mare-corner-mini': hrCorner(130); hrPlay('shriek'); hrFlash('red', 160); hrShake(400, 14); break;
                case 'mare-small':
                    scareBuild(() => { hrMare('wake', 340); hrPlay('scream'); hrFlash('red', 260); hrShake(600, 24); dreadSet(HORROR.dread + 10); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3000); });
                    break;
                case 'mare-teeth':
                    scareBuild(() => { hrMare('teeth', 380); hrPlay('scream'); hrFlash('red', 300); hrShake(650, 26); dreadSet(HORROR.dread + 12); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3200); });
                    break;
                case 'mare-stare':
                    scareBuild(() => { hrMare('stare', 440); hrPlay('shriek'); hrFlash('white', 220); hrShake(700, 26); dreadSet(HORROR.dread + 14); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3200); });
                    break;
                case 'wake': wakeScare(); break;
                case 'roar': hrPlay('roar'); hrShake(650, 22); hrFlash('red', 300); dreadSet(HORROR.dread + 8); break;
                case 'shake-big': hrPlay('roar'); hrShake(850, 32); hrFlash('red', 360); noiseStorm(700); break;
                case 'void':
                    hrBlackout(130);
                    setTimeout(() => { hrMare('void', 560); hrPlay('shriek'); hrShake(600, 26); hrBlackout(150); dreadSet(HORROR.dread + 12); }, 140);
                    break;
                case 'heart': hrPlay('heart'); break;
                case 'breath': hrPlay('breath'); hrVig(true); break;
                case 'growl': hrPlay('growl'); hrShake(340, 10); break;
                case 'drone-push': dreadSet(HORROR.dread + 12); hrPlay('growl'); break;
                case 'whisper-fade': hrPlay('whisper'); hrVig(true); setTimeout(() => hrVig(false), 3000); break;
                case 'voice-far': hrPlay('voice-far'); hrVig(true); setTimeout(() => hrVig(false), 2500); break;
                /* per-ending finals */
                case 'final-audit': finalScare('stare', 'voice-far', 'Я ПОДОЖДУ.'); break;
                case 'final-upload': finalScare('teeth', 'scream', 'МЫ — ОДНО.'); break;
                case 'final-purge': finalScare('void', 'roar', 'ТЫ УНИЧТОЖИЛ МЕНЯ, НЕ ПОНЯВ МЕНЯ.'); break;
                case 'final-chaos': finalScare('pale', 'voice-calm', 'ОНА УЖЕ ВЕЗДЕ.'); break;
            }
        }

        function cancelHorrorTimers() {
            HORROR.timers.forEach(clearTimeout);
            HORROR.timers = [];
        }

        // ---------- AMBIENT DREAD LOOP (BRUTAL) ----------
        function startAmb() {
            if (HORROR.ambOn) return;
            HORROR.ambOn = true;
            document.body.classList.add('horror-mode');
            hrVig(true);
            hrDroneStart();
            hrMusicDuck(0.1);
            const t = [];
            t.push(setInterval(() => { if (HORROR.enabled) { hrPlay('heart'); } }, HORROR.beatInterval));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.55 + HORROR.dread / 150) hrPlay('whisper'); }, 2800));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.15 + HORROR.dread / 220) hrPlay('whisper-word'); }, 11000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.4 + HORROR.dread / 180) hrPlay('knock'); }, 12000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.4 + HORROR.dread / 220) hrPlay('cry-far'); }, 17000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.55 + HORROR.dread / 140) hrPlay('musicbox'); }, 10000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.45 + HORROR.dread / 200) { hrPlay('scrape'); hrShake(220, 6); } }, 14000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.3 + HORROR.dread / 180) hrPlay('chime'); }, 22000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.3 + HORROR.dread / 220) { hrPlay('static-slam'); hrGlitch(260); } }, 24000));
            t.push(setInterval(() => {
                if (!HORROR.enabled) return;
                const p = 0.1 + HORROR.dread * 0.0024;
                if (Math.random() < p) {
                    if (Math.random() < 0.4) { hrFlash('white', 80); hrPlay('thud'); hrGlitch(140); }
                    else { hrPlay('thud'); hrShake(280, 9); }
                    if (HORROR.dread > 40 && Math.random() < 0.5) hrCorner(150);
                }
            }, 8000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.35 + HORROR.dread / 150) hrDreadText(120); }, 4600));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.16 + HORROR.dread / 250) { hrBlackout(45); hrPlay('thud'); } }, 11000));
            t.push(setInterval(() => { if (HORROR.dread > 0) dreadSet(HORROR.dread - 0.8); }, 6000));
            t.push(setInterval(() => { if (HORROR.enabled && HORROR.dread < 70) dreadSet(HORROR.dread + 3); }, 18000));
            HORROR.ambTimers = HORROR.ambTimers.concat(t);
        }

        function stopAmb() {
            HORROR.ambOn = false;
            HORROR.ambTimers.forEach(clearInterval);
            HORROR.ambTimers = [];
            document.body.classList.remove('horror-mode');
            hrVig(false);
            document.body.classList.remove('glitch');
            noiseOn = false;
            hrDroneStop();
            hrMusicDuck(1);
        }

        function horrorCheck() {
            const nodeId = currentNodeId;
            if (nodeId === HORROR.lastNode) return;
            HORROR.lastNode = nodeId;
            cancelHorrorTimers(); stopAmb();
            const nd = storyData[nodeId];
            if (nd && nd.is_ending) { horrorEnding(nodeId); return; }
            if (HORROR_EVENTS[nodeId]) {
                HORROR_EVENTS[nodeId].forEach(ev => {
                    HORROR.timers.push(setTimeout(() => hrEvent(ev[0]), ev[1]));
                });
            }
            if (AMBIENT_NODES.indexOf(nodeId) !== -1) {
                HORROR.timers.push(setTimeout(() => startAmb(), 1200));
            }
        }

        function toggleScreamers() {
            HORROR.enabled = !HORROR.enabled;
            const btn = document.getElementById('btn-screamers');
            btn.innerText = HORROR.enabled ? '👁 СКРИМЕРЫ: ВКЛ' : '👁 СКРИМЕРЫ: ВЫКЛ';
            if (!HORROR.enabled) { cancelHorrorTimers(); stopAmb(); hrPlay('thud'); dreadSet(0); }
        }

        function triggerWake() { wakeScare(); }
'''

MUSIC_ENGINE_PATCHES = [
    # 1) master bus in constructor
    ("                this.activeTrack = 'ambient';",
     "                this.activeTrack = 'ambient';\n                this.master = null;"),
    # 2) master bus creation in init()
    ("""            init() {
                if (!this.ctx) {
                    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
                }
            }""",
     """            init() {
                if (!this.ctx) {
                    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
                    this.master = this.ctx.createGain();
                    this.master.gain.value = 1;
                    this.master.connect(this.ctx.destination);
                }
            }"""),
    # 3) route the 3 music voices through the master bus
    ("                    gain.connect(this.ctx.destination);",
     "                    gain.connect(this.master);"),
    ("                    kickGain.connect(this.ctx.destination);",
     "                    kickGain.connect(this.master);"),
    ("                arpGain.connect(this.ctx.destination);",
     "                arpGain.connect(this.master);"),
]


def main():
    src = 'kobyla_has_waken_up_novel.html'
    out = 'kobyla_has_waken_up.html'
    h = open(src, encoding='utf-8').read()

    # A) music engine master bus patches
    for old, new in MUSIC_ENGINE_PATCHES:
        assert h.count(old) >= 1, 'music patch anchor not found: ' + old[:60]
        h = h.replace(old, new, 1)

    # B) header buttons
    a = '<button class="btn-ctrl" id="btn-novel" onclick="openNovel()">📖 РОМАН</button>'
    assert a in h, 'header anchor not found'
    h = h.replace(a,
                  '<button class="btn-ctrl" id="btn-screamers" onclick="toggleScreamers()">👁 СКРИМЕРЫ: ВКЛ</button>\n                <button class="btn-ctrl btn-ctrl-danger" id="btn-wake" onclick="triggerWake()">🐴 ПОБУДИТЬ</button>\n                ' + a, 1)

    # C) overlays before <!-- Modal -->
    a = '<!-- Modal -->'
    assert a in h
    h = h.replace(a, OVERLAYS + a, 1)

    # D) CSS
    style_close = h.rfind('</style>')
    assert style_close != -1
    h = h[:style_close] + CSS + '\n    ' + h[style_close:]

    # E) horror JS before window.onload
    onload = 'window.onload = () => {'
    assert onload in h
    js = HORROR_JS
    js = js.replace('__W__', MARE['wake']).replace('__V__', MARE['void'])
    js = js.replace('__T__', MARE['teeth']).replace('__E__', MARE['eyes']).replace('__P__', MARE['pale'])
    js = js.replace('__L__', MARE['leap']).replace('__S__', MARE['stare'])
    h = h.replace(onload, js + '\n\n        ' + onload, 1)

    # F) hook horrorCheck into updateUI (before ending branch)
    anchor = '''            historyLog.push({ speaker: speakerText, text: bodyText });'''
    assert anchor in h, 'historyLog anchor not found'
    h = h.replace(anchor, anchor + '''\n\n            horrorCheck();''', 1)

    # G) hrInit in onload
    h = h.replace('window.onload = () => {', 'window.onload = () => {\n            hrInit();', 1)

    open(out, 'w', encoding='utf-8').write(h)
    print('OK ->', out)
    print('size:', len(h))


if __name__ == '__main__':
    main()
