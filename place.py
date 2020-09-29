import pygame




# Class for each cell on the grid. 
# self.row represents row of the cell on the grid, similarly self.col represents column of the cell on the grid.
# Temp values on the cells are 0


# Design of this class is inspired from Tech With Tim


class Place:
	def __init__(self,value,row,col,width,height):
		self.value = value
		self.temp = 0
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.selected = False



	# Draws the cells on the screen considering different states of the cells
	def draw(self, screen, is_finished, is_custom):
		fnt = pygame.font.SysFont("comicsans", 40)

		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap

		# If the cell assigned to a temporary value
		if self.temp != 0 and self.value == 0:
			text = fnt.render(str(self.temp), 1, (128,128,128))
			screen.blit(text, (x+5, y+5))

		# If the cell has a permanent value
		elif not(self.value == 0):
			text = fnt.render(str(self.value), 1, (0, 0, 0))
			screen.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

		# If the cell is selected, the game is not over and cell does not have a permanent value draw a red rectangle on the cell indicating the selected cell on the screen
		if self.selected and not(is_finished) and self.value == 0:
			pygame.draw.rect(screen, (255,0,0), (x,y, gap ,gap), 3)

		# On the custom game creator page, user can select all the cells, does not matter whether the cell has a permanent value.
		if self.selected and is_custom:
			pygame.draw.rect(screen, (255,0,0), (x,y, gap ,gap), 3)


	# Draws the changed values on the cell while the engine solving the puzzle
	def draw_change(self, screen, is_valid = True):
		fnt = pygame.font.SysFont("comicsans", 40)

		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap

		pygame.draw.rect(screen, (255, 255, 255), (x, y, gap, gap), 0)

		text = fnt.render(str(self.value), 1, (0, 0, 0))
		screen.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
		if is_valid:
			pygame.draw.rect(screen, (0, 255, 0), (x, y, gap, gap), 3)
		else:
			pygame.draw.rect(screen, (255, 0, 0), (x, y, gap, gap), 3)

	def set(self,val):
		self.value = val

	def set_temp(self,val):
		self.temp = val
