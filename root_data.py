"""
Root CA data. Includes hash of root certificate location information.

This file contains extremely sensitive information.
the SHA512 fingerprint of this file can be found on https://github.com/ATMackay/bsv-x509

Check that this file has not been modified by typing

    ~/$PATH/bsv-x509 sha512sum root_data.py

The value returned should match the SHA512 fingerprint given in the repository.
If not, DO NOT EXECUTE the  main program. 

"""

root_data = {
    "root certificate" : "5a743f68a759bda8fecfc4aab4af4d8e75e300d2c880ebbef25abbd21680eaec", 
    "root certificate vout" : 0
    "root address" : '18aM1rxZL5wCmTrL9MVPjN7NAWjEM2jeHV'
    "intermediate certificate" : "5a743f68a759bda8fecfc4aab4af4d8e75e300d2c880ebbef25abbd21680eaec"
    "intermediate vout" : 0 
    "intermediate address" : '18aM1rxZL5wCmTrL9MVPjN7NAWjEM2jeHV'

}