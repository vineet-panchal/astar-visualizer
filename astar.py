import pygame
from queue import PriorityQueue
# importing libraries

WIDTH = 1000 # set width
DISPLAY = pygame.display.set_mode((WIDTH, WIDTH)) # set window to be width * width
pygame.display.set_caption("A Star Pathfinding Algorithm") # set title of window

DARKPURPLE = (74, 20, 30) # grid color
GREY = (207,207,205) # start and end Cells
YELLOW = (255, 158, 0) # final path
LIGHTPURPLE = (156, 47, 67) # Cells already visited
DARKYELLOW = (232, 171, 72) # Cells to be visited
BLACK = (0, 0, 0) # borders and out of bounds
DARKGREY = (87, 91, 97) # border for each cell
# define colors

class Cells: # class of cells in the grid
	def __init__(self, row, col, width, total_rows): # main constructor
		self.row = row
		self.col = col
		self.x = row * width # x coordinate
		self.y = col * width # y coordinate
		self.color = DARKPURPLE # start color, all cells are dark purple
		self.neighbors = [] # list of neighbors of a cell
		self.width = width 
		self.total_rows = total_rows

	def getPOS(self): # get position of a cell
		return self.row, self.col # POS = row, col

	def visited(self): # is cell visited? No: color = light purple
		return self.color == LIGHTPURPLE

	def notvisited(self): # is cell visited? Yes: color = dark yellow
		return self.color == DARKYELLOW

	def obstacle(self): # is the cell an obstacle? Yes: color = black
		return self.color == BLACK

	def start(self): # start cell: color = grey
		return self.color == GREY

	def end(self): # end cell: color = grey
		return self.color == GREY

	def reset(self): # reset function: color = dark purple
		self.color = DARKPURPLE

	def makeVisited(self): # create visited cell
		self.color = LIGHTPURPLE

	def makeNotVisited(self): # create not visited cell
		self.color = DARKYELLOW

	def makeObstacle(self): # create obstacle cell
		self.color = BLACK

	def makeStart(self): # create start cell
		self.color = GREY

	def makeEnd(self): # create end cell
		self.color = GREY

	def finalPath(self): # create final path
		self.color = YELLOW

	def drawingCell(self, win): # draw grid function
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width)) # take display, color, and dimensions

	def checkNeighbors(self, grid): # update the neighbors function
		self.neighbors = [] # empty list of neighbors
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].obstacle(): # checking cell below, if it is an obstacle or not
			self.neighbors.append(grid[self.row + 1][self.col]) # if it is not an obstacle, add to the neighbors list

		if self.row > 0 and not grid[self.row - 1][self.col].obstacle(): # checking cell above, if it is an obstacle or not
			self.neighbors.append(grid[self.row - 1][self.col]) # if it is not an obstacle, add to the neighbors list

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].obstacle(): # checking cell to the right, if it is an obstacle or not
			self.neighbors.append(grid[self.row][self.col + 1]) # if it is not an obstacle, add to the neighbors list

		if self.col > 0 and not grid[self.row][self.col - 1].obstacle(): # checking cell to the left, if it is an obstacle or not
			self.neighbors.append(grid[self.row][self.col - 1]) # if it is not an obstacle, add to the neighbors list

	def __lt__(self, other): # comparing two cells
		return False

def manDist(point1, point2):
# function to find the shortest manhattan distance between two points
	x1, y1 = point1 # point 1
	x2, y2 = point2 # point 2
	return abs(x1 - x2) + abs(y1 - y2) # manhattan distance function

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.finalPath()
		draw()

def algorithm(draw, grid, start, end):# function to implement the a star algorithm
	count = 0 # initialize count for which node is put in the queue and when
	open_set = PriorityQueue() # initializing a priority queue
	open_set.put((0, count, start)) # add the start node into the queue (score, the count number, actual node object)
	came_from = {} # keeping track of what node did the previous node come from
	g_score = {cell: float("inf") for row in grid for cell in row} # table for all of the g scores, a key for every cell, initially set as infinity
	g_score[start] = 0 # set initial g score to 0 for start node
	f_score = {cell: float("inf") for row in grid for cell in row} # table for all of the f scores, a key for every cell, initially set as infinity
	f_score[start] = manDist(start.getPOS(), end.getPOS()) # set f score as the manhattan distance between start and end nodes
	open_set_hash = {start}

	while not open_set.empty(): # loop while set isn't empty
		for event in pygame.event.get(): # get every event that happened so far
			if event.type == pygame.QUIT: # if x button is pressed
				pygame.quit() # quit pygame

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.makeEnd()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + manDist(neighbor.getPOS(), end.getPOS())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.makeNotVisited()
		draw()

		if current != start:
			current.makeVisited()
	return False

def createGrid(rows, width): # function to create the grid
	grid = [] # create empty grid
	cellSize = width // rows # size of a cell, how many rows fit into the width
	for i in range(rows): # loop through rows
		grid.append([]) # add a empty list for every row
		for j in range(rows): # loop through columns
			cell = Cells(i, j, cellSize, rows) # create object
			grid[i].append(cell) # add cell through position on grid
	return grid


def drawGrid(win, rows, width): # function to draw the grid
	cellSize = width // rows # size of a cell, how many rows fit into the width
	for i in range(rows): # loop through rows
		pygame.draw.line(win, DARKGREY, (0, i * cellSize), (width, i * cellSize)) # draw the lines to seperate the rows
		for j in range(rows): # loop through columns
			pygame.draw.line(win, DARKGREY, (j * cellSize, 0), (j * cellSize, width)) # draw the lines to seperate the columns

def drawCell(win, grid, rows, width):
	win.fill(DARKPURPLE)
	for row in grid:
		for cell in row:
			cell.drawingCell(win)
	drawGrid(win, rows, width) # draw the grid
	pygame.display.update() # update pygame display


def getPOS(pos, rows, width):
# function to get position of the mouse when clicked on the grid
	cellSize = width // rows # size of a cell, how many rows fit into the width
	y, x = pos # get x and y coordinates

	row = y // cellSize # get row where it is clicked
	col = x // cellSize # get column where it is clicked

	return row, col # return position

def main(win, width): # main function
	running = True;
	# clock = pygame.time.Clock()

	rows = 100 # initializing number of rows on the grid
	grid = createGrid(rows, width) # create grid

	start = None
	end = None
	# initialize start and end

	while running: # main while loop
		drawCell(win, grid, rows, width)
		for event in pygame.event.get(): # check all the events that have happened so far
			if event.type == pygame.QUIT: # if the x button is clicked
				running = False # stop running
			if pygame.mouse.get_pressed()[0]: # if left mouse was clicked
				pos = pygame.mouse.get_pos() # get position of mouse on screen
				row, col = getPOS(pos, rows, width) # get position of mouse on the grid
				cell = grid[row][col] # access the cell clicked 
				if not start and cell != end: # if start pos hasn't been placed yet
				# check if start and end are the same cell clicked
					start = cell # assign start to cell accessed
					start.makeStart() # create start cell
				elif not end and cell != start: # else if end pos hasn't been placed yet 
				# check if start and end are the same cell clicked
					end = cell # assign end to cell accessed
					end.makeEnd() # create end cell
				elif cell != end and cell != start: # else if obstacles haven't been placed yet
				# check if obstacles and start or end are the same cell clicked
					cell.makeObstacle() # create obstacle
			elif pygame.mouse.get_pressed()[2]: # else if right mouse was clicked
				pos = pygame.mouse.get_pos() # get position of mouse on screen
				row, col = getPOS(pos, rows, width) # get position of mouse on the grid
				cell = grid[row][col] # get cell accessed
				cell.reset() # reset the cell
				if cell == start: # if start is clicked
					start = None # reset start var
				elif cell == end: # else if end is clicked
					end = None # reset end var
			if event.type == pygame.KEYDOWN: # if a key is pressed
				if event.key == pygame.K_SPACE and start and end: # if the space bar is clicked
					for row in grid: # for every row in the grid
						for cell in row: # for every cell in a row
							cell.checkNeighbors(grid) # check if it is neighbor or not
					algorithm(lambda: drawCell(win, grid, rows, width), grid, start, end) # run the algorithm, call drawCell function directly using lambda
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = createGrid(rows, width)

	pygame.quit() # quit the application after main loop

if __name__ == "__main__": # main method
    main(DISPLAY, WIDTH)