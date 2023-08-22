def generate_crc_table(polynomial, width):
    crc_table = [0] * 256

    for i in range(256):
        crc = i << (width - 8)
        for _ in range(8):
            if crc & (1 << (width - 1)):
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
        crc_table[i] = crc

    return crc_table


def calculate_direct_reflected_crc(data, poly, initial_value=0xFFFFFFFF, final_xor=0xFFFFFFFF, width=32):
    crc = initial_value
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
    return crc ^ final_xor

def calculate_crc_with_table(data, crc_table, initial_value=0xFFFFFFFF, final_xor=0xFFFFFFFF, width=32):
    crc = initial_value
    for byte in data:
        crc = (crc >> 8) ^ crc_table[(crc ^ byte) & 0xFF]
    return crc ^ final_xor

def reverse_bits(data, width):
    reversed_data = 0
    for _ in range(width):
        reversed_data = (reversed_data << 1) | (data & 1)
        data >>= 1
    return reversed_data

def main():
    data = b"Hello, World!"

    # Reverse input data
    reversed_data = [reverse_bits(byte, 8) for byte in data]

    # CRC-32 parameters
    crc32_poly = 0x04C11DB7
    crc32_table = generate_crc_table(crc32_poly, width=32)

    # Calculate CRC-32 using table
    crc32_result = calculate_crc_with_table(reversed_data, crc32_table, width=32)

    # Reverse CRC-32 result
    reversed_crc32_result = reverse_bits(crc32_result, 32)
    print(f"CRC-32 value: {reversed_crc32_result:08X}")

if __name__ == "__main__":
    main()
