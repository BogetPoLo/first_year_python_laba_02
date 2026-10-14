class StreamStatsError(Exception):
    pass


class HeaderFieldError(StreamStatsError):
    def __init__(self, mess="Заголовочные поля в csv файле пустые."):
        super().__init__(mess)


class EmptyFieldError(StreamStatsError):
    def __init__(self, mess="Файл пустой."):
        super().__init__(mess)