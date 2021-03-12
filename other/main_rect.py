from module import *
import pygame
import sys
import math
#s = int(input("Introduce size: "))

BLUE = (62,74,137)
BLACK = (0,0,0)
GREY = (225,225,225)
RED = (239,83,80)
rows=3
columns=3
SIZE = 100


def draw_board(board):
		pygame.draw.rect(screen, BLACK, (0, 0, 100*columns, 100*rows))
		
		for c in range(columns):
			for r in range(rows):
				
				pygame.draw.rect(screen, GREY, [c*SIZE+5, r*SIZE+5, SIZE-8, SIZE-8])
		
		for c in range(columns):
			for r in range(rows):		
				if board[r][c] == 1:
					pygame.draw.rect(screen, BLUE, (c*SIZE+5, r*SIZE+5, SIZE-8, SIZE-8))
				elif board[r][c] == 2: 
					pygame.draw.rect(screen, RED, (c*SIZE+5, r*SIZE+5, SIZE-8, SIZE-8))
		pygame.draw.rect(screen, RED, (0, 0, 100*columns, 5))
		pygame.draw.rect(screen, RED, (0, 100*rows-5, 100*columns, 100*rows))
		pygame.draw.rect(screen, BLUE, (0, 5, 5, 100*rows))
		pygame.draw.rect(screen, BLUE, (100*columns-5, 0, 100*columns, 100*rows-5))

		pygame.display.update()

board = Board(rows,columns)
board.get_formatted_board()
game_over = False
##############
pygame.init()
width = columns * SIZE
height = rows * SIZE
size = (width, height)
screen = pygame.display.set_mode(size)
draw_board(board.board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
##############

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:	
			if board.get_turn()==1:
				posx= event.pos[0]
				print(posx)
				col = int(posx/SIZE)
				print(col)
				posy = event.pos[1]
				print(posy)
				row = int(posy/SIZE)
				print(row)
				#row = int(input("Player 1, row: "))
				#col = int(input("Player 1, col: "))
				valid = board.is_valid_location(row, col)
				while not valid:
				#	print("Please enter a valid location")
				#	row = int(input("Player 1, row: "))
				#	col = int(input("Player 1, col: "))
					valid = board.is_valid_location(row, col)
				board.drop_piece(row, col, 1)
				if board.get_winner():
					game_over = True
			
			elif board.get_turn()==2:
				posx= event.pos[0]
				col = int(posx/SIZE)
				print(col)
				posy = event.pos[1]
				row = int(posy/SIZE)
				print(row)
				#row = int(input("Player 2, row: "))
				#col = int(input("Player 2, col: "))
				valid = board.is_valid_location(row, col)
				while not valid:
					print("Please enter a valid location")
				#	row = int(input("Player 2, row: "))
				#	col = int(input("Player 2, col: "))
					valid = board.is_valid_location(row, col)
				board.drop_piece(row, col, 2)
				if board.get_winner():
					game_over = True
	
			board.get_formatted_board()	
			draw_board(board.board)
			board.turn += 1

			if game_over:
				pygame.time.wait(3000)
	



