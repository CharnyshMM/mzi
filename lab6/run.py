from gost341012 import EllipticCurve, sign, verify
from keygen import generate_keys
import params
from gost341112 import GOST341112 # Стрибог (хэш-функция по ГОСТ Р 34.11-2012)

message = "123456"

hashed_message = GOST341112(data=bytes(message, "utf-8")).digest()

E = EllipticCurve(*(params.CURVES[0]))
public_key, private_key = generate_keys(E)

print('Public key:', public_key)
print('Private key:', private_key)

signature = sign(E, private_key, hashed_message)
print('Signature', signature)

print('Verification: ', verify(E, public_key, hashed_message, signature))
