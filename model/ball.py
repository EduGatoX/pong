from dataclasses import dataclass


@dataclass(slots=True)
class BallEdge:
    x: int  # 'x' coordinate of the edge of the ball
    y: int  # 'y' coordinate of the edge of the ball

@dataclass
class Ball:
    x:int
    y:int
    radius:int
    vx:int
    vy:int

    @property
    def edge(self) -> BallEdge:
        """Returns the edge of the ball that may collide."""
        x = self.x + self.radius * (1 if self.vx >= 0 else -1)
        y = self.y + self.radius * (1 if self.vy >= 0 else -1)
        return BallEdge(x, y)

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy