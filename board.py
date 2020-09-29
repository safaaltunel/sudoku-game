from place import Place
import tables
import pygame


# Class for the board on the screen. Design of the class is inspired from Tech With Tim. Solver algorithm is fully constructed and implemented by myself.
class Board:
	
	# self.width indicates the width of the board
	# self.height indicates the height of the board
	# self.puzzle_num indicates the puzzle number in the tables.py file. If the user wants to solve default puzzles in the tables.py file, puzzle_num specifies which puzzle will be solved.
	# self.custom_puzzle indicates the custom puzzle that constructed by the user. 
	# If the puzzle_num and custom_puzzle is not given, that means user wants to construct a default puzzle so the beginning of the table is an empty table.
	# self.table indicates the table which will be solved.
	# self.model indicates the current puzzle state in any time. Always self.model is depicted on the screen.
	# self.remaining_places indicates the empty places on the puzzle.
	# self.filled_places indicates the temporarily filled cells on the screen. If the user checks these filled places(by pressing enter), filled_places becomes empty and ready for next filled places.
	def __init__(self,width, height, screen, puzzle_num = None, custom_puzzle = None):
		if custom_puzzle == None:
			if puzzle_num == None:
				self.table = [[0 for j in range(9)] for i in range(9)]
			else:
				self.table = tables.all_tables[puzzle_num]
		else:
			self.table = custom_puzzle
		self.remaining_places =  set([(i,j) for i in range(9) for j in range(9) if self.table[i][j] == 0])
		self.length_of_remaining_places = len(self.remaining_places)
		self.filled_places = set()
		self.width = width
		self.height = height
		self.places = [[Place(self.table[i][j], i, j, width, height) for j in range(9)] for i in range(9)]
		self.model = [[self.places[i][j].value for j in range(9)] for i in range(9)]
		self.selected = None
		self.screen = screen


	# Returns the clicked position on the screen
	def click(self, pos):
		if pos[0] < self.width and pos[1] < self.height:
			gap = self.width / 9
			x = pos[0] // gap
			y = pos[1] // gap
			return (int(y),int(x))
		else:
			return None


	# If a number is temporarily assigned on a cell, temp value of the cell is updated and the cell is added to the filled_places
	def sketch(self, val):
		row, col = self.selected
		self.places[row][col].set_temp(val)
		self.filled_places.add((row,col))



	# If a cell is selected, all the other cells become unselected.
	def select(self, row, col):
		for i in range(9):
			for j in range(9):
				self.places[i][j].selected = False

		self.places[row][col].selected = True
		self.selected = (row,col)



	# If the table is custom table, all the cells' values can be deleted, if it is a game table only the unpermanent values can be deleted.
	def clear(self, is_custom = False):
		row,col = self.selected
		if not(is_custom):
			if self.places[row][col].value == 0:
				self.filled_places.remove((row,col))
				self.places[row][col].set_temp(0)
		else:
			self.places[row][col].set_temp(0)
			self.places[row][col].set(0)
			self.model[row][col] = 0
			



	def draw(self, is_finished, is_custom):
		# Draw Grid Lines
		gap = self.width / 9
		for i in range(10):
			if i % 3 == 0:
				thick = 5
			else:
				thick = 1
			pygame.draw.line(self.screen, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
			pygame.draw.line(self.screen, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

		# Draw Places
		for i in range(9):
			for j in range(9):
				self.places[i][j].draw(self.screen, is_finished, is_custom)


	def get_block_nums(self,table,row,col):
		row_start = (row//3)*3
		col_start = (col//3)*3
		return [table[i][j] for i in range(row_start, row_start+3)  for j in range(col_start, col_start+3)]


	def find_possible_nums(self,table, row_nums, col_nums, row, col):
		all_nums = {1,2,3,4,5,6,7,8,9}
		return all_nums.difference(set(row_nums).union(set(col_nums)).union(set(self.get_block_nums(table,row,col))))


	def find_possible_places_in_row(self,table, num, row):
		possible_places = []
		for col in range(9):
			if table[row][col] == 0:
				if num in self.find_possible_nums(table, table[row], [table[j][col] for j in range(9)], row, col):
					possible_places.append((row,col))
		return possible_places

	def find_possible_places_in_column(self,table, num, column):
		possible_places = []
		for row in range(9):
			if table[row][column] == 0:
				if num in self.find_possible_nums(table, table[row], [table[j][column] for j in range(9)], row, column):
					possible_places.append((row,column))
		return possible_places

	def find_possible_places_in_block(self,table,num,row,col):
		possible_places = []
		for i in range((row//3)*3, (row//3)*3 + 3):
			for j in range((col//3)*3, (col//3)*3 + 3):
				if table[i][j] == 0:
					if num in self.find_possible_nums(table, table[i], [table[k][j] for k in range(9)], i, j):
						possible_places.append((i,j))
		return possible_places


	def make_implication(self,table, implied_places, remaining_places, is_gui):
		is_changed = False
		for row_num in range(9):
			if self.make_implication_by_rows(table,row_num,implied_places, remaining_places, is_gui) == True:
				is_changed = True
		for col_num in range(9):
			if self.make_implication_by_columns(table,col_num,implied_places, remaining_places, is_gui) == True:
				is_changed = True
		for block_num in range(9):
			if self.make_implication_by_blocks(table,block_num,(block_num%3)*3, implied_places, remaining_places, is_gui) == True:
				is_changed = True

		if is_changed == True:
			self.make_implication(table, implied_places, remaining_places, is_gui)

	def make_implication_by_rows(self,table, row, implied_places, remaining_places, is_gui):
		row_nums = set(table[row])
		possible_nums = {1,2,3,4,5,6,7,8,9}.difference(row_nums)
		for num in possible_nums:
			possible_places = self.find_possible_places_in_row(table, num, row)
			if len(possible_places) == 1:
				table[possible_places[0][0]][possible_places[0][1]] = num
				self.places[possible_places[0][0]][possible_places[0][1]].set(num)
				if is_gui:
					self.places[possible_places[0][0]][possible_places[0][1]].draw_change(self.screen, True)
					pygame.display.update()
					pygame.time.delay(50)
				implied_places.append((possible_places[0][0], possible_places[0][1]))
				remaining_places.remove((possible_places[0][0], possible_places[0][1]))
				self.length_of_remaining_places -= 1
				return True
		return False


	def make_implication_by_columns(self,table, column, implied_places, remaining_places, is_gui):
		col_nums = set([table[row][column] for row in range(9)])
		possible_nums = {1,2,3,4,5,6,7,8,9}.difference(col_nums)
		for num in possible_nums:
			possible_places = self.find_possible_places_in_column(table, num, column)
			if len(possible_places) == 1:
				table[possible_places[0][0]][possible_places[0][1]] = num
				self.places[possible_places[0][0]][possible_places[0][1]].set(num)
				if is_gui:
					self.places[possible_places[0][0]][possible_places[0][1]].draw_change(self.screen, True)
					pygame.display.update()
					pygame.time.delay(50)
				implied_places.append((possible_places[0][0], possible_places[0][1]))
				remaining_places.remove((possible_places[0][0], possible_places[0][1]))
				self.length_of_remaining_places -= 1
				return True
		return False

	def make_implication_by_blocks(self,table, row, col, implied_places, remaining_places, is_gui):
		block_nums = set(self.get_block_nums(table,row,col))
		possible_nums = {1,2,3,4,5,6,7,8,9}.difference(block_nums)
		for num in possible_nums:
			possible_places = self.find_possible_places_in_block(table, num, row, col)
			if len(possible_places) == 1:
				table[possible_places[0][0]][possible_places[0][1]] = num
				self.places[possible_places[0][0]][possible_places[0][1]].set(num)
				if is_gui:
					self.places[possible_places[0][0]][possible_places[0][1]].draw_change(self.screen, True)
					pygame.display.update()
					pygame.time.delay(50)
				implied_places.append((possible_places[0][0], possible_places[0][1]))
				remaining_places.remove((possible_places[0][0], possible_places[0][1]))
				self.length_of_remaining_places -= 1
				return True
		return False

	def revert_implications(self,table, implied_places, is_gui):
		for place in implied_places:
			table[place[0]][place[1]] = 0
			if is_gui:
				self.places[place[0]][place[1]].draw_change(self.screen, False)
				pygame.display.update()
				pygame.time.delay(50)
		self.length_of_remaining_places += len(implied_places)

	def check_the_puzzle(self, puzzle):
		for row in puzzle:
			if not(self.check_rows(row)):
				return False
		for col in range(9):
			col_nums = [puzzle[row][col] for row in range(9)]
			if not(self.check_cols(col_nums)):
				return False
		for row in range(0,9,3):
			for col in range(0,9,3):
				block_nums = self.get_block_nums(puzzle,row,col)
				if not(self.check_blocks(block_nums)):
					return False

		return True

	def check_rows(self, row):
		count = 0
		nums = set()
		for num in row:
			if num != 0:
				count += 1
				nums.add(num)
		return count == len(nums)

	def check_cols(self, col):
		count = 0
		nums = set()
		for num in col:
			if num != 0:
				count += 1
				nums.add(num)
		return count == len(nums)

	def check_blocks(self,block):
		count = 0
		nums = set()
		for num in block:
			if num != 0:
				count += 1
				nums.add(num)
		return count == len(nums)


	# This method uses basic backtracking but in every step, it checks the table and makes implications in order to not try unnecessary values.
	# is_gui parameter indicates if the solver method needs to print every step on the screen or it only needs to solve the puzzle.
	def solve_gui(self, is_gui):
		if self.length_of_remaining_places == 0:
			return True
		cur = self.remaining_places.pop()
		row, col = cur[0], cur[1]
		self.length_of_remaining_places -= 1
		row_nums = self.model[row]
		col_nums =  [self.model[i][col] for i in range(9)]
		possible_nums = self.find_possible_nums(self.model, row_nums, col_nums, row, col)
		for candidate in possible_nums:
			self.model[row][col] = candidate
			self.places[row][col].set(candidate)
			if is_gui:
				self.places[row][col].draw_change(self.screen, True)
				pygame.display.update()
				pygame.time.delay(50)
			implied_places = []
			self.make_implication(self.model, implied_places, self.remaining_places, is_gui)
			ans = self.solve_gui(is_gui)
			if ans != None:
				return ans
			self.model[row][col] = 0
			self.places[row][col].set(0)
			if is_gui:
				self.places[row][col].draw_change(self.screen, False)
				pygame.display.update()
				pygame.time.delay(50)
			self.revert_implications(self.model, implied_places, is_gui)
			for place in implied_places:
				self.remaining_places.add(place)
		self.remaining_places.add(cur)
		self.length_of_remaining_places += 1
