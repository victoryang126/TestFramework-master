def twos_complement_to_original(binary_str):
    if binary_str[0] == '1':
        # Negative number
        complement = ''.join('1' if bit == '0' else '0' for bit in binary_str[1:])
        original = -int(complement, 2) - 1
    else:
        # Positive number
        original = int(binary_str, 2)

    return original

def original_to_twos_complement(number, num_bits):
    if number >= 0:
        # Positive number
        binary_str = bin(number)[2:].zfill(num_bits)
    else:
        # Negative number
        complement = bin(abs(number) - 1)[2:].zfill(num_bits)
        binary_str = ''.join('1' if bit == '0' else '0' for bit in complement)

    return binary_str

def hex_twos_complement_to_original(hex_str):
    # Convert the hexadecimal string to an integer
    integer_value = int(hex_str, 16)

    # Check if it's a negative number (high bit set)
    num_bits = len(hex_str) * 4  # Calculate the number of bits
    if integer_value & (1 << (num_bits - 1)):
        # Calculate two's complement to obtain original value
        original_value = integer_value - (1 << num_bits)
    else:
        # Positive number, original value is the same as the integer value
        original_value = integer_value

    return original_value

def original_to_hex_twos_complement(number, num_bits):
    if number >= 0:
        # Positive number, convert to hexadecimal directly
        hex_str = hex(number)[2:].zfill(num_bits // 4)
    else:
        # Negative number, convert to hexadecimal two's complement
        complement = (1 << num_bits) + number  # Calculate two's complement
        hex_str = hex(complement)[2:].zfill(num_bits // 4)

    return hex_str


if __name__ == '__main__':
    pass