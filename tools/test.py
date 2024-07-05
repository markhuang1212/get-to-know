import json
import unittest

from dotenv import load_dotenv

load_dotenv()

from tools.fetch_web import fetch_web
from tools.web_search import web_search


class TestTools(unittest.TestCase):
    def test_web_search(self):
        result_str = web_search("python")
        result = json.loads(result_str)
        self.assertIsInstance(result, list)

    def test_fetch_web(self):
        result_str = fetch_web("https://rust-lang.org")
        result = json.loads(result_str)
        self.assertIsInstance(result["text"], str)
        self.assertIsInstance(result["links"], list)


if __name__ == "__main__":
    unittest.main()
