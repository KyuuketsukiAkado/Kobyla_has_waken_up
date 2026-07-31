import json, base64

image_path = "/home/user/uploads/111.png"
with open(image_path, "rb") as img_file:
    img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
img_data_url = f"data:image/png;base64,{img_b64}"

from generate_book_vn import book_story_nodes

html_book_cyberpunk_template = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOBYLA HAS WAKEN UP 2099 / КОБЫЛА ПРОСНУЛАСЬ 2099 - Book Edition</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@500;700;900&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');

        :root {{
            --bg-dark: #030205;
            --panel-bg: rgba(10, 4, 12, 0.94);
            --border-neon: #ff0033;
            --glow-red: #ff1a40;
            --neon-cyan: #00f0ff;
            --text-light: #e6f0ff;
            --text-gold: #ffcc00;
            --font-main: 'Share Tech Mono', monospace;
            --font-title: 'Orbitron', sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }}

        body {{
            background-color: var(--bg-dark);
            color: var(--text-light);
            font-family: var(--font-main);
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            background-image: 
                radial-gradient(circle at 50% 20%, rgba(255, 0, 51, 0.22) 0%, rgba(3, 2, 5, 0.98) 75%),
                linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
            background-size: 100% 100%, 30px 30px, 30px 30px;
        }}

        /* Scanlines */
        body::after {{
            content: " ";
            display: block;
            position: absolute;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
            background-size: 100% 4px;
            z-index: 99;
            pointer-events: none;
            opacity: 0.8;
        }}

        #fx-canvas {{
            position: absolute;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            pointer-events: none;
            z-index: 1;
        }}

        .screen-flash {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: 100;
            opacity: 0;
            transition: opacity 0.25s ease;
        }}
        .screen-flash.flash-red {{
            background-color: rgba(255, 0, 51, 0.5);
            opacity: 1;
        }}
        .screen-flash.flash-white {{
            background-color: rgba(0, 240, 255, 0.7);
            opacity: 1;
        }}

        /* Container */
        #app-container {{
            position: relative;
            z-index: 2;
            width: 100%;
            max-width: 1250px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 12px;
        }}

        /* Header */
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 18px;
            background: rgba(12, 5, 15, 0.92);
            border: 1px solid var(--border-neon);
            border-radius: 2px;
            box-shadow: 0 0 15px rgba(255, 0, 51, 0.3), inset 0 0 8px rgba(0, 240, 255, 0.1);
            margin-bottom: 8px;
        }}

        .game-title {{
            font-family: var(--font-title);
            font-size: 1.1rem;
            font-weight: 900;
            letter-spacing: 2px;
            color: var(--border-neon);
            text-shadow: 0 0 8px var(--border-neon), 0 0 20px var(--neon-cyan);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .track-indicator {{
            font-size: 0.75rem;
            color: var(--neon-cyan);
            background: rgba(0, 240, 255, 0.1);
            padding: 3px 8px;
            border: 1px solid var(--neon-cyan);
            border-radius: 2px;
        }}

        .controls {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}

        button.btn-ctrl {{
            background: #0d0208;
            color: var(--neon-cyan);
            border: 1px solid var(--neon-cyan);
            padding: 5px 12px;
            font-family: var(--font-title);
            font-size: 0.75rem;
            cursor: pointer;
            border-radius: 2px;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 0 5px rgba(0, 240, 255, 0.2);
        }}

        button.btn-ctrl:hover {{
            background: var(--border-neon);
            color: #fff;
            border-color: var(--border-neon);
            box-shadow: 0 0 12px var(--border-neon);
        }}

        button.btn-music-active {{
            background: var(--border-neon) !important;
            color: #fff !important;
            box-shadow: 0 0 10px var(--glow-red) !important;
        }}

        /* Stats Bar */
        .stats-bar {{
            display: flex;
            gap: 20px;
            padding: 6px 15px;
            background: rgba(8, 3, 10, 0.88);
            border: 1px solid rgba(255, 0, 51, 0.4);
            border-radius: 2px;
            margin-bottom: 8px;
            font-size: 0.85rem;
            font-family: var(--font-main);
        }}

        .stat-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .stat-val {{
            font-weight: bold;
            color: var(--text-gold);
            text-shadow: 0 0 5px var(--text-gold);
        }}

        /* Stage */
        #game-stage {{
            flex: 1;
            display: flex;
            gap: 15px;
            overflow: hidden;
            margin-bottom: 8px;
        }}

        /* Portrait */
        .portrait-frame {{
            flex: 0 0 380px;
            position: relative;
            background: #000;
            border: 2px solid var(--border-neon);
            border-radius: 2px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(255, 0, 51, 0.3), inset 0 0 15px rgba(0,240,255,0.2);
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .portrait-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease, filter 0.3s ease;
            filter: contrast(1.2) saturate(1.2);
        }}

        .portrait-frame.pulse-red .portrait-img {{
            animation: pulseCyber 1.5s infinite alternate;
        }}

        .portrait-frame.shake-heavy {{
            animation: glitchShake 0.25s infinite;
        }}

        @keyframes pulseCyber {{
            0% {{ filter: drop-shadow(0 0 8px var(--border-neon)) contrast(1.2); transform: scale(1); }}
            100% {{ filter: drop-shadow(0 0 25px var(--neon-cyan)) contrast(1.4) brightness(1.15); transform: scale(1.02); }}
        }}

        @keyframes glitchShake {{
            0% {{ transform: translate(2px, 1px) skewX(0deg); }}
            25% {{ transform: translate(-3px, -2px) skewX(2deg); }}
            50% {{ transform: translate(2px, 3px) skewX(-2deg); }}
            75% {{ transform: translate(-2px, 1px) skewX(1deg); }}
            100% {{ transform: translate(1px, -2px) skewX(0deg); }}
        }}

        .eye-glow-overlay {{
            position: absolute;
            top: 44%;
            left: 42%;
            width: 18%;
            height: 8%;
            background: radial-gradient(ellipse at center, rgba(0,240,255,0.95) 0%, rgba(255,0,51,0) 75%);
            mix-blend-mode: screen;
            opacity: 0.9;
            pointer-events: none;
            animation: eyeGlitch 1s infinite alternate;
        }}

        @keyframes eyeGlitch {{
            0% {{ opacity: 0.6; transform: scale(0.9); }}
            100% {{ opacity: 1; transform: scale(1.1); filter: drop-shadow(0 0 10px #00f0ff); }}
        }}

        /* Narrative Window */
        .story-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--panel-bg);
            border: 1px solid var(--border-neon);
            border-radius: 2px;
            padding: 20px;
            box-shadow: 0 0 25px rgba(0, 0, 0, 0.9);
            overflow-y: auto;
        }}

        .speaker-box {{
            font-family: var(--font-title);
            font-size: 1rem;
            font-weight: bold;
            color: var(--border-neon);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 1px solid rgba(255, 0, 51, 0.4);
            padding-bottom: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .chapter-title {{
            font-size: 0.8rem;
            color: var(--neon-cyan);
            font-family: var(--font-main);
        }}

        .story-text {{
            font-size: 1.05rem;
            line-height: 1.6;
            color: var(--text-light);
            margin-bottom: 18px;
            white-space: pre-wrap;
            flex: 1;
            text-shadow: 0 0 2px rgba(230, 240, 255, 0.3);
        }}

        /* Choices */
        .choices-container {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 5px;
        }}

        button.btn-choice {{
            background: linear-gradient(90deg, rgba(20, 4, 10, 0.95) 0%, rgba(40, 6, 18, 0.95) 100%);
            color: var(--text-light);
            border: 1px solid var(--border-neon);
            padding: 12px 16px;
            text-align: left;
            font-family: var(--font-main);
            font-size: 0.95rem;
            cursor: pointer;
            border-radius: 2px;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            box-shadow: 0 0 5px rgba(255,0,51,0.15);
        }}

        button.btn-choice::before {{
            content: "⚡ ";
            color: var(--neon-cyan);
            margin-right: 8px;
            font-size: 0.85rem;
        }}

        button.btn-choice:hover {{
            background: linear-gradient(90deg, rgba(255, 0, 51, 0.8) 0%, rgba(0, 240, 255, 0.8) 100%);
            color: #000;
            font-weight: bold;
            box-shadow: 0 0 15px var(--neon-cyan);
            transform: translateX(4px);
        }}

        /* Modal */
        .modal-overlay {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(2, 1, 4, 0.92);
            backdrop-filter: blur(6px);
            z-index: 500;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }}

        .modal-overlay.active {{
            opacity: 1;
            pointer-events: auto;
        }}

        .modal-card {{
            background: #08030a;
            border: 2px solid var(--neon-cyan);
            padding: 25px;
            max-width: 650px;
            width: 90%;
            border-radius: 2px;
            box-shadow: 0 0 30px var(--neon-cyan);
            max-height: 85vh;
            overflow-y: auto;
        }}

        .modal-title {{
            font-family: var(--font-title);
            font-size: 1.3rem;
            color: var(--neon-cyan);
            margin-bottom: 12px;
            text-align: center;
            border-bottom: 1px solid var(--border-neon);
            padding-bottom: 8px;
        }}

        .modal-body {{
            font-size: 0.95rem;
            line-height: 1.5;
            margin-bottom: 15px;
            color: var(--text-light);
        }}
    </style>
</head>
<body>

    <canvas id="fx-canvas"></canvas>
    <div id="screen-flash" class="screen-flash"></div>

    <div id="app-container">
        <header>
            <div class="game-title" id="ui-title">KOBYLA HAS WAKEN UP 2099</div>
            <div class="track-indicator" id="track-name">TRACK: THE NEON RUINS (90 BPM)</div>
            <div class="controls">
                <button class="btn-ctrl" id="btn-music" onclick="toggleMusic()">🎵 MUSIC: OFF</button>
                <button class="btn-ctrl" id="btn-lang" onclick="toggleLanguage()">RU / EN</button>
                <button class="btn-ctrl" id="btn-history" onclick="openHistory()">📜 LOG</button>
                <button class="btn-ctrl" id="btn-restart" onclick="restartGame()">🔄 RESTART</button>
            </div>
        </header>

        <div class="stats-bar">
            <div class="stat-item">
                <span id="lbl-sanity">Cyber-Sanity (Нейро-Рассудок):</span>
                <span class="stat-val" id="val-sanity">100%</span>
            </div>
            <div class="stat-item">
                <span id="lbl-willpower">Willpower (Воля):</span>
                <span class="stat-val" id="val-willpower">50</span>
            </div>
            <div class="stat-item">
                <span id="lbl-blood">Bio-Corrupt (Заражение):</span>
                <span class="stat-val" id="val-blood">0</span>
            </div>
        </div>

        <div id="game-stage">
            <div class="portrait-frame pulse-red" id="portrait-box">
                <img src="{img_data_url}" alt="Kobyla-99" class="portrait-img" id="portrait-img">
                <div class="eye-glow-overlay"></div>
            </div>

            <div class="story-container">
                <div class="speaker-box">
                    <span id="speaker-name">SPEAKER</span>
                    <span class="chapter-title" id="chapter-title">SECTOR</span>
                </div>
                <div class="story-text" id="story-text">INITIALIZING SYSTEM...</div>
                <div class="choices-container" id="choices-box"></div>
            </div>
        </div>
    </div>

    <!-- Modal -->
    <div class="modal-overlay" id="modal-box">
        <div class="modal-card">
            <div class="modal-title" id="modal-title">TERMINAL LOG</div>
            <div class="modal-body" id="modal-body"></div>
            <div style="text-align: center;">
                <button class="btn-ctrl" onclick="closeModal()">CLOSE</button>
            </div>
        </div>
    </div>

    <script>
        const storyData = {json.dumps(book_story_nodes, ensure_ascii=False, indent=2)};

        let currentLang = 'ru';
        let currentNodeId = 'START';
        let currentTrack = 'ambient';
        let stats = {{ sanity: 100, willpower: 50, blood: 0 }};
        let historyLog = [];

        // Multi-Track Web Audio Synthesizer Engine
        class MultiTrackCyberpunkMusic {{
            constructor() {{
                this.ctx = null;
                this.isPlaying = false;
                this.timer = null;
                this.step = 0;
                this.activeTrack = 'ambient';

                // Track Definitions
                this.tracks = {{
                    ambient: {{
                        name_ru: 'ТРЕК 1: НЕОНОВЫЕ РУИНЫ (90 BPM)',
                        name_en: 'TRACK 1: THE NEON RUINS (90 BPM)',
                        tempo: 90,
                        bass: [55, 55, 65.4, 55, 73.4, 55, 43.65, 55],
                        arp: [220, 261.63, 329.63, 392.00],
                        waveform: 'sawtooth',
                        kickInterval: 4
                    }},
                    confrontation: {{
                        name_ru: 'ТРЕК 2: КИБЕР-ДЕМОН БУНКЕРА (110 BPM)',
                        name_en: 'TRACK 2: CYBER-DEMON ENCOUNTER (110 BPM)',
                        tempo: 110,
                        bass: [65.4, 65.4, 73.4, 87.3, 65.4, 55, 65.4, 98],
                        arp: [261.63, 329.63, 392.00, 440, 523.25, 440],
                        waveform: 'sawtooth',
                        kickInterval: 2
                    }},
                    intense: {{
                        name_ru: 'ТРЕК 3: НЕЙРО-ПЕРЕГРУЗКА МАТРИЦЫ (135 BPM)',
                        name_en: 'TRACK 3: NEURAL OVERLOAD MATRIX (135 BPM)',
                        tempo: 135,
                        bass: [73.4, 87.3, 73.4, 110, 73.4, 98, 87.3, 130.8],
                        arp: [329.63, 392.00, 440, 523.25, 659.25, 523.25],
                        waveform: 'square',
                        kickInterval: 2
                    }},
                    resolution: {{
                        name_ru: 'ТРЕК 4: ЭХО ПОСТАПОКАЛИПСИСА (70 BPM)',
                        name_en: 'TRACK 4: AFTERMATH OF THE RED ECLIPSE (70 BPM)',
                        tempo: 70,
                        bass: [43.65, 43.65, 55, 43.65],
                        arp: [174.61, 220, 261.63, 329.63],
                        waveform: 'sine',
                        kickInterval: 8
                    }}
                }};
            }}

            init() {{
                if (!this.ctx) {{
                    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
                }}
            }}

            switchTrack(trackKey) {{
                if (this.tracks[trackKey]) {{
                    this.activeTrack = trackKey;
                    if (this.isPlaying) {{
                        this.restartTimer();
                    }}
                }}
            }}

            start() {{
                this.init();
                if (this.ctx.state === 'suspended') {{
                    this.ctx.resume();
                }}
                if (this.isPlaying) return;
                this.isPlaying = true;
                this.restartTimer();
            }}

            restartTimer() {{
                if (this.timer) clearInterval(this.timer);
                const tConfig = this.tracks[this.activeTrack];
                const stepTime = (60 / tConfig.tempo) / 4 * 1000;
                this.timer = setInterval(() => this.tick(), stepTime);
            }}

            stop() {{
                this.isPlaying = false;
                if (this.timer) {{
                    clearInterval(this.timer);
                    this.timer = null;
                }}
            }}

            tick() {{
                if (!this.isPlaying || !this.ctx) return;
                const now = this.ctx.currentTime;
                const config = this.tracks[this.activeTrack];
                const step = this.step;

                // 1. Synth Bass
                if (step % 2 === 0) {{
                    const bassFreq = config.bass[(step / 2) % config.bass.length];
                    const osc = this.ctx.createOscillator();
                    const filter = this.ctx.createBiquadFilter();
                    const gain = this.ctx.createGain();

                    osc.type = config.waveform;
                    osc.frequency.setValueAtTime(bassFreq, now);

                    filter.type = 'lowpass';
                    filter.frequency.setValueAtTime(800, now);
                    filter.frequency.exponentialRampToValueAtTime(110, now + 0.16);

                    gain.gain.setValueAtTime(0.3, now);
                    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.18);

                    osc.connect(filter);
                    filter.connect(gain);
                    gain.connect(this.ctx.destination);

                    osc.start(now);
                    osc.stop(now + 0.2);
                }}

                // 2. Kick Drum
                if (step % config.kickInterval === 0) {{
                    const kickOsc = this.ctx.createOscillator();
                    const kickGain = this.ctx.createGain();

                    kickOsc.type = 'sine';
                    kickOsc.frequency.setValueAtTime(150, now);
                    kickOsc.frequency.exponentialRampToValueAtTime(30, now + 0.1);

                    kickGain.gain.setValueAtTime(0.55, now);
                    kickGain.gain.exponentialRampToValueAtTime(0.01, now + 0.11);

                    kickOsc.connect(kickGain);
                    kickGain.connect(this.ctx.destination);

                    kickOsc.start(now);
                    kickOsc.stop(now + 0.12);
                }}

                // 3. High Arp
                const arpFreq = config.arp[step % config.arp.length];
                const arpOsc = this.ctx.createOscillator();
                const arpGain = this.ctx.createGain();

                arpOsc.type = 'triangle';
                arpOsc.frequency.setValueAtTime(arpFreq, now);

                arpGain.gain.setValueAtTime(0.06, now);
                arpGain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

                arpOsc.connect(arpGain);
                arpGain.connect(this.ctx.destination);

                arpOsc.start(now);
                arpOsc.stop(now + 0.09);

                this.step = (this.step + 1) % 32;
            }}
        }}

        const musicEngine = new MultiTrackCyberpunkMusic();

        function toggleMusic() {{
            const btn = document.getElementById('btn-music');
            if (musicEngine.isPlaying) {{
                musicEngine.stop();
                btn.innerText = '🎵 MUSIC: OFF';
                btn.classList.remove('btn-music-active');
            }} else {{
                musicEngine.start();
                btn.innerText = '🎵 MUSIC: ON';
                btn.classList.add('btn-music-active');
            }}
        }}

        // SFX Trigger
        function playSound(type) {{
            musicEngine.init();
            if (!musicEngine.ctx) return;
            const ctx = musicEngine.ctx;
            const now = ctx.currentTime;

            if (type === 'jack_in' || type === 'code') {{
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(800, now);
                osc.frequency.linearRampToValueAtTime(1800, now + 0.15);
                gain.gain.setValueAtTime(0.2, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.18);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.2);
            }} 
            else if (type === 'blade') {{
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(2200, now);
                osc.frequency.exponentialRampToValueAtTime(400, now + 0.25);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.28);
            }} 
            else if (type === 'screech' || type === 'roar') {{
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(200, now);
                osc.frequency.linearRampToValueAtTime(1200, now + 0.2);
                gain.gain.setValueAtTime(0.35, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.42);
            }}
        }}

        function triggerFx(fxType) {{
            const portraitBox = document.getElementById('portrait-box');
            const flash = document.getElementById('screen-flash');
            portraitBox.className = 'portrait-frame ' + (fxType || 'pulse-red');

            if (fxType === 'blood-flash') {{
                flash.className = 'screen-flash flash-red';
                setTimeout(() => flash.className = 'screen-flash', 300);
            }} else if (fxType === 'flash-white') {{
                flash.className = 'screen-flash flash-white';
                setTimeout(() => flash.className = 'screen-flash', 350);
            }}
        }}

        function updateUI() {{
            const node = storyData[currentNodeId];
            if (!node) return;

            // Handle Dynamic Music Track Switching!
            if (node.music_track && node.music_track !== currentTrack) {{
                currentTrack = node.music_track;
                musicEngine.switchTrack(currentTrack);
            }}

            const trackInfo = musicEngine.tracks[currentTrack];
            document.getElementById('track-name').innerText = currentLang === 'ru' ? trackInfo.name_ru : trackInfo.name_en;

            document.getElementById('lbl-sanity').innerText = currentLang === 'ru' ? 'Нейро-Рассудок:' : 'Cyber-Sanity:';
            document.getElementById('lbl-willpower').innerText = currentLang === 'ru' ? 'Воля:' : 'Willpower:';
            document.getElementById('lbl-blood').innerText = currentLang === 'ru' ? 'Заражение:' : 'Bio-Corrupt:';

            document.getElementById('val-sanity').innerText = stats.sanity + '%';
            document.getElementById('val-willpower').innerText = stats.willpower;
            document.getElementById('val-blood').innerText = stats.blood;

            document.getElementById('ui-title').innerText = currentLang === 'ru' ? 'КОБЫЛА ПРОСНУЛАСЬ 2099' : 'KOBYLA HAS WAKEN UP 2099';

            const titleText = currentLang === 'ru' ? node.title_ru : node.title_en;
            const speakerText = currentLang === 'ru' ? node.speaker_ru : node.speaker_en;
            const bodyText = currentLang === 'ru' ? node.text_ru : node.text_en;

            document.getElementById('chapter-title').innerText = titleText;
            document.getElementById('speaker-name').innerText = speakerText;
            document.getElementById('story-text').innerText = bodyText;

            triggerFx(node.effect);

            historyLog.push({{ speaker: speakerText, text: bodyText }});

            const choicesBox = document.getElementById('choices-box');
            choicesBox.innerHTML = '';

            if (node.is_ending) {{
                const restartBtn = document.createElement('button');
                restartBtn.className = 'btn-choice';
                restartBtn.innerText = currentLang === 'ru' ? ' Перезапустить книгу-новеллу 2099' : ' Reboot Cyberpunk Novel';
                restartBtn.onclick = () => restartGame();
                choicesBox.appendChild(restartBtn);
                return;
            }}

            node.choices.forEach((c) => {{
                const btn = document.createElement('button');
                btn.className = 'btn-choice';
                btn.innerText = currentLang === 'ru' ? c.text_ru : c.text_en;
                btn.onclick = () => makeChoice(c);
                choicesBox.appendChild(btn);
            }});
        }}

        function makeChoice(choice) {{
            if (!musicEngine.isPlaying) {{
                toggleMusic();
            }}

            if (choice.stats) {{
                if (choice.stats.sanity !== undefined) stats.sanity += choice.stats.sanity;
                if (choice.stats.willpower !== undefined) stats.willpower += choice.stats.willpower;
                if (choice.stats.blood !== undefined) stats.blood += choice.stats.blood;

                if (stats.sanity > 100) stats.sanity = 100;
                if (stats.sanity < 0) stats.sanity = 0;
            }}

            if (choice.sound) {{
                playSound(choice.sound);
            }}

            currentNodeId = choice.next;

            if (currentNodeId === 'CHECK_ENDING_SEAL') {{
                if (stats.sanity <= 20) currentNodeId = 'ENDING_3_TRAPPED';
                else currentNodeId = 'ENDING_1_SEALED';
            }}
            else if (currentNodeId === 'CHECK_ENDING_VESSEL') {{
                currentNodeId = 'ENDING_2_VESSEL';
            }}
            else if (currentNodeId === 'CHECK_ENDING_FIRE') {{
                currentNodeId = 'ENDING_4_FIRE';
            }}
            else if (currentNodeId === 'CHECK_ENDING_HERALD') {{
                currentNodeId = 'ENDING_5_HERALD';
            }}

            updateUI();
        }}

        function toggleLanguage() {{
            currentLang = currentLang === 'ru' ? 'en' : 'ru';
            updateUI();
        }}

        function openHistory() {{
            const modal = document.getElementById('modal-box');
            const title = document.getElementById('modal-title');
            const body = document.getElementById('modal-body');

            title.innerText = currentLang === 'ru' ? 'НЕЙРО-ЛОГ ТЕРМИНАЛА' : 'NEURAL TERMINAL LOG';
            body.innerHTML = historyLog.map(h => 
                `<div style="margin-bottom:10px; border-bottom:1px solid #ff0033; padding-bottom:6px;">
                    <strong style="color:var(--neon-cyan);">${{h.speaker}}:</strong><br>
                    <span>${{h.text}}</span>
                 </div>`
            ).join('');

            modal.classList.add('active');
        }}

        function closeModal() {{
            document.getElementById('modal-box').classList.remove('active');
        }}

        function restartGame() {{
            currentNodeId = 'START';
            currentTrack = 'ambient';
            stats = {{ sanity: 100, willpower: 50, blood: 0 }};
            historyLog = [];
            closeModal();
            updateUI();
            playSound('jack_in');
        }}

        // Matrix rain
        const canvas = document.getElementById('fx-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resizeCanvas() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        for (let i = 0; i < 55; i++) {{
            particles.push({{
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                length: Math.random() * 18 + 5,
                speedY: Math.random() * 3.5 + 1,
                alpha: Math.random() * 0.7 + 0.3
            }});
        }}

        function animateParticles() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {{
                p.y += p.speedY;
                if (p.y > canvas.height) p.y = 0;

                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p.x, p.y + p.length);
                ctx.strokeStyle = `rgba(0, 240, 255, ${{p.alpha}})`;
                ctx.lineWidth = 1;
                ctx.stroke();
            }});
            requestAnimationFrame(animateParticles);
        }}
        animateParticles();

        window.onload = () => {{
            updateUI();
        }};
    </script>
</body>
</html>
"""

with open("/home/user/kobyla_has_waken_up.html", "w", encoding="utf-8") as f:
    f.write(html_book_cyberpunk_template)

print("Saved book-length Cyberpunk VN with multi-track music!")

