from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from typing import Any, Union

def generate_key_pair() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def calculate_hash(message: bytes, hash_algorithm: Any = hashes.SHA256()) -> bytes:
    digest = hashes.Hash(hash_algorithm)
    digest.update(message)
    return digest.finalize()

def sign_message(hash_result: bytes, private_key: rsa.RSAPrivateKey,
                 mgf: Any, salt_length: int,
                 padding_algorithm: Any) -> bytes:
    signature = private_key.sign(
        hash_result,
        padding=padding_algorithm(
            mgf=mgf,
            salt_length=salt_length
        ),
        algorithm=hashes.SHA256()
    )
    return signature

def verify_signature(message: bytes, signature: bytes, public_key: rsa.RSAPublicKey,
                     mgf: Any, salt_length: int,
                     padding_algorithm: Any) -> bool:
    hash_result = calculate_hash(message)
    try:
        public_key.verify(
            signature,
            hash_result,
            padding=padding_algorithm(
                mgf=mgf,
                salt_length=salt_length
            ),
            algorithm=hashes.SHA256()
        )
        return True
    except Exception:
        return False

# Example usage:
private_key, public_key = generate_key_pair()
message_to_sign = b"Hello, digital signatures!"

# Calculate hash
hash_result = calculate_hash(message_to_sign)

# Specify parameters for PSS padding
mgf = padding.MGF1(hashes.SHA256())
salt_length = padding.PSS.MAX_LENGTH
padding_algorithm = padding.PSS

# Sign the message
signature = sign_message(hash_result, private_key, mgf, salt_length, padding_algorithm)

# Verify the signature
is_valid_signature = verify_signature(message_to_sign, signature, public_key, mgf, salt_length, padding_algorithm)

print("Signature is valid." if is_valid_signature else "Signature is invalid.")
