import unittest

import spetlrbootstrap


class TestCanImport(unittest.TestCase):
    def test_import(self):
        print(
            f"Seems we can import the spetlrboot module {spetlrbootstrap.__version__}"
        )
