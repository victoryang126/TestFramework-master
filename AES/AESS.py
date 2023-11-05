using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

public class AESCMAExample
    {
        public static byte[] EncryptAndMAC(byte[] data, byte[] key, byte[] nonce)
{
    using (Aes aesAlg = Aes.Create())
{
    aesAlg.Key = key;
aesAlg.Mode = CipherMode.ECB; // 使用ECB模式
aesAlg.Padding = PaddingMode.None; // 无填充

                                      // 初始化CBC-MAC算法
using (var macAlg = new HMACSHA256(key))
{
// 生成随机IV作为计数器
byte[] iv = new byte[16];
Array.Copy(nonce, iv, 8); // 使用前8个字节作为IV

                             // 创建内存流以保存加密后的数据
using (MemoryStream encryptedData = new MemoryStream())
{
// 加密数据
using (CryptoStream encryptor = new CryptoStream(encryptedData, aesAlg.CreateEncryptor(), CryptoStreamMode.Write))
{
    encryptor.Write(data, 0, data.Length);
encryptor.FlushFinalBlock();
}

byte[] encryptedBytes = encryptedData.ToArray();

// 计算CBC-MAC
macAlg.TransformBlock(iv, 0, iv.Length, iv, 0);
macAlg.TransformFinalBlock(encryptedBytes, 0, encryptedBytes.Length);

// 获取CBC-MAC结果
byte[] mac = macAlg.Hash;

// 将MAC追加到加密数据后面
byte[] encryptedDataWithMAC = new byte[encryptedBytes.Length + mac.Length];
Array.Copy(encryptedBytes, encryptedDataWithMAC, encryptedBytes.Length);
Array.Copy(mac, 0, encryptedDataWithMAC, encryptedBytes.Length, mac.Length);

return encryptedDataWithMAC;
}
}
}
}

public static byte[] DecryptAndVerify(byte[] data, byte[] key, byte[] nonce)
{
    using (Aes aesAlg = Aes.Create())
{
    aesAlg.Key = key;
aesAlg.Mode = CipherMode.ECB;
aesAlg.Padding = PaddingMode.None;

// 初始化CBC-MAC算法
using (var macAlg = new HMACSHA256(key))
{
// 从数据中分离MAC
byte[] mac = new byte[macAlg.HashSize / 8];
Array.Copy(data, data.Length - mac.Length, mac, 0, mac.Length);

// 生成随机IV作为计数器
byte[] iv = new byte[16];
Array.Copy(nonce, iv, 8);

// 验证MAC
macAlg.TransformBlock(iv, 0, iv.Length, iv, 0);
macAlg.TransformFinalBlock(data, 0, data.Length - mac.Length);

byte[] computedMAC = macAlg.Hash;

if (!CompareBytes(mac, computedMAC))
{
throw new Exception("MAC verification failed. Data may be tampered with.");
}

// 从数据中移除MAC部分
byte[] encryptedData = new byte[data.Length - mac.Length];
Array.Copy(data, encryptedData, encryptedData.Length);

// 解密数据
using (MemoryStream decryptedData = new MemoryStream())
{
using (CryptoStream decryptor = new CryptoStream(decryptedData, aesAlg.CreateDecryptor(), CryptoStreamMode.Write))
{
    decryptor.Write(encryptedData, 0, encryptedData.Length);
decryptor.FlushFinalBlock();
}

return decryptedData.ToArray();
}
}
}
}

public static bool CompareBytes(byte[] a, byte[] b)
{
if (a.Length != b.Length)
{
return false;
}

for (int i = 0; i < a.Length; i++)
{
    if (a[i] != b[i])
        {
    return false;
    }
    }

    return true;
}

public static void Main(string[] args)
{
byte[] key = Encoding.UTF8.GetBytes("YourEncryptionKey"); // 替换为你的密钥
byte[] nonce = Encoding.UTF8.GetBytes("YourNonceValue"); // 替换为你的随机值

string originalData = "Hello, AES-CMA!";
byte[] data = Encoding.UTF8.GetBytes(originalData);

// 加密和生成MAC
byte[] encryptedDataWithMAC = EncryptAndMAC(data, key, nonce);

// 解密和验证MAC
byte[] decryptedData = DecryptAndVerify(encryptedDataWithMAC, key, nonce);

string decryptedText = Encoding.UTF8.GetString(decryptedData);
Console.WriteLine("解密后的数据：" + decryptedText);
}
}
