from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

# Generate RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()
print(private_key,public_key)
# Message to be signed
message = b"Hello, digital signatures!"

# Digital signing process
digest = hashes.Hash(hashes.SHA256())
digest.update(message)
hash_result = digest.finalize()
print(f"hash:{hash_result.hex(' ')},length {len(hash_result)}")
signature = private_key.sign(
    hash_result,
    padding=padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    algorithm=hashes.SHA256()
)
print(f"signature:{signature.hex(' ')},length: {len(signature)}")
# Digital signature verification process
digest = hashes.Hash(hashes.SHA256())
digest.update(message)
hash_result = digest.finalize()

try:
    public_key.verify(
        signature,
        hash_result,
        padding=padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        algorithm=hashes.SHA256()
    )
    print("Signature is valid. Message has not been tampered.")
except:
    print("Signature is invalid. Message may have been tampered.")
