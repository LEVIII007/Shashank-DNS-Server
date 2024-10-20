import struct
from enum import Enum

class DNSRecordType(Enum):
    A = 1       # A record (IPv4 address)
    NS = 2      # NS record (Name Server)
    CNAME = 5   # CNAME record (Canonical Name)
    MX = 15     # MX record (Mail Exchange)
    AAAA = 28   # AAAA record (IPv6 address)

class DNSAnswer:
    def __init__(self, name: str, rtype: int, rclass: int, ttl: int, rdata: str):
        """
        name: The domain name for the answer
        rtype: Resource record type (e.g., 1 for A record)
        rclass: Class of the resource (e.g., 1 for IN)
        ttl: Time-to-live value
        rdata: The IP address or other data in the answer section
        """
        self.name = name
        self.rtype = rtype  # Record type
        self.rclass = rclass  # Record class
        self.ttl = ttl  # Time-to-live
        self.length = 4  # Length of the RDATA field (4 bytes for IPv4)
        self.rdata = rdata  # The data (e.g., IP address)

    def to_bytes(self) -> bytes:
        # Encode domain name
        encoded_name = self.encode_domain_name(self.name)

        # Pack type, class, and TTL fields
        rtype = struct.pack('>H', self.rtype)
        rclass = struct.pack('>H', self.rclass)
        ttl = struct.pack('>I', self.ttl)

        # Convert RDATA to bytes (for A record, this will be the 4-byte IP address)
        rdata = self.encode_rdata(self.rdata)

        # RDLENGTH is the length of the RDATA (for IPv4, it's always 4 bytes)
        rdlength = struct.pack('>H', len(rdata))

        # Combine all parts to form the answer section
        return encoded_name + rtype + rclass + ttl + rdlength + rdata

    def encode_domain_name(self, name: str) -> bytes:
        """
        Encodes a domain name as a sequence of labels.
        """
        labels = name.split('.')
        encoded_name = bytearray()
        for label in labels:
            encoded_name.append(len(label))
            encoded_name.extend(label.encode('utf-8'))
        encoded_name.append(0)  # End of domain name
        return bytes(encoded_name)

    def encode_rdata(self, rdata: str) -> bytes:
        """
        Encodes RDATA for A records (IPv4 address).
        """
        return struct.pack('>BBBB', *[int(octet) for octet in rdata.split('.')])
