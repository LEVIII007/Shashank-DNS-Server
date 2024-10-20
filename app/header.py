import struct


ResponseCode = {
    'NO_ERROR': 0,
    'FORMAT_ERROR': 1,
    'SERVER_FAILURE': 2,
    'NAME_ERROR': 3,
    'NOT_IMPLEMENTED': 4,
    'REFUSED': 5
}

opcodes = {
    'QUERY': 0,
    'IQUERY': 1,
    'STATUS': 2
}




class DNSHeader:
    def __init__(self, packet_id):
        self.id = 1234                     # Packet Identifier (from query)
        self.qr = 1                             # Query/Response Indicator (1 for response)
        self.opcode = 0                         # Operation Code (standard query)
        self.aa = 1                             # Authoritative Answer
        self.tc = 0                             # Truncation
        self.rd = 0                             # Recursion Desired
        self.ra = 0                             # Recursion Available
        self.z = 0                              # Reserved
        self.rcode = 0                          # Response Code (no error)   0 -> no erorr, 1 -> format error, 2 -> server failure, 3 -> name error, 4 -> not implemented, 5 -> refused
        self.qdcount = 1                        # Question Count (1 question)
        self.ancount = 0                        # Answer Record Count
        self.nscount = 0                        # Authority Record Count
        self.arcount = 0                        # Additional Record Count

    def to_bytes(self):
        # Pack flags into two bytes
        flags = (self.qr << 15) | (self.opcode << 11) | (self.aa << 10) | (self.tc << 9) | (self.rd << 8)
        flags |= (self.ra << 7) | (self.z << 6) | self.rcode

        # Convert the header fields into bytes
        return struct.pack('>HHHHHH',
                           self.id,
                           flags,
                           self.qdcount,  # Ensure QDCOUNT is 1
                           self.ancount,
                           self.nscount,
                           self.arcount)