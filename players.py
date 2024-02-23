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
			# Now lets try to do a function based on the sequences
		def count_sequences(board, num):
			count = 0
			score = 0
			for i in range(board.size):
				if board[i] == num:
					count += 1
					if count == 2:
						score += 1
					elif count == 3:
						score += 10
					elif count >= 4:
						score += 1000
				else: 
					count = 0
			return score
			
		total_score = 0
		board = deepcopy(env.board)
		# Check Rows
		for row in board:
			total_score += count_sequences(row, self.position)  # Maximizing player
			total_score -= count_sequences(row, self.opponent.position)  # Minimizing player
		
		for col in range(board.shape[1]):
			total_score += count_sequences(board[:, col], self.position)
			total_score -= count_sequences(board[:, col], self.opponent.position)

		# Check diagonals
		for diag in range(-board.shape[0] + 1, board.shape[1]):
			# Upward diagonals
			total_score += count_sequences(np.diag(board, k=diag), self.position)
			total_score -= count_sequences(np.diag(board, k=diag), self.opponent.position)
			# Downward diagonals (flip the board vertically to reuse the upward diagonal checking)
			total_score += count_sequences(np.diag(np.fliplr(board), k=diag), self.position)
			total_score -= count_sequences(np.diag(np.fliplr(board), k=diag), self.opponent.position)
		#if total_score > 0:
			#print(f"For this board {board}, the evaluation is {total_score}")
		#I first make an array for the weights that I want to use
		weights_array = np.array([[3,4,5,7,5,4,3],
						   [4,6,8,10,8,6,4],
						   [5,8,11,13,11,8,5],
						   [5,8,11,13,11,8,5],
							[4,6,8,10,8,6,4],
						  	[3,4,5,7,5,4,3]])
		 #Turn all the board where it says 2 into -1
		board[board == self.opponent.position] = -1
		evaluation = np.sum(weights_array * board)
		return evaluation
				

	def play(self, env: connect4, move: list) -> None:
		self.minimax(move, env, 5, True)
	def minimax(self, move: list, env: connect4, depth, if_maximizing,):
		# First, check if max player
		if if_maximizing:
			# Check if the opponent won the game with their last move, if they did then return -infinity
			if len(env.history[self.opponent.position - 1]) != 0 and env.gameOver(env.history[self.opponent.position - 1][-1], self.opponent.position):
				return -math.inf
			# Now, if depth has been reached, we check for an evaluation
			if depth == 0:
				evaluation = self.evaluation(env)
				print(f" Max talking: The board {env.board} has been given an evaluation of {evaluation}")
				return evaluation
			# Now, we run the minimax where we go through each possible move
			# First, create a list of all possible moves
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)
			v = -math.inf
			# Now, iterate through each move
			for column in indices:
				# First we simulate each move
				env1 = deepcopy(env)
				self.simulateMove(env1, column, self.position)
				v_temp = max(v, self.minimax(move, env1, depth - 1, False))
				if v_temp > v:
					move[:] = [column]
					v = v_temp
			print("Depth reached:", depth)
		else:
			# Check if the opponent won the game with their last move, if they did then return -infinity
			if len(env.history[self.position -1 ]) != 0 and env.gameOver(env.history[self.position - 1][-1], self.position):
				return math.inf
			# Now, if depth has been reached, we check for an evaluation
			if depth == 0:
				evaluation = self.evaluation(env)
				print(f"Min talking: The board {env.board} has been given an evaluation of {evaluation}")
				return evaluation
			# Now, we run the minimax where we go through each possible move
			# First, create a list of all possible moves
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)
			v = math.inf
			# Now, iterate through each move
			for column in indices:
				# First we simulate each move
				env1 = deepcopy(env)
				self.simulateMove(env1, column, self.opponent.position)
				# Then take the min of the current v and the recursive call to max
				v = min(v, self.minimax(move, env1, depth - 1, True,))
				# If change in V, then make the v
			print("Depth reached:", depth)

		return v

			
		


	def simulateMove(self, env: connect4, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[player-1].append(move)

				

			


class alphaBetaAI(connect4Player):

	def evaluation(self, env):
		score = 0
		board = env.board
		# Score center column
		center_array = board[:, env.board.shape[1] // 2]
		center_count = np.count_nonzero(center_array == self.position)
		score += center_count * 6

		# Score Horizontal
		for row in board:
			for col in range(env.board.shape[1] - 3):
				window = row[col:col+4]
				score += self.evaluate_window(window)

		# Score Vertical
		for col in range(env.board.shape[1]):
			for row in range(env.board.shape[0] - 3):
				window = board[row:row+4, col]
				score += self.evaluate_window(window)

		# Score positive diagonal
		for row in range(env.board.shape[0]-3):
			for col in range(env.board.shape[1]-3):
				window = [board[row+i][col+i] for i in range(4)]
				score += self.evaluate_window(window)

		# Score negative diagonal
		for row in range(env.board.shape[0]-3):
			for col in range(3, env.board.shape[1]):
				window = [board[row+i][col-i] for i in range(4)]
				score += self.evaluate_window(window)

		return score


	def evaluate_window(self, window):
		score = 0
		if np.count_nonzero(window == self.position) == 4:
			score += 100
		elif np.count_nonzero(window == self.position) == 3 and np.count_nonzero(window == 0) == 1:
			score += 5
		elif np.count_nonzero(window == self.position) == 2 and np.count_nonzero(window == 0) == 2:
			score += 2
		if np.count_nonzero(window == self.opponent.position) == 3 and np.count_nonzero(window == 0) == 1:
			score -= 4

		return score

	def evaluation_1(self, env):
			# Now lets try to do a function based on the sequences
		def count_sequences(board, num):
			count = 0
			score = 0
			for i in range(board.size):
				if board[i] == num:
					count += 1
					if count == 2:
						score += 1
					elif count == 3:
						score += 10
					elif count >= 4:
						score += 1000
				else: 
					count = 0
			return score
			
		# Here I am going to implement the sliding window approach to count for sequences
		def counting_sequences(array: np.ndarray):
			length = array.size
			# Initialize the two dictionary
			player_sequences = 0
			opponents_sequences = 0
			# Create a left pointer and a right pointer
			lp = 0
			rp = 1
			# Create a while loop, as long as the right pointer is still valid
			while rp != length:
				if array[lp] == 0:
					lp = rp
					rp = lp + 1
				elif array[lp] == self.position:
					if player_sequences < 1:
						player_sequences = 1
					if array[rp] == self.opponent.position:
						if rp - lp <= 3:
							if lp >= 1:
								if array[lp - 1] == self.opponent.position:
									player_sequences = 0
						lp = rp
						rp = lp + 1
					elif array[rp] == self.position:
						player_sequences += 1
						if rp + 1 == length and array[lp-1]==self.opponent.position:
							player_sequences = 0
						rp += 1
					else:
						if rp - lp >= 3:
							lp = rp
							rp += 1
						else:
							rp += 1
				else:
					if opponents_sequences < 1:
						opponents_sequences = 1
					if array[rp] == self.position:
						if rp - lp <= 4:
							if lp >= 1:
								if array[lp - 1] == self.position:
									opponents_sequences = 0
						lp = rp
						rp = lp + 1
					elif array[rp] == self.opponent.position:
						opponents_sequences += 1
						if rp + 1 == length and array[lp-1]==self.position:
							opponents_sequences = 0
						rp += 1
					else:
						if rp - lp >= 3:
							lp = rp
							rp += 1
						else:
							rp += 1
			player_value = 10 ** player_sequences
			opponent_value = 10 ** opponents_sequences
			return player_value - opponent_value

		total_score = 0
		board = deepcopy(env.board)
		center_column_index = board.shape[1] // 2  # Calculate the center column index
		center_column_bonus = 3
		# Check Rows
		for row in board:
			total_score += counting_sequences(row)
		# Check Columns
		for col in range(board.shape[1]):
			total_score += counting_sequences(board[:, col][::-1])
		# Positive diagonal
		for d in range(-board.shape[0] + 1, board.shape[1]):
			diag = np.diag(board, k=d)
			if len(diag) >= 4:
				total_score += counting_sequences(diag)
		
    # Negative diagonals
    # Flip the board horizontally to reuse the np.diag function
		flipped_board = np.fliplr(board)
		for d in range(-board.shape[0] + 1, board.shape[1]):
			diag = np.diag(flipped_board, k=d)
			if len(diag) >= 4:
				total_score += counting_sequences(diag)

		center_column = board[:, center_column_index]
		center_count = np.count_nonzero(center_column == self.position)
		total_score += center_count * center_column_bonus

		return total_score
		# Check diagonals
		#for diag in range(-board.shape[0] + 1, board.shape[1]):
			# Upward diagonals
			#total_score += count_sequences(np.diag(board, k=diag), self.position)
			#total_score -= count_sequences(np.diag(board, k=diag), self.opponent.position)
			# Downward diagonals (flip the board vertically to reuse the upward diagonal checking)
			#total_score += count_sequences(np.diag(np.fliplr(board), k=diag), self.position)
			#total_score -= count_sequences(np.diag(np.fliplr(board), k=diag), self.opponent.position)
		#if total_score > 0:
			#print(f"For this board {board}, the evaluation is {total_score}")
		#I first make an array for the weights that I want to use
		weights_array = np.array([[3,4,5,7,5,4,3],
						   [4,6,8,10,8,6,4],
						   [5,8,11,13,11,8,5],
						   [5,8,11,13,11,8,5],
							[4,6,8,10,8,6,4],
						  	[3,4,5,7,5,4,3]])
		 #Turn all the board where it says 2 into -1
		board[board == self.opponent.position] = -1
		evaluation = np.sum(weights_array * board)
		return total_score
				

	def play(self, env: connect4, move: list) -> None:
		self.minimax(move, env, 3, True, -math.inf, math.inf)


	def minimax(self, move: list, env: connect4, depth, if_maximizing, alpha, beta):
		# First, check if max player
		if if_maximizing:
			# Check if the opponent won the game with their last move, if they did then return -infinity
			if len(env.history[self.opponent.position - 1]) != 0 and env.gameOver(env.history[self.opponent.position - 1][-1], self.opponent.position):
				#print("The min player is boutta win")
				return -math.inf
			# Now, if depth has been reached, we check for an evaluation
			if depth == 0:
				evaluation = self.evaluation_1(env)
				#print(f" Max talking: The board {env.board} has been given an evaluation of {evaluation}")
				return evaluation
			# Now, we run the minimax where we go through each possible move
			# First, create a list of all possible moves
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)
			v = -math.inf
			# Now, iterate through each move
			for column in indices:
				# First we simulate each move
				env1 = deepcopy(env)
				self.simulateMove(env1, column, self.position)
				v_temp = max(v, self.minimax(move, env1, depth - 1, False, alpha, beta))
				if v_temp > v:
					move[:] = [column]
					v = v_temp
					if v >= beta:
						return v
					alpha = max(alpha, v)
			print("Depth reached:", depth)
		else:
			# Check if the opponent won the game with their last move, if they did then return -infinity
			if len(env.history[self.position -1 ]) != 0 and env.gameOver(env.history[self.position - 1][-1], self.position):
				#print("The max player is boutta win")
				return math.inf
			# Now, if depth has been reached, we check for an evaluation
			if depth == 0:
				evaluation = self.evaluation_1(env)
				#print(f"Min talking: The board {env.board} has been given an evaluation of {evaluation}")
				return evaluation
			# Now, we run the minimax where we go through each possible move
			# First, create a list of all possible moves
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)
			v = math.inf
			# Now, iterate through each move
			for column in indices:
				# First we simulate each move
				env1 = deepcopy(env)
				self.simulateMove(env1, column, self.opponent.position)
				# Then take the min of the current v and the recursive call to max
				v = min(v, self.minimax(move, env1, depth - 1, True, alpha,beta))
				# If change in V, then make the v
				if v <= alpha:
					return v
				beta = min(beta, v)
			#print("Depth reached:", depth)

		return v

			
	def simulateMove(self, env: connect4, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[player-1].append(move)

	


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




