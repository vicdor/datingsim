import pygame


class TextBox(pygame.sprite.Sprite):
    containers = []
    debug = False

    def __init__(self, text, pos, size=(200,400), font=None,
                 font_color=(255,255,255), font_size=30, bg_color=None,
                 frame_color=None, line_spacing=2):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.font = font or pygame.font.Font(None, font_size)
        self.font_color = font_color
        self.font_size = font_size
        self.bg_color = bg_color
        self.frame_color = frame_color
        self.line_spacing = line_spacing
        self.render()

    def render(self):
        lines = self.make_lines(self.text)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        if self.bg_color:
            self.image.fill(self.bg_color)

        rend_pos = [0, 0]
        for line in lines:
            surf = self.font.render(line, False, self.font_color)
            self.image.blit(surf, rend_pos)
            rend_pos[1] += self.line_spacing + surf.get_rect().h

    def make_lines(self, text):
        """Divides a string into several lines of words so that it can be
        displayed in a box without overflow."""
        if text == '':
            return []
        elif text[0] == '\n':
            return [''] + self.make_lines(text[1:])
        elif '\n\n' in text:
            lines = []
            for s in text.split('\n\n'):
                lines += self.make_lines(s) + ['']
            if lines[-1]:
                lines = lines[:-1]
            return lines
        elif '\n' in text:
            lines = []
            for s in text.split('\n'):
                lines += self.make_lines(s)
            return lines
        else:
            lines = []
            curr_line = ""
            for word in text.split():
                proposed_line = curr_line + word
                proposed_width = self.font.size(proposed_line)[0]
                if proposed_width > self.rect.w:
                    if len(curr_line) == 0:
                        lines.append(word)
                    else:
                        lines.append(curr_line)
                        curr_line = word + ' '
                else:
                    curr_line = proposed_line + ' '
            if len(curr_line) > 0:
                lines.append(curr_line)
            return lines


    @staticmethod
    def test():
        pygame.init()
        pygame.display.set_caption("TextBox")
        global GAME_WIDTH, GAME_HEIGHT, GAME_SIZE, screen
        GAME_WIDTH, GAME_HEIGHT = GAME_SIZE = (800, 600)
        screen = pygame.display.set_mode(GAME_SIZE)


        all_sprites = pygame.sprite.Group()
        TextBox.containers = all_sprites
        TextBox("Once upon a time there lived a great wizard named Boz.",
                        pos=(0,0), bg_color=(23, 155, 12))
        text = ("\n"
                "Duhduhduhduhdeeejaay\n"
                "Rockafeller runs this town\n"
                "we\n"
                "gonna\n\n"
                "run this town")
        TextBox(text, pos=(300,30), bg_color=(60,30,180))

        done = False
        while not done:
            for e in pygame.event.get():
                if e.type is pygame.QUIT:
                    done = True

            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()
            pygame.time.wait(1000//20)

if __name__ == '__main__':
    TextBox.test()
