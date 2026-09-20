import json

import pytest

import tasklist


def test_add_persists_tasks_and_increments_ids(monkeypatch, tmp_path, capsys):
    data_file = tmp_path / "tasks.json"
    monkeypatch.setenv("TASKLIST_DATA_FILE", str(data_file))

    assert tasklist.main(["add", "买牛奶"]) == 0
    assert "已添加任务 1" in capsys.readouterr().out

    assert tasklist.main(["add", "写作业"]) == 0
    assert "已添加任务 2" in capsys.readouterr().out

    assert json.loads(data_file.read_text(encoding="utf-8")) == [
        {"id": 1, "title": "买牛奶", "done": False},
        {"id": 2, "title": "写作业", "done": False},
    ]


def test_list_displays_persisted_tasks_in_chinese(monkeypatch, tmp_path, capsys):
    data_file = tmp_path / "tasks.json"
    monkeypatch.setenv("TASKLIST_DATA_FILE", str(data_file))
    data_file.write_text(
        json.dumps(
            [
                {"id": 1, "title": "买牛奶", "done": False},
                {"id": 2, "title": "写作业", "done": True},
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    assert tasklist.main(["list"]) == 0

    output = capsys.readouterr().out
    assert "1. [ ] 买牛奶" in output
    assert "2. [x] 写作业" in output


def test_list_reports_empty_data_file(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("TASKLIST_DATA_FILE", str(tmp_path / "tasks.json"))

    assert tasklist.main(["list"]) == 0

    assert capsys.readouterr().out == "暂无任务\n"


@pytest.mark.parametrize(
    "arguments", [["--help"], [], ["unknown"], ["add", "--help"], ["add"]]
)
def test_argparse_output_is_chinese(arguments, capsys):
    with pytest.raises(SystemExit):
        tasklist.main(arguments)

    output = capsys.readouterr()
    text = output.out + output.err
    assert any(word in text for word in ("用法", "位置参数", "错误"))
    assert not any(
        word in text
        for word in ("usage:", "positional arguments", "options:", "error:")
    )
