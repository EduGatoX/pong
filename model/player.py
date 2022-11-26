from dataclasses import dataclass, field
from .paddle import Paddle


@dataclass
class Player:
    name: str
    score: str
    paddle: Paddle = field(repr=False)
