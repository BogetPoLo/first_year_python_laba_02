# Лабораторная работа №2: анализ логов (toolkit)

1) Анализ файлов (analyze):
    - Поддержка форматов csv и jsonl.
    - Возможность одновременной обработки нескольких файлов с объединением их статистики.
2) Сбор статистики и анализа:
   - Подсчет общего количества событий и распределения по уровням логирования (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
   - Сбор статистики по каждому источнику (`source`).
   - Формирования топ-5 источников, чаще всего получавших ошибок уровней `ERROR/CRITICAL`.
3) Валидация:
   - Проверка (`timestamp`, `level`, `source`, `message`) через Pydantic.
   - Режим `--skip-invalid` - пропускает поврежденные строки, если такие были

## Примеры запуска
1) Для csv-файла
   `python -m streamstats analyze logs.csv --format csv --output report`
2) Для нескольких csv-файлов
   `python -m streamstats analyze logs.csv logs2.csv --format csv --output combined_report`
3) Для jsonl-файла
   - `python -m streamstats analyze logs.jsonl --format jsonl --skip-invalid`

## Справка
`python -m streamstats --help`

## Структура проекта
```lab_02/
├── pyproject.toml
├── README.md
├── src/
│   └── streamstats/
│       ├── __init__.py
│       ├── __main__.py
│       ├── models.py
│       ├── parsers.py
│       ├── analysis.py
│       ├── report.py
│       └── errors.py
└── tests/```