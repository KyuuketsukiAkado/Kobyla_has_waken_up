import json
from build_full_vn import story_nodes

md_content = """# KOBYLA HAS WAKEN UP / КОБЫЛА ПРОСНУЛАСЬ
## Полный сценарий и игровой дидактический гид интерактивной визуальной новеллы
### Full Interactive Visual Novel Script & Lore Document

---

## 👁️ ОБ ОБЗОРЕ И КОНЦЕПЦИИ / CONCEPT & OVERVIEW

**Русский:**
«KOBYLA HAS WAKEN UP / КОБЫЛА ПРОСНУЛАСЬ» — это готическая хоррор-визуальная новелла в жанре космического и древнеславянского мистического ужаса. Главным антагонистом новеллы выступает **Кобыла (Kobyla)** — древняя сущность, запертая на проклятом масляном холсте 1384 года безумным иконописцем братом Власом. 

Когда красное лунное затмение разрушает печати, масляные краски сжижаются, и Кобыла пробуждается. Игрок выступает в роли доктора Ильи Вэнса (Dr. Elijah Vance), ученого-экзорциста и антиквара, пытающегося сдержать пробудившийся кошмар.

**English:**
"KOBYLA HAS WAKEN UP / КОБЫЛА ПРОСНУЛАСЬ" is a gothic dark-horror visual novel blending cosmic dread and ancient Slavic folklore. The central antagonist is **Kobyla (The Mare)**—an eldritch nightmare entity trapped within a cursed 1384 oil canvas by the insane iconographer Brother Vlas.

When a red moon alignment shatters the ancient wards, the crimson paint turns to real blood and Kobyla awakens. You play as Dr. Elijah Vance, an antiquarian exorcist scholar struggling to bind or survive the unleashed nightmare.

---

## 🎭 ДЕЙСТВУЮЩИЕ ЛИЦА / CHARACTERS

### 1. Кобыла (Kobyla / The Nightmare Mare) — Главный Антагонист
* **Внешность:** Исполинская черная кобыла с шерстью цвета сгоревшего бархата, бушующей гривой из алого пламени и двумя слепящими ослепительно-белыми глазами без зрачков. За её головой висит багровый диск Алого Затмения.
* **Характер:** Древняя, насмешливая, вечная и беспощадная. Она питается страхом, грехами и человеческими снами.
* **Голос:** Хриплый, многоголосый шёпот, гремящий в голове жертвы подобно кузнечному молоту.

### 2. Доктор Илья Вэнс (Dr. Elijah Vance) — Протагонист
* **Роль:** Экзорцист, антиквар и хранитель тайных фолиантов. 
* **Характеристики:**
  * **Sanity / Рассудок (0–100%):** Показывает устойчивость психики к ментальным атакам Кобылы.
  * **Willpower / Воля:** Сила духовной защиты и способности противостоять гипнозу.
  * **Blood Mark / Кровавая Метка:** Уровень осквернения и ментальной связи с Кобылой.

---

## 🗺️ КАРТА РАЗВЕТВЛЕНИЙ И 5 ФИНАЛОВ / BRANCHING MAP & ENDINGS

1. **ФИНАЛ I: Священное Заточение (Sacred Sealing)** — Требует высокую Волю и Рассудок. Кобыла затягивается обратно в холст золотыми цепями. Илья выживает, но навсегда остается отмечен взглядом белых глаз.
2. **ФИНАЛ II: Сосуд Алого Затмения (The Red Eclipse Incarnate)** — Высокая Кровавая Метка. Илья отдает своё тело, становясь человеческим воплощением Кобылы на Земле.
3. **ФИНАЛ III: Пленник Алого Холста (Trapped in the Bleeding Canvas)** — Падение Рассудка до 0. Душа Илья затягивается в картину, становясь маленькой тенью на фоне Кобылы.
4. **ФИНАЛ IV: Пепел Святого Власа (Ashes of St. Vlas)** — Поджог монастыря. Илья и Кобыла сгорают в священном огне, спасая мир ценой жизни.
5. **ФИНАЛ V: Всадник Апокалипсиса (The Dark Herald)** — Принятие союза. Илья становится Темным Всадником Кобылы, несущим гибель королям и праведникам.

---

## 📜 ПОЛНЫЙ ДВУЯЗЫЧНЫЙ СЦЕНАРИЙ / FULL BILINGUAL SCRIPT

"""

# Append nodes
for node_id, node in story_nodes.items():
    md_content += f"### Node ID: `{node_id}`\n"
    md_content += f"**Заголовок:** {node['title_ru']} / {node['title_en']}\n\n"
    md_content += f"**Говорящий:** {node['speaker_ru']} / {node['speaker_en']}\n\n"
    md_content += f"#### Текст (Русский):\n{node['text_ru']}\n\n"
    md_content += f"#### Text (English):\n{node['text_en']}\n\n"
    
    if 'choices' in node and node['choices']:
        md_content += "**Варианты ответов / Choices:**\n"
        for idx, choice in enumerate(node['choices'], 1):
            md_content += f"{idx}. **[RU]** {choice['text_ru']}\n"
            md_content += f"   **[EN]** {choice['text_en']}\n"
            md_content += f"   *(Переход -> `{choice['next']}` | Статы: {choice.get('stats', {})})*\n"
    md_content += "\n---\n\n"

with open("/home/user/KOBYLA_HAS_WAKEN_UP_SCRIPT.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("Saved KOBYLA_HAS_WAKEN_UP_SCRIPT.md")

