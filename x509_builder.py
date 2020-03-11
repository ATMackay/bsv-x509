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
ca_prefix = 'CERT'

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
        self.root_loc = '84f6ff602f81e4d7980112d260a1917fd3200f454daf92e4c1abe67971c44eac'
        self.root_vout = 0 
        # Intermediate certificate location
        self.int_cert_loc = '930382cc6584529701b9aa3c9540cbf7b756292c565dd0d233fb5f31f31af56e'
        self.int_cert_vout = 0 
        # Validity period 
        self.not_before = time.time()
        self.not_after = time.time() + 7776000 # Time + 90 days
        # Root CA
        self.root_ca = "CT-AM Certificates"
        self.root_not_after = time.time() + 630700000 # Time + 20 years
        self.root_key = '03784c9066b6afd1baa83d7391126b073f539131d67c8ef932b54f4236ace5e289'
        # Policy (intermediate) CA
        self.int_ca = "CT-AM Certificates"
        self.int_not_after = time.time() + 157680000 # Time + 5 years
        self.int_key = '03784c9066b6afd1baa83d7391126b073f539131d67c8ef932b54f4236ace5e289'
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
        preimg = self.person_name.zfill(32) + self.device_type.zfill(32)
        return hashlib.sha256(preimg.encode()).hexdigest()[0:8]

    def user_id(self):
        # Generates unique user ID from user + company
        if type(self.person_name)!= str or sys.getsizeof(self.person_name) > 16*8:
            raise Exception("Name must be a string under 16 bytes in length!")  
        if type(self.company)!= str or sys.getsizeof(self.company) > 32*8:
            raise Exception("Name must be a string under 8 bytes in length!") 
        preimg = self.person_name.zfill(32) + self.company.zfill(64)
        return hashlib.sha256(preimg.encode()).hexdigest()[0:8]

    """
    Certificate generator functions.
    """

    # CHANGE FROM LIST TO DICT!!!!!
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

        certificate = dict()
        certificate["Version number"] = str(self.version) # !!!!!!!!!!
        certificate["Serial number"] = str(self.serial)
        certificate["Issuer"] = str(self.issuer)
        certificate["Root certificate txid"] = str(self.root_loc)
        certificate["Root certificate vout"] = str(self.root_vout)
        certificate["Intermediate certificate txid"] = str(self.int_cert_loc)
        certificate["Intermediate certificate vout"] = self.int_cert_vout
        certificate["Validity period start"] = str(self.not_before)
        certificate["Validity period finish"] = str(self.not_after)
        certificate["Subject name"] = str(self.person_name)
        certificate["Subject public key"] = str(self.pubkey)
        certificate["Subject device id"] = str(device_id)
        certificate["Subject unique id"] = str(unique_id)

        return certificate



    def generate_root(self):
        # Generate root certificate 
        root_id = cert.user_id(self.root_ca, self.root_ca)
        certificate = dict()
        certificate["Version number"] = str(self.version)
        certificate["Serial number"] = str(self.serial)
        certificate["Issuer"] = str(self.issuer)
        certificate["Validity period start"] = str(self.not_before)
        certificate["Validity period finish"] = str(self.root_not_after)
        certificate["Root CA public key"] = str(self.root_key)
        certificate[" Root CA unique id"] = str(self.root_id)

        return certificate

    def generate_int(self):
        #Generate intemediate certificate
        policy_id = cert.user_id(self.policy_ca, self.policy_ca)
        certificate = dict()
        certificate["Version number"] = str(self.version)
        certificate["Serial number"] = str(self.serial)
        certificate["Issuer"] = str(self.issuer)
        certificate["Validity period start"] = str(self.not_before)
        certificate["Validity period finish"] = str(self.int_not_after)
        certificate["Policy CA public key"] = str(self.int_key)
        certificate["Policy CA unique id"] = str(self.policy_id)

        return certificate

    """
    Certificate viewing functions.
    """
       
    def get_size(self, _cert):
        # returns memory size of certificate in bytes
        return sys.getsizeof(_cert)

    def json_format(self, _cert):
        # Input certificate array object
        if len(_cert) > 13:
            raise Exception('input must be an array of length 12 containing strings.')
        return json.dumps(_cert, indent = 4)




