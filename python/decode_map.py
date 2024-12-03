from PIL import Image
from draw_map import tileset

def decode_map(file_path, width=112, height=112):
    with open(file_path, "rb") as f:
        raw_data = f.read()

    # Decode the map tiles (assuming 2 bytes per tile)
    tiles = []
    for i in range(0, len(raw_data), 2):
        tile = raw_data[i]  # Use the first byte as the tile ID
        tiles.append(tile)

    # Convert the flat list into a 2D array
    return [tiles[i:i + width] for i in range(0, len(tiles), width)]


def draw_map(tilemap, tileset, tile_size=32, default_tile_id=0x00):
    """
    Draws a map based on tile IDs and a tileset dictionary.
    If a tile ID is not in the dictionary, it uses the default tile.

    Parameters:
        map_tiles (list of lists): 2D array of tile IDs.
        tileset (dict): Dictionary where keys are tile IDs and values are PIL images.
        tile_size (int): Size of each tile in pixels.
        default_tile_id (int): ID of the default tile to use for missing entries.
    """
    # Get the default tile image
    default_tile = tileset.get(default_tile_id)
    if default_tile is None:
        raise ValueError(f"Default tile ID {default_tile_id} not found in tileset.")

    map_height = len(tilemap)
    map_width = len(tilemap[0])
    map_image = Image.new("RGB", (map_width * tile_size, map_height * tile_size))

    # Draw the map
    for y, row in enumerate(map_tiles):
        for x, tile_id in enumerate(row):
            if tile_id in tileset.keys():
                tile_image = Image.open("../assets/" + tileset[tile_id])
            else:
                tile_image = Image.open("../assets/" + tileset[default_tile_id])
            map_image.paste(tile_image, (x * tile_size, y * tile_size))

    # Display the map
    map_image.show()

# Example: Draw the map
# Assume tileset is preloaded with images for each tile ID
map_tiles = decode_map("map_data.bin")
draw_map(map_tiles, tileset)
