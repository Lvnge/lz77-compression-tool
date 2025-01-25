import argparse
import os
import struct


def lz77_compress(input_file, output_file, window_size=4096, lookahead_size=18):
    with open(input_file, 'r') as file:
        input_data = file.read()

    compressed_data = []
    i = 0

    while i < len(input_data):
        match_offset = -1
        match_length = 0
        match_char = input_data[i]

        for j in range(max(0, i - window_size), i):
            length = 0
            while (i + length < len(input_data)) and (input_data[j + length] == input_data[i + length]):
                length += 1
                if length >= lookahead_size:
                    break
            if length > match_length:
                match_offset = i - j
                match_length = length
                match_char = input_data[i + length] if i + length < len(input_data) else '\x00'

        if match_length > 0:
            compressed_data.append((match_offset, match_length, match_char))
            i += match_length + 1
        else:
            compressed_data.append((0, 0, match_char))
            i += 1

    with open(output_file, 'wb') as file:
        compressed_length = len(compressed_data)
        file.write(struct.pack('I', compressed_length))

        for offset, length, char in compressed_data:
            file.write(struct.pack('I', offset))
            file.write(struct.pack('H', length))
            file.write(struct.pack('B', ord(char)))

    print(f"File compressed and saved to {output_file}")


def lz77_decompress(compressed_file, output_file):
    with open(compressed_file, 'rb') as file:
        compressed_length = struct.unpack('I', file.read(4))[0]
        decompressed_data = []

        for _ in range(compressed_length):
            offset = struct.unpack('I', file.read(4))[0]
            length = struct.unpack('H', file.read(2))[0]
            char = chr(struct.unpack('B', file.read(1))[0])

            if offset > 0 and length > 0:
                start = len(decompressed_data) - offset
                for i in range(length):
                    decompressed_data.append(decompressed_data[start + i])

            if char != '\x00':
                decompressed_data.append(char)

    with open(output_file, 'w') as out_file:
        out_file.write(''.join(decompressed_data))

    print(f"File decompressed and saved to {output_file}")


def calculate_compression_ratio(original_file, compressed_file):
    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)

    ratio = compressed_size / original_size
    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression ratio: {ratio:.2%}")


def main():
    parser = argparse.ArgumentParser(description="LZ77 Compression and Decompression Tool")
    parser.add_argument("mode", choices=["compress", "decompress"], help="Mode: compress or decompress")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    parser.add_argument("--window_size", type=int, default=4096, help="Sliding window size (default: 4096)")
    parser.add_argument("--lookahead_size", type=int, default=18, help="Lookahead buffer size (default: 18)")

    args = parser.parse_args()

    if args.mode == "compress":
        lz77_compress(args.input_file, args.output_file, args.window_size, args.lookahead_size)
        calculate_compression_ratio(args.input_file, args.output_file)
    elif args.mode == "decompress":
        lz77_decompress(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
