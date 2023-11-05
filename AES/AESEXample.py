using System;

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

private static byte[][] roundKeys;

public static byte[] KeyExpansion(byte[] key)
{
    roundKeys = new byte[11][];
roundKeys[0] = key;

for (int i = 1; i < 11; i++)
{
    roundKeys[i] = new byte[16];

byte[] temp = new byte[4];
for (int j = 0; j < 4; j++)
{
    temp[j] = roundKeys[i - 1][(i * 4) + j];
}

if (i % 4 == 0)
{
temp = SubWord(RotWord(temp));
temp[0] ^= Rcon[i / 4];
}

for (int j = 0; j < 4; j++)
{
roundKeys[i][j] = (byte)(roundKeys[i - 1][j] ^ temp[j]);
}

for (int j = 4; j < 16; j++)
{
roundKeys[i][j] = (byte)(roundKeys[i][j - 4] ^ roundKeys[i - 1][j]);
}
}

return null; // 返回扩展后的轮密钥
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
state = MixColumns(state);
state = AddRoundKey(state, round);
return state;
}

public static void Main(string[] args)
{
byte[] key = new byte[16]; // 替换为你的128位密钥
byte[] inputData = new byte[16]; // 替换为要加密的数据

roundKeys = KeyExpansion(key);

inputData = AddRoundKey(inputData, 0);

for (int round = 1; round < 10; round++)
    {
        inputData = SubBytes(inputData);
inputData = ShiftRows(inputData);
inputData = MixColumns(inputData);
inputData = AddRoundKey(inputData, round);
}

inputData = FinalRound(inputData, 10);

// 输出加密后的数据
Console.WriteLine("加密后的数据：" + BitConverter.ToString(inputData).Replace("-", ""));
}
}
