from datetime import datetime, timezone
from collections.abc import Generator

from streamstats.models import ResultStatistic, CounterSource, LineLogs


def sorted_top_five_error(result_statistic: ResultStatistic) -> dict[int, tuple[int, int, str]]:
    """Сортирует ошибки типа ERROR/CRITICAL в порядке убывания
    Args:
        result_statistic - объект dataclass
    Returns:
        Возвращает 5 или меньше строк с самыми часто встречающимися источниками,
        которые получали ошибку ERROR/CRITICAL"""
    top_five_source_list: list | list[tuple[str, int, int]] = []

    # Приводит словарь к типу [(источник, сколько раз встречался, тип ошибки 0 - ERROR, 1 - CRITICAL)]
    for key, value in result_statistic.counter_source.items():
        if value.error != 0:
            top_five_source_list.append((key, value.error, 0))
        if value.critical != 0:
            top_five_source_list.append((key, value.critical, 1))
    # Сортируем через lambda
    top_five_source: list[type[str, int, int]] = sorted(top_five_source_list, key=lambda x: (-x[1], -x[2], x[0]))[0:5]

    # Приводит к более удобному виду для записи и чтения в словаре,
    # а так же заменяем 0 на ERROR b 1 на CRITICAL
    top_five_source_dict: dict | dict[int, tuple[int, int, str]] = {}
    for i, value in enumerate(top_five_source):
        match value[-1]:
            case 0:
                value = (value[0], value[1], "ERROR")
            case 1:
                value = (value[0], value[1], "CRITICAL")
        top_five_source_dict[i] = value
    return top_five_source_dict


def sorted_data(result_statistic: ResultStatistic, my_generator: Generator[LineLogs, None, None]) -> None:
    """Сортирует данные для dataclass
    Args:
        result_statistic - объект dataclass
        my_generator - генераторная функция
    Returns:
        None"""
    for line in my_generator:
        if not line:
            result_statistic.skip_lines += 1
            continue
        elif line is None:
            break
        time: datetime = line.timestamp  # лог время
        level: str = line.level  # лог левел
        source: str = line.source  # лог источник
        mess: str = line.message  # лог сообщение

        # Записывает временные точки в итоговую статистику
        if result_statistic.start_time is None:
            result_statistic.start_time = time
            result_statistic.end_time = time
        else:
            if time < result_statistic.start_time:
                result_statistic.start_time = time
            if time > result_statistic.end_time:
                result_statistic.end_time = time

        # Записывает все level в итоговую статистику
        result_statistic.all_level += 1

        # Записывает новый source, если такого нет
        if source not in result_statistic.counter_source:
            result_statistic.counter_source[source] = CounterSource(timestamp=[], message=[])

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

        # Добавляем время в общую статистику
        counter_source.timestamp.append(time.isoformat())
        # Добавляем соо в общую статистику
        counter_source.message.append(mess)


def entry_point_for_file_analysis(
        result_statistic: ResultStatistic,
        my_generator: Generator[LineLogs, None, None]
    ) -> ResultStatistic:
    """Входная точка для анализа файла
    Args:
        name_file - имя файла, примеры: test.csv, test.json
    Returns:
        result_statistic - объект dataclass
    """

    # Вызов функции для сортировки данных
    sorted_data(result_statistic, my_generator)

    result_statistic.start_time = result_statistic.start_time.isoformat()
    result_statistic.end_time = result_statistic.end_time.isoformat()

    # Вызов функции для сортировки top-5 элементов
    result_statistic.top_five_source = sorted_top_five_error(result_statistic)

    return result_statistic
