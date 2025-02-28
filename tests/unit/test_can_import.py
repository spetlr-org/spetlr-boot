import unittest

import spetlrboot


class TestCanImport(unittest.TestCase):
    def test_import(self):
        print(f"Seems we can import the spetlrboot module {spetlrboot.__version__}")
