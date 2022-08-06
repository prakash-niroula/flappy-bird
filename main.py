from pygwin import *
import assets

# ATTRIBUTE
# Great Piano artist - Komiku - https://www.chosic.com/download-audio/25106/
# Its very nice music :)

# already can render out pipes so just randomize and collision and hook up to bird class August 5 2022

# container for everything
class FlappyBirdGame(pygwin):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.started = False

		self.music = pyg.loadmusic('audio/music.ogg')
		pyg.mixer.music.play(-1)
		pyg.mixer.music.set_volume(.4)
		
		self.bg = assets.Backround(
			bgimg='sprites/background-day.png', baseimg='sprites/base.png', size=self.size,
		)
		self.bg.to_update = False
		self.menu = assets.GameStart(img='sprites/message.png', size=self.size)

		self.bird = assets.Bird(
			flysound='audio/wing.ogg', pointsound='audio/point.ogg',
			hitsound='audio/hit.ogg', diesound='audio/die.ogg',
			img='sprites/yellowbird-{}.png', frames=3, size=self.size,
			pipehimg='sprites/pipe-head.png', pipebimg='sprites/pipe-body.png',
			numimg='sprites/{}.png', numframes=10, numcenter=(self.size[0]/2, self.size[1]/15)
		)
		self.bird.ingame = False

		self.gameover = assets.GameOver(img='sprites/gameover.png', size=self.size)
		self.gameover.to_draw = False

	def update(self):
		if self.bird.dead and not self.gameover.to_draw:
			self.bg.still()
			self.started = False
			self.gameover.to_draw = True
		self.bg.draw(self.screen)
		self.menu.draw(self.screen)
		self.bird.draw(self.screen)
		self.gameover.draw(self.screen)

	def handle_event(self, event):
		self.bird.handle_event(event)
		if self.started == False and (event.type == pyg.MOUSEBUTTONDOWN or event.type == pyg.KEYUP):
			self.menu.to_draw = False
			self.bg.to_update = True
			self.started = True
			self.gameover.to_draw = False
			self.bird.reset()
			self.bg.reset()

game = FlappyBirdGame(title="Let's go BOOM!", fps=30)
game.run()