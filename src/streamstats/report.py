from pathlib import Path
from dataclasses import asdict
import json

from streamstats.models import ResultStatistic


def make_name_file(pref_f: str, count_f: int, name_f: str, type_f: str) -> Path:
    """Формирует имя файла
    Args:
        pref_f - какой тип файла.
            all_statistic_files - статистика со всех файлов
            statistic_file - статистика с одного файла
        count_f - если имен повторяются
        name_f - имя файла
        type_f - тип фала
    Returns:
        Path
            """
    while True:
        name_file: Path = Path(f"{pref_f}_{count_f}_{name_f}{type_f}")
        if not name_file.is_file():
            return name_file
        count_f += 1


def write_json_file(name: Path, obj_d: list[dict] | dict) -> None:
    """Записывает файл
    Args:
        name - имя
        obj_d - данные, которые нужно записать
    Returns:
        None"""
    with open(name, mode="w", encoding="utf8") as j_wfile:
        json.dump(
            obj_d,
            j_wfile,
            ensure_ascii=False,
            indent=4
        )


def start_make_files(all_object: list[ResultStatistic], output_f: str) -> None:
    """Входная точка для записи файлов
    Args:
        all_object - все объекты с данными
        output_f - имя файла
    Returns:
        None"""
    file_path: Path = Path(output_f)
    name_f: str = file_path.stem if file_path.stem else "report"

    all_statistic_files_json: Path = make_name_file(
        "all_statistic_files",
        0,
        name_f,
        ".json")

    write_json_file(all_statistic_files_json, [asdict(ob) for ob in all_object])

    for ob in all_object:
        statistic_file = make_name_file(
            "statistic_file",
            0,
            name_f,
            ".json"
        )
        write_json_file(statistic_file, asdict(ob))
