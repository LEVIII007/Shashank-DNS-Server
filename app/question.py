# dns_question.py
import struct
from enum import Enum

class DNSQuestionType(Enum):
    A = 1
    NS = 2
    CNAME = 5
    MX = 15
    AAAA = 28



class DNSClass(Enum):
    IN = 1

class IDNSQuestion:
    def __init__(self, name: str, qtype: DNSQuestionType, qclass: DNSClass):
        self.name = name
        self.qtype = qtype
        self.qclass = qclass

def encode_domain_name(name: str) -> bytes:
    labels = name.split('.')
    encoded_name = bytearray()
    
    for label in labels:
        encoded_name.append(len(label))  # Length of the label
        encoded_name.extend(label.encode('utf-8'))  # Label data

    encoded_name.append(0)  # End of the domain name
    return bytes(encoded_name)

class DNSQuestion:
    @staticmethod
    def write(question: IDNSQuestion) -> bytes:
        name = encode_domain_name(question.name)
        qtype = struct.pack('>H', question.qtype.value)  # Big-endian unsigned short
        qclass = struct.pack('>H', question.qclass.value)  # Big-endian unsigned short
        return name + qtype + qclass
