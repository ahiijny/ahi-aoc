from collections import deque
from operator import add, sub

from enum import IntEnum

WIDTH = 7

class MyIntEnum(IntEnum):
	"""Same as IntEnum but with an additional convenience casting folder function"""
	@classmethod
	def from_repr(cls, obj):
		# obj is an enum
		if isinstance(type(obj), cls):
			return obj
		
		# obj is an enum value
		try:
			return cls(int(obj))
		except ValueError:
			pass

		# obj is a string representation of the enum name

		for item in dir(cls):
			value = getattr(cls, item)
			if item == obj and isinstance(value, cls):
				return value
		
		raise ValueError(f"{obj} could not be cast to {cls.__name__}")
		
class MoveType(MyIntEnum):
	UP = -1
	LEFT = 0
	DOWN = 1
	RIGHT = 2

class PieceType(MyIntEnum):
	M = 1
	P = 2
	J = 3
	I = 4
	O = 5

class BlockType(MyIntEnum):
	EMPTY = 0
	M = 1
	P = 2
	J = 3
	I = 4
	O = 5
	X = 6

	@classmethod
	def from_repr(cls, obj):
		try:
			return super().from_repr(obj)
		except ValueError:
			if obj == "`" or obj == " ": # more convenient ways of representing "empty"
				return BlockType.EMPTY
		raise ValueError(f"{obj} could not be cast to {cls.__name__}")

class BlockOffsets:
	"""Offsets are (row, col), with rows increasing left to right and cols increasing bottom to top."""
	OFFSETS = [
		[], # EMPTY
		[(0, 0), (1, 0), (2, 0), (3, 0)], # -
		[(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)], # +
		[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], # J
		[(0, 0), (0, 1), (0, 2), (0, 3)], # I
		[(0, 0), (1, 0), (0, 1), (1, 1)] # O
	]
	
	@staticmethod
	def of(piece_type):
		"""Return a copy of the block offsets corresponding to the given piece type"""
		assert int(piece_type) < len(BlockOffsets.OFFSETS)
		return list(BlockOffsets.OFFSETS[piece_type])
	
class MoveType(MyIntEnum):
	UP = -1
	LEFT = 0
	DOWN = 1
	RIGHT = 2

class Piece:
	def __init__(self, name, x=-1, y=-1, blocks=None):
		self.name = PieceType.from_repr(name)
		self.x = x
		self.y = y
		if blocks is None:
			self.blocks = BlockOffsets.of(self.name)
		else:
			self.blocks = blocks
		
	def clone(self):
		return Piece(name=self.name, x=self.x, y=self.y, blocks=list(self.blocks))
		
	def copy_state_from(self, other):
		self.x = other.x
		self.y = other.y
		self.blocks = list(other.blocks) # tuples are immutable, so don't need a deep copy
				
	def try_move(self, direction, grid):
		"""Direction should be a MoveType enum.
		Return True if move succeeded, False otherwise"""
		attempt = self.clone()
		direction = MoveType.from_repr(direction)
		if direction == MoveType.UP:
			attempt.y += 1
		elif direction == MoveType.LEFT:
			attempt.x -= 1
		elif direction == MoveType.DOWN:
			attempt.y -= 1
		elif direction == MoveType.RIGHT:
			attempt.x += 1
		if grid.can_place(attempt):
			self.copy_state_from(attempt)
			return True
		return False
		
class Field:
	def __init__(self, width=7, height=0):
		self.width = width
		self.height = height
		self.active_piece = None
		self.grid = [[BlockType.EMPTY for x in range(width)] for y in range(height)]
			# grid[y][x], 0-indexed, increasing bottom to top, left to right
			# putting y first because it makes it easier to print things
		self.extend_up()
		self.placements = []
			
	def extend_up(self):
		desired_y = self.stack_height() + 10
		delta = desired_y - self.height
		if delta > 0:
			self.height = desired_y
			for i in range(delta):
				self.grid.append([BlockType.EMPTY for x in range(self.width)])
			
	def stack_height(self):
		"""Return the y coordinate of the highest row that contains some block.
		Returns 0 if playfield is completely empty.
		Ignores the active piece.
		"""
		y = self.height - 1
		while y >= 0:
			for x in range(self.width):
				if self.grid[y][x] != BlockType.EMPTY:
					return y + 1
			y -= 1
		return y + 1
		
	def can_place(self, piece):
		for block in piece.blocks:
			(x, y) = (piece.x + block[0], piece.y + block[1])
			if x < 0 or x >= self.width or y < 0 or y >= self.height:
				return False
			if self.grid[y][x] != BlockType.EMPTY:
				return False
		return True
				
	def is_piece_on_floor(self):
		"""Return True if piece cannot fall any farther"""
		if self.active_piece is None:
			return False
		test = self.active_piece.clone()
		test.y -= 1
		return not self.can_place(test)
	
	def get_spawn_loc(self):
		return (2, self.stack_height() + 3)
		
	def spawn(self, piece):
		"""piece can be a Piece or PieceType"""
		if not isinstance(piece, Piece):
			piece_type = piece
			piece = Piece(piece_type)
		x, y = self.get_spawn_loc()
		
		self.active_piece = piece
		self.active_piece.x = x
		self.active_piece.y = y
	
	def lock(self):
		"""Cement the blocks belonging to the active piece into the playfield,
		but only if the active piece isn't currently overlapping with any existing blocks.
		"""
		if self.active_piece is None:
			return False

		piece = self.active_piece
		if self.can_place(piece):
			self.placements.append((piece.name.name, piece.x, piece.y))
			block_type = BlockType.X #BlockType(piece.name)

			for block in piece.blocks:
				self.grid[piece.y + block[1]][piece.x + block[0]] = block_type

			return True
		return False
	
	def calc_contour(self):
		y_top = self.stack_height()
		
		
	def __str__(self):
		shown_grid = [] # note: y and x are transposed, and y indicies are reversed, for easier printing
		for row in range(self.height):
			shown_grid.append([" " for col in range(self.width)])

		for y in range(self.height):
			for x in range(self.width):
				name = self.grid[y][x].name
				if name == "EMPTY":
					name = "`"
				elif name == "X":
					name = '#'
				shown_grid[self.height - 1 - y][x] = name

		if self.active_piece is not None:
			x = self.active_piece.x
			y = self.active_piece.y
			for (dx, dy) in self.active_piece.blocks:
				bx = x + dx # block x
				by = y + dy # block y
				if 0 <= bx and bx < self.width and 0 <= by and by < len(shown_grid):
					shown_grid[self.height - 1 - by][bx] = self.active_piece.name.name # use letters instead of numbers for active piece

		for r in range(len(shown_grid)):
			shown_grid[r] = "".join(str(cell) for cell in shown_grid[r]) # cast to str for printing

		return "\n".join(row_str for row_str in shown_grid)

def genmoves():
	global moves
	while True:
		for c in moves:
			yield c
			
def genpieces():
	order = ['M', 'P', 'J', 'I', 'O']
	while True:
		for p in order:
			yield Piece(p)

while True:
	try:
		moves = list(input())
	except EOFError:
		break
		
		
def run():			
	pcount = 0
	grid = Field()
	
	moves = genmoves()
	
	hist = {}
	
	for p in genpieces():
		mcount = 0
		if pcount > 100000:
			break
		grid.extend_up()
		grid.spawn(p)
		if pcount % 1000 == 0:
			print(f'pcount={pcount}, stack height={grid.stack_height()}')
		while True:
			mcount += 1
			move = next(moves)
			if move == '>':
				p.try_move(MoveType.RIGHT, grid)
			elif move == '<':
				p.try_move(MoveType.LEFT, grid)
			else:
				raise ValueError(f'unrecognized move: {move}')
			success = p.try_move(MoveType.DOWN, grid)
			if not success:
				grid.lock()
				pcount += 1
				if mcount not in hist:
					hist[mcount] = 1
				else:
					hist[mcount] += 1
				break
	print(f"{str(grid)}")
	print(grid.placements)
	print(f"mcounts: {hist}")
	
	check_cycles(grid)
	
def check_cycles(grid):
	n = 100
	while n < len(grid.placements)/2:
		valid = True
		if n % 1000 == 0:
			print(f"checking cycle of length={n}:")
		for i in range(n):
			model = grid.placements[i]
			if not valid:
				break
			for j in range(i+n, len(grid.placements), n):
				if grid.placements[j][0] != model[0] or grid.placements[j][1] != model[1]:
					valid = False
					break
		if valid:
			print(f"found valid cycle n={n}")
		n += 1
run()