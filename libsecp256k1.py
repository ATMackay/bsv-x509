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

#Symmetric Key 
sym_key_n = int(2**512)

#Base58 and Base64 encoding 
alphabet_58 = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
base58_count = len(alphabet_58)

alphabet_64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
base64_count = len(alphabet_64)

def password_check(password_attempt):
    if type(password_attempt) != str:
        raise Exception("password input must be a string!")
    # Uses a hard-coded password hash (insecure)
    password_hash = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    if hashlib.sha256(password_attempt.encode()).hexdigest() == password_hash:
        return True
    else:   
        return False

def bin_array(integer):
    # Returns a binarry array representation of a positive intger
    if type(integer)!= int or integer < 0:
        raise Exception("input must be a positive integer!")
    return [int(x) for x in bin(integer)[2:]]

class base_58(object):		
    def encode(self, num):
	    """ Returns num in a base64-encoded string"""
	    encode = ''
	    if (num < 0):
		    return ''
	    while (num >= base58_count):	
		    mod = num % base58_count
		    encode = alphabet_58[mod] + encode
		    num = num // base58_count
	    if (num):
		    encode = alphabet_58[num] + encode
	    return encode

    def decode(self, s):
	    """Decodes the base58-encoded string s into an integer"""
	    decoded = 0
	    multi = 1
	    s = s[::-1]
	    for char in s:
		    decoded += multi * alphabet_58.index(char)
		    multi = multi * base58_count
		
	    return decoded

class base_64(object):		
    def encode(self, num):
        """ Returns num in a base58-encoded string"""
        encode = ''
        if (num < 0):
            return ''
        while (num >= base64_count):	
            mod = num % base64_count
            encode = alphabet_64[mod] + encode
            num = num // base64_count
        if (num):
            encode = alphabet_64[num] + encode
        padding = "="
        return encode + padding

    def decode(self, s):
        if s[len(s)-1]!= '=':
            raise Exception("Base64 encoded object not formatted correctly. String should end with '='.")
        s = s[:len(s)-1]
        decoded = 0
        multi = 1
        s = s[::-1]
        for char in s:
            decoded += multi * alphabet_64.index(char)
            multi = multi * base64_count	
        return decoded
    
#Integer math

class intmath(object):
    def mod_inv(self, num, modulus):
        # finds inverse of a modulo p, assummes a and p are coprime
        if  type(num) != int:
            raise Exception("Inputs must be integer values")
        if num <= 0 or num > secp_p:
            num = num % modulus
        if num == 1:
            return a


        # Find gcd using Extended Euclid's Algorithm
        gcd, x, y = intmath().extended_euclid_gcd(num, modulus)


        # In case x is negative, we handle it by adding extra M
        # Because we know that multiplicative inverse of A in range M lies
        # in the range [0, M-1]
        if x < 0:
            x += modulus    
        return x   
     
    def extended_euclid_gcd(self, a, b):
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

    def sqrtmod(self, a, p):
        """ Find a quadratic residue (mod p) of 'a'. p
            must be an odd prime and p must be equivalent to 3 mod 4.

            Solve the congruence of the form:
                x^2 = a (mod p)
            And returns x. Note that p - x is also a root.

            0 is returned if no square root exists for
            these a and p.

            The Tonelli-Shanks algorithm is used (except
            for some simple cases in which the solution
            is known from an identity). This algorithm
            runs in polynomial time (unless the
            generalized Riemann hypothesis is false).
        """
        # Simple cases
        #
        if p % 4 == 3:
            power = (p+1) // 4
            return pow(a, power , p)
        elif a == 0:
            return 0
        elif p == 2:
            return 0
        elif intmath().legendre_symbol(a, p) != 1:
            return 0
        else:
            raise Exception("exponent must be 0, 1, 2 or prime and equivalent to 3 mod 4")
 
    def legendre_symbol(self, a, p):
        """ Compute the Legendre symbol a|p using
            Euler's criterion. p is a prime, a is
            relatively prime to p (if p divides
            a, then a|p = 0)

            Returns 1 if a has a square root modulo
            p, -1 otherwise.
        """
        ls = pow(a, int((p - 1) / 2), p)
        return -1 if ls == p - 1 else ls

# secp256k1
class libsecp(object):

    def private_key(self):
        return random.randint(1,secp_n)
           
    def public_key(self, priv_key):
        if priv_key > secp_n or priv_key < 0 or type(priv_key) != int:
            raise Exception("Private key must be an integer between 1 and n.")  
        return point_mul(priv_key, secp_G)

    def public_key_hex(self, pubkey):
        if type(pubkey[0]) != int or type(pubkey[1]) != int:
            raise Exception("input must be valid (x,y) coordinate.")
        if pubkey[0] > secp_p or pubkey[0] < 0 or pubkey[1] > secp_p or pubkey[1] < 0:
            raise Exception("input must be valid secp256k1 element.") 
        pubkey_x = hex(pubkey[0])
        pubkey_y = hex(pubkey[1])       
        result  = '0x04' + str(pubkey_x[2:]).zfill(64) + str(pubkey_y[2:]).zfill(64)
        return result

    def compress_key(self, pub_key):
        """Takes a hexadecimal encoded or integer array public key
           Returns a compressed public key '0x02....' or '0x03...' """  
        if type(pub_key) == str:
            if len(pub_key) != 132:
                raise Exception("Incorrect public key formatting.")
            pub_key_x = int(pub_key[4:68], 16)
            pub_key_y = int(pub_key[68:132], 16)
        elif len(pub_key) == 2:
            pub_key_x = pub_key[0]
            pub_key_y = pub_key[1]
        else:
            raise Exception("incorrect public key formatting.")
        if pub_key_x > secp_p or pub_key_x < 0 or pub_key_y > secp_p or pub_key_y < 0:
            raise Exception("public key values outside the accepted range!")  
        if pub_key_y < secp_p // 2:
            """If the y-coordinate is less than (secp256k1) p then y is a "negative" EC point"""
            pref = '02'
        else:
            pref = '03'   
        result = '0x' + pref + str(hex(pub_key_x)[2:])
        return result

    def decompress_key(self, comp_pub_key):
        raise Exception("Not currently supported.")
        """Calculate the modular square root of x^3 + 7"""
        if len(comp_pub_key) != 68:
            raise Exception("public key must be a 32 byte string")
        if comp_pub_key[0:4]!='0x02' and comp_pub_key[0:4]!='0x03':
            raise Exception("Compressed key not formatted correctly!")
        # Convert back to integer
        pub_key_x = int(comp_pub_key[4:], 16)
        rhs = (pow(pub_key_x,3) + secp_a*pub_key_x + secp_b) % secp_p    
        y_sol1 = intmath().sqrtmod(rhs, secp_p) 
        y_sol2 = (secp_p - y_sol1)
        if pow(y_sol1, 2, secp_p) == rhs and pow(y_sol2, 2, secp_p) == rhs:
            if comp_pub_key[0:4] == '0x02':
                hex_y_neg = hex(min(y_sol1, y_sol2))
                return '0x04' + str(comp_pub_key[4:]) + hex_y_neg[2:]
            if comp_pub_key[0:4] == '0x03':
                hex_y_pos = hex(max(y_sol1, y_sol2))
                return '0x04' + str(comp_pub_key[4:]) + hex_y_pos[2:]
        else: 
            raise Exception("Decompression Failed.")

    def wif(self, priv_key):
        prefix = "L"
        base58_enc = base_58().encode(priv_key)
        result = prefix + base58_enc
        return result 

    def decode_wif(self, priv_key_string):
        if type(priv_key_string) != str or priv_key_string[0] != 'L' or len(priv_key_string) > 50:
            raise Exception("WIF private key not formatted correctly.")
        priv_key = base_58().decode(priv_key_string[1:])
        return priv_key

    def point_double(self, A):
        return point_add(A,A)

    def point_add(self, A, B):
        # input 2 elliptic curve points
        if A==secp_inf_point:
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
            C_x = (pow(B[1]-A[1],2,secp_p)*pow(intmath().mod_inv(B[0]-A[0],secp_p),2,secp_p) - A[0] - B[0]) % secp_p 
            C_y = ((B[1]-A[1])*intmath().mod_inv(B[0]-A[0],secp_p)*(A[0]-C_x) - A[1]) % secp_p
            return [C_x, C_y]

        # if A is equal to B then use this formula
        if A==B:
            C_x = (pow(3*pow(A[0],2,secp_p) + secp_a,2,secp_p)*pow(intmath().mod_inv(2*A[1],secp_p),2,secp_p) - 2*A[0]) % secp_p
            C_y = ((3*pow(A[0],2,secp_p) + secp_a)*intmath().mod_inv(2*A[1],secp_p) + A[0] - C_x - A[1] )% secp_p          
            return [C_x, C_y]


    def point_mul(self, m, B):
        if m == 0:
            return secp_inf_point
        if m == 1:
            return B   
        if len(B)!=2:
            raise Exception("public key must be an array of length 2!")
        if type(m) != int or type(B[0]) != int:
            raise Exception("EC curve point must be an array of integers!")
        if m >= secp_n or m < 0:
            raise Exception("Input parameter 1 outside the accepted range!")
        if B[0] >= secp_n or B[0] < 0 or B[1] < 0 or B[1] >= secp_n:
            raise Exception("Input parameter 2 outside the accepted range!")
        m_bin_array = bin_array(m)
        double_point = B
        point_sum = secp_inf_point
        for i in range(len(m_bin_array)):
            if m_bin_array[len(m_bin_array)-i-1]==1:
                point_sum = libsecp().point_add(double_point, point_sum)
            double_point = libsecp().point_add(double_point,double_point) # This is not quite right!!
        return point_sum


    
def key_store(num_keys):
    for i in range(num_keys):
        privkey = libsecp().private_key()
        pubkey = libsecp().public_key(privkey)

        wallet_key = libsecp().wif(privkey)
        compressedkey = libsecp256k1().compress_key(pubkey)
        store.append([wallet_key, pubkey, compressedkey])
    return store


def symmetric_key():
    return random.randint(1, sym_key_n)




