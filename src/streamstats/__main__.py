from pathlib import Path
from streamstats.report import start_make_files

import typer

from typing import Annotated, Literal, Generator
from streamstats.models import ResultStatistic, LineLogs
from streamstats.analysis import entry_point_for_file_analysis
from streamstats.parsers import entry_point_for_file_parsers


app = typer.Typer()


@app.command()
def analyze(
        input_files: Annotated[
            list[Path],
            typer.Argument(help="Имя файла")],
        format: Annotated[
            Literal["csv", "jsonl", "CSV", "JSNOL"] | None,
            typer.Option("--format", help="Формат файла.")] = None,
        output: Annotated[
            str,
            typer.Option(
                "--output", help="Файл в который нужно записать результат программы."
            )] = "",
        skip_invalid: Annotated[
            bool,
            typer.Option(
                "--skip-invalid", help="Выводит предупреждение если строка не прошла валидацию.")
        ] = False
) -> None:
    """Создание модуля analyze
    Args:
        input_files - обязательный аргумент, в него передается имя файла/ов
        format - обязательный аргумент, в него передается формат всех файлов, которые были в input_file
        output - обязательный аргумент, в него передается в какой файл будет записанная общая статистика
        со всех файлов указанных в input_file
    Returns:
        None"""

    all_object: list[ResultStatistic] | list = []  # Все отсортированные логи файлов

    for file in input_files:
        if format is None:
            format = file.suffix[1::]

        result_statistic: ResultStatistic = ResultStatistic(
            counter_source={},
            top_five_source={}
        )  # Создаем объект класса ResultStatistic

        # Передаю в объект имя и формат файла
        result_statistic.name = file.stem
        result_statistic.format = format

        my_generator: Generator[LineLogs, None, None] = entry_point_for_file_parsers(
            file,
            format,
            skip_invalid
        )  # Генератор

        all_object.append(entry_point_for_file_analysis(result_statistic, my_generator))
    start_make_files(all_object, output)


@app.command()
def func_pass() -> None:
    """Функция затычка, нужна, что бы typer запускался модуль analyze"""
    pass


if __name__ == "__main__":
    app()
