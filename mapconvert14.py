import map
import struct

# Constants
map_width = 31
map_height = 23

tile_data = {
	'0' : 'empty',
	'1' : 'full',
	'3' : 'slopeSE',
	'2' : 'slopeSW',
	'4' : 'slopeNE',
	'5' : 'slopeNW',
	'G' : 'halfslopeVSE',
	'F' : 'halfslopeVSW',
	'H' : 'halfslopeVNE',
	'I' : 'halfslopeVNW',
	'?' : 'halfslopeHSE',
	'>' : 'halfslopeHSW',
	'@' : 'halfslopeHNE',
	'A' : 'halfslopeHNW',
	'7' : 'quarterpipeSE',
	'6' : 'quarterpipeSW',
	'8' : 'quarterpipeNE',
	'9' : 'quarterpipeNW',
	'Q' : 'halfW',
	'P' : 'halfN',
	'N' : 'halfS',
	'O' : 'halfE',
	'K' : 'raisedslopeVSE',
	'J' : 'raisedslopeVSW',
	'L' : 'raisedslopeVNE',
	'M' : 'raisedslopeVNW',
	'C' : 'raisedslopeHSE',
	'B' : 'raisedslopeHSW',
	'D' : 'raisedslopeHNE',
	'E' : 'raisedslopeHNW',
	';' : 'quartermoonSE',
	':' : 'quartermoonSW',
	'<' : 'quartermoonNE',
	'=' : 'quartermoonNW'
}

# Script (I get this is ugly...)
f = open("off.txt", "r")
map_text = f.read()
f.close()

tiles = [[]] * map_width
for i in range(len(tiles)):
	tiles[i] = [''] * map_height

for i in range(len(map_text)):
	tiles[i // map_height][i % map_height] = map_text[i]
	
for i in range(len(tiles)):
	for c in range(len(tiles[i])):
		tiles[i][c] = tile_data[tiles[i][c]]

f = open("doesntexist", "w")
f.close()

f = open("doesntexist", "r+b")

f.seek(0x4cd)
f.write(b'\00')

f.seek(map.memloc_tile)
for y in range(map_height):
	for x in range(map_width):
		map.write_tile(f, tiles[x][y], x, y)
		
map.write_name(f, 'Tile converter!!!!!')
map.write_mode(f, 'solo')

map.write_essentials(f)
		
f.close()
	
	