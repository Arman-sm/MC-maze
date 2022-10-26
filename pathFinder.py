from vec2 import Vec2
import typing
import attr
from libs import *

@attr.define(slots=True)
class pathfinder:
	maze: ground
	server: Minecraft
	pastPosition: Vec2 = Vec2(9,10)
	position: Vec2 = Vec2(9, 10)
	currentBranch: int = float("inf")
	#If the program has to do all the cycling stuff
	autoPilot: bool = True
	#Block visualization
	activeBlockType: block.Block | int | typing.Callable = block.GOLD_BLOCK
	leftoverBlockType: block.Block | int | typing.Callable = block.ICE
	#Vision
	visionCalculator: typing.Callable = iterableToBotVision
	visionBlocklist: typing.Iterable = botHVBlocklist

	def realizePosition(self):
		return self.position.x+self.maze.start.x, self.maze.height, self.position.y+self.maze.start.y

	def cycle(self):
		surrounding: list[Vec2] = list(self.visionCalculator(self.position, self.visionBlocklist))
		if self.pastPosition in surrounding:
			surrounding.remove(self.pastPosition)
		#Checking if there are valid blocks in our vision calculated by the self.visionCalculator
		if (surrounding:=tuple(filter(
				lambda block: 0 < block[1] <= self.currentBranch,
				((position, self.maze.getBlock(position)) for position in surrounding)))):
			
			self.server.setBlock(*self.realizePosition(), runIfRunnable(self.leftoverBlockType, self))
			#Updating past position
			self.pastPosition = self.position
			#Updating current position and branch info
			self.position, self.currentBranch = min(surrounding, key = lambda item: item[1])

			self.server.setBlock(*self.realizePosition(), runIfRunnable(self.activeBlockType, self))
			return True
		return False

	def __attrs_post_init__(self):
		self.pastPosition = self.position
		while self.autoPilot:
			if not self.cycle():
				break