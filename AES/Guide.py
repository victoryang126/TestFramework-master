密钥扩展（Key Expansion）：从输入的密钥生成一系列轮密钥（round keys），这些轮密钥将用于加密轮数中的每一轮。AES128算法将128位密钥扩展为轮密钥。

初始轮（Initial Round）：对输入的数据进行初始处理。加密和解密算法的初始轮有所不同。

多轮处理（Rounds）：AES128算法中进行多轮（通常为10轮）加密或解密处理。每轮包括几个步骤：

SubBytes：通过S盒（Substitution Box）对数据进行字节替换。
ShiftRows：对数据按特定规则进行行位移。
MixColumns：对数据进行列混淆，涉及有限域的乘法运算。
AddRoundKey：将轮密钥与数据进行按位异或运算。
最终轮（Final Round）：在最后一轮中，没有MixColumns步骤，其余步骤与多轮处理相同，包括SubBytes、ShiftRows和AddRoundKey。

输出：经过多轮处理后，得到加密或解密后的数据。

AES算法的关键特征是其设计结构的可逆性和强大的安全性。其安全性基于密钥长度和算法的设计。该算法在加密和解密中使用相同的密钥，因此是对称加密算法。

总的来说，AES128的算法逻辑包括密钥扩展、初始轮、多轮处理和最终轮，通过对数据进行一系列的替换、移位和按位运算，达到保护数据安全和隐私的目的。

S盒（Substitution Box，SBox）：

S盒是AES中的一个256字节的查找表，用于字节替换操作（SubBytes）。
SubBytes是AES的第一步，它将明文状态矩阵中的每个字节替换为S盒中的对应字节，引入非线性性，增加了数据的混淆性。
S盒是AES算法的一个关键元素，其设计经过数学分析和密码学原理的考量，以提高算法的安全性。不同的S盒实现可以导致不同的安全性水平。
轮常数（Round Constants，Rcon）：

轮常数是AES算法中的一个数组，用于密钥扩展过程（Key Expansion）。
在密钥扩展中，轮常数用于生成每一轮的轮密钥，以确保每轮的轮密钥都不同。
轮常数的值是预定义的，根据轮数（round number）来选择。轮常数的使用使得每一轮的轮密钥都不同，这对于AES的安全性是至关重要的


subKey2是根据subKey1生成的，它用于处理不完整块。
消息块处理：

将消息分成若干块，每个块的大小通常为128位（16字节）。
最后一个块的处理：

如果消息块大小不是16字节，需要进行填充（padding）。通常，AES-CMAC使用Bit Padding，即在消息块的末尾加上一个比特"1"，然后填充零位，直到块大小为16字节。
如果消息块大小为16字节，将其作为最后一个块处理。
CMAC计算：

对每个消息块进行以下操作：
如果这是最后一个块，将其与subKey2异或。
否则，将其与subKey1异或。
使用AES算法对结果块进行加密。
输出CMAC：

最后一个块的AES加密结果就是生成的CMAC，通常为128位
public static byte[] Encrypt(byte[] data, byte[] key, byte[] iv)
{
    using (Aes aesAlg = Aes.Create())
{
    aesAlg.Key = key;
aesAlg.IV = iv;

using (MemoryStream msEncrypt = new MemoryStream())
{
    using (CryptoStream csEncrypt = new CryptoStream(msEncrypt, aesAlg.CreateEncryptor(), CryptoStreamMode.Write))
{
    csEncrypt.Write(data, 0, data.Length);
}
return msEncrypt.ToArray();
}
}
}

初始数据准备：

输入数据：明文（plaintext），长度为128位（16字节）。
密钥（Key）：长度为128位（16字节），密钥用于加密和解密数据。
密钥扩展（Key Expansion）：

从输入的128位密钥生成一系列轮密钥（round keys），每个轮密钥的长度也为128位。
轮密钥生成使用密钥排列、替代和变换操作，以便在每轮中使用不同的轮密钥。
加密过程：

AES算法通常分为多轮（10轮）加密过程，每轮包括以下步骤：
SubBytes：通过S盒（Substitution Box）对数据进行字节替换。S盒将明文中的每个字节映射到另一个字节，引入了非线性性质。
ShiftRows：对数据进行行位移，不同行的位移量不同，这增加了数据的混淆性。
MixColumns：对数据进行列混淆，涉及有限域的乘法运算，增加了数据的扩散性。
AddRoundKey：将当前轮的轮密钥与数据进行按位异或运算，混淆数据。
最终轮（Final Round）：

最后一轮不包括MixColumns步骤，只进行SubBytes、ShiftRows和AddRoundKey步骤。

using System;

public class AES128Example
    {
    // 定义S盒（Substitution Box）
private static readonly byte[] SBox = {
                                          0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
                                          0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
                                      // 其余SBox值
};

// AES128的轮数
private const int Nr = 10;

// 加密轮密钥
private static byte[][] roundKeys;

public static void KeyExpansion(byte[] key)
{
    roundKeys = new byte[Nr + 1][];
roundKeys[0] = key;

for (int round = 1; round <= Nr; round++)
{
    roundKeys[round] = new byte[16];

// 实现轮密钥生成
   // 用前一轮的轮密钥生成当前轮的轮密钥
}
}

public static byte[] SubBytes(byte[] state)
{
for (int i = 0; i < state.Length; i++)
{
    state[i] = SBox[state[i]];
}
return state;
}

public static byte[] ShiftRows(byte[] state)
{
// 实现行位移操作
return state;
}

public static byte[] MixColumns(byte[] state)
{
// 实现列混淆操作
return state;
}

public static byte[] AddRoundKey(byte[] state, int round)
{
// 与轮密钥按位异或
return state;
}

public static byte[] FinalRound(byte[] state, int round)
{
state = SubBytes(state);
state = ShiftRows(state);
state = AddRoundKey(state, round);
return state;
}

public static void Main(string[] args)
{
byte[] key = new byte[16]; // 替换为你的128位密钥
byte[] inputData = new byte[16]; // 替换为要加密的数据

KeyExpansion(key);
inputData = AddRoundKey(inputData, 0);

for (int round = 1; round < Nr; round++)
    {
        inputData = SubBytes(inputData);
inputData = ShiftRows(inputData);
inputData = MixColumns(inputData);
inputData = AddRoundKey(inputData, round);
}

inputData = FinalRound(inputData, Nr);

// 输出加密后的数据
Console.WriteLine("加密后的数据：" + BitConverter.ToString(inputData).Replace("-", ""));
}
}



    public class AES128Example
        {
            private const int Nk = 4; // Nk 表示密钥中的32位字数目
    private const int Nb = 4; // Nb 表示分块的32位字数目
    private const int Nr = 10; // Nr 表示轮数

                                     // 定义Rcon表用于轮常数
    private static readonly byte[] Rcon = {
        0x01, 0x00, 0x00, 0x00,
        0x02, 0x00, 0x00, 0x00,
        0x04, 0x00, 0x00, 0x00,
        0x08, 0x00, 0x00, 0x00,
        0x10, 0x00, 0x00, 0x00,
        0x20, 0x00, 0x00, 0x00,
        0x40, 0x00, 0x00, 0x00,
        0x80, 0x00, 0x00, 0x00,
        0x1B, 0x00, 0x00, 0x00,
        0x36, 0x00, 0x00, 0x00
    };

    public static byte[] KeyExpansion(byte[] key)
    {
        int totalWords = Nb * (Nr + 1);
    byte[] roundKeys = new byte[totalWords * 4];

    // 将输入密钥复制到第一部分轮密钥中
    for (int i = 0; i < Nk; i++)
    {
        roundKeys[4 * i] = key[4 * i];
    roundKeys[4 * i + 1] = key[4 * i + 1];
    roundKeys[4 * i + 2] = key[4 * i + 2];
    roundKeys[4 * i + 3] = key[4 * i + 3];
    }

    for (int i = Nk; i < totalWords; i++)
    {
    byte[] temp = new byte[4];
    Array.Copy(roundKeys, 4 * (i - 1), temp, 0, 4);

    if (i % Nk == 0)
    {
    temp = SubWord(RotWord(temp));
    temp[0] ^= Rcon[i / Nk];
    }
    else if (Nk > 6 && i % Nk == 4)
    {
    temp = SubWord(temp);
    }

    roundKeys[4 * i] = (byte)(roundKeys[4 * (i - Nk)] ^ temp[0]);
    roundKeys[4 * i + 1] = (byte)(roundKeys[4 * (i - Nk) + 1] ^ temp[1]);
    roundKeys[4 * i + 2] = (byte)(roundKeys[4 * (i - Nk) + 2] ^ temp[2]);
    roundKeys[4 * i + 3] = (byte)(roundKeys[4 * (i - Nk) + 3] ^ temp[3]);
    }

    return roundKeys;
    }

    private static byte[] SubWord(byte[] word)
    {
    for (int i = 0; i < 4; i++)
        {
            word[i] = SBox[word[i]];
    }
    return word;
}

private static byte[] RotWord(byte[] word)
{
byte temp = word[0];
word[0] = word[1];
word[1] = word[2];
word[2] = word[3];
word[3] = temp;
return word;
}

private static readonly byte[] SBox = {
// S盒的值
};

public static void Main(string[] args)
{
byte[] key = new byte[] { 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x97, 0x75, 0x46, 0x20, 0x63, 0xed };
byte[] roundKeys = KeyExpansion(key);

// 输出扩展后的轮密钥
Console.WriteLine("Round Keys:");
for (int i = 0; i < roundKeys.Length; i += 16)
    {
for (int j = 0; j < 16; j++)
{
    Console.Write(roundKeys[i + j].ToString("X2") + " ");
}
Console.WriteLine();
}
}
}


    public class AES128Example
        {
            private static readonly byte[] SBox = {
                                                  // S盒的值
    };

    private static readonly byte[] Rcon = {
        0x01, 0x00, 0x00, 0x00,
        0x02, 0x00, 0x00, 0x00,
        0x04, 0x00, 0x00, 0x00,
        0x08, 0x00, 0x00, 0x00,
        0x10, 0x00, 0x00, 0x00,
        0x20, 0x00, 0x00, 0x00,
        0x40, 0x00, 0x00, 0x00,
        0x80, 0x00, 0x00, 0x00,
        0x1B, 0x00, 0x00, 0x00,
        0x36, 0x00, 0x00, 0x00
    };

    private static readonly byte[] MixColumnMatrix = {
        0x02, 0x03, 0x01, 0x01,
        0x01, 0x02, 0x03, 0x01,
        0x01, 0x01, 0x02, 0x03,
        0x03, 0x01, 0x01, 0x02
    };

    private static byte[][] roundKeys;

    public static byte[] SubBytes(byte[] state)
    {
    for (int i = 0; i < state.Length; i++)
    {
        state[i] = SBox[state[i]];
    }
    return state;
    }

    public static byte[] ShiftRows(byte[] state)
    {
    byte[] temp = new byte[16];
    for (int i = 0; i < 4; i++)
        {
    for (int j = 0; j < 4; j++)
    {
        temp[i + j * 4] = state[i + ((j + i) % 4) * 4];
    }
    }
    return temp;
}

public static byte[] MixColumns(byte[] state)
{
byte[] result = new byte[16];

for (int i = 0; i < 4; i++)
    {
for (int j = 0; j < 4; j++)
{
    byte val = 0;
for (int k = 0; k < 4; k++)
{
byte a = state[i + k * 4];
byte b = MixColumnMatrix[j + k * 4];
val ^= Multiply(a, b);
}
result[i + j * 4] = val;
}
}

return result;
}

public static byte[] AddRoundKey(byte[] state, int round)
{
for (int i = 0; i < 16; i++)
    {
        state[i] ^= roundKeys[round][i];
}
return state;
}

public static byte Multiply(byte a, byte b)
{
byte result = 0;
for (int i = 0; i < 8; i++)
    {
    if ((b & 1) != 0)
{
    result ^= a;
}
bool highBitSet = (a & 0x80) != 0;
a <<= 1;
if (highBitSet)
{
    a ^= 0x1B; // Rijndael's finite field polynomial
}
b >>= 1;
}
return result;
}

public static byte[] FinalRound(byte[] state)
{
state = SubBytes(state);
state = ShiftRows(state);
state = AddRoundKey(state, roundKeys.Length - 1);
return state;
}

public static void Main(string[] args)
{
byte[] key = new byte[16]; // 替换为你的128位密钥
byte[] inputData = new byte[16]; // 替换为要加密的数据

roundKeys = KeyExpansion(key);

inputData = AddRoundKey(inputData, 0);

for (int round = 1; round < roundKeys.Length - 1; round++)
    {
        inputData = SubBytes(inputData);
inputData = ShiftRows(inputData);
inputData = MixColumns(inputData);
inputData = AddRoundKey(inputData, round);
}

inputData = FinalRound(inputData);

// 输出加密后的数据
Console.WriteLine("加密后的数据：" + BitConverter.ToString(inputData).Replace("-", ""));
}
}


