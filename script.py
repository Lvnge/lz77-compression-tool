import argparse  # Module for parsing command-line arguments
import os  # Module for interacting with the operating system, e.g., file sizes
import struct  # Module for packing and unpacking binary data


# Function to perform LZ77 compression
def lz77_compress(input_file, output_file, window_size=4096, lookahead_size=18):
    # Open the input file and read its contents into memory
    with open(input_file, 'r') as file:
        input_data = file.read()

    # List to store the compressed data
    compressed_data = []
    i = 0  # Pointer to track the current position in input_data

    # Iterate over the input data to find matches for compression
    while i < len(input_data):
        match_offset = -1  # Default no match
        match_length = 0  # Length of the match found
        match_char = input_data[i]  # The next character to be compressed

        # Search for the longest match in the sliding window
        for j in range(max(0, i - window_size), i):
            length = 0
            # Check for matching characters starting from position 'j' in the window
            while (i + length < len(input_data)) and (input_data[j + length] == input_data[i + length]):
                length += 1
                if length >= lookahead_size:  # Don't exceed the lookahead size
                    break
            # Update the best match found so far
            if length > match_length:
                match_offset = i - j  # Offset from the current position
                match_length = length  # Length of the match
                match_char = input_data[i + length] if i + length < len(input_data) else '\x00'

        # If a match was found, store it in the compressed data
        if match_length > 0:
            compressed_data.append((match_offset, match_length, match_char))
            i += match_length + 1  # Move past the matched data
        else:
            # If no match, store the current character as a literal
            compressed_data.append((0, 0, match_char))
            i += 1  # Move to the next character

    # Write the compressed data to the output file in binary format
    with open(output_file, 'wb') as file:
        compressed_length = len(compressed_data)  # Total number of compressed entries
        # Write the total number of compressed entries (as a 4-byte unsigned integer)
        file.write(struct.pack('I', compressed_length))

        # Write each entry (offset, length, char) in a packed binary format
        for offset, length, char in compressed_data:
            file.write(struct.pack('I', offset))  # Write the offset (4 bytes)
            file.write(struct.pack('H', length))  # Write the length (2 bytes)
            file.write(struct.pack('B', ord(char)))  # Write the character (1 byte)

    print(f"File compressed and saved to {output_file}")


# Function to perform LZ77 decompression
def lz77_decompress(compressed_file, output_file):
    # Open the compressed file and read its contents
    with open(compressed_file, 'rb') as file:
        compressed_length = struct.unpack('I', file.read(4))[0]  # Read and unpack the compressed length
        decompressed_data = []  # List to store the decompressed data

        # Iterate through the compressed data and reconstruct the original
        for _ in range(compressed_length):
            offset = struct.unpack('I', file.read(4))[0]  # Read and unpack the offset (4 bytes)
            length = struct.unpack('H', file.read(2))[0]  # Read and unpack the length (2 bytes)
            char = chr(struct.unpack('B', file.read(1))[0])  # Read and unpack the character (1 byte)

            # If there was a match, repeat the data from the window based on the offset and length
            if offset > 0 and length > 0:
                start = len(decompressed_data) - offset  # Calculate the start position in the decompressed data
                for i in range(length):
                    decompressed_data.append(decompressed_data[start + i])  # Add the matched data

            # If the character is not null, add it as a literal character
            if char != '\x00':
                decompressed_data.append(char)

    # Write the decompressed data to the output file
    with open(output_file, 'w') as out_file:
        out_file.write(''.join(decompressed_data))  # Join the list into a string and write it to the file

    print(f"File decompressed and saved to {output_file}")


# Function to calculate and display the compression ratio
def calculate_compression_ratio(original_file, compressed_file):
    original_size = os.path.getsize(original_file)  # Get the size of the original file
    compressed_size = os.path.getsize(compressed_file)  # Get the size of the compressed file

    # Calculate the compression ratio
    ratio = compressed_size / original_size
    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression ratio: {ratio:.2%}")  # Display the compression ratio as a percentage


# Main function to handle command-line arguments and control flow
def main():
    # Set up argument parser for the command-line interface
    parser = argparse.ArgumentParser(description="LZ77 Compression and Decompression Tool")
    parser.add_argument("mode", choices=["compress", "decompress"], help="Mode: compress or decompress")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument("--window_size", type=int, default=4096, help="Sliding window size (default: 4096)")
    parser.add_argument("--lookahead_size", type=int, default=18, help="Lookahead buffer size (default: 18)")

    args = parser.parse_args()  # Parse the command-line arguments

    # Perform compression or decompression based on the mode specified
    if args.mode == "compress":
        lz77_compress(args.input_file, args.output_file, args.window_size, args.lookahead_size)
        calculate_compression_ratio(args.input_file, args.output_file)  # Calculate and display the compression ratio
    elif args.mode == "decompress":
        lz77_decompress(args.input_file, args.output_file)  # Perform decompression


# Entry point of the script
if __name__ == "__main__":
    main()  # Run the main function when the script is executed
