from dataclasses import dataclass


@dataclass
class LineLogs:
    """Находиться информация об одной строке лога"""
    timestamp: str = 0  # Временная точка
    level: str = 0  # Тип ошибка
    source: str = 0  # Источник
    message: str = 0  # Сообщение


@dataclass
class CounterSource:
    """Хранит информацию об источнике"""
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
    formatt: str | None = None
    # Отчетность по общему количеству событий
    all_level: int = 0
    # Типы ошибок
    debug: int = 0
    info: int = 0
    warning: int = 0
    error: int = 0
    critical: int = 0
    # Первая и последняя временная метка
    start_time: str | None = None
    end_time: str | None = None