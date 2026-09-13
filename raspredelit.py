import os
import shutil
import platform
import time

# ==== КУДА КОПИРОВАТЬ НАЙДЕННОЕ ====
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Found_Models")

# ==== РАСШИРЕНИЯ 3D-МОДЕЛЕЙ ====
MODEL_EXTENSIONS = (
    # Универсальные / обменные
    ".stl", ".obj", ".off", ".ply", ".3ds", ".dae", ".x3d", ".x3db",
    ".wrl", ".vrml", ".step", ".stp", ".iges", ".igs",
    # Игровые / DCC
    ".fbx", ".blend", ".gltf", ".glb", ".max", ".ma", ".mb",
    ".c4d", ".lwo", ".lws", ".abc", ".usd", ".usda", ".usdc", ".usdz",
    # CAD
    ".stp", ".step", ".sat", ".sab", ".3dm", ".3mf",
    # Специализированные
    ".gcode", ".amf", ".md2", ".md3", ".ms3d", ".b3d",
)

# ==== ГДЕ ИСКАТЬ ====
user_home = os.path.expanduser("~")

CANDIDATE_FOLDERS = [
    # Папка, где лежит сам скрипт
    os.path.dirname(os.path.abspath(__file__)),
    # Домашняя папка целиком (обходим рекурсивно)
    user_home,
]

# Явно добавим популярные подпапки (на случай, если родитель не обходится)
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


def is_model_file(filename: str) -> bool:
    """Регистронезависимая проверка расширения."""
    return filename.lower().endswith(MODEL_EXTENSIONS)


def scan_all_models():
    """Рекурсивно обходит все папки-кандидаты, возвращает список полных путей."""
    found = []
    visited = set()   # чтобы не обходить одну и ту же папку дважды

    for folder in CANDIDATE_FOLDERS:
        folder = os.path.abspath(folder)
        if not os.path.isdir(folder):
            continue
        if folder in visited:
            continue
        visited.add(folder)

        print(f"Сканирую: {folder}")
        for root, dirs, files in os.walk(folder):
            # Пропускаем системные/скрытые папки, где моделей точно нет
            dirs[:] = [d for d in dirs if not d.startswith(".") and d.lower() not in {
                "appdata", "application data", "windows", "$recycle.bin",
                "system volume information", "node_modules", "__pycache__",
                "programdata", "temp", "tmp",
            }]
            for f in files:
                if is_model_file(f):
                    found.append(os.path.join(root, f))

    return found


def copy_to_output(files, query: str):
    """Копирует найденные файлы в папку с именем запроса."""
    safe_name = "".join(c for c in query if c.isalnum() or c in " _-").strip()
    target_dir = os.path.join(OUTPUT_DIR, safe_name or "result")
    os.makedirs(target_dir, exist_ok=True)

    copied = 0
    for src in files:
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
            print(f"  Не удалось скопировать {src}: {e}")

    return target_dir, copied


def main():
    print("=" * 60)
    print(" Универсальный поиск 3D-моделей")
    print(f" ОС: {platform.system()}")
    print(f" Домашняя папка: {user_home}")
    print(f" Форматов: {len(MODEL_EXTENSIONS)} (включая .stl, .obj, .off, ...)")
    print("=" * 60)

    start = time.time()
    all_models = scan_all_models()
    elapsed = time.time() - start

    if not all_models:
        print("\n Ни одной 3D-модели не найдено.")
        print(" Проверь вручную, где лежит файл, и добавь путь вручную:")
        print('   CANDIDATE_FOLDERS.append(r"C:\\путь\\до\\папки")')
        return

    # Показать статистику по расширениям
    from collections import Counter
    ext_counter = Counter(os.path.splitext(p)[1].lower() for p in all_models)

    print(f"\n Найдено моделей: {len(all_models)} (за {elapsed:.1f} сек)")
    print("По форматам:")
    for ext, count in ext_counter.most_common():
        print(f"   {ext:8} — {count}")

    # Спросить запрос
    query = input("\n Введи название модели (часть имени, напр. 'skull' или 'череп'): ").strip().lower()
    if not query:
        print(" Пустой запрос.")
        return

    matched = [p for p in all_models if query in os.path.basename(p).lower()]

    if not matched:
        print(f"\n По запросу '{query}' ничего не найдено.")
        print(" Подсказка: можно ввести просто расширение, например '.off'")
        return

    print(f"\n Совпадений: {len(matched)}")
    for p in matched:
        print(f"   {p}")

    # Копируем
    target_dir, count = copy_to_output(matched, query)
    print(f"\n Готово! Скопировано {count} файлов в:\n   {target_dir}")


if __name__ == "__main__":
    main()