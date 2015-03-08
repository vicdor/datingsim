import pygame

class Pong(pygame.sprite.Sprite):
    """
    Play a game of Forever Alone Pong
    """

    def __init__(self, game_width=600, game_height=400, bg_color=(0,50,0), color_A=(255,255,80),
                 color_B=(200,60,180), color_C=(130,255,255),
                 paddle_pos = None,
                 paddle_length=90, paddle_thickness=20, ball_width=20, ball_vel=(8, 8),
                 ball_starting_pos=None, divider_x=None, dash_length=12, dash_width=3,
                 dash_spacing=8,
                 score_font=None):
        self.game_width, self.game_height = self.resolution = game_width, game_height
        self.image = pygame.Surface(self.resolution)
        self.bg_color = bg_color
        self.color_A, self.color_B, self.color_C = color_A, color_B, color_C
        self.paddle_pos = paddle_pos or [20, (game_height - paddle_length)/2]
        self.paddle_length = paddle_length
        self.paddle_thickness = paddle_thickness
        self.score_font = pygame.font.Font(None, 32)
        self.ball_width = ball_width
        self.ball_pos = list(ball_starting_pos or [
            (game_width - ball_width)/2, (game_height - ball_width)/2])
        self.ball_vel = list(ball_vel)
        self.divider_x = divider_x or game_width / 2
        self.dash_length = dash_length
        self.dash_width = dash_width
        self.dash_spacing = dash_spacing

    def render_dash(self):
        if (self.divider_x):
            left = self.divider_x - self.dash_width / 2
        else:
            left = (self.game_width - self.dash_width) / 2
        top = self.dash_spacing
        bot = top + self.dash_length + self.dash_spacing

        while bot < self.game_height:
            rect = pygame.Rect(left, top, self.dash_width, self.dash_length)
            pygame.draw.rect(self.image, self.color_C, rect)
            top, bot = bot, top + self.dash_length + self.dash_spacing

    def render_rect(self, pos, w, l, color):
        rect = pygame.Rect(pos[0], pos[1], w, l)
        pygame.draw.rect(self.image, self.color_A, rect)

    @property
    def ball_center(self):
        return self.ball_pos[0] + self.ball_width/2, self.ball_pos[1] + self.ball_width/2

    @property
    def paddle_center(self):
        return (self.paddle_pos[0] + self.paddle_thickness/2,
                self.paddle_pos[1] + self.paddle_length/2)

    def update(self):
        # move ball
        self.ball_pos[0] += self.ball_vel[0]
        self.ball_pos[1] += self.ball_vel[1]

        if self.ball_pos[1] < 0:
            self.ball_vel[1] *= -1
            self.ball_pos[1] *= -1
        elif self.ball_pos[1] + self.ball_width  > self.game_height:
            self.ball_vel[1] *= -1
            overflow = self.ball_pos[1] + self.ball_width - self.game_height
            self.ball_pos[1] = self.game_height - self.ball_width - overflow

        if self.ball_pos[0] < self.paddle_pos[0] + self.paddle_thickness:
            self.ball_vel[0] *= -1
            overflow = self.paddle_pos[0] + self.paddle_thickness - self.ball_pos[0]
            self.ball_pos[0] = self.paddle_pos[0] + self.paddle_thickness - overflow

        elif self.ball_pos[0] + self.ball_width  > self.game_width:
            self.ball_vel[0] *= -1
            overflow = self.ball_pos[0] + self.ball_width - self.game_width
            self.ball_pos[0] = self.game_width - self.ball_width - overflow


        # paddle ai
        cover_ratio = .6
        dy = self.ball_center[1] - self.paddle_center[1]
        self.paddle_pos[1] += dy * cover_ratio
        self.paddle_pos[1] = max(self.paddle_pos[1], 0)
        self.paddle_pos[1] = min(self.paddle_pos[1], self.game_height - self.paddle_length)

        self.image.fill(self.bg_color)
        self.render_dash()
        self.render_rect(self.paddle_pos, self.paddle_thickness, self.paddle_length,
                           self.color_B)
        self.render_rect(self.ball_pos, self.ball_width, self.ball_width, self.color_B)

    @staticmethod
    def test():
        pygame.init()
        pygame.display.set_caption("Pong test")
        pygame.display.set_mode([800, 600])
        surf = pygame.display.get_surface()
        pong = Pong()

        done = False
        while not done:
            for e in pygame.event.get():
                if e.type is pygame.QUIT:
                    done = True
            pong.update()
            surf.blit(pong.image, [100, 100])
            pygame.display.flip()
            pygame.time.wait(40)


if __name__ == '__main__':
    Pong.test()






