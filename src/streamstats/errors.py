class StreamStatsError(Exception):
    pass


class HeaderFieldError(StreamStatsError):
    """Ошибка для пустых заголовочных полей или пустых"""
    def __init__(self, mess="Заголовочные поля отсутствуют или написаны не правильно."):
        super().__init__(mess)


class EmptyFieldError(StreamStatsError):
    """Ошибка для пустого файла"""
    def __init__(self, mess="Файл пустой."):
        super().__init__(mess)


class FormatFieldError(StreamStatsError):
    """Ошибка для неправильного формата файла"""
    def __init__(self, mess="Неправильный формат фала."):
        super().__init__(mess)