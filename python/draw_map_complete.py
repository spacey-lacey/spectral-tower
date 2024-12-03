from PIL import Image

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



def get_hex_map(file_path, start_offset, rows=112, cols=112):
    """
    Read map tiles from binary data with 2 bytes per tile (1 byte + 1 zero byte)

    Parameters:
        file_path (str): Path to the binary file.
        start_offset (int): Offset where the map data starts.
        rows (int): Number of rows in the map.
        cols (int): Number of columns in the map.

    Returns:
        list: tile IDs
    """
    array = [[0 for _ in range(cols)] for _ in range(rows)]

    with open(file_path, "rb") as f:
        # Seek to the start of the map data
        f.seek(start_offset)

        # Read the required number of bytes (rows * cols * 2 bytes per tile)
        data = f.read(rows * cols * 2)

    # Process the data to extract only the first byte of each 2-byte pair
    tile_values = [data[i] for i in range(0, len(data), 2)]

    # Print the map as ASCII characters
    for row in range(rows):
        array[row] = tile_values[row * cols:(row + 1) * cols]

    return array


def assemble_map(tilemap, tileset, tile_size, output_file):
    """
    Assemble a map from a tilemap and tileset.

    Parameters:
        tilemap (list of lists): 2D array of tile indices.
        tileset (dict): Dictionary mapping tile indices to image paths.
        tile_size (int): Size of each tile (assumes square tiles).
        output_file (str): Path to save the assembled map.
    """
    map_height = len(tilemap)
    map_width = len(tilemap[0])
    map_image = Image.new("RGB", (map_width * tile_size, map_height * tile_size))

    for y, row in enumerate(tilemap):
        for x, tile_id in enumerate(row):
            tile_image = Image.open("../assets/" + tileset[tile_id])
            map_image.paste(tile_image, (x * tile_size, y * tile_size))

    map_image.save(output_file)
tile_size = 32  # Replace with your tile size



file_path = "../dumps/run3/floor1/(238) 0x114470000 - 0x114C64000 rw-"  # Replace with your file path
first_match = find_first_match(file_path, map_start)

if first_match != -1:
    print(f"First match found at offset: {first_match}")
    start_offset = first_match + 8
    array = get_hex_map(file_path, start_offset, rows=112, cols=112)
    assemble_map(array, tileset, tile_size, "map.png")
else:
    print("Sequence not found.")


