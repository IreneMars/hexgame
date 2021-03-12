from module import *
from draw_hex import * 
import pygame
import sys
from popup import *
from minimax import *
try:
	rows=board_size #this
	columns=board_size #and this value come from the module: popup.py 
	board=Board(rows,columns)
	if first_player=="Computer":
		board.turn += 1
	board.get_formatted_board()##optional

	pygame.init()#here begins the initialisation of pygame variables: pygame itself and its screen
	screen_height = board_size*total_h+10
	screen_width = (board_size*hex_size)+((board_size-1)*half)+10
	screen_size = (screen_width, screen_height)
	screen = pygame.display.set_mode(screen_size)

	dboard=DrawnBoard(board_size,screen)#here we create an object DrawnBoard 
	hexagons=[]
	hexagons=dboard.draw_board(board.board)
	#this method draws the board on the pygame screen, given the value of 
	#the matrix board.board
	#It returns a list of Hexagon objects. Because we are interested 
	#on knowing the coordinates of each Hexagon object later on the execution

	pygame.display.update()
	pygame.font.init()
	myfont=pygame.font.SysFont("verdana", 20)

	#####################################################
	#The most important method
	game_over=False
	while not game_over:
		rule, opponent_position = board.check_rule()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:	
				if board.get_turn()==1:#PLAYER 1
					posx= event.pos[0]
					posy = event.pos[1]
					coordinates=dboard.getCoordinates(hexagons,posx,posy) 
					#getCoordinates() takes the original list of drawn hexagons and 
					#the actual clicked position.
					#it returns the position of the original matrix we stepped into,
					#calculating on which of the hexagons we stepped into. Once we 
					#know the hexagon, the method.
					#returns [hexagon.row,hexagon.column]
					row = coordinates[0]
					col = coordinates[1]
					valid = board.is_valid_location(row, col,rule)
					while not valid:
						posx= event.pos[0]
						posy = event.pos[1]
						coordinates=dboard.getCoordinates(hexagons,posx,posy) 
						row = coordinates[0]
						col = coordinates[1]
						valid = board.is_valid_location(row, col,rule)
					board.drop_piece(row, col, 1)
					if board.get_winner()==1:
						label = myfont.render("Player 1 wins!!", False, BLACK)
						game_over = True
					board.get_formatted_board()#optional
					dboard.draw_board(board.board)									
					board.turn += 1
		
		if board.get_turn()==2 and not game_over:				
			row, col, minimax_score = alphaBetaPrunedMiniMax(board.board, True, board.rows,-math.inf,math.inf)
			if rule:
				board_copy1 = copy.deepcopy(board)
				board_copy2 = copy.deepcopy(board)
				board_copy1.drop_piece(row,col,2)
				board_copy2.drop_piece(opponent_position[0],opponent_position[1],2)
				row_alt1, col_alt1, minimax_score_alt1 = alphaBetaPrunedMiniMax(board_copy1.board, True, board.rows, -math.inf, math.inf)
				row_alt2, col_alt2, minimax_score_alt2 = alphaBetaPrunedMiniMax(board_copy2.board, True, board.rows, -math.inf, math.inf)
				if minimax_score_alt1 < minimax_score_alt2:
					board.drop_piece(opponent_position[0], opponent_position[1], 2)
					print(minimax_score_alt1)
					print(minimax_score_alt2)
					print("Player's position is better")
				else:
					print("My position is better")
					board.drop_piece(row, col, 2)
			else:
				board.drop_piece(row, col, 2)
			if board.get_winner()==2:
				label = myfont.render("Player 2 wins!!", False, BLACK)
				game_over = True
			board.get_formatted_board()#optional
			dboard.draw_board(board.board)					
			board.turn += 1
			
		if game_over:
			pygame.draw.rect(screen, WHITE, (10, 10, 150, 30))
			screen.blit(label,(10,10))
			pygame.display.update()
			pygame.time.wait(3000)

except pygame.error:
	print("The board size can not be 0.")

	



