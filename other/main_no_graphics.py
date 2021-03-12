from module1 import *
import pygame
import sys
import math
s = int(input("Introduce size: "))
rows=s
columns=s

board = Board(rows,columns)
board.get_formatted_board()
game_over = False


while not game_over:
	if board.get_turn()==1:		
		row = int(input("Player 1, row: "))
		col = int(input("Player 1, col: "))
		valid = board.is_valid_location(row, col)
		while not valid:
			print("Please enter a valid location")
			row = int(input("Player 1, row: "))
			col = int(input("Player 1, col: "))
			valid = board.is_valid_location(row, col)
		board.drop_piece(row, col, 1)
		if board.get_winner():
			game_over = True
			
	elif board.get_turn()==2:				
		row = int(input("Player 2, row: "))
		col = int(input("Player 2, col: "))
		
		while not valid:
			print("Please enter a valid location")
			row = int(input("Player 2, row: "))
			col = int(input("Player 2, col: "))
			valid = board.is_valid_location(row, col)
		board.drop_piece(row, col, 2)
		if board.get_winner():
			game_over = True
	
	board.get_formatted_board()		
	board.turn += 1

			



