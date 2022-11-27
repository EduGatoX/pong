import pygame

from model.game_model import GameModel
from model.ball import Ball
from model.paddle import Paddle
from model.player import Player
from model.paddle_listener import setup_paddle_event_handlers
from view.game_view import GameView

from event.event import post_event, EventType

# *************************************************** #
# ****************** View Settings ****************** #
# *************************************************** #

# ***************** Window Settings ***************** #

WINDOW_NAME = "Pong"  # name of the window
WINDOW_WIDTH, WINDOW_HEIGHT = 700, 500  # size of the window
FPS = 60  # frames per second

# ****************** Color Settings ***************** #

Color = tuple[int, int, int]  # represents an RGB color (3 numbers between 0 and 255)
BACKGROUND_COLOR: Color = (91, 136, 199)
MID_LINE_COLOR: Color = (100, 255, 255)
BALL_COLOR: Color = (35, 186, 58)
LEFT_PADDLE_COLOR: Color = (219, 131, 31)
RIGHT_PADDLE_COLOR: Color = (179, 23, 160)

# ****************** Text Settings ****************** #

SCORE_FONT = ("comicsans", 50)
MESSAGE_FONT = ("comicsans", 50)
SCORE_COLOR: Color = (190, 250, 244)
MESSAGE_COLOR: Color = (119, 245, 56)

# **************************************************** #
# ****************** Model Settings ****************** #
# **************************************************** #

WIN_SCORE = 5  # Score for winning the game
PADDLE_DELTA_Y = 5 # Paddle Y speed


class GameController:
    def __init__(self, model: GameModel, view: GameView) -> None:
        self.model = model
        self.view = view

    def process_model(self) -> Player | None:
        """Process the model and returns the Player that scored a point.
        None if there wasn't a score in this iteration"""
        return self.model.process()

    def process_user_input(self):
        """Process the user inputs by posting the corresponding event"""
        keys = pygame.key.get_pressed()
        paddle_left = self.model.player_left.paddle
        paddle_right = self.model.player_right.paddle
        if keys[pygame.K_w] and self.model.in_bounds(paddle_left, -PADDLE_DELTA_Y):
            post_event(EventType.paddle_up, paddle_left)
        if keys[pygame.K_s] and self.model.in_bounds(paddle_left, PADDLE_DELTA_Y):
            post_event(EventType.paddle_down, paddle_left)
        if keys[pygame.K_UP] and self.model.in_bounds(paddle_right, -PADDLE_DELTA_Y):
            post_event(EventType.paddle_up, paddle_right)
        if keys[pygame.K_DOWN] and self.model.in_bounds(paddle_right, PADDLE_DELTA_Y):
            post_event(EventType.paddle_down, paddle_right)

    def render_view(self) -> None:
        """Renders the view."""
        render_fns = (
            render_background(BACKGROUND_COLOR),
            render_mid_line(self.model.width, self.model.height, MID_LINE_COLOR),
            render_ball(self.model.ball, BALL_COLOR),
            render_paddle(self.model.player_left.paddle, LEFT_PADDLE_COLOR),
            render_paddle(self.model.player_right.paddle, RIGHT_PADDLE_COLOR),
            render_score(self.model.width // 4, 20, self.model.player_left),
            render_score(self.model.width * 3 // 4, 20, self.model.player_right),
        )
        self.view.render(*render_fns)
        self.view.update()

    def render_victory_view(self, player: Player):
        """Renders the victory screen"""
        self.view.render(render_victory(self.model.width, self.model.height, player))
        self.view.update()

    def mainloop(self) -> None:
        """Game's main loop"""
        run = True
        setup_paddle_event_handlers()
        self.view.setup(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)
        while run:
            self.view.tick(FPS)
            player = self.process_model()
            self.process_user_input()
            self.render_view()

            # Handle score
            if player:  # if there is a score
                pygame.time.delay(500)
                if player.score >= WIN_SCORE:  # checks if player winned the game
                    self.render_victory_view(player)
                    pygame.time.delay(2000)
                    break

            if self.view.check_if_quit():
                run = False

        self.view.quit()


# ****************************************************************** #
# ************************ Render Functions ************************ #
# ****************************************************************** #


def render_background(color: Color):
    """Returns a function that renders the background"""

    def render(window: pygame.Surface) -> None:
        window.fill(color)

    return render


def render_mid_line(field_width: int, field_height: int, color: Color):
    """Returns a function that renders the field's mid line"""

    def render(window: pygame.Surface) -> None:
        for i in range(10, field_height, field_height // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(
                window,
                color,
                (field_width // 2 - 2, i, 4, field_height // 20),
            )

    return render


def render_ball(ball: Ball, color: Color):
    """Returns a function that renders the ball"""

    def render(window: pygame.Surface) -> None:
        pygame.draw.circle(
            window,
            color,
            (ball.x, ball.y),
            ball.radius,
        )

    return render


def render_paddle(paddle: Paddle, color: Color):
    """Returns a function that renders a paddle"""

    def render(window: pygame.Surface) -> None:
        pygame.draw.rect(
            window,
            color,
            (paddle.x, paddle.y, paddle.width, paddle.height),
        )

    return render


def render_score(x_loc: int, y_loc: int, player: Player):
    """Returns a function that renders the player score at location
    '(x_loc, y_loc)'"""

    def render(window: pygame.Surface):
        font = pygame.font.SysFont(*SCORE_FONT)
        text = font.render(
            f"{player.score}",
            True,
            SCORE_COLOR,
        )
        window.blit(
            text,
            (x_loc - text.get_width() // 2, y_loc),
        )

    return render


def render_victory(field_width: int, field_height: int, player: Player):
    """Returns a function that renders a victory message on the screen"""

    def render(window: pygame.Surface) -> None:
        font = pygame.font.SysFont(*MESSAGE_FONT)
        text = font.render(
            f"{player.name.capitalize()} Won!",
            True,
            MESSAGE_COLOR,
        )
        window.blit(
            text,
            (
                field_width // 2 - text.get_width() // 2,
                field_height // 2 - text.get_height() // 2,
            ),
        )

    return render
