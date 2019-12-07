# HMAC 

# USAGE: 

    $ python hmac.py file_to_check.txt private_key_file.bin [file_with_hash_to_compare_with.bin]`

* if `file_with_hash_to_compare_with.bin` is not provided, then value of HMAC function for `file_to_check.txt` will be saved to `file_hash.bin`

# Key generation 

* To generate a key file use `keygen.py`:  

      python keygen.py