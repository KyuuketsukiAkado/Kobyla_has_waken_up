from generate_book_vn import book_story_nodes

md_book_content = """# KOBYLA HAS WAKEN UP 2099 / КОБЫЛА ПРОСНУЛАСЬ 2099
## Книга-Новелла: Полное Киберпанк Постапокалиптическое Издание
### Full Book-Length Interactive Cyberpunk Visual Novel Script & Technical Guide

---

## ⚡ КОНЦЕПЦИЯ И МИРОУСТРОЙСТВО / WORLD & CONCEPT

**Русский:**
2099 год. Земля после глобального коллапса цивилизации. Неоновые руины Сектора 0, кислотные дожди, заброшенные бункеры и черный рынок био-имплантов.

Эта новелла создана как полноценная **интерактивная книга** с масштабным литературным повествованием, глубоким прорабатыванием лора, развитыми диалогами и множеством уникальных персонажей.

### 🎭 Действующие Лица:
1. **Вэнс (Vance)** — Боевой нетраннер и кибер-экзорцист с плазменным клинком.
2. **КОБЫЛА-99 (KOBYLA-99)** — Главный Антагонист. Запрещенный био-ИИ и демонический вирус, проснувшийся в серверах Бункера-7.
3. **Кира Вейн (Kira Vane)** — Циничный главный фиксер Сектора 0 с кибер-глазом.
4. **Голем-09 (Unit-09 "Golem")** — 300-килограммовый наемник-киборг, зараженный сигналом Кобылы.
5. **Доктор Маркус Арис (Dr. Marcus Aris)** — Ученый, 20 лет удерживавший Кобылу в капсуле жизнеобеспечения.
6. **Эхо-7 (Echo-7)** — Голографический фантом из Призрачной Сети.

---

## 🎵 ДИНАМИЧЕСКИЙ МУЛЬТИ-ТРЕКОВЫЙ САУНДТРЕК (4 ТРЕКА)

Музыкальная система на Web Audio API автоматически меняет трек в зависимости от сюжета:
1. **`ambient` — THE NEON RUINS (90 BPM)**: Атмосферный эмбиент-синтвейв для исследования и диалогов.
2. **`confrontation` — CYBER-DEMON ENCOUNTER (110 BPM)**: Агрессивный Darksynth для сражений и напряжения.
3. **`intense` — NEURAL OVERLOAD MATRIX (135 BPM)**: Высокоскоростной хард-киберпанк для схватки внутри матрицы.
4. **`resolution` — AFTERMATH (70 BPM)**: Глубокий, медленный постапокалиптический гул для финалов.

---

## 📜 ПОЛНЫЙ КНИЖНЫЙ СЦЕНАРИЙ / FULL NOVEL SCRIPT

"""

for node_id, node in book_story_nodes.items():
    md_book_content += f"### Node ID: `{node_id}`\n"
    md_book_content += f"**Глава/Сцена:** {node['title_ru']} / {node['title_en']}\n\n"
    md_book_content += f"**Музыкальный трек:** `{node.get('music_track', 'ambient')}`\n\n"
    md_book_content += f"**Говорящий:** {node['speaker_ru']} / {node['speaker_en']}\n\n"
    md_book_content += f"#### Текст (Русский):\n{node['text_ru']}\n\n"
    md_book_content += f"#### Text (English):\n{node['text_en']}\n\n"
    
    if 'choices' in node and node['choices']:
        md_book_content += "**Варианты действий / Choices:**\n"
        for idx, choice in enumerate(node['choices'], 1):
            md_book_content += f"{idx}. **[RU]** {choice['text_ru']}\n"
            md_book_content += f"   **[EN]** {choice['text_en']}\n"
            md_book_content += f"   *(Переход -> `{choice['next']}` | Статы: {choice.get('stats', {})})*\n"
    md_book_content += "\n---\n\n"

with open("/home/user/KOBYLA_HAS_WAKEN_UP_SCRIPT.md", "w", encoding="utf-8") as f:
    f.write(md_book_content)

print("Saved Book-Length Cyberpunk KOBYLA_HAS_WAKEN_UP_SCRIPT.md")

