import random
import arcade
import os

import star

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_LASER = 0.8
COIN_COUNT = 20

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space ship"

BULLET_SPEED = 5

class FallingShip(arcade.Sprite):
    def update(self):
        self.center_y -= 2
        if self.top < 0:
            self.bottom = SCREEN_HEIGHT

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

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AERO_BLUE)

    def level_1(self):
        for i in range(COIN_COUNT):

            coin = arcade.Sprite("images/Gold.png", SPRITE_SCALING_COIN)

            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120, SCREEN_HEIGHT)

            self.coin_list.append(coin)

    def level_2(self):
        for i in range(50):

            coin = FallingShip("images/mship4.png", SPRITE_SCALING_COIN)

            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120,SCREEN_HEIGHT)

            self.coin_list.append(coin)

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.star_list = set()

        self.score = 0
        self.level = 1
        self.total_time = 60

        self.player_sprite = arcade.Sprite("images/mship4.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)

        self.level_1()

        arcade.set_background_color((5, 2, 27))

        for _ in range(25):
            self.create_star()

    def on_draw(self):
        """
        Render the screen.
        """
        Y_TEXT_POSITION = 15
        TEXT_SIZE = 14
        arcade.start_render()

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

    def update(self, delta_time):
        """ Movement and game logic """
        self.total_time -= delta_time
        for star in self.star_list:
            star.x -= star.speed * delta_time
            if star.x < 0:
                star.reset_pos(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bullet_list.update()

        for bullet in self.bullet_list:

            hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)
            player_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

            if len(hit_list) > 0:
                bullet.kill()

            for coin in hit_list:
                coin.kill()
                self.score += 1

            if len(self.coin_list) == 0 and self.level == 1:
                self.level += 1
                self.level_2()

            if bullet.bottom > SCREEN_HEIGHT:
                bullet.kill()
