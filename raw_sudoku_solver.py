def get_block_nums(table,row,col):
	row_start = (row//3)*3
	col_start = (col//3)*3
	return [table[i][j] for i in range(row_start, row_start+3)  for j in range(col_start, col_start+3)]


def find_possible_nums(table, row_nums, col_nums, row, col):
	all_nums = {1,2,3,4,5,6,7,8,9}
	return all_nums.difference(set(row_nums).union(set(col_nums)).union(set(get_block_nums(table,row,col))))


def find_possible_places_in_row(table, num, row):
	possible_places = []
	for col in range(9):
		if table[row][col] == 0:
			if num in find_possible_nums(table, table[row], [table[j][col] for j in range(9)], row, col):
				possible_places.append((row,col))
	return possible_places

def find_possible_places_in_column(table, num, column):
	possible_places = []
	for row in range(9):
		if table[row][column] == 0:
			if num in find_possible_nums(table, table[row], [table[j][column] for j in range(9)], row, column):
				possible_places.append((row,column))
	return possible_places

def find_possible_places_in_block(table,num,row,col):
	possible_places = []
	for i in range((row//3)*3, (row//3)*3 + 3):
		for j in range((col//3)*3, (col//3)*3 + 3):
			if table[i][j] == 0:
				if num in find_possible_nums(table, table[i], [table[k][j] for k in range(9)], i, j):
					possible_places.append((i,j))
	return possible_places


def make_implication(table, implied_places, remaining_places):
	is_changed = False
	for row_num in range(9):
		if make_implication_by_rows(table,row_num,implied_places, remaining_places) == True:
			is_changed = True
	for col_num in range(9):
		if make_implication_by_columns(table,col_num,implied_places, remaining_places) == True:
			is_changed = True
	for block_num in range(9):
		if make_implication_by_blocks(table,block_num,(block_num%3)*3, implied_places, remaining_places) == True:
			is_changed = True

	if is_changed == True:
		make_implication(table, implied_places, remaining_places)

def make_implication_by_rows(table, row, implied_places, remaining_places):
	global length_of_remaining_places
	row_nums = set(table[row])
	possible_nums = {1,2,3,4,5,6,7,8,9}.difference(row_nums)
	for num in possible_nums:
		possible_places = find_possible_places_in_row(table, num, row)
		if len(possible_places) == 1:
			table[possible_places[0][0]][possible_places[0][1]] = num
			implied_places.append((possible_places[0][0], possible_places[0][1]))
			remaining_places.remove((possible_places[0][0], possible_places[0][1]))
			length_of_remaining_places -= 1
			return True
	return False


def make_implication_by_columns(table, column, implied_places, remaining_places):
	global length_of_remaining_places
	col_nums = set([table[row][column] for row in range(9)])
	possible_nums = {1,2,3,4,5,6,7,8,9}.difference(col_nums)
	for num in possible_nums:
		possible_places = find_possible_places_in_column(table, num, column)
		if len(possible_places) == 1:
			table[possible_places[0][0]][possible_places[0][1]] = num
			implied_places.append((possible_places[0][0], possible_places[0][1]))
			remaining_places.remove((possible_places[0][0], possible_places[0][1]))
			length_of_remaining_places -= 1
			return True
	return False

def make_implication_by_blocks(table, row, col, implied_places, remaining_places):
	global length_of_remaining_places
	block_nums = set(get_block_nums(table,row,col))
	possible_nums = {1,2,3,4,5,6,7,8,9}.difference(block_nums)
	for num in possible_nums:
		possible_places = find_possible_places_in_block(table, num, row, col)
		if len(possible_places) == 1:
			table[possible_places[0][0]][possible_places[0][1]] = num
			implied_places.append((possible_places[0][0], possible_places[0][1]))
			remaining_places.remove((possible_places[0][0], possible_places[0][1]))
			length_of_remaining_places -= 1
			return True
	return False

def revert_implications(table, implied_places):
	global length_of_remaining_places
	for place in implied_places:
		table[place[0]][place[1]] = 0
	length_of_remaining_places += len(implied_places)


def solve(table, remaining_places):
	global length_of_remaining_places
	if length_of_remaining_places == 0:
		return table
	current_place = remaining_places.pop()
	length_of_remaining_places -= 1
	row, col = current_place[0], current_place[1]
	row_nums = table[row]
	col_nums =  [table[i][col] for i in range(9)]
	possible_nums = find_possible_nums(table, row_nums, col_nums, row, col)
	for candidate in possible_nums:
		table[row][col] = candidate
		implied_places = []
		make_implication(table, implied_places, remaining_places)
		ans = solve(table, remaining_places)
		if ans != None:
			return ans
		table[row][col] = 0
		revert_implications(table, implied_places)
		for place in implied_places:
			remaining_places.add(place)
	remaining_places.add(current_place)
	length_of_remaining_places += 1


if __name__ == "__main__":

	"""
	
	table = [
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,3,0,8,5],
			[0,0,1,0,2,0,0,0,0],
			[0,0,0,5,0,7,0,0,0],
			[0,0,4,0,0,0,1,0,0],
			[0,9,0,0,0,0,0,0,0],
			[5,0,0,0,0,0,0,7,3],
			[0,0,2,0,1,0,0,0,0],
			[0,0,0,0,4,0,0,0,9]
			]

	
	"""
	table = [
			[0,0,0,0,1,0,3,0,0], 
			[6,0,0,4,0,0,0,7,0],
			[0,0,8,0,0,3,2,0,4], 
			[9,0,0,0,0,2,0,1,0], 
			[3,0,1,7,0,5,9,0,8], 
			[0,8,0,1,0,0,0,0,3], 
			[5,0,3,8,0,0,4,0,0], 
			[0,6,0,0,0,4,0,0,7], 
			[0,0,7,0,5,0,0,0,0]
			]

	"""
	table = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    """
	remaining_places = set([(i,j) for i in range(9) for j in range(9) if table[i][j] == 0])
	length_of_remaining_places = len(remaining_places)
	implied_places = []
	make_implication(table, implied_places, remaining_places)
	ans = solve(table, remaining_places)
	for row in ans:
		print(row)