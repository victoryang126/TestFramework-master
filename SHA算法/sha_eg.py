import hashlib

# 使用SHA-256哈希算法示例
sha256 = hashlib.sha256()
sha256.update(b"Hello, hashlib!")
digest = sha256.hexdigest()
print("SHA-256 Digest:", digest)
