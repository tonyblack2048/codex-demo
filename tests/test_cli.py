import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from codex_demo.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "data" / "tasks.json"

    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["--data-file", str(self.path), *args]), 0)
        return output.getvalue()

    def test_persistent_task_lifecycle(self):
        self.assertIn("暂无任务", self.run_cli("list"))
        self.run_cli("add", "写 README")
        self.run_cli("add", "运行测试")
        self.assertIn("[ ] #1 写 README", self.run_cli("list"))
        self.run_cli("done", "1")
        self.assertIn("[x] #1 写 README", self.run_cli("list"))
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8"))[1]["id"], 2)

    def test_invalid_inputs_do_not_modify_data(self):
        self.run_cli("add", "保留这条任务")
        before = self.path.read_bytes()
        for args in [("add", "  "), ("done", "99")]:
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    self.run_cli(*args)
            self.assertEqual(error.exception.code, 1)
            self.assertEqual(self.path.read_bytes(), before)

    def test_corrupt_data_is_not_overwritten(self):
        self.path.parent.mkdir()
        for content in ['{broken', '{}', '[{"id": 1}]']:
            self.path.write_text(content, encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.run_cli("add", "新任务")
            self.assertEqual(self.path.read_text(encoding="utf-8"), content)


if __name__ == "__main__":
    unittest.main()
