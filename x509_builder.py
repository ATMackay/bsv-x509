# This programme contaisn a class of functions generates an X.512 certificate 
import time
import sys
import json
import numpy as np
import hashlib
import binascii
import random
import libsecp256k1

# Hard coded parameters
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

def gen_device_id(person_name, device_type):
    # Generates unique device ID from user + device name
    if type(person_name)!= str or len(person_name) > 32:
        raise Exception("Name must be a string of up to 32 characters!")  
    if type(device_type)!= str or len(device_type) > 32:
        raise Exception("Device type must be a string of up to 32 characters!")
    # Pad entries with 0 to format  
    person_name = person_name.zfill(32)
    device_type = device_type.zfill(32)
    preimg = person_name + device_type
    return hashlib.sha256(preimg.encode()).hexdigest()[0:8]

def user_id(person_name, company):
    # Generates unique user ID from user + company
    if type(person_name)!= str or sys.getsizeof(person_name) > 16*8:
        raise Exception("Name must be a string under 16 bytes in length!")  
    if type(company)!= str or sys.getsizeof(company) > 32*8:
        raise Exception("Name must be a string under 8 bytes in length!") 
    person_name = person_name.zfill(32)
    company = company.zfill(64)
    preimg = person_name + company
    return hashlib.sha256(preimg.encode()).hexdigest()[0:8]

# Certificate functions

def key_gen():
    priv_key = libsecp256k1.libsecp().private_key()
    pubkey = libsecp256k1.libsecp().point_mul(priv_key, libsecp256k1.secp_G)
    hex_pubkey = libsecp256k1.libsecp().public_key_hex(pubkey)
    return hex_pubkey

def encrypt(hex_cert, enc_key):
    raise Exception("Encryption not currently supported")
    # Does AES symmetric encryption of hex encoded formatted certificate
    if type(hex_cert) != hex:
        raise Excpetion("Certificate not formatted correctly for encryption.")
    #AES/BIE1 Encryption
    return 0

def cert_data(certified_party, company, device_type):
    # generates an array object containing certificate entries
    if type(certified_party) != str or sys.getsizeof(certified_party) > 128*8:
        raise Exception("Subject name must be a string object up to 128 bytes!")
    if type(company) != str or sys.getsizeof(company) > 34*8:
        raise Exception("Subject device ID must be a string object up to 32 bytes!")
    if type(device_type) != str or sys.getsizeof(device_type) > 34*8:
        raise Exception("Subject ID must be a string object up to 32 bytes!")
    device_id = gen_device_id(certified_party, device_type)
    unique_id = user_id(certified_party, company)


    certificate_data = list()
    certificate_data.append(version)
    certificate_data.append(serial)
    certificate_data.append(issuer)
    certificate_data.append(root_loc)
    certificate_data.append(root_vout)
    certificate_data.append(int_cert_loc)
    certificate_data.append(int_cert_vout)
    certificate_data.append(not_before)
    certificate_data.append(not_after)
    certificate_data.append(certified_party)
    certificate_data.append(key_gen())
    certificate_data.append(device_id)
    certificate_data.append(unique_id)

    return certificate_data
    

def generate(certified_party, company, device_type):
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



def get_size(cert_):
    # returns memory size of certificate in bytes
    return sys.getsizeof(cert_)

def json_format(cert_):
    # Input certificate array object
    if len(cert_) > 13:
        raise Exception('input must be an array of length 12 containing strings.')
    return json.dumps(cert_)

def hex_encode(cert_):
    serialized_obj = ''
    for i in range(len(cert_)):
        serialized_obj += str(cert_[i])
    # ASCII conversion
    return binascii.hexlify(serialized_obj.encode())

def hex_to_json(hex_cert):
    # Input formatted Hex encoded certificate
    # Outout a json object containing certificate
    decode = binascii.unhexlify(hex_cert)
    return decode









