import pygame

class Pong(pygame.sprite.Sprite):
    """
    Play a game of Forever Alone Pong
    """

    def __init__(self, game_width=600, game_height=400, bg_color=(0,0,0), color_A=(255,255,80),
                 color_B=(200,60,180),
                 paddle_length=60, paddle_thickness=20, ball_width=20,
                 ball_starting_pos=None, divider_x=None, dash_length=8, dash_width=3
                 score_font=None):
        self.game_width, self.game_height = self.resolution = game_width, game_height
        self.bg_color = bg_color
        self.color_A, self.color_B = color_A, color_B
        self.paddle_length = paddle_length
        self.paddle_thickness = paddle_thickness
        self.score_font = pygame.font.Font(None, 32)
        self.ball_width=20
        self.ball_starting_pos = ball_starting_pos or (
            (game_width - ball_width)/2, (game_height - ball_width)/2)
        self.divider_x = game_width / 2
        self.dash_length = dash_length
        self.dash_width = 3

    def render_dash(self, surf):
        pass

    def main_loop(self):
        pass





