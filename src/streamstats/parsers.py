import csv
import json
import os

from collections.abc import Generator, Sequence, Callable
from errors import HeaderFieldError, EmptyFieldError, FormatFieldError
from src.streamstats.models import LineLogs


def check_headlines(headlines: Sequence[str] | None) -> bool:
    """Проверяет заголовки файла
    Args:
        t, l, s, m - заголовки
    Returns:
        True - заголовки соответствуют
        False - в остальных случаях
    """
    match headlines:
        case ["timestamp", "level", "source", "message"]:
            return True
        case _:
            return False


def parsers_file_csv(name_file: str) -> Generator[LineLogs, None, None]:
    """
    Функция парсит файл типа csv
    Args:
        name_file - имя файла, примеры: test.csv, test.json
    Returns:
        None
    Raises:
        HeaderFieldError - заголовки отсутствуют или написаны не правильно
    """
    with open(name_file, mode="r", encoding="utf8") as rfile:
        t: str; l: str; s: str; m: str

        reader: csv.DictReader[str] = csv.DictReader(rfile)
        headlines: Sequence[str] | None = reader.fieldnames

        if not check_headlines(headlines):
            raise HeaderFieldError
        t, l, s, m = headlines

        for line in reader:
            yield LineLogs(
                timestamp=line[t],
                level=line[l],
                source=line[s],
                message=line[m]
            )


def parser_file_jsonl(name_file: str) -> Generator[LineLogs, None, None]:
    """
    Функция парсит файл типа json
    Args:
        name_file - имя файла, примеры: test.csv, test.json
    Returns:
        None
    Raises:
        HeaderFieldError - заголовки отсутствуют или написаны не правильно
    """
    with open(name_file, mode="r", encoding="utf8") as rfile:
        t: str; l: str; s: str; m: str

        for line in rfile:
            if not line.strip():
                continue
            line: dict[str, str] = json.loads(line)

            headlines: Sequence[str] | None = list(line.keys())

            if not check_headlines(headlines):
                raise HeaderFieldError
            t, l, s, m = headlines

            yield LineLogs(
                timestamp=line[t],
                level=line[l],
                source=line[s],
                message=line[m]
            )


def entry_point_for_file_parsers(name_file: str, format: str) -> Generator[LineLogs, None, None]:
    """
    Входная точка для парсинга файла
    Args:
        name_file - имя файла, примеры: test.csv, test.json
        format - вводимый формат файла, пример: csv, json
    Returns:
        None
    Raises:
        EmptyFieldError - файл пустой
        FormatFieldError - неправильный формат
    """
    if os.stat(name_file).st_size == 0:  # Ошибка выпадает если файл пустой
        raise EmptyFieldError

    def_func: dict[str, Callable[[str], Generator[LineLogs, None, None]]] = {
        "csv": parsers_file_csv,
        "jsonl": parser_file_jsonl
    }

    if format not in def_func:  # Ошибка выпадает если неправильный формат файла
        raise FormatFieldError()

    my_generator: Generator[LineLogs, None, None] = def_func[format](name_file)

    yield from my_generator
