'''
	Triangular Peg Solitare Solver
	(c) Nile Livingston 2015

	This program implements a depth-first search solver
	for peg solitaire on a triangular 15-peg board.
	The user can input the starting state of the board
	(i.e. which peg is missing) and the appropriate solution
	will be printed out.

'''

import random

# For printing debugging messages.
debug = False

# This data structure encodes all possible moves.
# Specifically, jumps[i] = [... , (j, k)  , ....]
# means there is a legal jump from peg i to peg j over peg k.
jumps = range(0, 16)
jumps[0] = None
jumps[1] = [(4, 2), (6, 3)]
jumps[2] = [(7, 4), (9, 5)]
jumps[3] = [(8, 5), (10, 6)]
jumps[4] = [(1, 2), (6, 5), (11, 7), (13, 8)]
jumps[5] = [(12, 8), (14, 9)]
jumps[6] = [(1, 3), (4, 5), (13, 9), (15, 10)]
jumps[7] = [(9, 8), (2, 4)]
jumps[8] = [(10, 9), (3, 5)]
jumps[9] = [(7, 8), (2, 5)]
jumps[10] = [(8, 9), (3, 6)]
jumps[11] = [(4, 7), (13, 12)]
jumps[12] = [(5, 8), (14, 13)]
jumps[13] = [(4, 8), (6, 9), (11, 12), (15, 14)]
jumps[14] = [(5, 9), (12, 13)]
jumps[15] = [(6, 10), (13, 14)]

class Pegboard:

	def __init__(self, peg_list):

		# Which holes have pegs in them.
		# Zero index is null, so that we can index things starting at 1.
		self.pegs = peg_list

	# Returns True iff the board is solved, i.e. only 1 peg remains.
	def isSolved(self):
		return sum(self.pegs[1:]) == 1

	# Return a list of all the legal moves for this game state, each of which is encoded as
	# a 3-tuple: (from peg, to peg, over peg)
	def getMoves(self):
		legal_moves = []
		for i in range(1, 16):
			if self.pegs[i] == 1:
				for (to_peg, over_peg) in jumps[i]:
					if self.pegs[to_peg] == 0 and self.pegs[over_peg] == 1:
						legal_moves.append((i, to_peg, over_peg))
		return legal_moves

	# Return the game state (i.e. Pegboard object) that would result from executing the move
	# (from_peg, to_peg, over_peg)
	def movePeg(self, from_peg, to_peg, over_peg):
		new_pegboard = Pegboard(list(self.pegs))
		new_pegboard.pegs[from_peg] = 0
		new_pegboard.pegs[to_peg] = 1
		new_pegboard.pegs[over_peg] = 0
		return new_pegboard

	# Print out a representation of the Pegboard.
	def printIt(self):
		print "    " + str(self.pegs[1])
		print "   " + str(self.pegs[2]) + " " + str(self.pegs[3])
		print "  " +str(self.pegs[4]) + " " + str(self.pegs[5]) + " " + str(self.pegs[6])
		print " " + str(self.pegs[7]) + " " + str(self.pegs[8]) + " " + str(self.pegs[9]) + " " + str(self.pegs[10])
		print str(self.pegs[11]) + " " + str(self.pegs[12]) + " " + str(self.pegs[13]) + " " + str(self.pegs[14]) + " " + str(self.pegs[15])

# Solves the peg puzzle through a recursive depth-first search. Prints out the solution when one is found.
def solvePegboard(pegboard, moves_so_far=[]):
	if debug: 
		print "Moves so far: " + str(moves_so_far)
		print "Current pegboard: "
		pegboard.printIt()

	legal_moves = []
	while True:
		# Get the next batch of legal moves
		legal_moves.extend(pegboard.getMoves())

		if debug: 
			print "   Legal moves: " + str(legal_moves)

		# For the current batch of moves
		while legal_moves != []:
			# Take a move off the queue.
			(from_peg, to_peg, over_peg) = legal_moves.pop(0)

			# Get the new Pegboard that would result from applying this move.
			new_pegboard = pegboard.movePeg(from_peg, to_peg, over_peg)

			# Check to see if we've solved it.
			if new_pegboard.isSolved():
				moves_so_far.append((from_peg, to_peg))

				print "Solution:"

				# Print the solution and exit.
				for (f, t) in moves_so_far:
					print "  Move peg " + str(f) + " to " + str(t)
				exit()

			# Copy the moves_so_far list and add the latest move.
			new_moves = list(moves_so_far)
			new_moves.append((from_peg, to_peg))

			# Recurse.
			solvePegboard(new_pegboard, new_moves)

		# If we're all out of moves, exit the loop.
		if legal_moves == []:
			break

# Print out a version of the pegboard demonstrating the peg indices.
print "     " + "1"
print "    " + "2 " + "3"
print "   " + "4 " + "5 " + "6"
print "  " + "7 " + "8 " + "9 " + "10"
print "11 " + "12 " + "13 " + "14 " + "15"

# Prompt the user for the starting state.
print "Welcome to the Peg Solitaire Solver. Start the puzzle with which peg missing? (1-15)"
while True:
	missing = raw_input()
	try:	
		missing = int(missing)
		if missing < 1 or missing > 15:
			print "Invalid peg index: pick an integer between 1 and 15"
		else: break
	except(ValueError):
		print "Invalid peg index: pick an integer between 1 and 15"

# Initialize the Pegboard object and run the solver.	
peg_list = [None, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
peg_list[missing] = 0
the_pegboard = Pegboard(peg_list)
solvePegboard(the_pegboard)