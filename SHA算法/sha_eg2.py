from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from typing import Any, Union


class CryptUtil:

    @staticmethod
    def generate_key_pair() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def calculate_hash(message: bytes, hash_algorithm: Any = hashes.SHA256()) -> bytes:
        digest = hashes.Hash(hash_algorithm)
        digest.update(message)
        return digest.finalize()

    @staticmethod
    def sign_message(hash_result: bytes, private_key: rsa.RSAPrivateKey,hash_algorithm:Any,
                     padding_algorithm: Any
                     ) -> bytes:
        signature = private_key.sign(
            hash_result,
            padding=padding_algorithm,
            algorithm=hash_algorithm
        )
        return signature


    @staticmethod
    def verify_signature(hash_result: bytes, signature: bytes,
                         public_key: rsa.RSAPublicKey,
                         hash_algorithm: Any ,
                        padding_algorithm
                                 ) -> bool:
        try:
            public_key.verify(
                signature,
                hash_result,
                padding=padding_algorithm,
                algorithm=hash_algorithm
            )
            return True
        except Exception:
            return False

# Example usage:
private_key, public_key = CryptUtil.generate_key_pair()
message_to_sign = b"Hello, digital signatures!"
# Calculate hash
hash_result = CryptUtil.calculate_hash(message_to_sign)
# Specify parameters for PSS padding
padding_algorithm = padding.PSS(padding.MGF1(hashes.SHA256()),padding.PSS.MAX_LENGTH)
# Sign the message
signature = CryptUtil.sign_message(hash_result, private_key,hashes.SHA256() ,padding_algorithm)
# Verify the signature
is_valid_signature = CryptUtil.verify_signature(message_to_sign, signature, public_key,hashes.SHA256(), padding_algorithm)
print("Signature is valid." if is_valid_signature else "Signature is invalid.")
