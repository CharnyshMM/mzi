# RSA lab

## USAGE: 

  * **encryption:** `python rsa.py enc filename_to_read [filename_to_take_keys_from]`
  * **decryption:** `python rsa.py dec filename_to_read filename_to_take_keys_from`

### Notes on commands:

  - data to process is read from filename_to_read file as unicode string
  - if you do not specify a filename_to_take_keys_from on encryption operation, 
  then the script will generate public_keys.txt and private_keys.txt automatically.

### Keys file format:

keys file format is (two ints separated with linebreak):  
- the 1st int number is Module, the 2nd is public or private exponent

      1628537
      1331305

    