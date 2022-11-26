from view.game_view import GameView
from model.game_model import GameModel
from controller.game_controller import GameController

FIELD_WIDTH, FIELD_HEIGHT = 700, 500


def main():
    model = GameModel(FIELD_WIDTH, FIELD_HEIGHT)
    view = GameView()
    controller = GameController(model, view)
    controller.mainloop()


if __name__ == "__main__":
    main()
