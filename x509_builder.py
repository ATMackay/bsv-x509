# This programme contaisn a class of functions generates an X.512 certificate 
import time
import sys
import json
import numpy as np
import hashlib
import binascii
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
class cert(object): 
    certificate_length = 7
    """This class contains functions that generate, encrypt and encode X.509 fields"""
    # 4-byte version number
    version = 3
    # 16-byte serial number 
    serial = 123456
    # Certificate issuer 
    issuer = "ATMackay Certificates"
    # Root certificate location
    root_loc = '5a743f68a759bda8fecfc4aab4af4d8e75e300d2c880ebbef25abbd21680eaec'
    root_vout = 0 
    # Intermediate certificate location
    int_cert_loc = '17a8b9994f1e89855b34660ea1d17061ae65833f1ded395c4c6a72d2d98832a6'
    int_cert_vout = 0 
    # Validity period 
    not_before = time.time()
    not_after = time.time() + 7776000 # Time + 90 days
    # subject public key info
        # These are inputs

    def key_gen(self):
        priv_key = libsecp256k1.libsecp().private_key()
        pubkey = libsecp256k1.libsecp().point_mul(priv_key, libsecp256k1.secp_G)
        hex_pubkey = libsecp256k1.libsecp().public_key_hex(pubkey)
        return hex_pubkey

    def encrypt(self, hex_cert, enc_key):
        # Does AES symmetric encryption of hex encoded formatted certificate
        if type(hex_cert) != hex:
            raise Excpetion("Certificate not formatted correctly for encryption.")

        #AES/BIE1 Encryption
        return 0

    def cert_data(self, certified_party, device_id, unique_id):
        # generates an array object containing certificate entries
        if type(certified_party) != str or sys.getsizeof(certified_party) > 128*8:
            raise Exception("Subject name must be a string object up to 128 bytes!")
        if type(device_id) != str or sys.getsizeof(device_id) > 34*8:
            raise Exception("Subject device ID must be a string object up to 32 bytes!")
        if type(unique_id) != str or sys.getsizeof(unique_id) > 34*8:
            raise Exception("Subject ID must be a string object up to 32 bytes!")
        certificate_data = list()
        certificate_data.append(cert().version)
        certificate_data.append(cert().serial)
        certificate_data.append(cert().issuer)
        certificate_data.append(cert().root_loc)
        certificate_data.append(cert().root_vout)
        certificate_data.append(cert().int_cert_loc)
        certificate_data.append(cert().int_cert_vout)
        certificate_data.append(cert().not_before)
        certificate_data.append(cert().not_after)
        certificate_data.append(certified_party)
        certificate_data.append(cert().key_gen())
        certificate_data.append(device_id)
        certificate_data.append(unique_id)

        return certificate_data
        

    def generate(self, certified_party, device_id, unique_id):
        # generates an array object containing certificate entries with labels 
        if type(certified_party) != str or sys.getsizeof(certified_party) > 128*8:
            raise Exception("Subject name must be a string object up to 128 bytes!")
        if type(device_id) != str or sys.getsizeof(device_id) > 34*8:
            raise Exception("Subject device ID must be a string object up to 32 bytes!")
        if type(unique_id) != str or sys.getsizeof(unique_id) > 34*8:
            raise Exception("Subject ID must be a string object up to 32 bytes!")
        certificate = list()
        c_data = cert().cert_data(certified_party, device_id, unique_id)
        certificate.append('Version number: '+str(c_data[0]))
        certificate.append('Serial number: '+str(c_data[1]))
        certificate.append('Issuer: '+str(c_data[2]))
        certificate.append('Root certificate txid: '+str(c_data[3]))
        certificate.append('Root certificate vout: '+str(c_data[4]))
        certificate.append('Intermediate certificate txid: '+str(c_data[5]))
        certificate.append('Intermediate certificate vout: '+str(c_data[6]))
        certificate.append('Validity period start: '+str(c_data[7]))
        certificate.append('Validity period finish: '+str(c_data[8]))
        certificate.append('Subject name: '+str(certified_party))
        certificate.append('Subject public key: '+str(c_data[10]))
        certificate.append('Subject device id: '+str(device_id))
        certificate.append('Subject unique id: '+str(unique_id))

        return certificate



    def get_size(self, cert):
        # returns memory size of certificate in bytes
        return sys.getsizeof(cert)

    def _format(self, cert):
        # Input certificate array object
        if len(cert) > 13:
            raise Exception('input must be an array of length 12 containing strings.')
        return json.dumps(cert)

    def hex_encode(self, cert_):
        serialized_obj = ''
        for i in range(len(cert_)):
            serialized_obj += str(cert_[i])
        # ASCII conversion
        return binascii.hexlify(serialized_obj.encode())

    def base64_encode(self, formatted_cert):
        # Input string contaning generated certificate 
        # Output Base64 encoding

        return encoded_cert

    def hex_decode(hex_cert):
        # Input formatted Base64 or Hex encoded certificate
        return 0






