import csv
import json
from pathlib import Path
import logging
from collections.abc import Generator, Sequence, Callable

from pydantic import ValidationError

from streamstats.errors import EmptyFieldError, FormatFieldError, HeaderFieldError, StreamStatsError
from streamstats.models import LineLogs, validate_header, validate_time

logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s"
    )
logger = logging.getLogger(__name__)


def parsers_file_csv(name_file: Path, skip_invalid: bool) -> Generator[LineLogs, None, None]:
    """
    Функция парсит файл типа csv
    Args:
        file - имя файла, примеры: test.csv, test.json
    Returns:
        None
    Raises:
        HeaderFieldError - заголовки отсутствуют или написаны не правильно
    """
    with open(name_file, mode="r", encoding="utf8") as rfile:
        t: str; l: str; s: str; m: str

        reader: csv.DictReader[str] = csv.DictReader(rfile)
        headlines: Sequence[str] | None = reader.fieldnames

        # Проверяет заголовки
        try:
            validate_header(headlines)
        except ValueError:
            if skip_invalid:
                logger.warning(f"Режим --skip-invalid: пропущен файл {name_file}: некорректный")
                return False
            else:
                raise

        t, l, s, m = headlines
        for i, line in enumerate(reader, start=2):
            try:
                yield LineLogs(
                    timestamp=validate_time(line[t]),
                    level=line[l],
                    source=line[s],
                    message=line[m]
                )
            except (ValueError, ValidationError, KeyError, StreamStatsError) as err:
                if skip_invalid:
                    logger.warning(f"Решим --skip-invalid: пропущена строка {i} в файле {name_file}: {err}")


def parser_file_jsonl(name_file: Path, skip_invalid: bool) -> Generator[LineLogs, None, None]:
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
        for i, line in enumerate(rfile, start=1):
            try:
                if not line.strip():
                    raise HeaderFieldError(f"Строка {i} пустая.")

                data = json.loads(line)
                if not isinstance(data, dict):
                    raise HeaderFieldError(f"Строка {i} не является JSON-объектом")

                headlines = list(data.keys())
                validate_header(headlines)

                t, l, s, m = headlines
                yield  LineLogs(
                    timestamp=validate_time(data[t]),
                    level=data[l],
                    source=data[s],
                    message=data[m]
                )
            except (json.JSONDecodeError, ValueError, ValidationError, KeyError, HeaderFieldError, StreamStatsError) as err:
                if skip_invalid:
                    logger.warning(f"Режим --skip-invalid: пропущена строка {i} в файле {name_file}: {err}")
                    yield False
                else:
                    raise


def entry_point_for_file_parsers(file: Path, format: str, skip_invalid: bool) -> Generator[LineLogs, None, None]:
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
    def_func: dict[str, Callable[[str], Generator[LineLogs, None, None]]] = {
        "csv": parsers_file_csv,
        "jsonl": parser_file_jsonl
    }

    if file.stat().st_size == 0:  # Ошибка выпадает если файл пустой
        raise EmptyFieldError

    if format not in def_func:  # Ошибка выпадает если неправильный формат файла
        raise FormatFieldError()

    my_generator: Generator[LineLogs, None, None] = def_func[format](file, skip_invalid)

    yield from my_generator
