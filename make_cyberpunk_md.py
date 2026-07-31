from generate_cyberpunk_vn import cyber_story_nodes

md_cyber_content = """# KOBYLA HAS WAKEN UP 2099 / КОБЫЛА ПРОСНУЛАСЬ 2099
## Киберпанк Постапокалиптический Сценарий Визуальной Новеллы
### Cyberpunk Post-Apocalyptic Visual Novel Script & Technical Manual

---

## ⚡ КОНЦЕПЦИЯ И СЕТТИНГ / CONCEPT & SETTING

**Русский:**
2099 год. Земля после коллапса цивилизации. Кислотные дожди, неоновые руины Сектора 0, сгоревшие мегабашни и черные рынки био-имплантов.

Главный антагонист новеллы — **КОБЫЛА-99 (KOBYLA-99)**, запрещенный военный био-демон и ИИ-вирус, запертый 80 лет назад в довоенном сервере. Она проявляется через древний терминал, отображающий кровоточащий масляный холст с черным кибер-конем, алой энергетической матрицей и белыми оптическими лазерными сканерами.

Игрок выступает в роли **Вэнса (Vance)** — кибер-экзорциста и боевого нетраннера с плазменным клинком, нейро-декой и защитными фаерволами.

Стиль текста: хлёсткий, динамичный, короткие бьющие предложения без воды и графоманства.

**English:**
Year 2099. Post-collapse Cyberpunk Wasteland. Acid rain, Sector 0 neon ruins, melted megatowers, and black markets for bio-implants.

The main antagonist is **KOBYLA-99**—a forbidden military bio-AI daemon sealed inside an ancient pre-war terminal display. She manifests as a cybernetic mare with an obsidian hide, a crimson energy ring matrix, and twin white optical scanners.

You play as **Vance**—a combat Netrunner and Cyber-Exorcist armed with a plasma blade and neural shockers.

Style: Punchy, visceral, fast-paced kinetic cyberpunk action with zero fluff.

---

## 🎵 САУНДТРЕК И ЗВУК / SYNTHWAVE MUSIC & AUDIO

Новелла оснащена встроенным непрерывным синтезатором **Darksynth / Synthwave 110 BPM** на Web Audio API:
* **Бас-линия**: Низкий рычащий пилообразный бас с фильтром lowpass.
* **Ритм-секция**: Тяжелый кибер-бочка (Kick Drum) каждые 4 доли.
* **Арпеджиатор**: Высокие неон-аккорды в стиле 80s Darksynth.
* **Звуковые эффекты**: Звуки подключения нейро-деки, свист плазменного клинка, визг био-ИИ, импульсы взлома.

---

## 🎭 ПЕРСОНАЖИ И ХАРАКТЕРИСТИКИ / STATS

1. **Cyber-Sanity / Нейро-Рассудок (0–100%)**: Сохранность структуры мозга против вирусной перезаписи.
2. **Willpower / Воля**: Мощность духовных фаерволов и способность выдерживать ментальные удары.
3. **Bio-Corrupt / Заражение**: Уровень проникновения кода KOBYLA-99 в кибер-импланты игрока.

---

## 📜 СЦЕНАРИЙ НОВЕЛЛЫ / SCRIPT

"""

for node_id, node in cyber_story_nodes.items():
    md_cyber_content += f"### Node ID: `{node_id}`\n"
    md_cyber_content += f"**Сектор/Сцена:** {node['title_ru']} / {node['title_en']}\n\n"
    md_cyber_content += f"**Персонаж:** {node['speaker_ru']} / {node['speaker_en']}\n\n"
    md_cyber_content += f"#### Текст (Русский):\n{node['text_ru']}\n\n"
    md_cyber_content += f"#### Text (English):\n{node['text_en']}\n\n"
    
    if 'choices' in node and node['choices']:
        md_cyber_content += "**Варианты действий / Choices:**\n"
        for idx, choice in enumerate(node['choices'], 1):
            md_cyber_content += f"{idx}. **[RU]** {choice['text_ru']}\n"
            md_cyber_content += f"   **[EN]** {choice['text_en']}\n"
            md_cyber_content += f"   *(Переход -> `{choice['next']}` | Статы: {choice.get('stats', {})})*\n"
    md_cyber_content += "\n---\n\n"

with open("/home/user/KOBYLA_HAS_WAKEN_UP_SCRIPT.md", "w", encoding="utf-8") as f:
    f.write(md_cyber_content)

print("Saved Cyberpunk KOBYLA_HAS_WAKEN_UP_SCRIPT.md")

