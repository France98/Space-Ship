import arcade

from spaceship import SpaceShip

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space"

def main():
    game = SpaceShip()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()