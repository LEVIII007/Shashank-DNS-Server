import struct

def encode_domain_name(domain):
    # Encode domain name according to DNS specifications
    labels = domain.split('.')
    encoded = b''
    for label in labels:
        length = len(label)
        encoded += struct.pack('B', length) + label.encode()
    encoded += b'\x00'  # Null byte to terminate the domain name
    return encoded