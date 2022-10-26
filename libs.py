#MCPI
from mcpi_e.minecraft import Minecraft
from mcpi_e.vec3 import Vec3
from mcpi_e import block
#Class libs
from dataclasses import dataclass
import typing
import attr
#Custom libs
from vec2 import Vec2
from ground import *

from functools import partial
from itertools import chain

def runIfRunnable(object, *args, **kwargs):
	if callable(object):
		return object(*args, **kwargs)
	return object

#Checking blocks surrounding the bot/pathfinder in each cycle
def iterableToBotVision(position: Vec2, iterable: typing.Iterable[typing.Iterable[int]]) -> typing.Generator:
	return [Vec2(position.x + xp, position.y + yp) for xp, yp in iterable]
def chainingIterablesToBotVision(position: Vec2, *iterables: typing.Iterable[typing.Iterable[int]]):
	return chain(*(iterableToBotVision(position, iterable) for iterable in iterables))
#Bot diagonal block vision list
botDiagonalVisionBlocklist = (
	(1, 1),
	(1, -1),
	(-1, 1),
	(-1, -1)
)
#Bot Horizontal & Vertical block vision list
botHVBlocklist = (
	(1, 0),
	(-1, 0),
	(0, 1),
	(0, -1)
)

def dive(object, key: typing.Callable, stopSign: typing.Callable):
	while True:
		if stopSign(object:=key(object)):
			return object