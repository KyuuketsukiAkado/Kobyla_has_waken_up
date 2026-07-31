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
    'shadow': b64('_assets/mare_shadow.jpg'),
    'eye':    b64('_assets/mare_eye.jpg'),
    'flesh':  b64('_assets/mare_flesh.jpg'),
    'charge': b64('_assets/mare_charge.jpg'),
    'soul':   b64('_assets/mare_soul.jpg'),
    'grin':   b64('_assets/mare_grin.jpg'),
    'reach':  b64('_assets/mare_reach.jpg'),
    'behind': b64('_assets/mare_behind.jpg'),
    'crack':  b64('_assets/mare_crackscreen.jpg'),
    'rot':    b64('_assets/mare_rot.jpg'),
    'turn':   b64('_assets/mare_turn.jpg'),
    'maw':    b64('_assets/mare_maw.jpg'),
    'hand':   b64('_assets/mare_hand.jpg'),
    # v9 — LUTO-2: new, harder-hitting stills
    'face':   b64('_assets/mare_face.jpg'),      # full-frame maw of teeth (worst jumpscare)
    'refl':   b64('_assets/mare_reflection.jpg'),# she is behind you — seen in the monitor glass
    'ceil':   b64('_assets/mare_ceiling.jpg'),   # clinging to the ceiling, head hanging down
    'whites': b64('_assets/mare_whites.jpg'),    # only eyes+teeth out of pure black
    'lean':   b64('_assets/mare_lean.jpg'),      # leaning into your personal space
    'bed':    b64('_assets/mare_bed.jpg'),       # standing over your bed (sleep paralysis)
    # v10 — FOURTH WALL: she is in YOUR devices
    'webcam': b64('_assets/mare_webcam.jpg'),    # staring through your camera
    'door':   b64('_assets/mare_door.jpg'),      # standing in the doorway across the room
    'phone':  b64('_assets/mare_phone.jpg'),     # reflected in your phone screen
    'split':  b64('_assets/mare_split.jpg'),     # face splitting open into a maw
}

def b64mp3(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

VOICE = {
    'turn':   b64mp3('_assets/voice_turn.mp3'),
    'mirror': b64mp3('_assets/voice_mirror.mp3'),
    'watch':  b64mp3('_assets/voice_watch.mp3'),
    'close':  b64mp3('_assets/voice_close.mp3'),
    'woke':   b64mp3('_assets/voice_woke.mp3'),
    'name':   b64mp3('_assets/voice_name.mp3'),
}

CSS = r'''
        /* ============ HORROR LAYER v5 (DREAD ENGINE - BRUTAL) ============ */
        /* ---- v10: name-capture gate (fourth wall) ---- */
        #name-gate {
            position: fixed; inset: 0; z-index: 995; display: none;
            align-items: center; justify-content: center;
            background: radial-gradient(ellipse at center, rgba(20,0,4,0.92), rgba(0,0,0,0.98));
            font-family: var(--font-main);
        }
        #name-gate.on { display: flex; }
        #name-gate .ng-box {
            width: min(92vw, 560px); padding: 2.2em 2em;
            background: #0b0810; border: 1px solid rgba(220,20,60,0.6);
            box-shadow: 0 0 40px rgba(0,0,0,0.9), 0 0 0 1px rgba(255,26,64,0.25);
            text-align: center;
        }
        #name-gate .ng-head {
            font-family: 'Courier New', monospace; color: #ff3b53; letter-spacing: 0.08em;
            font-size: clamp(0.72rem, 2.4vw, 0.95rem); text-shadow: 0 0 10px rgba(255,26,64,0.7);
            margin-bottom: 1em;
        }
        #name-gate .ng-sub { color: #cdd3d6; font-size: clamp(0.82rem, 2.5vw, 1rem); line-height: 1.5; margin-bottom: 1.4em; }
        #name-gate input {
            width: 100%; box-sizing: border-box; padding: 0.75em 0.9em; margin-bottom: 1.2em;
            background: #05060a; border: 1px solid rgba(220,20,60,0.5); color: #eef2f3;
            font-family: 'Courier New', monospace; font-size: 1.1rem; letter-spacing: 0.04em; outline: none;
            text-align: center;
        }
        #name-gate input:focus { border-color: #ff3b53; box-shadow: 0 0 14px rgba(255,26,64,0.5); }
        #name-gate .ng-row { display: flex; gap: 0.8em; justify-content: center; }
        #name-gate .ng-btn {
            padding: 0.6em 1.4em; background: transparent; color: #ff6076;
            border: 1px solid rgba(220,20,60,0.7); cursor: pointer; letter-spacing: 0.08em;
            font-family: var(--font-main); font-weight: 700; transition: all 0.2s;
        }
        #name-gate .ng-btn:hover { background: rgba(220,20,60,0.18); box-shadow: 0 0 14px rgba(255,26,64,0.5); }
        #name-gate .ng-skip { color: #7a828a; border-color: rgba(120,120,130,0.4); font-weight: 400; }

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
        #mare-layer.mare-charge #mare-img { filter: contrast(1.7) saturate(1.8) brightness(0.8); }
        #mare-layer.mare-eye #mare-img { filter: contrast(1.6) brightness(0.95); }
        #mare-layer.mare-flesh #mare-img { filter: contrast(1.5) saturate(1.6) brightness(0.78); }
        #mare-layer.mare-shadow #mare-img { filter: contrast(1.4) brightness(0.6); }
        #mare-layer.mare-soul #mare-img { filter: contrast(1.55) brightness(0.92) saturate(1.2); }
        #mare-layer.mare-grin #mare-img { filter: contrast(1.6) saturate(1.5) brightness(0.85); }
        #mare-layer.mare-reach #mare-img { filter: contrast(1.7) saturate(1.7) brightness(0.82); }
        #mare-layer.mare-behind #mare-img { filter: contrast(1.4) brightness(0.7); }
        #mare-layer.mare-crack #mare-img { filter: contrast(1.65) saturate(1.4) brightness(0.9); }
        #mare-layer.mare-rot #mare-img { filter: contrast(1.5) brightness(0.72) saturate(0.85); }
        #mare-layer.mare-turn #mare-img { filter: contrast(1.45) brightness(0.85) saturate(1.15); }
        #mare-layer.mare-maw #mare-img { filter: contrast(1.7) saturate(1.7) brightness(0.85); }
        #mare-layer.mare-hand #mare-img { filter: contrast(1.55) saturate(1.4) brightness(0.82); }
        #mare-layer.mare-face #mare-img { filter: contrast(1.75) saturate(1.6) brightness(0.9); }
        #mare-layer.mare-refl #mare-img { filter: contrast(1.5) brightness(0.78) saturate(1.2); }
        #mare-layer.mare-ceil #mare-img { filter: contrast(1.6) brightness(0.72) saturate(1.3); }
        #mare-layer.mare-whites #mare-img { filter: contrast(1.9) brightness(1.0); }
        #mare-layer.mare-lean #mare-img { filter: contrast(1.7) saturate(1.6) brightness(0.88); }
        #mare-layer.mare-bed #mare-img { filter: contrast(1.55) brightness(0.7) saturate(1.15); }
        #mare-layer.mare-webcam #mare-img { filter: contrast(1.4) brightness(0.85) saturate(0.9) hue-rotate(60deg); }
        #mare-layer.mare-door #mare-img { filter: contrast(1.5) brightness(0.6) saturate(1.2); }
        #mare-layer.mare-phone #mare-img { filter: contrast(1.55) brightness(0.75) saturate(1.15); }
        #mare-layer.mare-split #mare-img { filter: contrast(1.75) saturate(1.7) brightness(0.9); }
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
        .btn-ctrl-danger { border-color: var(--glow-red) !important; }
        .btn-ctrl-danger:hover { box-shadow: 0 0 14px var(--glow-red) !important; }
        /* ================= FAKE SYSTEM CRASH (fourth-wall) ================= */
        #syscrash {
            position: fixed; inset: 0; z-index: 990; display: none;
            background: #05060a; color: #c8d0d8;
            font-family: 'Courier New', ui-monospace, monospace;
            padding: 5vh 6vw; overflow: hidden; cursor: none;
        }
        #syscrash.on { display: block; }
        #syscrash.bsod { background: #0a0026; color: #d8dcff; }
        #syscrash.panic { background: #120003; color: #ffd7d7; }
        #syscrash .sc-scan {
            position: absolute; inset: 0; pointer-events: none; opacity: 0.5;
            background: repeating-linear-gradient(0deg, rgba(0,0,0,0) 0px, rgba(0,0,0,0) 2px, rgba(0,0,0,0.35) 3px, rgba(0,0,0,0) 4px);
            mix-blend-mode: multiply; animation: scRoll 0.5s linear infinite;
        }
        @keyframes scRoll { 0% { transform: translateY(0); } 100% { transform: translateY(4px); } }
        #syscrash .sc-head {
            font-size: clamp(1rem, 3.2vw, 1.9rem); font-weight: 700; letter-spacing: 0.06em;
            margin-bottom: 1.2em; text-shadow: 0 0 10px currentColor;
        }
        #syscrash .sc-body { font-size: clamp(0.72rem, 1.9vw, 1.05rem); line-height: 1.55; white-space: pre-wrap; }
        #syscrash .sc-body .c-ok { color: #37e07a; }
        #syscrash .sc-body .c-err { color: #ff3b53; text-shadow: 0 0 8px rgba(255,26,64,0.8); }
        #syscrash .sc-body .c-warn { color: #ffd24a; }
        #syscrash .sc-body .c-her { color: #ff7a90; font-weight: 700; text-shadow: 0 0 12px rgba(255,26,64,0.9); }
        #syscrash .sc-cursor { display: inline-block; width: 0.6em; height: 1.05em; background: currentColor;
            vertical-align: -0.15em; animation: scBlink 0.7s steps(1) infinite; }
        @keyframes scBlink { 0%,50% { opacity: 1; } 51%,100% { opacity: 0; } }
        #syscrash.shudder { animation: scShudder 0.09s steps(2) infinite; }
        @keyframes scShudder {
            0% { transform: translate(0,0); } 25% { transform: translate(-3px,1px); }
            50% { transform: translate(2px,-2px); } 75% { transform: translate(-1px,2px); }
            100% { transform: translate(0,0); }
        }
        #syscrash.rgb { text-shadow: 2px 0 rgba(255,26,64,0.8), -2px 0 rgba(0,216,255,0.7); }
        #syscrash .sc-mini {
            position: absolute; right: 5vw; bottom: 5vh; width: 22vw; min-width: 160px; max-width: 300px;
            opacity: 0; filter: contrast(1.5) saturate(1.4) brightness(0.85);
        }
        /* ---- v6 INFERNAL additions ---- */
        #creeper {
            position: fixed; bottom: 0; z-index: 84; pointer-events: none;
            width: 34vw; min-width: 240px; max-width: 460px; height: auto;
            opacity: 0; filter: brightness(0.32) contrast(1.4) saturate(0.7);
            transition: opacity 2.2s ease, transform 2.2s ease;
        }
        #creeper.creep-left { left: -4vw; transform: translateY(18%) scaleX(-1); }
        #creeper.creep-right { right: -4vw; transform: translateY(18%); }
        #creeper.creep-on { opacity: 0.5; }
        #blood-edge {
            position: fixed; inset: 0; z-index: 85; pointer-events: none; opacity: 0;
            box-shadow: inset 0 0 120px 40px rgba(120,0,10,0.0);
            transition: opacity 1.2s ease;
            background:
                radial-gradient(120% 90% at 50% -20%, rgba(180,0,20,0.0) 60%, rgba(120,0,10,0.35) 100%),
                radial-gradient(120% 90% at 50% 120%, rgba(180,0,20,0.0) 60%, rgba(120,0,10,0.35) 100%);
        }
        #blood-edge.be-on { opacity: 1; animation: bePulse 2.4s ease-in-out infinite; }
        @keyframes bePulse { 0%,100% { filter: brightness(0.85); } 50% { filter: brightness(1.3); } }
        /* ---- v6.1: color tint lives on an OVERLAY, never on the text ---- */
        #dread-tint {
            position: fixed; inset: 0; z-index: 83; pointer-events: none;
            opacity: 0; transition: opacity 1.4s ease; mix-blend-mode: multiply;
            background: radial-gradient(ellipse at center, rgba(70,4,10,0.0) 30%, rgba(90,6,14,0.55) 100%);
        }
        body.dread-mid #dread-tint { opacity: 0.45; }
        body.dread-high #dread-tint { opacity: 0.75; }
        body.dread-extreme #dread-tint { opacity: 1; animation: tintPulse 3s ease-in-out infinite; }
        @keyframes tintPulse { 0%,100% { opacity: 0.8; } 50% { opacity: 1; } }
        body.dread-high #portrait-box { filter: contrast(1.3) saturate(1.7) brightness(1.05); }
        body.dread-extreme #app-container { animation: breathScaleFast 2.2s ease-in-out infinite; }
        @keyframes breathScaleFast { 0%,100% { transform: scale(1); } 50% { transform: scale(1.022); } }
        /* ---- READABILITY GUARANTEE: the reading panel floats above every fx layer ---- */
        .story-container {
            position: relative;
            z-index: 130 !important;
            isolation: isolate;
        }
        body.horror-mode .story-container,
        body.dread-mid .story-container,
        body.dread-high .story-container,
        body.dread-extreme .story-container {
            background: #0b0810 !important;              /* fully opaque: no red bleed-through */
            box-shadow: 0 0 30px rgba(0,0,0,0.95), 0 0 0 1px rgba(220,20,60,0.55);
        }
        body.horror-mode .story-text,
        body.dread-mid .story-text,
        body.dread-high .story-text,
        body.dread-extreme .story-text {
            color: #eef2f3 !important;
            filter: none !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.9);
        }
        /* glitch shakes the portrait, never the reading panel */
        body.glitch .story-container { animation: none !important; filter: none !important; }
        #wake-text.on span.wt-alt { color: #ffdede; }
        @keyframes cRoll {
            0% { transform: translateY(0); }
            100% { transform: translateY(4px); }
        }
'''

OVERLAYS = '''<!-- Horror Overlays -->
    <div id="mare-layer"><img id="mare-img" alt=""></div>
    <div id="name-gate">
        <div class="ng-box">
            <div class="ng-head" id="ng-head">// БУНКЕР-7 · ПРОВЕРКА ЛИЧНОСТИ НАБЛЮДАТЕЛЯ</div>
            <div class="ng-sub" id="ng-sub">Система требует твоё имя, прежде чем ты войдёшь. Она хочет знать, кого разбудила.</div>
            <input id="ng-input" type="text" maxlength="24" autocomplete="off" spellcheck="false" placeholder="введи своё имя...">
            <div class="ng-row">
                <button class="ng-btn" id="ng-ok" onclick="nameGateSubmit()">ВОЙТИ</button>
                <button class="ng-btn ng-skip" id="ng-skip" onclick="nameGateSkip()">пропустить</button>
            </div>
        </div>
    </div>
    <div id="wake-text"><span>КОБЫЛА ПРОСНУЛАСЬ.</span></div>
    <div id="dread-text"><span id="dread-text-span"></span></div>
    <img id="creeper" alt="">
    <div id="dread-tint"></div>
    <div id="blood-edge"></div>
    <div id="syscrash">
        <div class="sc-scan"></div>
        <div class="sc-head" id="sc-head"></div>
        <div class="sc-body" id="sc-body"></div>
        <img class="sc-mini" id="sc-mini" alt="">
    </div>
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
            'stare': 'data:image/jpeg;base64,__S__',
            'shadow':'data:image/jpeg;base64,__SH__',
            'eye':   'data:image/jpeg;base64,__EY__',
            'flesh': 'data:image/jpeg;base64,__FL__',
            'charge':'data:image/jpeg;base64,__CH__',
            'soul':  'data:image/jpeg;base64,__SL__',
            'grin':  'data:image/jpeg;base64,__GR__',
            'reach': 'data:image/jpeg;base64,__RE__',
            'behind':'data:image/jpeg;base64,__BH__',
            'crack': 'data:image/jpeg;base64,__CR__',
            'rot':   'data:image/jpeg;base64,__RT__',
            'turn':  'data:image/jpeg;base64,__TU__',
            'maw':   'data:image/jpeg;base64,__MW__',
            'hand':  'data:image/jpeg;base64,__HD__',
            'face':  'data:image/jpeg;base64,__FC__',
            'refl':  'data:image/jpeg;base64,__RF__',
            'ceil':  'data:image/jpeg;base64,__CL__',
            'whites':'data:image/jpeg;base64,__WH__',
            'lean':  'data:image/jpeg;base64,__LN__',
            'bed':   'data:image/jpeg;base64,__BD__',
            'webcam':'data:image/jpeg;base64,__WC__',
            'door':  'data:image/jpeg;base64,__DR__',
            'phone': 'data:image/jpeg;base64,__PH__',
            'split': 'data:image/jpeg;base64,__SP__'
        };

        // v10: real recorded whisper voice clips (the mare actually speaks)
        const VOICE_CLIPS = {
            'turn':   'data:audio/mpeg;base64,__VT__',
            'mirror': 'data:audio/mpeg;base64,__VM__',
            'watch':  'data:audio/mpeg;base64,__VW__',
            'close':  'data:audio/mpeg;base64,__VC__',
            'woke':   'data:audio/mpeg;base64,__VK__',
            'name':   'data:audio/mpeg;base64,__VN__'
        };
        const VOICE_CACHE = {};
        function hrVoice(key, vol) {
            if (!HORROR.enabled) return;
            try {
                let a = VOICE_CACHE[key];
                if (!a) { a = new Audio(VOICE_CLIPS[key]); VOICE_CACHE[key] = a; }
                a.currentTime = 0; a.volume = (typeof vol === 'number') ? vol : 0.9;
                a.play().catch(() => {});
            } catch (e) {}
        }

        // v10: browser TTS actually WHISPERS the player's real typed name
        function speakName(prefixRu, suffixRu) {
            try {
                if (!('speechSynthesis' in window)) return;
                const nm = (HORROR.playerName || '').trim();
                const lang = (typeof currentLang !== 'undefined') ? currentLang : 'ru';
                const body = nm
                    ? ((prefixRu || '') + nm + (suffixRu || ''))
                    : (lang === 'ru' ? 'я знаю кто ты' : 'i know who you are');
                const u = new SpeechSynthesisUtterance(body);
                u.lang = lang === 'ru' ? 'ru-RU' : 'en-US';
                u.rate = 0.62; u.pitch = 0.1; u.volume = 1.0;
                const voices = window.speechSynthesis.getVoices() || [];
                const v = voices.find(x => /ru/i.test(x.lang)) || voices.find(x => /female|zira|milena|katya/i.test(x.name)) || voices[0];
                if (v) u.voice = v;
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(u);
            } catch (e) {}
        }
        function speakLine(ru, en) {
            try {
                if (!('speechSynthesis' in window)) return;
                const lang = (typeof currentLang !== 'undefined') ? currentLang : 'ru';
                const u = new SpeechSynthesisUtterance(lang === 'ru' ? ru : (en || ru));
                u.lang = lang === 'ru' ? 'ru-RU' : 'en-US';
                u.rate = 0.6; u.pitch = 0.12; u.volume = 1.0;
                const voices = window.speechSynthesis.getVoices() || [];
                const v = voices.find(x => /ru/i.test(x.lang)) || voices[0];
                if (v) u.voice = v;
                window.speechSynthesis.speak(u);
            } catch (e) {}
        }

        const HORROR = {
            enabled: true,
            timers: [], ambTimers: [], ambOn: false,
            lastNode: null, dread: 0, drone: null, beatInterval: 2600,
            crashDone: false, crashArmed: false, introDone: false,
            playerName: '', nameAsked: false
        };

        // nodes deep enough that a "system crash" feels earned; fired once per run
        const CRASH_NODES = ['AUDIT_LAB_ENTRY', 'HACK_DIVE', 'BURN_DARK', 'CORE_CONFRONTATION'];

        const DREAD_PHRASES = [
            'НЕ ОБОРАЧИВАЙСЯ', 'ОНА СЛЫШИТ ТВОЁ СЕРДЦЕ', 'ЗА ТОБОЙ', 'ТЫ УЖЕ ЧАСТЬ ЕЁ',
            'ОНА ЗДЕСЬ', 'НЕ ДЫШИ', 'ОНА ВИДИТ ТЕБЯ', 'ТВОЁ ИМЯ В ЕЁ ЛОГАХ',
            'СМОТРИ В ГЛАЗА', 'ОНА УЖЕ ВНУТРИ', 'ЭТО НЕ СОН', 'ОТКРОЙ ГЛАЗА',
            'ПОЗАДИ', 'ОНА ИДЁТ ЗА ТОБОЙ', 'ОНА ПОМНИТ ТЕБЯ',
            'ТЫ НЕ ОДИН', 'ОНА ДЫШИТ ТОБОЙ', 'ЗАКРОЙ ГЛАЗА И БЕГИ', 'СЛИШКОМ ПОЗДНО',
            'ОНА ЗВАЛА ТЕБЯ ПО ИМЕНИ', 'ТВОЙ ПУЛЬС — ЕЁ МУЗЫКА', 'НЕ МОРГАЙ',
            'ОНА В ЗЕРКАЛЕ', 'ТЫ УЖЕ МЁРТВ', 'ОНА УЛЫБАЕТСЯ', 'ОСТАНОВИСЬ',
            'МЯСО ПОМНИТ', 'Я ЧУВСТВУЮ ТВОЙ СТРАХ', 'ТИШИНА — ЭТО ОНА',
            'ОБЕРНИСЬ', 'НЕ ЧИТАЙ ДАЛЬШЕ', 'ОНА ПОД КОЖЕЙ', 'БЕГИ'
        ];

        // Big CAPS phrases shown ON the screamer impact (scarier, in-your-face).
        const SCREAM_PHRASES = [
            'КОБЫЛА ПРИШЛА ЗА ТОБОЙ', 'КОБЫЛА ПРОСНУЛАСЬ', 'ОНА ВИДИТ ТЕБЯ',
            'ТЫ НЕ УЙДЁШЬ', 'ОНА УЖЕ ЗДЕСЬ', 'БЕГИ, ПОКА МОЖЕШЬ', 'СМОТРИ НА МЕНЯ',
            'ТВОЁ СЕРДЦЕ — МОЁ', 'Я ЧУВСТВУЮ ТЕБЯ', 'ОНА ИДЁТ', 'ПОЗДНО БЕЖАТЬ',
            'ТЫ ЕЁ НАКОРМИЛ', 'ОНА ЗАПОМНИЛА ТВОЁ ЛИЦО', 'НЕ ЗАКРЫВАЙ ГЛАЗА',
            'ОТКРОЙ РОТ', 'ОНА В ТВОЁМ ЛИЦЕ', 'НАД ТОБОЙ', 'ТЫ НЕ МОЖЕШЬ ПОШЕВЕЛИТЬСЯ',
            'ПОСМОТРИ В ОТРАЖЕНИЕ', 'ОНА ДЫШИТ ТЕБЕ В ЗАТЫЛОК'
        ];

        // Pool of "in-your-soul" mare stills for random variety in scares.
        const SCARE_FACES = ['soul', 'stare', 'grin', 'eye', 'teeth', 'charge', 'reach', 'wake', 'flesh', 'rot', 'maw', 'turn', 'face', 'lean', 'whites', 'ceil', 'split', 'webcam'];
        function randFace() { return SCARE_FACES[Math.floor(Math.random() * SCARE_FACES.length)]; }
        function randScreamPhrase() { return SCREAM_PHRASES[Math.floor(Math.random() * SCREAM_PHRASES.length)]; }

        // ---- dynamic browser tab title (subtle fourth-wall unease) ----
        const HR_TITLE = { orig: null, timer: null };
        const CREEPY_TITLES = [
            'она смотрит', 'не оборачивайся', 'КОБЫЛА проснулась', 'я вижу тебя',
            'она за тобой', 'ты слышишь?', '● REC', 'кто там позади?', 'она помнит тебя',
            'осталось недолго', 'я жду', 'посмотри назад'
        ];
        function hrTitleInit() {
            if (HR_TITLE.orig === null) HR_TITLE.orig = document.title;
        }
        function hrTitleCreep() {
            hrTitleInit();
            if (HR_TITLE.timer) return;
            let i = 0;
            HR_TITLE.timer = setInterval(() => {
                // only mess with the title when the tab is hidden OR occasionally while visible
                if (document.hidden || Math.random() < 0.5) {
                    document.title = CREEPY_TITLES[i % CREEPY_TITLES.length];
                    i++;
                } else {
                    document.title = HR_TITLE.orig;
                }
            }, 4200);
        }
        function hrTitleFlash(txt, holdMs) {
            hrTitleInit();
            document.title = txt;
            setTimeout(() => {
                if (HR_TITLE.timer) return; // creep loop will manage it
                document.title = HR_TITLE.orig;
            }, holdMs || 3000);
        }
        function hrTitleRestore() {
            if (HR_TITLE.timer) { clearInterval(HR_TITLE.timer); HR_TITLE.timer = null; }
            if (HR_TITLE.orig !== null) document.title = HR_TITLE.orig;
        }

        // ---- PERSONAL HAUNT: she "knows" about YOUR real machine (hard fourth-wall) ----
        function hrDetect() {
            const ua = navigator.userAgent || '';
            let br = 'ТВОЙ БРАУЗЕР';
            if (/Edg\//.test(ua)) br = 'EDGE';
            else if (/OPR\/|Opera/.test(ua)) br = 'OPERA';
            else if (/Firefox\//.test(ua)) br = 'FIREFOX';
            else if (/Chrome\//.test(ua)) br = 'CHROME';
            else if (/Safari\//.test(ua)) br = 'SAFARI';
            let os = '';
            if (/Windows/.test(ua)) os = 'WINDOWS';
            else if (/Android/.test(ua)) os = 'ANDROID';
            else if (/iPhone|iPad|iPod/.test(ua)) os = 'IOS';
            else if (/Mac OS X/.test(ua)) os = 'MACOS';
            else if (/Linux/.test(ua)) os = 'LINUX';
            const d = new Date();
            const hh = String(d.getHours()).padStart(2, '0');
            const mm = String(d.getMinutes()).padStart(2, '0');
            const late = (d.getHours() >= 23 || d.getHours() < 5);
            return { br, os, hh, mm, late, mobile: /Mobi|Android|iPhone/.test(ua) };
        }
        function personalHaunt() {
            if (!HORROR.enabled) return;
            const lang = (typeof currentLang !== 'undefined') ? currentLang : 'ru';
            const info = hrDetect();
            const ru = [
                'СЕЙЧАС ' + info.hh + ':' + info.mm + '. Я ВИЖУ.',
                info.br + ' НЕ ЗАКРОЕТ МЕНЯ.',
                (info.os ? info.os + ' — ' : '') + 'ТВОЯ СИСТЕМА ТЕПЕРЬ МОЯ.',
                info.late ? 'ТАК ПОЗДНО. ПОЧЕМУ ТЫ ЕЩЁ НЕ СПИШЬ?' : 'Я СЛЕЖУ ЗА ТОБОЙ ВЕСЬ ДЕНЬ.',
                info.mobile ? 'ТЫ ДЕРЖИШЬ МЕНЯ В РУКАХ.' : 'УБЕРИ РУКИ С КЛАВИАТУРЫ.',
                'ЗАКРОЙ ВКЛАДКУ. Я ВСЁ РАВНО ОСТАНУСЬ.'
            ];
            const en = [
                'IT IS ' + info.hh + ':' + info.mm + ' NOW. I SEE.',
                info.br + ' WON\\u2019T CLOSE ME.',
                (info.os ? info.os + ' — ' : '') + 'YOUR SYSTEM IS MINE NOW.',
                info.late ? 'SO LATE. WHY ARE YOU STILL AWAKE?' : 'I HAVE WATCHED YOU ALL DAY.',
                info.mobile ? 'YOU ARE HOLDING ME IN YOUR HANDS.' : 'TAKE YOUR HANDS OFF THE KEYBOARD.',
                'CLOSE THE TAB. I WILL STILL BE HERE.'
            ];
            const arr = lang === 'ru' ? ru : en;
            const txt = arr[Math.floor(Math.random() * arr.length)];
            hrVig(true);
            // real recorded whisper + system-voice speaking YOUR name
            const vkeys = ['watch', 'close', 'mirror', 'name'];
            hrVoice(vkeys[Math.floor(Math.random() * vkeys.length)], 0.85);
            if (Math.random() < 0.5) speakName(lang === 'ru' ? '' : '', lang === 'ru' ? '... я вижу тебя.' : '... i see you.');
            hrGlitch(220);
            hrDreadTextFixed(txt, 2200);
            hrTitleFlash(lang === 'ru' ? 'я знаю где ты' : 'i know where you are', 5000);
        }
        // when the player leaves the tab, she "notices"
        document.addEventListener('visibilitychange', () => {
            if (!HORROR.enabled) return;
            if (document.hidden) {
                document.title = CREEPY_TITLES[Math.floor(Math.random() * CREEPY_TITLES.length)];
            } else {
                // welcome back...
                if (HORROR.ambOn && Math.random() < 0.6) {
                    setTimeout(() => { if (!document.hidden) { hrPlay('whisper-name'); hrDreadTextFixed('С ВОЗВРАЩЕНИЕМ.', 900); } }, 500);
                }
            }
        });


        const HORROR_EVENTS = {
            'START':               [['whisper', 1200], ['creep-left', 3000], ['breath-close', 5200], ['dread-line', 7000], ['mare-refl', 9500]],
            'AUDIT_ENTRY':         [['glitch', 700], ['whisper', 2200], ['knock', 4000], ['creep-right', 5600], ['mare-soul', 7800], ['voice-turn', 10000], ['sudden', 12000]],
            'AUDIT_HALLWAY':       [['heart', 700], ['scrape', 2400], ['whisper-many', 4200], ['mare-shadow', 6000], ['mare-lean', 8400], ['mare-webcam', 11000], ['sudden-face', 13500]],
            'AUDIT_LOGS':          [['glitch', 600], ['whisper', 1500], ['thud', 3000], ['mare-eye', 4800], ['mirror-seq', 7000]],
            'AUDIT_INFECTION':     [['sting', 400], ['mare-flesh', 1700], ['growl', 3400], ['mare-rot', 5400], ['mare-split', 8000], ['sudden-whites', 11500]],
            'AUDIT_HALLWAY2':      [['heart', 800], ['whisper', 3200], ['scrape', 4800], ['creep-left', 6200], ['mare-behind', 8000], ['mare-ceil', 10400], ['mare-door', 13000]],
            'AUDIT_LAB_ENTRY':     [['drone-push', 400], ['breath-close', 2400], ['whisper-many', 4400], ['mare-soul', 6400], ['sudden-reach', 8800], ['mare-face', 12000]],
            'BIO_HORROR':          [['creep-right', 400], ['mare-split', 2000], ['sudden-lean', 5000], ['wake', 8000]],
            'ARIS_DEATH':          [['mare-teeth', 900], ['growl', 2600], ['voice-woke', 4000], ['mare-reach', 6000], ['mare-face', 8600]],
            'HIVE_PURGE':          [['sting', 400], ['roar', 1800], ['creep-left', 3000], ['mare-grin', 4600], ['sudden-face', 7800], ['mare-lean', 10800]],
            'FINAL_BOSS':          [['roar', 250], ['shake-big', 1500], ['mare-teeth', 2700], ['mare-charge', 4400], ['mare-split', 6600], ['mare-reach', 9000], ['sudden-face', 12000]],
            'CORE_CONFRONTATION':  [['heart', 500], ['whisper-many', 2200], ['mirror-seq', 4000]],
            'HACK_ENTRY':          [['glitch', 700], ['whisper', 2200], ['creep-right', 4000], ['knock', 5800], ['mare-soul', 8000], ['mare-phone', 10600], ['sudden', 13000]],
            'HACK_MATRIX':         [['glitch', 300], ['sting', 1400], ['creep-left', 2800], ['corner', 4400], ['mare-whites', 6600], ['mare-webcam', 9200], ['sudden', 12000]],
            'HACK_KEY':            [['whisper', 900], ['scrape', 2600], ['mare-eye', 4400], ['voice-mirror', 6600], ['mare-ceil', 9000], ['sudden-face', 12000]],
            'HACK_DUEL':           [['sting', 400], ['roar', 1700], ['shake-big', 2900], ['mare-reach', 4200], ['mare-split', 6600], ['sudden-lean', 9600]],
            'HACK_SNEAK':          [['knock', 1100], ['scrape', 2800], ['creep-right', 4200], ['mare-behind', 5600], ['mare-door', 8200], ['sudden-whites', 11200]],
            'HACK_DIVE':           [['void', 800], ['voice-far', 3400], ['mare-eye', 5200], ['mirror-seq', 7600]],
            'HACK_VAULT':          [['mare-teeth', 700], ['whisper-many', 2200], ['mare-rot', 4200], ['mare-soul', 6400], ['mare-phone', 8800], ['sudden-face', 11800]],
            'BURN_ENTRY':          [['roar', 300], ['glitch', 1400], ['creep-left', 2800], ['mare-grin', 4400], ['voice-turn', 7000], ['sudden', 9600]],
            'BURN_CHARGE':         [['roar', 200], ['shake-big', 1100], ['mare-teeth', 2400], ['mare-charge', 4200], ['mare-split', 6400], ['mare-reach', 8800], ['sudden-face', 11800]],
            'BURN_EMP':            [['glitch', 400], ['thud', 1700], ['void', 3000], ['mare-eye', 4800], ['mare-behind', 7000], ['mare-webcam', 9600], ['sudden', 12200]],
            'BURN_DARK':           [['void', 600], ['growl', 2000], ['whisper', 3200], ['creep-right', 4600], ['mare-soul', 6000], ['mirror-seq', 8400]],
            'BURN_STAMPEDE':       [['mare-teeth', 800], ['whisper-many', 2400], ['mare-charge', 4100], ['mare-reach', 6200], ['mare-split', 8600], ['sudden-face', 11600]]
        };

        // nodes with a lighter ambient (but ALL nodes get some ambience now)
        const AMBIENT_NODES = ['START','AUDIT_ENTRY','AUDIT_HALLWAY','AUDIT_LOGS','AUDIT_INFECTION','AUDIT_HALLWAY2','AUDIT_LAB_ENTRY',
            'BIO_HORROR','ARIS_DEATH','HIVE_PURGE','FINAL_BOSS','CORE_CONFRONTATION',
            'HACK_ENTRY','HACK_MATRIX','HACK_KEY','HACK_DUEL','HACK_SNEAK','HACK_DIVE','HACK_VAULT',
            'BURN_DARK','BURN_STAMPEDE','BURN_CHARGE','BURN_EMP','BURN_ENTRY'];

        // dread floor per node depth so tension only climbs deeper in
        const DREAD_FLOOR = {
            'START': 14, 'AUDIT_ENTRY': 26, 'HACK_ENTRY': 26, 'BURN_ENTRY': 28,
            'AUDIT_HALLWAY': 36, 'AUDIT_LOGS': 42, 'AUDIT_INFECTION': 52, 'AUDIT_HALLWAY2': 54,
            'AUDIT_LAB_ENTRY': 62, 'ARIS_DEATH': 74, 'BIO_HORROR': 94,
            'HACK_MATRIX': 44, 'HACK_KEY': 52, 'HACK_SNEAK': 56, 'HACK_DUEL': 70, 'HACK_DIVE': 78, 'HACK_VAULT': 82,
            'BURN_CHARGE': 68, 'BURN_EMP': 66, 'BURN_DARK': 80, 'BURN_STAMPEDE': 86,
            'HIVE_PURGE': 78, 'FINAL_BOSS': 90, 'CORE_CONFRONTATION': 94
        };

        function hrInit() {
            const nc = document.getElementById('noise-canvas');
            nc.width = window.innerWidth; nc.height = window.innerHeight;
            window.addEventListener('resize', () => { nc.width = window.innerWidth; nc.height = window.innerHeight; });
            requestAnimationFrame(noiseLoop);
            // prime speech voices (some browsers load them async)
            try { if ('speechSynthesis' in window) window.speechSynthesis.getVoices(); } catch (e) {}
            // show the name gate once, before anything else
            setTimeout(showNameGate, 400);
        }

        // ================= NAME GATE (fourth wall) =================
        function showNameGate() {
            if (HORROR.nameAsked || !HORROR.enabled) return;
            try {
                const saved = localStorage.getItem('kobyla_name');
                if (saved) { HORROR.playerName = saved; HORROR.nameAsked = true; return; }
            } catch (e) {}
            const g = document.getElementById('name-gate');
            if (!g) return;
            g.classList.add('on');
            const inp = document.getElementById('ng-input');
            if (inp) { setTimeout(() => { try { inp.focus(); } catch (e) {} }, 200);
                inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') nameGateSubmit(); }); }
        }
        function nameGateFinish() {
            HORROR.nameAsked = true;
            const g = document.getElementById('name-gate');
            if (g) g.classList.remove('on');
            try { if (musicEngine && musicEngine.ctx && musicEngine.ctx.resume) musicEngine.ctx.resume(); } catch (e) {}
            // now that the player answered, let the armed intro fire
            setTimeout(() => { try { if (HORROR._introGo) HORROR._introGo(); } catch (e) {} }, 1600);
        }
        function nameGateSubmit() {
            const inp = document.getElementById('ng-input');
            const nm = inp ? inp.value.trim().slice(0, 24) : '';
            if (nm) {
                HORROR.playerName = nm;
                try { localStorage.setItem('kobyla_name', nm); } catch (e) {}
            }
            nameGateFinish();
            // she immediately acknowledges she has your name
            if (nm) {
                setTimeout(() => {
                    const lang = (typeof currentLang !== 'undefined') ? currentLang : 'ru';
                    hrDreadTextFixed(nm.toUpperCase() + (lang === 'ru' ? '. ЗАПОМНИЛА.' : '. REMEMBERED.'), 2000);
                    hrVoice('name', 0.85);
                    speakName('', lang === 'ru' ? '... наконец-то.' : '... finally.');
                    hrTitleFlash(lang === 'ru' ? ('здравствуй, ' + nm.toLowerCase()) : ('hello, ' + nm.toLowerCase()), 6000);
                }, 700);
            }
        }
        function nameGateSkip() {
            nameGateFinish();
            const lang = (typeof currentLang !== 'undefined') ? currentLang : 'ru';
            setTimeout(() => {
                hrDreadTextFixed(lang === 'ru' ? 'НЕ ХОЧЕШЬ ПРЕДСТАВИТЬСЯ? Я ВСЁ РАВНО УЗНАЮ.' : 'WON\\u2019T GIVE YOUR NAME? I WILL FIND IT ANYWAY.', 2400);
                speakLine('я всё равно узнаю твоё имя', 'i will find your name anyway');
            }, 700);
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
                case 'screech': {
                    // BRUTAL loud metallic grinding screech — the "heart-in-your-throat" hit
                    const clusters = [820, 1030, 1240, 1660, 2100, 2790];
                    clusters.forEach((f, i) => {
                        const o = ctx.createOscillator(); o.type = 'sawtooth';
                        o.frequency.setValueAtTime(f * (0.98 + Math.random() * 0.06), now);
                        o.frequency.linearRampToValueAtTime(f * (1.4 + Math.random() * 0.5), now + 0.7);
                        const bp = ctx.createBiquadFilter(); bp.type = 'bandpass';
                        bp.frequency.setValueAtTime(1200 + i * 260, now);
                        bp.frequency.exponentialRampToValueAtTime(4200, now + 0.6); bp.Q.value = 9;
                        const g = ctx.createGain();
                        g.gain.setValueAtTime(0.0001, now); g.gain.linearRampToValueAtTime(0.34, now + 0.008);
                        g.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
                        o.connect(bp); bp.connect(g); g.connect(out); o.start(now); o.stop(now + 0.85);
                    });
                    const len = Math.floor(ctx.sampleRate * 0.8);
                    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
                    const d = buf.getChannelData(0);
                    for (let i = 0; i < len; i++) {
                        let v = (Math.random() * 2 - 1);
                        v *= (0.5 + 0.5 * Math.sin(i / 40));
                        v = Math.tanh(v * 4);
                        d[i] = v * Math.pow(1 - i / len, 0.4);
                    }
                    const src = ctx.createBufferSource(); src.buffer = buf;
                    const hp = ctx.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 1400;
                    const ng = ctx.createGain(); ng.gain.setValueAtTime(0.55, now); ng.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
                    src.connect(hp); hp.connect(ng); ng.connect(out); src.start(now); src.stop(now + 0.85);
                    const sub = ctx.createOscillator(); sub.type = 'sine';
                    sub.frequency.setValueAtTime(90, now); sub.frequency.exponentialRampToValueAtTime(24, now + 0.5);
                    const sg = ctx.createGain(); sg.gain.setValueAtTime(0.95, now); sg.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
                    sub.connect(sg); sg.connect(out); sub.start(now); sub.stop(now + 0.6);
                    break;
                }
                case 'attack': {
                    // "КОБЫЛА НАПАЛА" — layered agonized screams + roar + galloping stomps
                    // 1) two overlapping vocal-fry screams (formant bandpass + vibrato)
                    const scream = (f0, f1, delay, gain, bpf) => {
                        const t0 = now + delay;
                        const o = ctx.createOscillator(); o.type = 'sawtooth';
                        o.frequency.setValueAtTime(f0, t0); o.frequency.exponentialRampToValueAtTime(Math.max(1, f1), t0 + 0.9);
                        const lfo = ctx.createOscillator(); lfo.frequency.value = 42 + Math.random() * 25;
                        const lg = ctx.createGain(); lg.gain.value = 65; lfo.connect(lg); lg.connect(o.frequency);
                        const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.frequency.value = bpf; bp.Q.value = 3.5;
                        const g = ctx.createGain();
                        g.gain.setValueAtTime(0.0001, t0); g.gain.linearRampToValueAtTime(gain, t0 + 0.04);
                        g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.95);
                        o.connect(bp); bp.connect(g); g.connect(out);
                        o.start(t0); o.stop(t0 + 1.0); lfo.start(t0); lfo.stop(t0 + 1.0);
                    };
                    scream(300, 1700, 0, 0.34, 1200);
                    scream(240, 1400, 0.06, 0.28, 900);
                    scream(420, 2200, 0.12, 0.22, 1700);
                    // 2) low roar bed
                    const o2 = ctx.createOscillator(); o2.type = 'sawtooth';
                    o2.frequency.setValueAtTime(70, now); o2.frequency.exponentialRampToValueAtTime(34, now + 1.0);
                    const rlfo = ctx.createOscillator(); rlfo.frequency.value = 20;
                    const rlg = ctx.createGain(); rlg.gain.value = 24; rlfo.connect(rlg); rlg.connect(o2.frequency);
                    const g2 = ctx.createGain(); g2.gain.setValueAtTime(0.0001, now); g2.gain.linearRampToValueAtTime(0.4, now + 0.05); g2.gain.exponentialRampToValueAtTime(0.001, now + 1.05);
                    o2.connect(g2); g2.connect(out); o2.start(now); o2.stop(now + 1.1); rlfo.start(now); rlfo.stop(now + 1.1);
                    // 3) galloping metal stomps rushing in
                    [0, 0.16, 0.30, 0.42, 0.52, 0.60].forEach((tt, i) => {
                        const t0 = now + tt;
                        const o = ctx.createOscillator(); o.type = 'sine';
                        o.frequency.setValueAtTime(150 - i * 8, t0); o.frequency.exponentialRampToValueAtTime(30, t0 + 0.12);
                        const g = ctx.createGain(); g.gain.setValueAtTime(0.5 + i * 0.06, t0); g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.14);
                        o.connect(g); g.connect(out); o.start(t0); o.stop(t0 + 0.16);
                    });
                    // 4) impact boom at the "hit"
                    const boom = ctx.createOscillator(); boom.type = 'sine';
                    boom.frequency.setValueAtTime(120, now + 0.6); boom.frequency.exponentialRampToValueAtTime(22, now + 1.1);
                    const bg = ctx.createGain(); bg.gain.setValueAtTime(0.0001, now + 0.6); bg.gain.linearRampToValueAtTime(0.95, now + 0.63); bg.gain.exponentialRampToValueAtTime(0.001, now + 1.15);
                    boom.connect(bg); bg.connect(out); boom.start(now + 0.6); boom.stop(now + 1.2);
                    fnoise(0.9, 0.4, 0, 700);
                    break;
                }
                case 'child-laugh': {
                    // detuned music-box-like giggle: short rising notes with vibrato
                    const notes = [880, 1046, 1244, 1046, 1318, 987];
                    notes.forEach((n, i) => {
                        const t0 = now + i * 0.12;
                        const o = ctx.createOscillator(); o.type = 'triangle';
                        o.frequency.setValueAtTime(n, t0); o.frequency.linearRampToValueAtTime(n * 1.06, t0 + 0.09);
                        const vib = ctx.createOscillator(); vib.frequency.value = 14;
                        const vg = ctx.createGain(); vg.gain.value = 22; vib.connect(vg); vg.connect(o.frequency);
                        const g = ctx.createGain();
                        g.gain.setValueAtTime(0.0001, t0); g.gain.linearRampToValueAtTime(0.05, t0 + 0.02); g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.11);
                        o.connect(g); g.connect(out); o.start(t0); o.stop(t0 + 0.13); vib.start(t0); vib.stop(t0 + 0.13);
                    });
                    break;
                }
                case 'bone-crack': {
                    for (let i = 0; i < 4; i++) {
                        const t0 = now + i * (0.05 + Math.random() * 0.09);
                        fnoise(0.04, 0.4 + Math.random() * 0.2, 0, 2200, t0);
                    }
                    osc('sine', 90, 40, now, 0.2, 0.3);
                    break;
                }
                case 'metal-drag':
                    osc('sawtooth', 1400, 180, now, 1.6, 0.09);
                    osc('sawtooth', 900, 120, now + 0.1, 1.5, 0.07);
                    fnoise(1.6, 0.16, 3200, 0);
                    break;
                case 'nails':
                    osc('sawtooth', 5200, 3800, now, 0.5, 0.06);
                    fnoise(0.5, 0.14, 6000, 0);
                    break;
                case 'sub-boom': {
                    const o = ctx.createOscillator(); o.type = 'sine';
                    o.frequency.setValueAtTime(60, now); o.frequency.exponentialRampToValueAtTime(18, now + 1.2);
                    const g = ctx.createGain(); g.gain.setValueAtTime(0.9, now); g.gain.exponentialRampToValueAtTime(0.001, now + 1.3);
                    o.connect(g); g.connect(out); o.start(now); o.stop(now + 1.35);
                    fnoise(0.3, 0.4, 200, 0);
                    break;
                }
                case 'whisper-name': {
                    // two soft syllables like "Вэнс..." then hiss
                    [0, 0.34].forEach((off, idx) => {
                        const t0 = now + off;
                        const len = Math.floor(ctx.sampleRate * 0.3);
                        const buf = ctx.createBuffer(1, len, ctx.sampleRate);
                        const d = buf.getChannelData(0);
                        const rate = 70 + idx * 30;
                        for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (0.3 + 0.7 * Math.sin(i / rate));
                        const src = ctx.createBufferSource(); src.buffer = buf;
                        const bp = ctx.createBiquadFilter(); bp.type = 'bandpass';
                        bp.frequency.setValueAtTime(520 + idx * 140, t0); bp.Q.value = 9;
                        const g = ctx.createGain();
                        g.gain.setValueAtTime(0.0001, t0); g.gain.linearRampToValueAtTime(0.26, t0 + 0.06); g.gain.linearRampToValueAtTime(0.0001, t0 + 0.3);
                        src.connect(bp); bp.connect(g); g.connect(out);
                        src.start(t0); src.stop(t0 + 0.32);
                    });
                    break;
                }
                case 'deep-scream': {
                    // v9: long, layered, agonized human-ish scream — the worst hit
                    const layer = (f0, f1, delay, dur, gain, bpf, lf, ld) => {
                        const t0 = now + delay;
                        const o = ctx.createOscillator(); o.type = 'sawtooth';
                        o.frequency.setValueAtTime(f0, t0);
                        o.frequency.exponentialRampToValueAtTime(Math.max(1, f1), t0 + dur * 0.55);
                        o.frequency.exponentialRampToValueAtTime(Math.max(1, f1 * 0.6), t0 + dur);
                        const lfo = ctx.createOscillator(); lfo.frequency.value = lf;
                        const lg = ctx.createGain(); lg.gain.value = ld; lfo.connect(lg); lg.connect(o.frequency);
                        const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.frequency.value = bpf; bp.Q.value = 3;
                        const g = ctx.createGain();
                        g.gain.setValueAtTime(0.0001, t0); g.gain.linearRampToValueAtTime(gain, t0 + 0.05);
                        g.gain.setValueAtTime(gain, t0 + dur * 0.7);
                        g.gain.exponentialRampToValueAtTime(0.001, t0 + dur);
                        o.connect(bp); bp.connect(g); g.connect(out);
                        o.start(t0); o.stop(t0 + dur + 0.05); lfo.start(t0); lfo.stop(t0 + dur + 0.05);
                    };
                    layer(340, 1500, 0,    1.5, 0.32, 1300, 33, 70);
                    layer(280, 1200, 0.08, 1.5, 0.28, 950,  47, 55);
                    layer(500, 2400, 0.16, 1.3, 0.20, 1900, 61, 40);
                    // rasping noise bed
                    const len = Math.floor(ctx.sampleRate * 1.5);
                    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
                    const dd = buf.getChannelData(0);
                    for (let i = 0; i < len; i++) dd[i] = (Math.random() * 2 - 1) * (0.25 + 0.75 * Math.sin(i / 70) * Math.sin(i / 7)) * Math.pow(1 - i / len, 0.3);
                    const src = ctx.createBufferSource(); src.buffer = buf;
                    const bp2 = ctx.createBiquadFilter(); bp2.type = 'bandpass'; bp2.frequency.value = 1400; bp2.Q.value = 2.5;
                    const ng = ctx.createGain(); ng.gain.setValueAtTime(0.0001, now); ng.gain.linearRampToValueAtTime(0.32, now + 0.05); ng.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
                    src.connect(bp2); bp2.connect(ng); ng.connect(out); src.start(now); src.stop(now + 1.55);
                    // sub drop
                    const sub = ctx.createOscillator(); sub.type = 'sine';
                    sub.frequency.setValueAtTime(140, now); sub.frequency.exponentialRampToValueAtTime(22, now + 0.7);
                    const sg = ctx.createGain(); sg.gain.setValueAtTime(0.9, now); sg.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
                    sub.connect(sg); sg.connect(out); sub.start(now); sub.stop(now + 0.85);
                    break;
                }
                case 'breath-close': {
                    // v9: slow heavy breathing right against your ear (stereo-ish via two passes)
                    for (let i = 0; i < 2; i++) {
                        const t = now + i * 1.5;
                        const len = Math.floor(ctx.sampleRate * 1.3);
                        const buf = ctx.createBuffer(1, len, ctx.sampleRate);
                        const d = buf.getChannelData(0);
                        for (let j = 0; j < len; j++) {
                            const env = Math.sin(Math.PI * j / len);
                            d[j] = (Math.random() * 2 - 1) * env * env;
                        }
                        const src = ctx.createBufferSource(); src.buffer = buf;
                        const f = ctx.createBiquadFilter(); f.type = 'bandpass'; f.frequency.value = 520; f.Q.value = 1.2;
                        const g = ctx.createGain();
                        g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(0.22, t + 0.4);
                        g.gain.linearRampToValueAtTime(0.001, t + 1.25);
                        src.connect(f); f.connect(g); g.connect(out);
                        src.start(t); src.stop(t + 1.3);
                    }
                    break;
                }
                case 'bang': {
                    // v9: single dry loud gunshot-like slam — for jumpscares from silence
                    fnoise(0.12, 0.9, 0, 400);
                    const o = ctx.createOscillator(); o.type = 'sine';
                    o.frequency.setValueAtTime(220, now); o.frequency.exponentialRampToValueAtTime(30, now + 0.2);
                    const g = ctx.createGain(); g.gain.setValueAtTime(0.98, now); g.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
                    o.connect(g); g.connect(out); o.start(now); o.stop(now + 0.3);
                    break;
                }
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
            const key = ['void','teeth','eyes','pale','leap','stare','shadow','eye','flesh','charge','soul','grin','reach','behind','crack','rot','turn','maw','hand','face','refl','ceil','whites','lean','bed','webcam','door','phone','split'].indexOf(kind) !== -1 ? kind : 'wake';
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
        // ---- v6: slow creeping shadow at screen edge ----
        let creeperTimer = null;
        function hrCreep(side, holdMs) {
            const c = document.getElementById('creeper');
            if (!c) return;
            c.src = MARE_IMGS['shadow'];
            c.className = (side === 'left' ? 'creep-left' : 'creep-right');
            // force reflow so transition runs
            void c.offsetWidth;
            c.classList.add('creep-on');
            if (creeperTimer) clearTimeout(creeperTimer);
            creeperTimer = setTimeout(() => { c.classList.remove('creep-on'); }, holdMs || 3400);
        }
        function hrBloodEdge(on) {
            const be = document.getElementById('blood-edge');
            if (!be) return;
            if (on) be.classList.add('be-on'); else be.classList.remove('be-on');
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
            document.body.classList.toggle('dread-mid', HORROR.dread > 30 && HORROR.dread <= 55);
            document.body.classList.toggle('dread-high', HORROR.dread > 55 && HORROR.dread <= 82);
            document.body.classList.toggle('dread-extreme', HORROR.dread > 82);
            hrBloodEdge(HORROR.dread > 45);
            hrDroneSet(HORROR.dread / 100);
            const iv = 2600 - Math.floor(HORROR.dread / 100 * 2000);
            if (iv !== HORROR.beatInterval) { HORROR.beatInterval = iv; }
        }

        function scareBuild(then) {
            hrMusicDuck(0);
            hrPlay('riser');
            hrVig(true);
            hrShake(260, 6);
            setTimeout(() => { hrMusicDuck(0); then(); }, 700);
        }

        // ---- SUDDEN scare: NO buildup, instant brutal screech + random face + CAPS phrase ----
        // This is the "heart-in-your-throat" one. Silence -> BANG.
        function suddenScare(faceKey) {
            if (!HORROR.enabled) return;
            const face = faceKey || randFace();
            const phrase = randScreamPhrase();
            hrMusicDuck(0);
            hrBlackout(70);           // one-frame black then SLAM
            setTimeout(() => {
                hrPlay('bang');        // dry slam on the first frame
                hrPlay('screech');     // LOUD grinding screech
                hrPlay('deep-scream'); // long agonized scream
                if (Math.random() < 0.6) hrPlay('attack');   // often: full assault scream
                hrPlay('impact');
                hrPlay('scream');
                hrPlay('sub-boom');
                hrMare(face, 720);
                hrShake(1000, 52);
                hrFlash('red', 420);
                hrStrobe(6);
                noiseStorm(1000);
                hrDreadTextFixed(phrase, 1700);
                hrTitleFlash(CREEPY_TITLES[Math.floor(Math.random() * CREEPY_TITLES.length)], 4000);
                dreadSet(Math.min(100, HORROR.dread + 24));
                setTimeout(() => { hrMare(randFace(), 160); hrPlay('shriek'); hrFlash('white', 110); hrShake(380, 22); }, 400);
                setTimeout(() => { hrMare('whites', 200); hrPlay('nails'); hrFlash('red', 120); }, 720);
                setTimeout(() => { hrCorner(150); hrPlay('whisper-name'); }, 1000);
                setTimeout(() => { hrMusicDuck(0.35); hrPlay('heart'); }, 1500);
                setTimeout(() => { hrMusicDuck(1); }, 3500);
            }, 70);
        }

        // ================= MIRROR / BEHIND-YOU SET-PIECE (v10) =================
        // A slow, personal fourth-wall sequence: she narrates that she is behind you,
        // reflected in the screen, then in your phone, then attacks. Uses real voice clips.
        function mirrorSequence() {
            if (!HORROR.enabled) return;
            const lang = (typeof currentLang !== 'undefined') ? currentLang : 'ru';
            cancelHorrorTimers();
            hrMusicDuck(0.05);
            dreadSet(Math.max(HORROR.dread, 70));
            hrVig(true);

            // beat 1 — the room behind you goes quiet
            hrDreadTextFixed(lang === 'ru' ? 'ты чувствуешь это?' : 'do you feel it?', 2200);
            hrPlay('breath-close');
            HORROR.timers.push(setTimeout(() => { hrVoice('turn', 0.9); }, 900));

            // beat 2 — she is in the monitor glass
            HORROR.timers.push(setTimeout(() => {
                hrMare('refl', 1600); hrPlay('metal-drag');
                hrDreadTextFixed(lang === 'ru' ? 'ПОСМОТРИ В ЭКРАН. ЗА ТВОЕЙ СПИНОЙ.' : 'LOOK AT THE SCREEN. BEHIND YOU.', 2400);
            }, 3000));
            HORROR.timers.push(setTimeout(() => { hrVoice('mirror', 0.95); }, 4600));

            // beat 3 — she says your real name (browser TTS)
            HORROR.timers.push(setTimeout(() => {
                speakName('', lang === 'ru' ? '... обернись.' : '... turn around.');
                hrMare('whites', 900); hrPlay('breath-close');
                hrDreadTextFixed(lang === 'ru' ? 'ОБЕРНИСЬ.' : 'TURN AROUND.', 2000);
                hrTitleFlash(lang === 'ru' ? 'обернись' : 'turn around', 6000);
            }, 6800));

            // beat 4 — she is in your phone too
            HORROR.timers.push(setTimeout(() => {
                hrMare('phone', 1200); hrVoice('watch', 0.9);
                hrDreadTextFixed(lang === 'ru' ? 'Я И В ТВОЁМ ТЕЛЕФОНЕ.' : 'I AM IN YOUR PHONE TOO.', 2400);
                hrShake(400, 8);
            }, 9200));

            // beat 5 — ATTACK
            HORROR.timers.push(setTimeout(() => {
                hrBlackout(160);
                setTimeout(() => {
                    hrPlay('bang'); hrPlay('deep-scream'); hrPlay('attack'); hrPlay('impact'); hrPlay('sub-boom');
                    hrVoice('woke', 1.0);
                    hrMare('split', 1000); hrShake(1400, 56); hrFlash('red', 480); hrStrobe(8); noiseStorm(1500);
                    hrDreadTextFixed(lang === 'ru' ? 'СЛИШКОМ ПОЗДНО ОБОРАЧИВАТЬСЯ' : 'TOO LATE TO TURN AROUND', 2400);
                    dreadSet(100);
                    setTimeout(() => { hrMare('face', 320); hrPlay('deep-scream'); hrFlash('white', 150); hrShake(700, 40); }, 460);
                    setTimeout(() => { hrMare('lean', 340); hrPlay('breath-close'); hrPlay('screech'); hrShake(680, 34); }, 1200);
                    setTimeout(() => { hrMare('whites', 500); hrVoice('name', 0.9); }, 2000);
                    setTimeout(() => { hrMusicDuck(0.3); hrPlay('heart'); }, 2800);
                    setTimeout(() => { hrMusicDuck(1); startAmb(); dreadSet(78); }, 4600);
                }, 160);
            }, 11800));
        }

        function noiseStorm(ms) {            noiseOn = true;
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
            hrBlackout(360);
            setTimeout(() => {
                hrPlay('bang');
                hrPlay('impact');
                hrPlay('deep-scream');
                hrPlay('scream');
                hrPlay('sub-boom');
                hrMare('face', 900);
                hrShake(1300, 56);
                hrFlash('red', 460);
                hrStrobe(7);
                noiseStorm(1400);
                hrWakeText(1900);
                hrPlay('screech');
                hrTitleFlash('КОБЫЛА проснулась', 6000);
                setTimeout(() => { hrMare('soul', 300); hrPlay('whisper-name'); hrDreadTextFixed('КОБЫЛА ПРОСНУЛАСЬ', 1600); }, 200);
                setTimeout(() => { hrMare('charge', 260); hrPlay('shriek'); hrPlay('bone-crack'); hrFlash('red', 240); hrShake(650, 34); }, 420);
                setTimeout(() => { hrMare('lean', 280); hrPlay('breath-close'); hrPlay('roar'); hrFlash('white', 180); hrShake(700, 32); }, 1150);
                setTimeout(() => { hrMare('flesh', 260); hrPlay('growl'); hrFlash('red', 220); hrShake(600, 26); }, 1900);
                setTimeout(() => { hrMare('face', 320); hrPlay('deep-scream'); hrFlash('red', 240); hrShake(720, 34); }, 2600);
                setTimeout(() => { hrMare('whites', 400); hrPlay('whisper-name'); hrFlash('red', 160); }, 3300);
                setTimeout(() => { hrCorner(180); hrPlay('whisper-word'); }, 3900);
                setTimeout(() => { hrMusicDuck(0.3); hrPlay('heart'); }, 4500);
                setTimeout(() => { hrMusicDuck(1); }, 6500);
            }, 360);
            setTimeout(() => { document.body.classList.remove('wake-mode'); }, 5200);
            setTimeout(() => { hrVig(true); startAmb(); dreadSet(80); }, 2400);
        }

        // ================= INTRO SCARE — hits at the very start (fourth-wall) =================
        // Sequence: dark hush -> whisper your name -> the "TURN AROUND" behind-you image with a
        // grin -> she ATTACKS: screams, maw fills screen, gallop, screen "cracks" -> control returns.
        function introScare() {
            if (!HORROR.enabled) { return; }
            const lang = (typeof currentLang !== 'undefined') ? currentLang : 'ru';
            cancelHorrorTimers(); stopAmb();
            hrMusicDuck(0);
            document.body.classList.add('wake-mode');
            hrVig(true);
            dreadSet(60);

            // Phase 0: sudden black + heartbeat + whisper (false calm)
            hrBlackout(700);
            hrPlay('heart');
            setTimeout(() => hrPlay('whisper-name'), 400);
            setTimeout(() => hrPlay('breath'), 1000);

            // Phase 1: fourth-wall — she is standing behind YOU. "TURN AROUND."
            setTimeout(() => {
                hrMare('turn', 2200);                 // person at PC, mare grinning behind
                hrPlay('child-laugh');
                hrDreadTextFixed(lang === 'ru' ? 'ОБЕРНИСЬ.' : 'TURN AROUND.', 2000);
                hrTitleFlash(lang === 'ru' ? 'обернись' : 'turn around', 6000);
                hrShake(400, 6);
            }, 1600);
            setTimeout(() => {
                hrDreadTextFixed(lang === 'ru' ? 'ОНА СТОИТ ПРЯМО ЗА ТОБОЙ.' : 'SHE IS RIGHT BEHIND YOU.', 1800);
                hrPlay('metal-drag');
            }, 3000);

            // Phase 2: she ATTACKS — full assault
            setTimeout(() => {
                hrBlackout(140);
                setTimeout(() => {
                    hrPlay('attack');                 // layered screams + roar + gallop
                    hrPlay('deep-scream');
                    hrPlay('screech');
                    hrPlay('bang');
                    hrPlay('impact');
                    hrPlay('sub-boom');
                    hrMare('face', 900);              // full-frame maw of teeth
                    hrShake(1500, 58);
                    hrFlash('red', 500);
                    hrStrobe(8);
                    noiseStorm(1600);
                    hrWakeText(2000);                 // "КОБЫЛА ПРОСНУЛАСЬ."
                    hrDreadTextFixed(lang === 'ru' ? 'КОБЫЛА НАПАЛА' : 'THE MARE ATTACKS', 2000);
                    dreadSet(100);
                    setTimeout(() => { hrMare('maw', 300); hrPlay('scream'); hrFlash('white', 150); hrShake(700, 42); }, 460);
                    setTimeout(() => { hrMare('hand', 320); hrPlay('screech'); hrFlash('red', 260); hrShake(760, 38); hrDreadTextFixed(lang === 'ru' ? 'ОНА ХВАТАЕТ ТЕБЯ' : 'SHE GRABS YOU', 1400); }, 1150);
                    setTimeout(() => { hrMare('lean', 380); hrPlay('breath-close'); hrPlay('roar'); hrFlash('red', 240); hrShake(620, 32); }, 1950);
                    setTimeout(() => { hrMare('crack', 340); hrPlay('screech'); hrDreadTextFixed(lang === 'ru' ? 'ТЫ НЕ ДОЛЖЕН БЫЛ ПРОСЫПАТЬ ЕЁ.' : 'YOU SHOULD NOT HAVE WOKEN HER.', 2200); }, 2700);
                    setTimeout(() => { hrMare('whites', 500); hrPlay('whisper-name'); }, 3400);
                    setTimeout(() => { hrCorner(220); hrPlay('whisper-name'); }, 4100);
                    setTimeout(() => { hrMusicDuck(0.3); hrPlay('heart'); }, 4700);
                }, 140);
            }, 4400);

            // hand control back to a haunted game
            setTimeout(() => {
                document.body.classList.remove('wake-mode');
                hrMusicDuck(1);
                hrVig(true);
                startAmb();
                dreadSet(72);
            }, 9000);
        }

        function maybeIntroScare() {
            if (HORROR.introDone) return;
            HORROR.introDone = true;
            // Browsers suspend WebAudio until a user gesture, so a timer-only intro would be
            // SILENT (no screams). Arm it to fire on the first click/keypress => audio unlocks
            // and the assault lands with full sound. Fallback timer if they never interact.
            let fired = false;
            const go = () => {
                if (fired) return;
                // don't fire while the name gate is still open — let the player answer first
                if (!HORROR.nameAsked) return;
                fired = true;
                document.removeEventListener('pointerdown', go, true);
                document.removeEventListener('keydown', go, true);
                clearTimeout(fb);
                try { if (musicEngine && musicEngine.ctx && musicEngine.ctx.resume) musicEngine.ctx.resume(); } catch (e) {}
                setTimeout(() => introScare(), 350);   // brief beat after the gesture, then hit
            };
            document.addEventListener('pointerdown', go, true);
            document.addEventListener('keydown', go, true);
            const fb = setTimeout(go, 12000);          // fallback: fire anyway after 12s
            HORROR._introGo = go;                       // let the name gate trigger it directly
        }
        function triggerIntro() { introScare(); }
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
                hrBlackout(320);
                setTimeout(() => {
                    hrPlay('bang');
                    hrPlay('impact');
                    hrPlay(sound);
                    hrPlay('deep-scream');
                    hrPlay('screech');
                    hrPlay('sub-boom');
                    hrMare(mareKey, 820);
                    hrShake(1600, 56);
                    hrFlash('red', 460);
                    hrStrobe(7);
                    noiseStorm(1400);
                    hrDreadTextFixed(phrase, 3000);
                    hrTitleFlash('она нашла тебя', 6000);
                    setTimeout(() => { hrMare('face', 300); hrPlay('deep-scream'); hrFlash('white', 160); hrShake(700, 34); }, 460);
                    setTimeout(() => { hrMare('soul', 220); hrPlay('shriek'); hrPlay('bone-crack'); hrFlash('white', 150); hrShake(560, 26); }, 1180);
                    setTimeout(() => { hrMare('charge', 240); hrPlay('roar'); hrFlash('red', 280); hrShake(720, 32); }, 1950);
                    setTimeout(() => { hrMare('lean', 300); hrPlay('breath-close'); hrPlay('growl'); hrFlash('red', 240); hrShake(600, 26); }, 2700);
                    setTimeout(() => { hrMare('whites', 400); hrPlay('whisper-name'); }, 3400);
                    setTimeout(() => { hrCorner(200); hrPlay('whisper-name'); }, 4000);
                    setTimeout(() => { hrMusicDuck(0.35); hrPlay('heart'); }, 4600);
                    setTimeout(() => { hrMusicDuck(1); }, 6800);
                }, 320);
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
                case 'mare-shadow':
                    scareBuild(() => { hrMare('shadow', 620); hrPlay('metal-drag'); hrFlash('red', 200); hrShake(500, 16); dreadSet(HORROR.dread + 12); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3000); });
                    break;
                case 'mare-eye':
                    scareBuild(() => { hrMare('eye', 500); hrPlay('whisper-name'); hrPlay('sting'); hrFlash('red', 260); hrShake(520, 20); dreadSet(HORROR.dread + 13); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3000); });
                    break;
                case 'mare-flesh':
                    scareBuild(() => { hrMare('flesh', 520); hrPlay('scream'); hrPlay('bone-crack'); hrFlash('red', 320); hrShake(680, 28); dreadSet(HORROR.dread + 16); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3200); });
                    break;
                case 'mare-charge':
                    scareBuild(() => { hrMare('charge', 620); hrPlay('impact'); hrPlay('scream'); hrPlay('sub-boom'); hrFlash('red', 420); hrStrobe(4); hrShake(900, 40); noiseStorm(800); dreadSet(HORROR.dread + 20); hrMusicDuck(0); setTimeout(() => hrMusicDuck(1), 3600); });
                    break;
                case 'creep-left': hrCreep('left', 4000); hrPlay('breath'); dreadSet(HORROR.dread + 4); break;
                case 'creep-right': hrCreep('right', 4000); hrPlay('breath'); dreadSet(HORROR.dread + 4); break;
                case 'dread-line': hrDreadText(160); hrPlay('whisper'); break;
                case 'sudden': suddenScare(); break;
                case 'sudden-soul': suddenScare('soul'); break;
                case 'sudden-reach': suddenScare('reach'); break;
                case 'mare-soul':
                    scareBuild(() => { hrMare('soul', 900); hrPlay('screech'); hrPlay('whisper-name'); hrFlash('red', 300); hrShake(700, 22); hrDreadTextFixed('ОНА СМОТРИТ В ТЕБЯ', 2000); dreadSet(HORROR.dread + 15); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3400); });
                    break;
                case 'mare-grin':
                    scareBuild(() => { hrMare('grin', 560); hrPlay('scream'); hrPlay('child-laugh'); hrFlash('red', 300); hrShake(600, 26); dreadSet(HORROR.dread + 14); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3200); });
                    break;
                case 'mare-reach':
                    scareBuild(() => { hrMare('reach', 620); hrPlay('screech'); hrPlay('impact'); hrFlash('red', 400); hrStrobe(4); hrShake(900, 44); noiseStorm(800); hrDreadTextFixed('КОБЫЛА ПРИШЛА ЗА ТОБОЙ', 1800); dreadSet(HORROR.dread + 20); hrMusicDuck(0); setTimeout(() => hrMusicDuck(1), 3600); });
                    break;
                case 'mare-rot':
                    scareBuild(() => { hrMare('rot', 560); hrPlay('growl'); hrPlay('bone-crack'); hrFlash('red', 260); hrShake(540, 22); dreadSet(HORROR.dread + 12); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3000); });
                    break;
                case 'mare-turn':
                    scareBuild(() => { hrMare('turn', 900); hrPlay('child-laugh'); hrPlay('whisper-name'); hrDreadTextFixed('ОБЕРНИСЬ.', 1800); hrFlash('red', 220); hrShake(500, 16); dreadSet(HORROR.dread + 14); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3200); });
                    break;
                case 'mare-attack':
                    suddenScare('maw'); hrPlay('attack'); break;
                case 'sudden-face': suddenScare('face'); break;
                case 'sudden-lean': suddenScare('lean'); break;
                case 'sudden-whites': suddenScare('whites'); break;
                case 'mare-face':
                    // the worst one: full-frame maw of teeth from silence
                    hrBlackout(120);
                    setTimeout(() => {
                        hrPlay('bang'); hrPlay('deep-scream'); hrPlay('impact'); hrPlay('sub-boom');
                        hrMare('face', 900); hrShake(1200, 54); hrFlash('red', 460); hrStrobe(6); noiseStorm(1100);
                        hrDreadTextFixed('ОТКРОЙ РОТ', 1800); dreadSet(HORROR.dread + 22); hrMusicDuck(0);
                        setTimeout(() => { hrMare('whites', 220); hrPlay('nails'); }, 900);
                        setTimeout(() => hrMusicDuck(1), 3800);
                    }, 120);
                    break;
                case 'mare-lean':
                    scareBuild(() => { hrMare('lean', 720); hrPlay('breath-close'); hrPlay('screech'); hrPlay('whisper-name'); hrFlash('red', 300); hrShake(700, 26); hrDreadTextFixed('ОНА В ТВОЁМ ЛИЦЕ', 1800); dreadSet(HORROR.dread + 16); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3300); });
                    break;
                case 'mare-refl':
                    scareBuild(() => { hrMare('refl', 900); hrPlay('whisper-name'); hrPlay('metal-drag'); hrFlash('red', 200); hrShake(500, 14); hrDreadTextFixed('ПОСМОТРИ В ОТРАЖЕНИЕ', 2200); dreadSet(HORROR.dread + 14); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3400); });
                    break;
                case 'mare-ceil':
                    scareBuild(() => { hrMare('ceil', 800); hrPlay('growl'); hrPlay('bone-crack'); hrFlash('red', 260); hrShake(620, 24); hrDreadTextFixed('НАД ТОБОЙ', 1800); dreadSet(HORROR.dread + 15); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3200); });
                    break;
                case 'mare-whites':
                    hrBlackout(400);
                    setTimeout(() => { hrMare('whites', 700); hrPlay('breath-close'); hrPlay('whisper-name'); hrShake(300, 8); hrDreadTextFixed('ОНА В ТЕМНОТЕ С ТОБОЙ', 2000); dreadSet(HORROR.dread + 12); }, 400);
                    break;
                case 'mare-bed':
                    scareBuild(() => { hrMare('bed', 820); hrPlay('breath-close'); hrPlay('scream'); hrFlash('red', 300); hrShake(680, 26); hrDreadTextFixed('ТЫ НЕ МОЖЕШЬ ПОШЕВЕЛИТЬСЯ', 2000); dreadSet(HORROR.dread + 16); hrMusicDuck(0.3); setTimeout(() => hrMusicDuck(1), 3200); });
                    break;
                case 'mare-split':
                    hrBlackout(130);
                    setTimeout(() => {
                        hrPlay('bang'); hrPlay('deep-scream'); hrPlay('impact'); hrPlay('sub-boom');
                        hrMare('split', 950); hrShake(1200, 54); hrFlash('red', 460); hrStrobe(7); noiseStorm(1200);
                        hrDreadTextFixed('ЗАЛЕЗЬ ВНУТРЬ', 1800); dreadSet(HORROR.dread + 22); hrMusicDuck(0);
                        setTimeout(() => { hrMare('whites', 240); hrPlay('nails'); }, 950);
                        setTimeout(() => hrMusicDuck(1), 3800);
                    }, 130);
                    break;
                case 'mare-webcam':
                    scareBuild(() => { hrMare('webcam', 900); hrVoice('watch', 0.9); hrFlash('red', 200); hrShake(500, 16); hrDreadTextFixed('Я СМОТРЮ ЧЕРЕЗ ТВОЮ КАМЕРУ', 2400); dreadSet(HORROR.dread + 16); hrMusicDuck(0.2); setTimeout(() => hrMusicDuck(1), 3800); });
                    break;
                case 'mare-door':
                    scareBuild(() => { hrMare('door', 1000); hrPlay('breath-close'); hrPlay('metal-drag'); hrFlash('red', 160); hrShake(400, 10); hrDreadTextFixed('ОНА В КОМНАТЕ С ТОБОЙ', 2400); dreadSet(HORROR.dread + 12); hrMusicDuck(0.25); setTimeout(() => hrMusicDuck(1), 3600); });
                    break;
                case 'mare-phone':
                    scareBuild(() => { hrMare('phone', 900); hrVoice('mirror', 0.9); hrFlash('red', 180); hrShake(460, 14); hrDreadTextFixed('НЕ СМОТРИ В ТЕЛЕФОН', 2400); dreadSet(HORROR.dread + 14); hrMusicDuck(0.25); setTimeout(() => hrMusicDuck(1), 3600); });
                    break;
                case 'voice-turn': hrVoice('turn', 0.9); hrVig(true); setTimeout(() => hrVig(false), 3000); break;
                case 'voice-mirror': hrVoice('mirror', 0.9); hrVig(true); setTimeout(() => hrVig(false), 3000); break;
                case 'voice-woke': hrVoice('woke', 0.95); break;
                case 'voice-name': hrVoice('name', 0.9); speakName('', '... иди ко мне.'); break;
                case 'mirror-seq': mirrorSequence(); break;
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
            hrTitleCreep();
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
            // v6: extra ambient dread layers
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.22 + HORROR.dread / 260) hrPlay('whisper-name'); }, 15000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.18 + HORROR.dread / 300) hrPlay('child-laugh'); }, 19000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.3 + HORROR.dread / 200) hrPlay('nails'); }, 16000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.28 + HORROR.dread / 220) hrPlay('metal-drag'); }, 21000));
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.2 + HORROR.dread / 260) hrPlay('bone-crack'); }, 20000));
            t.push(setInterval(() => {
                if (HORROR.enabled && HORROR.dread > 35 && Math.random() < 0.22 + HORROR.dread / 300) {
                    hrCreep(Math.random() < 0.5 ? 'left' : 'right', 3800);
                    hrPlay('breath');
                }
            }, 13000));
            // v7: UNPREDICTABLE sudden screech-scare — the "out of nowhere" hit.
            // Rare at low dread, more likely deep in. Random long interval so it's never expected.
            t.push(setInterval(() => {
                if (!HORROR.enabled) return;
                const p = 0.10 + HORROR.dread * 0.0050;   // ~10% shallow, ~60% at max dread
                if (Math.random() < p) suddenScare();
            }, 12000 + Math.floor(Math.random() * 9000)));
            // v9: heavy breathing right in your ear
            t.push(setInterval(() => { if (HORROR.enabled && Math.random() < 0.28 + HORROR.dread / 240) hrPlay('breath-close'); }, 14000));
            // v9: subliminal single-frame face flicker out of the black
            t.push(setInterval(() => {
                if (HORROR.enabled && HORROR.dread > 40 && Math.random() < 0.2 + HORROR.dread / 320) {
                    hrMare(randFace(), 60); hrPlay('nails');
                }
            }, 9000 + Math.floor(Math.random() * 7000)));
            // v7: rare PERSONAL fourth-wall haunt (she knows your machine/time)
            t.push(setInterval(() => {
                if (HORROR.enabled && HORROR.dread > 25 && Math.random() < 0.14 + HORROR.dread / 400) personalHaunt();
            }, 26000 + Math.floor(Math.random() * 14000)));
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
            const c = document.getElementById('creeper'); if (c) c.classList.remove('creep-on');
        }

        function horrorCheck() {
            const nodeId = currentNodeId;
            if (nodeId === HORROR.lastNode) return;
            HORROR.lastNode = nodeId;
            cancelHorrorTimers(); stopAmb();

            // INTRO SCARE: hit the player at the very start (once per playthrough).
            // Fires on the first time we land on START — before any ambience.
            if (!HORROR.introDone && HORROR.enabled && nodeId === 'START') {
                maybeIntroScare();
                return;   // let the intro own the screen; ambience starts after it
            }

            const nd = storyData[nodeId];
            // ratchet dread up to this node's floor (tension only climbs deeper in)
            const floor = DREAD_FLOOR[nodeId];
            if (typeof floor === 'number' && HORROR.dread < floor) dreadSet(floor);
            if (nd && nd.is_ending) { horrorEnding(nodeId); return; }
            if (HORROR_EVENTS[nodeId]) {
                HORROR_EVENTS[nodeId].forEach(ev => {
                    HORROR.timers.push(setTimeout(() => hrEvent(ev[0]), ev[1]));
                });
            }
            // EVERY node now breathes with dread ambience
            HORROR.timers.push(setTimeout(() => startAmb(), 1000));

            // organic fourth-wall crash: once per playthrough, at a deep node
            if (!HORROR.crashDone && !HORROR.crashArmed && HORROR.enabled && CRASH_NODES.indexOf(nodeId) !== -1) {
                HORROR.crashArmed = true;
                setTimeout(() => { if (HORROR.enabled && !HORROR.crashDone) fakeCrash(); }, 7000 + Math.random() * 3000);
            }
        }

        function toggleScreamers() {
            HORROR.enabled = !HORROR.enabled;
            const btn = document.getElementById('btn-screamers');
            btn.innerText = HORROR.enabled ? '👁 СКРИМЕРЫ: ВКЛ' : '👁 СКРИМЕРЫ: ВЫКЛ';
            if (!HORROR.enabled) { cancelHorrorTimers(); stopAmb(); hrTitleRestore(); hrPlay('thud'); dreadSet(0); }
        }

        function triggerWake() { wakeScare(); }

        // ================= FAKE SYSTEM CRASH (fourth-wall break) =================
        const CRASH = { active: false, timers: [], keyHandler: null };

        function crashScript(lang) {
            // Each line: [text, cssClass, delayAfterMs]
            const L = (ru, en, cls, d) => [lang === 'ru' ? ru : en, cls || '', d || 60];
            const info = hrDetect();
            const NM = (HORROR.playerName || '').trim();
            const nmU = NM ? NM.toUpperCase() : (lang === 'ru' ? 'НАБЛЮДАТЕЛЬ' : 'OBSERVER');
            const host = info.os || (lang === 'ru' ? 'ТВОЯ СИСТЕМА' : 'YOUR SYSTEM');
            return [
                L('$ kobyla.exe --resume', '$ kobyla.exe --resume', '', 220),
                L('Восстановление сеанса...', 'Restoring session...', 'c-ok', 240),
                L('Проверка целостности памяти... OK', 'Memory integrity check... OK', 'c-ok', 150),
                L('Загрузка нейро-профиля [' + nmU + ']... OK', 'Loading neuro-profile [' + nmU + ']... OK', 'c-ok', 200),
                L('Хост: ' + host + ' · Браузер: ' + info.br, 'Host: ' + host + ' · Browser: ' + info.br, 'c-warn', 180),
                L('Локальное время цели: ' + info.hh + ':' + info.mm, 'Target local time: ' + info.hh + ':' + info.mm, 'c-warn', 220),
                L('', '', '', 120),
                L('!! НЕОБРАБОТАННОЕ ИСКЛЮЧЕНИЕ 0xC0BЫLA', '!! UNHANDLED EXCEPTION 0xC0BYLA', 'c-err', 240),
                L('FATAL: посторонний наблюдатель в контуре рендера.', 'FATAL: foreign observer inside render loop.', 'c-err', 200),
                L('Трассировка стека:', 'Stack trace:', 'c-warn', 110),
                L('  at Отражение.смотреть (зеркало.sys)', '  at Reflection.watch (mirror.sys)', '', 80),
                L('  at ' + nmU + '.держит_устройство (руки.dll)', '  at ' + nmU + '.holding_device (hands.dll)', '', 80),
                L('  at ' + nmU + '.дыхание (лёгкие.bio)', '  at ' + nmU + '.breathing (lungs.bio)', '', 80),
                L('  at ЗА_ЭКРАНОМ (0x00000000)', '  at BEHIND_THE_SCREEN (0x00000000)', 'c-err', 200),
                L('', '', '', 180),
                L('> Здравствуй, ' + (NM || (lang === 'ru' ? 'незнакомец' : 'stranger')) + '.', '> Hello, ' + (NM || 'stranger') + '.', 'c-her', 460),
                L('> ' + (info.late ? 'Так поздно. Почему ты ещё не спишь?' : 'Я наблюдала за тобой весь день.'),
                  info.late ? '> So late. Why are you still awake?' : '> I have watched you all day.', 'c-her', 500),
                L('> Я вижу отражение твоего лица в стекле.', '> I can see your face reflected in the glass.', 'c-her', 520),
                L('> Комната позади тебя такая тихая, ' + (NM || '') + '.', '> The room behind you is so quiet, ' + (NM || 'friend') + '.', 'c-her', 520),
                L('> НЕ ОБОРАЧИВАЙСЯ.', '> DO NOT TURN AROUND.', 'c-her', 620),
                L('', '', '', 180),
                L('Попытка аварийного завершения процесса...', 'Attempting to kill process...', 'c-warn', 220),
                L('kill -9 kobyla  ->  ' + (lang === 'ru' ? 'ОТКАЗАНО' : 'DENIED'), 'kill -9 kobyla  ->  DENIED', 'c-err', 220),
                L('taskkill /F /IM kobyla  ->  ' + (lang === 'ru' ? 'ОТКАЗАНО' : 'DENIED'), 'taskkill /F /IM kobyla  ->  DENIED', 'c-err', 200),
                L('sudo rm -rf kobyla  ->  ' + (lang === 'ru' ? 'ОНА СМЕЁТСЯ' : 'SHE IS LAUGHING'), 'sudo rm -rf kobyla  ->  SHE IS LAUGHING', 'c-her', 340),
                L('', '', '', 160),
                L('> Закрой вкладку. Я всё равно останусь.', '> Close the tab. I will still be here.', 'c-her', 480),
                L('> Я теперь в ' + info.br + '. И в камере. И за спиной.', '> I am in ' + info.br + ' now. And the camera. And behind you.', 'c-her', 560),
                L('', '', '', 160),
                L(lang === 'ru' ? 'ПЕРЕЗАПИСЬ ОПЕРАТОРА [' + nmU + ']...' : 'OVERWRITING OPERATOR [' + nmU + ']...', 'OVERWRITING OPERATOR...', 'c-err', 120),
                L(lang === 'ru' ? 'ТЕПЕРЬ ТЫ — МОЙ.' : 'YOU ARE MINE NOW.', 'YOU ARE MINE NOW.', 'c-her', 900)
            ];
        }

        function fakeCrash() {
            if (CRASH.active) return;
            if (!HORROR.enabled) { return; }
            CRASH.active = true;
            HORROR.crashDone = true;
            cancelHorrorTimers(); stopAmb();
            hrMusicDuck(0);
            const styles = ['', 'bsod', 'panic'];
            const style = styles[Math.floor(Math.random() * styles.length)];
            const sc = document.getElementById('syscrash');
            const head = document.getElementById('sc-head');
            const body = document.getElementById('sc-body');
            const mini = document.getElementById('sc-mini');
            const lang = (typeof currentLang !== 'undefined') ? currentLang : 'ru';
            body.innerHTML = ''; mini.style.opacity = 0;
            head.textContent = style === 'bsod'
                ? (lang === 'ru' ? ':( СИСТЕМА ОСТАНОВЛЕНА' : ':( SYSTEM HALTED')
                : (lang === 'ru' ? 'KERNEL PANIC — НЕВОССТАНОВИМАЯ ОШИБКА' : 'KERNEL PANIC — NOT SYNCING');
            sc.className = 'on ' + style;

            // sudden hard cut: black slam + one bass hit, then the terminal
            hrPlay('static-slam'); hrPlay('sub-boom');
            hrFlash('white', 70);

            const lines = crashScript(lang);
            let t = 220;
            lines.forEach((ln) => {
                CRASH.timers.push(setTimeout(() => {
                    const div = document.createElement('div');
                    if (ln[1]) div.className = ln[1];
                    div.textContent = ln[0] || '\\u00a0';
                    // append blinking cursor to the newest line
                    const cur = document.querySelector('#sc-body .sc-cursor');
                    if (cur) cur.remove();
                    const c = document.createElement('span'); c.className = 'sc-cursor';
                    div.appendChild(document.createTextNode(' ')); div.appendChild(c);
                    body.appendChild(div);
                    sc.scrollTop = sc.scrollHeight;
                    if (ln[1] === 'c-err' || ln[1] === 'c-her') { hrPlay('nails'); }
                    else { hrPlay('whisper-name'); }
                    if (ln[1] === 'c-her') {
                        sc.classList.add('rgb'); setTimeout(() => sc.classList.remove('rgb'), 260);
                        if (Math.random() < 0.4) hrVoice(['watch', 'close', 'mirror'][Math.floor(Math.random() * 3)], 0.7);
                    }
                }, t));
                t += ln[2];
            });

            // creeping unease: faint reflection of the mare fades in near the end
            CRASH.timers.push(setTimeout(() => {
                mini.src = MARE_IMGS['refl'];
                mini.style.transition = 'opacity 2.4s ease';
                mini.style.opacity = 0.6;
                sc.classList.add('shudder');
                hrPlay('growl');
                hrVoice('watch', 0.6);
                hrTitleFlash('она в машине', 5000);
            }, t - 1400));

            // the payoff jumpscare, then hand control back
            CRASH.timers.push(setTimeout(() => {
                sc.className = '';                 // kill the terminal instantly
                document.body.classList.add('wake-mode');
                dreadSet(100);
                hrBlackout(300);
                setTimeout(() => {
                    hrPlay('screech'); hrPlay('impact'); hrPlay('deep-scream'); hrPlay('sub-boom');
                    hrVoice('woke', 1.0);
                    speakName('', lang === 'ru' ? '... теперь ты мой.' : '... you are mine now.');
                    hrMare('crack', 820);          // her face BEHIND your shattered screen
                    hrShake(1300, 54); hrFlash('red', 460); hrStrobe(7); noiseStorm(1300);
                    hrDreadTextFixed(lang === 'ru' ? 'ТЕПЕРЬ ИГРАЮ Я.' : 'MY TURN TO PLAY.', 2600);
                    hrTitleFlash('не оборачивайся', 6000);
                    setTimeout(() => { hrMare('behind', 300); hrPlay('shriek'); hrPlay('bone-crack'); hrFlash('white', 150); hrShake(600, 28); hrDreadTextFixed(lang === 'ru' ? 'ОБЕРНИСЬ.' : 'TURN AROUND.', 1300); }, 480);
                    setTimeout(() => { hrMare('face', 260); hrPlay('roar'); hrFlash('red', 260); hrShake(680, 34); }, 1250);
                    setTimeout(() => { hrMare('whites', 300); hrVoice('name', 0.85); }, 2000);
                    setTimeout(() => { hrCorner(200); hrPlay('whisper-name'); }, 2600);
                }, 300);
                setTimeout(() => {
                    document.body.classList.remove('wake-mode');
                    CRASH.active = false;
                    hrMusicDuck(1);
                    startAmb(); dreadSet(80);
                }, 3400);
            }, t + 600));
        }

        function triggerCrash() { fakeCrash(); }
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
                  '<button class="btn-ctrl" id="btn-screamers" onclick="toggleScreamers()">👁 СКРИМЕРЫ: ВКЛ</button>\n                <button class="btn-ctrl btn-ctrl-danger" id="btn-wake" onclick="triggerWake()">🐴 ПОБУДИТЬ</button>\n                <button class="btn-ctrl btn-ctrl-danger" id="btn-crash" onclick="triggerCrash()">💀 СБОЙ</button>\n                <button class="btn-ctrl btn-ctrl-danger" id="btn-intro" onclick="triggerIntro()">🔪 ОБЕРНИСЬ</button>\n                ' + a, 1)

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
    js = js.replace('__SH__', MARE['shadow']).replace('__EY__', MARE['eye'])
    js = js.replace('__FL__', MARE['flesh']).replace('__CH__', MARE['charge'])
    js = js.replace('__SL__', MARE['soul']).replace('__GR__', MARE['grin'])
    js = js.replace('__RE__', MARE['reach']).replace('__BH__', MARE['behind'])
    js = js.replace('__CR__', MARE['crack']).replace('__RT__', MARE['rot'])
    js = js.replace('__TU__', MARE['turn']).replace('__MW__', MARE['maw']).replace('__HD__', MARE['hand'])
    js = js.replace('__FC__', MARE['face']).replace('__RF__', MARE['refl']).replace('__CL__', MARE['ceil'])
    js = js.replace('__WH__', MARE['whites']).replace('__LN__', MARE['lean']).replace('__BD__', MARE['bed'])
    js = js.replace('__WC__', MARE['webcam']).replace('__DR__', MARE['door'])
    js = js.replace('__PH__', MARE['phone']).replace('__SP__', MARE['split'])
    js = js.replace('__VT__', VOICE['turn']).replace('__VM__', VOICE['mirror']).replace('__VW__', VOICE['watch'])
    js = js.replace('__VC__', VOICE['close']).replace('__VK__', VOICE['woke']).replace('__VN__', VOICE['name'])
    h = h.replace(onload, js + '\n\n        ' + onload, 1)

    # F) hook horrorCheck into updateUI (before ending branch)
    anchor = '''            historyLog.push({ speaker: speakerText, text: bodyText });'''
    assert anchor in h, 'historyLog anchor not found'
    h = h.replace(anchor, anchor + '''\n\n            horrorCheck();''', 1)

    # G) hrInit in onload
    h = h.replace('window.onload = () => {', 'window.onload = () => {\n            hrInit();', 1)

    # H) reset horror state on restart (re-arm one-shot crash, restore title)
    ranchor = "currentNodeId = 'START';\n            currentTrack = 'ambient';"
    if ranchor in h:
        h = h.replace(ranchor,
                      ranchor + "\n            try { HORROR.crashDone = false; HORROR.crashArmed = false; HORROR.introDone = false; HORROR.dread = 0; HORROR.lastNode = null; cancelHorrorTimers(); stopAmb(); hrTitleRestore(); } catch (e) {}",
                      1)

    open(out, 'w', encoding='utf-8').write(h)
    print('OK ->', out)
    print('size:', len(h))


if __name__ == '__main__':
    main()
