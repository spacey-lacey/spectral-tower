import sys

file_path = sys.argv[1]



hex_to_unicode = \
{
    0x01: " ",
    0x02: "█",
    0x03: "▐",
    0x04: "▌",
    0x05: "▄",
    0x06: "▀",
    0x07: "▗",
    0x08: "▖",
    0x09: "▝",
    0x0A: "▘",
    0x0B: "▛",
    0x0C: "▜",
    0x0D: "▙",
    0x0E: "▟",
    0x0F: "░",
    0x10: "F",
    0x11: "P",
    0x12: "S",
    0x13: "B",
    0x14: "W",
    0x15: "T",
    0x16: "J",
    0x18: "X",
    0x19: "Z",
    0x1A: ".",
    0x1B: ";",
    0x1C: "▒",
    0x1D: "▓"
}

map_start = "23 00 00 00 70 70 20 20"

def find_first_match(file_path, hex_sequence):
    '''
    Find the first occurrence of a hex sequence in a binary file.

    Parameters:
        file_path (str): Path to the binary file.
        hex_sequence (str): Hex sequence to search for (e.g., "01 02 03 04").

    Returns:
        int: Offset of the first match, or -1 if not found.
    '''
    byte_sequence = bytes.fromhex(hex_sequence.replace(" ", ""))

    with open(file_path, "rb") as f:
        binary_data = f.read()  # Load the entire file into memory
        first_match = binary_data.find(byte_sequence)

    return first_match


def print_ascii_map(file_path, start_offset, rows, cols):
    """
    Print a map as ASCII characters from binary data with 2 bytes per tile (1 byte + 1 zero byte).

    Parameters:
        file_path (str): Path to the binary file.
        start_offset (int): Offset where the map data starts.
        rows (int): Number of rows in the map.
        cols (int): Number of columns in the map.
    """
    tile_symbols = hex_to_unicode

    with open(file_path, "rb") as f:
        # Seek to the start of the map data
        f.seek(start_offset)

        # Read the required number of bytes (rows * cols * 2 bytes per tile)
        data = f.read(rows * cols * 2)

    # Process the data to extract only the first byte of each 2-byte pair
    tile_values = [data[i] for i in range(0, len(data), 2)]
    print(tile_values)

    # Print the map as ASCII characters
    for row in range(rows):
        line = tile_values[row * cols:(row + 1) * cols]
        print("".join(tile_symbols.get(byte, '?') for byte in line))


# Example Usage
#file_path = "../dumps/run3/floor2/(238) 0x114470000 - 0x114C64000 rw-"  # Replace with your file path
first_match = find_first_match(file_path, map_start)

if first_match != -1:
    print(f"First match found at offset: {first_match}")
    start_offset = first_match + 8
    print_ascii_map(file_path, start_offset, rows=112, cols=112)
else:
    print("Sequence not found.")


# Example Usage
