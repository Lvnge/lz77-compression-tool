# LZ77 Compression and Decompression Tool

## Overview
This project implements a file compression and decompression tool using the LZ77 algorithm. It provides an efficient way to compress text files by identifying and encoding repetitive patterns in the data. The tool is designed to be used via the command line and supports customization of algorithm parameters.

## Features
- **LZ77 Compression and Decompression**: Compress text files into a smaller binary format and decompress them back to their original state.
- **Command-Line Interface (CLI)**: Easy-to-use interface for specifying input and output files, as well as compression settings.
- **Adjustable Parameters**: Customize the sliding window size and lookahead buffer size for optimal compression.
- **Compression Efficiency Metrics**: Displays the original and compressed file sizes, as well as the compression ratio.

## Requirements
- Python 3.8 or later

## Usage
### Command-Line Arguments
- `mode`: Choose between `compress` or `decompress`.
- `input_file`: Path to the input file to be compressed or decompressed.
- `output_file`: Path to save the compressed or decompressed file.
- `--window_size`: (Optional) Sliding window size. Default: `4096`.
- `--lookahead_size`: (Optional) Lookahead buffer size. Default: `18`.

### Example Commands
#### Compress a File
```bash
python script.py compress input.txt output.lz77
```

#### Decompress a File
```bash
python script.py decompress output.lz77 decompressed.txt
```

#### Adjust Compression Parameters
```bash
python script.py compress input.txt output.lz77 --window_size 8192 --lookahead_size 32
```

## How It Works
### Compression
The tool uses a sliding window and lookahead buffer to identify repeated patterns in the data. Matches are encoded as `(offset, length, next_char)` and stored in a binary format.

### Decompression
The compressed data is decoded to reconstruct the original file using the stored offsets and lengths.

## Compression Efficiency
The script calculates and displays the compression ratio as follows:
```bash
Compression ratio = (compressed size / original size) * 100%
```
This helps evaluate the effectiveness of the compression.

## Example
### Input (input.txt):
```
ABABABABABABABABABABABABABABABABABABABABABABABAB
```

### Compression Command:
```bash
python script.py compress input.txt output.lz77
```

### Decompression Command:
```bash
python script.py decompress output.lz77 decompressed.txt
```

### Output (decompressed.txt):
```
ABABABABABABABABABABABABABABABABABABABABABABABAB
```

## Limitations
- Currently supports only plain text files.
- Performance may vary for very large files or high repetition data.

## Future Enhancements
- Add support for binary file compression.
- Develop a graphical user interface (GUI).
- Implement additional compression algorithms (e.g., Huffman coding).
- Profile and optimize memory and CPU usage.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- The LZ77 algorithm was originally introduced by Abraham Lempel and Jacob Ziv in 1977.

---
Feel free to contribute by submitting pull requests or reporting issues!

