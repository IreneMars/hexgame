from module import *
import pygame
from minimax import *
try:
	board_size=0
	board_size=int(input("Give a board size: "))
	while board_size<3 or board_size>16:
		print("That's not a valid board size.")
		board_size = int(input("Give a board size: "))
	rows=board_size
	columns=board_size
	board=Board(rows,columns)
	

	beginner = int(input("Who starts? Player[1] or computer?[2]: "))
	if beginner==2:
		board.turn += 1
	

	board.get_formatted_board()##optional

	#####################################################

	game_over=False
	while not game_over:
		rule, opponent_position = board.check_rule()
		if rule:
			print("Possible application of Pie Rule")
		if board.get_turn() == 1:			
			row = int(input("Player 1, row: "))
			col = int(input("Player 1, col: "))
			valid = board.is_valid_location(row, col,rule)
			while not valid:
				print("Please enter a valid location")
				row = int(input("Player 1, row: "))
				col = int(input("Player 1, col: "))
				valid = board.is_valid_location(row, col,rule)
			board.drop_piece(row, col, 1)
		if board.get_winner()==1:
			print("Player 1 wins!!")
			game_over = True


		elif board.get_turn()==2 and not game_over:
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
					print("Computer says: player's position is better")
				else:
					print("Computer says: my position is better")
					board.drop_piece(row, col, 2)
			else:
				board.drop_piece(row, col, 2)
			if board.get_winner()==2:
				print("Player 2 wins!!")
				game_over = True
		board.get_formatted_board()#optional
		board.turn += 1


except pygame.error:
	print("The board size can not be 0.")

	



