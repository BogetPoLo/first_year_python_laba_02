from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Sequence
from pydantic import BaseModel, Field, TypeAdapter

from streamstats.errors import HeaderFieldError, InvalidTimestampError


class LineLogs(BaseModel):
    """Находиться информация об одной строке лога"""
    timestamp: datetime  # Временная точка
    level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL"
    ]  # Тип ошибка
    source: str = Field(min_length=1)  # Источник
    message: str  # Сообщение


@dataclass
class CounterSource:
    """Хранит информацию об источнике"""
    # Временная точка
    timestamp: list[datetime] | None = None
    # Сообщение
    message: list[str] | None = None
    # Количество встретившихся level
    all_event: int = 0
    # Типы ошибок
    debug: int = 0
    info: int = 0
    warning: int = 0
    error: int = 0
    critical: int = 0


@dataclass
class ResultStatistic:
    """Хранит статистику которую нужно будет записать в файл JSON b CSV"""
    # Отчетность по общему количеству событий для каждого source
    counter_source: dict[str, CounterSource] | dict
    # top-5 источников ошибок уровня ERROR/CRITICAL
    top_five_source: dict | dict[int, tuple[int, int, str]]
    # Имя файла
    name: str | None = None
    format: str | None = None
    # Отчетность по общему количеству событий
    all_level: int = 0
    # Типы ошибок
    debug: int = 0
    info: int = 0
    warning: int = 0
    error: int = 0
    critical: int = 0
    # Первая и последняя временная метка
    start_time: str | datetime | None = None
    end_time: str | datetime | None = None
    skip_lines: int = 0


def validate_header(header: Sequence[str] | None) -> bool:
    """Валидирует заголовки файла csv/jsonl
    Args:
        header = заголовки
    Returns:
        True - если функция выполнилась
    Raises:
        ValueError("Заголовков меньше 4. Должны быть: timestamp, level, source, message")
        """
    validate_header_str = TypeAdapter(Literal["timestamp", "level", "source", "message"])
    if header == None or len(header) != 4:
        raise HeaderFieldError("Заголовков меньше 4. Должны быть: timestamp, level, source, message")
    for head in header:
        validate_header_str.validate_python(head)
    return True


def validate_time(str_time: str) -> datetime:
    """Валидирует строку, а так же переводит строку в тип данных datetime
    Args:
        str_time - строка записанная как временная метка
    Returns:
        True - если функция выполнилась
        """
    try:
        return datetime.fromisoformat(str_time)
    except (ValueError, TypeError) as err:
        raise InvalidTimestampError(f"Неверная временная метка")
