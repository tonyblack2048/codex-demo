"""Task CLI with a small JSON persistence layer."""

import argparse
import json
import os
import tempfile
from pathlib import Path


def load_tasks(path: Path) -> list[dict]:
    if not path.exists():
        return []
    tasks = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(tasks, list):
        raise ValueError("任务文件必须是 JSON 数组")
    ids = set()
    for task in tasks:
        if (not isinstance(task, dict)
                or type(task.get("id")) is not int or task["id"] < 1
                or not isinstance(task.get("title"), str)
                or not task["title"].strip()
                or type(task.get("done")) is not bool):
            raise ValueError("任务文件包含无效记录")
        if task["id"] in ids:
            raise ValueError("任务文件包含重复编号")
        ids.add(task["id"])
    return tasks


def save_tasks(path: Path, tasks: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(tasks, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Codex Demo：本地任务清单")
    parser.add_argument("--data-file", type=Path,
                        default=Path(".codex-demo/tasks.json"),
                        help="JSON 数据文件，默认为当前目录的 .codex-demo/tasks.json")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="添加任务")
    add.add_argument("title")
    commands.add_parser("list", help="查看任务")
    done = commands.add_parser("done", help="完成任务")
    done.add_argument("id", type=int)
    args = parser.parse_args(argv)
    try:
        tasks = load_tasks(args.data_file)
        if args.command == "add":
            title = args.title.strip()
            if not title:
                raise ValueError("任务名称不能为空")
            task_id = max((task["id"] for task in tasks), default=0) + 1
            tasks.append({"id": task_id, "title": title, "done": False})
            save_tasks(args.data_file, tasks)
            print(f"已添加 #{task_id}：{title}")
        elif args.command == "list":
            if not tasks:
                print("暂无任务，使用 add 添加一个。")
            for task in tasks:
                mark = "x" if task["done"] else " "
                print(f"[{mark}] #{task['id']} {task['title']}")
        else:
            task = next((task for task in tasks if task["id"] == args.id), None)
            if task is None:
                raise ValueError(f"找不到任务 #{args.id}")
            task["done"] = True
            save_tasks(args.data_file, tasks)
            print(f"已完成 #{args.id}")
    except (OSError, ValueError) as error:
        parser.exit(1, f"错误：{error}\n")
    return 0
