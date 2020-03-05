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


class cert(object):
    def __init__(self, person_name, device_type, company):
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
        if type(self.device_type)!= str or len(selfdevice_type) > 32:
            raise Exception("Device type must be a string of up to 32 characters!")
        # Pad entries with 0 to format  
        self.person_name = self.person_name.zfill(32)
        self.device_type = self.device_type.zfill(32)
        preimg = self.person_name + self.device_type
        return hashlib.sha256(preimg.encode()).hexdigest()[0:8]

    def user_id(person_name, company):
        # Generates unique user ID from user + company
        if type(self.person_name)!= str or sys.getsizeof(self.person_name) > 16*8:
            raise Exception("Name must be a string under 16 bytes in length!")  
        if type(self.company)!= str or sys.getsizeof(self.company) > 32*8:
            raise Exception("Name must be a string under 8 bytes in length!") 
        preimg = self.person_name.zfill(32) + self.company.zfill(64)
        return hashlib.sha256(preimg.encode()).hexdigest()[0:8]

    # Certificate functions
        

    def generate(self):
        certified_party, company, device_type = self., cert_data[11], cert_data[12]
        # generates an array object containing certificate entries with labels 
        if type(certified_party) != str or sys.getsizeof(certified_party) > 128*8:
            raise Exception("Subject name must be a string object up to 128 bytes!")
        if type(company) != str or sys.getsizeof(company) > 34*8:
            raise Exception("Subject device ID must be a string object up to 32 bytes!")
        if type(device_type) != str or sys.getsizeof(device_type) > 34*8:
            raise Exception("Subject ID must be a string object up to 32 bytes!")
        device_id = gen_device_id(certified_party, device_type)
        unique_id = user_id(certified_party, company)

        certificate = list()
        certificate.append('Version number: '+str(cert_data[0]))
        certificate.append('Serial number: '+str(cert_data[1]))
        certificate.append('Issuer: '+str(cert_data[2]))
        certificate.append('Root certificate txid: '+str(cert_data[3]))
        certificate.append('Root certificate vout: '+str(cert_data[4]))
        certificate.append('Intermediate certificate txid: '+str(cert_data[5]))
        certificate.append('Intermediate certificate vout: '+str(cert_data[6]))
        certificate.append('Validity period start: '+str(cert_data[7]))
        certificate.append('Validity period finish: '+str(cert_data[8]))
        certificate.append('Subject name: '+str(certified_party))
        certificate.append('Subject public key: '+str(cert_data[10]))
        certificate.append('Subject device id: '+str(device_id))
        certificate.append('Subject unique id: '+str(unique_id))

        # Create certificate list 
        self._cert = certificate

        return self._cert



    def generate_root(self):
        # Clean up 
        root_id = cert.user_id(self.root_ca, self.root_ca)
        certificate = list()
        certificate.append('Version number: '+str(self.version))
        certificate.append('Serial number: '+str(self.serial))
        certificate.append('Issuer: '+str(self.issuer))
        certificate.append('Validity period start: '+str(self.not_before))
        certificate.append('Validity period finish: '+str(self.not_after))
        certificate.append('CA Root public key: '+str(self.root_key))
        certificate.append('CA unique id: '+str(self.root_id))

        self._cert = certificate
        return self._cert
       

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def get_size(self):
        # returns memory size of certificate in bytes
        
        return sys.getsizeof(self._cert)

    def json_format(self):
        # Input certificate array object
        if len(self._cert) > 13:
            raise Exception('input must be an array of length 12 containing strings.')
        return json.dumps(self._cert, indent = 4)


    #!!!!!!!!!!!!!!!!! Need to fix encoding utf-8
    def hex_encode(cert_):
        # JSON object to hex 
        prefix = transaction.ca_prefix
        serialized_obj = prefix
        for i in range(len(cert_)):
            serialized_obj += str(cert_[i]).zfill(f_format[i])
        # ASCII conversion
        return serialized_obj.encode('utf-8') #binascii.hexlify(serialized_obj.encode())

    def hex_encode_root(cert_):
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
"""






