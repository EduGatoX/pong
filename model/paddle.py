from enum import Enum
from dataclasses import dataclass


@dataclass(slots=True)
class PaddleEdge:
    """Represents the 'x' coordinate of the edge
    of the paddle, used for collision detection purposes"""

    x: int


class PaddleType(Enum):
    LEFT_PADDLE = "left_paddle"
    RIGHT_PADDLE = "right_paddle"


@dataclass
class Paddle:
    x: int
    y: int
    width: int
    height: int
    vy: int
    paddle_type: PaddleType

    @property
    def edge(self) -> PaddleEdge:
        """Returns an object that represents the edge of the paddle"""
        if self.paddle_type == PaddleType.LEFT_PADDLE:
            return PaddleEdge(self.x + self.width)

        return PaddleEdge(self.x)

    def move(self) -> None:
        self.y += self.vy
