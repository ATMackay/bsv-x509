# This programme contaisn a class of functions generates an X.512 certificate 
import time
import sys
import json
import numpy as np
import hashlib
import binascii
import random
import libsecp256k1
import transaction

#Hard coded variables
ca_prefix = '424430a'

class cert(object):
    def __init__(self, person_name, device_type, company, pubkey):
        # Hard coded parameters
        self.certificate_length = 7
        """This class contains functions that generate, encrypt and encode X.509 fields"""
        # 4-byte version number
        self.version = 3
        # 16-byte serial number 
        self.serial = 123456
        # Certificate issuer 
        self.issuer = "CT-AM Certificates"
        # Root certificate location
        self.root_loc = '5a743f68a759bda8fecfc4aab4af4d8e75e300d2c880ebbef25abbd21680eaec'
        self.root_vout = 0 
        # Intermediate certificate location
        self.int_cert_loc = '17a8b9994f1e89855b34660ea1d17061ae65833f1ded395c4c6a72d2d98832a6'
        self.int_cert_vout = 0 
        # Validity period 
        self.not_before = time.time()
        self.not_after = time.time() + 7776000 # Time + 90 days

        # Root CA
        self.root_ca = "CT-AM Certificates"
        self.root_not_after = time.time() + 630700000 # Time + 20 years
        self.root_key = '033b8143795af7ff119608282fe496ed5e7bbd87eecf43200e41892ba4088a00b'

        # Subject Key info
        self.pubkey = pubkey

        #Field format size
        self.f_format  = [4, 8, 32, 64, 4, 64, 4, 32, 18, 18, 66, 8, 8] 
        self.f_format_root  = [4, 8, 32, 18, 18, 66, 8] 

        # Input variables
        self.person_name = person_name
        self.device_type = device_type
        self.company = company

    def gen_device_id(self):
        # Generates unique device ID from user + device name
        if type(self.person_name)!= str or len(self.person_name) > 32:
            raise Exception("Name must be a string of up to 32 characters!")  
        if type(self.device_type)!= str or len(self.device_type) > 32:
            raise Exception("Device type must be a string of up to 32 characters!")
        # Pad entries with 0 to format  
        self.person_name = self.person_name.zfill(32)
        self.device_type = self.device_type.zfill(32)
        preimg = self.person_name + self.device_type
        return hashlib.sha256(preimg.encode()).hexdigest()[0:8]

    def user_id(self):
        # Generates unique user ID from user + company
        if type(self.person_name)!= str or sys.getsizeof(self.person_name) > 16*8:
            raise Exception("Name must be a string under 16 bytes in length!")  
        if type(self.company)!= str or sys.getsizeof(self.company) > 32*8:
            raise Exception("Name must be a string under 8 bytes in length!") 
        preimg = self.person_name.zfill(32) + self.company.zfill(64)
        return hashlib.sha256(preimg.encode()).hexdigest()[0:8]

    # Certificate functions
        

    def generate(self):
        # generates an array object containing certificate entries with labels 
        if type(self.person_name) != str or sys.getsizeof(self.person_name) > 128*8:
            raise Exception("Subject name must be a string object up to 128 bytes!")
        if type(self.company) != str or sys.getsizeof(self.company) > 34*8:
            raise Exception("Subject device ID must be a string object up to 32 bytes!")
        if type(self.device_type) != str or sys.getsizeof(self.device_type) > 34*8:
            raise Exception("Subject ID must be a string object up to 32 bytes!")
        # add checksum check
        if type(self.pubkey) != str or self.pubkey[0] != '1' or len(self.pubkey) > 36:
            raise Exception("Public key not formatted correctly.")

        device_id = cert.gen_device_id(self)
        unique_id = cert.user_id(self)

        certificate = list()
        certificate.append('Version number: '+str(self.version))
        certificate.append('Serial number: '+str(self.serial))
        certificate.append('Issuer: '+str(self.issuer))
        certificate.append('Root certificate txid: '+str(self.root_loc))
        certificate.append('Root certificate vout: '+str(self.root_vout))
        certificate.append('Intermediate certificate txid: '+str(self.int_cert_loc))
        certificate.append('Intermediate certificate vout: '+str(self.int_cert_vout))
        certificate.append('Validity period start: '+str(self.not_before))
        certificate.append('Validity period finish: '+str(self.not_after))
        certificate.append('Subject name: '+str(self.person_name))
        certificate.append('Subject public key: '+str(self.pubkey))
        certificate.append('Subject device id: '+str(device_id))
        certificate.append('Subject unique id: '+str(unique_id))


        return certificate



    def generate_root(self):
        # Clean up 
        root_id = cert.user_id(self.root_ca, self.root_ca)
        certificate = list()
        certificate.append('Version number: '+str(self.version))
        certificate.append('Serial number: '+str(self.serial))
        certificate.append('Issuer: '+str(self.issuer))
        certificate.append('Validity period start: '+str(self.not_before))
        certificate.append('Validity period finish: '+str(self.root_not_after))
        certificate.append('CA Root public key: '+str(self.root_key))
        certificate.append('CA unique id: '+str(self.root_id))

        return certificate
       

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def get_size(self, _cert):
        # returns memory size of certificate in bytes
        return sys.getsizeof(_cert)

    def json_format(self, _cert):
        # Input certificate array object
        if len(_cert) > 13:
            raise Exception('input must be an array of length 12 containing strings.')
        return json.dumps(_cert, indent = 4)






"""
def root_cert_data(root_ca):
    # generates an array object containing root certificate entries
    if type(root_ca) != str or sys.getsizeof(root_ca) > 128*8:
        raise Exception("Subject name must be a string object up to 128 bytes!")

    

    certificate_data = list()
    certificate_data.append(version)
    certificate_data.append(serial)
    certificate_data.append(root_ca)
    certificate_data.append(not_before)
    certificate_data.append(root_not_after)
    certificate_data.append(root_key)
    certificate_data.append(root_id)

    return certificate_data

    #!!!!!!!!!!!!!!!!! Need to fix encoding utf-8
    def hex_encode(self, _cert):
        # JSON object to hex 
        prefix = transaction.ca_prefix
        serialized_obj = prefix
        for i in range(len(self.cert)):
            serialized_obj += str(cert_[i]).zfill(f_format[i])
        # ASCII conversion
        return serialized_obj.encode('utf-8') #binascii.hexlify(serialized_obj.encode())

    def hex_encode_root(self cert_):
        # JSON object to hex 
        prefix = transaction.ca_prefix
        serialized_obj = prefix
        for i in range(len(cert_)):
            serialized_obj += str(cert_[i]).zfill(f_format_root[i])
        # ASCII conversion
        return binascii.hexlify(serialized_obj.encode())

    def hex_to_string(hex_cert):
        # Input formatted Hex encoded certificate
        # Outout a json object containing certificate
        # CERTIFICATE NEEDS TO BE ENCODED CORRECTLY 
        decode = binascii.unhexlify(hex_cert)
        return decode

    def bytes_to_ascii(byt):
        # input bytes
        # output ascii text
        string = ''
        loop_num = len(byt)//45
        for i in range(loop_num):
            string += str(binascii.b2a_hex(byt[45*i:45*(i+1)]))
        return string 

"""






