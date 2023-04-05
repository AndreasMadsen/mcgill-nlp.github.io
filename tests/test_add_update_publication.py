from genericpath import exists
from pathlib import Path
import unittest
import os
import json
import shutil
from ruamel.yaml import YAML

import src.python.add_update_publication as mod

from .config import REMOVE_GENERATED_FILES


class TestAddUpdatePublication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        yaml = YAML()
        yaml.preserve_quotes = True
        with open("_data/authors.yml") as f:
            cls.authors = yaml.load(f)

        os.makedirs("tests/scratch/assets/images/papers/", exist_ok=True)

        cls.save_dir = "tests/scratch/_posts/papers/"
        cls.image_dir = "tests/scratch/assets/images/papers/"

    @classmethod
    def tearDownClass(cls) -> None:
        if REMOVE_GENERATED_FILES:
            for path in [
                cls.save_dir,
                cls.image_dir,
            ]:
                if os.path.exists(path):
                    shutil.rmtree(path)

    def test_add_publication(self):
        in_path = "tests/data/add_publication/in.md"
        expected_out_path = "tests/data/add_publication/out.md"

        with open(in_path) as f:
            issue_body = f.read()

        with open(expected_out_path) as f:
            expected = f.read()

        parsed = mod.parse_issue_body(issue_body)
        formatted = mod.main(parsed, save_dir=self.save_dir, image_dir=self.image_dir)

        saved_file_path = Path(self.save_dir) / formatted["filename"]

        error_msg = f"\n\n!!! Expected content of file {saved_file_path} to match content of file {expected_out_path}, but they did not match !!!"

        self.assertEqual(formatted["content"], expected, error_msg)

    def test_update_publication(self):
        with open("tests/data/update_publication/in.md") as f:
            issue_body = f.read()

        with open("tests/data/update_publication/out.md") as f:
            expected = f.read()

        parsed = mod.parse_issue_body(issue_body)
        formatted = mod.main(parsed, save_dir=self.save_dir, image_dir=self.image_dir)

        self.assertEqual(formatted["content"], expected)

        path = os.path.join(self.image_dir, "1904.1234.jpg")
        self.assertTrue(
            os.path.isfile(path),
            msg=f"Expected a file to find a file at {path}, but only the following files were there: {os.listdir(self.image_dir)}",
        )
