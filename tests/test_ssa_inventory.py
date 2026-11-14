"""Small fixtures cover inventory correctness and unsafe input failures."""

import hashlib
from pathlib import Path
import tempfile
import unittest

from src.ssa_inventory import InventoryError, inspect_file, inventory, main, source_files, write_inventory


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = self.root / "state"
        self.national = self.root / "national"
        self.state.mkdir()
        self.national.mkdir()
        self.state_bytes = b"CA,F,1910,Mary,5\r\nCA,M,1912,John,7\r\n"
        (self.state / "CA.TXT").write_bytes(self.state_bytes)
        (self.national / "yob1880.txt").write_bytes(b"Mary,F,10\nJohn,M,12\n")
        (self.national / "yob1882.txt").write_bytes(b"Mary,F,8")

    def test_exact_bytes_rows_and_observed_coverage(self):
        records, summary = inventory(self.state, self.national)
        ca = records[0]
        self.assertEqual(ca["sha256"], hashlib.sha256(self.state_bytes).hexdigest())
        self.assertEqual(ca["bytes"], len(self.state_bytes))
        self.assertEqual(ca["row_count"], 2)
        self.assertEqual(ca["years_present"], [1910, 1912])
        self.assertEqual(ca["sex_codes"], ["F", "M"])
        self.assertEqual(ca["geographies"], ["CA"])
        self.assertEqual(summary["datasets"]["national"]["row_count"], 3)
        self.assertEqual(summary["datasets"]["national"]["missing_years_within_observed_range"], [1881])
        self.assertEqual(summary["datasets"]["state"]["missing_years_within_observed_range"], [1911])
        self.assertIn("DC", summary["datasets"]["state"]["missing_states_including_dc"])
        self.assertIn("duplicate-key audit", summary["not_performed"])
        self.assertEqual((self.state / "CA.TXT").read_bytes(), self.state_bytes)

    def test_deterministic_outputs_and_readme_companions(self):
        (self.state / "StateReadMe.pdf").write_bytes(b"source documentation")
        (self.national / ".gitkeep").touch()
        records, summary = inventory(self.state, self.national)
        output = self.root / "out"
        write_inventory(records, summary, output)
        first = {path.name: path.read_bytes() for path in output.iterdir()}
        write_inventory(*inventory(self.state, self.national), output)
        self.assertEqual(first, {path.name: path.read_bytes() for path in output.iterdir()})

    def test_bad_rows_fail_with_location(self):
        bad_rows = [
            b"CA,F,1910,Mary\n", b"NY,F,1910,Mary,5\n", b"CA,X,1910,Mary,5\n",
            b"CA,F,nope,Mary,5\n", b"CA,F,1910,Mary,0\n", b"CA,F,1910,Mary,5.0\n",
            b"CA,F,1910,,5\n", b"CA,F,1910,Mary,-1\n", b"\n",
            b'CA,F,1910,"Mary,5\n', b"CA,F,1910,\xff,5\n",
        ]
        for contents in bad_rows:
            with self.subTest(contents=contents):
                (self.state / "CA.TXT").write_bytes(contents)
                with self.assertRaisesRegex(InventoryError, r"CA\.TXT, line"):
                    inspect_file(self.state / "CA.TXT", "state")

    def test_unknown_filename_empty_and_missing_data_fail(self):
        (self.state / "extra.csv").touch()
        with self.assertRaisesRegex(InventoryError, "Unrecognised"):
            source_files(self.state, "state")
        (self.state / "extra.csv").unlink()
        (self.state / "CA.TXT").write_bytes(b"")
        with self.assertRaisesRegex(InventoryError, "Empty data file"):
            inspect_file(self.state / "CA.TXT", "state")
        (self.state / "CA.TXT").unlink()
        with self.assertRaisesRegex(InventoryError, "No state data files"):
            source_files(self.state, "state")
        with self.assertRaisesRegex(InventoryError, "Missing state data directory"):
            source_files(self.root / "missing", "state")

    def test_cli_does_not_write_outputs_on_bad_input(self):
        (self.national / "yob1880.txt").write_text("bad\n")
        output = self.root / "output"
        result = main(["--state-dir", str(self.state), "--national-dir", str(self.national), "--output-dir", str(output)])
        self.assertEqual(result, 1)
        self.assertFalse(output.exists())

    def test_state_only_does_not_require_national_data(self):
        for path in self.national.iterdir():
            path.unlink()
        self.national.rmdir()
        records, summary = inventory(self.state, self.national, ("state",))
        self.assertEqual(len(records), 1)
        self.assertEqual(list(summary["datasets"]), ["state"])
        self.assertEqual(summary["datasets_not_inventoried"], ["national"])
        self.assertEqual(main(["--datasets", "state", "--state-dir", str(self.state), "--national-dir", str(self.national), "--output-dir", str(self.root / "out")]), 0)

    def test_cli_refuses_output_inside_raw(self):
        with self.assertRaises(SystemExit) as error:
            main(["--state-dir", str(self.state), "--national-dir", str(self.national), "--output-dir", str(self.state / "output")])
        self.assertEqual(error.exception.code, 2)
        self.assertFalse((self.state / "output").exists())


if __name__ == "__main__":
    unittest.main()
