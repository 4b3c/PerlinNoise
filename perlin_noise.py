import random, pygame, math

# random.seed(89243598)
y_scale = 2

def smooth(x):
	return (6 * (x**5.1)) - (15 * (x**4)) + (10 * (x**3)) + (math.sin(math.pi * 7 * x) / 30)

# def mountain(x)

#one dimension
class perlin_noise():
	__slots__ = ("length", "points")

	def __init__(self, length):
		self.length = length + 1

	def generate_noise(self):
		self.points = [random.uniform(0, 1) for i in range(self.length)]
		# if random.uniform(0, 1) > 0.5:

	def noise(self, x):
		whole = int(x)
		part = x - whole

		return self.points[whole] + smooth(part) * (self.points[whole + 1] - self.points[whole])

pn = perlin_noise(10)
pn.generate_noise()

pygame.init()
window = pygame.display.set_mode((900, 500))

for i in range(900):
    y = pn.noise(i / 90) / y_scale
    window.set_at((i, 450 - (int(y * 500))), (255, 255, 255))

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

