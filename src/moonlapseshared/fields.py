

class Field:
    size: int   # to override. The size in bytes of this field

    def __init__(self):
        self.value = None
        self.size = self.__class__.size

    def to_bytes(self) -> bytes:
        raise NotImplementedError()

    @classmethod
    def from_bytes(cls, bs: bytes):
        raise NotImplementedError()

    def __invert__(self):
        return self.value

    def __len__(self):
        return self.size

    def __str__(self):
        return f"({self.__class__.__name__}: {~self})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__


class IntField(Field):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def to_bytes(self) -> bytes:
        return self.value.to_bytes(self.size, 'big')

    @classmethod
    def from_bytes(cls, bs: bytes):
        return cls(int.from_bytes(bs, 'big'))


class CharField(IntField):
    """
    1 byte integer
    """

    size = 1

    def __init__(self, value: int):
        super().__init__(value)


class ShortField(IntField):
    """
    2 bytes integer
    """

    size = 2

    def __init__(self, value: int):
        super().__init__(value)


class LongField(IntField):
    """
    4 bytes integer
    """

    size = 4

    def __init__(self, value: int):
        super().__init__(value)


class LongLongField(IntField):
    """
    8 bytes integer
    """

    size = 8

    def __init__(self, value: int):
        super().__init__(value)


class StringFixedField(Field):
    """
    Fixed-sized string
    """

    def __init__(self, value: str):
        super().__init__()
        if len(value) > 20:
            raise AttributeError("Value longer than acceptable size")
        self.value = value

    def to_bytes(self) -> bytes:
        value = self.value.ljust(self.size, '\0')
        return value.encode('ASCII')

    @classmethod
    def from_bytes(cls, bs: bytes):
        value = bs.decode('ASCII')
        value = value.rstrip('\0')
        return cls(value)


class String20Field(StringFixedField):
    size = 20
