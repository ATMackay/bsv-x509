# This programme contains functions and classes for secp256k1 elliptic curve cryptography
import numpy as np
import hashlib
import random
from getpass import getpass

#Hard coded varaibles
# secp256k1 parameters
secp_G = [int("79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798", 16),\
     int("483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8", 16)]
secp_n = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141", 16)
secp_p = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F", 16)
secp_a = int(0)
secp_b = int(7)
secp_inf_point = [0, 0]

sym_key_n = int(2**512)



def bin_array(integer):
    # Returns a binarry array representation of a positive intger
    if type(integer)!= int or integer < 0:
        raise Exception("input must be a positive integer!")
    return [int(x) for x in bin(integer)[2:]]

def mod_inv(num,modulus):
    # finds inverse of a modulo p, assummes a and p are coprime
    if num <= 0 or num > secp_p or type(num) != int:
        raise Exception("input must be an integer between 1 and modulus")
    if num == 1:
        return a


    # Find gcd using Extended Euclid's Algorithm
    gcd, x, y = extended_euclid_gcd(num, modulus)


    # In case x is negative, we handle it by adding extra M
    # Because we know that multiplicative inverse of A in range M lies
    # in the range [0, M-1]
    if x < 0:
        x += modulus    
    return x   
 
def extended_euclid_gcd(a, b):
    """
    Returns a list `result` of size 3 where:
    Referring to the equation ax + by = gcd(a, b)
        result[0] is gcd(a, b)
        result[1] is x
        result[2] is y 
    """
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a
    while r != 0:
        quotient = old_r//r 
        # In Python, // operator performs integer or floored division
        # This is a pythonic way to swap numbers
        # See the same part in C++ implementation below to know more
        old_r, r = r, old_r - quotient*r
        old_s, s = s, old_s - quotient*s
        old_t, t = t, old_t - quotient*t
    return [old_r, old_s, old_t]    


def password_check():
    return getpass()
    

# secp256k1
class libsecp(object):

    def private_key(self):
        return random.randint(1,secp_n)
           
    def public_key(self,priv_key):
        return point_mul(priv_key, secp_G)

    def wif(self,priv_key):
        prefix = "L"
        base58_enc = 0
        result = 0
        return result 

    def decode_wif(self,priv_key_string):
        priv_key = priv_key_string

    def point_double(self, A):
        return point_add(A,A)

    def point_add(self, A, B):
        # input 2 elliptic curve points
        if A==secp_inf_point or B== secp_inf_point:
            return B
        if B == secp_inf_point:
            return A
        if len(A)!=2 or len(B)!=2:
            raise Exception("public key must be an array of length 2!")
        if type(A[0]) != int or type(B[0]) != int:
            raise Exception("EC curve point must be an array of integers!")
        if A[0] >= secp_n or A[0] < 0 or A[1] < 0 or A[1] >= secp_n:
            raise Exception("input parameter 1 outside the accepted range!")
        if B[0] >= secp_n or B[0] < 0 or B[1] < 0 or B[1] >= secp_n:
            raise Exception("input parameter 2 outside the accepted range!")

        # if A is not equal to B then use this formula
        if A!=B:
            C_x = pow(B[1]-A[1],2,secp_p)*pow(mod_inv(B[0]-A[0],secp_p),2,secp_p) - A[0] - B[0] % secp_p 
            C_y = (B[1]-A[1])*mod_inv(B[0]-A[0],secp_p)*(A[0]-C_x) - A[1] % secp_p
            return [C_x, C_y]

        # if A is equal to B then use this formula
        if A==B:
            C_x = pow(3*pow(A[0],2,secp_p) + secp_a,2,secp_p)*pow(mod_inv(2*A[1],secp_p),2,secp_p) - 2*A[0] % secp_p
            C_y = (3*pow(A[0],2,secp_p) + secp_a)*mod_inv(2*A[1],secp_p) + A[0] - C_x - A[1] % secp_p            
            return [C_x, C_y]


    def point_mul(self, m, B):
        print(m)
        if m == 0:
            return secp_inf_point
        if m == 1:
            return B   
        if len(B)!=2:
            raise Exception("public key must be an array of length 2!")
        if type(m) != int or type(B[0]) != int:
            raise Exception("EC curve point must be an array of integers!")
        if m >= secp_n or m < 0:
            raise Exception("input parameter 1 outside the accepted range!")
        if B[0] >= secp_n or B[0] < 0 or B[1] < 0 or B[1] >= secp_n:
            raise Exception("input parameter 2 outside the accepted range!")

        m_bin_array = bin_array(m)
        double_point = secp_inf_point
        for i in range(len(m_bin_array)):
            if m_bin_array==1:
                point_sum = libsecp().point_add(double_point, B)
            else: 
                double_point = libsecp().point_add(B,B) # This is not quite right!!
        return point_sum


    def compress_key(pub_key):
        if len(pub_key)!=2:
            raise Exception("public key must be an array of length 2!")
        if type(pubkey[0]) != int or type(pubkey[1]) != int:
            raise Exception("public key must be an array of integers!")
        if pubkey[0] > secp_n or pubkey[1] > secp_n or pubkey[0] < 0 or pubkey[1] > 0:
            raise Exception("public key values outside the accepted range!")
        return '0x' + str(pub_key[0])

      

def key_store(num_keys):
    for i in range(num_keys):
        privkey = libsecp256k1().private_key()
        pubkey = libsecp256k1().public_key(p_key)
        compressedkey = libsecp256k1().compress_key(pubkey)
        store.append([privkey, pubkey, compressedkey])
    return store


def symmetric_key():
    return random.randint(1, sym_key_n)

#Unittest
privkey = libsecp().private_key()
print(privkey)

pubkey = libsecp().point_mul(privkey, secp_G)
print(pubkey)

