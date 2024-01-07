from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# 从PEM文件加载私钥
def load_private_key_from_pem_file(pem_file_path):
    with open(pem_file_path, "rb") as pem_file:
        private_key = serialization.load_pem_private_key(
            pem_file.read(),
            password=None,  # 如果有密码，传递密码字符串；否则为None
            backend=serialization.DefaultBackend()
        )
    return private_key

# 根据给定的参数创建公钥
def create_public_key(modulus, public_exponent):
    numbers = rsa.RSAPublicNumbers(e=public_exponent, n=modulus)
    public_key = numbers.public_key(backend=serialization.DefaultBackend())
    return public_key

# 示例使用
pem_file_path = "path/to/private_key.pem"
private_key = load_private_key_from_pem_file(pem_file_path)

# 替换以下参数为你实际使用的参数
modulus = 12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
public_exponent = 65537

public_key = create_public_key(modulus, public_exponent)
