from mcpi_e.minecraft import Minecraft
from mcpi_e.block import *
from time import sleep

server = Minecraft.create("192.168.1.107", 4711, "Ironman1388")
offset = server.player.getPos()

while True:
	server.setBlock(offset.x, offset.y, offset.z, Block(251,9))
	sleep(0.5)
	server.setBlock(offset.x, offset.y, offset.z, 0)
	offset.z += 1