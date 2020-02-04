# This programme contaisn a class of functions generates an X.512 certificate 
import time
import sys
import numpy as np
import hashlib
import random
import libsecp256k1


def gen_device_id(person_name, device_type):
    if type(person_name)!= str or sys.getsizeof(person_name) > 16*8:
        raise Exception("Name must be a string under 16 bytes in length!")  
    if type(device_type)!= str or sys.getsizeof(device_type) > 8*8:
        raise Exception("Name must be a string under 8 bytes in length!")  
    person_name = person_name.zfill(16)
    device_type = device_type.zfill(8)
    preimg = person_name + device_type
    return hashlib.sha256(preimg.encode()).digest()

def user_id(person_name, company):
    if type(person_name)!= str or sys.getsizeof(person_name) > 16*8:
        raise Exception("Name must be a string under 16 bytes in length!")  
    if type(company)!= str or sys.getsizeof(company) > 32*8:
        raise Exception("Name must be a string under 8 bytes in length!") 
    person_name = person_name.zfill(16)
    company = company.zfill(32)
    preimg = person_name + company
    return hashlib.sha256(preimg.encode()).digest()

# Certificate class
class cert_x509(object): 
    certificate_length = 7
    """This class generates X.509 fields"""
    # 4-byte version number
    version = 3
    # 16-byte serial number 
    serial = 123456
    # Certificate issuer 
    issuer = "ATMackay Certificates"
    # Root certificate location
    root_loc = 0x5a743f68a759bda8fecfc4aab4af4d8e75e300d2c880ebbef25abbd21680eaec
    root_vout = 0 
    # Intermediate certificate location
    int_cert_loc = 0x17a8b9994f1e89855b34660ea1d17061ae65833f1ded395c4c6a72d2d98832a6
    int_cert_vout = 0 
    # Validity period 
    not_before = time.time()
    not_after = time.time() + 7776000 # Time + 90 days
    # subject public key info
        # These are inputs

    def key_gen(self):
        priv_key = libsecp256k1.libsecp().private_key()
        pub_key = libsecp256k1.libsecp().public_hex_key(priv_key)
        return pub_key

    def encrypt(self, hex_cert, enc_key):
        # Does AES symmetric encryption of hex encoded formatted certificate
        if type(hex_cert) != hex:
            raise Excpetion("Certificate not formatted correctly for encryption.")
        return 0

    def generate(self, certified_party, device_id, unique_id):
        if type(certified_party) != str or sys.getsizeof(certified_party) > 128:
            raise Exception("Subject name must be a string object up to 128 bytes!")
        if type(device_id) != str or sys.getsizeof(device_id) > 34:
            raise Exception("Subject name must be a string object up to 32 bytes!")
        if type(unique_id) != str or sys.getsizeof(unique_id) > 34:
            raise Exception("Subject name must be a string object up to 32 bytes!")
        certificate = dict()
        certificate[0] = cert_x509().version
        certificate[1] = cert_x509().serial
        certificate[2] = cert_x509().issuer
        certificate[3] = cert_x509().root_loc
        certificate[4] = cert_x509().root_vout
        certificate[5] = cert_x509().int_cert_loc
        certificate[6] = cert_x509().int_cert_vout
        certificate[6] = cert_x509().not_before
        certificate[6] = cert_x509().not_after
        certificate[7] = str(certified_party)
        certificate[8] = cert_x509().key_gen()
        certificate[9] = str(device_id)
        certificate[10] = str(unique_id)
        return certificate

    def x509_format(self, cert):
        # Input certificate array object
        if len(cert) != 7:
            raise Exception('input must be an array of length 10 containing certificate field objects')
        #
        return 0

    def hex_encode(self, formatted_cert):
        serialized_obj = ''
        for i in range(len(formatted_cert)):
            serialized_obj += formatted_cert[i]
        # ASCII conversion
        return 0

    def base64_encode(self, formatted_cert):
        # Input string contaning generated certificate 
        # Output Base64 encoding

        return encoded_cert

    def hex_decode(hex_cert):
        # Input formatted Base64 or Hex encoded certificate
        return 0


# Test





