import perlin_noise, pygame, time
from PIL import Image


def avm(x1, x2):
	return max(0, min(255, (x1 + x2) / 2))

def jm(x):
	return max(0, min(255, x))

start = time.time()
map_size = [12, 8]
map_size2 = [6, 4]

pn = perlin_noise.perlin_noise_2d(map_size[0], map_size[1])
pn2 = perlin_noise.perlin_noise_2d(map_size2[0], map_size2[1])
pn.generate_noise()
pn2.generate_noise()

resolution = 1
cell_size = 80
cell_size2 = 160

pygame.init()
window = pygame.display.set_mode((900, 600))

image = Image.open("images/turtle.png")

for x in range(0, map_size[0] * cell_size, resolution):
	for y in range(0, map_size[1] * cell_size, resolution):
		tri = pn.noise_triangle(x / cell_size, y / cell_size) * -300
		sqr = pn2.noise_square(x / cell_size2, y / cell_size2) * 300

		try:
			pixel = image.getpixel((x / 1, y / 1))
		except:
			pixel = (0, 0, 0)


		try:
			# pygame.draw.rect(window, (avm(pixel[1], 255 - pixel[2]), avm(pixel[0], pixel[2]), avm(255 - pixel[0], pixel[1])), (x, y, resolution, resolution))
			# pygame.draw.rect(window, (avm(sqr, pixel[0]), avm(255 - pixel[1], 0), avm(255 - tri, 100 - pixel[2])), (x, y, resolution, resolution))
			# pygame.draw.rect(window, (min(255, sqr + pixel[0]), min(255, 10 + pixel[1]), min(255, tri + pixel[2])), (x, y, resolution, resolution))
			pygame.draw.rect(window, (avm(sqr, 255 + tri), 0, avm(sqr * 2, tri / 2)), (x, y, resolution, resolution))
		except:
			print(sqr, tri, pixel)


	pygame.display.flip()

pygame.image.save(window, "images/img.png")
print("Elapsed time:", time.time() - start)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()