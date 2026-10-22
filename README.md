# codex-demo

一个用于演示 Codex / ChatGPT 迭代开发的最小 Python 项目。第一版是本地任务清单，支持添加、查看和完成任务，并将数据保存到 JSON 文件。

## 技术选择

- Python 3.11+，运行时只用标准库，无需 API Key、数据库或第三方服务。
- `argparse` 提供命令行，`json` 保存数据，`unittest` 验证核心行为。
- 采用 `src` 布局，命令入口与持久化函数清晰可见，后续可拆分模块。

这是代码协作演示项目，当前没有接入模型 API。可以让 Codex 在此基础上实现删除、筛选、截止日期等功能。

## 目录

```text
codex-demo/
├── README.md
├── AGENTS.md                # 后续代码协作约定
├── .gitignore
├── pyproject.toml           # 包信息及可选安装入口
├── run.py                   # 免安装启动入口
├── src/codex_demo/
│   ├── __init__.py
│   ├── __main__.py          # python -m codex_demo
│   └── cli.py               # 命令与 JSON 持久化
└── tests/
    └── test_cli.py
```

## 快速启动（Windows / macOS / Linux）

安装 Python 3.11 或更新版本，打开终端：

```bash
git clone https://github.com/tonyblack2048/codex-demo.git
cd codex-demo
python --version
python run.py
python run.py add "完成第一次 Codex 演示"
python run.py list
python run.py done 1
python run.py list
```

如果系统只有 `python3` 命令，将示例中的 `python` 换为 `python3`。Windows 也可使用 `py`。

任务默认保存在**当前工作目录**的 `.codex-demo/tasks.json`，重新启动仍会保留。该目录已忽略，不提交到 Git。指定其他路径时，全局参数放在子命令前：

```bash
python run.py --data-file ./local-tasks.json add "使用独立数据文件"
python run.py --data-file ./local-tasks.json list
```

自定义数据文件请自行加入 `.gitignore`。编号不存在、空白任务名、损坏的数据文件会返回退出码 1；损坏文件不会被自动覆盖。

## 测试

从仓库根目录设置源码路径，然后运行测试。无需安装第三方依赖。

macOS / Linux：

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Windows PowerShell：

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

Windows CMD：

```bat
set PYTHONPATH=src
python -m unittest discover -s tests -v
```

测试使用临时目录，覆盖任务完整流程、无效输入和损坏数据保护，不会修改个人任务。

## 可选：安装为命令

建议在虚拟环境内运行 `python -m pip install -e .`，之后可使用 `codex-demo --help` 或 `python -m codex_demo --help`。安装需要 setuptools 构建工具；免安装的 `run.py` 路径不需要联网。

## 后续迭代

1. 添加 `delete <id>`，同时验证删除其他任务后编号不会冲突。
2. 添加 `list --pending`，只显示未完成任务。
3. 拆分存储层，并在需要并发时迁移到 SQLite。

可以给 Codex 的首个任务：

> 阅读 README 和 AGENTS.md，实现 list --pending，补充覆盖筛选行为的测试，并运行现有测试。

## 当前边界

这是单用户本地演示，不支持并发写入。保存采用同目录临时文件加原子替换，避免直接覆盖过程中留下半份 JSON；它不提供多进程锁。数据以明文存储，不适合保存敏感信息。
