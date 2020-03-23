# bsv-x509
This program generates/validates x.509 public key certificates and publishes them to the Bitcoin SV blockchain.
To run you will need to have installed the following

* Python 3.6 or later
* bitsv

Running bsv-x509

Linux:

    1) Go the the bsv-x509 directory

        ~/$PATH/bsv-x509

<<<<<<< HEAD
    2) To execute the certificate viewer run the main.py file 
=======
    2)  Verify SHA512 fingerprint of the root data file
        
        ~/$PATH/bsv-x509 sha512sum root_data.py
>>>>>>> dev

        The return value should equal --> 61438e7699f236b229aa197175e306e55c9a369d4b7ff321ec4ad0eb91885ddd2165f5548324dfbc9e9f69fd4d3e4c19c315038bad16a621df359637457a081e  root_data.py

        If the fingerprint values do not match DO NOT EXECUTE the main program

    3)  To execute the certificate viewer program run the main.py file 

        ~/$PATH/bsv-x509 python3 main.py

    3) Follow instructions to create or validate digital certificates on the BSV blockchain

Example Transactions (WhatsOnChain.com)

* https://whatsonchain.com/tx/28487c32c7fe6e73467c07e903f25bdead33e439591e603b23bfeaf7ee5570be
* https://whatsonchain.com/tx/930382cc6584529701b9aa3c9540cbf7b756292c565dd0d233fb5f31f31af56e

© 2019 nChain Limited. All rights reserved. This software is provided without any warranties whatsoever and shall not result in the grant of any license, whether implied or otherwise. nChain Limited shall not be liable in any way for the use of the information provided herein.
