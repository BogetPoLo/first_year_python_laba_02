class StreamStatsError(Exception):
    """Основной класс для всех остальных"""
    pass


class HeaderFieldError(StreamStatsError, ValueError):
    """Ошибка для пустых заголовочных полей или пустых"""
    pass


class EmptyFieldError(StreamStatsError):
    """Ошибка для пустого файла"""
    pass


class InvalidTimestampError(StreamStatsError):
    """Ошибка для не верной временной метки"""
    pass


class FormatFieldError(StreamStatsError):
    """Ошибка для неправильного формата файла"""
    pass