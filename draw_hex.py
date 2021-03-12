import pygame
import math
from shapely.geometry import Point, Polygon
WHITE = (255,255,255)
BLUE = (62,74,137)
BLACK = (0,0,0)
GREY = (225,225,225)
RED = (239,83,80)
hex_size = 100
half=int(hex_size/2)
quarter=int(half/2)
quarter_and_half=quarter+half
h=math.floor(math.sqrt(half**2-(quarter**2)))
total_h=2*h


class Hexagon:
	def __init__(self,row,column,polygon):
		self.row=row
		self.column=column	
		self.polygon = polygon

class DrawnBoard():
	def __init__(self,size,screen):
		self.size=size
		self.screen=screen
		self.screen_height = size*total_h+10
		self.screen_width = (size*hex_size)+((size-1)*half)+10
	
	def get_points(self):
		points = []	
		p1=[5,5+self.size*h]
		p2=[p1[0]+quarter,p1[1]-h]
		p3=[p2[0]+half,p1[1]-h]
		p4=[p3[0]+quarter,p1[1]]
		p5=[p3[0],p1[1]+h]
		p6=[p2[0],p1[1]+h]
		points.append(p1) #1
		points.append(p2) #2
		points.append(p3) #3
		points.append(p4) #4
		points.append(p5) #5
		points.append(p6) #6
		return points

	def move_horizontally(self,row, column):	
		points_h=self.move_vertically(self.get_points(),row)
		for x in range(len(points_h)):		
			points_h[x][0]=points_h[x][0]+quarter_and_half*column
			points_h[x][1]=points_h[x][1]-h*column
		return points_h

	def move_vertically(self,points, index):
		for i in range(len(points)):
			points[i][0]=points[i][0]+(quarter_and_half)*index
			points[i][1]=points[i][1]+h*index
		return points

	def draw_board(self,board):
		hexagons=[]
		pygame.draw.rect(self.screen, WHITE, (0, 0, self.screen_width, self.screen_height))
		pygame.draw.rect(self.screen, RED, (0, 0, (self.screen_width/2), (self.screen_height/2)))
		pygame.draw.rect(self.screen, BLUE, (self.screen_width/2, 0, self.screen_width, (self.screen_height/2)))
		pygame.draw.rect(self.screen, RED, ((self.screen_width/2), self.screen_height/2, self.screen_width, self.screen_height))
		pygame.draw.rect(self.screen, BLUE, (0, (self.screen_height/2), self.screen_width/2, self.screen_height))
		for r in range(self.size):
			for c in range(self.size):				
				new_points=self.move_horizontally(r,c)
				polygon = Polygon(new_points)
				hexagons.append(Hexagon(r,c,polygon))
				if board[r][c] == 1:
					pygame.draw.polygon(self.screen, BLUE, new_points)
				elif board[r][c] == 2: 
					pygame.draw.polygon(self.screen, RED, new_points)
				else:
					pygame.draw.polygon(self.screen, GREY, new_points)
				pygame.draw.polygon(self.screen, BLACK, new_points,1)

				c=c+1
			r=r+1
		pygame.display.update()
		return hexagons

	def getCoordinates(self,hexagons,x,y):
		p = Point(x,y)
		for i in range(len(hexagons)):
			if hexagons[i].polygon.contains(p):
				return [hexagons[i].row,hexagons[i].column]		