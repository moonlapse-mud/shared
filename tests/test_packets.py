import os
import unittest
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.moonlapseshared.packet import *
from src.moonlapseshared.crypto import *


class PacketTests(unittest.TestCase):
    def test_pid(self):
        p = DenyPacket()
        self.assertEqual(DenyPacket.pid, ~p.pid)

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

    def test_encrypt(self):
        key = 'sixteen byte key'
        c = AESCipher(key)
        p = MovePacket(1, 0)
        data = p.to_bytes().decode('ASCII')
        enc = c.encrypt(data)
        dec = c.decrypt(enc)
        p2 = MovePacket.from_bytes(dec.encode('ASCII'))
        self.assertEqual(p, p2)

    def test_print_char_field(self):
        cf = fields.CharField(5)
        self.assertEqual(str(cf), '(CharField: 5)')

    def test_equal_fields(self):
        sf = fields.ShortField(0xFFFF)
        sf2 = fields.ShortField(0xFFFF)
        self.assertEqual(sf, sf2)

    def test_equal_fields_wrong_type(self):
        sf = fields.ShortField(0xFF)
        cf = fields.CharField(0xFF)
        self.assertNotEqual(sf, cf)

    def test_iter_move_packet(self):
        mp = MovePacket(1, 0)
        fs = [f for f in mp]
        self.assertEqual(fs[0], fields.ShortField(MovePacket.pid))
        self.assertEqual(fs[1], fields.CharField(1))
        self.assertEqual(fs[2], fields.CharField(0))

    def test_equal_move_packet(self):
        mp1 = MovePacket(1, 0)
        bs = mp1.to_bytes()
        mp2 = from_bytes(bs)
        self.assertEqual(mp1, mp2)

    def test_print_move_packet(self):
        mp = MovePacket(1, 0)
        self.assertEqual(str(mp), "MovePacket: ['(ShortField: 3)', '(CharField: 1)', '(CharField: 0)']")


if __name__ == '__main__':
    unittest.main()
