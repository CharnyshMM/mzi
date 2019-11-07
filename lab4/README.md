# EL-GAMAL scheme lab 

## USAGE: 
  * **demo run** `python el_gamal.py demo`
  * **encryption:** `python el_gamal.py enc filename_to_read [filename_to_take_keys_from]`
  * **decryption:** `python el_gamal.py dec filename_to_read filename_to_take_keys_from`

### Notes on commands:

  - data to process is read from filename_to_read file as unicode symbols
  - if you do not specify a filename_to_take_keys_from on encryption operation, 
  then the script will generate and use public_keys.txt and private_keys.txt automatically.

### Keys file format:

keys file format is (two ints separated with linebreak):  
- *public keys*: the 1st int number is _P_, the 2nd is _G_, the 3rd is _Y_

      95369
      35392
      15389

- *private keys*: the 1st int number is _P_, the 2nd is _X_

      95369
      2660


## Prime numbers note
- `primes.txt` file is required to be in the same directory with `el_gamal.py` file.
- prime numbers are taken from `primes.txt` file using python default random module
- Lower bound and upper bound for choosing a prime number are defined in `rsa.py` as R_LO & R_HI constants. Their values are _INDEXES_ of prime numbers from the file, not the real number bounds
- the bigger are primes the slower script works :)

    
