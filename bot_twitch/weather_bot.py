import json
import re
import socket
import time
import urllib.parse
import urllib.request

# --- НАСТРОЙКИ ---
SERVER = "irc.chat.twitch.tv"
PORT = 6667
NICK = "GavGavichBot_"
TOKEN = "oauth:c7s7bd241bmuwilojv0xe1gjbe43a1"
CHANNEL = "#surgefly"
OWNER_LOGIN = CHANNEL.lstrip("#").lower()
WEATHER_API_URL = "https://weather-bot-6-vxs1.onrender.com/weather?city={}"
USER_LEVELS_FILE = "user_levels.json"
HIGH_LEVEL_USERS_FILE = "high_level_users.json"

BANNED_WORDS = {
    "zov": 600,
    "зов": 600,
    "z": 10,
    "з": 10,
}
RESPONSE_TAG_RE = re.compile(r"\s*(?:#?(?:reply|say)#?)\s*$", re.IGNORECASE)

DISCORD_URL = "https://discord.gg/eUuvyvDVy6"
DONATE_URLS = "https://donatepay.eu/don/22792 / https://destream.net/live/kxrvinho/donate"
TIKTOK_URL = "https://www.tiktok.com/@kxrvinho28"
YOUTUBE_URL = "https://www.youtube.com/@kxrvinhofn"
TRACKER_URL = "https://fortnitetracker.com/profile/all/kxrvinho.gg33"
SPOTIFY_URL = "https://open.spotify.com/user/98c989tklfakvmp7qnsy2w5nb"
PLAYLIST_URL = "https://open.spotify.com/playlist/5L9RmnsYoL8L3ErNr5zQrZ?si=e3b9104791cf4c33"
PLAYLIST_URLS = (
    "https://open.spotify.com/playlist/5L9RmnsYoL8L3ErNr5zQrZ?si=e3b9104791cf4c33 / "
    "https://vk.com/music?z=audio_playlist384656841_83889939/90e725b9a047edd1dc / "
    "https://music.yandex.ru/users/Yeatsbigtonka/playlists/1002"
)
TWITTER_URL = "https://twitter.com/28kxrvinho"
INSTAGRAM_URL = "https://www.instagram.com/champagnepapi/"
STEAM_TRADE_URL = "https://steamcommunity.com/tradeoffer/new/?partner=346043495&token=cpPiJxRi"
TG_URL = "https://t.me/kxrvinhoGG33"
LUDO_TG_URL = "https://t.me/volodyaludik"
FUNPAY_URL = "https://funpay.com/go/NewYearKxrvinho"

HEADSET = "HyperX Cloud 2"
KEYBOARD = "Steel Series Apex Pro"
MOUSE = "Finalmouse ultralightx Guardian Lion"
MOUSEPAD = "XTRFY GP4"
MONITOR = "Acer Predator 240hz"
MICROPHONE = f"От наушников ({HEADSET})"
DEVICE_LIST = f"{KEYBOARD}, {MOUSE}, {HEADSET}, {MOUSEPAD}"
PC_SPECS = "i7-12700kf rtx 3070ti MSI PRO z690-a ddr4 ssd 980 samsung 500gb"
MOVEMENT_CLIP = "75 90 135 https://clips.twitch.tv/SpikyTriangularPartridgeBuddhaBar-U4QvEiWnogsb0H_q"
BINDS_CLIP = "https://clips.twitch.tv/OddCourageousBurritoPeteZaroll-QuFSUvPTnXlsHeQE"
GRAPHIC_CLIP = "https://clips.twitch.tv/SmilingAttractiveAlligatorGivePLZ-Qj8g1q_MNvjqIHNS"
SETTINGS_CLIP = "https://www.twitch.tv/kxrvinho/clip/DoubtfulHorribleShingleNononoCat-hKTzXD3lIURzt8qt"
SENS_TEXT = "x: 8.0 / y: 8.0 / 30% ads (800 dpi)"
SUPERMAP_TEXT = "Новая карта для фана – Crazy PVP! Бери любое оружие, суперсилы, гоняй на чем хочешь и мочи всех! Код: 0852-9606-7878"

# --- ДАННЫЕ ---
commands = {
    "!0delay": "VOLODYA 0 DELAY 1V1 - 3968-5016-9340",
    "!0дилей": "VOLODYA 0 DELAY 1V1 - 3968-5016-9340",
    "!1v1": "1602-5676-9780",
    "!1в1": "1602-5676-9780",
    "!7tv": "Не хочешь быть обычным типом, который не видит крутые анимированные смайлы в чате? Тогда скачивай расширение и кайфуй! https://7tv.app/",
    "!52": "писят два 🖐✌",
    "!bestfriend": "Tetris_qq",
    "!brightness": "100%",
    "!city": "Kiev ili Kyiv",
    "!code": "VOLODYA in the item shop #ad",
    "!colorblind": "off 3",
    "!commands": "Список команд: https://b2sd.github.io/commands/Commands.html",
    "!devices": DEVICE_LIST,
    "!discord": DISCORD_URL,
    "!donate": DONATE_URLS,
    "!doublemovement": MOVEMENT_CLIP,
    "!dpi": "800",
    "!ds": DISCORD_URL,
    "!dstimer": f"Подпишись, чтобы первым узнавать о новостях и анонсах! {TG_URL} DinoDance",
    "!duo": "@7tor",
    "!earnings": "пару раз похавать",
    "!edit": "edit on release on (bind F, edit)",
    "!editonrelease": "on",
    "!epicgames": "BAN HIS ASAP!!!! STREAMSNIPING ME FOR 1.5 YEARS.I HAVE ALREADY LOST ALL MY BRAINCELLS! PLEASE ERIC GAMES",
    "!from": "Украина, Киев.",
    "!funpay": f"Покупай В-Баксы на FunPay - {FUNPAY_URL}",
    "!graphic": GRAPHIC_CLIP,
    "!headphones": HEADSET,
    "!headset": HEADSET,
    "!hud": "75%",
    "!hz": "240hz",
    "!inst": INSTAGRAM_URL,
    "!keyboard": KEYBOARD,
    "!live": "Kiev ili Kyiv",
    "!map": "1602-5676-9780",
    "!mic": MICROPHONE,
    "!micro": MICROPHONE,
    "!microphone": MICROPHONE,
    "!mogged": "❌SIGMA - 1v1 больше нет ❌ 🏆НОВАЯ КАРТА - MOGGED 1v1 🏆 . Код карты: 1602-5676-9780 Заходи ДРУГ!🍻",
    "!monitor": MONITOR,
    "!mouse": MOUSE,
    "!mousepad": MOUSEPAD,
    "!movement": MOVEMENT_CLIP,
    "!name": "Vladimir",
    "!pc": PC_SPECS,
    "!pcboost": "От Missout",
    "!playlist": PLAYLIST_URL,
    "!pvp": "Играй на карте MOGGED PVP - 6297-2345-7833",
    "!rank": "Величайший",
    "!res": "1920x1080",
    "!resolution": "1920x1080",
    "!sens": SENS_TEXT,
    "!sensitivity": SENS_TEXT,
    "!setting": SETTINGS_CLIP,
    "!settings": SETTINGS_CLIP,
    "!setup": "!keyboard !mouse !mousepad !headphones",
    "!shorts": YOUTUBE_URL,
    "!sigma": "1602-5676-9780",
    "!sigmapvp": "SIGMA PVP - 6297-2345-7833",
    "!song": "Сейчас играет $(lastfm kxrvmusic) / Заказать свою музыку на стрим – 160₽ - !донат",
    "!spotify": SPOTIFY_URL,
    "!supermap": SUPERMAP_TEXT,
    "!tg": TG_URL,
    "!tiktok": TIKTOK_URL,
    "!tracker": TRACKER_URL,
    "!tt": TIKTOK_URL,
    "!twitter": TWITTER_URL,
    "!w": "W😈",
    "!x": TWITTER_URL,
    "!youtube": YOUTUBE_URL,
    "!yt": YOUTUBE_URL,
    "!аук": f"АУК НА ФИЛЬМ {DONATE_URLS}",
    "!ахуетьхуйня": "Сигма брат",
    "!бинды": BINDS_CLIP,
    "!буст": "от missout",
    "!вебка": "canon prosto 480L",
    "!графика": GRAPHIC_CLIP,
    "!даблмувмент": MOVEMENT_CLIP,
    "!девайсы": DEVICE_LIST,
    "!дипиай": "800",
    "!дискорд": DISCORD_URL,
    "!донат": DONATE_URLS,
    "!дпи": "800",
    "!дс": DISCORD_URL,
    "!закреп": f"🍻 USE CODE VOLODYA IN FORTNITE SHOP / DS - {DISCORD_URL} / TG - {TG_URL} / TT - {TIKTOK_URL}",
    "!имя": "Владимир",
    "!карта": "MOGGED 1V1 - 1602-5676-9780",
    "!катка": "Катка 3/3 за победу дают 100$",
    "!кейбоард": KEYBOARD,
    "!кейборд": KEYBOARD,
    "!клава": KEYBOARD,
    "!клавиатура": KEYBOARD,
    "!код": "КОД АВТОРА - VOLODYA",
    "!красота": "КОНКУРС КРАСОТЫ НА СТРИМЕ , КИДАЕМ ВНЕШКУ - https://discord.com/channels/1181217671908438117/1373740649026949271",
    "!лудотг": f"ЛУДО КАНАЛ - {LUDO_TG_URL}",
    "!микро": MICROPHONE,
    "!микрофон": MICROPHONE,
    "!монитор": MONITOR,
    "!мувмент": MOVEMENT_CLIP,
    "!музыка": f"Заказать свою музыку на стрим – 155₽ - {DONATE_URLS}",
    "!мышка": MOUSE,
    "!мышь": MOUSE,
    "!н": HEADSET,
    "!настройки": GRAPHIC_CLIP,
    "!наушники": HEADSET,
    "!начало": "Начало 01:44",
    "!ник": "Карвиньо",
    "!нуихуйня": "Играй на карте SIGMA PVP - 9735-2382-8408",
    "!пк": PC_SPECS,
    "!пкбуст": "Миссаут",
    "!плейлист": PLAYLIST_URLS,
    "!плэйлист": PLAYLIST_URLS,
    "!погода": "Напиши город после команды, например: !погода Kyiv",
    "!порода": "бульбульдог",
    "!ранг": "КМС ПО ЛОББИ",
    "!рефка": f"Рефка в моем лудотг в закрепе - {LUDO_TG_URL}",
    "!сенса": SENS_TEXT,
    "!сигматг": f"Чтобы сыграть на стриме нужно - Поставить лайк на карте SIGMА 1v1 (1602-5676-9780) + добавить в FAVORITE , скинуть ОДИН скрин в тг, под последний пост и написать свой ник - {TG_URL}",
    "!ситингс": GRAPHIC_CLIP,
    "!спотифай": SPOTIFY_URL,
    "!ставка": "СТАВКА В ЧАТЕ",
    "!супер": SUPERMAP_TEXT,
    "!суперкарта": "⚡️ All Guns Superpowers FFA : 0852-9606-7878 ⚡️",
    "!сэтингс": GRAPHIC_CLIP,
    "!таймердс": f"/announceblue Заходи на наш Discord-сервер! Тут можно пообщаться, отдохнуть и весело провести время: {DISCORD_URL}",
    "!таймерзаказатьтрек": f"/announceorange Заказать свою музыку на стрим – 155₽ - {DONATE_URLS}",
    "!таймеркод": "/announceblue USE CODE VOLODYA IN FORTNITE SHOP | FAVORITE CREATOR VOLODYA",
    "!таймертг": f"/announceblue Подпишись, чтобы первым быть в курсе всех новостей и анонсов! {TG_URL}",
    "!тг": f"Подпишись, чтобы первым быть в курсе всех новостей и анонсов! {TG_URL}",
    "!тикток": TIKTOK_URL,
    "!трейд": STEAM_TRADE_URL,
    "!трек": "Сейчас играет $(lastfm kxrvmusic) / Заказать свою музыку на стрим – 160₽ - !донат",
    "!трекер": TRACKER_URL,
    "!тт": TIKTOK_URL,
    "!ухилянты": "зетич 📺 зетквизи 🚌 зетостя 🌊 зетенок 📝 зетеня 🦺 зетанита 👄 зотатитек 🎵 - вместе мы зетерка 🦸",
    "!уши": HEADSET,
    "!цветокор": "Протанопия 3",
    "!чиназес": "Санчизес",
    "!ют": YOUTUBE_URL,
    "!ютуб": YOUTUBE_URL,
    "!яркость": "100%",
}

dynamic_commands = {}
user_levels = {}
high_level_users = []
sock = None

try:
    with open("dynamic_commands.json", "r", encoding="utf-8") as file:
        dynamic_commands = json.load(file)
except Exception:
    pass

try:
    with open(USER_LEVELS_FILE, "r", encoding="utf-8") as file:
        user_levels = json.load(file)
except Exception:
    pass

try:
    with open(HIGH_LEVEL_USERS_FILE, "r", encoding="utf-8") as file:
        high_level_users = json.load(file)
except Exception:
    pass


def clean_response(text):
    if not isinstance(text, str):
        return None
    return RESPONSE_TAG_RE.sub("", text).strip()


def extract_login(response_line):
    match = re.search(r":([a-zA-Z0-9_]+)![^ ]+ PRIVMSG", response_line)
    if match:
        return match.group(1)
    return None


def save_dynamic():
    with open("dynamic_commands.json", "w", encoding="utf-8") as file:
        json.dump(dynamic_commands, file, ensure_ascii=False, indent=2)


def save_user_levels():
    with open(USER_LEVELS_FILE, "w", encoding="utf-8") as file:
        json.dump(user_levels, file, ensure_ascii=False, indent=2)


def save_high_level_users():
    with open(HIGH_LEVEL_USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(high_level_users, file, ensure_ascii=False, indent=2)


def connect():
    global sock

    if sock is not None:
        try:
            sock.close()
        except OSError:
            pass

    sock = socket.socket()
    sock.connect((SERVER, PORT))
    sock.sendall("CAP REQ :twitch.tv/tags twitch.tv/commands\r\n".encode("utf-8"))
    sock.sendall(f"PASS {TOKEN}\r\n".encode("utf-8"))
    sock.sendall(f"NICK {NICK}\r\n".encode("utf-8"))
    sock.sendall(f"JOIN {CHANNEL}\r\n".encode("utf-8"))
    print("Бот запущен!")


def send(message):
    response = clean_response(message)
    if not response:
        return

    payload = f"PRIVMSG {CHANNEL} :{response}\r\n".encode("utf-8")
    try:
        sock.sendall(payload)
    except OSError:
        connect()
        sock.sendall(payload)


def get_response(command_name):
    if command_name in commands:
        return clean_response(commands[command_name])
    if command_name in dynamic_commands:
        return clean_response(dynamic_commands[command_name])
    return None


def normalize_login(login):
    return login.lstrip("@").strip().lower()


def is_high_level_user(user_login):
    return normalize_login(user_login) in {normalize_login(login) for login in high_level_users}


def get_user_level(user_login, is_broadcaster):
    normalized_login = normalize_login(user_login)
    if normalized_login == OWNER_LOGIN or is_broadcaster or is_high_level_user(normalized_login):
        return 99
    return int(user_levels.get(normalized_login, 0))


def can_use_spam(level):
    return level >= 1


def can_add_commands(level):
    return level >= 2


def spam_command(command_name, count):
    text = get_response(command_name)
    if not text:
        return

    for _ in range(min(count, 10)):
        send(text)
        time.sleep(0.2)


def fetch_weather(message):
    parts = message.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        return commands["!погода"]

    city = parts[1].strip()
    url = WEATHER_API_URL.format(urllib.parse.quote(city))

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return clean_response(response.read().decode("utf-8", errors="ignore"))
    except Exception:
        return "Не удалось получить погоду, попробуй позже."


def handle_privmsg(response_line):
    if "PRIVMSG" not in response_line:
        return

    tags = response_line.split(" ")[0]
    is_broadcaster = "badges=broadcaster/1" in tags
    is_mod = "mod=1" in tags or is_broadcaster

    user_match = re.search(r"display-name=([^; ]+)", tags)
    user_name = user_match.group(1) if user_match else "User"
    user_login = extract_login(response_line) or user_name
    user_level = get_user_level(user_login, is_broadcaster)

    try:
        message = response_line.split(f"PRIVMSG {CHANNEL} :", 1)[1].strip()
    except (IndexError, ValueError):
        return

    if not message:
        return

    message_lower = message.lower()
    command_name = message_lower.split()[0]

    if not is_mod:
        for word, timeout in BANNED_WORDS.items():
            if re.search(rf"\b{re.escape(word)}\b", message_lower):
                send(f"/timeout {user_login} {timeout}")
                return

    if message_lower.startswith("!lvl "):
        if user_level < 99:
            return

        parts = message_lower.split()
        if len(parts) == 3 and parts[1].isdigit():
            new_level = int(parts[1])
            target_login = normalize_login(parts[2])

            if new_level not in (0, 1, 2):
                send(f"@{user_login} доступные уровни: 0, 1, 2")
                return

            if target_login == OWNER_LOGIN:
                send(f"@{user_login} владельцу уровень менять нельзя")
                return

            if new_level == 0:
                user_levels.pop(target_login, None)
            else:
                user_levels[target_login] = new_level

            save_user_levels()
            send(f"{user_login} выдал пользователю @{target_login} {new_level} уровень  модерации")
        return

    if message_lower.startswith("!highlvl "):
        if normalize_login(user_login) != OWNER_LOGIN:
            return

        parts = message_lower.split()
        if len(parts) == 2:
            target_login = normalize_login(parts[1])

            if target_login == OWNER_LOGIN:
                send(f"@{user_login} ты уже главный")
                return

            if target_login not in {normalize_login(login) for login in high_level_users}:
                high_level_users.append(target_login)
                save_high_level_users()

            send(f"{user_login} выдал пользователю {target_login} уровень ГЛАВНЫЙ теперь у него полный доступ")
        return

    if message_lower.startswith("!unhighlvl "):
        if normalize_login(user_login) != OWNER_LOGIN:
            return

        parts = message_lower.split()
        if len(parts) == 2:
            target_login = normalize_login(parts[1])
            updated_high_levels = [login for login in high_level_users if normalize_login(login) != target_login]

            if len(updated_high_levels) == len(high_level_users):
                send(f"@{user_login} пользователь @{target_login} не найден в highlvl")
                return

            high_level_users.clear()
            high_level_users.extend(updated_high_levels)
            save_high_level_users()
            send(f"@{user_login} пользователь @{target_login} удален из highlvl")
        return

    if message_lower == "!lvllist":
        if user_level < 99:
            return

        if not user_levels:
            send(f"@{user_login} список lvl пуст")
            return

        level_entries = [f"@{login} {level} lvl" for login, level in sorted(user_levels.items())]
        send("Лист уровней модерации: " + ", ".join(level_entries))
        return

    if message_lower == "!highlvllist":
        if user_level < 99:
            return

        normalized_high_levels = sorted({normalize_login(login) for login in high_level_users})
        if not normalized_high_levels:
            send(f"@{user_login} список highlvl пуст")
            return

        send("highlvl: " + ", ".join(f"@{login}" for login in normalized_high_levels))
        return

    if message_lower.startswith("!cmd add "):
        if not can_add_commands(user_level):
            return

        parts = message.split(" ", 3)
        if len(parts) >= 4:
            name = parts[2].lower()
            if not name.startswith("!"):
                name = "!" + name
            dynamic_commands[name] = clean_response(parts[3])
            save_dynamic()
            send(f"@{user_login} команда {name} добавлена")
        return

    if message_lower.startswith("!спам "):
        if not can_use_spam(user_level):
            return

        parts = message_lower.split()
        if len(parts) == 3 and parts[2].isdigit():
            cmd = parts[1]
            if not cmd.startswith("!"):
                cmd = "!" + cmd
            spam_command(cmd, int(parts[2]))
        return

    match = re.fullmatch(r"(!\S+?)(\d+)", command_name)
    if can_use_spam(user_level) and match:
        spam_command(match.group(1), int(match.group(2)))


# --- ЗАПУСК ---
connect()
buffer = ""

while True:
    try:
        buffer += sock.recv(4096).decode("utf-8", errors="ignore")
    except OSError:
        connect()
        buffer = ""
        continue

    while "\r\n" in buffer:
        response_line, buffer = buffer.split("\r\n", 1)

        if not response_line:
            continue

        if response_line.startswith("PING"):
            sock.sendall("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            continue

        handle_privmsg(response_line)
