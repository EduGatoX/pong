from .player import Player
from .ball import Ball
from .paddle import Paddle, PaddleType

# CONSTANTS
# Ball parameters
BALL_RADIUS = 10
BALL_VX0, BALL_VY0 = -6, 0  # ball initial velocity
BALL_VX_MAX, BALL_VY_MAX = 2, 2  # ball maximum velocity
BALL_VEL_MULTIPLIER = 1.1  # ball increase velocity multiplier

# Paddle parameters
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100  # paddle size
PADDLE_VY = 0  # paddle movement velocity

# Collision parameters
TOLERANCE = 0.5


class GameModel:
    def __init__(self, width: int, height: int) -> None:
        """
        Class responsible for managing the behavior of the model.
        
        Attributes:
            width (int) : width of the pong field
            height (int) : height of the pong field
            ball (Ball) : Ball object of the game
            player_left (Player) : Player object at the left side of the field
            player_right (Player) : Player object at the right side of the field
        """
        # Size of the game field
        self.width = width
        self.height = height

        # Create ball
        self.ball = Ball(
            x=width // 2,
            y=height // 2 + 10,
            radius=BALL_RADIUS,
            vx=BALL_VX0,
            vy=BALL_VY0,
        )

        # Create left player with its paddle
        self.player_left = Player(
            name="left player",
            score=0,
            paddle=Paddle(
                x=10,
                y=(height - PADDLE_HEIGHT) // 2,
                width=PADDLE_WIDTH,
                height=PADDLE_HEIGHT,
                vy=PADDLE_VY,
                paddle_type=PaddleType.LEFT_PADDLE,
            ),
        )

        # Create right player with its paddle
        self.player_right = Player(
            name="right player",
            score=0,
            paddle=Paddle(
                x=width - 10 - PADDLE_WIDTH,
                y=(height - PADDLE_HEIGHT) // 2,
                width=PADDLE_WIDTH,
                height=PADDLE_HEIGHT,
                vy=PADDLE_VY,
                paddle_type=PaddleType.RIGHT_PADDLE,
            ),
        )

    def reset(self) -> None:
        self.ball.x = self.width // 2
        self.ball.y = self.height // 2 + 10
        self.ball.vx = BALL_VX0
        self.ball.vy = BALL_VY0
        self.player_left.paddle.y = (self.height - PADDLE_HEIGHT) // 2
        self.player_right.paddle.y = (self.height - PADDLE_HEIGHT) // 2

    def process(self) -> Player | None:
        self.process_ball()
        self.process_paddle()
        player = self.process_score()
        if player: # if there is a score
            self.reset()
        return player

    def process_ball(self) -> None:
        """Moves the ball and handles the collisions"""
        # move the ball
        self.ball.move()

        # handle ball collisions
        handle_floor_ceiling_collision(self.ball, self.height)
        handle_paddle_collision(self.ball, self.player_left.paddle)
        handle_paddle_collision(self.ball, self.player_right.paddle)

    def process_score(self) -> Player | None:
        """Process the score. If a point has been scored by a Player
        updates the corresponding Player score and returns that Player
        back to the caller.
        Returns None if no player have scored a point in this check."""
        player = None
        if has_scored(self.ball, edge=self.width):
            self.player_left.score += 1
            player = self.player_left
        elif has_scored(self.ball, edge=0):
            self.player_right.score += 1
            player = self.player_right
        return player

    def process_paddle(self) -> None:
        self.player_left.paddle.move()


# ************************* #
# **** Score Functions **** #
# ************************* #


def has_scored(ball: Ball, edge: int) -> bool:
    """Returns True if the 'ball' has reached the 'edge'
    which means that a point has been scored.
    Returns False if not."""
    if abs(ball.edge.x - edge) <= TOLERANCE:
        return True
    return False


# ************************* #
# ** Collision Functions ** #
# ************************* #

def handle_paddle_collision(ball: Ball, paddle: Paddle):
    """Handles the collision between the ball and the paddle.
    It checks if there was a collision, reverse the direction of the ball
    and performs a variable update for vy."""
    has_collided = (
        abs(ball.edge.x - paddle.edge.x) <= TOLERANCE
        and paddle.y <= ball.y <= paddle.y + paddle.height
    )

    if has_collided:
        # Reverse the 'x' direction
        ball.vx *= -1
        # Change 'vy' of the ball depending on the relative 'y'
        # position of the ball and the center of the paddle.
        dy = ball.y - (paddle.y + paddle.height / 2)
        ball.vy = BALL_VY_MAX * dy / (paddle.height / 2)


def handle_floor_ceiling_collision(ball: Ball, height: int):
    """Handles the collision between the ball and the floor or ceiling.
    It checks if there was a collision ans reverse the direction of the ball."""

    has_collided = (
        abs(ball.edge.y) <= TOLERANCE or abs(ball.edge.y - height) <= TOLERANCE
    )

    if has_collided:
        # Reverse the 'y' direction
        ball.vy *= -1
