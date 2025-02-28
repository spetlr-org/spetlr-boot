import json
import sys
import unittest

from spetlrbootstrap.download import download


class TestDownload(unittest.TestCase):
    def test_import(self):

        sys.argv += [
            "--dependencies=./tmp/downloads",
            f'--requirements={json.dumps(["packaging","requests"])}',
        ]
        print("sys.argv=", sys.argv)
        download()
