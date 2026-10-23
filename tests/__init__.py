import json
import pytest
from streamstats.parsers import entry_point_for_file_parsers
from streamstats.errors import EmptyFieldError, FormatFieldError


def test_csv(tmp_path):
    f = tmp_path / "test.csv"
    f.write_text(
        "timestamp,level,source,message\n"
        "2026-10-25T12:00:00,INFO,app,ok\n",
        encoding="utf-8"
    )
    logs = list(entry_point_for_file_parsers(f, "csv", skip_invalid=False))
    assert len(logs) == 1
    assert logs[0].level == "INFO"
    assert logs[0].source == "app"


def test_jsonl(tmp_path):
    f = tmp_path / "test.jsonl"
    data = {"timestamp": "2026-10-25T12:00:00", "level": "ERROR", "source": "db", "message": "fail"}
    f.write_text(json.dumps(data) + "\n", encoding="utf-8")

    logs = list(entry_point_for_file_parsers(f, "jsonl", skip_invalid=False))
    assert len(logs) == 1
    assert logs[0].level == "ERROR"
    assert logs[0].source == "db"


def test_unicode(tmp_path):
    f = tmp_path / "test.csv"
    f.write_text(
        "timestamp,level,source,message\n"
        "2026-10-25T12:00:00,INFO,сервис,ошибка сети\n",
        encoding="utf-8"
    )
    logs = list(entry_point_for_file_parsers(f, "csv", skip_invalid=False))
    assert logs[0].source == "сервис"
    assert logs[0].message == "ошибка сети"


def test_empty_file(tmp_path):
    f = tmp_path / "empty.csv"
    f.write_text("", encoding="utf-8")
    with pytest.raises(EmptyFieldError):
        list(entry_point_for_file_parsers(f, "csv", skip_invalid=False))


def test_invalid_format(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("data", encoding="utf-8")
    with pytest.raises(FormatFieldError):
        list(entry_point_for_file_parsers(f, "txt", skip_invalid=False))


def test_skip_invalid(tmp_path):
    f = tmp_path / "test.jsonl"
    valid = {"timestamp": "2026-10-25T12:00:00", "level": "INFO", "source": "app", "message": "ok"}
    invalid = {"timestamp": "bad_date", "level": "INFO", "source": "app", "message": "err"}
    f.write_text(f"{json.dumps(valid)}\n{json.dumps(invalid)}\n", encoding="utf-8")

    logs = list(entry_point_for_file_parsers(f, "jsonl", skip_invalid=True))
    valid_logs = [item for item in logs if item]
    assert len(valid_logs) == 1