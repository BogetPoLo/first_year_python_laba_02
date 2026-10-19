from collections.abc import Generator

from src.streamstats.parsers import entry_point_for_file_parsers
from src.streamstats.models import ResultStatistic, CounterSource, LineLogs


def sorted_top_five_error(
        d_name: str, d_value: int, top_five_source: list | list[tuple[str, int]]
        ) -> list | list[tuple[str, int]]:
    """Сортирует 5 ошибок по критерию CRITICAL/ERROR
    Args:
        d_name - источник для сортировки
        d_value - количество ошибок источника
        top_five_source - список со всеми ошибками, отсортированный
    Returns:
        top_five_source - список со всеми ошибками, отсортированный
        """
    t_name: str; t_error: int

    if d_value != 0:
        for i, tuple_value in enumerate(top_five_source):
            t_name, t_error = tuple_value
            if t_error < d_value:  # Проверяет какой источник чаще встречался, если d_name,
                                   # тогда он встает на место t_name
                top_five_source.insert(i, (d_name, d_value))
                return top_five_source
            elif t_error == d_value:  # Если два источника встречались два раза подряд,
                                      # тогда они, сравниваюсь по имени:
                if t_name > d_name:
                    top_five_source.insert(i, (d_name, d_value))
                    return top_five_source
                else:
                    top_five_source.insert(i + 1, (d_name, d_value))
                    return top_five_source
    return top_five_source


def entry_point_for_file_analysis(name_file: str):
    """Входная точка для анализа файла
    Args:
        name_file - имя файла, примеры: test.csv, test.json
    Returns:

    """
    name: str; format: str

    result_statistic: ResultStatistic = ResultStatistic(counter_source={},top_five_source=[])  # Создаем объект класса ResultStatistic

    name, format = name_file.split(".")
    my_generator: Generator[LineLogs, None, None] = entry_point_for_file_parsers(name_file, format)

    # Записываю имя файла в итоговую статистику
    result_statistic.name = name

    for line in my_generator:
        time: str = line.timestamp  # лог время
        level: str = line.level  # лог левел
        source: str = line.source  # лог источник

        # Записывает временные точки в итоговую статистику
        if result_statistic.start_time is None:
            result_statistic.start_time = time
        result_statistic.end_time = time

        # Записывает все level в итоговую статистику
        result_statistic.all_event += 1

        # Записывает новый source, если такого нет
        if source not in result_statistic.counter_source:
            result_statistic.counter_source[source] = CounterSource()

        # Записывает сколько каждый level встречался в логах,
        # а так же сколько раз встречался level для каждого source
        counter_source = result_statistic.counter_source[source]
        match level:
            case "DEBUG":
                result_statistic.debug += 1
                counter_source.debug += 1
            case "INFO":
                result_statistic.info += 1
                counter_source.info += 1
            case "WARNING":
                result_statistic.warning += 1
                counter_source.warning += 1
            case "ERROR":
                result_statistic.error += 1
                counter_source.error += 1
            case "CRITICAL":
                result_statistic.critical += 1
                counter_source.critical += 1

    top_five_source: list | list[tuple[str, int]] = []  # [(name, critical/error)]
    for key, value in result_statistic.counter_source.items():
        if len(top_five_source) == 0:
            if value.critical != 0:
                top_five_source.append((key, value.critical))
            if value.error != 0:
                if value.error > value.critical:
                    top_five_source.insert(0, (key, value.error))
                else:
                    top_five_source.append((key, value.error))
            continue

        top_five_source = sorted_top_five_error(key, value.critical, top_five_source)
        top_five_source = sorted_top_five_error(key, value.error, top_five_source)

    result_statistic.top_five_source = top_five_source