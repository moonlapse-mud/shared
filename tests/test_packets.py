import os
import unittest
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.moonlapseshared.packet import *


class PacketTests(unittest.TestCase):
    def test_pid(self):
        p = AggregatePacket()
        self.assertEqual(AggregatePacket.pid, ~p.pid)

    def test_from_to_bytes(self):
        p = MovePacket(0xFF, 1)
        bs = p.to_bytes()
        p2 = from_bytes(bs)
        bs2 = p2.to_bytes()
        self.assertEqual(bs, bs2)

    def test_ok_from_to_bytes(self):
        p = OkPacket()
        bs = p.to_bytes()
        p2 = from_bytes(bs)
        bs2 = p2.to_bytes()
        self.assertEqual(bs, bs2)

    def test_char_field_length(self):
        c = fields.CharField(255)
        self.assertEqual(len(c), 1)

    def test_move_packet_size(self):
        p = MovePacket()
        self.assertEqual(len(p), 4)


if __name__ == '__main__':
    unittest.main()
