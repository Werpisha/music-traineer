"""
Music Trainer — весь сайт в одном файле.
Запуск: streamlit run app.py

Структура (создай вручную папки):
  app.py
  requirements.txt
  library/        <- сюда кладёшь PDF/DOC
  data/           <- создастся автоматически
"""
import os
import json
import hashlib
import random

import streamlit as st

# =========================================================
#  НАСТРОЙКА СТРАНИЦЫ
# =========================================================
st.set_page_config(
    page_title="Music Trainer",
    page_icon="🎵",
    layout="centered",
)

# =========================================================
#  ПУТИ
# =========================================================
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
LIBRARY_DIR = "library"

# =========================================================
#  БАЗА ДАННЫХ УПРАЖНЕНИЙ
# =========================================================
NOTES_RU = ["до", "ре", "ми", "фа", "соль", "ля", "си"]

INTERVALS = [
    "ч.1", "м.2", "б.2", "м.3", "б.3",
    "ч.4", "ув.4", "ум.5", "ч.5",
    "м.6", "б.6", "м.7", "б.7", "ч.8",
]

INTERVAL_SEMITONES = {
    "ч.1": 0, "м.2": 1, "б.2": 2, "м.3": 3, "б.3": 4,
    "ч.4": 5, "ув.4": 6, "ум.5": 6, "ч.5": 7,
    "м.6": 8, "б.6": 9, "м.7": 10, "б.7": 11, "ч.8": 12,
}

TRIADS_BEGINNER = ["мажорное", "минорное", "увеличенное", "уменьшённое"]

TRIAD_INVERSIONS = [
    "секстаккорд мажорный", "квартсекстаккорд мажорный",
    "секстаккорд минорный", "квартсекстаккорд минорный",
]

SEVENTH_CHORDS = ["D7", "D65", "D43", "D2", "II7", "VII7"]

BASIC_MAJOR_KEYS = [
    ("До мажор", 0),
    ("Соль мажор", 1), ("Ре мажор", 2), ("Ля мажор", 3),
    ("Ми мажор", 4), ("Си мажор", 5),
    ("Фа мажор", 1), ("Си-бемоль мажор", 2), ("Ми-бемоль мажор", 3),
    ("Ля-бемоль мажор", 4), ("Ре-бемоль мажор", 5),
]

BASIC_MINOR_KEYS = [
    ("Ля минор", 0),
    ("Ми минор", 1), ("Си минор", 2), ("Фа-диез минор", 3),
    ("До-диез минор", 4), ("Соль-диез минор", 5),
    ("Ре минор", 1), ("Соль минор", 2), ("До минор", 3),
    ("Фа минор", 4), ("Си-бемоль минор", 5),
]

PARALLEL_KEYS = [
    ("До мажор", "Ля минор"),
    ("Соль мажор", "Ми минор"),
    ("Ре мажор", "Си минор"),
    ("Ля мажор", "Фа-диез минор"),
    ("Ми мажор", "До-диез минор"),
    ("Си мажор", "Соль-диез минор"),
    ("Фа мажор", "Ре минор"),
    ("Си-бемоль мажор", "Соль минор"),
    ("Ми-бемоль мажор", "До минор"),
    ("Ля-бемоль мажор", "Фа минор"),
    ("Ре-бемоль мажор", "Си-бемоль минор"),
]

SCALE_TYPES_NATURAL = ["натуральная мажорная", "натуральная минорная"]
SCALE_TYPES_EXOTIC = ["хроматическая", "целотонная", "уменьшенная"]
SCALE_TYPES_ALL = [
    "натуральная мажорная", "натуральная минорная",
    "гармоническая мажорная", "гармоническая минорная",
    "мелодическая мажорная", "мелодическая минорная",
    "хроматическая", "целотонная", "уменьшенная",
]

ARPEGGIO_TRIADS = ["мажорное", "минорное", "увеличенное", "уменьшённое"]
ARPEGGIO_SEVENTH = ["D7", "D65", "D43", "D2", "II7", "VII7"]

# =========================================================
#  БИБЛИОТЕКА — ФАЙЛЫ И ССЫЛКИ
# =========================================================
FILES_THEORY = [
    {
        "name": "!!!Панова_Конспекты по элементарной теории музыки.pdf",
        "title": "Панова — Конспекты по элементарной теории музыки",
        "author": "Н. В. Панова",
        "note": "Краткое и доступное изложение основ теории музыки.",
    },
    {
        "name": "Корсаков В.С. Схемы и таблицы по теории музыки.pdf",
        "title": "Корсаков — Схемы и таблицы по теории музыки",
        "author": "В. С. Корсаков",
        "note": "50 схем — удобно для повторения и как шпаргалка.",
    },
    {
        "name": "Koroleva_Ya_slyshu_znayu_i_poyu.pdf",
        "title": "Королёва — Я слышу, знаю и пою (полная версия)",
        "author": "С. Б. Королёва",
        "note": "Теория музыки с 1 по 7 класс: стихи и картинки.",
    },
    {
        "name": "Королева 1 класс.pdf",
        "title": "Королёва — 1 класс",
        "author": "С. Б. Королёва",
        "note": "Нотная грамота для 1 класса.",
    },
    {
        "name": "Королева 2-3 класс.pdf",
        "title": "Королёва — 2–3 класс",
        "author": "С. Б. Королёва",
        "note": "Лады, интервалы, минор, трезвучия.",
    },
    {
        "name": "Королева 4-5 класс.pdf",
        "title": "Королёва — 4–5 класс",
        "author": "С. Б. Королёва",
        "note": "Септаккорды, тритоны, транспозиция, размер 6/8.",
    },
    {
        "name": "Королева 6-7 класс.pdf",
        "title": "Королёва — 6–7 класс",
        "author": "С. Б. Королёва",
        "note": "Энгармонизм, гармонический мажор, характерные интервалы, родственные тональности.",
    },
    {
        "name": "Королева содержание.pdf",
        "title": "Королёва — Содержание",
        "author": "С. Б. Королёва",
        "note": "Оглавление всех классов.",
    },
    {
        "name": "teoriya_muzyki_v_tablicah.doc",
        "title": "Теория музыки в таблицах",
        "author": "А. Б. Ханова",
        "note": "Краткая формулировка + таблица/схема. Для повторения.",
    },
]

FILES_PRACTICE = [
    {
        "name": "шпаргалки для 1 класса.pdf",
        "title": "Шпаргалки для 1 класса",
        "author": "—",
        "note": "Быстрый справочник по основам нотной грамоты.",
    },
    {
        "name": "Гаммы и арпеджио(пианино).pdf",
        "title": "Гаммы и арпеджио для фортепиано",
        "author": "Н. Ширинская",
        "note": "Все виды гамм и арпеджио по нотам.",
    },
    {
        "name": "Гаммы и арпеджио(скрипка).pdf",
        "title": "Гаммы и арпеджио для скрипки",
        "author": "К. Флеш",
        "note": "Гаммы, арпеджио и двойные ноты.",
    },
    {
        "name": "Произведения на пианино.pdf",
        "title": "Произведения на пианино (Чайковский, «Детский альбом»)",
        "author": "П. И. Чайковский",
        "note": "24 пьесы для игры и разбора.",
    },
]

EXTERNAL_LINKS = [
    {
        "title": "Теория и практика с нуля по классам (ДШИ Нижний Новгород)",
        "url": "https://dshish.nnov.muzkult.ru/Digitallibrary",
        "note": "Полная программа ДМШ/ДШИ — теория и практика по классам.",
    },
    {
        "title": "Пособия для начинающих скрипачей (МСЦ1)",
        "url": "https://msc1.ru/biblioteka/noty-dlja-strunno-smychkovyh-instrumentov/noty-dlja-skripki/posobija-dlja-nachinajushhih-dlja-skripki/",
        "note": "Теория и произведения для скрипки по уровням.",
    },
]

# =========================================================
#  АВТОРИЗАЦИЯ
# =========================================================
def _ensure_users_file():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False)


def _load_users() -> dict:
    _ensure_users_file()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def _save_users(users: dict):
    _ensure_users_file()
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register(username: str, password: str):
    username = username.strip()
    if not username or not password:
        return False, "Имя пользователя и пароль не могут быть пустыми."
    if len(username) < 3:
        return False, "Имя пользователя должно быть не короче 3 символов."
    if len(password) < 4:
        return False, "Пароль должен быть не короче 4 символов."
    users = _load_users()
    if username in users:
        return False, "Такое имя пользователя уже существует."
    users[username] = {
        "password_hash": _hash(password),
        "stats": {"correct": 0, "wrong": 0},
        "wrong_exercises": [],
        "favorites": [],
    }
    _save_users(users)
    return True, f"Пользователь «{username}» успешно зарегистрирован."


def login(username: str, password: str):
    username = username.strip()
    users = _load_users()
    if username not in users:
        return False, "Пользователь не найден."
    if users[username]["password_hash"] != _hash(password):
        return False, "Неверный пароль."
    return True, f"Добро пожаловать, {username}!"


def get_user(username: str) -> dict:
    return _load_users().get(username, {})


def update_user(username: str, updater):
    users = _load_users()
    if username in users:
        updater(users[username])
        _save_users(users)


def add_correct(username: str):
    def upd(u):
        u["stats"]["correct"] = u["stats"].get("correct", 0) + 1
    update_user(username, upd)


def add_wrong(username: str, exercise: dict):
    def upd(u):
        u["stats"]["wrong"] = u["stats"].get("wrong", 0) + 1
        key = (exercise["topic"], exercise["question"])
        if not any((e["topic"], e["question"]) == key for e in u["wrong_exercises"]):
            u["wrong_exercises"].append(exercise)
    update_user(username, upd)


def add_favorite(username: str, exercise: dict):
    def upd(u):
        key = (exercise["topic"], exercise["question"])
        if not any((e["topic"], e["question"]) == key for e in u["favorites"]):
            u["favorites"].append(exercise)
    update_user(username, upd)


def remove_favorite(username: str, exercise: dict):
    def upd(u):
        key = (exercise["topic"], exercise["question"])
        u["favorites"] = [
            e for e in u["favorites"]
            if (e["topic"], e["question"]) != key
        ]
    update_user(username, upd)


def reset_stats(username: str):
    def upd(u):
        u["stats"] = {"correct": 0, "wrong": 0}
        u["wrong_exercises"] = []
    update_user(username, upd)


def get_stats(username: str) -> dict:
    user = get_user(username)
    return user.get("stats", {"correct": 0, "wrong": 0})


def get_wrong_by_topic(username: str) -> dict:
    user = get_user(username)
    result = {}
    for ex in user.get("wrong_exercises", []):
        result.setdefault(ex["topic"], []).append(ex)
    return result


def get_favorites_by_topic(username: str) -> dict:
    user = get_user(username)
    result = {}
    for ex in user.get("favorites", []):
        result.setdefault(ex["topic"], []).append(ex)
    return result


# =========================================================
#  ГЕНЕРАЦИЯ УПРАЖНЕНИЙ
# =========================================================
def gen_interval_from_sound() -> dict:
    note = random.choice(NOTES_RU)
    interval = random.choice(INTERVALS)
    semitones = INTERVAL_SEMITONES[interval]
    return {
        "topic": "интервалы",
        "subtopic": "от звука",
        "question": f"Постройте {interval} вверх от ноты «{note}».",
        "answer": (
            f"{interval} от «{note}» вверх содержит {semitones} полутон(ов). "
            f"Сыграйте его и проверьте себя на слух."
        ),
        "hint": "Проверьте себя на инструменте.",
    }


def gen_interval_in_key() -> dict:
    key, _ = random.choice(BASIC_MAJOR_KEYS)
    step = random.choice(["I", "II", "III", "IV", "V", "VI", "VII"])
    interval = random.choice(
        ["м.2", "б.2", "м.3", "б.3", "ч.4", "ч.5", "м.6", "б.6", "м.7", "б.7"]
    )
    return {
        "topic": "интервалы",
        "subtopic": "в тональности",
        "question": f"Постройте {interval} на {step} ступени тональности «{key}».",
        "answer": (
            f"Проверьте построение на инструменте. "
            f"Помните о ключевых знаках тональности «{key}»."
        ),
        "hint": "Сначала определите все ноты тональности.",
    }


def gen_chord_from_sound(level: str) -> dict:
    note = random.choice(NOTES_RU)
    if level == "Новичок":
        chord = random.choice(TRIADS_BEGINNER)
        return {
            "topic": "аккорды",
            "subtopic": "трезвучие от звука",
            "question": f"Постройте {chord} трезвучие от ноты «{note}».",
            "answer": (
                f"{chord} трезвучие строится по терциям. "
                f"мажор = б.3+м.3; минор = м.3+б.3; "
                f"увеличенное = б.3+б.3; уменьшённое = м.3+м.3."
            ),
            "hint": "Считайте терциями.",
        }
    elif level == "Средний":
        chord = random.choice(TRIAD_INVERSIONS)
        return {
            "topic": "аккорды",
            "subtopic": "обращение трезвучия",
            "question": f"Постройте {chord} от ноты «{note}».",
            "answer": (
                f"{chord} — обращение трезвучия. "
                f"Секстаккорд = терция + кварта; квартсекстаккорд = кварта + терция."
            ),
            "hint": "Помните интервальный состав.",
        }
    else:
        chord = random.choice(SEVENTH_CHORDS)
        return {
            "topic": "аккорды",
            "subtopic": "септаккорд",
            "question": f"Постройте {chord} от ноты «{note}».",
            "answer": (
                f"{chord} — септаккорд (или его обращение). "
                f"D7 = б.3+м.3+м.3; D65 = м.3+м.3+б.2; "
                f"D43 = м.3+б.2+б.3; D2 = б.2+б.3+м.3."
            ),
            "hint": "Считайте интервалы последовательно.",
        }


def gen_chord_in_key() -> dict:
    key, _ = random.choice(BASIC_MAJOR_KEYS)
    step = random.choice(["I", "II", "III", "IV", "V", "VI", "VII"])
    kind = random.choice(["трезвучие", "секстаккорд", "квартсекстаккорд"])
    return {
        "topic": "аккорды",
        "subtopic": "в тональности",
        "question": f"Постройте {kind} на {step} ступени тональности «{key}».",
        "answer": (
            f"Проверьте: {kind} на {step} ступени в «{key}». "
            f"Учтите ключевые знаки."
        ),
        "hint": "Сначала выпишите гамму.",
    }


def _key_signs(key: str) -> int:
    for k, n in BASIC_MAJOR_KEYS + BASIC_MINOR_KEYS:
        if k == key:
            return n
    return 0


def _is_flat_key(key: str) -> bool:
    flat_1 = {"Фа мажор", "Ре минор"}
    flat_2 = {"Си-бемоль мажор", "Соль минор"}
    flat_3 = {"Ми-бемоль мажор", "До минор"}
    flat_4 = {"Ля-бемоль мажор", "Фа минор"}
    flat_5 = {"Ре-бемоль мажор", "Си-бемоль минор"}
    if "бемоль" in key:
        return True
    return key in (flat_1 | flat_2 | flat_3 | flat_4 | flat_5)


def gen_key_signs() -> dict:
    all_keys = BASIC_MAJOR_KEYS + BASIC_MINOR_KEYS
    key, signs = random.choice(all_keys)
    if _is_flat_key(key):
        return {
            "topic": "тональности",
            "subtopic": "знаки при ключе",
            "question": f"Сколько бемолей при ключе в тональности «{key}»?",
            "answer": f"{signs} бемоль(ей)",
            "hint": "Скороговорка: си, ми, ля, ре, соль, до, фа.",
            "correct": str(signs),
        }
    return {
        "topic": "тональности",
        "subtopic": "знаки при ключе",
        "question": f"Сколько диезов при ключе в тональности «{key}»?",
        "answer": f"{signs} диез(ов)",
        "hint": "Скороговорка: фа, до, соль, ре, ля, ми, си.",
        "correct": str(signs),
    }


def gen_parallel_key() -> dict:
    major, minor = random.choice(PARALLEL_KEYS)
    if random.random() < 0.5:
        return {
            "topic": "тональности",
            "subtopic": "параллельная",
            "question": f"Какая тональность параллельна «{major}»?",
            "answer": minor,
            "hint": "Параллельная — на малую терцию вниз от мажора.",
            "correct": minor.lower(),
        }
    return {
        "topic": "тональности",
        "subtopic": "параллельная",
        "question": f"Какая тональность параллельна «{minor}»?",
        "answer": major,
        "hint": "Параллельная — на малую терцию вверх от минора.",
        "correct": major.lower(),
    }


def gen_parallel_and_signs() -> dict:
    major, minor = random.choice(PARALLEL_KEYS)
    signs = _key_signs(major)
    return {
        "topic": "тональности",
        "subtopic": "знаки + параллельная",
        "question": (
            f"Для тональности «{major}»: "
            f"1) сколько знаков при ключе? "
            f"2) какая параллельная тональность?"
        ),
        "answer": f"Знаков: {signs}. Параллельная: {minor}.",
        "hint": (
            "Скороговорки: фа-до-соль-ре-ля-ми-си (диезы); "
            "си-ми-ля-ре-соль-до-фа (бемоли). "
            "Параллельная — на м.3 вниз от мажора."
        ),
        "correct": f"{signs}|{minor.lower()}",
    }


def gen_scale(level: str) -> dict:
    if level == "Новичок":
        scale_type = random.choice(SCALE_TYPES_NATURAL)
    elif level == "Средний":
        scale_type = random.choice(SCALE_TYPES_NATURAL + SCALE_TYPES_EXOTIC)
    else:
        scale_type = random.choice(SCALE_TYPES_ALL)
    key, _ = random.choice(BASIC_MAJOR_KEYS + BASIC_MINOR_KEYS)
    tonic = key.split()[0]
    return {
        "topic": "гаммы",
        "subtopic": scale_type,
        "question": f"Сыграйте {scale_type} гамму от ноты «{tonic}».",
        "answer": (
            f"{scale_type.capitalize()} гамма от «{tonic}». "
            f"Проверьте ключевые знаки тональности «{key}» и играйте медленно."
        ),
        "hint": "Следите за ключевыми знаками.",
    }


def gen_arpeggio(level: str) -> dict:
    note = random.choice(NOTES_RU)
    if level == "Умеющий":
        chord = random.choice(ARPEGGIO_TRIADS)
        return {
            "topic": "арпеджио",
            "subtopic": "трезвучие",
            "question": f"Сыграйте арпеджио {chord} трезвучия от ноты «{note}».",
            "answer": (
                f"Арпеджио {chord} трезвучия от «{note}»: "
                f"играйте по звукам трезвучия вверх и вниз."
            ),
            "hint": "Сначала постройте трезвучие.",
        }
    else:
        chord = random.choice(ARPEGGIO_SEVENTH)
        return {
            "topic": "арпеджио",
            "subtopic": "септаккорд",
            "question": f"Сыграйте арпеджио {chord} от ноты «{note}».",
            "answer": (
                f"Арпеджио {chord} от «{note}»: играйте по звукам септаккорда "
                f"(или его обращения) вверх и вниз."
            ),
            "hint": "Помните интервальный состав.",
        }


def generate_exercise(level: str) -> dict:
    if level == "Новичок":
        categories = ["интервалы", "аккорды", "тональности"]
    elif level == "Средний":
        categories = ["интервалы", "аккорды", "тональности", "гаммы"]
    else:
        categories = ["интервалы", "аккорды", "тональности", "гаммы", "арпеджио"]

    cat = random.choice(categories)

    if cat == "интервалы":
        if level == "Новичок":
            return gen_interval_from_sound()
        return random.choice([gen_interval_from_sound, gen_interval_in_key])()

    if cat == "аккорды":
        if level == "Новичок":
            return gen_chord_from_sound("Новичок")
        if level == "Средний":
            return random.choice([gen_chord_from_sound, gen_chord_in_key])()
        return gen_chord_from_sound(level)

    if cat == "тональности":
        if level == "Новичок":
            return gen_key_signs()
        if level in ("Средний", "Умеющий"):
            return random.choice([gen_key_signs, gen_parallel_key])()
        return random.choice([gen_key_signs, gen_parallel_key, gen_parallel_and_signs])()

    if cat == "гаммы":
        return gen_scale(level)

    if cat == "арпеджио":
        return gen_arpeggio(level)

    return gen_interval_from_sound()


# =========================================================
#  ИНИЦИАЛИЗАЦИЯ СЕССИИ
# =========================================================
def init_state():
    defaults = {
        "username": None,
        "current_page": "home",
        "level": None,
        "current_exercise": None,
        "show_answer": False,
        "text_answer_checked": False,
        "text_answer_correct": None,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


init_state()


# =========================================================
#  СТРАНИЦА: АВТОРИЗАЦИЯ
# =========================================================
def render_auth():
    st.title("🎵 Music Trainer")
    st.caption("Тренажёр музыкальной теории. Регистрация без почты.")

    tab_login, tab_register = st.tabs(["Вход", "Регистрация"])

    with tab_login:
        with st.form("login_form"):
            u = st.text_input("Имя пользователя", key="login_u")
            p = st.text_input("Пароль", type="password", key="login_p")
            submit = st.form_submit_button("Войти", use_container_width=True)
            if submit:
                ok, msg = login(u, p)
                if ok:
                    st.session_state.username = u.strip()
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    with tab_register:
        with st.form("register_form"):
            u = st.text_input("Имя пользователя", key="reg_u")
            p = st.text_input("Пароль", type="password", key="reg_p")
            p2 = st.text_input("Повторите пароль", type="password", key="reg_p2")
            submit = st.form_submit_button("Зарегистрироваться", use_container_width=True)
            if submit:
                if p != p2:
                    st.error("Пароли не совпадают.")
                else:
                    ok, msg = register(u, p)
                    if ok:
                        st.success(msg + " Теперь войдите.")
                    else:
                        st.error(msg)


# =========================================================
#  ШАПКА
# =========================================================
def render_header():
    st.markdown(
        f"<div style='text-align:center; color:#666;'>Пользователь: "
        f"<b>{st.session_state.username}</b></div>",
        unsafe_allow_html=True,
    )
    cols = st.columns([1, 1, 1, 1, 1])
    with cols[0]:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.session_state.current_exercise = None
            st.session_state.show_answer = False
            st.rerun()
    with cols[1]:
        if st.button("📊 Статистика", use_container_width=True):
            st.session_state.current_page = "statistics"
            st.rerun()
    with cols[2]:
        if st.button("⭐ Избранное", use_container_width=True):
            st.session_state.current_page = "favorites"
            st.rerun()
    with cols[3]:
        if st.button("📚 Обучение", use_container_width=True):
            st.session_state.current_page = "library"
            st.rerun()
    with cols[4]:
        if st.button("🚪 Выход", use_container_width=True):
            st.session_state.username = None
            st.session_state.current_page = "home"
            st.rerun()
    st.markdown("---")


# =========================================================
#  СТРАНИЦА: HOME
# =========================================================
def render_home():
    st.title("🎵 Music Trainer")
    st.subheader("Выберите уровень")

    levels = [
        ("Новичок", "Трезвучия от звука, интервалы, базовые тональности.", "🟢"),
        ("Средний", "+ обращения трезвучий, гаммы (натуральные, хроматическая, целотонная, уменьшенная), параллельные тональности.", "🟡"),
        ("Умеющий", "Септаккорды, арпеджио, все виды гамм и тональностей.", "🟠"),
        ("Продвинутый", "Тональности: знаки + параллельная; сложные задания.", "🔴"),
    ]

    for lvl, desc, emoji in levels:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"### {emoji} {lvl}")
                st.caption(desc)
            with c2:
                if st.button("Выбрать", key=f"lvl_{lvl}", use_container_width=True):
                    st.session_state.level = lvl
                    st.session_state.current_page = "exercises"
                    st.session_state.current_exercise = generate_exercise(lvl)
                    st.session_state.show_answer = False
                    st.session_state.text_answer_checked = False
                    st.session_state.text_answer_correct = None
                    st.rerun()


# =========================================================
#  СТРАНИЦА: УПРАЖНЕНИЕ
# =========================================================
def _next_exercise():
    st.session_state.current_exercise = generate_exercise(st.session_state.level)
    st.session_state.show_answer = False
    st.session_state.text_answer_checked = False
    st.session_state.text_answer_correct = None
    st.rerun()


def render_exercise():
    level = st.session_state.level
    if st.session_state.current_exercise is None:
        st.session_state.current_exercise = generate_exercise(level)

    ex = st.session_state.current_exercise

    st.subheader(f"Уровень: {level}")
    st.caption(f"Тема: **{ex['topic']}** — {ex.get('subtopic', '')}")
    st.markdown("---")
    st.markdown(f"### {ex['question']}")

    is_text_input = ex["topic"] == "тональности"

    if is_text_input:
        if not st.session_state.text_answer_checked:
            user_answer = st.text_input(
                "Ваш ответ (число или название тональности):",
                key="text_answer_input_field",
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Проверить", use_container_width=True):
                    if user_answer.strip():
                        correct = ex.get("correct", "").lower()
                        user_norm = user_answer.strip().lower().replace(" ", "")
                        correct_norm = correct.replace(" ", "")
                        ok = user_norm == correct_norm
                        st.session_state.text_answer_correct = ok
                        st.session_state.text_answer_checked = True
                        if ok:
                            add_correct(st.session_state.username)
                        else:
                            add_wrong(st.session_state.username, {
                                "topic": ex["topic"],
                                "question": ex["question"],
                                "answer": ex["answer"],
                            })
                        st.rerun()
            with c2:
                if st.button("Показать ответ", use_container_width=True):
                    st.session_state.show_answer = True
                    st.rerun()

            if st.session_state.show_answer:
                st.info(f"**Правильный ответ:** {ex['answer']}")
                st.caption(f"💡 Подсказка: {ex.get('hint', '')}")
                cc1, cc2 = st.columns(2)
                with cc1:
                    if st.button("✅ Я ответил правильно", use_container_width=True):
                        add_correct(st.session_state.username)
                        _next_exercise()
                with cc2:
                    if st.button("❌ Я ответил неправильно", use_container_width=True):
                        add_wrong(st.session_state.username, {
                            "topic": ex["topic"],
                            "question": ex["question"],
                            "answer": ex["answer"],
                        })
                        _next_exercise()
        else:
            if st.session_state.text_answer_correct:
                st.success("✅ Правильно!")
            else:
                st.error("❌ Неправильно.")
                st.info(f"**Правильный ответ:** {ex['answer']}")
            if st.button("➡️ Следующее упражнение", use_container_width=True):
                _next_exercise()
    else:
        if not st.session_state.show_answer:
            if st.button("Показать ответ/разбор", use_container_width=True):
                st.session_state.show_answer = True
                st.rerun()
        else:
            st.info(f"**Разбор:** {ex['answer']}")
            st.caption(f"💡 {ex.get('hint', '')}")
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button("✅ Правильно", use_container_width=True):
                    add_correct(st.session_state.username)
                    _next_exercise()
            with cc2:
                if st.button("❌ Неправильно", use_container_width=True):
                    add_wrong(st.session_state.username, {
                        "topic": ex["topic"],
                        "question": ex["question"],
                        "answer": ex["answer"],
                    })
                    _next_exercise()

    st.markdown("---")
    if st.button("⭐ Добавить в избранное", use_container_width=True):
        add_favorite(st.session_state.username, {
            "topic": ex["topic"],
            "question": ex["question"],
            "answer": ex["answer"],
        })
        st.success("Добавлено в избранное!")


# =========================================================
#  СТРАНИЦА: СТАТИСТИКА
# =========================================================
def render_statistics():
    st.title("📊 Статистика")
    username = st.session_state.username
    s = get_stats(username)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("✅ Правильных", s.get("correct", 0))
    with c2:
        st.metric("❌ Неправильных", s.get("wrong", 0))

    st.markdown("---")
    st.subheader("Ошибочные задания")

    wrong_by_topic = get_wrong_by_topic(username)
    if not wrong_by_topic:
        st.info("Здесь пока ничего нет — вы ещё не ошибались!")
    else:
        for topic, items in wrong_by_topic.items():
            with st.expander(f"📁 {topic} ({len(items)})"):
                for i, ex in enumerate(items, 1):
                    with st.container(border=True):
                        st.markdown(f"**{i}. {ex['question']}**")
                        st.caption(f"Ответ: {ex['answer']}")

    st.markdown("---")
    if st.button("🗑️ Сбросить статистику", type="secondary"):
        reset_stats(username)
        st.success("Статистика сброшена.")
        st.rerun()


# =========================================================
#  СТРАНИЦА: ИЗБРАННОЕ
# =========================================================
def render_favorites():
    st.title("⭐ Избранное")
    username = st.session_state.username
    fav_by_topic = get_favorites_by_topic(username)

    if not fav_by_topic:
        st.info("Здесь пока ничего нет.")
        return

    for topic, items in fav_by_topic.items():
        with st.expander(f"📁 {topic} ({len(items)})", expanded=False):
            for i, ex in enumerate(items, 1):
                with st.container(border=True):
                    st.markdown(f"**{i}. {ex['question']}**")
                    st.caption(f"Ответ: {ex['answer']}")
                    if st.button("Удалить из избранного", key=f"del_{topic}_{i}"):
                        remove_favorite(username, ex)
                        st.rerun()


# =========================================================
#  СТРАНИЦА: БИБЛИОТЕКА
# =========================================================
def _file_available(filename: str) -> bool:
    return os.path.isfile(os.path.join(LIBRARY_DIR, filename))


def _file_path(filename: str) -> str:
    return os.path.join(LIBRARY_DIR, filename)


def render_library():
    st.title("📚 Библиотека")
    st.caption("Теория, практика и полезные ссылки.")

    st.subheader("🌐 Полезные ссылки")
    for link in EXTERNAL_LINKS:
        with st.container(border=True):
            st.markdown(f"**[{link['title']}]({link['url']})**")
            st.caption(link["note"])

    st.markdown("---")
    st.subheader("📖 Теория")
    st.caption("Нажмите «Скачать», если файл загружен в папку `library/`.")

    for f in FILES_THEORY:
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{f['title']}**")
                st.caption(f"{f['author']} — {f['note']}")
            with c2:
                if _file_available(f["name"]):
                    with open(_file_path(f["name"]), "rb") as fp:
                        st.download_button(
                            "📥 Скачать",
                            fp.read(),
                            file_name=f["name"],
                            key=f"dl_theory_{f['name']}",
                            use_container_width=True,
                        )
                else:
                    st.caption("⏳ Не загружен")

    st.markdown("---")
    st.subheader("🎼 Практика")
    for f in FILES_PRACTICE:
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{f['title']}**")
                st.caption(f"{f['author']} — {f['note']}")
            with c2:
                if _file_available(f["name"]):
                    with open(_file_path(f["name"]), "rb") as fp:
                        st.download_button(
                            "📥 Скачать",
                            fp.read(),
                            file_name=f["name"],
                            key=f"dl_practice_{f['name']}",
                            use_container_width=True,
                        )
                else:
                    st.caption("⏳ Не загружен")


# =========================================================
#  ГЛАВНЫЙ РОУТЕР
# =========================================================
if st.session_state.username is None:
    render_auth()
else:
    render_header()
    page = st.session_state.current_page

    if page == "home":
        render_home()
    elif page == "exercises":
        render_exercise()
    elif page == "statistics":
        render_statistics()
    elif page == "favorites":
        render_favorites()
    elif page == "library":
        render_library()
