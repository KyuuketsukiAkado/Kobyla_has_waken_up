import json, base64

# Load image in base64
image_path = "/home/user/uploads/111.png"
with open(image_path, "rb") as img_file:
    img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
img_data_url = f"data:image/png;base64,{img_b64}"

from build_full_vn import story_nodes

# Generate HTML file
html_template = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KOBYLA HAS WAKEN UP / КОБЫЛА ПРОСНУЛАСЬ - Visual Novel</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Marcellus&display=swap');

        :root {{
            --bg-dark: #050202;
            --panel-bg: rgba(18, 8, 8, 0.88);
            --border-red: #8b0000;
            --glow-red: #ff1a1a;
            --text-light: #e0d5d5;
            --text-gold: #e6c687;
            --accent-blood: #dc143c;
            --font-en: 'Cinzel', serif;
            --font-ru: 'Playfair Display', 'Marcellus', serif;
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
            font-family: var(--font-ru);
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            background-image: 
                radial-gradient(circle at 50% 30%, rgba(139, 0, 0, 0.25) 0%, rgba(5, 2, 2, 0.95) 70%),
                repeating-linear-gradient(0deg, rgba(0,0,0,0.15) 0px, rgba(0,0,0,0.15) 1px, transparent 1px, transparent 2px);
        }}

        /* Overlay Visual Effects */
        #fx-canvas {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 1;
        }}

        .screen-flash {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            z-index: 100;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        .screen-flash.flash-red {{
            background-color: rgba(220, 20, 60, 0.6);
            opacity: 1;
        }}
        .screen-flash.flash-white {{
            background-color: rgba(255, 255, 255, 0.85);
            opacity: 1;
        }}

        /* Main Container */
        #app-container {{
            position: relative;
            z-index: 2;
            width: 100%;
            max-width: 1200px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 15px;
        }}

        /* Header Bar */
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background: rgba(10, 3, 3, 0.85);
            border: 1px solid var(--border-red);
            border-radius: 4px;
            box-shadow: 0 0 15px rgba(255, 26, 26, 0.2);
            margin-bottom: 10px;
        }}

        .game-title {{
            font-family: var(--font-en);
            font-size: 1.3rem;
            font-weight: 900;
            letter-spacing: 2px;
            color: var(--glow-red);
            text-shadow: 0 0 8px rgba(255, 26, 26, 0.6);
        }}

        .controls {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}

        button.btn-ctrl {{
            background: linear-gradient(180deg, #2a0808 0%, #120303 100%);
            color: var(--text-gold);
            border: 1px solid var(--border-red);
            padding: 6px 14px;
            font-family: var(--font-en);
            font-size: 0.85rem;
            cursor: pointer;
            border-radius: 3px;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        button.btn-ctrl:hover {{
            background: var(--border-red);
            color: #fff;
            box-shadow: 0 0 10px var(--glow-red);
        }}

        /* Stats Bar */
        .stats-bar {{
            display: flex;
            gap: 20px;
            padding: 6px 15px;
            background: rgba(15, 5, 5, 0.7);
            border: 1px solid rgba(139, 0, 0, 0.4);
            border-radius: 4px;
            margin-bottom: 10px;
            font-size: 0.9rem;
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

        /* Stage Layout */
        #game-stage {{
            flex: 1;
            display: flex;
            gap: 20px;
            overflow: hidden;
            margin-bottom: 10px;
        }}

        /* Portrait Area */
        .portrait-frame {{
            flex: 0 0 380px;
            position: relative;
            background: #000;
            border: 2px solid var(--border-red);
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0,0,0,0.9), inset 0 0 15px rgba(255,26,26,0.3);
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .portrait-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease, filter 0.5s ease;
        }}

        .portrait-frame.pulse-red .portrait-img {{
            animation: pulseAura 2s infinite alternate;
        }}

        .portrait-frame.shake-heavy {{
            animation: shakeHard 0.4s infinite;
        }}

        @keyframes pulseAura {{
            0% {{ filter: drop-shadow(0 0 10px var(--glow-red)) contrast(1.1); transform: scale(1); }}
            100% {{ filter: drop-shadow(0 0 30px var(--glow-red)) contrast(1.35) brightness(1.1); transform: scale(1.03); }}
        }}

        @keyframes shakeHard {{
            0% {{ transform: translate(1px, 1px) rotate(0deg); }}
            20% {{ transform: translate(-3px, 0px) rotate(1deg); }}
            40% {{ transform: translate(1px, -1px) rotate(-1deg); }}
            60% {{ transform: translate(-2px, 2px) rotate(0deg); }}
            80% {{ transform: translate(2px, 1px) rotate(1deg); }}
            100% {{ transform: translate(1px, -2px) rotate(-1deg); }}
        }}

        /* Glowing eyes effect overlay */
        .eye-glow-overlay {{
            position: absolute;
            top: 45%;
            left: 42%;
            width: 18%;
            height: 8%;
            background: radial-gradient(ellipse at center, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0) 70%);
            mix-blend-mode: screen;
            opacity: 0.8;
            pointer-events: none;
            animation: eyePulse 1.5s infinite alternate;
        }}

        @keyframes eyePulse {{
            0% {{ opacity: 0.5; filter: blur(2px); }}
            100% {{ opacity: 1; filter: blur(5px); }}
        }}

        /* Narrative Window */
        .story-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--panel-bg);
            border: 1px solid var(--border-red);
            border-radius: 4px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
            overflow-y: auto;
        }}

        .speaker-box {{
            font-family: var(--font-en);
            font-size: 1.1rem;
            font-weight: bold;
            color: var(--glow-red);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 1px solid rgba(139, 0, 0, 0.5);
            padding-bottom: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .chapter-title {{
            font-size: 0.85rem;
            color: var(--text-gold);
            font-style: italic;
        }}

        .story-text {{
            font-size: 1.05rem;
            line-height: 1.7;
            color: var(--text-light);
            margin-bottom: 20px;
            white-space: pre-wrap;
            flex: 1;
        }}

        /* Choices Area */
        .choices-container {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 10px;
        }}

        button.btn-choice {{
            background: linear-gradient(90deg, rgba(30, 8, 8, 0.9) 0%, rgba(60, 10, 10, 0.9) 100%);
            color: var(--text-light);
            border: 1px solid var(--border-red);
            padding: 12px 18px;
            text-align: left;
            font-family: inherit;
            font-size: 0.95rem;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
        }}

        button.btn-choice::before {{
            content: "◆ ";
            color: var(--glow-red);
            margin-right: 10px;
            font-size: 0.8rem;
        }}

        button.btn-choice:hover {{
            background: linear-gradient(90deg, rgba(139, 0, 0, 0.8) 0%, rgba(80, 5, 5, 0.9) 100%);
            color: #fff;
            box-shadow: 0 0 12px rgba(255, 26, 26, 0.5);
            transform: translateX(5px);
        }}

        /* Ending Screen Modal / Overlay */
        .modal-overlay {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.85);
            backdrop-filter: blur(5px);
            z-index: 500;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.4s ease;
        }}

        .modal-overlay.active {{
            opacity: 1;
            pointer-events: auto;
        }}

        .modal-card {{
            background: #120505;
            border: 2px solid var(--glow-red);
            padding: 30px;
            max-width: 650px;
            width: 90%;
            border-radius: 6px;
            box-shadow: 0 0 30px rgba(255, 26, 26, 0.4);
            max-height: 85vh;
            overflow-y: auto;
        }}

        .modal-title {{
            font-family: var(--font-en);
            font-size: 1.5rem;
            color: var(--glow-red);
            margin-bottom: 15px;
            text-align: center;
            border-bottom: 1px solid var(--border-red);
            padding-bottom: 10px;
        }}

        .modal-body {{
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: 20px;
            color: var(--text-light);
        }}

        /* Responsive Design */
        @media (max-width: 850px) {{
            #game-stage {{
                flex-direction: column;
            }}
            .portrait-frame {{
                flex: 0 0 220px;
                width: 100%;
            }}
            .story-container {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>

    <canvas id="fx-canvas"></canvas>
    <div id="screen-flash" class="screen-flash"></div>

    <div id="app-container">
        <header>
            <div class="game-title" id="ui-title">KOBYLA HAS WAKEN UP</div>
            <div class="controls">
                <button class="btn-ctrl" id="btn-lang" onclick="toggleLanguage()">RU / EN</button>
                <button class="btn-ctrl" id="btn-audio" onclick="toggleAudio()">🔊 FX ON</button>
                <button class="btn-ctrl" id="btn-history" onclick="openHistory()">📜 LOG</button>
                <button class="btn-ctrl" id="btn-restart" onclick="restartGame()">🔄 RESTART</button>
            </div>
        </header>

        <div class="stats-bar">
            <div class="stat-item">
                <span id="lbl-sanity">Sanity (Рассудок):</span>
                <span class="stat-val" id="val-sanity">100%</span>
            </div>
            <div class="stat-item">
                <span id="lbl-willpower">Willpower (Воля):</span>
                <span class="stat-val" id="val-willpower">50</span>
            </div>
            <div class="stat-item">
                <span id="lbl-blood">Blood Mark (Кровь):</span>
                <span class="stat-val" id="val-blood">0</span>
            </div>
        </div>

        <div id="game-stage">
            <div class="portrait-frame pulse-red" id="portrait-box">
                <img src="{img_data_url}" alt="Kobyla" class="portrait-img" id="portrait-img">
                <div class="eye-glow-overlay"></div>
            </div>

            <div class="story-container">
                <div class="speaker-box">
                    <span id="speaker-name">SPEAKER</span>
                    <span class="chapter-title" id="chapter-title">CHAPTER</span>
                </div>
                <div class="story-text" id="story-text">Loading story...</div>
                <div class="choices-container" id="choices-box"></div>
            </div>
        </div>
    </div>

    <!-- Modal for History / Log / Ending -->
    <div class="modal-overlay" id="modal-box">
        <div class="modal-card">
            <div class="modal-title" id="modal-title">HISTORY LOG</div>
            <div class="modal-body" id="modal-body"></div>
            <div style="text-align: center;">
                <button class="btn-ctrl" onclick="closeModal()">CLOSE</button>
            </div>
        </div>
    </div>

    <script>
        // Story Data Object
        const storyData = {json.dumps(story_nodes, ensure_ascii=False, indent=2)};

        // Game State
        let currentLang = 'ru'; // Default to Russian as requested, can toggle to EN
        let currentNodeId = 'START';
        let stats = {{
            sanity: 100,
            willpower: 50,
            blood: 0
        }};
        let historyLog = [];
        let audioEnabled = true;
        let audioCtx = null;

        // Web Audio Synthesizer
        function initAudio() {{
            if (!audioCtx) {{
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }}
        }}

        function playSound(type) {{
            if (!audioEnabled) return;
            initAudio();
            if (!audioCtx) return;

            const now = audioCtx.currentTime;

            if (type === 'whisper') {{
                // Soft dark noise burst
                const bufferSize = audioCtx.sampleRate * 0.4;
                const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
                const data = buffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) {{
                    data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.3));
                }}
                const noise = audioCtx.createBufferSource();
                noise.buffer = buffer;
                const filter = audioCtx.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.value = 400;
                noise.connect(filter);
                filter.connect(audioCtx.destination);
                noise.start(now);
            }} 
            else if (type === 'heartbeat') {{
                // Double thump
                [0, 0.2].forEach(offset => {{
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(60, now + offset);
                    osc.frequency.exponentialRampToValueAtTime(30, now + offset + 0.15);
                    gain.gain.setValueAtTime(0.5, now + offset);
                    gain.gain.exponentialRampToValueAtTime(0.01, now + offset + 0.15);
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start(now + offset);
                    osc.stop(now + offset + 0.2);
                }});
            }} 
            else if (type === 'blade') {{
                // High metallic sheen
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(1200, now);
                osc.frequency.exponentialRampToValueAtTime(300, now + 0.3);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start(now);
                osc.stop(now + 0.35);
            }} 
            else if (type === 'screech' || type === 'roar') {{
                // Harsh screech sting
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(150, now);
                osc.frequency.linearRampToValueAtTime(800, now + 0.15);
                osc.frequency.exponentialRampToValueAtTime(80, now + 0.6);
                gain.gain.setValueAtTime(0.4, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.6);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start(now);
                osc.stop(now + 0.65);
            }}
            else if (type === 'chant') {{
                // Sacred resonant chime
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(440, now);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start(now);
                osc.stop(now + 1.25);
            }}
        }}

        function triggerFx(fxType) {{
            const portraitBox = document.getElementById('portrait-box');
            const flash = document.getElementById('screen-flash');

            portraitBox.className = 'portrait-frame ' + (fxType || 'pulse-red');

            if (fxType === 'blood-flash' || fxType === 'blood-bleed') {{
                flash.className = 'screen-flash flash-red';
                setTimeout(() => flash.className = 'screen-flash', 400);
            }} else if (fxType === 'flash-white') {{
                flash.className = 'screen-flash flash-white';
                setTimeout(() => flash.className = 'screen-flash', 500);
            }}
        }}

        function updateUI() {{
            const node = storyData[currentNodeId];
            if (!node) return;

            // Labels
            document.getElementById('lbl-sanity').innerText = currentLang === 'ru' ? 'Рассудок:' : 'Sanity:';
            document.getElementById('lbl-willpower').innerText = currentLang === 'ru' ? 'Воля:' : 'Willpower:';
            document.getElementById('lbl-blood').innerText = currentLang === 'ru' ? 'Кровавая Метка:' : 'Blood Mark:';

            document.getElementById('val-sanity').innerText = stats.sanity + '%';
            document.getElementById('val-willpower').innerText = stats.willpower;
            document.getElementById('val-blood').innerText = stats.blood;

            document.getElementById('ui-title').innerText = currentLang === 'ru' ? 'КОБЫЛА ПРОСНУЛАСЬ' : 'KOBYLA HAS WAKEN UP';

            const titleText = currentLang === 'ru' ? node.title_ru : node.title_en;
            const speakerText = currentLang === 'ru' ? node.speaker_ru : node.speaker_en;
            const bodyText = currentLang === 'ru' ? node.text_ru : node.text_en;

            document.getElementById('chapter-title').innerText = titleText;
            document.getElementById('speaker-name').innerText = speakerText;
            document.getElementById('story-text').innerText = bodyText;

            triggerFx(node.effect);

            // Append to history
            historyLog.push({{
                speaker: speakerText,
                text: bodyText
            }});

            // Render choices
            const choicesBox = document.getElementById('choices-box');
            choicesBox.innerHTML = '';

            if (node.is_ending) {{
                const restartBtn = document.createElement('button');
                restartBtn.className = 'btn-choice';
                restartBtn.innerText = currentLang === 'ru' ? ' Начать новеллу заново' : ' Restart Visual Novel';
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
            if (choice.stats) {{
                if (choice.stats.sanity !== undefined) stats.sanity += choice.stats.sanity;
                if (choice.stats.willpower !== undefined) stats.willpower += choice.stats.willpower;
                if (choice.stats.blood !== undefined) stats.blood += choice.stats.blood;

                // Clamp sanity
                if (stats.sanity > 100) stats.sanity = 100;
                if (stats.sanity < 0) stats.sanity = 0;
            }}

            if (choice.sound) {{
                playSound(choice.sound);
            }}

            currentNodeId = choice.next;

            // Stat driven branch triggers if appropriate
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

        function toggleAudio() {{
            audioEnabled = !audioEnabled;
            document.getElementById('btn-audio').innerText = audioEnabled ? '🔊 FX ON' : '🔇 FX OFF';
            if (audioEnabled) playSound('heartbeat');
        }}

        function openHistory() {{
            const modal = document.getElementById('modal-box');
            const title = document.getElementById('modal-title');
            const body = document.getElementById('modal-body');

            title.innerText = currentLang === 'ru' ? 'ИСТОРИЯ ДИАЛОГОВ' : 'STORY HISTORY LOG';
            body.innerHTML = historyLog.map(h => 
                `<div style="margin-bottom:12px; border-bottom:1px solid #331010; padding-bottom:8px;">
                    <strong style="color:var(--glow-red);">${{h.speaker}}:</strong><br>
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
            stats = {{ sanity: 100, willpower: 50, blood: 0 }};
            historyLog = [];
            closeModal();
            updateUI();
            playSound('chant');
        }}

        // Particle Canvas Background
        const canvas = document.getElementById('fx-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resizeCanvas() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        for (let i = 0; i < 60; i++) {{
            particles.push({{
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: Math.random() * 2 + 1,
                speedY: -Math.random() * 0.8 - 0.2,
                alpha: Math.random() * 0.6 + 0.2
            }});
        }}

        function animateParticles() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = 'rgba(255, 26, 26, ';

            particles.forEach(p => {{
                p.y += p.speedY;
                if (p.y < 0) p.y = canvas.height;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(220, 20, 60, ${{p.alpha}})`;
                ctx.fill();
            }});

            requestAnimationFrame(animateParticles);
        }}
        animateParticles();

        // Initial Load
        window.onload = () => {{
            updateUI();
        }};
    </script>
</body>
</html>
"""

with open("/home/user/kobyla_has_waken_up.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Saved kobyla_has_waken_up.html")

