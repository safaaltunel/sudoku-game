import pygame, sys

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption("game base")
screen = pygame.display.set_mode((500,500), 0, 32)

font = pygame.font.SysFont(None,40)

def draw_text(text,font,color,surface,x,y):
	textobj = font.render(text,1,color)
	textrect = textobj.get_rect()
	textrect.topleft = (x,y)
	surface.blit(textobj,textrect)

click = False

def main_menu():
	while True:

		screen.fill((255,255,255))
		draw_text("main menu", font, (0,0,0), screen, 20, 20)

		mx, my = pygame.mouse.get_pos()

		button_1 = pygame.Rect(50,100,100,50)
		button_2 = pygame.Rect(50,200,100,50)
		if button_1.collidepoint((mx, my)):
			if click:
				game()

		if button_2.collidepoint((mx,my)):
			if click:
				options()
		pygame.draw.rect(screen,(255,0,0),button_1)
		pygame.draw.rect(screen,(0,255,0),button_2)
		draw_text("options",font,(0,0,0),screen, 60,200)
		draw_text("game",font,(0,0,0),screen, 60,100)

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()

			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True


		pygame.display.update()
		mainClock.tick(60)

def game():
	screen.fill((255,255,255))
	draw_text("game", font, (0,0,0), screen, 20, 20)
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False

			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True		
		pygame.display.update()
		mainClock.tick(60)

def options():
	screen.fill((255,255,255))
	draw_text("options", font, (0,0,0), screen, 20, 20)
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False

			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True		
		pygame.display.update()
		mainClock.tick(60)


main_menu()