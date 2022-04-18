from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

key = RSA.generate(1024)
private_key = key.export_key()

test = "hello"

public_key = key.publickey().export_key()

pkey = RSA.importKey(public_key)
prkey = RSA.importKey(private_key)

print("Private key", private_key)
print(type(private_key))


#Testing RSA

print("Public key", public_key)
cipher = PKCS1_OAEP.new(pkey)
ciphertext = cipher.encrypt(test.encode())

print("Cipher Text: ", ciphertext)

cipher2 = PKCS1_OAEP.new(prkey)
pltext = cipher2.decrypt(ciphertext)

print("Plain Text: ", pltext.decode())


print("***********************************************************************\n**********************Signing***********************")

#Test Signing

hashed = SHA256.new(test.encode())

signer = pkcs1_15.new(prkey)
sig = signer.sign(hashed)
print("Signed hash: ", sig)


hash2 = SHA256.new(test.encode())
try:
    pkcs1_15.new(pkey).verify(hash2, sig)
    print("Valid")
except (ValueError, TypeError):
    print("invalid")

#Create keys A

# key = RSA.generate(1024)
# private_key = key.export_key()
# file_out = open("S-private.key", "wb")
# file_out.write(private_key)
# file_out.close()
#
# public_key = key.publickey().export_key()
# file_out = open("S-public.key", "wb")
# file_out.write(public_key)
# file_out.close()





