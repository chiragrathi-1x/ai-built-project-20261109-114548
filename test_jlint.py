import unittest
import json
from jlint import validate_and_format

class TestJlint(unittest.TestCase):
    def test_valid_json(self):
        """Test that valid JSON is correctly formatted."""
        raw = '{"name": "jlint", "version": 1}'
        result = validate_and_format(raw, indent=2, sort_keys=True)
        parsed = json.loads(result)
        self.assertEqual(parsed["name"], "jlint")
        self.assertTrue("\n  " in result)

    def test_invalid_json_reporting(self):
        """Test that invalid JSON raises a ValueError with line details."""
        broken = '{"key": "missing quote}'
        with self.assertRaisesRegex(ValueError, "line 1, column 22"):
            validate_and_format(broken, 4, False)

    def test_sort_keys(self):
        """Test that keys are sorted alphabetically when requested."""
        raw = '{"z": 1, "a": 2}'
        result = validate_and_format(raw, indent=4, sort_keys=True)
        lines = [line.strip() for line in result.splitlines() if '"' in line]
        self.assertTrue(lines[0].startswith('"a"'))
        self.assertTrue(lines[1].startswith('"z"'))

    def test_empty_input(self):
        """Test that empty strings cause a parsing error."""
        with self.assertRaises(ValueError):
            validate_and_format("", 4, False)

if __name__ == "__main__":
    unittest.main()