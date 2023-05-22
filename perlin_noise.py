import random, pygame, math

random.seed(89243598)
# https://www.desmos.com/calculator/fb4sly23hg

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
		# self.points = [[0.3, 1], [0, 0.5]]
		self.points = []
		for i in range(self.height):
			row = [random.uniform(0, 1) for i in range(self.length)]
			self.points.append(row)

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
		side = x_deci + y_deci

		origin = self.points[whole_y][whole_x]
		end_x = self.points[whole_y][whole_x + 1]
		end_y = self.points[whole_y + 1][whole_x]
		end_xy = self.points[whole_y + 1][whole_x + 1]

		if (side <= 1):
			interp_x = origin + smooth(side) * (end_x - origin)
			interp_y = origin + smooth(side) * (end_y - origin)

			return interp_x + (smooth(math.sqrt(2 * (y_deci**2))) / 2) * (interp_y - interp_x)

		else:
			side = (1 - x_deci) + (1 - y_deci)

			interp_x = end_y + smooth(1 - side) * (end_xy - end_y)
			interp_y = end_x + smooth(1 - side) * (end_xy - end_x)

			return interp_x + (smooth(math.sqrt(2 * (1 - y_deci**2))) / 2) * (interp_y - interp_x)




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




pn = perlin_noise_2d(4, 2)
pn.generate_noise()

print(pn.noise_triangle(0.5, 0.99))
print(pn.noise_triangle(0.5, 1.01))
print()

pygame.init()
window = pygame.display.set_mode((1800, 900))

for x in range(0, 400, 3):
	for y in range(0, 200, 3):
		try:
			color = pn.noise_triangle(x / 100, y / 100) * 255
		except:
			pass
		for i in range(3):
			for j in range(3):
				try:
					window.set_at((x + i + 50, y + j + 50), (color, color, color))
				except:
					print(x / 100, y / 100)

		pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()

