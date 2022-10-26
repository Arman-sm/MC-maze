from multipledispatch import dispatch
from dataclasses import dataclass
from requests import get
from mcpi_e.vec3 import Vec3
from vec2 import Vec2

class ground:
	def __init__(self, start: Vec3, groundText: str | list):
		self.ground = [line.split() for line in groundText.split("\n")] if isinstance(groundText, str) else groundText
		self.start = Vec2(start.x, start.z)
		self.height = start.y
		self.end = Vec2(start.x + len(self.ground), start.y + len(self.ground[0]))
		self.translateCache = None
		self.protectiveWallEnabled = True 
		self.active = True
	#translate each block type by a dict
	def translateTypeGen(self, charDict: dict):
		return map(lambda row: map(lambda char: charDict[char], row), self.ground)
	def translateType(self, charDict: dict):
		return [[charDict[blockType] for blockType in blockTypes] for blockTypes in self.ground]

	@dispatch(int, object)
	def getBlock(self, x: int, y: int):
		try:
			return self.ground[x][y]
		except IndexError:
			# result = -1 if self.protectiveWallEnabled else -2
			# self.protectiveWallEnabled = False
			# return result
			return -2 if x > 0 and y > 0 else 0
	@dispatch(Vec2)
	def getBlock(self, position: Vec2):
		return self.getBlock(position.x, position.y)

	@dispatch(int, int, object)
	def setBlock(self, x, y, blockType, /) -> None:
		self.ground[x][y] = blockType
	@dispatch(Vec2, object)
	def setBlock(self, position: Vec2, blockType, /) -> None:
		self.ground[position.x][position.y] = blockType

	def fixedTypeTranslate(self, charDict) -> None:
		self.ground = self.translateType(charDict)

def visualizeGround(
	startX: int, startY: int, startZ: int,
	size: str, ground: ground,
	server,
	blockTypes: dict) -> None:

	for x, blockIds in enumerate(
			ground.translateTypeGen(blockTypes),
			startX
		):
		for z, blockId in enumerate(blockIds, startZ):
			server.setBlock(x, startY, z, blockId)