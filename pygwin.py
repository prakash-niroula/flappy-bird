import pygame as pyg
import sys

class pygsprite:

	def __init__(self):
		self.to_update = True
		self.to_draw = True

	def draw_sprite(self, screen):
		pass

	def update(self):
		pass

	def draw(self, screen):
		if self.to_draw: self.draw_sprite(screen)
		if self.to_update: self.update()

class __pygimg__:
	
	def __init__(self):
		pass

	def crop(self, image, tocrop):
		pys = pyg.Surface((tocrop[2], tocrop[3]))
		pys.blit(image, (0,0), (tocrop[0], tocrop[1], tocrop[2], tocrop[3]))
		pys.set_colorkey('black')
		return pys

	def resize(self, *args, **kwargs):
		return pyg.transform.scale(*args, **kwargs)

	def scale(self, img, scaleFactor):
		x, y = img.get_size()
		return pyg.transform.scale(img, (x * scaleFactor, y * scaleFactor))

	def load(self, *args, **kwargs):
		return pyg.image.load(*args, **kwargs)

	def rotate(self, *args, **kwargs):
		return pyg.transform.rotate(*args, **kwargs)


class pygwin:
	
	def __init__(self, title="Hello World!", size=(600, 600), fps=60):
		self.title = title
		self.size = size
		self.fps = fps
		self.clock = pyg.time.Clock()
		pyg.init()
		self.screen = pyg.display.set_mode(self.size)
		pyg.display.set_caption(self.title)

	def blit(self, *args, **kwargs):
		self.screen.blit(*args, **kwargs)

	def handle_event(self, event):
		pass

	def update(self):
		pass


	def run(self):

		while True:
			for event in pyg.event.get():
				self.handle_event(event)
				if event.type == pyg.QUIT:
					pyg.quit()
					sys.exit(1)

			self.update()
			pyg.display.update()
			self.clock.tick(self.fps)

pygimg = __pygimg__()

def __loadsound__(*args, **kwargs):
	return pyg.mixer.Sound(*args, **kwargs)

def __loadmusic__(*args, **kwargs):
	return pyg.mixer.music.load(*args, **kwargs)

pyg.loadsound = __loadsound__
pyg.loadmusic = __loadmusic__