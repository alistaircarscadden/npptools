#Python3.6

from map import *

import sys
import random

def carve_random( tiles ):
	x0 = random.randint(0, map_width - 1)
	y0 = random.randint(0, map_height - 1)
	x1 = random.randint(0, map_width - 1)
	y1 = random.randint(0, map_height - 1)
	
	for xi in range(min(x0, x1), max(x0, x1)):
		for yi in range(min(y0, y1), max(y0, y1)):
			tiles[xi][yi] = 'empty'
			
def random_tile() :
	"Returns coordinate pair to a random tile"
	return [random.randint(0, map_width - 1), random.randint(0, map_height - 1)]

def path_current_pos( path ):
	"Used by path to get current position"
	return path[len(path) - 1]
	
def generate_path( ):
	path = [] # list of coordinate pair lists eg, [5, 4], [3, 2]
	path.append(random_tile())
	
	num_nodes = 1
	going_vertical = True if random.random() >= 0.5 else False
	while(random.random() > (num_nodes/10)):
		cur_pos = path_current_pos(path)
		if(going_vertical):
			going_down = True if random.random() >= (cur_pos[1] / map_height) else False
			if(going_down):
				new_y = random.randint(cur_pos[1] + 1, map_height - 1)
				path.append([cur_pos[0], new_y])
			else: #going up
				new_y = random.randint(0, cur_pos[1] - 1)
				path.append([cur_pos[0], new_y])
		else: #going horizontal
			going_right = True if random.random() >= (cur_pos[0] / map_width) else False
			if(going_right):
				new_x = random.randint(cur_pos[0], map_width - 1)
				path.append([new_x, cur_pos[1]])
			else: #going left
				new_x = random.randint(0, cur_pos[0] - 1)
				path.append([new_x, cur_pos[1]])
		going_vertical = not going_vertical
	
	return path

if(len(sys.argv) != 2):
	print("Usage: py srgen.py <map name>")
	
map = open(sys.argv[1], "w+b") # "w+b" : truncate to write binary mode
map.close()
map = open(sys.argv[1], "r+b") # "r+b" : truncate, readwrite, binary, once file exists

tiles = [0] * map_width
for i in range(0, map_width):
	tiles[i] = ['full'] * map_height
	
path = generate_path()
print(path)
for i in range(0, len(path) - 2):
	_from = path[i]
	_to = path[i + 1]
	
	x_step = 0 if _from[0] == _to[0] else -1 if _from[0] > _to[0] else 1
	y_step = 0 if _from[1] == _to[1] else -1 if _from[1] > _to[1] else 1
	length = abs(_to[0] - _from[0] + _to[1] - _from[1])
	_pos = [_from[0], _from[1]] # copy

	for i in range(0, length):
		tiles[_pos[0]][_pos[1]] = 'empty'
		_pos[0] += x_step
		_pos[1] += y_step

empty_tile = [0, 0]
for x in range(0, len(tiles)):
	for y in range(0, len(tiles[0])):
		if(tiles[x][y] == 'empty'):
			empty_tile = obj_coord_of_tile(x, y)

for x in range(0, len(tiles)):
	for y in range(0, len(tiles[0])):
		write_tile(map, tiles[x][y], x, y)

write_object(map, ['ninja', empty_tile[0] + 2, empty_tile[1] + 2, 0, 0], 0)
write_name(map, sys.argv[1])
write_mode(map, 'solo')
write_essentials(map)

map.close()