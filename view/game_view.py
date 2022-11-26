import pygame
from typing import Callable

# A function that takes a Surface as argument and performs a rendering into it.
RenderFunction = Callable[[pygame.Surface], None]


class GameView:
    """
    Class responsible for managing what is rendered on the screen.
    """

    def setup(self, window_name: str, window_width: int, window_height: int):
        pygame.init()
        self.window = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(window_name)

    def tick(self, fps: int) -> None:
        """Sets the framerate of the window"""
        self.clock.tick(fps)

    def render(self, *render_fns: RenderFunction) -> None:
        """Renders into self.window whatever comes inside render_fn"""
        for render_fn in render_fns:
            render_fn(self.window)

    def update(self) -> None:
        """Updates the window"""
        pygame.display.update()

    def check_if_quit(self) -> bool:
        """Returns True if the event of quitting has been created,
        False if not."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def quit(self) -> None:
        """Quits the program"""
        pygame.quit()
