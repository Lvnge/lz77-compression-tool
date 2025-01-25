import struct


def lz77_decompress(compressed_file, output_file):
    """
    Decompress a file using the LZ77 algorithm and save the decompressed output to another file.
    Args:
    - compressed_file (str): The path to the compressed file.
    - output_file (str): The path to save the decompressed file.
    """
    with open(compressed_file, 'rb') as file:
        # Read the total compressed data length (first 4 bytes)
        compressed_length = struct.unpack('I', file.read(4))[0]

        decompressed_data = []

        # Decompress data by reading triples
        for _ in range(compressed_length):
            offset = struct.unpack('I', file.read(4))[0]  # Read offset (4 bytes)
            length = struct.unpack('H', file.read(2))[0]  # Read length (2 bytes)
            char = chr(struct.unpack('B', file.read(1))[0])  # Read character (1 byte)

            # If there's a match, copy data from the previous decompressed data
            if offset > 0 and length > 0:
                start = len(decompressed_data) - offset
                for i in range(length):
                    decompressed_data.append(decompressed_data[start + i])

            # Append the character, if not null
            if char != '\x00':
                decompressed_data.append(char)

        # Write the decompressed data to the output file
        with open(output_file, 'w') as out_file:
            out_file.write(''.join(decompressed_data))

    print(f"File decompressed and saved to {output_file}")

# Example usage:
if __name__ == "__main__":
    input_compressed_file = 'files/output.lz77'  # Path to the compressed file
    output_decompressed_file = 'files/decompressed.txt'  # Path to save the decompressed file
    
    # Decompress the file
    lz77_decompress(input_compressed_file, output_decompressed_file)
