import json, base64

# Load image in base64
image_path = "/home/user/uploads/111.png"
with open(image_path, "rb") as img_file:
    img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
img_data_url = f"data:image/png;base64,{img_b64}"

story_nodes = {
    "START": {
        "title_en": "Prologue: The Sunken Vault",
        "title_ru": "Пролог: Затопленный Склеп",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "The air in the subterranean crypt beneath St. Vlas Monastery is suffocatingly thick with the stink of damp mold, centuries of sealed dust, and cold iron. Rain thunders against the mud outside, sending streams of dark water dripping through the groined vault ceiling.\n\nYou are Dr. Elijah Vance—scholar, exorcist, and antiquarian. Seven long years you have spent hunting the terrifying legend of 'Kobyla' (The Mare), an ancient cosmic entity of nightmare, pestilence, and blood-frenzy trapped within a cursed canvas painted in 1384 by Brother Vlas before he went mad.\n\nNow, standing on the mossy flagstones with flickering torchlight in hand, you behold it. Upon a heavy iron easel rests the framed painting: a terrifying black equine silhouette with a wild crimson mane, framed by a burning blood-red orb. Her eyes are two hollow voids of blinding, pure white fire that seem to stare directly into your mortal soul.",
        "text_ru": "Воздух в подземном склепе под монастырём Святого Власа удушливо густ. Он пропитан запахом сырой плесени, многовековой пыли и холодного железа. Снаружи бушует гроза, и темные ручьи стекают по сводам готического потолка.\n\nВы — доктор Илья Вэнс, учёный-экзорцист и антиквар. Семь долгих лет вы выслеживали жуткую легенду о «Кобыле» — древнем космическом сущности-кошмаре, несущей мор, кровь и безумие. Она была заточена на проклятом холсте, написанном в 1384 году безумным монахом Власом перед тем, как тот выколол себе глаза.\n\nИ вот, стоя на мшистых плитах с факелом в руке, вы видите её. На тяжелом железном мольберте покоится картина: жуткий силуэт черной кобылы с дикой алой гривой на фоне пылающего кроваво-красного диска. Её глаза — два слепящих омута чистого белого огня, которые будто смотрят в самую глубину вашей смертной души.",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "Approach the easel and examine the oil pigments up close.",
                "text_ru": "Подойти к мольберту и изучить масляные пигменты вблизи.",
                "next": "EXAMINE_CANVAS",
                "stats": {"sanity": -5, "willpower": 5, "blood": 0},
                "sound": "whisper"
            },
            {
                "text_en": "Unroll the ancient parchment and begin reciting the Holy Sealing Incantation.",
                "text_ru": "Развернуть древний пергамент и начать читать Священное Заклятие Заточения.",
                "next": "READ_PRAYER",
                "stats": {"sanity": 0, "willpower": 10, "blood": 0},
                "sound": "chant"
            },
            {
                "text_en": "Draw your consecrated obsidian dagger and take a defensive stance.",
                "text_ru": "Обнажить освященный обсидиановый клинок и встать в защитную стойку.",
                "next": "DRAW_DAGGER",
                "stats": {"sanity": 5, "willpower": 5, "blood": 5},
                "sound": "blade"
            }
        ]
    },
    
    "EXAMINE_CANVAS": {
        "title_en": "The Bleeding Oil",
        "title_ru": "Кровоточащее Масло",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "You step forward, your boots squelching in the shallow muddy water. As your torchlight draws near the canvas, the red circle behind the black mare begins to pulse with a low, rhythmic throb—like a severed giant heart beating under water.\n\nSuddenly, the thick oil paint along her mane liquifies! Warm, visceral blood, heavy with the stench of copper and burnt ozone, oozes from the canvas frame and drips onto the altar below. *Drip. Drip. Sizzle.* The blood burns smoke into the cold stones.\n\nThe white eyes on the painting dilate. A whisper—raspy, feminine, and echoing with the screams of a thousand dying horses—resonates inside your ribcage.",
        "text_ru": "Вы делаете шаг вперед, и ваши сапоги хлюпают по мелководью. Как только свет факела приближается к холсту, алый диск за черной кобылой начинает пульсировать с низким, ритмичным глухим звуком — словно отсеченное сердце гиганта, бьющееся под водой.\n\nВнезапно густая масляная краска вдоль её гривы сжижается! Тёплая, вязкая кровь с тяжелым запахом меди и жжёного озона сочится из деревянной рамы и капает на алтарь. *Кап. Кап. Шипение.* Кровь дымится на холодном камне.\n\nБелые глаза на картине расширяются. Шёпот — хриплый, женский, отзывающийся эхом тысяч гибущих коней — раздаётся прямо внутри вашей грудной клетки.",
        "effect": "blood-bleed",
        "choices": [
            {
                "text_en": "Reach out and touch the dripping crimson blood with your bare fingers.",
                "text_ru": "Протянуть руку и прикоснуться к стекающей алой крови голыми пальцами.",
                "next": "TOUCH_BLOOD",
                "stats": {"sanity": -10, "willpower": -5, "blood": 25},
                "sound": "screech"
            },
            {
                "text_en": "Step back immediately and raise your holy lantern high.",
                "text_ru": "Немедленно отступить и высоко поднять святой фонарь.",
                "next": "AWAKENING",
                "stats": {"sanity": 10, "willpower": 10, "blood": 0},
                "sound": "heartbeat"
            },
            {
                "text_en": "Address the canvas directly: 'Kobyla! I know your true name!'",
                "text_ru": "Обратиться к холсту напрямую: «Кобыла! Я знаю твоё истинное имя!»",
                "next": "CHALLENGE_NAME",
                "stats": {"sanity": -5, "willpower": 15, "blood": 5},
                "sound": "roar"
            }
        ]
    },

    "READ_PRAYER": {
        "title_en": "The Shattered Incantation",
        "title_ru": "Разрушенное Заклятие",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "You unroll the yellowed lambskin parchment and raise your voice: 'In nomine Sancti Vlasii, principis exorcistarum, retro ire Spiritus Immundus...'\n\nBefore you can finish the second verse, a sound like a cracking skull explodes in the room! The Latin words on your parchment char into black ash. The burning paper drops from your numb fingers.\n\nFrom inside the canvas, the Mare's jaws part slightly. Rows of razor-sharp, needle-like silver teeth gleam in the dark. A deep, mocking laughter vibrates through the soles of your feet.",
        "text_ru": "Вы разворачиваете пожелтевший пергамент и громко произносите: «In nomine Sancti Vlasii, principis exorcistarum, retro ire Spiritus Immundus...»\n\nНе успеваете вы дочитать вторую строчку, как в склепе раздается звук, подобный раскалывающемуся черепу! Латинские буквы на пергаменте обугливаются и превращаются в черный пепел. Горящая бумага выпадает из ваших онемевших пальцев.\n\nИз глубины холста пасть Кобылы слегка приоткрывается. Ряды острейших серебряных зубов блестят во мраке. Низкий, глумливый хохот сотрясает плиты под вашими ногами.",
        "effect": "flash-white",
        "choices": [
            {
                "text_en": "Persist with sheer willpower, finishing the prayer from memory!",
                "text_ru": "Продолжать на одной лишь силе воли, читая молитву по памяти!",
                "next": "AWAKENING",
                "stats": {"sanity": -15, "willpower": 25, "blood": 0},
                "sound": "chant"
            },
            {
                "text_en": "Grasp your silver crucifix and press it against the wet frame!",
                "text_ru": "Схватить серебряный крест и прижать его к мокрому холсту!",
                "next": "AWAKENING",
                "stats": {"sanity": 5, "willpower": 10, "blood": 5},
                "sound": "blade"
            }
        ]
    },

    "DRAW_DAGGER": {
        "title_en": "Steel and Shadow",
        "title_ru": "Сталь и Тень",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "The obsidian dagger hums with intense cold in your hand. Engraved rune grooves along the spine glow with pale violet light. You drop into a low combat stance, keeping the blade pointed at the creature's glowing throat.\n\n'Come forth then, demon!' you call out. 'My blade was forged in mountain silver and quenched in holy oil!'\n\nThe painted silhouette in the red circle does not recoil. Instead, her ears flatten against her head. A heavy, viscous mist—smelling of blood, rotting straw, and sulfur—pours out of the frame like water overflowing a dam.",
        "text_ru": "Обсидиановый клинок гудит от лютого холода в вашей руке. Рунические желоба вдоль обуха вспыхивают бледным фиолетовым светом. Вы опускаетесь в боевую стойку, направляя острие прямо в светящееся горло твари.\n\n«Выходи же, демон!» — восклицаете вы. «Мой клинок выкован из горного серебра и закалён в святом елее!»\n\nНарисованный силуэт в алом круге не отступает. Напротив, её уши прижимаются к голове. Густой, вязкий туман с запахом крови, гнилой соломы и серы хлынул из рамы, словно вода из прорванной плотины.",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "Lunge forward and strike the obsidian knife into the canvas heart!",
                "text_ru": "Ринуться вперед и вонзить обсидиановый нож в сердце холста!",
                "next": "STAB_ATTEMPT",
                "stats": {"sanity": -10, "willpower": 15, "blood": 15},
                "sound": "blade"
            },
            {
                "text_en": "Slice your own left palm and coat the blade with your blood as a ward.",
                "text_ru": "Надрезать левую ладонь и окропить клинок своей кровью для защиты.",
                "next": "TOUCH_BLOOD",
                "stats": {"sanity": -5, "willpower": 10, "blood": 30},
                "sound": "whisper"
            }
        ]
    },

    "TOUCH_BLOOD": {
        "title_en": "The Blood Mark",
        "title_ru": "Кровавая Метка",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "The moment your fingers touch the hot vermilion paint, a agonizing shock of psychic lightning shoots up your arm! You fall to one knee, gasping for breath. The crimson pigment burrows into your pores, staining the skin of your hand a permanent demonic crimson.\n\nInside your vision, the crypt fades for a fraction of a second. You see endless fields of burning red grass under a dead black sun. Millions of skeletal horses gallop across a horizon made of ash.\n\n*'You have marked yourself, Elijah...'* Kobyla's voice caresses your brain. *'You are mine now.'*",
        "text_ru": "В ту же секунду, как ваши пальцы касаются горячей киновари, жгучий разряд психической молнии пронзает вашу руку! Вы падаете на одно колено, хватая воздух ртом. Алый пигмент въедается в поры, окрашивая кожу вашей кисти в не смываемый багровый цвет.\n\nНа долю секунды склеп исчезает из глаз. Вы видите бесконечные поля горящей красной травы под мертвым черным солнцем. Миллионы скелетов коней несутся по горизонту из пепла.\n\n*«Ты сам отдал себя мне, Илья...»* — шёпот Кобылы ласкает ваш мозг. *«Теперь ты отмечен.»*",
        "effect": "blood-flash",
        "choices": [
            {
                "text_en": "Clench your bloodied fist and stand tall! 'My soul belongs to no beast!'",
                "text_ru": "Сжать окровавленный кулак и встать во весь рост! «Моя душа не принадлежит твари!»",
                "next": "AWAKENING",
                "stats": {"sanity": 10, "willpower": 20, "blood": 10},
                "sound": "roar"
            },
            {
                "text_en": "Inhale the crimson fumes, succumbing to the dark euphoria.",
                "text_ru": "Вдохнуть алый пар, поддаваясь темной эйфории.",
                "next": "AWAKENING",
                "stats": {"sanity": -25, "willpower": -10, "blood": 35},
                "sound": "whisper"
            }
        ]
    },

    "CHALLENGE_NAME": {
        "title_en": "Invocation of the Beast",
        "title_ru": "Оклик Демона",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "Your words shatter the eerie silence of the crypt like thunder. 'I call thee Kobyla! Mare of the Seven Plagues! Red Nightmare of the Sunken Steppes!'\n\nThe canvas frame groans under tremendous physical pressure. The wooden joints split with sharp cracks. The crimson circle behind the mare blazes so brightly that shadows in the room bend backward.\n\nSlowly, deliberate as a descending mountain, the dark painted head begins to push outwards through the stretched fabric, swelling into physical dimension!",
        "text_ru": "Ваши слова раскатываются по склепу, словно гром. «Я призываю тебя, Кобыла! Мать Семи Моров! Алый Кошмар Затонувших Степей!»\n\nДеревянная рама стонет под страшным давлением. Стыки трескаются. Алый диск за кобылой вспыхивает настолько ярко, что тени в комнате изгибаются в обратную сторону.\n\nМедленно, с неотвратимостью сходящей лавины, черная нарисованная голова начинает вылезать сквозь натянутый холст, обретая плоть и объём в нашем мире!",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "Brace yourself for her full physical arrival!",
                "text_ru": "Приготовиться к её полному явлению в наш мир!",
                "next": "AWAKENING",
                "stats": {"sanity": 0, "willpower": 15, "blood": 5},
                "sound": "roar"
            }
        ]
    },

    "STAB_ATTEMPT": {
        "title_en": "The Ruptured Canvas",
        "title_ru": "Пробитый Холст",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "You drive the obsidian dagger forward with all your strength! The tip pierces the canvas right in the center of the crimson circle. *SCHLICK!*\n\nInstead of tearing dry cloth, the blade sinks into warm, muscular flesh! A high-pitched, deafening equine shriek erupts from the canvas, blowing out the flame of your torch and instantly shattering every glass bottle on your alchemy belt!\n\nHot crimson gore spouts from the tear, drenching your clothes. The canvas canvas dissolves completely into a vortex of blood and black fire!",
        "text_ru": "Вы с силой вонзаете обсидиановый нож! Острие пробивает холст прямо в центре алого диска. *ХЛЮП!*\n\nВместо сухой ткани клинок погружается в горячую, мускулистую плоть! Оглушительный, потусторонний визг кобылы вырывается из картины. Он мгновенно гасит факел и разбивает все стеклянные склянки на вашем поясе!\n\nГорячая багровая кровь фонтаном брызжет из разрыва, заливая вашу одежду. Сам холст растворяется в вихре крови и черного огня!",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "Stand your ground in the darkness and hold fast to your dagger!",
                "text_ru": "Удержать равновесие во тьме и крепче сжать клинок!",
                "next": "AWAKENING",
                "stats": {"sanity": -5, "willpower": 15, "blood": 20},
                "sound": "screech"
            }
        ]
    },

    "AWAKENING": {
        "title_en": "Chapter I: Kobyla Steps Forth",
        "title_ru": "Глава I: Пробуждение Кобылы",
        "speaker_en": "Kobyla",
        "speaker_ru": "Кобыла",
        "text_en": "The canvas is gone. In its place stands the nightmare manifested.\n\nA colossal, pitch-black equine torso emerges into the crypt. Her coat is dark as dried blood and cracked velvet; her mane billows in an invisible gale of crimson flames. Behind her head, a ring of pure red light hovers like a desecrated halo. Her twin eyes shine with blinding, piercing white luminance, leaving no room for human doubt.\n\nShe lowers her massive head until her wet black nostrils are inches from your face. Steam smelling of ancient ash and metal vents onto your throat.\n\n'Mortal clay...' her voice booms inside your mind like ringing iron. 'Seven hundred winters I slept in ink and grease. Did you come to worship me... or to be devoured?'",
        "text_ru": "Холста больше нет. На его месте предстает воплощенный кошмар.\n\nИсполинское черное тело кобылы выступает из мрака. Её шерсть темна, как засохшая кровь и потрескавшийся бархат; грива развевается на невидимом ветру алого пламени. За её головой висит кольцо чистого красного света, подобно оскверненному нимбу. Её глаза сияют ослепительным, испепеляющим белым светом.\n\nОна опускает свою огромную голову, пока её влажные черные ноздри не оказываются в сантиметрах от вашего лица. Пар с запахом древнего пепла и раскаленного металла обжигает вам шею.\n\n«Смертная глина...» — её голос гремит в вашей голове, как удары молота по наковальне. «Семьсот зим я спала в чернилах и жире. Ты пришел поклониться мне... или быть сожранным?»",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "'I am Elijah of the Sacred Order! By the light of truth, I demand you yield!'",
                "text_ru": "«Я Илья из Священного Ордена! Именем истины я требую от тебя смирения!»",
                "next": "CONFRONTATION_STRENGTH",
                "stats": {"sanity": 5, "willpower": 20, "blood": -5},
                "sound": "roar"
            },
            {
                "text_en": "'What are you? Why do you hungering for human souls?'",
                "text_ru": "«Что ты такое? Почему ты жаждешь человеческих душ?»",
                "next": "CONFRONTATION_LORE",
                "stats": {"sanity": -10, "willpower": 5, "blood": 5},
                "sound": "whisper"
            },
            {
                "text_en": "'I brought you blood, Ancient One... Teach me the secrets of immortality!'",
                "text_ru": "«Я принес тебе кровь, Древняя... Научи меня тайнам бессмертия!»",
                "next": "CONFRONTATION_BARGAIN",
                "stats": {"sanity": -20, "willpower": -10, "blood": 30},
                "sound": "whisper"
            }
        ]
    },

    "CONFRONTATION_STRENGTH": {
        "title_en": "Unbroken Will",
        "title_ru": "Непреклонная Воля",
        "speaker_en": "Kobyla",
        "speaker_ru": "Кобыла",
        "text_en": "Kobyla rears back, her massive hooves crashing down onto the stone floor, splintering the granite flags like glass! Red sparks fly in every direction.\n\n'Foolish priest!' she shrieks, a pitch so high it vibrates the blood inside your veins. 'Your 'Order' built their foundations on my bones! Your saints drew their chants from my dreams! You cannot chain a storm with thread!'\n\nShe leans closer, opening her jaws wide. Inside her mouth is not a throat, but a swirling galaxy of burning crimson stars.",
        "text_ru": "Кобыла взвивается на дыбы! Её тяжелые копыта с грохотом обрушиваются на каменный пол, расщепляя гранитные плиты, словно хрупкое стекло! Во все стороны летят красные искры.\n\n«Глупый священник!» — визжит она на частоте, от которой закипает кровь в жилах. «Твой 'Орден' построил свои храмы на моих костях! Ваши святые черпали молитвы из моих снов! Нельзя удержать бурю ниткой!»\n\nОна наклоняется ближе, распахнув пасть. Внутри неё — не горло, а вихрящаяся галактика пылающих алых звезд.",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "Stand tall and channel your inner spiritual flame directly into her white eyes!",
                "text_ru": "Встать во весь рост и направить духовный свет прямо в её белые глаза!",
                "next": "REALM_TRANSITION",
                "stats": {"sanity": 10, "willpower": 25, "blood": -10},
                "sound": "chant"
            },
            {
                "text_en": "Slash at her throat with your weapon, refusing to back down!",
                "text_ru": "Рассечь её горло оружием, отказываясь отступать!",
                "next": "REALM_TRANSITION",
                "stats": {"sanity": -5, "willpower": 15, "blood": 10},
                "sound": "blade"
            }
        ]
    },

    "CONFRONTATION_LORE": {
        "title_en": "Eldritch Origin",
        "title_ru": "Древнее Происхождение",
        "speaker_en": "Kobyla",
        "speaker_ru": "Кобыла",
        "text_en": "A sinister, guttural hum ripples from her throat. Her white eyes dim slightly, swirling like pearlescent clouds of death.\n\n'Hunger?' she speaks, her tone strangely solemn now. 'I do not hunger as beasts hunger. I am the Dread Maiden of the Eclipse. When mortal kingdoms rot under their own sin, I am born from their fear. Brother Vlas thought he could capture me on a square of cloth. He painted my mane with his brother's blood and my eyes with crushed moonlight.'\n\nShe steps closer, her heat radiating like a furnace. 'He thought he was saving his village... yet all he did was build me a throne of silk and frame.'",
        "text_ru": "Зловещий гул вырывается из её груди. Белые глаза немного тускнеют, превращаясь в перламутровые облака смерти.\n\n«Голод?» — говорит она, и её тон становится жутко торжественным. «Я не голодаю так, как зверье. Я — Дева Алого Затмения. Когда смертные королевства гниют в грехах, я рождаюсь из их страха. Брат Влас думал, что сможет удержать меня на куске холста. Он писал мою гриву кровью брата, а глаза — толченым лунным светом.»\n\nОна делает шаг вперед, излучая жар, как доменная печь. «Он думал, что спасает деревню... а создал для меня трон из шелка и дерева.»",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "'Brother Vlas was a fool. But I am your judge!'",
                "text_ru": "«Брат Влас был безумцем. Но я — твой судья!»",
                "next": "REALM_TRANSITION",
                "stats": {"sanity": 5, "willpower": 15, "blood": 0},
                "sound": "roar"
            },
            {
                "text_en": "'Show me the world as you see it, Kobyla...'",
                "text_ru": "«Покажи мне мир таким, каким его видишь ты, Кобыла...»",
                "next": "REALM_TRANSITION",
                "stats": {"sanity": -20, "willpower": -5, "blood": 20},
                "sound": "whisper"
            }
        ]
    },

    "CONFRONTATION_BARGAIN": {
        "title_en": "The Seduction of Blood",
        "title_ru": "Соблазн Крови",
        "speaker_en": "Kobyla",
        "speaker_ru": "Кобыла",
        "text_en": "Her jagged silver teeth bare in a horrifying equine smile. A jet of hot steam bursts from her nostrils.\n\n'Ah... a scholar with appetite!' she croons inside your head. 'Your holy brothers lied to you, Elijah. They preached poverty and mortality while drinking fine wines in stone castles. Join me! Give me your blood, and I will make you the Nightmare King of this dying world. Kings will kneel before the shadow of our hooves!'\n\nShe lowers her muzzle. Her long, black tongue licks the air, tasting the scent of your adrenaline and blood.",
        "text_ru": "Её серебряные зубы обнажаются в ужасающей лошадиной оскале. Из ноздрей вырывается струя горячего пара.\n\n«А-а... учёный с аппетитом!» — мурлычет она в вашей голове. «Твои святые братья лгали тебе, Илья. Они проповедовали бедность, попивая винные соки в каменных замках. Присоединяйся! Отдай мне свою кровь, и я сделаю тебя Повелителем Кошмаров этого умирающего мира. Короли склонятся перед тенью наших копыт!»\n\nОна опускает морду. Её длинный черный язык слизывает воздух, улавливая запах вашего адреналина и крови.",
        "effect": "blood-bleed",
        "choices": [
            {
                "text_en": "Kneel down and press your hand into her mane: 'I yield my mortal destiny to you!'",
                "text_ru": "Встать на колени и запустить руку в её гриву: «Я отдаю тебе свою смертную судьбу!»",
                "next": "REALM_TRANSITION",
                "stats": {"sanity": -30, "willpower": -20, "blood": 40},
                "sound": "whisper"
            },
            {
                "text_en": "'It was a trick, beast!' Splash your holy flask directly into her open jaws!",
                "text_ru": "«Это была уловка, тварь!» Плеснуть святую воду прямо в её открытую пасть!",
                "next": "REALM_TRANSITION",
                "stats": {"sanity": 15, "willpower": 20, "blood": -10},
                "sound": "screech"
            }
        ]
    },

    "REALM_TRANSITION": {
        "title_en": "Chapter II: The Realm of the Red Eclipse",
        "title_ru": "Глава II: Царство Алого Затмения",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "With a deafening crack that tears through space itself, the walls of St. Vlas Monastery disintegrate into crimson ash!\n\nYou fall through an endless sky of swirling blood mist, landing hard on a desert composed entirely of pale human dust and crushed skulls. Overhead hangs a giant, pulsating Red Eclipse—a black sun crowned by a blinding red ring of fire.\n\nKobyla stands before you, now vast as a mountain range. Her body is woven from black thunderstorms and liquid starlight; her red mane flows across the sky like rivers of blood. Her glowing white eyes occupy half the horizon.",
        "text_ru": "С оглушительным треском, разрывающим само пространство, стены монастыря рассыпаются в багровый пепел!\n\nВы падаете сквозь бесконечное небо из алого тумана и с грохотом приземляетесь на пустыню из белой человеческой пыли и расколотых черепов. Над головой висит гигантское, пульсирующее Алое Затмение — черное солнце, увенчанное короной огня.\n\nКобыла возвышается перед вами, подобно горному хребту. Её тело соткано из грозовых туч и жидкого света; её алая грива течет по небу, словно река крови. Её белые глаза занимают пол-горизонта.",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "Build a spiritual barrier around your mind using your pure Willpower!",
                "text_ru": "Возвести духовный барьер вокруг разума, используя силу Воли!",
                "next": "TRIAL_VISIONS",
                "stats": {"sanity": 10, "willpower": 25, "blood": 0},
                "sound": "chant"
            },
            {
                "text_en": "Draw power from the blood mark on your hand to withstand her pressure!",
                "text_ru": "Черпать силу из кровавой метки на своей руке!",
                "next": "TRIAL_VISIONS",
                "stats": {"sanity": -15, "willpower": 10, "blood": 20},
                "sound": "whisper"
            },
            {
                "text_en": "Search the landscape for the spectral anchor binding her to the original art.",
                "text_ru": "Искать в пейзаже призрачный якорь, привязывающий её к картине.",
                "next": "TRIAL_VISIONS",
                "stats": {"sanity": 15, "willpower": 15, "blood": -5},
                "sound": "heartbeat"
            }
        ]
    },

    "TRIAL_VISIONS": {
        "title_en": "Chapter III: The Trial of Torment",
        "title_ru": "Глава III: Испытание Муками",
        "speaker_en": "Kobyla",
        "speaker_ru": "Кобыла",
        "text_en": "The sky above you split into a million mirror fragments. In each mirror, you see visions of your past and future.\n\nYou see your family homestead engulfed in crimson flames. You see your old mentor lying dead in his library, eyes turned to chalk. You see yourself—aged, broken, wandering through a desolate plague-ridden land, rejected by god and man alike.\n\n'This is your reality, Elijah!' Kobyla's voice roars like avalanche stone. 'All your holy studies, all your sacrifices... worthless dust! Give up your fragile mind! Let me drown your memories in warm crimson water!'",
        "text_ru": "Небо над вами раскалывается на миллионы зеркальных осколков. В каждом из них вы видите видения своего прошлого и будущего.\n\nВы видите свой отчий дом, объятый алым пламенем. Вы видите своего старого учителя, лежащего мертвым в библиотеке с ослепшими глазами. Вы видите себя — старого, сломленного, бредущего по вымершей от чумы земле, отвергнутого богом и людьми.\n\n«Это твоя реальность, Илья!» — голос Кобылы грохочет, как горный обвал. «Все твои молитвы, все твои жертвы... никчёмная пыль! Отдай мне свой хрупкий разум! Позволь мне утопить твои воспоминания в теплой алой воде!»",
        "effect": "blood-flash",
        "choices": [
            {
                "text_en": "Plunge your dagger into your leg to break the hypnotic vision with real physical pain!",
                "text_ru": "Вонзить нож себе в ногу, чтобы пробить гипноз реальной физической болью!",
                "next": "ALTAR_RETURN",
                "stats": {"sanity": 20, "willpower": 30, "blood": 10},
                "sound": "blade"
            },
            {
                "text_en": "Embrace the grief and let the dark waters fill your heart.",
                "text_ru": "Принять эту боль и позволить темным водам залить сердце.",
                "next": "ALTAR_RETURN",
                "stats": {"sanity": -35, "willpower": -20, "blood": 30},
                "sound": "whisper"
            },
            {
                "text_en": "Focus on the glowing silver seal ring buried in the skeletal dust at your feet!",
                "text_ru": "Фокусироваться на светящемся серебряном кольце-печати в пыли под ногами!",
                "next": "ALTAR_RETURN",
                "stats": {"sanity": 15, "willpower": 20, "blood": -5},
                "sound": "chant"
            }
        ]
    },

    "ALTAR_RETURN": {
        "title_en": "Chapter IV: The Climax at the Altar",
        "title_ru": "Глава IV: Развязка у Алтаря",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "The dreamscape collapses in a blinding explosion of scarlet light!\n\nYou crash back onto the stone altar of the flooded crypt. The storm outside is howling through shattered rose windows. Before you, Kobyla's massive physical avatar is pinned between our realm and the empty canvas frame, thrashing in demonic fury.\n\nHer glowing white eyes lock onto yours. The blood in the crypt rises to your knees. This is the moment of final choice. You hold the power to shape the fate of humanity and your soul forever.",
        "text_ru": "Иллюзия рушится с ослепительным взрывом скарлатинового света!\n\nВы снова в склепе на каменном алтаре. Гроза снаружи бушует сквозь разбитые готические витражи. Перед вами исполинский силуэт Кобылы застрял между нашим миром и пустой рамой картины, биясь в адском гневе.\n\nЕё белые глаза впиваются в вас. Кровь в склепе поднимается уже до колен. Это момент окончательного выбора. В ваших руках — судьба вашего разума и всего человечества.",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "Perform the Ultimate Sacrificial Sealing Rite using your consecrated blood!",
                "text_ru": "Провести Высший Ритуал Заточения с использованием своей священной крови!",
                "next": "CHECK_ENDING_SEAL",
                "stats": {"sanity": 0, "willpower": 0, "blood": 0},
                "sound": "chant"
            },
            {
                "text_en": "Offer your throat and mortal body to become the physical Host of Kobyla!",
                "text_ru": "Предложить своё горло и тело, став физическим Сосудом Кобылы!",
                "next": "CHECK_ENDING_VESSEL",
                "stats": {"sanity": 0, "willpower": 0, "blood": 0},
                "sound": "whisper"
            },
            {
                "text_en": "Hurl your lit lantern into the dry grain and oil barrels, burning the entire monastery down!",
                "text_ru": "Бросить горящий фонарь в бочки с маслом, сжигая монастырь дотла!",
                "next": "CHECK_ENDING_FIRE",
                "stats": {"sanity": 0, "willpower": 0, "blood": 0},
                "sound": "screech"
            },
            {
                "text_en": "Mount the dark beast, swear fealty to the Red Eclipse, and become her Dark Herald!",
                "text_ru": "Оседлать темную тварь, поклясться в верности Алому Затмению и стать её Всадником!",
                "next": "CHECK_ENDING_HERALD",
                "stats": {"sanity": 0, "willpower": 0, "blood": 0},
                "sound": "roar"
            }
        ]
    },

    "CHECK_ENDING_SEAL": {
        "title_en": "Resolving the Binding...",
        "title_ru": "Завершение Ритуала...",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "You raise your obsidian blade, carving holy seals into your chest while chanting the ancient vow of St. Vlas. The blood from your heart ignites into golden-white fire!",
        "text_ru": "Вы поднимаете обсидиановый клинок, высекая священные знаки на своей груди и произнося древнюю клятву Святого Власа. Кровь из вашего сердца вспыхивает золотисто-белым огнем!",
        "effect": "flash-white",
        "choices": [
            {
                "text_en": "Seal her away forever!",
                "text_ru": "Заточить её навеки!",
                "next": "ENDING_1_SEALED",
                "stats": {},
                "sound": "chant"
            }
        ]
    },

    "CHECK_ENDING_VESSEL": {
        "title_en": "The Transformation...",
        "title_ru": "Преображение...",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "You drop your blade into the dark water and open your arms. Kobyla screeches in demonic joy as her shadow surges down your throat!",
        "text_ru": "Вы бросаете клинок в темную воду и расправляете руки. Кобыла визжит от адской радости, когда её тень устремляется в ваше горло!",
        "effect": "blood-flash",
        "choices": [
            {
                "text_en": "Become the Vessel!",
                "text_ru": "Стать Сосудом!",
                "next": "ENDING_2_VESSEL",
                "stats": {},
                "sound": "whisper"
            }
        ]
    },

    "CHECK_ENDING_FIRE": {
        "title_en": "The Purifying Flames...",
        "title_ru": "Очищающий Огонь...",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "You smash the brass lantern against the oil drums! An instantaneous wall of roaring yellow flame engulfs the easel, the canvas, and the ancient timber vaults!",
        "text_ru": "Вы разбиваете латунный фонарь о бочки с маслом! Мгновенная стена ревущего желтого пламени охватывает мольберт, холст и древние деревянные своды!",
        "effect": "shake-heavy",
        "choices": [
            {
                "text_en": "Witness the inferno!",
                "text_ru": "Узреть адское пламя!",
                "next": "ENDING_4_FIRE",
                "stats": {},
                "sound": "screech"
            }
        ]
    },

    "CHECK_ENDING_HERALD": {
        "title_en": "The Dark Alliance...",
        "title_ru": "Темный Альянс...",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "You leap onto the muscular back of the demonic mare, gripping her fiery red mane in your bloodied hands! Together, you burst through the cathedral ceiling into the stormy sky!",
        "text_ru": "Вы взбираетесь на мускулистую спину демонической кобылы, сжимая её огненную алую гриву окровавленными руками! Вместе вы пробиваете своды собора и вылетаете в грозовое небо!",
        "effect": "pulse-red",
        "choices": [
            {
                "text_en": "Ride into the night!",
                "text_ru": "Мчаться в ночь!",
                "next": "ENDING_5_HERALD",
                "stats": {},
                "sound": "roar"
            }
        ]
    },

    "ENDING_1_SEALED": {
        "title_en": "ENDING I: Sacred Sealing (Holy Victory)",
        "title_ru": "ФИНАЛ I: Священное Заточение (Победа Веры)",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "The golden holy fire engulfs Kobyla! She screams in agony as invisible chains of sacred light pull her back into the canvas frame. The paint hardens; the blood cools into black lacquer.\n\nThe canvas is quiet once more. Kobyla is bound for another millennium.\n\nYou stumble out of the crumbling ruins as the dawn light breaks over the mountains. You survived... but every time you close your eyes, you still see those two blinding white eyes watching you from the deep crimson darkness.",
        "text_ru": "Золотой священный огонь охватывает Кобылу! Она визжит от боли, пока невидимые цепи святого света затягивают её обратно в раму холста. Краска затвердевает; кровь превращается в черный лак.\n\nХолст снова неподвижен. Кобыла заточена ещё на одно тысячелетие.\n\nВы выбираетесь из рушащихся руин, когда над горами встает рассвет. Вы выжили... но каждый раз, закрывая глаза, вы видите два слепящих белых глаза, смотрящих на вас из багровой тьмы.",
        "effect": "flash-white",
        "is_ending": True,
        "ending_id": "ENDING_1",
        "choices": []
    },

    "ENDING_2_VESSEL": {
        "title_en": "ENDING II: The Red Eclipse Incarnate (Dark Loss)",
        "title_ru": "ФИНАЛ II: Сосуд Алого Затмения (Темное Поглощение)",
        "speaker_en": "Kobyla / Elijah",
        "speaker_ru": "Кобыла / Илья",
        "text_en": "Kobyla's shadow pours down your throat like liquid magma. Your ribs crack; your blood boils. When you open your eyes, they shine with pure, blinding white luminescence.\n\nDr. Elijah Vance is no more. Only Kobyla remains, now clothed in human flesh.\n\nYou walk out of the sunken monastery into the night. Where you step, flowers wither and cattle drop dead. A new age of nightmares has begun for the world of men.",
        "text_ru": "Тень Кобылы вливается в ваше горло, словно жидкая магма. Ребра трещат; кровь закипает. Когда вы открываете глаза, они сияют чистым, ослепительным белым светом.\n\nДоктора Ильи Вэнса больше нет. Осталась лишь Кобыла, обретшая человеческую плоть.\n\nВы выходите из затопленного монастыря в ночь. Там, где вы ступаете, вянут цветы и падает мертвым скот. Для мира людей началась новая эпоха кошмаров.",
        "effect": "blood-flash",
        "is_ending": True,
        "ending_id": "ENDING_2",
        "choices": []
    },

    "ENDING_3_TRAPPED": {
        "title_en": "ENDING III: Trapped in the Bleeding Canvas (Eternal Nightmare)",
        "title_ru": "ФИНАЛ III: Пленник Алого Холста (Вечный Кошмар)",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "Your sanity shatters completely under her mental assault! Kobyla laughs as she pulls your soul out of your body and drags it into the oil pigments.\n\nYour physical corpse falls lifelessly into the flooded tomb. Inside the painting, you are now a tiny, terrified shadow figure painted into the crimson background, trapped forever as Kobyla stares down at you with her burning white eyes.",
        "text_ru": "Ваш разум окончательно раскалывается под её ментальным ударом! Кобыла хохочет, вырывая вашу душу из тела и затягивая её прямо в масляные краски.\n\nВаш смертный труп безжизненно падает в воду склепа. А внутри картины вы становитесь крошечной, дрожащей тенью на багровом фоне, заточенной навеки, пока Кобыла смотрит на вас своими белыми глазами.",
        "effect": "pulse-red",
        "is_ending": True,
        "ending_id": "ENDING_3",
        "choices": []
    },

    "ENDING_4_FIRE": {
        "title_en": "ENDING IV: Ashes of St. Vlas (Pyrrhic Martyrdom)",
        "title_ru": "ФИНАЛ IV: Пепел Святого Власа (Мученическая Жертва)",
        "speaker_en": "Narrator",
        "speaker_ru": "Повествователь",
        "text_en": "The inferno consumes everything! Flame eats through the canvas, burning the oil pigments into nonexistence. Kobyla screams in fury as her physical anchor dissolves in holy heat.\n\nThe stone vaults collapse above, burying the crypt, the easel, and yourself under hundreds of tons of rubble.\n\nYou die in the flames, but as your breathing stops, you smile knowing that the nightmare was destroyed with you.",
        "text_ru": "Адское пламя пожирает всё! Огонь въедается в холст, выжигая масляные краски без остатка. Кобыла визжит от ярости, пока её якорь растворяется в раскаленном жаре.\n\nКаменные своды рушатся, погребая склеп, мольберт и вас самих под сотнями тонн обломков.\n\nВы погибаете в огне, но, засыпая навеки, улыбаетесь — вы знаете, что кошмар уничтожен вместе с вами.",
        "effect": "shake-heavy",
        "is_ending": True,
        "ending_id": "ENDING_4",
        "choices": []
    },

    "ENDING_5_HERALD": {
        "title_en": "ENDING V: The Dark Herald (Apocalyptic Triumph)",
        "title_ru": "ФИНАЛ V: Всадник Апокалипсиса (Темный Триумф)",
        "speaker_en": "Elijah & Kobyla",
        "speaker_ru": "Илья и Кобыла",
        "text_en": "You do not submit as a slave—you claim your place as her Dark Rider! Together you charge into the stormy night sky under the light of the Red Eclipse.\n\nWith your obsidian blade in hand and Kobyla beneath you, you ride across human lands, bringing dark justice, tearing down corrupt kingdoms, and heralding a grand new red dawn.",
        "text_ru": "Вы не подчиняетесь как раб — вы заявляете свои права как её Темный Всадник! Вместе вы устремляетесь в грозовое ночное небо под светом Алого Затмения.\n\nС обсидиановым клинком в руке и Кобылой под вами вы несетесь по землям людей, неся темную справедливость, руша гнилые королевства и возвещая новый алый рассвет.",
        "effect": "pulse-red",
        "is_ending": True,
        "ending_id": "ENDING_5",
        "choices": []
    }
}

print("Story nodes created:", len(story_nodes))
