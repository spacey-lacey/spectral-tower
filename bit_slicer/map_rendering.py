from config import assets_path
from tileset import tileset
from PIL import Image
import logging


# constants
tile_size = 32
default_tile_id = 0x00


def decode_map(map_data, width, height):
    '''
    translate map data to tile codes
    '''
    # extract tile IDs as a list
    # every other byte is a tile ID (others are zero)
    tiles = [map_data[i] for i in range(0, len(map_data), 2)]

    # convert to an array and check size
    tile_array = [tiles[i:i + width] for i in range(0, len(tiles), width)]
    if len(tile_array) != height:
        raise ValueError(f"Map height should be {height} (got {len(tile_array)})")

    return tile_array


def draw_map(tile_array, width, height):
    '''
    use tile IDs and tileset dictionary to draw map
    '''
    # create image
    image_size = (width * tile_size, height * tile_size)
    map_image = Image.new("RGB", image_size)

    # add tiles
    for y, row in enumerate(tile_array):
        for x, tile_id in enumerate(row):
            position = (x * tile_size, y * tile_size)

            if tile_id in tileset.keys():
                current_tile_id = tile_id
            else:
                # substitute the default (blank) tile
                current_tile_id = default_tile_id
                # print a warning with the missing hex value so we can add it later
                # FIXME not tested
                logging.warning(f"Tile ID {tile_id:#04x} not found")

            tile_image = Image.open(assets_path / tileset[tile_id])
            map_image.paste(tile_image, position)

    return map_image


def display_map(map_image):
    map_image.show()
