import random, pygame, math

# random.seed(89243598)
y_scale = 2

def smooth(x):
	return (6 * (x**5)) - (15 * (x**4)) + (10 * (x**3))
	 # + (math.sin(math.pi * 7 * x) / 30)


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
		self.points = []
		for i in range(self.height):
			row = [random.uniform(0, 1) for i in range(self.length)]
			self.points.append(row)

	def noise(self, x, y):
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




pn = perlin_noise_2d(85, 45)
pn.generate_noise()

pygame.init()
window = pygame.display.set_mode((1800, 900))

while True:

	for x in range(0, 1700, 3):
		for y in range(0, 800, 3):
			color = pn.noise(x / 20, y / 20) * 255
			for i in range(3):
				for j in range(3):
					window.set_at((x + i + 50, y + j + 50), (color, 255 - color, 255))

			pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()

