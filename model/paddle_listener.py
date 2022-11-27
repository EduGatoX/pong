import controller.game_controller as game_controller
from event.event import subscribe, EventType
from model.paddle import Paddle


def handle_paddle_up(paddle: Paddle):
    paddle.move(-game_controller.PADDLE_DELTA_Y)


def handle_paddle_down(paddle: Paddle):
    paddle.move(game_controller.PADDLE_DELTA_Y)


def setup_paddle_event_handlers():
    subscribe(EventType.paddle_up, handle_paddle_up)
    subscribe(EventType.paddle_down, handle_paddle_down)
