class LineLogs:
    """Находиться информация об одной строке лога"""
    def __init__(self, timestamp: str, level: str, source: str, message: str):
        self.timestamp: str = timestamp
        self.level: str = level
        self.source: str = source
        self.message: str = message


class CounterSource:
    """Хранит информацию об источнике"""
    def __init__(self):
        self.all_event: int = 0
        self.debug: int = 0
        self.info: int = 0
        self.warning: int = 0
        self.error: int = 0
        self.critical: int = 0


class ResultStatistic:
    """Хранит статистику которую нужно будет записать в файл JSON b CSV"""
    def __init__(self):
        # Имя файла
        self.name: str | None = None
        # Отчетность по общему количеству событий
        self.all_event: int = 0
        # Отчетность по общему количеству событий для каждого level
        self.debug: int = 0
        self.info: int = 0
        self.warning: int = 0
        self.error: int = 0
        self.critical: int = 0
        # Отчетность по общему количеству событий для каждого source
        self.counter_source = {}
        # Первая и последняя временная метка
        self.start_time: str | None = None
        self.end_time: str | None = None
        # top-5 источников ошибок уровня ERROR/CRITICAL
        self.top_five_source: list | list[tuple[str, int]] = []