# Moonlapse Shared

This is the shared package between the client and server. It contains the packet specification as well as game models and static terrain information.

## Developer's Guide

This section contains minor documentation regarding how to implement the features in this repository.

### Install Package

To include this package in your environment, run:

```
$ pip3 install git+https://github.com/moonlapse-mud/shared#egg=moonlapse-shared
```

### Packet

The Moonlapse Packet design consists of a header and a payload. The header is constructed as follows:

**Header: 32 bits**
- Flags: 8 bits
- ID: 13 bits
- Length: 11 bits

```
   Flags           ID             Length
+---------++----------------++-------------+
 0000 0000  0000 0000 0000 0  000 0000 0000
```

This allows up to 8 flags to be set, 8192 possible unique packet IDs, and a max payload length of 2048.

Note that the length in the header refers to the length of the payload, not the entire packet.

#### New Packet Types

Any new packet type being made must follow these standards:

* They must be defined in `packet.py` above the line that contains the comment: `# ALL PACKETS MUST LIVE ABOVE THIS LINE`
    - This is because the global `from_bytes` function uses reflection and requires the packet types already defined.

* They must inherit `Packet` and override the `pid` member. `pid` is a unique integer between 0 and 8192, which correlates to the unique packet ID.

* You can define any new members in the packet constructor, but any members that are of type `Field` will be included in the bytes when using `to_bytes`.

* `to_bytes` will attach the header information and then any field in order of declaration.

#### Other Packet Info and Tips

* `len(Packet)` will return the size in bytes of all of its `Field` members.

* You can iterate over a Packet. It will simply iterate through the `Field` members.

* Equality has been overrided.


### Fields

Fields are the building blocks of Packets. They consist only of a `size` member and a `value` member, which may depend on the type of Field.

#### Other Field Info and Tips

* `len(Field)` will return the size in bytes of this Field. It is equal to `size`.

* You can quickly take the value of a `Field` by applying the unary negate operator ~
    - e.g.
    ```python
    f = CharField(4)
    assert ~f == 4
    ```

