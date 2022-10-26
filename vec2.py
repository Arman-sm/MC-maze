from dataclasses import dataclass
@dataclass(slots=True)
class Vec2:
	x: int
	y: int