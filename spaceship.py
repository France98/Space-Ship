import random
import arcade
import os
from enum import Enum

import star

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_LASER = 0.8
COIN_COUNT = 20

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space ship"

BULLET_SPEED = 5

class GameStates(Enum):
    GAME_OVER = 0
    RUNNING = 1
    INTRO = 2

class SpaceShip(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.player_list = None
        self.coin_list = None
        self.bullet_list = None
        self.star_list = set()

        self.player_sprite = None
        self.score = 0
        self.level = 1
        self.total_time = 0.0
        self.state = None

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AERO_BLUE)

    def level_1(self):
        for i in range(COIN_COUNT):
            coin = arcade.Sprite("images/mship4.png", SPRITE_SCALING_COIN)

            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(200, SCREEN_HEIGHT)

            self.coin_list.append(coin)

    def level_2(self):
        self.total_time += 10
        for i in range(50):

            coin = arcade.Sprite("images/mship4.png", SPRITE_SCALING_COIN)

            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(200,SCREEN_HEIGHT)

            self.coin_list.append(coin)

    def draw_Intro(self):
        arcade.set_background_color((5, 2, 27))
        for star in self.star_list:
            star.draw()

        arcade.draw_text("Space Ship",
            SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 68,
            arcade.color.WHITE, 54,
            align="center", anchor_x="center", anchor_y="center"
        )

        arcade.draw_text("Press SPACE to restart",
            SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2),
            arcade.color.WHITE, 24,
            align="center", anchor_x="center", anchor_y="center"
        )


    def setup(self):
        """ Set up the game and initialize the variables. """

        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.star_list = set()
        self.state = GameStates.INTRO

        self.score = 0
        self.level = 1
        self.total_time = 31

        self.player_sprite = arcade.Sprite("images/mship4.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)

        self.level_1()

        arcade.set_background_color((5, 2, 27))

        for _ in range(25):
            self.create_star()

    def draw_game_over(self):
        arcade.set_background_color((5, 2, 27))
        arcade.draw_text("Time's up",
            SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 68,
            arcade.color.WHITE, 54,
            align="center", anchor_x="center", anchor_y="center"
        )

        arcade.draw_text("Press SPACE to restart",
            SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2),
            arcade.color.WHITE, 24,
            align="center", anchor_x="center", anchor_y="center"
        )
        self.total_time = 31
        self.score = 0
        self.level = 1

    def drawGame(self):
        Y_TEXT_POSITION = 15
        TEXT_SIZE = 14
        arcade.set_background_color((5, 2, 27))
        self.coin_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60

        for star in self.star_list:
            star.draw()

        arcade.draw_text(f"Score : {self.score}", 15,  Y_TEXT_POSITION, arcade.color.WHITE,  TEXT_SIZE)
        arcade.draw_text(f"Level: {self.level}", 10, 35, arcade.color.WHITE, 15)
        arcade.draw_text(f"Time : {minutes:02d}:{seconds:02d}", SCREEN_WIDTH - 15,  Y_TEXT_POSITION, arcade.color.WHITE,  TEXT_SIZE, align="right", anchor_x="right", anchor_y="baseline")

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        if self.state == GameStates.INTRO:
            self.draw_Intro()

        if self.state == GameStates.RUNNING:
            self.drawGame()
        
        if self.state == GameStates.GAME_OVER:
            self.draw_game_over()
            self.level = 1


    def create_star(self):
        self.star_list.add(star.Star(SCREEN_WIDTH, SCREEN_HEIGHT))

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):

        bullet = arcade.Sprite("images/Red_laser2.png", SPRITE_SCALING_LASER)

        bullet.angle = 90

        bullet.change_y = BULLET_SPEED

        bullet.center_x = self.player_sprite.center_x
        bullet.bottom = self.player_sprite.top

        self.bullet_list.append(bullet)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE and self.state == GameStates.INTRO:
            self.state = GameStates.RUNNING
        elif key == arcade.key.SPACE and self.state == GameStates.GAME_OVER:
            self.state = GameStates.RUNNING


    def update(self, delta_time):
        """ Movement and game logic """
        self.total_time -= delta_time
        for star in self.star_list:
            star.x -= star.speed * delta_time
            if star.x < 0:
                star.reset_pos(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bullet_list.update()
        
        if self.state == GameStates.RUNNING:
            for bullet in self.bullet_list:

                hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)

                if len(hit_list) > 0:
                    bullet.kill()

                for coin in hit_list:
                    coin.kill()
                    self.score += 1
                if self.state == GameStates.GAME_OVER:
                    self.drawGame()
                    self.level_1()
                if len(self.coin_list) == 0 and self.level == 1:
                    self.level += 1
                    self.level_2()
                if bullet.bottom > SCREEN_HEIGHT:
                    bullet.kill()
            if self.total_time <= 0:
                    self.state = GameStates.GAME_OVER
