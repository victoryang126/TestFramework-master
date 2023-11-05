using System;
using System.Security.Cryptography;

public class AESCMACExample
    {
        public static byte[] GenerateCMAC(byte[] key, byte[] message)
{
    using (Aes aes = Aes.Create())
{
    aes.Key = key;
aes.Mode = CipherMode.ECB;
aes.Padding = PaddingMode.None;

byte[] subKey1 = aes.CreateEncryptor().TransformFinalBlock(new byte[16], 0, 16);
byte[] subKey2 = GenerateSubKey2(subKey1);

int blockSize = 16;
int messageLength = message.Length;

byte[] lastBlock = new byte[blockSize];
Array.Copy(message, messageLength - blockSize, lastBlock, 0, blockSize);

if (messageLength % blockSize == 0)
{
    lastBlock = XOR(lastBlock, subKey1);
}
else
{
    lastBlock = Padding(lastBlock);
lastBlock = XOR(lastBlock, subKey2);
}

byte[] result = aes.CreateEncryptor().TransformFinalBlock(lastBlock, 0, blockSize);

return result;
}
}

private static byte[] GenerateSubKey2(byte[] subKey1)
{
    byte[] result = new byte[16];

for (int i = 0; i < 16; i++)
{
result[i] = (byte)(subKey1[i] << 1);
if (i < 15 && (subKey1[i + 1] & 0x80) == 0x80)
    {
        result[i] ^= 0x87;
}
}

return result;
}

private static byte[] XOR(byte[] a, byte[] b)
{
byte[] result = new byte[a.Length];
for (int i = 0; i < a.Length; i++)
    {
        result[i] = (byte)(a[i] ^ b[i]);
}
return result;
}

private static byte[] Padding(byte[] block)
{
block[block.Length - 1] |= 0x80;
return block;
}

public static void Main(string[] args)
{
byte[] key = new byte[16]; // 替换为你的128位密钥
byte[] message = Encoding.UTF8.GetBytes("Hello, AES-CMAC!");

byte[] cmac = GenerateCMAC(key, message);

// 输出生成的CMAC
Console.WriteLine("生成的CMAC：" + BitConverter.ToString(cmac).Replace("-", ""));
}
}
