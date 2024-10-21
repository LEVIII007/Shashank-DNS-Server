import socket
import struct
from question import IDNSQuestion, DNSQuestionType, DNSClass, DNSQuestion
from header import DNSHeader  # Assuming DNSHeader handles header section generation
from answer import DNSAnswer  # Assuming DNSAnswer for the answer section

def parse_domain_name(data, offset):
    labels = []
    while True:
        length = data[offset]
        if length == 0:
            offset += 1
            break
        labels.append(data[offset + 1:offset + 1 + length].decode())
        offset += length + 1
    domain_name = ".".join(labels)
    return domain_name, offset

def parse_questions(data, offset):
    questions = []
    q_count = struct.unpack(">H", data[4:6])[0]  # Extract question count from the header
    for _ in range(q_count):
        domain_name, offset = parse_domain_name(data, offset)
        qtype = struct.unpack(">H", data[offset:offset + 2])[0]  # Type (A = 1)
        qclass = struct.unpack(">H", data[offset + 2:offset + 4])[0]  # Class (IN = 1)
        questions.append((domain_name, qtype, qclass))
        offset += 4  # Move past the QTYPE and QCLASS
    return questions, offset


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            # Receive the DNS query packet
            buf, source = udp_socket.recvfrom(512)  # Receive up to 512 bytes
            print(f"Received packet from {source}")
            print(f"Data: {buf}")

            # Parse the packet header (first 12 bytes are the DNS header)
            query_id = struct.unpack(">H", buf[:2])[0]  # Extract Packet ID (first 2 bytes)
            flags = struct.unpack(">H", buf[2:4])[0]    # Extract flags (2nd 2 bytes)

            print(f"Query ID: {query_id}")
            # Extract key bits from the flags
            qr = (flags >> 15) & 0x1       # Query/Response Indicator (bit 16)
            opcode = (flags >> 11) & 0xF   # Operation Code (bits 12-15)
            aa = (flags >> 10) & 0x1       # Authoritative Answer (bit 11)
            tc = (flags >> 9) & 0x1        # Truncation (bit 10)
            rd = (flags >> 8) & 0x1        # Recursion Desired (bit 9)

            print(f"QR: {qr}, Opcode: {opcode}, AA: {aa}, TC: {tc}, RD: {rd}")

            # Determine RCODE based on OPCODE
            if opcode == 0:
                rcode = 0  # No error for standard queries
            else:
                rcode = 4  # Not implemented for any other OPCODE

            # Set response-specific flags
            qr = 1  # It's a response
            aa = 0  # Not authoritative
            tc = 0  # No truncation
            ra = 0  # Recursion Available is always 0 in this case

            # Parse the question section
            offset = 12  # Start after the DNS header (12 bytes)
            questions, offset = parse_questions(buf, offset)  # Correct parsing of questions

            print(f"Parsed Questions: {questions}")

            # Construct the response header
            header = DNSHeader(
                packet_id=query_id,
                qr=qr, opcode=opcode, aa=aa, tc=tc,
                rd=rd, ra=ra, rcode=rcode
            )

            print(f"Response header: {header}")

            response = header.to_bytes()

            # For each parsed question, we will construct the answer section
            for domain_name, qtype, qclass in questions:
                # Add the uncompressed question section
                question = IDNSQuestion(name=domain_name, qtype=DNSQuestionType.A, qclass=DNSClass.IN)
                question_bytes = DNSQuestion.write(question)
                response += question_bytes

                # Add the answer section (hardcoded IP address)
                answer = DNSAnswer(name=domain_name, rtype=DNSQuestionType.A.value, rclass=DNSClass.IN.value, ttl=60, rdata="8.8.8.8")
                answer_bytes = answer.to_bytes()
                response += answer_bytes

            print(f"Final Response: {response}")

            # Send the response back to the source
            udp_socket.sendto(response, source)
            print(f"Sent response to {source}")

        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()
