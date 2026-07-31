import json, base64

image_path = "/home/user/uploads/111.png"
with open(image_path, "rb") as img_file:
    img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
img_data_url = f"data:image/png;base64,{img_b64}"

from expanded_story import expanded_nodes as publicist_nodes

html_template = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOBYLA HAS WAKEN UP 2099 / КОБЫЛА ПРОСНУЛАСЬ 2099 - Publicist Edition</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;700&family=Inter:wght@400;600;800;900&display=swap');

        :root {{
            --bg-dark: #080608;
            --panel-bg: rgba(14, 10, 16, 0.94);
            --border-red: #dc143c;
            --glow-red: #ff1a40;
            --neon-cyan: #00d8ff;
            --text-light: #e8eeef;
            --text-gold: #ffc837;
            --font-main: 'Roboto Mono', monospace;
            --font-title: 'Inter', sans-serif;
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
                radial-gradient(circle at 50% 20%, rgba(220, 20, 60, 0.18) 0%, rgba(8, 6, 8, 0.98) 75%),
                linear-gradient(rgba(0, 216, 255, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 216, 255, 0.02) 1px, transparent 1px);
            background-size: 100% 100%, 25px 25px, 25px 25px;
        }}

        body::after {{
            content: " ";
            display: block;
            position: absolute;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.22) 50%);
            background-size: 100% 4px;
            z-index: 99;
            pointer-events: none;
            opacity: 0.7;
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
            background-color: rgba(220, 20, 60, 0.45);
            opacity: 1;
        }}
        .screen-flash.flash-white {{
            background-color: rgba(0, 216, 255, 0.65);
            opacity: 1;
        }}

        #app-container {{
            position: relative;
            z-index: 2;
            width: 100%;
            max-width: 1280px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 12px;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background: rgba(16, 10, 20, 0.94);
            border: 1px solid var(--border-red);
            border-radius: 3px;
            box-shadow: 0 0 15px rgba(220, 20, 60, 0.25);
            margin-bottom: 8px;
        }}

        .game-title {{
            font-family: var(--font-title);
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: 1px;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .game-title span.badge {{
            background: var(--border-red);
            color: #fff;
            padding: 2px 8px;
            border-radius: 2px;
            font-size: 0.75rem;
            text-transform: uppercase;
        }}

        .track-indicator {{
            font-size: 0.75rem;
            color: var(--neon-cyan);
            background: rgba(0, 216, 255, 0.08);
            padding: 4px 10px;
            border: 1px solid rgba(0, 216, 255, 0.4);
            border-radius: 2px;
        }}

        .controls {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}

        button.btn-ctrl {{
            background: #120a14;
            color: var(--neon-cyan);
            border: 1px solid var(--neon-cyan);
            padding: 6px 14px;
            font-family: var(--font-title);
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            border-radius: 2px;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        button.btn-ctrl:hover {{
            background: var(--border-red);
            color: #fff;
            border-color: var(--border-red);
            box-shadow: 0 0 10px var(--glow-red);
        }}

        button.btn-music-active {{
            background: var(--border-red) !important;
            color: #fff !important;
            border-color: var(--border-red) !important;
        }}

        .stats-bar {{
            display: flex;
            gap: 25px;
            padding: 6px 18px;
            background: rgba(12, 8, 16, 0.9);
            border: 1px solid rgba(220, 20, 60, 0.35);
            border-radius: 2px;
            margin-bottom: 8px;
            font-size: 0.85rem;
        }}

        .stat-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .stat-val {{
            font-weight: bold;
            color: var(--text-gold);
        }}

        #game-stage {{
            flex: 1;
            display: flex;
            gap: 15px;
            overflow: hidden;
            margin-bottom: 8px;
        }}

        .portrait-frame {{
            flex: 0 0 380px;
            position: relative;
            background: #000;
            border: 2px solid var(--border-red);
            border-radius: 2px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0,0,0,0.9), inset 0 0 15px rgba(220,20,60,0.3);
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .portrait-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease, filter 0.3s ease;
            filter: contrast(1.15) saturate(1.1);
        }}

        .portrait-frame.pulse-red .portrait-img {{
            animation: pulseAura 2s infinite alternate;
        }}

        .portrait-frame.shake-heavy {{
            animation: shakeHard 0.3s infinite;
        }}

        @keyframes pulseAura {{
            0% {{ filter: drop-shadow(0 0 8px var(--border-red)) contrast(1.15); transform: scale(1); }}
            100% {{ filter: drop-shadow(0 0 25px var(--glow-red)) contrast(1.3) brightness(1.1); transform: scale(1.02); }}
        }}

        @keyframes shakeHard {{
            0% {{ transform: translate(1px, 1px); }}
            25% {{ transform: translate(-2px, -1px); }}
            50% {{ transform: translate(2px, 2px); }}
            75% {{ transform: translate(-1px, 1px); }}
            100% {{ transform: translate(1px, -1px); }}
        }}

        .eye-glow-overlay {{
            position: absolute;
            top: 44%;
            left: 42%;
            width: 18%;
            height: 8%;
            background: radial-gradient(ellipse at center, rgba(255,255,255,0.95) 0%, rgba(220,20,60,0) 75%);
            mix-blend-mode: screen;
            opacity: 0.85;
            pointer-events: none;
            animation: eyePulse 1.2s infinite alternate;
        }}

        @keyframes eyePulse {{
            0% {{ opacity: 0.5; filter: blur(2px); }}
            100% {{ opacity: 1; filter: blur(4px); }}
        }}

        .story-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--panel-bg);
            border: 1px solid var(--border-red);
            border-radius: 2px;
            padding: 22px;
            box-shadow: 0 0 25px rgba(0, 0, 0, 0.85);
            overflow-y: auto;
        }}

        .speaker-box {{
            font-family: var(--font-title);
            font-size: 1.05rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(220, 20, 60, 0.4);
            padding-bottom: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .chapter-title {{
            font-size: 0.8rem;
            color: var(--neon-cyan);
            font-family: var(--font-main);
            font-weight: 500;
        }}

        .story-text {{
            font-size: 1.02rem;
            line-height: 1.65;
            color: var(--text-light);
            margin-bottom: 20px;
            white-space: pre-wrap;
            flex: 1;
        }}

        .choices-container {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 5px;
        }}

        button.btn-choice {{
            background: linear-gradient(90deg, rgba(24, 14, 22, 0.95) 0%, rgba(42, 18, 32, 0.95) 100%);
            color: var(--text-light);
            border: 1px solid var(--border-red);
            padding: 12px 18px;
            text-align: left;
            font-family: var(--font-main);
            font-size: 0.92rem;
            cursor: pointer;
            border-radius: 2px;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            line-height: 1.4;
        }}

        button.btn-choice::before {{
            content: "▶ ";
            color: var(--neon-cyan);
            margin-right: 10px;
            font-size: 0.8rem;
        }}

        button.btn-choice:hover {{
            background: linear-gradient(90deg, rgba(220, 20, 60, 0.85) 0%, rgba(0, 216, 255, 0.85) 100%);
            color: #000;
            font-weight: bold;
            box-shadow: 0 0 12px var(--neon-cyan);
            transform: translateX(4px);
        }}

        .modal-overlay {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(4, 2, 6, 0.92);
            backdrop-filter: blur(5px);
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
            background: #0e0a12;
            border: 2px solid var(--border-red);
            padding: 25px;
            max-width: 680px;
            width: 90%;
            border-radius: 2px;
            box-shadow: 0 0 30px rgba(220, 20, 60, 0.3);
            max-height: 85vh;
            overflow-y: auto;
        }}

        .modal-title {{
            font-family: var(--font-title);
            font-size: 1.25rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 12px;
            text-align: center;
            border-bottom: 1px solid var(--border-red);
            padding-bottom: 8px;
        }}

        .modal-body {{
            font-size: 0.92rem;
            line-height: 1.55;
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
            <div class="game-title">
                KOBYLA HAS WAKEN UP 2099
                <span class="badge">Публицистическое Издание</span>
            </div>
            <div class="track-indicator" id="track-name">ТРЕК: НЕОНОВЫЕ РУИНЫ (90 BPM)</div>
            <div class="controls">
                <button class="btn-ctrl" id="btn-music" onclick="toggleMusic()">🎵 MUSIC: OFF</button>
                <button class="btn-ctrl" id="btn-lang" onclick="toggleLanguage()">RU / EN</button>
                <button class="btn-ctrl" id="btn-history" onclick="openHistory()">📜 LOG</button>
                <button class="btn-ctrl" id="btn-restart" onclick="restartGame()">🔄 RESTART</button>
            </div>
        </header>

        <div class="stats-bar">
            <div class="stat-item">
                <span id="lbl-sanity">Нейро-Рассудок:</span>
                <span class="stat-val" id="val-sanity">100%</span>
            </div>
            <div class="stat-item">
                <span id="lbl-willpower">Воля:</span>
                <span class="stat-val" id="val-willpower">50</span>
            </div>
            <div class="stat-item">
                <span id="lbl-blood">Уровень Инфекции:</span>
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
                    <span id="speaker-name">СПИКЕР</span>
                    <span class="chapter-title" id="chapter-title">ГЛАВА</span>
                </div>
                <div class="story-text" id="story-text">ЗАГРУЗКА ИНТЕРФЕЙСА...</div>
                <div class="choices-container" id="choices-box"></div>
            </div>
        </div>
    </div>

    <!-- Modal -->
    <div class="modal-overlay" id="modal-box">
        <div class="modal-card">
            <div class="modal-title" id="modal-title">ЖУРНАЛ ИЗМЕНЕНИЙ СИСТЕМЫ</div>
            <div class="modal-body" id="modal-body"></div>
            <div style="text-align: center;">
                <button class="btn-ctrl" onclick="closeModal()">ЗАКРЫТЬ</button>
            </div>
        </div>
    </div>

    <script>
        const storyData = {json.dumps(publicist_nodes, ensure_ascii=False, indent=2)};

        let currentLang = 'ru';
        let currentNodeId = 'START';
        let currentTrack = 'ambient';
        let stats = {{ sanity: 100, willpower: 50, blood: 0 }};
        let historyLog = [];

        // Web Audio Synthesizer Engine
        class MultiTrackMusicEngine {{
            constructor() {{
                this.ctx = null;
                this.isPlaying = false;
                this.timer = null;
                this.step = 0;
                this.activeTrack = 'ambient';

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
                    }},
                    horror: {{
                        name_ru: 'ТРЕК 5: НЕЙРОННЫЙ КОШМАР (60 BPM)',
                        name_en: 'TRACK 5: NEURAL NIGHTMARE (60 BPM)',
                        tempo: 60,
                        bass: [32.7, 30.87, 27.5, 24.5],
                        arp: [130.81, 138.59, 123.47, 116.54],
                        waveform: 'sine',
                        kickInterval: 16
                    }},
                    battle: {{
                        name_ru: 'ТРЕК 6: СТОЛКНОВЕНИЕ С ГОЛЕМОМ (150 BPM)',
                        name_en: 'TRACK 6: GOLEM CONFRONTATION (150 BPM)',
                        tempo: 150,
                        bass: [55, 65.4, 55, 73.4, 55, 87.3, 55, 98],
                        arp: [220, 330, 440, 550, 660, 440],
                        waveform: 'sawtooth',
                        kickInterval: 1
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

                    gain.gain.setValueAtTime(0.28, now);
                    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.18);

                    osc.connect(filter);
                    filter.connect(gain);
                    gain.connect(this.ctx.destination);

                    osc.start(now);
                    osc.stop(now + 0.2);
                }}

                if (step % config.kickInterval === 0) {{
                    const kickOsc = this.ctx.createOscillator();
                    const kickGain = this.ctx.createGain();

                    kickOsc.type = 'sine';
                    kickOsc.frequency.setValueAtTime(150, now);
                    kickOsc.frequency.exponentialRampToValueAtTime(30, now + 0.1);

                    kickGain.gain.setValueAtTime(0.5, now);
                    kickGain.gain.exponentialRampToValueAtTime(0.01, now + 0.11);

                    kickOsc.connect(kickGain);
                    kickGain.connect(this.ctx.destination);

                    kickOsc.start(now);
                    kickOsc.stop(now + 0.12);
                }}

                const arpFreq = config.arp[step % config.arp.length];
                const arpOsc = this.ctx.createOscillator();
                const arpGain = this.ctx.createGain();

                arpOsc.type = 'triangle';
                arpOsc.frequency.setValueAtTime(arpFreq, now);

                arpGain.gain.setValueAtTime(0.05, now);
                arpGain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

                arpOsc.connect(arpGain);
                arpGain.connect(this.ctx.destination);

                arpOsc.start(now);
                arpOsc.stop(now + 0.09);

                this.step = (this.step + 1) % 32;
            }}
        }}

        const musicEngine = new MultiTrackMusicEngine();

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
            else if (type === 'heartbeat') {{
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(60, now);
                osc.frequency.exponentialRampToValueAtTime(20, now + 0.1);
                gain.gain.setValueAtTime(0.6, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.2);
            }}
            else if (type === 'static' || type === 'glitch') {{
                const bufferSize = ctx.sampleRate * 0.2;
                const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
                const data = buffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) {{
                    data[i] = Math.random() * 2 - 1;
                }}
                const noise = ctx.createBufferSource();
                noise.buffer = buffer;
                const gain = ctx.createGain();
                gain.gain.setValueAtTime(0.1, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
                noise.connect(gain);
                gain.connect(ctx.destination);
                noise.start(now);
                noise.stop(now + 0.2);
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

            if (node.music_track && node.music_track !== currentTrack) {{
                currentTrack = node.music_track;
                musicEngine.switchTrack(currentTrack);
            }}

            const trackInfo = musicEngine.tracks[currentTrack];
            document.getElementById('track-name').innerText = currentLang === 'ru' ? trackInfo.name_ru : trackInfo.name_en;

            document.getElementById('lbl-sanity').innerText = currentLang === 'ru' ? 'Нейро-Рассудок:' : 'Cyber-Sanity:';
            document.getElementById('lbl-willpower').innerText = currentLang === 'ru' ? 'Воля:' : 'Willpower:';
            document.getElementById('lbl-blood').innerText = currentLang === 'ru' ? 'Инфекция:' : 'Infection:';

            document.getElementById('val-sanity').innerText = stats.sanity + '%';
            document.getElementById('val-willpower').innerText = stats.willpower;
            document.getElementById('val-blood').innerText = stats.blood;

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
                restartBtn.innerText = currentLang === 'ru' ? ' Перезапустить публицистическую новеллу' : ' Restart Publicist Visual Novel';
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

            title.innerText = currentLang === 'ru' ? 'ЖУРНАЛ ИЗМЕНЕНИЙ СИСТЕМЫ' : 'SYSTEM CHANGE LOG';
            body.innerHTML = historyLog.map(h => 
                `<div style="margin-bottom:10px; border-bottom:1px solid #dc143c; padding-bottom:6px;">
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

        const canvas = document.getElementById('fx-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resizeCanvas() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        for (let i = 0; i < 45; i++) {{
            particles.push({{
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                length: Math.random() * 15 + 5,
                speedY: Math.random() * 3 + 1,
                alpha: Math.random() * 0.6 + 0.2
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
                ctx.strokeStyle = `rgba(0, 216, 255, ${{p.alpha}})`;
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
    f.write(html_template)

print("Saved publicist edition kobyla_has_waken_up.html")

