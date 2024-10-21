import struct
class DNSHeader:
    def __init__(self, packet_id, opcode, qr=0, aa=0, tc=0, rd=0, ra=0, rcode=0):
        self.packet_id = packet_id
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.rcode = rcode

    def to_bytes(self):
        flags = 0
        flags |= (self.qr << 15)
        flags |= (self.opcode << 11)
        flags |= (self.aa << 10)
        flags |= (self.tc << 9)
        flags |= (self.rd << 8)
        flags |= (self.ra << 7)
        flags |= (self.rcode & 0xF)  # Response code is in the lower 4 bits

        header = struct.pack(">HHHHHH",
                             self.packet_id,  # ID
                             flags,           # Flags
                             1,               # QDCOUNT (Number of questions)
                             1,               # ANCOUNT (Number of answers)
                             0,               # NSCOUNT (Number of authority records)
                             0)               # ARCOUNT (Number of additional records)

        return header
