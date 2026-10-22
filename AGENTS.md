# 开发约定

- 项目使用 Python 3.11+，运行时仅依赖标准库。
- 源码放在 `src/codex_demo/`，测试放在 `tests/`。
- 从仓库根目录运行 `python run.py` 查看命令帮助。
- 提交前运行 `python -m unittest discover -s tests -v`，先按 README 设置 PYTHONPATH。
- 修改命令行行为时同步更新 README 和相关测试。
- 不提交本地任务数据、凭据或虚拟环境。
- 当前 JSON 存储面向单用户串行调用；引入并发写入前先设计锁或数据库方案。
