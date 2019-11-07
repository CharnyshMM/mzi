def save_keys_to_file(filename, *keys):
     with open(filename, 'w', encoding="utf-8") as f:
        for k in keys:
          f.write(f'{str(k)}\n')
        

def save_chars_to_file(filename, chars_list, separator=None):
    with open(filename, "w", encoding="utf-8") as f:
        for char in chars_list:
            f.write(str(char))
            if (separator):
                f.write(separator)


def read_n_keys_from_file(filename, n):
    keys = []
    with open(filename, "r") as f: 
        for _ in range(n):
            keys.append(int(f.readline()))
    return (*keys,)

