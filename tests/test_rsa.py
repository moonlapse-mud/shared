from pathlib import Path
import unittest
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.moonlapseshared.crypto import *


class MyTestCase(unittest.TestCase):

    def test_rsa(self):
        dir = os.path.join(str(Path.home()), '.moonlapse', 'server')
        pubkey, privkey = load_rsa_keypair(dir)
        print(pubkey)
        print(privkey)
        pass


if __name__ == '__main__':
    unittest.main()
