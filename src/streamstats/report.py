from src.streamstats.analysis import entry_point_for_file_analysis
from src.streamstats.models import ResultStatistic
from dataclasses import asdict
from typing import Any
from pathlib import Path
from json import dump


def write_files(name_file):
    name: str; formatt: str
    name, formatt = name_file.split(".")

    result_statistic: ResultStatistic = entry_point_for_file_analysis(name_file, name, formatt)
    name_statistics: str = f"{name}_statistics.json"

    count_file: int = 0
    file_path: Path = Path(name_statistics)
    if file_path.exists() or file_path.is_file():
        while file_path.exists() or file_path.is_file():
            name_statistics = f"{name}_statistics_{count_file}.json"
            file_path = Path(name_statistics)
            count_file += 1

    # Записывает файл со статистикой, только по этому файлу
    with open(name_statistics, mode="w", encoding="utf8") as wfile:
        result_dict: dict[str, Any] = asdict(result_statistic)
        dump(result_dict, wfile, indent=4, ensure_ascii=False)


write_files("logs.jsonl")