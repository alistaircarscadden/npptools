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
game_modes = {
	'solo' : 0x00,
	'coop' : 0x01,
	'race' : 0x02,
	'unset' : 0x04
}

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

f = open("TILE TOP", "r+b")

write_mode(f, 'race')
f.close()
	

	