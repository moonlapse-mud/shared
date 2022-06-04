import os
import unittest
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.moonlapseshared.packet import *
from src.moonlapseshared.crypto import *


current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
pub, priv = crypto.load_rsa_keypair(current_dir)


class PacketTests(unittest.TestCase):
    def test_pid(self):
        p = DenyPacket()
        self.assertEqual(DenyPacket.pid, p.pid)

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
        self.assertEqual(len(p), 2)

    def test_encrypt(self):
        p = MovePacket(1, 0, flags=Flags.ENCRYPT)
        bs = p.to_bytes(pub)
        p2 = MovePacket.from_bytes(bs, priv)
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
        self.assertEqual(fs[0], fields.CharField(1))
        self.assertEqual(fs[1], fields.CharField(0))

    def test_equal_move_packet(self):
        mp1 = MovePacket(1, 0)
        bs = mp1.to_bytes()
        mp2 = from_bytes(bs)
        self.assertEqual(mp1, mp2)

    def test_print_move_packet(self):
        mp = MovePacket(1, 0)
        self.assertEqual(str(mp), "MovePacket: ['(CharField: 1)', '(CharField: 0)']")

    def test_header(self):
        mp = MovePacket(dy=1, dx=0, flags=Flags.ENCRYPT)
        bs = mp.to_bytes(pub)
        mp2 = MovePacket.from_bytes(bs, priv)
        bs2 = mp2.to_bytes(pub)
        self.assertEqual(bs[0:4], bs2[0:4])

    def test_flags(self):
        p = OkPacket(Flags.ENCRYPT)
        bs = p.to_bytes(pub)
        p2 = from_bytes(bs, priv)
        self.assertEqual(p, p2)

    def test_new_header(self):
        h = Header(MovePacket.pid, Flags.ENCRYPT, 2)
        self.assertEqual(h.to_bytes(), b'\x01\x00\x18\x02')


if __name__ == '__main__':
    unittest.main()
