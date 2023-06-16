import pygame
from PIL import Image

image = Image.open("images/feat_map.jpg")

pygame.init()
window = pygame.display.set_mode((900, 600))

def jm(x):
	return max(0, min(255, x))

for x in range(898):
	for y in range(598):
		pixel = image.getpixel((x, y))
		
		pygame.draw.rect(window, (jm(100 - pixel), pixel, pixel), (x, y, 1, 1))

	pygame.display.flip()


pygame.image.save(window, "images/img.png")


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()