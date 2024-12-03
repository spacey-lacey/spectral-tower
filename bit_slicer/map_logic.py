# map logic for Bit Slicer written as a script

from bitslicer import VirtualMemoryError, DebuggerError
from map_rendering import decode_map, draw_map, display_map


# finding the map
map_start_sequence = "23 00 00 00 70 70 20 20"
map_sequence_length = 8
n_map_columns = 112
n_map_rows = 112
n_map_bytes = 2 * n_map_rows * n_map_columns # 2 bytes per tile

# finding the floor/tower values
# positions are relative to map_sequence_address
random_values_offset = 0x1142C4000 - 0x1142732D0
random_values_length = 4
tower_offset = 0x1142C4000 - 0x1141A0A24
tower_to_floor_offset = 3

# tower ID to name for debug notifying
tower_name = \
{
    0x01: "Goblin Tower",
    0x02: "Robber Tower",
    0x03: "Queenrose Tower",
    0x04: "Spectral Tower",
    0x05: "The Final Tower",
    0x06: "None (not in a tower)"
}

# how often to check for new floor
time_interval = 1 # seconds


class MapLogic(object):

    def __init__(self, vm, debug):

        self.vm = vm
        self.debug = debug
        self.debug.log("Initializing map script...")

        # locate map by known byte string
        addresses = vm.scanByteString(map_start_sequence)
        map_sequence_address = addresses[0]
        self.debug.log("Found map start sequence at " + str(hex(map_sequence_address)))

        # where we start reading the map
        self.map_start_address = map_sequence_address + map_sequence_length

        # locate tower/floor ID relative to map sequence
        self.tower_address = map_sequence_address - tower_offset
        self.floor_address = self.tower_address + tower_to_floor_offset
        self.debug.log("Calculated tower/floor address: " + str(hex(self.tower_address)))
        self.update_tower()
        self.update_floor()

        # now the weird random values
        self.random_values_address = map_sequence_address - random_values_offset
        self.debug.log("Calculated random floor values address: " + str(hex(self.random_values_address)))
        self.update_random_values()

        # initialize time
        self.time_passed = 0

        # update map if we are in a tower
        self.update_map_values()
        self.create_and_display_map()


    def execute(self, delta_time):
        self.update_time(delta_time)

        # every time interval, check if we are on a new floor
        if self.time_passed >= time_interval:

            # random values change when we move to a new floor
            # but they also change when we defeat a boss
            current_random_values = self.get_random_values()
            if current_random_values != self.random_values:
                self.update_random_values()

                # so we need to check whether the floor actually changed
                # or whether we entered a tower (floor = 0 in overworld and first floor)
                current_floor = self.get_floor()
                current_tower = self.get_tower()
                if current_floor != self.floor or current_tower != self.tower:
                    if current_floor != self.floor:
                        self.update_floor()
                    if current_tower != self.tower:
                        self.update_tower() # only "need" this for map naming

                    self.update_map_values()
                    self.create_and_display_map()

            self.reset_time()


    def finish(self):
        self.debug.log("Map logic terminated.")


    def get_random_values(self):
        '''
        return current random "floor" values
        '''
        return self.vm.readBytes(self.random_values_address, random_values_length)

    def update_random_values(self):
        '''
        update stored random values
        '''
        self.random_values = self.get_random_values()
        self.debug.log("Random values changed to " + str(self.random_values))


    def get_floor(self):
        '''
        return current floor number, which is a "big endian" 16-bit int
        bit slicer can't seem to adjust for this, so we do it ourselves
        floor numbering starts at 0 internally, so we add 1
        '''
        floor_bytes = self.vm.readBytes(self.floor_address, 2) # 2 bytes
        return int.from_bytes(floor_bytes, byteorder="big") + 1

    def update_floor(self):
        '''
        update stored floor number
        '''
        self.floor = self.get_floor()
        self.debug.log("Floor changed to " + str(self.floor))


    def get_tower(self):
        '''
        return current tower as integer ID
        '''
        return self.vm.readInt8(self.tower_address)

    def update_tower(self):
        '''
        update stored tower ID and name
        '''
        self.tower = self.get_tower()
        self.tower_name = tower_name[self.tower]
        self.debug.log("Tower changed to " + self.tower_name)


    def update_map_values(self):
        '''
        update stored map values if we are in a tower
        1-5 are valid towers, 6 is the overworld map
        '''
        if (self.tower < 6):
            self.map_values = self.vm.readBytes(self.map_start_address, n_map_bytes)
            self.debug.log("Read " + str(n_map_bytes) + " map bytes")
        else:
            self.debug.log("Map not read in (not in a tower)")

    def create_and_display_map(self):
        '''
        create and save/display map however i decided
        need to add that functionality tho
        '''
        map_tiles = decode_map(self.map_values, n_map_rows, n_map_columns)
        map_image = draw_map(map_tiles, n_map_rows, n_map_columns)
        display_map(map_image)


    def reset_time(self):
        '''
        reset time interval for checking random values
        '''
        self.time_passed -= time_interval

    def update_time(self, delta_time):
        '''
        update current time on each cycle
        '''
        self.time_passed += delta_time
