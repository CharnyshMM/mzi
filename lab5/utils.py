def save_key_to_file(filename, key):
     with open(filename, 'wb') as f:
          f.write(key)


def read_key_from_file(filename):
    with open(filename, "rb") as f: 
      return f.read()

 

