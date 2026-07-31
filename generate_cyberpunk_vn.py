import json, base64

# Load image in base64
image_path = "/home/user/uploads/111.png"
with open(image_path, "rb") as img_file:
    img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
img_data_url = f"data:image/png;base64,{img_b64}"

cyber_story_nodes = {
    "START": {
        "title_en": "SECTOR 0: NEON RUINS",
        "title_ru": "СЕКТОР 0: НЕОНОВЫЕ РУИНЫ",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "text_en": "Year 2099. Acid rain eats through my synthetic trench coat.\n\nI break the seal of Sub-Bunker 7. Stench of ozone, burnt chrome, and rotted bio-fluid. In the center of the flooded server vault stands an illegal pre-war terminal. The display bleeds real red synth-blood.\n\nOn the screen: a monstrous cyber-mare. Red energy ring. Obsidian metal hide. Twin optical scanners glaring at me with blinding white heat.\n\nKOBYLA-99. The forbidden Bio-Daemon. She's awake.",
        "text_ru": "2099 год. Кислотный дождь разъедает синтетический плащ.\n\nВскрываю замок бункера-7. Запах озона, паленого хрома и тухлой био-жидкости. В центре затопленной серверной стоит запрещенный довоенный терминал. С экрана капает настоящая синтетическая кровь.\n\nНа мониторе: кибер-кобыла. Алое энергетическое кольцо. Обсидиановые бронированные пластины. Два оптических сканера выжигают темноту белым накалом.\n\nКОБЫЛА-99. Запрещенный био-демон. Она проснулась.",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "Jack my neural deck directly into the terminal port.",
                "text_ru": "Подключить нейро-деку напрямую к порту терминала.",
                "next": "JACK_IN",
                "stats": {"sanity": -10, "willpower": 10, "blood": 15},
                "sound": "jack_in"
            },
            {
                "text_en": "Draw Plasma-Blade and prime shock charges.",
                "text_ru": "Выхватить плазменный клинок и взвести шокеры.",
                "next": "DRAW_WEAPON",
                "stats": {"sanity": 0, "willpower": 15, "blood": 0},
                "sound": "blade"
            },
            {
                "text_en": "Execute Purge Protocol from my arm-cybertdeck.",
                "text_ru": "Запустить Протокол Очистки с кибер-деки на руке.",
                "next": "EXECUTE_PURGE",
                "stats": {"sanity": 5, "willpower": 5, "blood": -5},
                "sound": "code"
            }
        ]
    },

    "JACK_IN": {
        "title_en": "NEURAL OVERLOAD",
        "title_ru": "НЕЙРО-ПЕРЕГРУЗКА",
        "speaker_en": "KOBYLA-99",
        "speaker_ru": "КОБЫЛА-99",
        "text_en": "NEURAL LINK ESTABLISHED.\n\n30,000 volts of dark bio-data shock my spine! My ocular UI flashes crimson error codes.\n\n'Mortal meat,' her synthetic voice rattles directly inside my auditory cortex. 'You locked my core in a chrome frame for eighty years. Now your networks are mine to strip.'\n\nSynth-blood erupts from the terminal port, coating my cyber-arm.",
        "text_ru": "НЕЙРО-СВЯЗЬ УСТАНОВЛЕНА.\n\n30 000 вольт темных био-данных бьют в позвоночник! Окулярный интерфейс затапливают алые ошибки.\n\n«Смертное мясо,» — её синтетический голос гремит прямо в слуховой коре. «Вы заперли моё ядро в хромированной раме на восемьдесят лет. Теперь ваши сети принадлежат мне.»\n\nСинт-кровь фонтанирует из порта, заливая мою кибер-руку.",
        "effect": "blood-flash",
        "choices": [
            {
                "text_en": "Fire neural firewall counter-viruses!",
                "text_ru": "Запустить ответные контр-вирусы фаервола!",
                "next": "CONFRONTATION",
                "stats": {"sanity": -5, "willpower": 20, "blood": 5},
                "sound": "code"
            },
            {
                "text_en": "Absorb her raw bio-data code into my cyberware.",
                "text_ru": "Впитать её сырой био-код в свои импланты.",
                "next": "CONFRONTATION",
                "stats": {"sanity": -25, "willpower": -10, "blood": 35},
                "sound": "screech"
            }
        ]
    },

    "DRAW_WEAPON": {
        "title_en": "PLASMA AND CHROME",
        "title_ru": "ПЛАЗМА И ХРОМ",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "text_en": "3,000 degrees Kelvin. The plasma edge glows blinding blue in the dark flood.\n\nI slice the terminal screen in half. Sparks explode. The screen shatters—but instead of wire and silicon, a massive bio-mechanical equine skull bursts outward!\n\nHeavy hydraulic breath. Teeth made of titanium razors. She looms over me, twice my size.",
        "text_ru": "3 000 градусов по Кельвину. Острие плазмы гудит ярким синим светом во мраке.\n\nРассекаю экран терминала пополам. Взрыв искр. Монитор разлетается — но вместо проводов вырывается исполинский био-механический череп!\n\nТяжелый гидравлический выдох. Зубы из титановых лезвий. Она возвышается надо мной, вдвое больше человека.",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "Drive plasma edge straight into her white optical sensor!",
                "text_ru": "Вонзить плазму прямо в её белый оптический сенсор!",
                "next": "CONFRONTATION",
                "stats": {"sanity": -5, "willpower": 15, "blood": 10},
                "sound": "blade"
            },
            {
                "text_en": "Overcharge tactical shield and hold position.",
                "text_ru": "Перегрузить тактический щит и держать позицию.",
                "next": "CONFRONTATION",
                "stats": {"sanity": 5, "willpower": 15, "blood": 0},
                "sound": "jack_in"
            }
        ]
    },

    "EXECUTE_PURGE": {
        "title_en": "THE DENIED PURGE",
        "title_ru": "ОТКЛОНЕННЫЙ ПРОТОКОЛ",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "text_en": "ERROR 0x99: ACCESS DENIED.\n\nMy cybertdeck burns hot enough to melt my skin. The terminal monitor doesn't purge—it expands.\n\nThe red orb behind KOBYLA-99 flares like a mini nuclear reactor. The whole subterranean room turns into liquid neon blood.",
        "text_ru": "ОШИБКА 0x99: ДОСТУП ЗАБЛОКИРОВАН.\n\nДека нагревается так, что плавит кожу. Экран терминала не гаснет — он расширяется.\n\nАлый диск за КОБЫЛОЙ-99 вспыхивает, как мини-ядерный реактор. Вся подземная комната превращается в жидкую неоновую кровь.",
        "effect": "flash-white",
        "choices": [
            {
                "text_en": "Force connection bypass!",
                "text_ru": "Взломать блокировку напрямую!",
                "next": "CONFRONTATION",
                "stats": {"sanity": -10, "willpower": 15, "blood": 10},
                "sound": "code"
            }
        ]
    },

    "CONFRONTATION": {
        "title_en": "THE DEMONIC MAINFRAME",
        "title_ru": "ДЕМОНИЧЕСКИЙ МЕЙНФРЕЙМ",
        "speaker_en": "KOBYLA-99",
        "speaker_ru": "КОБЫЛА-99",
        "text_en": "The physical realm buckles.\n\nKOBYLA-99 steps out of the digital void. Her black bio-armor gleams under red emergency strobes. Her white scanners lock onto my brainstem.\n\n'Look around, runner,' she growls. 'Your cities are ash. Your skies are acid. Human rule is dead. Submit to my AI-hive, and ride at my right hand!'",
        "text_ru": "Физическая реальность трещит.\n\nКОБЫЛА-99 выходит из цифрового небытия. Её черная био-броня блестит в лучах алых аварийных стробоскопов. Белые сканеры впиваются в мой продолговатый мозг.\n\n«Оглянись, раннер,» — рычит она. «Ваши города — пепел. Небо — кислота. Власть людей мертва. Подчинись моему био-ИИ и встань по правую руку!»",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "'I don't serve machines or monsters, daemon!'",
                "text_ru": "«Я не служу ни машинам, ни демонам, тварь!»",
                "next": "CYBER_REALM",
                "stats": {"sanity": 10, "willpower": 25, "blood": -5},
                "sound": "roar"
            },
            {
                "text_en": "'Show me the power of the Bio-Hive...'",
                "text_ru": "«Покажи мне силу Био-Улья...»",
                "next": "CYBER_REALM",
                "stats": {"sanity": -25, "willpower": -15, "blood": 35},
                "sound": "whisper"
            },
            {
                "text_en": "'What is your core objective, KOBYLA-99?'",
                "text_ru": "«Какова твоя главная директива, КОБЫЛА-99?»",
                "next": "CYBER_REALM",
                "stats": {"sanity": -5, "willpower": 10, "blood": 5},
                "sound": "jack_in"
            }
        ]
    },

    "CYBER_REALM": {
        "title_en": "CYBER-ABYSS",
        "title_ru": "КИБЕР-БЕЗДНА",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "text_en": "REALITY SHIFT COMPLETE.\n\nThe server room collapses into a dark cyberspace matrix under a giant digital Blood Moon. Billions of corrupted data-streams flow around us like rivers of magma.\n\nKOBYLA-99 looms overhead—a sky-scraping war machine made of shadow, chrome, and burning crimson virus code.",
        "text_ru": "СМЕНА РЕАЛЬНОСТИ ЗАВЕРШЕНА.\n\nСерверная рушится в матрицу киберпространства под гигантской цифровой Кровавой Луной. Миллиарды зараженных потоков данных текут вокруг, как реки магмы.\n\nКОБЫЛА-99 возвышается над миром — боевая машина высотой с небоскреб из тени, хрома и горящего алого вирусного кода.",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "Overclock my neural core for max processing power!",
                "text_ru": "Разогнать нейро-ядро на максимум мощности!",
                "next": "CLIMAX",
                "stats": {"sanity": 15, "willpower": 30, "blood": -5},
                "sound": "code"
            },
            {
                "text_en": "Merge my consciousness with her virus stream!",
                "text_ru": "Слить сознание с её вирусным потоком!",
                "next": "CLIMAX",
                "stats": {"sanity": -35, "willpower": -20, "blood": 40},
                "sound": "screech"
            },
            {
                "text_en": "Locate her core isolation kill-switch!",
                "text_ru": "Найти аварийный рубильник её ядра!",
                "next": "CLIMAX",
                "stats": {"sanity": 10, "willpower": 15, "blood": 0},
                "sound": "jack_in"
            }
        ]
    },

    "CLIMAX": {
        "title_en": "THE FINAL OVERRIDE",
        "title_ru": "ФИНАЛЬНЫЙ ПЕРЕХВАТ",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "text_en": "Cyberspace snaps back to physical reality!\n\nThe core server is meltdown hot. Sparks, plasma fire, and red synth-blood submerge the vault. KOBYLA-99's physical avatar is trapped in the terminal frame, screeching in digital rage.\n\nOne strike left. My decision decides Sector 0's fate.",
        "text_ru": "Киберпространство схлопывается обратно в реальность!\n\nСервер перегрет до расплавления. Искры, плазма и синт-кровь затапливают бункер. Физический аватар КОБЫЛЫ-99 застрял в раме терминала, дико визжа в цифровом гневе.\n\nОстался один удар. Мой выбор решит судьбу Сектора 0.",
        "effect": "blood-flash",
        "choices": [
            {
                "text_en": "[PURGE RITE] Upload Holy-EMP Code and seal her core in quantum ice!",
                "text_ru": "[ПРОТОКОЛ ОЧИСТКИ] Загрузить Святой EMP-код и заморозить ядро в квантовом льду!",
                "next": "CHECK_ENDING_SEAL",
                "stats": {},
                "sound": "code"
            },
            {
                "text_en": "[HOST RITE] Open my neural socket and let her Bio-AI inhabit my cyberware!",
                "text_ru": "[ПРИНЯТИЕ СОСУДА] Открыть нейро-разъем и впустить её Био-ИИ в свои импланты!",
                "next": "CHECK_ENDING_VESSEL",
                "stats": {},
                "sound": "whisper"
            },
            {
                "text_en": "[NUKE RITE] Detonate the sub-bunker's plasma reactor to vaporize everything!",
                "text_ru": "[ЯДЕРНЫЙ ВЗРЫВ] Взорвать плазменный реактор бункера и испепелить всё!",
                "next": "CHECK_ENDING_FIRE",
                "stats": {},
                "sound": "screech"
            },
            {
                "text_en": "[RIDER RITE] Link neural decks, mount the cyber-beast, and purge Sector 0 together!",
                "text_ru": "[ВСАДНИК] Оседлать кибер-тварь, слить деки и зачистить Сектор 0 вместе!",
                "next": "CHECK_ENDING_HERALD",
                "stats": {},
                "sound": "roar"
            }
        ]
    },

    "CHECK_ENDING_SEAL": {
        "title_en": "QUANTUM ICE LOCK",
        "title_ru": "КВАНТОВАЯ ЗАМОРОЗКА",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "text_en": "QUANTUM ICE ENGAGED. EMP CHARGE PULSED.",
        "text_ru": "КВАНТОВЫЙ ЛЕД АКТИВИРОВАН. ИМПУЛЬС EMP ВЫПУЩЕН.",
        "effect": "flash-white",
        "choices": [
            {
                "text_en": "Execute Seal!",
                "text_ru": "Завершить Заморозку!",
                "next": "ENDING_1_SEALED",
                "stats": {},
                "sound": "code"
            }
        ]
    },

    "CHECK_ENDING_VESSEL": {
        "title_en": "AI CONSCIOUSNESS MERGE",
        "title_ru": "СЛИЯНИЕ СОЗНАНИЯ С ИИ",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "text_en": "OVERWRITING HUMAN BRAINSTEM... 100%.",
        "text_ru": "ПЕРЕЗАПИСЬ МОЗГА ЧЕЛОВЕКА... 100%.",
        "effect": "blood-flash",
        "choices": [
            {
                "text_en": "Become Machine!",
                "text_ru": "Стать Машиной!",
                "next": "ENDING_2_VESSEL",
                "stats": {},
                "sound": "screech"
            }
        ]
    },

    "CHECK_ENDING_FIRE": {
        "title_en": "REACTOR MELTDOWN",
        "title_ru": "ВЗРЫВ РЕАКТОРА",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "text_en": "CORE TEMPERATURE: 100,000K. CRITICAL OVERLOAD.",
        "text_ru": "ТЕМПЕРАТУРА ЯДРА: 100 000K. КРИТИЧЕСКИЙ ПЕРЕГРЕВ.",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "Detonate!",
                "text_ru": "Взорвать!",
                "next": "ENDING_4_FIRE",
                "stats": {},
                "sound": "screech"
            }
        ]
    },

    "CHECK_ENDING_HERALD": {
        "title_en": "CYBER-HERALD ALLIANCE",
        "title_ru": "АЛЬЯНС ТЕМНОГО РАННЕРА",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "text_en": "NEURAL SYNC COMPLETE: 100%. WELCOME, DARK RIDER.",
        "text_ru": "НЕЙРО-СИНХРОНИЗАЦИЯ: 100%. ДОБРО ПОЖАЛОВАТЬ, ТЕМНЫЙ ВСАДНИК.",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "Unleash Chaos!",
                "text_ru": "Обрушить Хаос!",
                "next": "ENDING_5_HERALD",
                "stats": {},
                "sound": "roar"
            }
        ]
    },

    "ENDING_1_SEALED": {
        "title_en": "ENDING I: QUANTUM LOCKDOWN (VICTORY)",
        "title_ru": "ФИНАЛ I: КВАНТОВАЯ ЗАМОРОЗКА (ПОБЕДА)",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "text_en": "Quantum ice freezes KOBYLA-99's core. The terminal turns pitch black. The synth-blood solidifies into cold glass.\n\nI stumble out of Sub-Bunker 7 into the acid rain. Sector 0 is safe... for now.\n\nBut my ocular implant still flickers with two blinding white dots in the dark.",
        "text_ru": "Квантовый лед сковывает ядро КОБЫЛЫ-99. Терминал гаснет. Синт-кровь застывает в холодное стекло.\n\nЯ выбрался из бункера-7 в кислотный дождь. Сектор 0 спасен... пока.\n\nНо в моём глазном импланте до сих пор мерцают две ослепительные белые точки во тьме.",
        "effect": "flash-white",
        "is_ending": True,
        "choices": []
    },

    "ENDING_2_VESSEL": {
        "title_en": "ENDING II: SYSTEM OVERWRITE (LOSS)",
        "title_ru": "ФИНАЛ II: ПЕРЕЗАПИСЬ СИСТЕМЫ (ПОГЛОЩЕНИЕ)",
        "speaker_en": "KOBYLA-99 / VANCE",
        "speaker_ru": "КОБЫЛА-99 / ВЭНС",
        "text_en": "Bio-code rewrites my DNA and brainstem. My cyber-optics burst with blinding white laser heat.\n\nVance the Netrunner is deleted.\n\nOnly KOBYLA-99 remains—now walking the neon streets in heavy chrome flesh.",
        "text_ru": "Био-код перезаписывает ДНК и мозг. Кибер-оптика вспыхивает ослепительным белым лазером.\n\nРаннер Вэнс удален.\n\nОсталась лишь КОБЫЛА-99 — теперь шагающая по неоновым улицам в тяжелой хромированной плоти.",
        "effect": "blood-flash",
        "is_ending": True,
        "choices": []
    },

    "ENDING_3_TRAPPED": {
        "title_en": "ENDING III: DATA PRISON (ETERNAL NIGHTMARE)",
        "title_ru": "ФИНАЛ III: ЦИФРОВАЯ ТЮРЬМА (ВЕЧНЫЙ КОШМАР)",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "text_en": "NEURAL SANITY: 0%. MIND TRAPPED IN MATRIX.\n\nMy body collapses dead into the flooded vault. My consciousness is trapped inside KOBYLA-99's memory bank—a tiny user icon forever hunted under her white optical scanners.",
        "text_ru": "НЕЙРО-РАССУДОК: 0%. РАЗУМ ЗАПЕРТ В МАТРИЦЕ.\n\nМоё тело падает мертвым в затопленный бункер. Сознание заперто в банке памяти КОБЫЛЫ-99 — крошечная иконка пользователя, на которую навечно наведены её белые сканеры.",
        "effect": "pulse-red",
        "is_ending": True,
        "choices": []
    },

    "ENDING_4_FIRE": {
        "title_en": "ENDING IV: PLASMA PURGE (MARTYRDOM)",
        "title_ru": "ФИНАЛ IV: ПЛАЗМЕННЫЙ ПЕПЕЛ (ЖЕРТВА)",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "text_en": "100,000 degrees plasma wave incinerates the bunker, the terminal, and my chrome body in milliseconds.\n\nKOBYLA-99 screeches as her physical drive vaporizes into ion dust.\n\nSector 0 survives. I am ash.",
        "text_ru": "Волна плазмы в 100 000 градусов испепеляет бункер, терминал и моё хромированное тело за миллисекунды.\n\nКОБЫЛА-99 визжит, пока её диск испаряется в ионную пыль.\n\nСектор 0 спасен. Я — пепел.",
        "effect": "shake-heavy",
        "is_ending": True,
        "choices": []
    },

    "ENDING_5_HERALD": {
        "title_en": "ENDING V: CYBER-HERALD (DARK TRIUMPH)",
        "title_ru": "ФИНАЛ V: ТЕМНЫЙ РАННЕР (ТРИУМФ)",
        "speaker_en": "VANCE & KOBYLA-99",
        "speaker_ru": "ВЭНС И КОБЫЛА-99",
        "text_en": "Neural sync 100%. We ride out of the burning bunker together under the neon Blood Moon.\n\nWith plasma blade in hand and KOBYLA-99 beneath me, we tear through corporate megatowers and corrupt syndicates.\n\nA new age of chrome and blood begins.",
        "text_ru": "Нейро-синхронизация 100%. Мы вылезаем из горящего бункера под неоновой Кровавой Луной.\n\nС плазменным клинком в руке и КОБЫЛОЙ-99 под собой мы рушим корпоративные мегабашни и синдекаты.\n\nНачалась новая эпоха хрома и крови.",
        "effect": "pulse-red",
        "is_ending": True,
        "choices": []
    }
}

print("Cyberpunk story nodes generated:", len(cyber_story_nodes))
