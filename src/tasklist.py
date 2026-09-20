"""Command-line Todo application for codex-loop-lab."""

import argparse
import json
import os
from pathlib import Path


def _data_path() -> Path:
    return Path(os.environ.get("TASKLIST_DATA_FILE", "tasks.json"))


def _load_tasks() -> list[dict]:
    path = _data_path()
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _save_tasks(tasks: list[dict]) -> None:
    path = _data_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _add_task(title: str) -> None:
    tasks = _load_tasks()
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    _save_tasks(tasks)
    print(f"已添加任务 {next_id}: {title}")


def _list_tasks() -> None:
    tasks = _load_tasks()
    if not tasks:
        print("暂无任务")
        return
    for task in tasks:
        marker = "x" if task["done"] else " "
        print(f"{task['id']}. [{marker}] {task['title']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="命令行 Todo 列表")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="新增任务")
    add_parser.add_argument("title", help="任务标题")
    subparsers.add_parser("list", help="列出任务")

    args = parser.parse_args(argv)
    if args.command == "add":
        _add_task(args.title)
    else:
        _list_tasks()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
