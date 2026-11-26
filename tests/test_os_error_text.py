"""tools/os_error_text.py: an OSError's paths are printed as written, not as repr() (no doubled backslashes).

    python -I tests/test_os_error_text.py
"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from os_error_text import os_error_text  # noqa: E402

WINDOWS_PATH = "C:\\Users\\me\\blocked"


class OsErrorTextTest(unittest.TestCase):
    def test_windows_path_is_printed_as_written(self):
        error = PermissionError(13, "Permission denied", WINDOWS_PATH)
        self.assertNotIn(WINDOWS_PATH, str(error))  # what the tools printed before: the path's repr()
        self.assertEqual(os_error_text(error), "[Errno 13] Permission denied: C:\\Users\\me\\blocked")

    def test_both_paths_of_a_rename(self):
        error = OSError(18, "Invalid cross-device link", "C:\\a\\old", None, "D:\\b\\new")  # 4th: winerror
        self.assertEqual(os_error_text(error), "[Errno 18] Invalid cross-device link: C:\\a\\old -> D:\\b\\new")

    def test_bytes_and_pathlike_paths(self):
        self.assertEqual(os_error_text(FileNotFoundError(2, "No such file", b"dir/x.bin")),
                         "[Errno 2] No such file: dir/x.bin")

        class Spot:
            def __fspath__(self):
                return "dir\\y.bin"

        self.assertEqual(os_error_text(FileNotFoundError(2, "No such file", Spot())),
                         "[Errno 2] No such file: dir\\y.bin")

    @unittest.skipUnless(os.name == "nt", "winerror is set only on Windows")
    def test_windows_error_keeps_the_winerror_code(self):
        error = OSError(None, "Access is denied", WINDOWS_PATH, 5)
        self.assertEqual(os_error_text(error), "[WinError 5] Access is denied: C:\\Users\\me\\blocked")

    def test_errors_without_a_path_are_unchanged(self):
        for error in (OSError("disk full"), OSError(28, "No space left on device"), ValueError("bad row 3"),
                      KeyError("name")):
            self.assertEqual(os_error_text(error), str(error))


if __name__ == "__main__":
    unittest.main()
