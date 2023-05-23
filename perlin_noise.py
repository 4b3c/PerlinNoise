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
		# x + y gives us the length of the non hypotenuse sides of a 45 degree triangle
		tri_side = x_deci + y_deci

		# get the heights of the top left and right, then bottom left and right corners
		origin = self.points[whole_y][whole_x]
		end_x = self.points[whole_y][whole_x + 1]
		end_y = self.points[whole_y + 1][whole_x]
		end_xy = self.points[whole_y + 1][whole_x + 1]

		# if tri_side is less than 1, the point is in the top left half of the cell
		# which means we interpolate based on the top and left 1d interpolations
		# also note this is done at the length of the triangle side so that
		# when the diagonal interpolation is done it will pass through the point
		if (tri_side <= 1):
			interp_x = origin + smooth(tri_side) * (end_x - origin)
			interp_y = origin + smooth(tri_side) * (end_y - origin)

			# lastly interpolate between the two interpolated sides using a diagonal interpolation
			return interp_x + (smooth(math.sqrt(2 * (y_deci**2))) / math.sqrt(tri_side)) * (interp_y - interp_x)

		# if tri_side is greater than 1, we do the same thing but from the bottom right triangle
		# so intead of the top and left, we use the bottom and right sides, then interpolate between them as before
		else:
			tri_side = (1 - x_deci) + (1 - y_deci)

			interp_x = end_xy + smooth(1 - tri_side) * (end_y - end_xy)
			interp_y = end_xy + smooth(1 - tri_side) * (end_x - end_xy)

			return interp_y + (smooth(math.sqrt(2 * (1 - y_deci**2))) / math.sqrt(tri_side)) * (interp_x - interp_y)




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

print(pn.noise_triangle(0.49, 0.49))
print(pn.noise_triangle(0.51, 0.51))
print()

pygame.init()
window = pygame.display.set_mode((1800, 900))

for x in range(0, 400, 8):
	for y in range(0, 200, 8):
		try:
			color = pn.noise_triangle(x / 100, y / 100) * 255
		except:
			pass
		for i in range(8):
			for j in range(8):
				try:
					window.set_at((x + i + 50, y + j + 50), (color, color, color))
				except:
					print(x / 100, y / 100)

		pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()

