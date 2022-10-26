from commandManager import *
from time import sleep
from libs import *
from pathFinder import pathfinder

commands = [
	[
		"maze",
		{
			"-":False,
			"--bot":False,
			"-o":"~,~,~",
			"-s":"small",
			"-w":"stone",
			"-p":"air",
			"--clean":False
		}
	],
	[
		"bot",
		{
			"-":False,
			"-d":"0",
			"-o":"~,~,~",
			"--clean":False
		}
	]
]

def colorization(bot, blockType: block.Block | int = 251, blockVariationCount: int = 15) -> block.Block:
	return block.Block(blockType if isinstance(blockType, int) else blockType.id, bot.branch % blockVariationCount + 1)

server = Minecraft.create("SERVER_ADDRESS", 4711, "USERNAME")
server.setBlock(25,37,146,57,0)
#Player position calculation
def calcOffset() -> tuple[int]:
	return tuple(server.player.getTilePos())

botGround: ground
#region bot vision
server.setBlock
#endregion
@attr.define(slots=True)
class bot:
	branch: int = 1
	#Visuals
	leftoverBlockType: block.Block | int = colorization
	activeBlockType: block.Block | int = block.MELON
	expandedBlockType: block.Block | int = block.LAPIS_LAZULI_BLOCK
	destructedBlockType: block.Block | int = block.BRICK_BLOCK
	lastBlockType: block.Block | int = block.DIAMOND_BLOCK
	#Bot current position
	position: Vec2 = attr.Factory(lambda: (lambda pos: Vec2(pos[0]-botGround.start.x, pos[2]-botGround.start.y))(calcOffset()))
	#Vision
	visionCalculator: typing.Callable = iterableToBotVision
	visionBlocklist: typing.Iterable = botHVBlocklist
	#Tells us if the bot has crashed
	isActive: bool = True
	#Bots we have to pulse later
	sub_branches: list = []

	def realizePosition(self):
		return self.position.x+botGround.start.x, botGround.height, self.position.y+botGround.start.y

	def growNewGen(self, blocks: list[Vec2]) -> None:
		self.sub_branches: list[bot] = [
			bot(
				branch=self.branch+1,
				leftoverBlockType=self.leftoverBlockType,
				activeBlockType=self.activeBlockType,
				destructedBlockType=self.destructedBlockType,
				expandedBlockType=self.expandedBlockType,
				visionCalculator=self.visionCalculator,
				visionBlocklist=self.visionBlocklist,
				position=block,
			) for block in blocks
		]
		botGround.setBlock(self.position, self.branch)
		server.setBlock(*self.realizePosition(), runIfRunnable(self.expandedBlockType, self))
		self.isActive = False

	def cycle(self):
		#Pulsing the sub_branches if the bot is not active
		if not self.isActive:
			results = []
			for idx, child in enumerate(self.sub_branches):
				match child.cycle():
					case False:
						del self.sub_branches[idx]
					case True:
						return True
				results.append(child.cycle())
			else:
				print(f"branch {self.branch} has gotten pulsed successfully")
				#Sending the destruction signal if there are no sub-branches left
				if len(self.sub_branches) == 0:
					return False
			return

		occupiable = []
		#Looking around
		for block in self.visionCalculator(self.position, self.visionBlocklist):
			if (currentBlock:=botGround.getBlock(block)) == -1: 
				occupiable.append(block)
			elif currentBlock == -2:
				server.setBlock(*self.realizePosition(), runIfRunnable(self.lastBlockType, self))
				return True
		#If the bot has crashed
		if len(occupiable) == 0:
			self.isActive = False
			botGround.setBlock(self.position, self.branch)
			server.setBlock(*self.realizePosition(), runIfRunnable(self.destructedBlockType, self))
			print(f"branch {self.branch} crashed")
			return False
		#If the bot has crashed
		elif len(occupiable) > 1:
			self.growNewGen(occupiable)
			return

		botGround.setBlock(self.position, self.branch)
		server.setBlock(*self.realizePosition(), runIfRunnable(self.leftoverBlockType, self))

		self.position = occupiable[0]
		server.setBlock(*self.realizePosition(), runIfRunnable(self.activeBlockType, self))

	def __attrs_post_init__(self):
		botGround.setBlock(self.position, self.branch)
		server.setBlock(*self.realizePosition(), runIfRunnable(self.activeBlockType, self))
#endregion
#endregion

offset: tuple[int] = calcOffset()
playGround: ground
#Solves a maze
def botGroup(playGround: ground, start: Vec2, delay: float | int, clean):
	global botGround
	botGround = ground(Vec3(playGround.start.x, playGround.height, playGround.start.y), playGround.ground)
	botGround.fixedTypeTranslate(
		{
			"w":0,
			"p":-1
		}
	)
	
	botBlockConfig = {}
	if clean:
		for key in (
			"leftoverBlockType",
			"expandedBlockType",
			"activeBlockType",
			"destructedBlockType"):
			botBlockConfig[key] = block.AIR

	botFather = bot(
		position = Vec2(start.x-botGround.start.x, start.y-botGround.start.y),
		**botBlockConfig
	)

	while True:
		match botFather.cycle():
			#Happens when the maze is solved
			case True: 
				print("done with solving the maze")
				break
			#Happens when no bots are left and all of them have crashed
			case False:
				print("failed with solving the maze")
				break
		sleep(delay)
	return botFather
	
while True:
	for msg in server.player.pollChatPosts():
		match (command:=bakeCommand(
				msg.message,
				commands
			))["name"]:
			case "maze":
				
				#Calculating the offset if needed
				if command["tags"]["-"]:
					offset = calcOffset()

				offset = [numParse(rawNum=raw, baseNum=offset[idx]) for idx, raw in enumerate(commands[0][1]["-o"].split(","))]

				for idx, raw in zip(range(3), command["tags"]["-o"].split(",")):
					offset[idx] = numParse(rawNum=raw, baseNum=offset[idx])

				# with open("a.txt") as f:
				# 	global file
				# 	file = "".join(list(f))
				
				#Making the ground
				playGround: ground = ground(
					Vec3(*offset),
					get(
						"http://mcedu.ir/yas/api/mazemap",
						params={"size":command["tags"]["-s"]}
					).text
				)
				#Building the ground in minecraft
				try:
					visualizeGround(
						*offset,
						command["tags"]["-s"],
						playGround,
						server,
						{
							"w":int(blockType) if ((blockType:=command["tags"]["-w"]).isdigit()) else getattr(block, blockType.upper()),
							"p":int(blockType) if ((blockType:=command["tags"]["-p"]).isdigit()) else getattr(block, blockType.upper())
						}
					)
				except AttributeError:
					server.postToChat("Error: invalid block type")
					print("Error: invalid block type for ground visualization")
					continue

				if command["tags"]["--bot"] or command["tags"]["--solve"]:
					botFather: bot = botGroup(playGround=playGround, start=Vec2(offset[0]+1, offset[2]), delay=0, clean=command["tags"]["--clean"])
					if command["tags"].get("--solve", False):
						pathfinder(
							botGround, server,
							dive(
								botFather,
								lambda item: item.sub_branches[0],
								lambda item: len(item.sub_branches) == 0
							).position
						)

			case "bot":
				if command["tags"].get("--offset-automatically", False):
					offset = (playGround.start.x+1, playGround.height, playGround.start.y)
				elif command["tags"]["-"]:
					offset = calcOffset()

				offset = [numParse(rawNum=raw, baseNum=offset[idx]) for idx, raw in enumerate(commands[1][1]["-o"].split(","))]

				for idx, raw in zip(range(3), command["tags"]["-o"].split(",")):
					offset[idx] = numParse(rawNum=raw, baseNum=offset[idx])

				botFather: bot = botGroup(playGround, Vec2(offset[0], offset[2]), float(command["tags"]["-d"]), command["tags"]["--clean"])

				if command["tags"].get("--solve", False):
					pathfinder(
						botGround, server,
						dive(
							botFather,
							lambda item: item.sub_branches[0],
							lambda item: len(item.sub_branches) == 0
						).position
					)
			case "exit":
				exit()
	sleep(1)