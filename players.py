import random
import time
import pygame
import math
from connect4 import connect4
import numpy as np
from copy import deepcopy
class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move: list) -> None:
		move = [-1]

class human(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):

	def evaluation(self, env):
		# I first make an array for the weights that I want to use
		weights_array = np.array([[3,4,5,7,5,4,3],
						   [4,6,8,10,8,6,4],
						   [5,8,11,13,11,8,5],
						   [5,8,11,13,11,8,5],
						   [4,6,8,10,8,6,4],
						   [3,4,5,7,5,4,3]])
		# Turn all the board where it says 2 into -1
		board = deepcopy(env.board)
		board[board == 2] = -1
		evaluation = np.sum(weights_array * board)
		return evaluation
				

	def play(self, env: connect4, move: list) -> None:
		def minimax(env, depth, maximizing):
			env = deepcopy(env)
			env.visualize = False
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)
			#print("This is the indices -MM", indices)
			if maximizing:
				v = -math.inf
			else:
				v = math.inf
			for moves in indices:
				#print(f"This loop has gone {moves} times")
				#print(f"This is the environment {env.topPosition[moves]}")
				#print(f"this is the board {env.board}")
				env = deepcopy(env)
				if maximizing:
					env.board[env.topPosition[moves]][moves] = 1
					env.topPosition[moves] -= 1
					#print("Right before the gameOver ", "Column = ", moves, "Top Position =", env.topPosition[moves])
					if env.gameOver(moves, 1):
						return math.inf
					if depth == 0:
						return self.evaluation(env)
					v_temp = max(v, minimax(env, depth - 1, maximizing=False))
					if v_temp > v:
						move[:] = np.array([moves])
						v = v_temp
				else:
					env.board[env.topPosition[moves]][moves] = 2
					env.topPosition[moves] -= 1
					if env.gameOver(moves, 2):
						return -math.inf
					if depth == 0:
						return self.evaluation(env)
					v_temp = min(v, minimax(env, depth - 1, maximizing=True))
					if v_temp < v :
						move[:] = np.array([moves])
						v = v_temp
			return v
					
		# Start with depth = 1
		depth = 1
		while depth < 7:
			# Run the minimax with depth 1
			minimax(env, depth, maximizing = True)
			# Keep increasing the depth until time runs out
			depth += 1



				

			


class alphaBetaAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		pass


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




