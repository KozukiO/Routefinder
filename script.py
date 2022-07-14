from collections import deque
import random



# Breadth first Search Implementation of a Node or Position
class Node:
	# (x, y) represents a position or coordinates of a cell in the matrix
	# The parent Node will be used to print path in the correct order 
	def __init__(self, x, y, prev_pos=None):
		self.x = x
		self.y = y
		self.prev_pos = prev_pos

	#to string function for the coordinates of the matrix	
	def __repr__(self):
		return str((self.x, self.y))

	#is equal function to check whether two point are the same
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y


# Below lists detail all Eight possible movements from a cell
# The list is traversed one by one in pairs in the implementation below
row = [0, 1,-1, 0, -1, 1, 1,-1]
col = [1, 0, 0, -1,-1,-1, 1, 1]


# The function returns false if (x, y) is not a valid position
def isValid(x, y, N):
	return (0 <= x < N) and (0 <= y < N)


# Utility function to find path from source to destination
def getRoute(node, route=[]):
	if node:
		getRoute(node.prev_pos, route)
		route.append(node)

# Utility function to set array position to 0 to indicate obstacles
def setObstacle(grid,x,y):
	grid[x][y] = 0

# Get random positions
def get_random_position(n, occupied_positions):
    rnd = random.randint(0, n*n - 1 - len(occupied_positions))
    for (row, col) in occupied_positions:
        if rnd < row*n+col:
            break
        rnd += 1
    return (rnd // n, rnd % n)

# Find the shortest route in a matrix from source cell (x, y) to
# destination cell (N-1, N-1)
def findRoute(matrix, x=0, y=0):
	# base case
	if not matrix or not len(matrix):
		return

	# 10 × 10 grid
	N = 10

	# create a queue and enqueue the first node
	q = deque()
	src = Node(x, y)
	q.append(src)

	# set to check if the matrix cell is visited before or not
	visited = set()

	key = (src.x, src.y)
	visited.add(key)

	# loop till queue is empty
	while q:

		# dequeue front node and process it
		curr = q.popleft()
		i = curr.x
		j = curr.y

		# return if the destination is found
		if i == N - 1 and j == N - 1:
			route = []
			getRoute(curr, route)
			return route

		# value of the current cell
		n = matrix[i][j]

		# check all four possible movements from the current cell
		# and recur for each valid movement
		for k in range(len(row)):
			# get next position coordinates using the value of the current cell
			x = i + row[k] 
			y = j + col[k] 

			# check if it is possible to go to the next position
			# from the current position
			if (isValid(x, y, N) and 
			matrix[x][y] == 1):
				# construct the next cell node
				next = Node(x, y, curr)
				key = (next.x, next.y)

				# if it isn't visited yet
				if key not in visited:
					# enqueue it and mark it as visited
					q.append(next)
					visited.add(key)

	# return None if the path is not possible
	return


if __name__ == '__main__':

	#Create grid of 1's where 1 indicates a valid path
	grid = [[1 for _ in range(10)] for _ in range(10)]

	#Create list of obstacles
	obstacle_list = []
	obstacle_list.append((9,7))
	obstacle_list.append((8,7))
	obstacle_list.append((6,7))
	obstacle_list.append((6,8))

	#Scan board for all open positions 
	#Add all open positions to list indices
	indices = []
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] == 1:
				indices.append((i,j))

	#Remove Start and Destination from open positions
	indices.remove((0,0))
	indices.remove((9,9))

	#Create new unique subset og obstacles from open positions
	new_obstacles = random.sample(indices,20)

	#Add new obstacles to obstacle list
	obstacle_list = new_obstacles + obstacle_list

	#Set random obstacles
	for item in obstacle_list:
			setObstacle(grid,item[0],item[1])

	#Print positons of obstacles
	print("THE POSITIONS OF THE OBSTACLES ARE:\n",obstacle_list,"\n")


	# Find a route in the matrix from source cell (0, 0) to
	# destination cell (N-1, N-1)
	path = findRoute(grid)

	#Print path
	if path:
		print('THE SHORTEST PATH IS:\n',path, "\n")
		print("Number of steps is:",len(path) - 2)
	else:
		print('Destination is not found')
