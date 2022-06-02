# Moonlapse Shared

This is the shared package between the client and server. It contains the packet specification as well as game models and static terrain information.

## Developer's Guide

This section contains minor documentation regarding how to implement the features in this repository.

### Packet

The Moonlapse Packet design consists of a header and a payload. The header is constructed as follows:

**Header: 32 bytes**
- Flags: 8 bits
- ID: 13 bits
- Length: 11 bits

```
   Flags           ID             Length
+---------++----------------++-------------+
 0000 0000  0000 0000 0000 0  000 0000 0000
```

This allows up to 8 flags to be set, 8,192 possible unique packet IDs, and a max payload length of 2048.

Note that the length in the header refers to the length of the payload, not the entire packet.