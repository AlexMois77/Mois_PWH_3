"""
Завдання: Сортування файлів у папці.
Копіювати файли із зазначеної папки та покласти в нову папку з розширенням цього файлу.
"""

import argparse
from pathlib import Path
from shutil import copyfile
import threading
from threading import Thread
from datetime import datetime
import logging

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())

source = Path(args.get("source"))
output_folder = Path(args.get("output"))

folders = []


def read_folder(path: Path) -> None:
    for element in path.iterdir():
        if element.is_dir():  #  перевіряємо чи елемент є папкою
            threading.Thread(
                target=read_folder(element)
            ).start()  # Рекурсивно викликаємо функцію з новим шляхом
        else:  # Тоді це файл
            folders.append(element)
            # copy_file(element)  # Функція для копіювання файлів


def copy_file(file: Path) -> None:
    ext = file.suffix[1:]  # Отримуємо розширення з файлів: .JPG, .PNG, .SVG, etc. та зрізаємо крапку
    new_path = output_folder / ext  # Будуємо новий шляхз назвою з розширення файлу
    new_path.mkdir(parents=True, exist_ok=True)  # Створюємо папку за новим шляхом
    copyfile(file, new_path / file.name)  # Копіюємо файл


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    start = datetime.now()
    read_folder(source)

    threads = []
    for folder in folders:
        th = Thread(target=copy_file, name=f"Thread{folder}", args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    logging.info(datetime.now() - start)
