class CRC:

    @staticmethod
    def generate_crc_table(polynomial, width):
        crc_table = [0] * 256
        for i in range(256):
            crc = i << (width - 8)
            for _ in range(8):
                if crc & (1 << (width - 1)):
                    crc = (crc << 1) ^ polynomial
                else:
                    crc <<= 1
            crc_table[i] = crc & ((1 << width) - 1)  # handler the overflow
        print([hex(i) for i in crc_table])
        return crc_table

    @staticmethod
    def calculate_crc(data, polynomial, initial_value=0xFFFFFFFF, final_xor=0xFFFFFFFF, width=32, input_reflect=False,
                      result_reflect=False):
        crc = initial_value

        for byte in data:
            if input_reflect:
                byte = CRC.reverse_bits(byte, 8)

            crc ^= byte << (width - 8)
            for _ in range(8):
                if crc & (1 << (width - 1)):
                    crc = (crc << 1) ^ polynomial
                else:
                    crc <<= 1
            crc &= (1 << width) - 1

        if result_reflect:
            crc = CRC.reverse_bits(crc, width)
        crc = crc ^ final_xor
        print(hex(crc))

        return crc

    @staticmethod
    def calculate_crc_with_table(data, crc_table, crc_initial, final_xor, width=32, input_reflect=False,
                                 result_reflect=False):
        crc = crc_initial

        for byte in data:
            if input_reflect:
                byte = CRC.reverse_bits(byte, 8)

            index = (crc ^ byte) & 0xFF
            crc = (crc >> 8) ^ crc_table[index]
            crc &= ((1 << width) - 1)

        if result_reflect:
            crc = CRC.reverse_bits(crc, width)
        crc = (crc ^ final_xor) & ((1 << width) - 1)
        print(hex(crc))
        return crc

    @staticmethod
    def reverse_bits(data, width):
        reversed_data = 0
        for _ in range(width):
            reversed_data = (reversed_data << 1) | (data & 1)
            data >>= 1
        return reversed_data


if __name__ == "__main__":
    data = b"Hello, World!"

    # Reverse input data
    reversed_data = [CRC.reverse_bits(byte, 8) for byte in data]

    # CRC-32 parameters
    poly = 0x1D
    crc_table = CRC.generate_crc_table(poly, width=8)

    CRC.calculate_crc(bytearray([0x31, 0x32, 0x33]), 0x1D, 0xFF, 0xFF, 8)
    CRC.calculate_crc_with_table(bytearray([0x31, 0x32, 0x33]), crc_table, 0xFF, 0xFF, 8)

    poly = 0x1021
    crc_table = CRC.generate_crc_table(poly, width=16)
    CRC.calculate_crc(bytearray([0x31, 0x32, 0x33]), 0x1021, 0x0, 0x0, 16)
    CRC.calculate_crc_with_table(bytearray([0x31, 0x32, 0x33]), crc_table, 0x0, 0x00, 16)
    # # Calculate CRC-32 using table
    # crc32_result = CRC.calculate_crc_with_table(reversed_data, crc32_table, width=32)
    #
    # # Reverse CRC-32 result
    # reversed_crc32_result = CRC.reverse_bits(crc32_result, 32)
    # print(f"CRC-32 value: {reversed_crc32_result:08X}")
