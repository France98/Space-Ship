import arcade

from audition import AuditionWindow

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space"

def main():
    game = AuditionWindow()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()