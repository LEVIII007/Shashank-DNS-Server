import socket
import struct

class DNSHeader:
    def __init__(self):
        self.id = 1234                          # Packet Identifier
        self.qr = 1                             # Query/Response Indicator
        self.opcode = 0                         # Operation Code
        self.aa = 0                             # Authoritative Answer
        self.tc = 0                             # Truncation
        self.rd = 0                             # Recursion Desired
        self.ra = 0                             # Recursion Available
        self.z = 0                              # Reserved
        self.rcode = 0                          # Response Code
        self.qdcount = 0                        # Question Count
        self.ancount = 0                        # Answer Record Count
        self.nscount = 0                        # Authority Record Count
        self.arcount = 0                        # Additional Record Count

    def to_bytes(self):
        # Convert the header fields into bytes
        return struct.pack('>HBBHHHHHHHH',
                           self.id,
                           (self.qr << 7),
                           (self.opcode << 3),
                           (self.aa << 2),
                           (self.tc << 1),
                           (self.rd),    # Flags
                           0,                               # Unused
                           self.qdcount,
                           self.ancount,
                           self.nscount,
                           self.arcount)

def main():
    print("Logs from your program will appear here!")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            print(f"Received packet from {source}")

            # Create DNS header
            header = DNSHeader()
            response = header.to_bytes()

            # Send response back to the source
            udp_socket.sendto(response, source)
            print(f"Sent response to {source}")

        except Exception as e:
            print(f"Error receiving data: {e}")
            break

if __name__ == "__main__":
    main()
