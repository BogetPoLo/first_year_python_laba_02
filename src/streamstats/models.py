from dataclasses import dataclass


@dataclass
class LineLogs:
    """Находиться информация об одной строке лога"""
    timestamp: str  # Временная точка
    level: str  # Тип ошибка
    source: str  # Источник
    message: str  # Сообщение


@dataclass
class CounterSource:
    """Хранит информацию об источнике"""
    all_event: int  # Количество встретившихся level
    # Типы ошибок
    debug: int
    info: int
    warning: int
    error: int
    critical: int


class ResultStatistic:
    """Хранит статистику которую нужно будет записать в файл JSON b CSV"""
    # Имя файла
    name: str | None
    # Отчетность по общему количеству событий
    all_event: int
    # Типы ошибок
    debug: int
    info: int
    warning: int
    error: int
    critical: int
    # Отчетность по общему количеству событий для каждого source
    counter_source: CounterSource
    # Первая и последняя временная метка
    start_time: str | None
    end_time: str | None
    # top-5 источников ошибок уровня ERROR/CRITICAL
    top_five_source: list | list[tuple[str, int]]