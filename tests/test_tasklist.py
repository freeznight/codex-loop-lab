import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import tasklist


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_module_runs_from_repository_root_without_pythonpath(tmp_path):
    data_file = tmp_path / "tasks.json"
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["TASKLIST_DATA_FILE"] = str(data_file)

    added = subprocess.run(
        [sys.executable, "-m", "tasklist", "add", "买牛奶"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    listed = subprocess.run(
        [sys.executable, "-m", "tasklist", "list"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert added.returncode == 0
    assert added.stdout == "已添加任务 1: 买牛奶\n"
    assert added.stderr == ""
    assert listed.returncode == 0
    assert listed.stdout == "1. [ ] 买牛奶\n"
    assert listed.stderr == ""


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
