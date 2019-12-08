# Diffie–Hellman protocol utility

# USAGE:

1. Create text file with common parameters (Elleptic CUrve initialisation parameters). The file should contain **p**, **a**, **b**, **Gx**, **Gy**, **n** values as integer numbers, each number should be placed on a new line. See `common_params.txt` file on this repo for an example
2. Run 

        $ python generate.py common_params.txt
    
    This will generate `private_key.txt` & `public_key.txt`. Keep your private key and share the public key file with the other correspondent (someone you want to communicate with). 

3. Recieve a `other_user_public_key.txt` from the other correspondent.
   
4. Run

        $ python common_params.txt private_key.txt other_user_public_key.txt

    This will generate a `symmetric_key.txt` file, that contains a key you can use for some symmetric cryptography protocol 