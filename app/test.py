import socket
import struct

def create_query(domain_names):
    # Build the DNS header
    packet_id = 0x1a2b  # Random ID
    flags = 0x0100  # Standard query
    qdcount = len(domain_names)  # Number of questions
    header = struct.pack('>HHHHHH', packet_id, flags, qdcount, 0, 0, 0)

    questions = b''
    for domain in domain_names:
        # Split domain into labels
        labels = domain.split('.')
        for label in labels:
            questions += struct.pack('B', len(label)) + label.encode()
        questions += struct.pack('B', 0)  # Null byte at the end of the question

        # Append QTYPE (A) and QCLASS (IN)
        questions += struct.pack('>HH', 1, 1)  # QTYPE A (1), QCLASS IN (1)

    return header + questions

def main():
    # List of domains to query
    domains = ['codecrafters.io', 'example.com']

    # Create DNS query packet
    query_packet = create_query(domains)

    # Send query to DNS server
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(query_packet, ('127.0.0.1', 2053))
    print(f"Sent query: {query_packet}")
    # Receive response
    response, _ = udp_socket.recvfrom(512)
    print(f"Received response: {response}")

if __name__ == "__main__":
    main()
