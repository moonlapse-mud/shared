import abc
from . import fields


class Packet(abc.ABC):
    pid: int    # to override. The unique ID of this packet

    def __init__(self):
        self.pid: fields.ShortField = fields.ShortField(self.__class__.pid)

    def to_bytes(self) -> bytes:
        """
        Converts this packet to a byte array in network-byte order.
        """
        bs = b''
        fs = self.__dict__
        for v in fs.values():
            if isinstance(v, fields.Field):
                bs += v.to_bytes()
        return bs

    @classmethod
    def from_bytes(cls, bs: bytes):
        p = cls()
        fs = p.__dict__

        index = 0

        for key, value in fs.items():
            if not isinstance(value, fields.Field):
                continue
            size = value.size
            value = value.__class__.from_bytes(bs[index:(index + size)])
            p.__setattr__(key, value)
            index += size

        return p

    def __len__(self):
        size = 0
        for f in self.__dict__.values():
            size += len(f)
        return size

    def __iter__(self):
        self.__field_n_ = 0
        return self

    def __next__(self):
        fs = list(self.__dict__.values())
        if self.__field_n_ == len(fs) - 1:
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

    def __init__(self, dy=0, dx=0):
        super().__init__()
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


def from_bytes(bs: bytes) -> Packet:
    pid = int.from_bytes(bs[0:2], 'big')
    for ptype in __packet_py_packet_types:
        t = globals()[ptype]
        if pid == t.pid:
            return t.from_bytes(bs)
    raise Exception(f"{pid} not a registered packet id.")