SHA算法的原理涉及到一系列步骤，主要包括消息填充、初始化、数据处理和输出。以下是SHA算法的基本原理：

消息填充（Padding）： 首先，要处理的消息被填充，以确保其长度是一个固定的块大小。这通常包括在消息的末尾添加一些比特，以满足特定的块大小要求。

初始化（Initialization）： 初始化阶段涉及设置一些初始的常量和变量。这些初始值通常称为"初始化向量"，并在算法的整个执行过程中使用。

数据处理（Data Processing）： 消息被分割成块，每个块经过一系列的处理步骤。这些步骤包括将块与之前处理的结果进行混合、应用逻辑函数、循环迭代等。这一步骤是SHA算法中最为复杂的部分，且不同版本的SHA算法有不同的处理步骤。

输出（Output）： 在数据处理的最后阶段，得到的结果被合并成最终的消息摘要。这个摘要是一个固定长度的哈希值，通常以十六进制表示


PKCS #8 的原理涉及到两个主要概念：PrivateKeyInfo 结构和 DER 编码。以下是关键的原理解释：

PrivateKeyInfo 结构： PKCS #8 定义了一个结构称为 PrivateKeyInfo，该结构包含了私钥的信息。这个结构的字段包括：

version：指定私钥信息的版本号。
privateKeyAlgorithm：包含一个表示私钥算法的标识符。
privateKey：包含经过编码的私钥数据。
DER 编码： PKCS #8 使用 ASN.1（Abstract Syntax Notation One）作为数据结构的描述语言，并使用 DER（Distinguished Encoding Rules）作为其二进制编码规则。ASN.1 是一种用于描述数据结构的抽象标记语言，而 DER 是用于将这些数据结构编码为二进制的规则。

ASN.1： ASN.1 描述了数据结构的抽象表示形式，包括其字段和类型。在 PKCS #8 中，ASN.1 描述了 PrivateKeyInfo 结构的字段和类型。

DER 编码： DER 是 ASN.1 的二进制编码规则，定义了如何将 ASN.1 描述的数据结构编码为二进制。这种编码保证了数据的唯一性和一致性，允许在不同系统之间共享。

因此，PKCS #8 的原理可以总结为将私钥信息表示为 PrivateKeyInfo 结构，然后使用 ASN.1 和 DER 编码将这个结构转换为二进制格式。这种格式化使得私钥在不同系统和应用中更容易地传输、存储和解析。在密码学中，PKCS #8 主要用于在数字证书、密钥协商等场景中处理私钥信息


公钥（Public Key）：

公钥是用于加密的密钥，可以安全地分享给任何人。
通过使用公钥加密的数据，只能使用与之相关的私钥进行解密。
公钥通常用于向其他人提供安全的通信方式，可以在网络上公开传播而不会引起安全问题。
私钥（Private Key）：

私钥是与公钥配对的密钥，是用于解密加密数据的密钥。
只有持有私钥的一方才能够解密使用公钥加密的数据。
私钥应该被保持安全，并只有其所有者知道。一旦私钥泄漏，加密的安全性就会受到威胁。
关系和应用：

公钥和私钥之间是一对密切相关的密钥，它们由相同的加密算法生成。
公钥用于加密信息，私钥用于解密信息。这种关系确保了只有私钥持有者才能解密被公钥加密的数据。
另一方面，私钥用于数字签名，而公钥用于验证数字签名。这种机制确保了只有私钥持有者才能生成数字签名，并且任何人都可以使用公钥验证签名的真实性。


public_key：
Modulus (n)： 公钥中的模数，是两个质数的乘积。n 决定了密钥的长度。

Public Exponent (e)： 公钥中的指数值。e 是用于加密的指数。

private_key：
Modulus (n)： 私钥中的模数，与公钥相同，是两个质数的乘积。n 决定了密钥的长度。

Private Exponent (d)： 私钥中的指数值。d 是用于解密的指数。

Public Exponent (e)： 与公钥中的 e 相同，是用于加密的指数。

First Prime Factor (p) 和 Second Prime Factor (q)： 私钥中的两个质数，它们的乘积等于模数 n。这两个质数的保密性非常重要，它们用于计算其他私钥参数。

Private Key Coefficient (dmp1, dmq1, iqmp)： 这些参数用于提高私钥的运算效率，具体涉及到模数 n 的计算。

这些信息共同构成了完整的 RSA 密钥对，其中公钥信息可供外部使用，而私钥信息应该被妥善保护。在使用 cryptography 库时，这些信息通常是通过相应的属性（如 public_key().public_numbers() 或 private_key().private_numbers()）来获取的。

数字签名过程：
消息摘要计算： 首先，对要签名的消息进行哈希计算，得到消息的摘要（hash value）。

私钥签名： 使用私钥对摘要进行加密，生成数字签名。这通常涉及使用非对称加密算法的私钥部分，例如 RSA 算法。

生成数字签名： 将加密后的摘要与原始消息一起构成数字签名。

数字签名验证过程：
消息摘要计算： 对接收到的消息进行相同的哈希计算，得到消息的摘要。

使用公钥解密： 使用与签名过程中使用的私钥对应的公钥对数字签名进行解密，得到解密后的摘要。

比较摘要： 将接收到的摘要与解密得到的摘要进行比较。如果两者相匹配，说明签名有效，消息未被篡改。

这样，数字签名的过程保证了两个重要的性质：

身份认证： 数字签名可以确保签名者拥有对应的私钥，因为只有私钥的持有者才能正确地生成有效的签名。
消息完整性： 数字签名的验证过程可以确定消息是否被篡改过，因为任何对消息的修改都会导致签名验证失败。
总体而言，数字签名是一种用于确保消息的来源和完整性的重要安全机制