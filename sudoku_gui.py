import pygame
import time
import tables
import sys
import os
from board import Board
from place import Place


# Placing the game window on the screen
x = 300
y = 40
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)




pygame.font.init()


screen = pygame.display.set_mode((540,660),0,32)
font = pygame.font.SysFont("comicsans", 40)
title_font = pygame.font.SysFont("comicsans", 50)
big_title_font = pygame.font.SysFont("comicsans", 60)




def redraw_window(win, board, time = None, false_answers = 0, is_finished = False, last_timer =None, is_custom = False):
	win.fill((255,255,255))
	if time != None:
		# Draw time
		fnt = pygame.font.SysFont("comicsans", 40)
		if is_finished:
			text = fnt.render("Time: " + format_time(last_timer), 1, (0,0,0))
		else:
			text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
		win.blit(text, (540 - 160, 560))
		# Draw False answers
		text = fnt.render("X " * false_answers, 1, (255, 0, 0))
		win.blit(text, (20, 560))
	# Draw grid and board
	board.draw(is_finished, is_custom)


def format_time(secs):
	sec = secs%60
	minute = secs//60
	hour = minute//60

	mat = " " + str(minute) + ":" + str(sec)
	return mat

def draw_text(text,fnt,color,surface,x,y):
	textobj = fnt.render(text,1,color)
	surface.blit(textobj,(x,y))

def draw_instructions(screen,custom_button, puzzle_num):
	title_font = pygame.font.SysFont("comicsans", 40)
	big_title_font = pygame.font.SysFont("comicsans", 50)
	font = pygame.font.SysFont(None, 25)

	draw_text("Welcome to the Sudoku Game/Solver!",big_title_font,(0,0,0),screen, 210,10)
	draw_text("How it works:",title_font,(0,0,0),screen, 18,40)
	draw_text("1- You can solve default puzzles or create your own puzzle and solve it",font,(0,0,0),screen, 18,70)
	draw_text("2- If you want to solve default puzzles type in the puzzle number(1-32)",font,(0,0,0),screen, 18,100)
	draw_text(" you want to solve and press enter",font,(0,0,0),screen, 34,120)
	draw_text("3- If you want to create your own puzzle click on the create puzzle button",font,(0,0,0),screen, 18,140)

	draw_text("Solver Instructions",title_font,(0,0,0),screen, 18,170)
	draw_text("1- You can select a cell by clicking on it",font,(0,0,0),screen, 18,200)
	draw_text("2- You can temporarily assign a number to the selected cell by typing the number you want",font,(0,0,0),screen, 18,220)
	draw_text("3- You can delete the assigned number by pressing backspace button",font,(0,0,0),screen, 18,240)
	draw_text("4- If you want to check whether the assigned values are true or not, you can press enter",font,(0,0,0),screen, 18,260)
	draw_text("5- True values will be permanent on the grid, false values will be deleted",font,(0,0,0),screen, 18,280)
	draw_text("6- There will be red X's on the bottom left which will indicate how many wrong assignments",font,(0,0,0),screen, 18,300)
	draw_text(" you did",font,(0,0,0),screen, 34,320)
	draw_text("7- If you want to see the answer of the puzzle, you can press spacebar anytime you want and ",font,(0,0,0),screen, 18,340)
	draw_text(" watch how the engine solves the puzzle", font, (0,0,0), screen, 34, 360)
	draw_text("8- If you want to solve other puzzles, you can click on the Main Page button and get back to", font, (0,0,0), screen, 18, 380)
	draw_text(" this page and enjoy other puzzles", font, (0,0,0), screen, 34, 400)

	draw_text("Custom Puzzle Creator Instructions",title_font,(0,0,0),screen, 18,430)
	draw_text("1- You can select a cell by clicking on it",font,(0,0,0),screen, 18,460)
	draw_text("2- You can add the numbers you want to these cells",font,(0,0,0),screen, 18,480)
	draw_text("3- If you finished constructing the puzzle press enter and click Check Puzzle button",font,(0,0,0),screen, 18,500)
	draw_text("4- If your puzzle is valid, you can start solving it",font,(0,0,0),screen, 18,520)
	draw_text("5- If it is not valid, the game will warn you!",font,(0,0,0),screen, 18,540)
	draw_text("6- You can delete the values on the cells by clicking on them and pressing backspace",font,(0,0,0),screen, 18,560)
	draw_text("7- Be sure that your puzzle has unique solution",font,(0,0,0),screen, 18,580)
	draw_text("8- If not, you and the engine may get different answers",font,(0,0,0),screen, 18,600)
	draw_text("9- DO NOT FORGET TO PRESS ENTER BEFORE CLICKING ON THE CHECK PUZZLE BUTTON!",font,(0,0,0),screen, 18,620)
	draw_text("If you are ready let's get started!", font, (0,0,0), screen, 240, 660)
	draw_text("Type in the puzzle number(1-32) you want to solve and press enter:",font,(0,0,0),screen, 18,680)
	draw_text(puzzle_num,font,(0,0,0),screen, 573,680)
	pygame.draw.rect(screen, (0,0,255), custom_button)
	draw_text("Create Puzzle",font,(0,0,0),screen, 625,710)


# Game Page
def game(puzzle_num = None, custom_puzzle = None, solved_puzzle = None):
	screen = pygame.display.set_mode((540,660))
	if custom_puzzle == None: # If user wants to solve default puzzles
		board = Board(540,540,screen, puzzle_num)
		solved_board = Board(540,540, screen, puzzle_num)
		solved_board.make_implication(solved_board.model,[],solved_board.remaining_places, False)
		solved_board.solve_gui(False)

	else: # If user created custom puzzle, than the puzzle and its answer is assigned
		board = Board(540,540,screen, custom_puzzle = custom_puzzle)
		solved_board = solved_puzzle
	key = None
	run = True
	start = time.time()
	false_answers = 0
	stop_timer = False
	last_timer = None
	click = False

	while run:
		mx, my = pygame.mouse.get_pos()
		main_page_button = pygame.Rect(200,600,170,50)
		# If user clicks on the Main Page button
		if main_page_button.collidepoint((mx, my)):
			if click:
				main_page()


		# Counts how many seconds has passed
		play_time = round(time.time() - start)


		# Checks whether the game is over
		is_finished = True
		for i in range(9):
			for j in range(9):
				if board.places[i][j].value != solved_board.places[i][j].value:
					is_finished = False

		# If the game is over, stops the timer
		if is_finished and not(stop_timer):
			stop_timer = True
			last_timer = play_time


		click = False
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					key = 1
				if event.key == pygame.K_2:
					key = 2
				if event.key == pygame.K_3:
					key = 3
				if event.key == pygame.K_4:
					key = 4
				if event.key == pygame.K_5:
					key = 5
				if event.key == pygame.K_6:
					key = 6
				if event.key == pygame.K_7:
					key = 7
				if event.key == pygame.K_8:
					key = 8
				if event.key == pygame.K_9:
					key = 9
				if event.key == pygame.K_KP1:
					key = 1
				if event.key == pygame.K_KP2:
					key = 2
				if event.key == pygame.K_KP3:
					key = 3
				if event.key == pygame.K_KP4:
					key = 4
				if event.key == pygame.K_KP5:
					key = 5
				if event.key == pygame.K_KP6:
					key = 6
				if event.key == pygame.K_KP7:
					key = 7
				if event.key == pygame.K_KP8:
					key = 8
				if event.key == pygame.K_KP9:
					key = 9
				if event.key == pygame.K_BACKSPACE:
					board.clear()
					key = None


				if event.key == pygame.K_SPACE: # If the user wants the engine solve the puzzle
					board.make_implication(board.model,[], board.remaining_places,True)
					board.solve_gui(True)

				if event.key == pygame.K_RETURN: # If the user checks the assigned values are true or not
					for place in board.filled_places:
						row = place[0]
						col = place[1]

						# If the assigned value is true
						if board.places[row][col].temp == solved_board.places[row][col].value:
							board.remaining_places.remove((row,col))
							board.length_of_remaining_places -= 1
							board.places[row][col].set(board.places[row][col].temp)
							board.model[row][col] = board.places[row][col].temp


						# If the assigned value is not true
						else:
							board.places[row][col].set_temp(0)
							board.model[row][col] = 0
							false_answers += 1
					board.filled_places = set()
					key = None



			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
				pos = pygame.mouse.get_pos()
				clicked = board.click(pos)
				if clicked:
					board.select(clicked[0],clicked[1])
					key = None


		if board.selected and key != None:
			board.sketch(key)

		redraw_window(screen, board, play_time, false_answers, is_finished, last_timer)
		pygame.draw.rect(screen, (0,255,0), main_page_button)
		draw_text("Main Page",font,(0,0,0),screen, 215,610)
		pygame.display.update()





# Main Page
def main_page():
	screen = pygame.display.set_mode((1000,780),0,32)
	screen.fill((255,255,255))
	puzzle_num = ""
	click = False
	while True:
		screen.fill((255,255,255))
		mx, my = pygame.mouse.get_pos()
		custom_button = pygame.Rect(600,695,170,50)

		# If user clicks on the create puzzle button
		if custom_button.collidepoint((mx, my)):
			if click:
				custom()

		click = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True


			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_0:
					puzzle_num += str(0)
				if event.key == pygame.K_1:
					puzzle_num += str(1)
				if event.key == pygame.K_2:
					puzzle_num += str(2)
				if event.key == pygame.K_3:
					puzzle_num += str(3)
				if event.key == pygame.K_4:
					puzzle_num += str(4)
				if event.key == pygame.K_5:
					puzzle_num += str(5)
				if event.key == pygame.K_6:
					puzzle_num += str(6)
				if event.key == pygame.K_7:
					puzzle_num += str(7)
				if event.key == pygame.K_8:
					puzzle_num += str(8)
				if event.key == pygame.K_9:
					puzzle_num += str(9)
				if event.key == pygame.K_KP0:
					puzzle_num += str(0)
				if event.key == pygame.K_KP1:
					puzzle_num += str(1)
				if event.key == pygame.K_KP2:
					puzzle_num += str(2)
				if event.key == pygame.K_KP3:
					puzzle_num += str(3)
				if event.key == pygame.K_KP4:
					puzzle_num += str(4)
				if event.key == pygame.K_KP5:
					puzzle_num += str(5)
				if event.key == pygame.K_KP6:
					puzzle_num += str(6)
				if event.key == pygame.K_KP7:
					puzzle_num += str(7)
				if event.key == pygame.K_KP8:
					puzzle_num += str(8)
				if event.key == pygame.K_KP9:
					puzzle_num += str(9)

				if event.key == pygame.K_BACKSPACE:
					puzzle_num = puzzle_num[:len(puzzle_num)-1]

				if event.key == pygame.K_RETURN:
					game(int(puzzle_num)-1)


		draw_instructions(screen,custom_button, puzzle_num)
		pygame.display.update()



def custom():
	screen = pygame.display.set_mode((540,660))
	board = Board(540,540,screen)
	key = None
	run = True
	click = False
	is_valid_table = True

	while run:
		mx, my = pygame.mouse.get_pos()
		options_button = pygame.Rect(280,600,170,50)
		check_button = pygame.Rect(40,600,200,50)

		# If the user clicks on the main page button
		if options_button.collidepoint((mx, my)):
			if click:
				main_page()

		# If user clicks on the check puzzle button
		if check_button.collidepoint((mx, my)):
			if click:
				checked_board = Board(540,540,screen,custom_puzzle = board.model)

				# If there are no same values on the rows, cols, or blocks
				if checked_board.check_the_puzzle(checked_board.model):

					# Solver tries to solve the puzzle
					checked_board.make_implication(checked_board.model,[],checked_board.remaining_places, False)
					checked_board.solve_gui(False)

					# If the board is solvable
					if checked_board.model != None:
						game(custom_puzzle = board.model, solved_puzzle = checked_board)
					else:
						is_valid_table = False
				else:
					is_valid_table = False



		click = False
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					key = 1
				if event.key == pygame.K_2:
					key = 2
				if event.key == pygame.K_3:
					key = 3
				if event.key == pygame.K_4:
					key = 4
				if event.key == pygame.K_5:
					key = 5
				if event.key == pygame.K_6:
					key = 6
				if event.key == pygame.K_7:
					key = 7
				if event.key == pygame.K_8:
					key = 8
				if event.key == pygame.K_9:
					key = 9
				if event.key == pygame.K_KP1:
					key = 1
				if event.key == pygame.K_KP2:
					key = 2
				if event.key == pygame.K_KP3:
					key = 3
				if event.key == pygame.K_KP4:
					key = 4
				if event.key == pygame.K_KP5:
					key = 5
				if event.key == pygame.K_KP6:
					key = 6
				if event.key == pygame.K_KP7:
					key = 7
				if event.key == pygame.K_KP8:
					key = 8
				if event.key == pygame.K_KP9:
					key = 9
				if event.key == pygame.K_BACKSPACE:
					board.clear(is_custom = True)
					key = None


				if event.key == pygame.K_RETURN:
					for place in board.filled_places:
						row = place[0]
						col = place[1]
						board.places[row][col].set(board.places[row][col].temp)
						board.model[row][col] = board.places[row][col].temp

					board.filled_places = set()
					key = None



			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
				pos = pygame.mouse.get_pos()
				clicked = board.click(pos)
				if clicked:
					board.select(clicked[0],clicked[1])
					key = None


		if board.selected and key != None:
			board.sketch(key)

		redraw_window(screen, board, is_custom = True)
		pygame.draw.rect(screen, (0,255,0), options_button)
		pygame.draw.rect(screen, (0,0,255), check_button)
		draw_text("Check Puzzle",font,(0,0,0),screen, 45,610)
		draw_text("Main Page",font,(0,0,0),screen, 295,610)
		if not(is_valid_table):
			draw_text("Not Valid!",font,(255,0,0),screen, 200,560)
		pygame.display.update()




main_page()
pygame.quit()
