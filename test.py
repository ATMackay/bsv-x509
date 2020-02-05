# Test pieces of the code
import libsecp256k1 
import unittest
import x509_builder
import network
import transaction

# Example Transaction IDS 
tx_id = "81d29f7cd268249d33e617e511221718ac2b955a1b3f0a3b915e122bd904bb3e"
tx_id2 = "5f40fa5a4291b369035cb65d2a0086c3e3b05f7e95efca0682a418f6929dec0b"

# libsecp256k1 Unittest
#privkey = libsecp256k1.libsecp().private_key()
#pubkey = libsecp256k1.libsecp().point_mul(privkey, secp_G)
#hex_pubkey = libsecp256k1.libsecp().public_key_hex(pubkey)
#comp_pubkey = libsecp256k1.libsecp().compress_key(pubkey)
#comp_hex_pubkey = libsecp256k1.libsecp().compress_key(hex_pubkey)
#wif_key = libsecp256k1.libsecp().wif(privkey)

#print("Private Key:", privkey)
#print("Public Key:", pubkey)
#print("Public Key (hex):", hex_pubkey)
#print("Compressed public key:", comp_pubkey)
#print("Compressed (hex) public key:", comp_hex_pubkey)
#print("Compression equality:", comp_pubkey == comp_hex_pubkey)
#print("Decompressed public key:", libsecp().decompress_key(comp_pubkey))
#print("Decompressed key length:", len(libsecp().decompress_key(comp_pubkey)))
#print("Decompressed key = pubkey:", libsecp().decompress_key(comp_pubkey) == pubkey)
#print("WIF private key:", wif_key)
#print("decoded WIF key:", libsecp().decode_wif(wif_key))


# Network Unit Test
#print(network.retrieve_tx(tx_id), "\n \n")
#print(transaction.get_pubkeys(tx_id))
#print(extract_nulldata(tx_id2, 0), "\n \n")

# x509 unit test
test_cert = x509_builder.cert_data('a','a','a')
formatted_cert = x509_builder.json_format(test_cert)
h = x509_builder.hex_encode(formatted_cert)
d = x509_builder.hex_to_json(h)
print(test_cert)
print(formatted_cert)
print('\n\n', h)
print('\n\n', d)
