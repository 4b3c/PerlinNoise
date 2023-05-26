import random, pygame, math, time

# random.seed(89243598)
# https://www.desmos.com/calculator/fb4sly23hg
sqrt2 = math.sqrt(2)

def smooth(x):
	return (6 * (x**5)) - (15 * (x**4)) + (10 * (x**3)) + (math.sin(math.pi * 10 * x) / 30)

def get_border_indices(array):
	rows = len(array)
	columns = len(array[0])

	border_indices = []

	border_indices.extend([(0, col) for col in range(columns)])
	border_indices.extend([(rows - 1, col) for col in range(columns)])
	border_indices.extend([(row, 0) for row in range(1, rows - 1)])
	border_indices.extend([(row, columns - 1) for row in range(1, rows - 1)])

	return border_indices

#one dimension
class perlin_noise_1d():
	__slots__ = ("length", "points")

	def __init__(self, length):
		self.length = length + 1

	def generate_noise(self):
		self.points = [random.uniform(0, 1) for i in range(self.length)]

	def noise(self, x):
		whole = int(x)
		part = x - whole

		return self.points[whole] + smooth(part) * (self.points[whole + 1] - self.points[whole])

#simple two dimensions
class perlin_noise_2d():
	__slots__ = ("length", "height", "points")

	def __init__(self, length, height):
		self.length = length + 1
		self.height = height + 1

	def generate_noise(self):
		self.points = [[random.uniform(0, 1) for i in range(self.length)] for j in range(self.height)]
		for border in get_border_indices(self.points):
			if self.points[border[0]][border[1]] > 0.7: self.points[border[0]][border[1]] -= 0.3

	def noise_square(self, x, y):
		whole_x = int(x)
		whole_y = int(y)
		x_deci = x - whole_x
		y_deci = y - whole_y

		origin = self.points[whole_y][whole_x]
		end_x = self.points[whole_y][whole_x + 1]
		end_y = self.points[whole_y + 1][whole_x]
		end_xy = self.points[whole_y + 1][whole_x + 1]

		interp_x1 = origin + smooth(x_deci) * (end_x - origin)
		interp_x2 = end_y + smooth(x_deci) * (end_xy - end_y)
		interp_y = interp_x1 + smooth(y_deci) * (interp_x2 - interp_x1)

		interp_y1 = origin + smooth(y_deci) * (end_y - origin)
		interp_y2 = end_x + smooth(y_deci) * (end_xy - end_x)
		interp_x = interp_y1 + smooth(x_deci) * (interp_y2 - interp_y1)

		return (interp_x + interp_y) / 2

	def noise_triangle(self, x, y):
		whole_x = int(x)
		whole_y = int(y)
		x_deci = x - whole_x
		y_deci = y - whole_y
		tri_side = x_deci + y_deci

		origin = self.points[whole_y][whole_x]
		end_x = self.points[whole_y][whole_x + 1]
		end_y = self.points[whole_y + 1][whole_x]
		end_xy = self.points[whole_y + 1][whole_x + 1]

		if tri_side == 0:
			return origin

		elif (tri_side <= 1):
			interp_x = origin + smooth(tri_side) * (end_x - origin)
			interp_y = origin + smooth(tri_side) * (end_y - origin)

			# return interp_y + smooth(math.sqrt(2 * (x_deci**2)) / math.sqrt(2 * (tri_side**2))) * (interp_x - interp_y)
			# simply simplified confusingly
			return interp_y + smooth((sqrt2 * x_deci) / (sqrt2 * tri_side)) * (interp_x - interp_y)


		else:
			tri_side = (1 - x_deci) + (1 - y_deci)

			interp_x = end_xy + smooth(tri_side) * (end_y - end_xy)
			interp_y = end_xy + smooth(tri_side) * (end_x - end_xy)

			# return interp_y + smooth(math.sqrt(2 * (1 - x_deci)**2) / math.sqrt(2 * (tri_side**2))) * (interp_x - interp_y)
			# simply simplified confusingly
			return interp_y + smooth((sqrt2 * (1 - x_deci)) / (sqrt2 * tri_side)) * (interp_x - interp_y)



y_scale = 2

# pn = perlin_noise_1d(10)
# pn.generate_noise()

# pygame.init()
# window = pygame.display.set_mode((900, 500))

# for i in range(900):
#     y = pn.noise(i / 90) / y_scale
#     print(y)
#     window.set_at((i, 450 - (int(y * 500))), (255, 255, 255))

# pygame.display.update()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             quit()




start = time.time()
map_size = [12, 6]

pn = perlin_noise_2d(map_size[0], map_size[1])
pn.generate_noise()

resolution = 4
cell_size = 150

pygame.init()
window = pygame.display.set_mode((1800, 900))

for x in range(0, map_size[0] * cell_size, resolution):
	for y in range(0, map_size[1] * cell_size, resolution):
		tri = pn.noise_triangle(x / cell_size, y / cell_size)
		sqr = pn.noise_square(x / cell_size, y / cell_size)
		mtnx = (-abs(x-900) / (0.24 * 1800)) + 0.18
		mnty = (-abs(y-450) / (0.24 * 900)) + 0.18
		height = max(0, min(1, (((tri + sqr) / 1.5) + ((mtnx + mnty) / 2))))

		if height < 0.2:
			color = (27, 149, 224)
		elif height < 0.3:
			color = (205, 170, 109)
		elif height < 0.6:
			color = (124, 252, 0)
		elif height < 0.86:
			color = (1, 68, 33)
		elif height < 0.98:
			color = (122, 114, 113)
		else:
			color = (255, 255, 255)

		pygame.draw.rect(window, (color), (x, y, resolution, resolution))

	pygame.display.flip()

print("Elapsed time:", time.time() - start)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()

