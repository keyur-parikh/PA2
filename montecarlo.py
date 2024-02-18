import numpy as np
import random
import sys
import signal
from players import connect4Player
from connect4 import connect4
from copy import deepcopy

class monteCarloAI(connect4Player):

	def play(self, env: connect4, move: list, iterator = 10) -> None:
		random.seed(self.seed)
		# Find legal moves
		env = deepcopy(env)
		env.visualize = False
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		#print("This is the indices -MC", indices)
		#print("This is the possible -MC", possible)
		for moves in indices:
			print("This is the environment -MC", env.topPosition[moves])
		# Init fitness trackers
		vs = np.zeros(7)
		# Play until told to stop
		counter = 0
		while counter < 1000:
			first_move = random.choice(indices)
			if counter < 10:
				turnout = self.playRandomGame(deepcopy(env), first_move, True)
			else:
				turnout = self.playRandomGame(deepcopy(env), first_move, False)
			if turnout == self.position:
				vs[first_move] += 1
			elif turnout != 0:
				vs[first_move] -= 1
			if counter % 100 == 0:
				move[:] = [np.argmax(vs)]
			counter += 1
		move[:] = [np.argmax(vs)]

	def playRandomGame(self, env, first_move: int, boolean):
		switch = {1:2,2:1}
		move = first_move
		player = self.position
		self.simulateMove(env, move, player)
		if boolean:
			print("This is the Monte Carlo Move", move, player)
			print("And this is the index that would go into the function", env.topPosition[move])
		while not env.gameOver(move, player,):
			player = switch[player]
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)


			move = random.choice(indices)
			self.simulateMove(env, move, player)
		if len(env.history[0]) == 42: return 0
		return player

	def simulateMove(self, env: connect4, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)

	def signal_handler(self):
		print("SIGTERM ENCOUNTERED")
		sys.exit(0)

