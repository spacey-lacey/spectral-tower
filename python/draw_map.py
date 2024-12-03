from PIL import Image

tileset = \
{
    0x00: "00.png",
    0x01: "01.png",
    0x02: "02.png",
    0x03: "03.png",
    0x04: "04.png",
    0x05: "05.png",
    0x06: "06.png",
    0x07: "07.png",
    0x08: "08.png",
    0x09: "09.png",
    0x0A: "0A.png",
    0x0B: "0B.png",
    0x0C: "0C.png",
    0x0D: "0D.png",
    0x0E: "0E.png",
    0x0F: "0F.png",
    0x10: "10.png",
    0x11: "11.png",
    0x12: "12.png",
    0x13: "13.png",
    0x14: "14.png",
    0x15: "15.png",
    0x16: "16.png",
    0x18: "18.png",
    0x19: "19.png",
    0x1A: "1A.png",
    0x1B: "1B.png",
    0x1C: "1C.png",
    0x1D: "1D.png"
}

def draw_map(map_tiles, tileset):
    tile_size = 32  # Size of each tile in pixels
    width = len(map_tiles[0]) * tile_size
    height = len(map_tiles) * tile_size

    map_image = Image.new("RGB", (width, height))
    for y, row in enumerate(tilemap):
        for x, tile_id in enumerate(row):
            tile_image = Image.open(tileset[tile_id])
            map_image.paste(tile_image, (x * tile_size, y * tile_size))

    map_image.show()

# Example: Draw the map
# Assume tileset is preloaded with images for each tile ID
draw_map(map_tiles, tileset)
