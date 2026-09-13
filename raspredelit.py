import os
import re
import json
import shutil
import platform
import subprocess
import time
from collections import Counter

# ==== КУДА КОПИРОВАТЬ НАЙДЕННОЕ ====
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Found_Models")

# ==== ФАЙЛ ИСТОРИИ ПОИСКОВ ====
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "search_history.json")

# ==== РАСШИРЕНИЯ 3D-МОДЕЛЕЙ ====
MODEL_EXTENSIONS = (
    ".stl", ".obj", ".off", ".ply", ".3ds", ".dae", ".x3d", ".x3db",
    ".wrl", ".vrml", ".step", ".stp", ".iges", ".igs",
    ".fbx", ".blend", ".gltf", ".glb", ".max", ".ma", ".mb",
    ".c4d", ".lwo", ".lws", ".abc", ".usd", ".usda", ".usdc", ".usdz",
    ".sat", ".sab", ".3dm", ".3mf",
    ".gcode", ".amf", ".md2", ".md3", ".ms3d", ".b3d",
)

# ==== ГДЕ ИСКАТЬ ====
user_home = os.path.expanduser("~")

CANDIDATE_FOLDERS = [
    os.path.dirname(os.path.abspath(__file__)),
    user_home,
]

POPULAR_SUBFOLDERS = [
    "Pictures", "Изображения", "Images",
    "Downloads", "Загрузки",
    "Desktop", "Рабочий стол",
    "Documents", "Документы",
    "3D", "Models", "Модели", "3DModels",
    "STL", "OBJ", "OFF", "Prints", "Для печати",
]

for name in POPULAR_SUBFOLDERS:
    path = os.path.join(user_home, name)
    if os.path.isdir(path):
        CANDIDATE_FOLDERS.append(path)


# =========================================================
#   ИСТОРИЯ
# =========================================================

def load_history() -> dict:
    if not os.path.isfile(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_history(history: dict):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f" Не удалось сохранить историю: {e}")


def open_in_explorer(path: str):
    if not os.path.isdir(path):
        print(f" Папка не существует: {path}")
        return
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        print(f" Открываю проводник: {path}")
    except Exception as e:
        print(f" Не удалось открыть проводник: {e}")


# =========================================================
#   СКАНИРОВАНИЕ
# =========================================================

def is_model_file(filename: str) -> bool:
    return filename.lower().endswith(MODEL_EXTENSIONS)


def scan_all_models():
    found = []
    visited = set()
    output_abs = os.path.abspath(OUTPUT_DIR).lower()

    for folder in CANDIDATE_FOLDERS:
        folder = os.path.abspath(folder)
        if not os.path.isdir(folder) or folder in visited:
            continue
        visited.add(folder)

        print(f" Сканирую: {folder}")
        for root, dirs, files in os.walk(folder):
            dirs[:] = [
                d for d in dirs
                if not d.startswith(".")
                and d.lower() not in {
                    "appdata", "application data", "windows", "$recycle.bin",
                    "system volume information", "node_modules", "__pycache__",
                    "programdata", "temp", "tmp",
                }
                and not os.path.abspath(os.path.join(root, d)).lower().startswith(output_abs)
            ]

            if os.path.abspath(root).lower().startswith(output_abs):
                continue

            for f in files:
                if is_model_file(f):
                    found.append(os.path.join(root, f))

    return found


# =========================================================
#   ДЕДУПЛИКАЦИЯ
# =========================================================

def normalize_name(filename: str) -> str:
    name = os.path.splitext(filename)[0].lower().strip()
    name = re.sub(r"\s+(copy|копия)(\s*\d+)?$", "", name)
    name = re.sub(r"[\s_\-]*[\(\[\{]\s*\d+\s*[\)\]\}]\s*$", "", name)

    while True:
        new_name = re.sub(r"[\s_\-]+v?\d+$", "", name)
        if new_name == name:
            break
        name = new_name

    name = re.sub(r"[\s_\-]+", "_", name).strip("_")
    return name or "unnamed"


def deduplicate(files):
    groups = {}
    for path in files:
        key = normalize_name(os.path.basename(path))
        groups.setdefault(key, []).append(path)

    unique = []
    for key, group in groups.items():
        group.sort(key=lambda p: (
            len(os.path.basename(p)),
            -os.path.getsize(p) if os.path.isfile(p) else 0,
        ))
        unique.append(group[0])

    return unique, groups


# =========================================================
#   КОПИРОВАНИЕ
# =========================================================

def copy_to_output(files, query: str):
    safe_name = "".join(c for c in query if c.isalnum() or c in " _-").strip()
    target_dir = os.path.join(OUTPUT_DIR, safe_name or "result")
    os.makedirs(target_dir, exist_ok=True)
    target_abs = os.path.abspath(target_dir).lower()

    copied = 0
    for src in files:
        if os.path.abspath(src).lower().startswith(target_abs):
            print(f"   Уже в целевой папке: {os.path.basename(src)}")
            continue

        dst = os.path.join(target_dir, os.path.basename(src))
        base, ext = os.path.splitext(dst)
        counter = 1
        while os.path.exists(dst):
            dst = f"{base}_{counter}{ext}"
            counter += 1

        try:
            shutil.copy2(src, dst)
            print(f"  {os.path.basename(src)}")
            copied += 1
        except Exception as e:
            print(f"   Не удалось скопировать {src}: {e}")

    return target_dir, copied


# =========================================================
#   MAIN
# =========================================================

def main():
    print("=" * 60)
    print(" Умный поиск 3D-моделей")
    print(f" ОС: {platform.system()}")
    print(f" Домашняя папка: {user_home}")
    print(f" Папка вывода: {OUTPUT_DIR}")
    print(f" Форматов: {len(MODEL_EXTENSIONS)}")
    print("=" * 60)

    # ==== 1. ИСТОРИЯ ====
    history = load_history()
    if history:
        print(f"\n История поисков: {len(history)} записей")
        for q, info in history.items():
            folder = info.get("folder", "?")
            when = info.get("time", "?")
            print(f"   • '{q}' → {folder}  ({when})")
    else:
        print("\n История поисков пуста.")

    # ==== 2. СКАНИРОВАНИЕ (ДО ввода запроса) ====
    print("\n" + "─" * 60)
    print(" Сканирую компьютер на 3D-модели...")
    print("─" * 60)

    start = time.time()
    all_models = scan_all_models()
    elapsed = time.time() - start

    if not all_models:
        print("\n Ни одной 3D-модели не найдено на компьютере.")
        return

    ext_counter = Counter(os.path.splitext(p)[1].lower() for p in all_models)

    print("\n" + "─" * 60)
    print(f" Найдено моделей: {len(all_models)}  (за {elapsed:.1f} сек)")
    print(" По форматам:")
    for ext, count in ext_counter.most_common():
        print(f"   {ext:8} — {count}")
    print("─" * 60)

    # ==== 3. ВВОД ЗАПРОСА ====
    query = input("\n Введи название модели для поиска: ").strip().lower()
    if not query:
        print(" Пустой запрос.")
        return

    # ==== 4. ПРОВЕРКА ИСТОРИИ ПО КОНКРЕТНОМУ ЗАПРОСУ ====
    if query in history:
        info = history[query]
        old_folder = info.get("folder", "")
        print(f"\n Ты уже искал '{query}' ранее!")
        print(f"   Папка: {old_folder}")

        if os.path.isdir(old_folder):
            print("  Открываю её...")
            open_in_explorer(old_folder)
            again = input("\n Искать заново? (y/N): ").strip().lower()
            if again not in ("y", "yes", "д", "да"):
                print(' Готово.')
                return
        else:
            print("    Папка удалена — ищу заново.")

    # ==== 5. ФИЛЬТР ====
    matched = [p for p in all_models if query in os.path.basename(p).lower()]
    if not matched:
        print(f"\n По запросу '{query}' ничего не найдено.")
        return

    print(f"\n Совпадений до дедупликации: {len(matched)}")

    # ==== 6. ДЕДУПЛИКАЦИЯ ====
    unique, groups = deduplicate(matched)
    dupes_count = len(matched) - len(unique)

    if dupes_count > 0:
        print(f" После дедупликации: {len(unique)} (убрано дубликатов: {dupes_count})")
        for key, group in groups.items():
            if len(group) > 1:
                print(f"   • '{key}': {len(group)} → 1 (взял: {os.path.basename(group[0])})")

    print("\n Что будет скопировано:")
    for p in unique:
        print(f"    {p}")

    # ==== 7. КОПИРОВАНИЕ ====
    target_dir, count = copy_to_output(unique, query)
    print(f"\n Готово! Скопировано {count} файлов в:\n   {target_dir}")

    # ==== 8. ИСТОРИЯ ====
    history[query] = {
        "folder": target_dir,
        "found": count,
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_history(history)

    # ==== 9. ПРОВОДНИК ====
    open_in_explorer(target_dir)


if __name__ == "__main__":
    main()