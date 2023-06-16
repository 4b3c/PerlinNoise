import perlin_noise, pygame, time
from PIL import Image


def avm(x1, x2):
	return max(0, min(255, (x1 + x2)))

def jm(x):
	return max(0, min(255, x))

start = time.time()
map_size = [6, 4]

pn = perlin_noise.perlin_noise_2d(map_size[0], map_size[1])
pn.generate_noise()

resolution = 1
cell_size = 160

pygame.init()
window = pygame.display.set_mode((900, 600))

image = Image.open("images/sunset.jpg")

for x in range(0, map_size[0] * cell_size, resolution):
	for y in range(0, map_size[1] * cell_size, resolution):
		tri = pn.noise_triangle(x / cell_size, y / cell_size) * 105
		sqr = pn.noise_square(x / cell_size, y / cell_size) * 105

		try:
			pixel = image.getpixel((x / 1, y / 1))
		except:
			pixel = (0, 0, 0)

		# pygame.draw.rect(window, (avm(sqr, pixel[0]), avm(pixel[1] * 2, 0), avm(tri, pixel[2])), (x, y, resolution, resolution))
		# pygame.draw.rect(window, (min(255, sqr + pixel[0]), min(255, 10 + pixel[1]), min(255, tri + pixel[2])), (x, y, resolution, resolution))
		pygame.draw.rect(window, (jm(10), jm(tri), jm(sqr + x / 30)), (x, y, resolution, resolution))

	pygame.display.flip()

pygame.image.save(window, "images/img.png")
print("Elapsed time:", time.time() - start)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()