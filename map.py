import struct

# Memory Locations and lengths in bytes
memloc_unknown0    = 0x00
memlen_unknown0    = 4

memloc_file_length = 0x04
memlen_file_length = 2

memloc_unknown1    = 0x06
memlen_unknown1    = 6

memloc_mode        = 0x0c
memlen_mode        = 1

memloc_unknown2    = 0x0d
memlen_unknown2    = 25

memloc_name        = 0x26
memlen_name        = 128

memloc_tile        = 0xb8
memlen_tile        = 966

memloc_obj_count   = 0x47e
memlen_obj_count   = 80

memloc_obj         = 0x4ce
memlen_obj         = 0 # to EOF

# Type Data
game_modes_amount = 4
game_modes = {
	'solo'  : 0x00,
	'coop'  : 0x01,
	'race'  : 0x02,
	'unset' : 0x04
}

tile_amount = 34
tile_data = {
    'empty' : 0x00,
    'full' : 0x01,
	'halfN' : 0x02, #N = North
	'halfE' : 0x03, #E = East
	'halfS' : 0x04, #S = South
	'halfW' : 0x05, #W = West
	'slopeNW' : 0x06,
	'slopeNE' : 0x07,
	'slopeSE' : 0x08,
	'slopeSW' : 0x09,
	'quartermoonNW' : 0x0a,
	'quartermoonNE' : 0x0b,
	'quartermoonSE' : 0x0c,
	'quartermoonSW' : 0x0d,
	'quarterpipeNW' : 0x0e,
	'quarterpipeNE' : 0x0f,
	'quarterpipeSE' : 0x10,
	'quarterpipeSW' : 0x11,
	'halfslopeHNW' : 0x12, #H = Horizontal
	'halfslopeHNE' : 0x13,
	'halfslopeHSE' : 0x14,
	'halfslopeHSW' : 0x15,
	'raisedslopeHNW' : 0x16,
	'raisedslopeHNE' : 0x17,
	'raisedslopeHSE' : 0x18,
	'raisedslopeHSW' : 0x19,
	'halfslopeVNW' : 0x1a, #V = Vertical
	'halfslopeVNE' : 0x1b,
	'halfslopeVSE' : 0x1c,
	'halfslopeVSW' : 0x1d,
	'raisedslopeVNW' : 0x1e,
	'raisedslopeVNE' : 0x1f,
	'raisedslopeVSE' : 0x20,
	'raisedslopeVSW' : 0x21
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
map_object_x_min = 4   #0x04
map_object_y_min = 4   #0x04
map_object_x_max = 172 #0xac
map_object_y_max = 96  #0x60

def write_file_length( map, length = None ):
	"This writes the length of the file to the file, if length is None get_file_size_bytes() is used"
	if(length is None):
		length = get_file_size_bytes(map)
	
	map.seek(memloc_file_length)
	length_short = struct.pack("<H", length) # <h represents little-endian short
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
	"Write object in file at index, obj should be list with exmaple format: ['mine', 4, 3, 0, 0] or [2, 4, 3, 0, 0]"
	if(isinstance(obj[0], str)): #if type is string, convert to int
		obj[0] = object_data[obj[0]]
	map.seek(memloc_obj + index * 5)
	map.write(bytes(obj))

def write_object_count( map, obj, count ):
	"Writes the object count for the object represented by obj, for the amount of (integer) count."
	if(isinstance(obj, str)):
		obj_num = object_data[obj]
	else:
		obj_num = obj
	map.seek(memloc_obj_count + obj_num * 2) # add obj_num * 2 as offset, each object is a 2 byte short
	count_short_bytes = struct.pack("<h", count)
	map.write(count_short_bytes)
	
def get_file_size_bytes( file ):
	"Returns the number of bytes in file"
	file_position = file.tell() #remember start position to return to it
	file.seek(0, 2) #seek 0 bytes (0), relative to the end of the file (2)
	file_end_position = file.tell()
	file.seek(file_position)
	return file_end_position #return file's current position (EOF)
	
def bytes_to_int( byte_string ):
	return int(byte_string.decode('utf-8'), 16)
	
def get_object_counts( map ):
	"Returns array of integers representing counts of objects found in object data area"
	object_counts = [0] * object_amount #one integer per object
	map.seek(memloc_obj)
	file_size_bytes = get_file_size_bytes(map)
	
	while(map.tell() < file_size_bytes):
		byte = map.read(1) #byte contains the object type
		obj_type = struct.unpack("B", byte)[0]
		object_counts[obj_type] += 1 #increment the current type's counter
		map.seek(4, 1) #skip the four bytes that are not the object type

	return object_counts
	
def write_object_counts( map, object_counts = None ):
	"Writes the object counts, expects an integer array of length object_amount for object_counts, uses get_object_counts() by default"
	map.seek(memloc_obj_count)
	
	if(object_counts is None):
		object_counts = get_object_counts(map)
	
	for i in range(len(object_counts)):
		write_object_count(map, i, object_counts[i])
		
def sort_objects( map ):
	"Sorts all of the objects by type, necessary for a map to function expectedly"
	map.seek(memloc_obj)
	
	num_objects = get_total_objects(map)
	
	objects = [[]] * num_objects
	for i in range(len(objects)):
		objects[i] = [0] * 5
	
	objects_byte_pos = 0
	byte = map.read(1)
	while(byte):
		byte_value = struct.unpack("B", byte)[0]
		objects[objects_byte_pos//5][objects_byte_pos%5] = byte_value
		objects_byte_pos += 1
		byte = map.read(1)
	
	objects.sort(key=lambda x:x[0])
	
	map.seek(memloc_obj)
	object_index = 0
	for object_list in objects:
		write_object(map, object_list, object_index)
		object_index += 1
		
	
def get_total_objects( map ):
	"Returns the number of objects in a map"
	return (get_file_size_bytes(map) - 0x4ce) // 5 #in brackets is # of bytes in object area of file, each object is 5 bytes

	
def write_essentials( map ):
	"Makes calls to the following functions, all necessary for a map to work: sort_objects, write_object_counts, write_file_length"
	sort_objects(map)
	write_object_counts(map)
	write_file_length(map)
