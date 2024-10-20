import socket
import struct

class DNSHeader:
    def __init__(self, packet_id):
        self.id = packet_id                     # Packet Identifier (from query)
        self.qr = 1                             # Query/Response Indicator (1 for response)
        self.opcode = 0                         # Operation Code (standard query)
        self.aa = 1                             # Authoritative Answer
        self.tc = 0                             # Truncation
        self.rd = 0                             # Recursion Desired
        self.ra = 0                             # Recursion Available
        self.z = 0                              # Reserved
        self.rcode = 0                          # Response Code (no error)
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

def encode_domain_name(domain):
    # Encode domain name according to DNS specifications
    labels = domain.split('.')
    encoded = b''
    for label in labels:
        length = len(label)
        encoded += struct.pack('B', length) + label.encode()
    encoded += b'\x00'  # Null byte to terminate the domain name
    return encoded

def main():
    print("Logs from your program will appear here!")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            print(f"Received packet from {source}")

            # Extract the ID from the query packet (first 2 bytes)
            query_id = struct.unpack(">H", buf[:2])[0]

            # Create DNS header with extracted query_id
            header = DNSHeader(query_id)
            response = header.to_bytes()

            # Encode the domain name for the question section
            domain_name = "codecrafters.io"
            encoded_name = encode_domain_name(domain_name)

            # Append the question section
            question_type = struct.pack('>H', 1)  # Type A (1)
            question_class = struct.pack('>H', 1) # Class IN (1)
            response += encoded_name + question_type + question_class

            # Send response back to the source
            udp_socket.sendto(response, source)
            print(f"Sent response to {source}")

        except Exception as e:
            print(f"Error receiving data: {e}")
            break

if __name__ == "__main__":
    main()
