import numpy as np
alphabet="abcdefghijklmnopqrs"

class Board:
	def __init__(self,rows,columns):
		self.rows=rows
		self.columns=columns		
		self.board = np.zeros((rows,columns))
		self.turn=0

	def get_formatted_board(self):
		letters=alphabet[:self.rows]
		b={}
		b[0]=list(letters)
		print(b)
		for r in range(self.rows):
			del b[r]
			b[r+1]=list(self.board[r])
			print(b)

	def check_rule(self):
		count=0
		valid=True
		position=[]
		for r in range(self.rows):
			for c in range(self.columns):
				if self.board[r][c]>0:
					count += 1
					if count>1:
						valid = False
						break
					else:
						position=[r,c]
		if count==0:
			valid=False
		return valid,position

	def get_board(self):
		nodes=[]
		for r in range(self.rows):
			for c in range(self.columns):
				#letter=alphabet[c]
				node = Node(r,c,self.board[r][c])
				nodes[r].append(node)

	def get_turn(self):
		turn = self.turn
		return (turn%2)+1
	
	def drop_piece(self, row, col, player_id):
		#row=row-1
		#col=col-1
		self.board[row][col] = player_id

	def is_valid_location(self, row, col,rule):
		#row=row-1
		#col=col-1
		if 0<=row<self.rows and 0<=col<self.columns:
			if self.board[row][col] == 0:
				return True
			elif self.board[row][col] > 0 and rule:
				return True
			elif self.board[row][col] > 0 and rule==False:
				print("That location is occupied")
				return False			
		elif (row<0 or row>=self.rows) and 0<=col<self.columns:
			print("The given row is nonexistent")
			return False
		elif 0<=row<self.rows and (col<0 or col>=self.columns):
			print("The given column is nonexistent")
			return False

	
	
	def possible_winner(self):
			poss_win=[0]
			#blue side
			for r in range(self.rows):
				if self.board[r][0]>0 and self.board[r][0]==1:
					poss_win.insert(0,1)
					break
			#red side
			for c in range(self.columns):
				if self.board[0][c]>0 and self.board[0][c]==2:
					poss_win.insert(0,2)
					break
			if len(poss_win)>1:
				poss_win.pop()
			return poss_win
	
	def get_winner(self):
		aux=[]
		poss_win=self.possible_winner()

		if 1 in poss_win:
			for r in range(self.rows):
				if self.board[r][0] == 1:
					node = Node(r,0,1)
					visited = self.dfs(node,aux)					
					for v in visited:
						if v.column==self.columns-1:
							print("The winner is player 1")
							return 1
		if 2 in poss_win:
			for c in range(self.columns):
				if self.board[0][c] == 2:				
					node = Node(0,c,2)
					visited = self.dfs(node,aux)
					for v in visited:
						if v.row==self.rows-1:
							print("The winner is player 2")
							return 2
#			return visited
		if 0 in poss_win:
			return 0

	def dfs(self,node,visited):
		visited_names=[]
		for vnode in visited:
			visited_names.append(vnode.name)
		if node.name not in visited_names:
			visited.append(node)
			#print(node.name)
			for n in node.visited_neighbors(self.board):
				#print("neighbor:"+n.name)
				self.dfs(n,visited)
		return visited

#graph takes a board and the node where to start



class Node:
	#A node is defined by a letter which represents its row 
	#and a number that represents its column
	def __init__(self,row,column,player_id):
		self.row=row
		self.column=column
		self.name=str(self.row+1)+alphabet[self.column]
		self.player_id=player_id
	
	def visited_neighbors(self,board):
		neighbors=self.get_neighbors(board)
		visited_neighbors=[]
		for n in neighbors:
			if  self.player_id==n.player_id:
				visited_neighbors.append(n)
		return visited_neighbors

	def get_neighbors(self,board):		
		neighbors=[]
		row=self.row
		column=self.column
		actual_node=[row,column]
		top_left=[[0,1],[1,0]]
		top_right=[[0,-1],[1,-1],[1,0]]
		bottom_left=[[-1,0],[-1,1],[0,1]]
		bottom_right=[[-1,0],[0,-1]]
		left=[[-1,0],[-1,1],[0,1],[1,0]]
		top=[[0,-1],[1,-1],[1,0],[0,1]]
		right=[[-1,0],[0,-1],[1,-1],[1,0]]
		bottom=[[0,-1],[-1,0],[-1,1],[0,1]]
		middle=[[-1,0],[-1,1],[0,1],[1,0],[1,-1],[0,-1]]
		coordinates=[]
		if row==0 and column==0:#top_left
			coordinates = top_left
		elif row==0 and column==len(board)-1:#top_right
			coordinates = top_right
		elif row==len(board)-1 and column==0:#bottom_left
			coordinates = bottom_left
		elif row==len(board)-1 and column==len(board)-1:#bottom_right
			coordinates = bottom_right	
		elif 0<row<len(board)-1 and column==0:#left
			coordinates = left
		elif row==0 and 0<column<len(board)-1:#top
			coordinates = top
		elif 0<row<len(board)-1 and column==len(board)-1:#right
			coordinates = right
		elif row==len(board)-1 and 0<column<len(board)-1:#bottom
			coordinates = bottom
		elif 0<row<len(board)-1 and 0<column<len(board)-1:#middle
			coordinates = middle
		for c in coordinates:
				neighbor_coord = list(i+j for (i,j) in zip(actual_node,c))
				player_id=board[neighbor_coord[0]][neighbor_coord[1]]		
				neighbor=Node(neighbor_coord[0],neighbor_coord[1],player_id)			
				neighbors.append(neighbor)
		return neighbors

