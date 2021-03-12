import math
from random import randint
import copy
#red player is the computer (2) blue player human (1)
#returns double
#board: Board, maximizingPlayer: Bool, depth: Int, alpha: Double, beta: Double
#alphaBetaPrunedMiniMax(board,True,board.size,-math.inf,math.inf)
def is_board_full(board):
        res=True
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c]==0:
                    res=False
        return res
    
def get_possible_moves(board):
    moves=[]
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c]==0:
                moves.append([r,c])
    return moves

def drop_piece(board, row, col, player_id):
    board[row][col] = player_id


def alphaBetaPrunedMiniMax(board, maximizingPlayer, depth, alpha, beta):
    if depth == 0 or is_board_full(board):
        graph=Graph(board)          
        score=get_heuristic_score(graph)
        return None,None,score      
    moves = get_possible_moves(board)
    if moves!=[]:
        if maximizingPlayer:
            best_value=-math.inf
            aux_move=moves[randint(0,len(moves)-1)]
            for move in moves:

                print("Max moves: ",moves)
                board_copy=copy.deepcopy(board)
                drop_piece(board_copy,move[0], move[1], 2)
                print("Maximising")
                print("board copy\n",board_copy)

                aux_r,aux_c,new_score = alphaBetaPrunedMiniMax(board_copy,False,depth-1,alpha,beta)

                print("Max:new_score:",new_score)
                if new_score>best_value:
                    print("new score is better:", new_score)
                    best_value = new_score
                    aux_move=move
                alpha = max(alpha, best_value)
                if beta <= alpha: 
                    break                  
            return aux_move[0],aux_move[1],best_value
        else:
            best_value = math.inf
            aux_move=moves[randint(0,len(moves)-1)]
            for move in moves:
                print("Min moves: ", moves)
                board_copy=copy.deepcopy(board)
                drop_piece(board_copy,move[0], move[1], 1)
                print("Minimising")
                print(board_copy)
                print("copy board:\n", board_copy)
                aux_r,aux_c,new_score=alphaBetaPrunedMiniMax(board_copy,True,depth-1,alpha,beta)

                if new_score<best_value:
                    best_value = new_score
                    aux_move = move
                beta = min(beta, best_value)
                if beta<=alpha:
                    break                         
            return aux_move[0],aux_move[1],best_value

def get_heuristic_score(graph):
      computerPath=getComputerShortestPath(graph)
      playerPath=getPlayerShortestPath(graph)
      computerScore=getScoreForPath(computerPath,2)#1=computer
      print("computer score: ",computerScore)
      playerScore=getScoreForPath(playerPath,1)
      print("player score: ", playerScore)
      res=playerScore-computerScore
      return res
    
def getComputerShortestPath(graph):
    down_hex = graph.get_side_hexagon("D")
    top_hex = graph.get_side_hexagon("T")
    print("perspective:",down_hex.perspective)
    return graph.getShortestPathFrom(down_hex, top_hex, 2) 

def getPlayerShortestPath(graph):
    left_hex = graph.get_side_hexagon("L")
    right_hex = graph.get_side_hexagon("R")
    print("perspective:",left_hex.perspective)
    return graph.getShortestPathFrom(left_hex, right_hex, 1)        

def getScoreForPath(path,perspective):
    res = 0.0
    if path.distance == 0.0:
        res=-math.inf #Game over
    else:

        for h in path.pathHexagons:
            if h.perspective==0:#gray tiles
                res=res+1
    return res
     
class Hexagon():
    def __init__(self,row,column,perspective,outside):
        self.row=row
        self.column=column 
        self.name="" 
        self.perspective=perspective#grey    
        self.outside=outside  
        self.pathLengthFromStart = math.inf
        hexagons=[]
        self.pathVerticesFromStart = hexagons
  
    def get_name(self):

        if self.name!="":
            return self.name
        else:
            return str(self.row)+str(self.column)

    def clearVertexCache(self):
        self.pathLengthFromStart = math.inf
        self.pathVerticesFromStart = []


class Graph():     
    def __init__(self,board):
        self.board=board
        vertices=[]
        for r in range(len(board)):
            for c in range(len(board)):
                hexagon= Hexagon(r,c,board[r][c],False)
                vertices.append(hexagon)
        hexagon_D = Hexagon(len(board),0,2,True)
        hexagon_D.name="D"
        vertices.append(hexagon_D)
        hexagon_T = Hexagon(-1,0,2,True)
        hexagon_T.name="T"
        vertices.append(hexagon_T)
        hexagon_L = Hexagon(0,-1,1,True)
        hexagon_L.name="L"
        vertices.append(hexagon_L)
        hexagon_R = Hexagon(0,len(board),1,True)
        hexagon_R.name="R"
        vertices.append(hexagon_R)
        self.vertices=vertices#actual state of the COPY of the board

    def get_neighbors(self,vertex):
        neighbors = []
        if vertex.name=="L":  # L
            for v in self.vertices:
                if v.column==0:
                    neighbors.append(v)
        if vertex.name=="R":  # R
            for v in self.vertices:
                if v.column == len(self.board)-1:
                    neighbors.append(v)
        if vertex.name=="T":  # T
            for v in self.vertices:
                if v.row == 0:
                    neighbors.append(v)
        if vertex.name=="D":  # D
            for v in self.vertices:
                if v.row == len(self.board)-1:
                    neighbors.append(v)
        else:
            actual_coords = [vertex.row, vertex.column]
            row = vertex.row
            column = vertex.column
            top_left = [[0, 1], [1, 0], [0, -1], [-1, 0]]
            top_right = [[0, -1], [1, -1], [1, 0], [-1, 0], [0, 1]]
            bottom_left = [[-1, 0], [-1, 1], [0, 1], [0, -1], [1, 0]]
            bottom_right = [[-1, 0], [0, -1], [1, 0], [0, 1]]
            left = [[-1, 0], [-1, 1], [0, 1], [1, 0], [0, -1]]
            top = [[0, -1], [1, -1], [1, 0], [0, 1], [-1, 0]]
            right = [[-1, 0], [0, -1], [1, -1], [1, 0], [0, 1]]
            bottom = [[0, -1], [-1, 0], [-1, 1], [0, 1], [1, 0]]
            middle = [[-1, 0], [-1, 1], [0, 1], [1, 0], [1, -1], [0, -1]]
            coordinates = []

            if row == 0 and column == 0:
                coordinates = top_left
            elif row == 0 and column == len(self.board) - 1:
                coordinates = top_right
            elif row == len(self.board) - 1 and column == 0:
                coordinates = bottom_left
            elif row == len(self.board) - 1 and column == len(self.board) - 1:
                coordinates = bottom_right
            elif 0 < row < len(self.board) - 1 and column == 0:
                coordinates = left
            elif row == 0 and 0 < column < len(self.board) - 1:
                coordinates = top
            elif 0 < row < len(self.board) - 1 and column == len(self.board) - 1:
                coordinates = right
            elif row == len(self.board) - 1 and 0 < column < len(self.board) - 1:
                coordinates = bottom
            elif 0 < row < len(self.board) - 1 and 0 < column < len(self.board) - 1:
                coordinates = middle
            neighbor_coordinates=[]
            for c in coordinates:
                neighbor_coordinate = list(i + j for (i, j) in zip(actual_coords, c))
                neighbor_coordinates.append(neighbor_coordinate)
            for v in self.vertices:
                if v.name == "D":
                    for nc in neighbor_coordinates:
                        if nc[0] == len(self.board):
                            neighbors.append(v)
                elif v.name == "T":
                    for nc in neighbor_coordinates:
                        if nc[0] < 0:
                            neighbors.append(v)
                elif v.name == "L":
                    for nc in neighbor_coordinates:
                        if nc[1] < 0:
                            neighbors.append(v)
                elif v.name == "R":
                    for nc in neighbor_coordinates:
                        if nc[1] == len(self.board):
                            neighbors.append(v)
                else:
                    if[v.row,v.column] in neighbor_coordinates:
                        neighbors.append(v)
        return neighbors

    def get_side_hexagon(self,letter):
        for v in self.vertices:
            if v.name==letter:
                return v
    def print_vertices(self,vertices):
        res=""
        for v in vertices:
            res=res+v.get_name()+","
        return res
    def getShortestPathFrom(self,from_hex,to_hex,perspective):
        starting_vertex=from_hex
        if from_hex.perspective==perspective:#if the side of the board corresponds to the player
            for v in self.vertices:
                v.clearVertexCache()
            self.findShortestPathsUsingDijkstra(starting_vertex,perspective)
            print("vertices of shortest path:",self.print_vertices(to_hex.pathVerticesFromStart))
            print(to_hex.pathLengthFromStart)
            print("#####################################################################################")
            p = Path(starting_vertex.name,to_hex.name,to_hex.pathVerticesFromStart,to_hex.pathLengthFromStart)
        return p

    def getMinimumLengthVertex(self, vertices):
        if len(vertices) == 1:
            return vertices[0]
        elif len(vertices)>1:
            minimum = vertices[0]
            for i in range(1, len(vertices)):
                if vertices[i].pathLengthFromStart < vertices[i-1].pathLengthFromStart:
                    minimum = vertices[i]
            return minimum

    def findShortestPathsUsingDijkstra(self,start_vertex, perspective):
        print("#######################################dijkstra:#########################################")

        start_vertex.pathLengthFromStart=0
        start_vertex.pathVerticesFromStart.append(start_vertex)
        print("start_vertex:",start_vertex.column,start_vertex.row,start_vertex.name)
        current_vertex=start_vertex
        current_vertices=self.vertices
        visited_vertices = []
        while current_vertices!=[]:
            visited_vertices.append(current_vertex)
            current_vertices.remove(current_vertex)

            unchecked_neighbors = []
            neighbors_aux=self.get_neighbors(current_vertex)
            for c in current_vertices:
                if c in neighbors_aux:
                    unchecked_neighbors.append(c)

            valid_neighbors = []
            for nc in unchecked_neighbors:
                if (nc.perspective == 0 or nc.perspective == perspective) and nc not in visited_vertices:
                    valid_neighbors.append(nc)

            for valid_n in valid_neighbors:
                weight=1.0
                if valid_n.perspective == perspective:
                    weight=0.0
                theoretic_new_weight = current_vertex.pathLengthFromStart + weight
                if theoretic_new_weight < valid_n.pathLengthFromStart:
                    valid_n.pathLengthFromStart = theoretic_new_weight
                    valid_n.pathVerticesFromStart = copy.deepcopy(current_vertex.pathVerticesFromStart)
                    valid_n.pathVerticesFromStart.append(valid_n)
            if len(current_vertices)>0:
                current_vertex=self.getMinimumLengthVertex(current_vertices)
        self.vertices=visited_vertices

class Path():
    def __init__(self,from_hex,to_hex,pathHexagons,distance):
        self.from_hex=from_hex
        self.to_hex=to_hex
        self.pathHexagons=pathHexagons
        self.distance=distance