import struct

# Memory Locations and lengths in bytes
memloc_unknown0 = 0x00
memlen_unknown0 = 4

memloc_file_length = 0x04
memlen_file_length = 2

memloc_unknown1 = 0x06
memlen_unknown1 = 6

memloc_mode = 0x0c
memlen_mode = 1

memloc_unknown2 = 0x0d
memlen_unknown2 = 25

memloc_name = 0x26
memlen_name = 128

memloc_tile = 0xb8
memlen_tile = 966

memloc_obj_count  = 0x47e
memlen_obj_count  = 80

memloc_obj = 0x4ce
memlen_obj = 0 # to EOF

# Type Data
game_modes_amount = 4
game_modes = {
	'solo' : 0x00,
	'coop' : 0x01,
	'race' : 0x02,
	'unset' : 0x04
}

tile_amount = -1 # FIX ME
tile_data = {
        'empty' : 0x00,
        'full' : 0x01
}

object_amount = 0x1c + 1
object_length_bytes = 5 #number of bytes in an object
object_data = {
	'ninja' : 0x00,
	'mine' : 0x01,
	'gold' : 0x02,
	'exit' : 0x03,
	'exit switch' : 0x04,
	'regular door' : 0x05,
	'locked door' : 0x06,
	'locked door switch' : 0x07,
	'trap door' : 0x08,
	'trap door switch' : 0x09,
	'bounce pad' : 0x0a,
	'one way' : 0x0b,
	'chaingun drone' : 0x0c,
	'laser drone' : 0x0d,
	'zap drone' : 0x0e,
	'chaser drone' : 0x0f,
	'floor guard' : 0x10,
	'bounce block' : 0x11,
	'rocket turret' : 0x12,
	'gauss turret' : 0x13,
	'thwump' : 0x14,
	'toggle mine' : 0x15,
	'evil ninja' : 0x16,
	'laser turret' : 0x17,
	'boost pad' : 0x18,
	'deathball' : 0x19,
	'micro drone' : 0x1a,
	'deathball unknown' : 0x1b,
	'shove thwump' : 0x1c
}

# Map Constants
map_width = 42
map_height = 23

def write_file_length( map, length = None ):
	"This writes the length of the file to the file, if length is None get_file_size_bytes() is used"
	if(length is None):
		length = get_file_size_bytes(map)
	
	map.seek(memloc_file_length)
	length_short = struct.pack("<h", length) # <h represents little-endian short
	map.write(length_short)

def erase_name( map ):
	"This removes all characters from the name of the map, leaving it blank."
	map.seek(memloc_name)
	map.write(bytes([0x00] * 128))
	
def write_name( map, name ):
	"This writes the name field in a map, does not clear name field beforehand."
	map.seek(memloc_name)
	map.write(bytes(name.encode(encoding='ascii')))

def write_mode( map, mode ):
	"This writes the mode of the map. Modes: 'solo', 'coop', 'race', 'unset'."
	map.seek(memloc_mode)
	map.write(bytes([game_modes[mode]]))

def write_tile( map, tile, location_x, location_y = None ):
	if(location_y is not None):
		location_x += location_y * map_width
	
	map.seek(memloc_tile + location_x)
	map.write(bytes([tile_data[tile]]))
	
def write_object( map, obj, index ):
	"Write object in file at index, obj should be list with exmaple format: ['mine', 4, 3, 0, 0]"
	map.seek(memloc_obj + index * 5)
	obj[0] = object_data[obj[0]]
	map.write(bytes(obj))

def write_obj_count( map, obj, count ):
	"Writes the object count for the object represented by obj, for the amount of (integer) count."
	obj_num = object_data[obj]
	map.seek(memloc_obj_count + obj_num * 2) # add obj_num * 2 as offset, each object is a 2 byte short
	count_short_bytes = struct.pack("<h", count)
	map.write(count_short_bytes)
	
def get_file_size_bytes( file ):
	"Returns the number of bytes in file"
	map.seek(0, 2) #seek 0 bytes (0), relative to the end of the file (2)
	return map.tell() #return file's current position (EOF)
	
def get_object_counts( map ):
	"Returns array of integers representing counts of objects found in object data area"
	object_counts = [] * object_amount #one integer per object
	map.seek(memloc_obj)
	while(map.tell < get_file_size_bytes(map)):
		
	

f = open("TILE TOP", "r+b")
erase_name(f)
write_name(f, 'Level name, first test. Long name is okay?')
write_mode(f, 'unset')
write_object(f, ['gold', 43, 42, 0, 1], 0)

f.close()
