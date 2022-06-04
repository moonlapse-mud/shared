from . import fields
from . import crypto


class Flags:
    ENCRYPT = 0b0000_0001


class Packet:
    pid: int    # to override. The unique ID of this packet.

    def __init__(self, flags=0):
        self.pid = self.__class__.pid
        self.flags = flags

    def get_fields(self):
        d = {}
        for key, value in self.__dict__.items():
            if isinstance(value, fields.Field):
                d[key] = value
        return d

    def to_bytes(self, pubkey=None) -> bytes:
        """
        Converts this packet to a byte array in network-byte order.
        """
        bs = b''

        encrypted = self.flags & Flags.ENCRYPT

        # add all payload fields
        fs = self.get_fields()
        for f in fs.values():
            bs += f.to_bytes()

        if encrypted:
            if not pubkey:
                raise AttributeError("Packet was encrypted, but public key was not supplied")
            bs = crypto.encrypt(bs, pubkey)

        # attach header information
        # padding + flags + pid + length
        flags = self.flags << 24
        pid = self.pid << 11
        length = len(bs)
        header = fields.LongField(flags | pid | length)

        return header.to_bytes() + bs

    @classmethod
    def from_bytes(cls, bs: bytes, privkey=None):
        p = cls()
        fs = p.get_fields()

        # extract header
        header = int.from_bytes(bs[0:4], 'big')
        p.flags = header >> 24
        p.pid = (header & 0xFFF8) >> 11

        bs = bs[4:]

        encrypted = p.flags & Flags.ENCRYPT
        if encrypted:
            if not privkey:
                raise AttributeError("Packet was encrypted, but private key was not supplied")
            bs = crypto.decrypt(bs, privkey)

        index = 0

        for key, value in fs.items():
            size = value.size
            value = value.__class__.from_bytes(bs[index:(index + size)])
            p.__setattr__(key, value)
            index += size

        return p

    def __len__(self):
        size = 0
        for f in self.get_fields().values():
            size += len(f)
        return size

    def __iter__(self):
        self.__field_n_ = 0
        return self

    def __next__(self):
        fs = list(self.get_fields().values())
        if self.__field_n_ == len(fs):
            raise StopIteration
        result = fs[self.__field_n_]
        self.__field_n_ += 1
        return result

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def __str__(self):
        fs = [str(f) for f in self]
        return f"{self.__class__.__name__}: {fs}"


class OkPacket(Packet):
    pid = 0x0001


class DenyPacket(Packet):
    pid = 0x0002


class MovePacket(Packet):
    pid = 0x0003

    def __init__(self, dy=0, dx=0, flags=0):
        super().__init__(flags=flags)
        self.dy: fields.CharField = fields.CharField(dy)
        self.dx: fields.CharField = fields.CharField(dx)


#
# ALL PACKETS MUST LIVE ABOVE THIS LINE
#

# equivalent of #ifndef. This clause is for reflection to return the correct packet type at runtime
if '__packet_py_packet_types' not in globals().keys():
    __packet_py_packet_types = []
    global_copy = globals().copy()
    for k, _ in global_copy.items():
        if 'Packet' in k:
            __packet_py_packet_types += [k]
    __packet_py_packet_types.remove('Packet')


def from_bytes(bs: bytes, privkey=None) -> Packet:
    header = int.from_bytes(bs[0:4], 'big')
    pid = (header & 0xFFF8) >> 11

    for ptype in __packet_py_packet_types:
        t = globals()[ptype]
        if pid == t.pid:
            return t.from_bytes(bs, privkey)
    raise Exception(f"{pid} not a registered packet id.")
