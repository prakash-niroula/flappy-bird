from pygwin import *
import random

# Game Background

class Backround(pygsprite):

	# make a background moving type thingy
	# [ TO IMPRESS THE USER IN SOME WAY HUH ?, umm no for a cool feature ]
	def __init__(self, bgimg, baseimg, size):
		super().__init__()
		# SETUP ALL THE THINGS, images, timers, speed and MORE
		self.size = size
		self.img_load = pygimg.load(bgimg).convert_alpha()
		
		self.img = pygimg.resize(self.img_load, (self.size[0], self.size[1]-75))
		self.image_rect = [
			pyg.Rect(0, 0, self.size[0], self.size[1]-75),
			pyg.Rect(self.size[0], 0, self.size[0], self.size[1]-75)
		]
		self.base_img = pygimg.load(baseimg).convert_alpha()
		self.base = pygimg.resize(self.base_img, (self.size[0], 75))
		self.base = pygimg.crop(self.base, (0,2,self.base.get_size()[0], self.base.get_size()[1]))
		self.base_rect = [
			pyg.Rect(0, self.size[1]-75, self.size[0], self.size[1]),
			pyg.Rect(self.size[0], self.size[1]-75, self.size[0], self.size[1])
		]
		self.speedx = 2
		self.basespeed = 5

	def reset(self):
		self.image_rect = [
			pyg.Rect(0, 0, self.size[0], self.size[1]-75),
			pyg.Rect(self.size[0], 0, self.size[0], self.size[1]-75)
		]
		self.base_rect = [
			pyg.Rect(0, self.size[1]-75, self.size[0], self.size[1]),
			pyg.Rect(self.size[0], self.size[1]-75, self.size[0], self.size[1])
		]

	def update(self):
		# the movement in y axis

		# the movement in the so called "x axis" aka the "parallax effect" of infinite movement
		self.image_rect[0].x -= self.speedx
		self.image_rect[1].x -= self.speedx
		self.base_rect[0].x -= self.basespeed
		self.base_rect[1].x -= self.basespeed

		# if things kinda overflow, handle that YOU BAD CODE

		if self.image_rect[1].x-self.speedx < 0:
			self.image_rect[0].x = 0
			self.image_rect[1].x = self.size[0]

		if self.base_rect[1].x-self.basespeed < 0:
			self.base_rect[0].x = 0
			self.base_rect[1].x = self.size[0]

	def still(self):
		self.to_update = False

	def draw_sprite(self, screen):
		# oh wait, this guy's chilling man. I wish everything could be that simple
		# JUST BLIT It into its RECT
		screen.blit(self.img, self.image_rect[0])
		screen.blit(self.img, self.image_rect[1])
		screen.blit(self.base, self.base_rect[0])
		screen.blit(self.base, self.base_rect[1])
# Game Startscreen

class GameStart(pygsprite):
	# do you want a cool type start screen in less than 25 lines of code ?
	# OBVIUSLY WHY NOT, PLEASE I BEG YOU
	# your wish has been granted
	def __init__(self, img, size):
		super().__init__()
		self.img = pygimg.load(img).convert_alpha()
		self.img_rect = self.img.get_rect(center=(size[0]/2, size[1]/2))
		self.alpha = 255
		self.speed = 20

	def draw_sprite(self, screen):
		screen.blit(self.img, self.img_rect)

	def update(self):
		self.alpha -= self.speed
		
		if self.alpha > 255:
			self.speed = -self.speed

		if self.alpha-self.speed < 20:
			self.speed = -self.speed

		self.img.set_alpha(self.alpha)

class Numbers(pygsprite):

	def __init__(self, images, frames, num, center):
		super().__init__()
		self.value = str(num)
		self.numd = {}
		for x in range(frames):
			self.numd[str(x)] = pygimg.load(images.format(x)).convert_alpha()

		self.rect = self.numd["0"].get_rect(center=center)
		self.x = self.rect.x

		self.center = center

	def draw_sprite(self, screen):
		tw = self.rect.width * len(self.value)
		px, py = self.x - tw//2, self.rect.y
		for x in self.value:
			self.rect.x = px
			screen.blit(self.numd[x], self.rect)
			px += self.rect.width + ( -5 if x=="1" else 2)

	def update_num(self, num):
		self.value = str(num)


# the flapping bird aka the BAD BIRD WITH BAD CODE
class Bird(pygsprite):

	def __init__(
		self, img, size, frames, pipehimg, pipebimg, numimg, numframes, numcenter, flysound,
		pointsound, hitsound, diesound
	):
		super().__init__()
		self.frames = []
		self.original_frames = []
		self.size = size

		self.flysound = pyg.loadsound(flysound)
		self.flysound.set_volume(0.3)
		self.pointsound = pyg.loadsound(pointsound)
		self.hitsound = pyg.loadsound(hitsound)
		self.diesound = pyg.loadsound(diesound)
		
		for x in range(frames):
			self.frames.append(pygimg.scale(pygimg.load(img.format(x)).convert_alpha(), 1.4))
			self.original_frames.append(pygimg.scale(pygimg.load(img.format(x)).convert_alpha(), 1.4))

		# SO MUCH VARIABLES brain.py has stopped working
		self.img_rect = self.frames[0].get_rect(center=(size[0]/2, size[1]/1.72))
		self.currentFrame = 0
		self.timer = 0
		self.ingame = False
		self.animateTimer = 0
		self.up = True
		self.animateTimer2 = 0
		self.animateJump = False
		self.fangle = -91
		self.moved = False
		self.launch = False
		self.launchVel = 0
		self.launchTime = 0
		self.launchAdd = 1
		self.launchup = True
		self.dead = False
		self.flapanimation = True
		self.take_input = True
		self.once = False
		self.score = 0
		self.tmpsc = 0
		self.num = Numbers(numimg, numframes, 0, numcenter)

		w, h = self.frames[0].get_size()
		self.x = 0.2*self.size[0],
		self.y = 0.5*self.size[1],
		self.w = w
		self.h = h

		# timer of pipe spawning [ how frequent do they spawn in the code ]
		self.pipeTimer = 0
		self.pipes = []
		self.pipehimg = pygimg.load(pipehimg).convert_alpha()
		self.pipebimg = pygimg.load(pipebimg).convert_alpha()

	def draw_sprite(self, screen):
		for y in self.pipes:
			y.draw(screen)
		screen.blit(self.frames[self.currentFrame], self.img_rect)
		self.num.update_num(num=self.score)
		self.num.draw(screen)

	def launch_up(self):
		self.flapanimation = True
		# first launch up INTO THE AIR
		self.launchVel -= 1
		self.launchTime += self.launchVel
		# if the velocity reached 0 when launching
		if self.launchVel == 0:
			self.launchup = False
			self.launchTime = 0
		self.img_rect.y -= self.launchTime

	def push_down(self):
		self.launchTime += 2
		if self.launchTime > 10:
			# COLLISION DETECTION OF GROUND GRRRRRRR
			if self.img_rect.y+140 >= self.size[1]:
				self.dead = True
				return True
			# THEN BRING THE BIRD TO TOUCH THE GROUND
			self.flapanimation = False
			self.currentFrame = 1
			self.img_rect.y += self.launchTime - 10

	def animate_down(self, curAngle):
		# BUT HEY, NOW HOW ARE YOU GONNA MAKE IT SMOOTHLY TURN DOWN
		# brain.py has stopped working x2
		# BUT I MANAGED TO PULL IT OFF
		# - Meanwhile the gods in heaven: Hello sir, may you tell what is your name?
		# - We can't let you enter without it
		self.animateTimer += self.animateTimer + 0.5
		
		# unless the birdie is -90 degrees turned, smoothly turn by 45 - animateTimer
		# animateTimer is being increased by itself + 0.5 so smooth [ at least i think so]
		if self.fangle > -90: self.fangle = curAngle - self.animateTimer

		# Wooo crazy code, wanna be -91 and beyond, I WONT LET THAT YOU BAD CODE
		if self.fangle < -90: self.fangle = -90
		if self.fangle >= -90:
			# now rotate every frame [ WHO TOLD YOU TO FLAP THE BIRD in FIRST PLACE ]
			# OH WHO TOLD YOU TO MAKE THIS GAME
			# WHO TOLD TO LEARN PYTHON, WHO TOLD YOU TO BE BORN..
			# uhmm it's going too far i guess we should stop, yeah ok.
			for x in range(len(self.frames)):
				self.frames[x] = pygimg.rotate(self.original_frames[x], self.fangle)

	def collides(self, cord1, cord2):
		# is cord1's body over cord2 ?
		# WAIT, ARE THEY HAVING *** ?
		# KILL THEM IF THEY ARE
		a = (
			cord1[2] >= cord2[0] and cord1[0] <= cord2[2] and cord1[3] >= cord2[1] and cord1[1] <= cord2[3]
		)
		return a or False

	def update(self):	

		# increase the timer BRO
		self.pipeTimer += 1

		if True: # what the ****, oh wait, its for making the code looong so i seem smart 8) don't mind me
			self.x, self.y = self.img_rect.x, self.img_rect.y
			self.cords = [self.x, self.y, self.x+self.w, self.y+self.h]


		if self.dead:
			for y in self.pipes:
				y.to_update = False
			self.to_update = False
			self.diesound.play()

		# frame update to flap its wings
		if self.flapanimation:
			self.timer += 1
			if self.timer < 3:
				pass
			else:
				self.currentFrame += 1
				self.timer = 0
			if self.currentFrame > len(self.frames)-1:
				self.currentFrame = 0

		# this is the bird in verge of dying
		if self.img_rect.y < 0:
			self.img_rect.y = 0
			self.hitsound.play()
			self.launch = True
			self.launchup = False
			self.animateJump = True
			self.up = False
			self.animateTimer = 1
			self.take_input = False
			return

		tmpvar = False
		for x in self.pipes:
			if (self.collides(self.cords, x.cords[0]) or self.collides(self.cords, x.cords[1])) and self.take_input:
				self.hitsound.play()
				for y in range(len(self.pipes)):
					self.pipes[y].to_update = False
					self.once = False
				self.launch = True
				self.launchup = False
				self.animateJump = True
				self.up = False
				self.animateTimer = 1
				self.take_input = False
			tmpvar = tmpvar or self.cords[2] > x.cords[0][0] and x.cords[0][2] > self.cords[2]
			if self.cords[2] > x.cords[0][0] and x.cords[0][2] > self.cords[2] and not self.tmpsc:
				self.tmpsc = True
				self.score += 1
				self.pointsound.play()
		if not tmpvar:
			self.tmpsc = False


		# code to launch up [ only the movement i mean the y axis velocity]
		# brain.py has stopped working
		if self.launch:
			if self.launchup:
				self.launch_up()
			else:
				# simple right ? NO LOOK THE CODE IN THE FUNCTIONS ;-;
				if self.push_down(): return

		# Me coding to animate the jump
		# - Meanwhile the news reporter: The Sun has turned into a Red Giant
		if self.animateJump:
			self.animateTimer2 += 1

			if self.animateTimer2 > 10 and self.up:
				# stop for a while to let the user press a key :/
				self.up = False
				self.animateTimer = 0

			if self.up == True and self.animateTimer==0:
				# Let's now animate the birdie flying up in 45 degress that's pretty easy

				self.animateTimer = 1
				# make the angle 45 degree
				self.fangle = 45
				# apply to every frame
				for x in range(len(self.frames)):
					self.frames[x] = pygimg.rotate(self.original_frames[x], self.fangle)
			elif self.up == False:
				self.animate_down(45)


		# are we in game birdie ? I guess so, user pressed a key, HURRY UP
		# HURRY HURRY, umm what happened ? JUST COME HERE YOUR ARRIVAL IS NECESSARY
		# OK dude CaLm DoWn!
		if self.moved == False and self.img_rect.x > (0.2*self.size[0]) and self.ingame:
			self.img_rect.x = 0.2*self.size[0]
			self.moved = True

		# Spawn some pipes for the spice BROO - are u sure to terminate your brain : YEAH T_T
		if self.pipeTimer > random.randint(30, 50) and self.once:
			self.pipeTimer = 0
			total = random.randint(280, 310)
			h1 = random.randint(10, total-10)
			h2 = total - h1
			if len(self.pipes) < 6:
				# push pipe
				self.pipes.append(Pipe(
					headimg=self.pipehimg, bodyimg=self.pipebimg, x=600,
					y=self.size[1]-75, h1=h1, h2=h2
				))
			else:
				# remove the "hidden" or the first pipe which is no more in screen
				# AND AGAIN PUSH PIPES
				self.pipes = self.pipes[1:]
				# [ wait you could have pushed pipes below if statement ] - SHHHH
				# I NEED TO MAKE THE CODE SEEM LONG NERD
				self.pipes.append(Pipe(headimg=self.pipehimg, bodyimg=self.pipebimg, x=600, y=self.size[1]-75, h1=h1, h2=h2))


	def reset(self):
		# THIS IS SOME LONG CODE HAHA
		# wait, isn't calling self.__init__() partially right ? I WILL KILL YOU STOP TELLING
		# I NEED LOOONG CODE
		self.img_rect = self.frames[0].get_rect(center=(self.size[0]/2, self.size[1]/1.72))
		self.img_rect.x = 0.2*self.size[0]
		self.ingame = True
		self.to_update = True
		self.to_draw = True
		self.currentFrame = 0
		self.timer = 0
		self.animateTimer = 0
		self.up = True
		self.animateTimer2 = 0
		self.animateJump = False
		self.fangle = -91
		self.moved = True
		self.launch = False
		self.launchVel = 0
		self.launchTime = 0
		self.launchAdd = 1
		self.launchup = True
		self.dead = False
		self.flapanimation = True
		self.take_input = True
		self.pipeTimer = 0
		self.pipes = []
		self.once = False
		self.score = 0
		self.tmpsc = 0
		for x in range(len(self.frames)):
			self.frames[x] = self.original_frames[x]

	def flap(self):
		self.flysound.play()
		# bird.flap()
		# When bird flaps, animate the jump to make that look sick
		self.animateJump = True
		# OBVIOUSLY BIRD GOES UP RIGHT?
		self.up = True

		# TIME IS NECESSARY IN ANIMATION
		self.animateTimer2 = 0
		self.animateTimer = 0

		# LAUNCH THE BIRDIE with a velocity of 6 [ higher might make the bird goto heaven ]
		self.launch = True
		self.launchVel = 6
		# LAUNCH TIME IS ALSO NECESSARY
		self.launchTime = 0
		# WHAT ARE YOU QUESTIONING BRO LAUNCH UP using JETFUEL
		self.launchup = True

	def handle_event(self, event):
		# Hey function, You are having a good time than us :)
		# just handle User Input :>

		# Umm yeah :) ok!
		if self.take_input:
			if event.type == pyg.MOUSEBUTTONDOWN and self.ingame:
				self.flap()
				if not self.once: self.once = True
			elif event.type == pyg.KEYDOWN and self.ingame:
				if event.key == pyg.K_SPACE:
					self.flap()
					if not self.once: self.once = True

class GameOver(pygsprite):
	# do you want a cool type GameOver screen in less than 25 lines of code ?
	# OBVIUSLY WHY NOT, PLEASE I BEG YOU
	# your wish has been granted
	def __init__(self, img, size):
		super().__init__()
		self.img = pygimg.load(img).convert_alpha()
		self.img_rect = self.img.get_rect(center=(size[0]/2, size[1]/2))
		self.alpha = 255
		self.speed = 25

	def draw_sprite(self, screen):
		screen.blit(self.img, self.img_rect)

	def update(self):
		self.alpha -= self.speed
		
		if self.alpha > 255:
			self.speed = -self.speed

		if self.alpha-self.speed < 20:
			self.speed = -self.speed

		self.img.set_alpha(self.alpha)

class Pipe(pygsprite):
	# THe pIpE [ may look simple but it isn't - keep eye on #notSimple ]

	def __init__(self, headimg, bodyimg, x, y, h1, h2):
		super().__init__()

		# Let's take its cut out HEAD and cut out BODY
		# AND stretch it out LIKE CHEWING GUM to meet our requirements

		self.head = headimg
		self.body = bodyimg

		w, _ = self.body.get_size()

		self.body_r1 = pyg.Rect(x, 0, w, h1)
		self.body_r2 = pyg.Rect(x, y - h2, w, h2)

		self.head_r1 = self.head.get_rect()
		self.head_r1.x = x
		self.head_r1.y = h1
		self.head_r2 = self.head.get_rect()
		self.head_r2.x = x

		self.speed = 5

		# notSimple
		_, hh = self.head.get_size()
		self.head_r2.y = y - h2 - hh
		
		# notSimple
		self.width = w
		self.h1, self.h2 = h1, h2
		self.hidden = False

		# NOT SIMPLE WTH [ brain.py has stopped working ]
		self.cords = [[x+2, 0, x+self.width-2, h1+hh-8], [x+4, y - h2 - hh + 4 , x+self.width-2, y]]

	def update(self):
		if not self.hidden:
			# move the head and body at the same speed to give illusion
			# to user that it is same object :troll:
			self.cords[0][0] -= self.speed
			self.cords[0][2] -= self.speed

			self.cords[1][0] -= self.speed
			self.cords[1][2] -= self.speed

			self.head_r1.x -= self.speed
			self.head_r2.x -= self.speed
			self.body_r1.x -= self.speed
			self.body_r2.x -= self.speed


	def draw_sprite(self, screen):
		# STRETCH THE BODDDDY
		tmpb = pygimg.resize(self.body, (self.width, self.h1))
		tmpb2 = pygimg.resize(self.body, (self.width, self.h2))

		if not self.hidden:
			# DRAW THE BODY
			screen.blit(self.head, self.head_r1)
			screen.blit(self.head, self.head_r2)
			screen.blit(tmpb, self.body_r1)
			screen.blit(tmpb2, self.body_r2)