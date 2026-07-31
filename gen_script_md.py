# -*- coding: utf-8 -*-
"""
Regenerates KOBYLA_HAS_WAKEN_UP_SCRIPT.md (bilingual script document)
from the expanded story data used by the game.
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from story_part1 import NODES_A
from story_part2 import NODES_B
from story_part3 import NODES_C
from story_part4 import NODES_D
from story_part5 import NODES_E

story = {}
for part in (NODES_A, NODES_B, NODES_C, NODES_D, NODES_E):
    story.update(part)

MUSIC = {
    'ambient': 'ТРЕК 1: НЕОНОВЫЕ РУИНЫ (90 BPM) / TRACK 1: THE NEON RUINS (90 BPM)',
    'confrontation': 'ТРЕК 2: КИБЕР-ДЕМОН БУНКЕРА (110 BPM) / TRACK 2: CYBER-DEMON ENCOUNTER (110 BPM)',
    'intense': 'ТРЕК 3: НЕЙРО-ПЕРЕГРУЗКА МАТРИЦЫ (135 BPM) / TRACK 3: NEURAL OVERLOAD MATRIX (135 BPM)',
    'resolution': 'ТРЕК 4: ЭХО ПОСТАПОКАЛИПСИСА (70 BPM) / TRACK 4: AFTERMATH OF THE RED ECLIPSE (70 BPM)',
    'horror': 'ТРЕК 5: НЕЙРОННЫЙ КОШМАР (60 BPM) / TRACK 5: NEURAL NIGHTMARE (60 BPM)',
    'battle': 'ТРЕК 6: СТОЛКНОВЕНИЕ С ГОЛЕМОМ (150 BPM) / TRACK 6: GOLEM CONFRONTATION (150 BPM)',
    'stalk': 'ТРЕК 7: ПУЛЬС В ТУМАНЕ (65 BPM) / TRACK 7: PULSE IN THE FOG (65 BPM)',
    'war': 'ТРЕК 8: ВОЙНА БУНКЕРА (170 BPM) / TRACK 8: BUNKER WAR (170 BPM)',
    'void': 'ТРЕК 9: БЕЗДНА НЕЙРОНОВ (55 BPM) / TRACK 9: THE NEURAL VOID (55 BPM)',
    'ascension': 'ТРЕК 10: ВОЗНЕСЕНИЕ (78 BPM) / TRACK 10: ASCENSION (78 BPM)',
    'finale': 'ТРЕК 11: ПОСЛЕ СИГНАЛА (72 BPM) / TRACK 11: AFTER THE SIGNAL (72 BPM)',
}

order = [
    'START',
    'AUDIT_ENTRY', 'AUDIT_LOGS', 'AUDIT_INFECTION', 'AUDIT_HALLWAY', 'AUDIT_HALLWAY2', 'AUDIT_LAB_ENTRY',
    'BIO_HORROR', 'ARIS_DEATH', 'HIVE_PURGE', 'FINAL_BOSS', 'CORE_CONFRONTATION',
    'HACK_ENTRY', 'HACK_MATRIX', 'HACK_SNEAK', 'HACK_VAULT', 'HACK_DUEL', 'HACK_KEY', 'HACK_DIVE',
    'BURN_ENTRY', 'BURN_CHARGE', 'BURN_STAMPEDE', 'BURN_EMP', 'BURN_DARK',
    'ENDING_AUDIT', 'ENDING_UPLOAD', 'ENDING_PURGE', 'ENDING_CHAOS',
]

def dump_node(k):
    v = story[k]
    ch = v.get('choices', [])
    L = []
    L.append(f"### Node ID: `{k}`")
    L.append(f"**Сцена:** {v.get('title_ru','')} / {v.get('title_en','')}")
    track = MUSIC.get(v.get('music_track'), v.get('music_track'))
    L.append(f"**Музыка:** `{v.get('music_track')}` — {track}")
    L.append(f"**Спикер:** {v.get('speaker_ru','')} / {v.get('speaker_en','')}")
    if v.get('is_ending'):
        L.append("**СТАТУС: КОНЕЦ ПРОХОЖДЕНИЯ / ENDING NODE**")
        L.append(f"**Итог (RU):** {v.get('ending_tag_ru','')} | **Route:** {v.get('route_ru','')}")
    L.append("")
    L.append("#### Текст (Русский):")
    L.append(v.get('text_ru',''))
    L.append("")
    L.append("#### Text (English):")
    L.append(v.get('text_en',''))
    if v.get('is_ending'):
        L.append("")
        L.append("**📊 АНАЛИТИЧЕСКИЙ ВЫВОД (RU):**")
        L.append(v.get('takeaway_ru',''))
        L.append("")
        L.append("**📊 ANALYTICAL TAKEAWAY (EN):**")
        L.append(v.get('takeaway_en',''))
    L.append("")
    if ch:
        L.append("**Варианты ответов / Choices:**")
        for i, c in enumerate(ch, 1):
            L.append(f"{i}. **[RU]** {c.get('text_ru','')}")
            L.append(f"   **[EN]** {c.get('text_en','')}")
            st = c.get('stats') or {}
            L.append(f"   *(Переход -> `{c.get('next')}` | Статы: {st} | Звук: {c.get('sound')})*")
        L.append("")
    L.append("---")
    L.append("")
    return '\n'.join(L)

hdr = """# KOBYLA HAS WAKEN UP 2099 / КОБЫЛА ПРОСНУЛАСЬ 2099
## Публицистический Сценарий и Аналитический Документ (Расширенное издание)
### Publicist Style Interactive Cyberpunk Script & Analytical Guide — Expanded Edition

---

## 🏛️ СТИЛЬ И ПУБЛИЦИСТИЧЕСКАЯ КОНЦЕПЦИЯ / STYLE & CONCEPT

**Русский:**
Настоящее издание новеллы переработано в **стиле современного аналитика и публициста**. Текст освобожден от клинических клише и бессмысленного «графоманства». Повествование — строгая логика, чёткие аргументы, глубинные параллели между развитием искусственного интеллекта, корпоративной этикой и выживанием человека. Расширенное издание добавляет экшен, драму и элементы хоррора, не меняя стилистику.

### 🔀 Разветвленная система Рутов (Multiple Routes):
1. **РУТ А: КОРПОРАТИВНЫЙ АУДИТ (Corporate Audit Route)** — Расследование причин сбоя, анализ системных ошибок менеджмента и протоколирование био-нейронной угрозы.
2. **РУТ Б: ТЕНЕВОЙ ВЗЛОМ (Underground Netrunning Route)** — Теневая извлечение ядра для черного рынка, исследование алгоритмической свободы ИИ.
3. **РУТ В: РАДИКАЛЬНАЯ ЛИКВИДАЦИЯ (Sanctioned Containment Route)** — Бескомпромиссная силовая очистка и термическое уничтожение угрозы.

### 🎵 МУЛЬТИ-ТРЕКОВАЯ МУЗЫКА / MULTI-TRACK WEB AUDIO
11 динамических треков (Web Audio API): ambient, confrontation, intense, resolution, horror, battle + 5 новых — stalk, war, void, ascension, finale.

### 📖 РОМАН ВНУТРИ ИГРЫ / NOVEL IN GAME
Полный текст романа «КОБЫЛА ПРОСНУЛАСЬ 2099. Книга первая: АНАЛИТИКА ОТЧАЯНИЯ» встроен в игру кнопкой «📖 РОМАН» в шапке.

---

"""
body = '\n'.join(dump_node(k) for k in order)
open('KOBYLA_HAS_WAKEN_UP_SCRIPT.md', 'w', encoding='utf-8').write(hdr + body)
print('script md regenerated:', len(hdr + body), 'chars, nodes:', len(order))
