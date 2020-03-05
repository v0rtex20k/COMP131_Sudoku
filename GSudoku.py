# COMP131 
# 03/05/20
# Victor Arsenescu and Vladimir Porohkin

from string import ascii_uppercase as E

def letter_to_number(letter):
	assert letter.upper() <= 'I'
	return ord(letter.upper()) - ord('A') + 1

class Square(object):
	def __init__(self, value, row, col):
		self.domain = {value} if isinstance(value, int) else value
		self.row    = letter_to_number(row)
		self.col    = col
	def __str__(self):
		return '({},{},{})'.format(self.domain, self.row, self.col)
	def __eq__(self, other):
		return True if self.domain == other.domain and \
		self.row == other.row and self.col == other.col else False

def box_domain(q, knowns):
	B = set()
	right = (3 - q.col%3)%3
	left  = abs(2 - right)
	down  = (3 - q.row%3)%3
	up    = abs(2 - down)
	for s in knowns:
		if (s.col >= q.col - left) and (s.col <= q.col + right) \
		 and (s.row >= q.row - up) and (s.row <= q.row + down)  \
		 and ((s.row, s.col) != (q.row, q.col)):
		 B.update(s.domain)
	return B
def row_domain(q, knowns):
	R = set()
	[R.update(s.domain) for s in knowns if s.row == q.row]
	return R
def col_domain(q, knowns):
	C = set()
	[C.update(s.domain) for s in knowns if s.col == q.col]
	return C


def restrict_domain(q, knowns):
	B = box_domain(q, knowns)
	R = row_domain(q, knowns)
	C = col_domain(q, knowns)
	q.domain.difference_update(B)
	q.domain.difference_update(R)
	q.domain.difference_update(C)
	naked_triples(q, B, R, C)
	return q


def arc_consistency(unknowns, knowns):
	while unknowns:
		q = unknowns.pop(0)
		#print("Starting ({},{}) --> {}".format(q.row, q.col, q.domain))
		oldD = len(q.domain)
		q = restrict_domain(q, unknowns, knowns)
		newD = len(q.domain)
		if newD != oldD:
			if newD == 0:
				return False, knowns
			elif newD == 1:
				print("Figured out {}".format(q))
				knowns.append(q)
				continue
		#print("Finishing ({},{}) --> {} ***".format(q.row, q.col, q.domain))
		unknowns.append(q)
	return True, knowns

def empty(row, col, knowns):
	r = letter_to_number(row)
	return False if any((r, col) == (s.row, s.col) for s in knowns) else True
def generate_variables_and_domains(knowns): 
	unknowns = [Square({i for i in range(1,10)}, row, col) 
				for row in E[:9] for col in range(1,10)
				if empty(row, col, knowns)]
	return unknowns
def pretty_print(consistent, solution):
	if consistent:
		solution.sort(key = lambda x: (x.row, x.col))
		x = 0
		for i, square in enumerate(solution):
			print(square.domain, end = "  ")
			x += 1
			if x == 9:
				print("")
				x -= 9
if __name__ == '__main__':
	easy_puzzle = [ Square(6, 'A', 1), Square(8, 'E', 2),
	                Square(8, 'A', 3), Square(7, 'E', 8),
	                Square(7, 'A', 4), Square(5, 'F', 1),
	                Square(2, 'A', 6), Square(9, 'F', 3),
	                Square(1, 'A', 7), Square(6, 'F', 5),
	                Square(4, 'B', 1), Square(3, 'F', 7),
	                Square(1, 'B', 5), Square(1, 'F', 9),
	                Square(2, 'B', 9), Square(6, 'G', 6),
	                Square(2, 'C', 2), Square(7, 'G', 7),
	                Square(5, 'C', 3), Square(5, 'G', 8),
	                Square(4, 'C', 4), Square(2, 'H', 1), 
	                Square(7, 'D', 1), Square(9, 'H', 5),
	                Square(1, 'D', 3), Square(8, 'H', 9),
	                Square(8, 'D', 5), Square(6, 'I', 3),
	                Square(4, 'D', 7), Square(8, 'I', 4),
	                Square(5, 'D', 9), Square(5, 'I', 6),
	                Square(2, 'I', 7), Square(3, 'I', 9) ]

	evil_puzzle = [ Square(7, 'A', 2), Square(3, 'E', 3),
					Square(4, 'A', 5), Square(7, 'E', 7),
					Square(2, 'A', 6), Square(5, 'F', 1),
					Square(8, 'B', 6), Square(1, 'F', 4),
					Square(6, 'B', 7), Square(8, 'G', 1),
					Square(1, 'B', 8), Square(7, 'G', 8),
					Square(3, 'C', 1), Square(6, 'G', 9),
					Square(9, 'C', 2), Square(5, 'H', 2),
					Square(7, 'C', 9), Square(4, 'H', 3),
					Square(4, 'D', 6), Square(8, 'H', 4),
					Square(9, 'D', 9), Square(6, 'I', 4),
					Square(1, 'I', 5), Square(5, 'H', 8) ]

	unknowns = generate_variables_and_domains(evil_puzzle)
	consistent, solution = arc_consistency(unknowns, evil_puzzle)
	pretty_print(consistent, solution)






