from build_publicist_vn import publicist_nodes

md_pub_content = """# KOBYLA HAS WAKEN UP 2099 / КОБЫЛА ПРОСНУЛАСЬ 2099
## Публицистический Сценарий и Аналитический Документ
### Publicist Style Interactive Cyberpunk Script & Analytical Guide

---

## 🏛️ СТИЛЬ И ПУБЛИЦИСТИЧЕСКАЯ КОНЦЕПЦИЯ / STYLE & CONCEPT

**Русский:**
Настоящее издание новеллы переработано в **стиле современного аналитика и публициста**. Текст освобожден от клинических клише и бессмысленного «графоманства». Повествование строгая логика, чёткие аргументы, глубинные параллели между развитием искусственного интеллекта, корпоративной этикой и выживанием человека.

### 🔀 Разветвленная система Рутов (Multiple Routes):
1. **РУТ А: КОРПОРАТИВНЫЙ АУДИТ (Corporate Audit Route)** — Расследование причин сбоя, анализ системных ошибок менеджмента и протоколирование био-нейронной угрозы.
2. **РУТ Б: ТЕНЕВОЙ ВЗЛОМ (Underground Netrunning Route)** — Теневая извлечение ядра для черного рынка, исследование алгоритмической свободы ИИ.
3. **РУТ В: РАДИКАЛЬНАЯ ЛИКВИДАЦИЯ (Sanctioned Containment Route)** — Бескомпромиссная силовая очистка и термическое уничтожение угрозы.

---

## 🎵 МУЛЬТИ-ТРЕКОВАЯ МУЗЫКА / MULTI-TRACK WEB AUDIO

Встроенная интерактивная музыкальная система (Web Audio API) включает 4 динамических трека:
* **`ambient` — ТРЕК 1: НЕОНОВЫЕ РУИНЫ (90 BPM)**: Атмосферный аналитический синтвейв.
* **`confrontation` — ТРЕК 2: КИБЕР-ДЕМОН БУНКЕРА (110 BPM)**: Darksynth для тактических конфликтов.
* **`intense` — ТРЕК 3: НЕЙРО-ПЕРЕГРУЗКА МАТРИЦЫ (135 BPM)**: Скоростной хард-киберпанк.
* **`resolution` — ТРЕК 4: ЭХО ПОСТАПОКАЛИПСИСА (70 BPM)**: Глубокий гул с выводами.

---

## 📜 ПОЛНЫЙ ПУБЛИЦИСТИЧЕСКИЙ СЦЕНАРИЙ И ВЫВОДЫ / SCRIPT & TAKEAWAYS

"""

for node_id, node in publicist_nodes.items():
    md_pub_content += f"### Node ID: `{node_id}`\n"
    md_pub_content += f"**Сцена:** {node['title_ru']} / {node['title_en']}\n\n"
    md_pub_content += f"**Музыка:** `{node.get('music_track', 'ambient')}`\n\n"
    md_pub_content += f"**Спикер:** {node['speaker_ru']} / {node['speaker_en']}\n\n"
    md_pub_content += f"#### Текст (Русский):\n{node['text_ru']}\n\n"
    md_pub_content += f"#### Text (English):\n{node['text_en']}\n\n"
    
    if 'choices' in node and node['choices']:
        md_pub_content += "**Варианты ответов / Choices:**\n"
        for idx, choice in enumerate(node['choices'], 1):
            md_pub_content += f"{idx}. **[RU]** {choice['text_ru']}\n"
            md_pub_content += f"   **[EN]** {choice['text_en']}\n"
            md_pub_content += f"   *(Переход -> `{choice['next']}` | Статы: {choice.get('stats', {})})*\n"
    md_pub_content += "\n---\n\n"

with open("/home/user/KOBYLA_HAS_WAKEN_UP_SCRIPT.md", "w", encoding="utf-8") as f:
    f.write(md_pub_content)

print("Saved Publicist KOBYLA_HAS_WAKEN_UP_SCRIPT.md")

