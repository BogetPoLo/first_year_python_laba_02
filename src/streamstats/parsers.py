import csv
import json
import os
from collections.abc import Generator, Sequence
from errors import HeaderFieldError, EmptyFieldError


def parsers_file_csv(name_file: str) -> Generator[tuple[str, str, str, str], None, None]:
    """
    Функция парсит файл типа csv
    Args:
        name_file - имя файла, примеры: test.csv, test.json
    Returns:
        None
    """
    with open(name_file, mode="r", encoding="utf8") as rfile:
        timestamp: str
        level: str
        source: str
        message: str

        reader: csv.DictReader[str] = csv.DictReader(rfile)
        headlines: Sequence[str] | None = reader.fieldnames

        if headlines == []:  # Ошибка выпадает, кода нет заголовка
            raise HeaderFieldError()

        timestamp, level, source, message = headlines

        for line in reader:
            yield (line[timestamp], line[level], line[source], line[message])

def parser_file_jsonl(name_file: str) -> Generator[tuple[str, str, str, str], None, None]:
    """
    Функция парсит файл типа json
    Args:
        name_file - имя файла, примеры: test.csv, test.json
    Returns:
        None
    """

    with open(name_file, mode="r", encoding="utf8") as rfile:
        timestamp: str
        level: str
        source: str
        message: str

        for line in rfile:
            if not line.strip():
                continue
            row = json.loads(line)
            timestamp, level, source, message = row.keys()
            yield (row[timestamp], row[level], row[source], row[message])


def entry_point_for_file_parsers(name_file: str, format: str):
    """
    Входная точка для парсинга файла
    Args:
        name_file - имя файла, примеры: test.csv, test.json
        format - вводимый формат файла, пример: csv, json
    Returns:
        None
    """
    if os.stat(name_file).st_size == 0:  # Ошибка выпадает если файл пустой
        raise EmptyFieldError

    def_func = {
        "csv": parsers_file_csv,
        "jsonl": parser_file_jsonl
    }

    my_generator = def_func[format](name_file)

    yield from my_generator


# # !! для тестов !!
# for name in (("logs.csv", "csv"), ("logs.jsonl", "jsonl")):
#     my_generator = entry_point_for_file_parsers(*name)
#     for i in my_generator:
#         print(i)
#     print("----------------------------")