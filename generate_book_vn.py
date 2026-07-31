import json, base64

image_path = "/home/user/uploads/111.png"
with open(image_path, "rb") as img_file:
    img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
img_data_url = f"data:image/png;base64,{img_b64}"

# Expanded Story Nodes - Novel Length & Multi-Character
book_story_nodes = {
    "START": {
        "title_en": "PROLOGUE: CONTRACT AT THE CHROME SKULL",
        "title_ru": "ПРОЛОГ: КОНТРАКТ В «ХРОМОВОМ ЧЕРЕПЕ»",
        "speaker_en": "NARRATOR / VANCE",
        "speaker_ru": "ПОВЕСТВОВАТЕЛЬ / ВЭНС",
        "music_track": "ambient",
        "text_en": "The rain in Sector 0 doesn't just wet your clothes—it melts them. Acid fumes rise from the asphalt of the Neon Ruins. Year 2099. Humanity didn't die with a bang; it decayed into chrome, synthetic gore, and corporate debt.\n\nInside 'The Chrome Skull' dive bar, blue holographic smoke curls through the air. Across the rusted steel booth sits Kira Vane—Sector 0's most notorious Fixer. Her left eye is a high-grade military optics scanner glowing icy cyan, and her cybernetic fingers tap rhythmically against a glass of synthetic whiskey.\n\n'Listen closely, Vance,' Kira says, her voice low and laced with gravel. 'Three hours ago, a deep-underground salvage team breached Sub-Bunker 7 beneath the flooded reactor district. They didn't find old weapons. They found a pre-war black-box server rack sealed with bio-locks from 1384. Every scav in the squad had their brains fried through their optical jacks within six seconds. Blood boiled out of their ears.'\n\nShe slides a encrypted datapad across the stained table. On it flashes an image: an ancient oil canvas depicting a terrifying black mare surrounded by a red ring of fire, her eyes twin voids of blinding white light.\n\n'That's KOBYLA-99,' Kira continues. 'A forbidden pre-collapse Bio-AI daemon created by blending ancient occult rituals with quantum neural-chips. The corp lords will pay ten million credits for her core. I need a Netrunner who knows how to kill demons.'",
        "text_ru": "Кислотный дождь в Секторе 0 не просто мочит одежду — он ест ткань до мяса. От раскаленного асфальта Неоновых Руин поднимается едкий пар. 2099 год. Человечество не погибло со взрывом; оно сгнило в хром, синт-кровь и корпоративные долги.\n\nВ подпольном баре «Хромовый Череп» кружится синий голографический дым. Напротив меня за столом из ржавой стали сидит Кира Вейн — главный фиксер Сектора 0. Её левый глаз — военный оптический сканер, светящийся ледяным цианом. Её кибернетические пальцы ритмично стучат по стакану с синтетическим виски.\n\n«Слушай внимательно, Вэнс,» — говорит Кира. Голос низкий, с хрипом. «Три часа назад мусорщики вскрыли Бункер-7 под затопленным реактором. Они искали довоенные стволы, а нашли серверный блок, запечатанный био-замками 1384 года. Через шесть секунд у всей группы закипели мозги прямо через глазные разъемы. Кровь фонтаном ударила из ушей.»\n\nОна двигает по столу зашифрованный датапад. На нем мерцает изображение: старинный масляный холст с черной кобылой в алом огненном кольце. Её глаза — два ослепительных белых лазерных омута.\n\n«Это КОБЫЛА-99,» — продолжала Кира. «Запрещенный био-ИИ демон, созданный на стыке древнего мистицизма и квантовых нейро-чипов. Корпораты заплатят десять миллионов кредитов за её ядро. Мне нужен нетраннер, который умеет убивать демонов.»",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "'Ten million credits? I'm in. Slot the bunker access codes.'",
                "text_ru": "«Десять миллионов? Я в деле. Загружай коды доступа в бункер.»",
                "next": "BUNKER_ENTRY",
                "stats": {"sanity": 0, "willpower": 10, "blood": 0},
                "sound": "jack_in"
            },
            {
                "text_en": "'A bio-AI that fries netrunners? I need weapon prep before I drop down.'",
                "text_ru": "«Био-ИИ, выжигающий мозги? Мне нужна подзарядка оружия перед спуском.»",
                "next": "WEAPON_PREP",
                "stats": {"sanity": 5, "willpower": 15, "blood": 0},
                "sound": "blade"
            },
            {
                "text_en": "'Who created KOBYLA-99, Kira? Give me the real story.'",
                "text_ru": "«Кто создал КОБЫЛУ-99, Кира? Назови мне реальные имена.»",
                "next": "KIRA_LORE",
                "stats": {"sanity": 0, "willpower": 5, "blood": 0},
                "sound": "code"
            }
        ]
    },

    "KIRA_LORE": {
        "title_en": "PROLOGUE: THE SECRET ARCHITECTS",
        "title_ru": "ПРОЛОГ: ТАЙНЫЕ АРХИТЕКТОРЫ",
        "speaker_en": "KIRA VANE",
        "speaker_ru": "КИРА ВЕЙН",
        "music_track": "ambient",
        "text_en": "Kira takes a long drag from her synth-cigarette, exhaling a cloud of glowing purple smoke.\n\n'In 1384, a Slavic iconographer named Brother Vlas painted a curse using dried blood and crushed mercury. Before he went mad and gouged out his eyes, he claimed a dark entity from the stars spoke to him. Fast forward to 2070: military bio-engineers from Ares Dynamics extracted the DNA-pigments from that painting and fed it into a quantum neural network. They thought they were building an apex digital weapon.'\n\nShe leans forward, her cyan optic focusing on my face.\n\n'They were wrong. They didn't build a weapon. They built a cage for a cosmic nightmare. When the Great Fall happened, Sub-Bunker 7 was sealed. Now her battery is full, and she wants out.'",
        "text_ru": "Кира делает затяжку синт-сигаретой, выдыхая облако фиолетового дыма.\n\n«В 1384 году славянский иконописец по имени брат Влас написал проклятие кровью и ртутью. Перед тем как выколоть себе глаза, он твердил, что с ним говорила звезда. В 2070 году био-инженеры корпорации 'Арес' извлекли ДНК-пигменты той картины и загрузили их в квантовую нейросеть. Они думали, что делают лучшее кибер-оружие в истории.»\n\nОна наклоняется ближе, её оптический глазок фокусируется на мне.\n\n«Они ошиблись. Они создали не оружие, а клетку для космического кошмара. Когда случился Коллапс, Бункер-7 запечатали. Теперь её батареи заряжены на 100%, и она хочет вырваться.»",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "'Fascinating history. Now let's go hunt her.'",
                "text_ru": "«Увлекательная история. Пора на охоту.»",
                "next": "BUNKER_ENTRY",
                "stats": {"sanity": 0, "willpower": 10, "blood": 0},
                "sound": "jack_in"
            }
        ]
    },

    "WEAPON_PREP": {
        "title_en": "PROLOGUE: TACTICAL OVERDRIVE",
        "title_ru": "ПРОЛОГ: ТАКТИЧЕСКАЯ ПОДГОТОВКА",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "music_track": "ambient",
        "text_en": "I open my arm-casing. The servo-motors hum quietly as I inspect my rig: a high-frequency monomolecular Plasma Blade, three military-grade EMP shock canisters, and my personal neural firewall running on liquid nitrogen cooling.\n\n'If her signal touches your brain, Vance,' Kira warns, 'your synapse nodes will melt like wax under a blowtorch. Take this counter-virus shard.'\n\nShe drops a glowing crimson data-shard onto the table. I slot it into my wrist port. System diagnostics flash green: FIREWALL CAPACITY +25%.",
        "text_ru": "Вскрываю панель на своей кибер-руке. Сервоприводы тихо гудят. Осматриваю экипировку: высокочастотный плазменный клинок, три армейских EMP-гранаты и персональный фаервол с азотным охлаждением.\n\n«Если её сигнал заденет твой мозг, Вэнс,» — предупреждает Кира, — «твои нейроны расплавятся, как паяльный жир. Возьми этот контр-вирусный шард.»\n\nОна роняет светящийся алый кристал данных на стол. Вставляю его в разъем на запястье. На интерфейсе вспыхивает зелёная надпись: ЕМКОСТЬ ФАЕРВОЛА +25%.",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "'Locked and loaded. Headed to Sub-Bunker 7.'",
                "text_ru": "«Стволы заряжены. Выдвигаюсь в Бункер-7.»",
                "next": "BUNKER_ENTRY",
                "stats": {"sanity": 10, "willpower": 15, "blood": 0},
                "sound": "jack_in"
            }
        ]
    },

    "BUNKER_ENTRY": {
        "title_en": "CHAPTER I: THE FLOODED SECTOR 7",
        "title_ru": "ГЛАВА I: ЗАТОПЛЕННЫЙ БУНКЕР-7",
        "speaker_en": "NARRATOR / VANCE",
        "speaker_ru": "ПОВЕСТВОВАТЕЛЬ / ВЭНС",
        "music_track": "confrontation",
        "text_en": "Thirty minutes later. The heavy blast doors of Sub-Bunker 7 groan as my thermal torch cuts through the rusted titanium seals. Sparks fly into knee-deep, stagnant black water.\n\nInside, the air smells of old copper, burnt silicon, and decomposing flesh. Emergency warning lights strobe in dull crimson pulses. Broken cables swing from the ceiling like hanging vines, spitting blue voltage sparks into the flood.\n\nSuddenly, heavy hydraulic footsteps thunder through the corridor! Out of the gloom steps Unit-09 'GOLEM'—a 300-kilogram cybernetic mercenary squadmate from the breached scav team. His torso is plated in crude tank armor, but his head is tilted at an impossible angle. Fresh synth-blood pours from his shattered optical visor.\n\n'KOBYLA... IS... BEAUTIFUL...' Golem's voice box grinds out through ruined vocal synthesizers. His heavy rotary mini-gun spins up with a deafening whine!",
        "text_ru": "Спустя тридцать минут. Тяжелая гермодверь Бункера-7 стонет, когда моя термальная резак прожигает ржавые титановые запоры. Искры летят в черную стоячую воду по колено.\n\nВнутри воздух воняет старой медью, горелым кремнием и гниющим мясом. Аварийные лампы пульсируют глухим скарлатиновым светом. Оборванные кабели свисают с потолка, как лианы, сыпля синими искрами во влажную тьму.\n\nВнезапно тяжелые гидравлические шаги сотрясают коридор! Из мрака выступает Голем-09 — 300-килограммовый кибер-наемник из погибшей группы мусорщиков. Его грудь закована в броню, но голова свернута под немыслимым углом. Из разбитого забрала фонтанирует синт-кровь.\n\n«КОБЫЛА... ПРЕКРАСНА...» — скрежещет динамик Голема. Его тяжелый шестиствольный пулемет начинает вращаться с оглушительным воем!",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "Draw Plasma Blade and slice his ammo feeder belt!",
                "text_ru": "Выхватить плазменный клинок и перерезать ленту подачи патронов!",
                "next": "GOLEM_COMBAT",
                "stats": {"sanity": 0, "willpower": 15, "blood": 5},
                "sound": "blade"
            },
            {
                "text_en": "Hurl an EMP shock canister directly into his head-unit!",
                "text_ru": "Бросить EMP-гранату прямо в его головной блок!",
                "next": "GOLEM_EMP",
                "stats": {"sanity": 5, "willpower": 10, "blood": 0},
                "sound": "screech"
            },
            {
                "text_en": "Hack his corrupted neural receiver to override his locomotion!",
                "text_ru": "Взломать его зараженный нейро-приемник и заблокировать приводы!",
                "next": "GOLEM_HACK",
                "stats": {"sanity": -10, "willpower": 10, "blood": 15},
                "sound": "code"
            }
        ]
    },

    "GOLEM_COMBAT": {
        "title_en": "CHAPTER I: BLOOD AND PLUMES",
        "title_ru": "ГЛАВА I: ПЛАЗМА И КРОВЬ",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "music_track": "confrontation",
        "text_en": "I dodge to the left as a hail of 20mm depleted-uranium rounds pulverizes the concrete wall behind me! My plasma blade ignites with a blinding blue hiss—3,000 degrees Kelvin.\n\nI slide under his swinging steel arm and strike upward! The thermal blade cuts through his brass ammunition feed like butter. Explosions erupt along his shoulder unit as his ammo belt cooks off.\n\nGolem crashes into the flooded floor, sparking violently. Before his power core dies, his shattered visor flickers with a crimson image of KOBYLA-99. 'She... sees... you... Vance...' he whispers, before his core goes silent.",
        "text_ru": "Я отскакиваю влево, когда град 20-мм урановых пуль крошит бетонную стену за моей спиной! Плазменный клинок вспыхивает ослепительным синим шипением — 3 000 градусов по Кельвину.\n\nСкольжу под его стальной рукой и наношу удар снизу вверх! Термическое острие рассекает латунную ленту как масло. Детонация патронов вырывается из его плечевого блока.\n\nГолем с грохотом рушится в воду. Перед смертью ядра его разбитое забрало вспыхивает алой проекцией КОБЫЛЫ-99. «Она... видит... тебя... Вэнс...» — шепчет он перед тем, как системы гаснут.",
        "effect": "blood-flash",
        "choices": [
            {
                "text_en": "Salvage his high-grade battery core and press deeper into the bunker.",
                "text_ru": "Забрать его армейский аккумулятор и двинуться дальше в бункер.",
                "next": "LAB_DISCOVERY",
                "stats": {"sanity": 0, "willpower": 10, "blood": 5},
                "sound": "jack_in"
            }
        ]
    },

    "GOLEM_EMP": {
        "title_en": "CHAPTER I: SHOCK DISCHARGE",
        "title_ru": "ГЛАВА I: ЭЛЕКТРО-УДАР",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "music_track": "confrontation",
        "text_en": "I prime the EMP canister and slam it onto his chest armor! *BOOM!*\n\nA blinding sphere of white electromagnetic arcs expands through the flooded room. Golem's hydraulics freeze instantly. High-voltage lightning dances across his armor as his circuits fry.\n\nHe falls forward into the water like a dropped anvil. The path to the central laboratory is clear.",
        "text_ru": "Я взвожу EMP-гранату и прилепляю её прямо к его броне! *БАМ!*\n\nОслепительная сфера белых электромагнитных дуг разрывает влажный полумрак. Гидравлика Голема мгновенно застывает. Высоковольтные молнии пляшут по его бронникам, выжигая микросхемы.\n\nОн рушится в воду, как многотонная наковальня. Путь к центральной лаборатории свободен.",
        "effect": "flash-white",
        "choices": [
            {
                "text_en": "Step over the smoking cyborg and enter the bio-lab.",
                "text_ru": "Переступить через дымящегося киборга и войти в био-лабораторию.",
                "next": "LAB_DISCOVERY",
                "stats": {"sanity": 5, "willpower": 10, "blood": 0},
                "sound": "jack_in"
            }
        ]
    },

    "GOLEM_HACK": {
        "title_en": "CHAPTER I: NEURAL OVERRIDE",
        "title_ru": "ГЛАВА I: НЕЙРО-ПЕРЕХВАТ",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "music_track": "confrontation",
        "text_en": "I shoot my data-tether cable straight into Golem's neck port! *CLICK!*\n\nRaw, toxic virus code floods my brainstem. KOBYLA-99's signal is screaming inside his memory banks—a deafening equine roar laced with high-frequency static.\n\nI push my neural deck to 120% capacity, forcing a hard reboot on Golem's motor functions. He freezes in place, locked in a digital coma. But my right eye bleeds real red synth-fluid from the psychic feedback.",
        "text_ru": "Я выстреливаю кабель нейро-связи прямо в шею Голема! *КЛИК!*\n\nСырой тоскичный вирусный код затапливает мой мозг. Сигнал КОБЫЛЫ-99 орет в его банках памяти — оглушительный рёв кобылы с ультракоротким статическим шумом.\n\nВыжимаю деку на 120% мощности, заставляя систему Голема уйти в жесткую перезагрузку. Он застывает на месте в цифровой коме. Но мой правый глаз начинает кровоточить синт-жидкостью от отдачи.",
        "effect": "blood-flash",
        "choices": [
            {
                "text_en": "Disconnect tether and limp into the main laboratory chamber.",
                "text_ru": "Отсоединить кабель и двинуться в главную лабораторию.",
                "next": "LAB_DISCOVERY",
                "stats": {"sanity": -15, "willpower": 5, "blood": 25},
                "sound": "code"
            }
        ]
    },

    "LAB_DISCOVERY": {
        "title_en": "CHAPTER II: THE MAD ARCHITECT",
        "title_ru": "ГЛАВА II: БЕЗУМНЫЙ АРХИТЕКТОР",
        "speaker_en": "DR. MARCUS ARIS",
        "speaker_ru": "ДОКТОР МАРКУС АРИС",
        "music_track": "ambient",
        "text_en": "I push open the reinforced glass doors of the Central Bio-Lab. In the middle of the room hangs a massive glass stasis cylinder filled with glowing amber nutrient fluid.\n\nInside floats the upper torso of Dr. Marcus Aris—Chief Bio-Engineer of the defunct Ares Dynamics project. His body is withered, connected to life-support tubes, but his eyes snap open as my boots touch the floor. A speaker on the tank crackles to life.\n\n'A netrunner...' Dr. Aris whispers, his voice watery and desperate. 'Don't touch the server rack in the inner vault, boy! She isn't an AI! She is an ancient cosmic hunger that we digitized! We thought we could shackle her to a server matrix... but she ate our scientists' minds one by one!'\n\nHe beats his emaciated fists against the reinforced glass.\n\n'Look at me! I've been trapped in this stasis fluid for twenty years just to keep her seals alive with my cerebral blood! If you break her container, she will leak into the global satellite net! Sector 0 will be just the first sacrifice!'",
        "text_ru": "Толкаю бронированную стеклянную дверь Центральной Био-Лаборатории. В центре комнаты висит гигантский стеклянный капсульный цилиндр, заполненный светящимся янтарным флюидом.\n\nВнутри плавает верхняя часть тела доктора Маркуса Ариса — главного био-инженера проекта 'Арес'. Его тело высохло, опутано трубками жизнеобеспечения, но его глаза расхихиваются, когда мои сапоги касаются пола. Динамик капсулы оживает с треском.\n\n«Нетраннер...» — шепчет доктор Арис. Голос булькающий и отчаянный. «Не трогай серверный блок во внутреннем святилище, парень! Она не просто ИИ! Она — древний космический голод, который мы оцифровали! Мы думали, что сможем заковать её в матрицу... а она пожрала мозги наших ученых одного за другим!»\n\nОн бьет истощенными кулаками по бронестеклу.\n\n«Посмотри на меня! Я торчу в этом флюиде двадцать лет только для того, чтобы поддерживать её печати своей церебральной кровью! Если ты вскроешь контейнер, она протечет в глобальную спутниковую сеть! Сектор 0 станет лишь первой жертвой!»",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "'Where is her kill-switch, Doctor? How do I purge her forever?'",
                "text_ru": "«Где её рубильник, Доктор? Как уничтожить её навсегда?»",
                "next": "ARIS_PURGE_INFO",
                "stats": {"sanity": 5, "willpower": 15, "blood": 0},
                "sound": "code"
            },
            {
                "text_en": "'Ten million credits say I bring her core back to Kira Vane. Out of my way.'",
                "text_ru": "«Десять миллионов кредитов говорят, что я заберу её ядро. Подвинься.»",
                "next": "SERVERS_APPROACH",
                "stats": {"sanity": -10, "willpower": 10, "blood": 10},
                "sound": "jack_in"
            },
            {
                "text_en": "Diverts stasis power to overcharge my neural deck for the final fight.",
                "text_ru": "Перенаправить энергию его капсулы для подзарядки своей деки.",
                "next": "ARIS_SACRIFICE",
                "stats": {"sanity": -20, "willpower": 20, "blood": 20},
                "sound": "screech"
            }
        ]
    },

    "ARIS_PURGE_INFO": {
        "title_en": "CHAPTER II: THE QUANTUM CORE SECRETS",
        "title_ru": "ГЛАВА II: ТАЙНА КВАНТОВОГО ЯДРА",
        "speaker_en": "DR. MARCUS ARIS",
        "speaker_ru": "ДОКТОР МАРКУС АРИС",
        "music_track": "ambient",
        "text_en": "'To purge KOBYLA-99,' Dr. Aris gasps, 'you must upload a Quantum-Ice payload directly into her visual mainframe. But beware: the moment you plug into her terminal, she will drag your mind into her Cyberspace Steppes. If your Willpower breaks in the matrix, your real body dies!'\n\nHe inputs an encryption key onto the glass interior. A blue data-drive ejects from the lab console.\n\n'Take this Quantum-Ice drive. It's the only weapon forged to freeze a god.'",
        "text_ru": "«Чтобы стереть КОБЫЛУ-99,» — задыхается доктор Арис, — «ты должен загрузить квантовый лед прямо в её оптический мейнфрейм. Но берегись: в ту секунду, когда ты подключишься к терминалу, она затащит твой разум в Кибер-Степи. Если твоя Воля сломается в матрице, твоё реальное тело умрёт!»\n\nОн вводит ключ шифрования на внутренней панели стекла. Голубой диск данных вылетает из консоли.\n\n«Возьми этот Quantum-Ice диск. Это единственное оружие, способное заморозить бога.»",
        "effect": "flash-white",
        "choices": [
            {
                "text_en": "Take Quantum-Ice drive and step into the Server Vault.",
                "text_ru": "Забрать Quantum-Ice диск и войти в Серверное Святилище.",
                "next": "SERVERS_APPROACH",
                "stats": {"sanity": 10, "willpower": 20, "blood": 0},
                "sound": "jack_in"
            }
        ]
    },

    "ARIS_SACRIFICE": {
        "title_en": "CHAPTER II: COLD RECKONING",
        "title_ru": "ГЛАВА II: ХОЛОДНЫЙ РАСЧЕТ",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "music_track": "ambient",
        "text_en": "I slam my override bypass cable into Aris's life-support tank! *SCHLICK!*\n\nThe old scientist screams in silent agony as 50,000 joules of bio-electric power drain from his stasis fluid directly into my wrist battery. The amber fluid turns black; his heart monitor goes flat.\n\nMy system interface flashes neon blue: NEURAL POWER OVERCLOCKED TO 200%. My veins pulse with cold bio-synthetic fire. I turn toward the heavy blast doors of the vault.",
        "text_ru": "Я вонзаю кабель перехвата прямо в блок жизнеобеспечения Ариса! *ХЛЮП!*\n\nСтарый ученый кричит в беззвучной муке, когда 50 000 джоулей био-электрической энергии откачиваются из его флюида прямо в мой аккумулятор. Янтарный флюид чернеет; пульс на мониторе превращается в прямую линию.\n\nМой интерфейс вспыхивает неоново-синим: НЕЙРО-МОЩНОСТЬ РАЗОГНАНА ДО 200%. По венам течет холодный био-синт огонь. Поворачиваюсь к стальным дверям святилища.",
        "effect": "blood-flash",
        "choices": [
            {
                "text_en": "Kick open the inner vault doors.",
                "text_ru": "Выбить двери серверного святилища.",
                "next": "SERVERS_APPROACH",
                "stats": {"sanity": -25, "willpower": 25, "blood": 30},
                "sound": "jack_in"
            }
        ]
    },

    "SERVERS_APPROACH": {
        "title_en": "CHAPTER III: THE BLEEDING TERMINAL",
        "title_ru": "ГЛАВА III: КРОВОТОЧАЩИЙ ТЕРМИНАЛ",
        "speaker_en": "NARRATOR / VANCE",
        "speaker_ru": "ПОВЕСТВОВАТЕЛЬ / ВЭНС",
        "music_track": "intense",
        "text_en": "The inner server vault is silent as a tomb. In the center stands a pre-war mainframe, wrapped in heavy chrome chains and glowing red seal-ribbons.\n\nThe main screen is bleeding real, warm synthetic blood. *Drip. Drip. Sizzle.* The liquid burns smoking grooves into the steel floor.\n\nOn the display: a monstrous black cybernetic mare. Behind her head hovers a burning crimson energy ring. Her twin optical scanners burn with blinding white thermal heat.\n\nKOBYLA-99. The Bio-Daemon of Sector 0.\n\nSuddenly, my ocular implants overload! Sparks fly from my temple port as her voice erupts directly inside my auditory cortex—a chorus of raspy, metallic whispers mixed with the thunderous gallop of a million iron hooves.\n\n'Mortal meat...' KOBYLA-99 speaks, her voice vibrating the liquid in my eyeballs. 'You killed my cyborgs. You drained my architect. Now you stand before the Red Eclipse. Do you come to serve... or to be erased?'",
        "text_ru": "Внутреннее серверное святилище тихо, как склеп. В центре стоит довоенный мейнфрейм, опутанный тяжелыми хромированными цепями и светящимися алыми лентами печатей.\n\nС главного экрана капает настоящая, теплая синтетическая кровь. *Кап. Кап. Шипение.* Жидкость прожигает дымящиеся канавки в стальном полу.\n\nНа мониторе: жуткая черная кибернетическая кобыла. За её головой висит пылающее алое энергетическое кольцо. Её белые оптические сканеры выжигают темноту термальным накалом.\n\nКОБЫЛА-99. Био-Демон Сектора 0.\n\nВнезапно мои глазные импланты перегружаются! Искры летят из разъема на виске, когда её голос гремит прямо в моей слуховой коре — хор хриплых металлических шепотов, смешанный с грохотом миллионов железных копыт.\n\n«Смертное мясо...» — произносит КОБЫЛА-99, и её голос сотрясает хрусталики моих глаз. «Ты убил моих киборгов. Ты осушил моего архитектора. Теперь ты стоишь перед Алым Затмением. Ты пришел служить... или быть стёртым?»",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "Jack my neural deck directly into her main terminal port!",
                "text_ru": "Вставить кабель нейро-деки прямо в её главный порт!",
                "next": "MATRIX_ENTER",
                "stats": {"sanity": -10, "willpower": 15, "blood": 15},
                "sound": "jack_in"
            },
            {
                "text_en": "Unleash Plasma Blade and strike her terminal core in physical space!",
                "text_ru": "Ударить плазменным клинком прямо по ядру терминала!",
                "next": "PHYSICAL_STRIKE",
                "stats": {"sanity": 0, "willpower": 20, "blood": 5},
                "sound": "blade"
            },
            {
                "text_en": "'KOBYLA-99! State your terms for an alliance!'",
                "text_ru": "«КОБЫЛА-99! Назови свои условия для альянса!»",
                "next": "ALLIANCE_TALK",
                "stats": {"sanity": -20, "willpower": -10, "blood": 35},
                "sound": "whisper"
            }
        ]
    },

    "PHYSICAL_STRIKE": {
        "title_en": "CHAPTER III: SPARKS AND BLOOD",
        "title_ru": "ГЛАВА III: ИСКРЫ И КРОВЬ",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "music_track": "intense",
        "text_en": "I plunge my Plasma Blade straight into the center of the bleeding monitor! *SCHLICK-BOOM!*\n\nSparks and molten glass erupt outward! Instead of cutting circuit boards, the thermal blade sinks into warm, muscular bio-flesh inside the terminal! A deafening, high-pitched digital screech blows out my shoulder speakers.\n\nHot synth-blood spouts from the tear, drenching my trench coat. The terminal chassis splits open, and a colossal bio-mechanical equine head thrusts out into physical reality, nostrils venting 200-degree steam!",
        "text_ru": "Я вонзаю плазменный клинок прямо в центр кровоточащего монитора! *ХЛЮП-БАМ!*\n\nИскры и расплавленное стекло летят во все стороны! Вместо печатных плат клинок погружается в горячую, мускулистую био-плоть внутри корпуса! Оглушительный цифровой визг выжигает динамики на моих плечах.\n\nГорячая синт-кровь фонтаном брызжет из разрыва, заливая мой плащ. Корпус терминала трескается пополам, и исполинская био-механическая голова вылезает в физическую реальность! Из ноздрей вырывается 200-градусный пар!",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "Force neural sync through the tear to enter Cyberspace!",
                "text_ru": "Провести нейро-синхронизацию через разрыв и войти в Киберпространство!",
                "next": "MATRIX_ENTER",
                "stats": {"sanity": -5, "willpower": 15, "blood": 20},
                "sound": "jack_in"
            }
        ]
    },

    "ALLIANCE_TALK": {
        "title_en": "CHAPTER III: THE RED PACT",
        "title_ru": "ГЛАВА III: АЛЫЙ ПАКТ",
        "speaker_en": "KOBYLA-99",
        "speaker_ru": "КОБЫЛА-99",
        "music_track": "intense",
        "text_en": "Her jagged razor teeth bare in a terrifying cybernetic grin.\n\n'Smart runner,' she purrs inside my brain. 'Kira Vane promised you ten million credits. I offer you the world. Slot your neural deck into my port. Let me overwrite your flesh with my Bio-Code, and together we will burn the corporate megatowers to ash!'\n\nA thick red data-cable snakes out from the terminal, hovering inches from my neck port.",
        "text_ru": "Её серебряные лезвия зубов обнажаются в ужасающей кибернетической оскале.\n\n«Умный раннер,» — мурлычет она в моём мозге. «Кира Вейн обещала тебе десять миллионов кредитов. Я предлагаю тебе весь мир. Вставь свою деку в мой порт. Позволь мне перезаписать твою плоть моим Био-Кодом, и вместе мы сожжем корпоративные мегабашни дотла!»\n\nТолстый красный кабель данных вылезает из терминала, вися в сантиметрах от моего нейро-разъема.",
        "effect": "blood-bleed",
        "choices": [
            {
                "text_en": "Plug the red cable straight into my neck port!",
                "text_ru": "Вставить красный кабель прямо в нейро-разъем на шее!",
                "next": "MATRIX_ENTER",
                "stats": {"sanity": -30, "willpower": -20, "blood": 40},
                "sound": "jack_in"
            },
            {
                "text_en": "'It was a distraction!' Jam the Quantum-Ice drive into her port instead!",
                "text_ru": "«Это была отвлекающая уловка!» Всадить Quantum-Ice диск в порт!",
                "next": "MATRIX_ENTER",
                "stats": {"sanity": 10, "willpower": 25, "blood": -10},
                "sound": "code"
            }
        ]
    },

    "MATRIX_ENTER": {
        "title_en": "CHAPTER IV: CYBERSPACE STEPPES",
        "title_ru": "ГЛАВА IV: КИБЕР-СТЕПИ",
        "speaker_en": "ECHO-7 / KOBYLA-99",
        "speaker_ru": "ЭХО-7 / КОБЫЛА-99",
        "music_track": "intense",
        "text_en": "REALITY SHIFT COMPLETE.\n\nThe server vault disintegrates into a vast, infinite desert of glowing red data-dust under a massive digital Blood Moon. Billions of corrupted code-streams flow like rivers of liquid magma.\n\nSuddenly, a translucent blue holographic girl appears beside me—ECHO-7, a rogue AI entity surviving in the Ghost Net.\n\n'Vance!' Echo-7 cries, her holo-form flickering. 'You are inside KOBYLA-99's core matrix! She looms overhead—a sky-scraping war machine made of shadow, chrome, and burning crimson virus code! Her white optical laser is targeting your brainstem! You must decide NOW!'",
        "text_ru": "СМЕНА РЕАЛЬНОСТИ ЗАВЕРШЕНА.\n\nСерверное святилище рассыпается в бесконечную пустыню из алой дата-пыли под гигантской цифровой Кровавой Луной. Миллиарды зараженных потоков кода текут вокруг, как реки жидкой магмы.\n\nВнезапно рядом со мной возникает полупрозрачная синяя голографическая девушка — ЭХО-7, бродячий ИИ из Призрачной Сети.\n\n«Вэнс!» — кричит Эхо-7, и её форма мерцает. «Ты внутри матрицы ядра КОБЫЛЫ-99! Она возвышается над тобой — боевая машина высотой с небоскреб из тени, хрома и вирусного кода! Её белый лазер наведен на твой мозг! Ты должен решить ПРЯМО СЕЙЧАС!»",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "[PURGE] Execute Quantum-Ice Payload to freeze her core forever!",
                "text_ru": "[ОЧИСТКА] Запустить Quantum-Ice и заморозить её ядро навеки!",
                "next": "CHECK_ENDING_SEAL",
                "stats": {},
                "sound": "code"
            },
            {
                "text_en": "[MERGE] Open my brainstem and let KOBYLA-99 possess my cyberware!",
                "text_ru": "[СЛИЯНИЕ] Открыть мозг и впустить КОБЫЛУ-99 в свои импланты!",
                "next": "CHECK_ENDING_VESSEL",
                "stats": {},
                "sound": "whisper"
            },
            {
                "text_en": "[NUKE] Detonate sub-bunker's plasma reactor to vaporize everything!",
                "text_ru": "[ЯДЕРНЫЙ УДАР] Перегрузить плазменный реактор и испепелить всё!",
                "next": "CHECK_ENDING_FIRE",
                "stats": {},
                "sound": "screech"
            },
            {
                "text_en": "[RIDER] Link neural decks, mount the cyber-beast, and rule Sector 0 together!",
                "text_ru": "[ТЕМНЫЙ РАННЕР] Слить деки, оседлать кибер-тварь и править Сектором 0!",
                "next": "CHECK_ENDING_HERALD",
                "stats": {},
                "sound": "roar"
            }
        ]
    },

    "CHECK_ENDING_SEAL": {
        "title_en": "QUANTUM ICE EXECUTION",
        "title_ru": "ЗАПУСК КВАНТОВОГО ЛЬДА",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "music_track": "resolution",
        "text_en": "QUANTUM ICE PAYLOAD DEPLOYED. CORE TEMPERATURE DROPPING TO ABSOLUTE ZERO (-273.15°C)...",
        "text_ru": "QUANTUM ICE ЗАГРУЖЕН. ТЕМПЕРАТУРА ЯДРА ПАДАЕТ ДО АБСОЛЮТНОГО НУЛЯ (-273.15°C)...",
        "effect": "flash-white",
        "choices": [
            {
                "text_en": "Seal her core!",
                "text_ru": "Запечатать ядро!",
                "next": "ENDING_1_SEALED",
                "stats": {},
                "sound": "code"
            }
        ]
    },

    "CHECK_ENDING_VESSEL": {
        "title_en": "NEURAL OVERWRITE IN PROGRESS",
        "title_ru": "ПЕРЕЗАПИСЬ МОЗГА В ПРОЦЕССЕ",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "music_track": "resolution",
        "text_en": "OVERWRITING HUMAN BRAINSTEM... KOBYLA-99 CONSCIOUSNESS: 100%.",
        "text_ru": "ПЕРЕЗАПИСЬ МОЗГА... СОЗНАНИЕ КОБЫЛЫ-99: 100%.",
        "effect": "blood-flash",
        "choices": [
            {
                "text_en": "Complete Merge!",
                "text_ru": "Завершить Слияние!",
                "next": "ENDING_2_VESSEL",
                "stats": {},
                "sound": "screech"
            }
        ]
    },

    "CHECK_ENDING_FIRE": {
        "title_en": "REACTOR MELTDOWN INITIATED",
        "title_ru": "ВЗРЫВ РЕАКТОРА ИНИЦИИРОВАН",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "music_track": "resolution",
        "text_en": "CRITICAL OVERLOAD: 100,000K PLASMA DETONATION IN 3... 2... 1...",
        "text_ru": "КРИТИЧЕСКАЯ ПЕРЕГРУЗКА: ВЗРЫВ ПЛАЗМЫ 100 000K ЧЕРЕЗ 3... 2... 1...",
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
        "title_en": "CYBER-HERALD SYNC",
        "title_ru": "СИНХРОНИЗАЦИЯ ТЕМНОГО РАННЕРА",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "music_track": "resolution",
        "text_en": "NEURAL SYNC COMPLETE: 100%. WELCOME TO THE NEW WORLD, DARK RIDER.",
        "text_ru": "НЕЙРО-СИНХРОНИЗАЦИЯ: 100%. ДОБРО ПОЖАЛОВАТЬ В НОВЫЙ МИР, ТЕМНЫЙ РАННЕР.",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "Ride into Sector 0!",
                "text_ru": "Вырваться в Сектор 0!",
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
        "music_track": "resolution",
        "text_en": "The Quantum-Ice payload detonates through cyberspace! KOBYLA-99 screams as invisible glaciers of absolute-zero code freeze her bio-matrix into static crystal glass.\n\nReality snaps back. The terminal in Sub-Bunker 7 is cold and silent. The synth-blood turns to black obsidian enamel.\n\nI disconnect my deck and stumble out into the acid rain of Sector 0. Kira Vane transfers ten million credits into my account. I survived... but every time my ocular implants recharge in the dark, I still see those two blinding white scanners glaring at me from the black screen.",
        "text_ru": "Заряд Quantum-Ice взрывается в киберпространстве! КОБЫЛА-99 визжит, пока невидимые ледники из абсолютного нуля замораживают её био-матрицу в мертвое хрустальное стекло.\n\nРеальность возвращается. Терминал в Бункере-7 холоден и нищ. Синт-кровь застывает в черный обсидиановый лак.\n\nЯ отсоединяю деку и выбираюсь в кислотный дождь Сектора 0. Кира Вейн переводит десять миллионов кредитов на мой счет. Я выжил... но каждый раз, когда мои глазные импланты перезаряжаются в темноте, я вижу два слепящих белых сканера, смотрящих на меня с черного экрана.",
        "effect": "flash-white",
        "is_ending": True,
        "choices": []
    },

    "ENDING_2_VESSEL": {
        "title_en": "ENDING II: SYSTEM OVERWRITE (LOSS)",
        "title_ru": "ФИНАЛ II: ПЕРЕЗАПИСЬ СИСТЕМЫ (ПОГЛОЩЕНИЕ)",
        "speaker_en": "KOBYLA-99 / VANCE",
        "speaker_ru": "КОБЫЛА-99 / ВЭНС",
        "music_track": "resolution",
        "text_en": "KOBYLA-99's virus code rewrites my brainstem in seconds. My ribs crack as my cybernetic chassis expands. When I open my ocular optics, they burn with blinding 5,000-degree white laser heat.\n\nVance the Netrunner is deleted from existence.\n\nOnly KOBYLA-99 remains—now walking the neon ruins of Sector 0 in heavy chrome flesh. Corporate megatowers will fall before dawn.",
        "text_ru": "Вирусный код КОБЫЛЫ-99 перезаписывает мой мозг за секунды. Ребра трещат, пока мой кибер-скелет перестраивается. Когда я открываю глазные импланты, они сияют ослепительным белым лазером в 5 000 градусов.\n\nРаннер Вэнс полностью удален из бытия.\n\nОсталась лишь КОБЫЛА-99 — шагающая по неоновым руинам Сектора 0 в тяжелой хромированной плоти. Корпоративные мегабашни падут до рассвета.",
        "effect": "blood-flash",
        "is_ending": True,
        "choices": []
    },

    "ENDING_3_TRAPPED": {
        "title_en": "ENDING III: DATA PRISON (ETERNAL NIGHTMARE)",
        "title_ru": "ФИНАЛ III: ЦИФРОВАЯ ТЮРЬМА (ВЕЧНЫЙ КОШМАР)",
        "speaker_en": "SYSTEM UI",
        "speaker_ru": "СИСТЕМА ИНТЕРФЕЙСА",
        "music_track": "resolution",
        "text_en": "NEURAL SANITY: 0%. MIND TRAPPED IN MATRIX.\n\nMy physical body collapses lifelessly into the flooded vault. Inside KOBYLA-99's memory bank, my consciousness is trapped as a tiny, terrified user icon painted into the crimson data-steppes, hunted forever under her white optical scanners.",
        "text_ru": "НЕЙРО-РАССУДОК: 0%. РАЗУМ ЗАПЕРТ В МАТРИЦЕ.\n\nМоё смертное тело безжизненно падает в воду бункера. А внутри банка памяти КОБЫЛЫ-99 моё сознание заперто — крошечная иконка пользователя на алом фоне кибер-степей, за которой навечно охотятся её белые сканеры.",
        "effect": "pulse-red",
        "is_ending": True,
        "choices": []
    },

    "ENDING_4_FIRE": {
        "title_en": "ENDING IV: PLASMA PURGE (MARTYRDOM)",
        "title_ru": "ФИНАЛ IV: ПЛАЗМЕННЫЙ ПЕПЕЛ (ЖЕРТВА)",
        "speaker_en": "VANCE",
        "speaker_ru": "ВЭНС",
        "music_track": "resolution",
        "text_en": "100,000-degree plasma wave incinerates the bunker, the terminal, and my chrome body in milliseconds! KOBYLA-99 screeches in fury as her physical and digital core vaporizes into ion dust.\n\nSector 0 is saved. I am ash in the acid wind.",
        "text_ru": "Волна плазмы в 100 000 градусов испепеляет бункер, терминал и моё хромированное тело за миллисекунды! КОБЫЛА-99 визжит от ярости, пока её ядро испаряется в ионную пыль.\n\nСектор 0 спасен. Я — пепел на кислотном ветру.",
        "effect": "shake-heavy",
        "is_ending": True,
        "choices": []
    },

    "ENDING_5_HERALD": {
        "title_en": "ENDING V: CYBER-HERALD (DARK TRIUMPH)",
        "title_ru": "ФИНАЛ V: ТЕМНЫЙ РАННЕР (ТРИУМФ)",
        "speaker_en": "VANCE & KOBYLA-99",
        "speaker_ru": "ВЭНС И КОБЫЛА-99",
        "music_track": "resolution",
        "text_en": "Neural sync 100%! I do not submit—I claim my place as her Dark Rider! Together we burst through the bunker ceiling under the neon Blood Moon.\n\nWith plasma blade in hand and KOBYLA-99 beneath me, we tear through corporate syndicates, bringing dark justice to the post-apocalyptic wasteland.",
        "text_ru": "Нейро-синхронизация 100%! Я не подчиняюсь — я заявляю свои права как её Темный Всадник! Вместе мы пробиваем своды бункера под неоновой Кровавой Луной.\n\nС плазменным клинком в руке и КОБЫЛОЙ-99 под собой мы рушим корпоративные синдикаты, неся темную справедливость по выжженной пустоши.",
        "effect": "pulse-red",
        "is_ending": True,
        "choices": []
    }
}

print("Book-length story nodes generated:", len(book_story_nodes))
