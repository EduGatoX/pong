from typing import Protocol
import pygame

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

WINNING_SCORE = 5


class Drawable(Protocol):
    def draw(self, win):
        """Draws the drawable object on 'win'"""


class Ball:
    MAX_VEL = 10
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0


class Paddle:
    COLOR = WHITE
    VEL = 8

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, delta_y: int):
        """Move the paddle a distance of 'delta_y'"""
        self.y += delta_y

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


def draw(win, *drawables: Drawable, left_score, right_score):
    """Draw the drawables on 'win'"""
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (3 * WIDTH // 4 - right_score_text.get_width() // 2, 20))

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    for drawable in drawables:
        drawable.draw(win)
    pygame.display.update()


def handle_paddle_movement(keys, left_paddle: Paddle, right_paddle: Paddle):
    delta_y1 = 0
    delta_y2 = 0

    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        delta_y1 = -Paddle.VEL
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + left_paddle.VEL <= HEIGHT:
        delta_y1 = Paddle.VEL
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        delta_y2 = -Paddle.VEL
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + right_paddle.VEL <= HEIGHT:
        delta_y2 = Paddle.VEL

    left_paddle.move(delta_y1)
    right_paddle.move(delta_y2)


def handle_collision(ball: Ball, left_paddle: Paddle, right_paddle: Paddle) -> None:
    # Handling roof and ceiling collisions
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        # left paddle
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            # first check if the 'y' coordinate of the ball is within the 'y' coordinates
            # of the paddle
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                # The ball collide with the paddle
                # handle x_vel
                ball.x_vel *= -1
                # handle y_vel
                middle_y = left_paddle.y + left_paddle.height / 2
                delta_y = ball.y - middle_y
                ball.y_vel += ball.MAX_VEL * delta_y / left_paddle.height / 2
    else:
        # right paddle
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                # handle x_vel
                ball.x_vel *= -1
                # handle y_vel
                middle_y = right_paddle.y + right_paddle.height / 2
                delta_y = ball.y - middle_y
                ball.y_vel += ball.MAX_VEL * delta_y / right_paddle.height / 2


def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, left_paddle, right_paddle, ball, left_score=left_score, right_score=right_score)

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        #         break
        if pygame.event.get(pygame.QUIT):
            print("Quitting the game.")
            run = False

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Score
        if ball.x < 0:
            right_score += 1
            pygame.time.delay(500)
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            pygame.time.delay(500)
            ball.reset()

        # Winning
        won = False
        if left_score == WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score == WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            left_score = 0

    pygame.quit()


if __name__ == "__main__":
    main()
