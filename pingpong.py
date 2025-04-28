import pygame, sys

win_h = 800
win_w = 1280
bg_color = (200, 200, 200)
pl_h = 150
pl_w = 20
pl_color_l = (20, 250, 20)
pl_color_r = (250, 20, 20)
pl_speed = 0.5
ball_radius = 10
ball_color = (250, 250, 250)
ball_speed = 0.2
left_player_score = 0
right_player_score = 0


class PingPong:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((win_w, win_h))
        pygame.display.set_caption("Ping Pong")
        self.left_pl = Platform(self, 0)
        self.right_pl = Platform(self, win_w-pl_w)
        self.ball = Ball(self)
        self.left_player_score = 0
        self.right_player_score = 0

    def draw_score(self, screen, left_score, right_score):
        font = pygame.font.SysFont(None, 72)
        score_text = f"{left_score} : {right_score}"
        text_surface = font.render(score_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(win_w // 2, 30))
        screen.blit(text_surface, text_rect)

    def display_update(self):
        self.screen.fill((bg_color))
        self.left_pl.platform_update(pl_color_l)
        self.right_pl.platform_update(pl_color_r)
        self.ball.update_ball(ball_color)
        self.draw_score(self.screen, self.left_player_score, self.right_player_score)
        pygame.display.flip()

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.left_pl.move_up = True
                elif event.key == pygame.K_s:
                    self.left_pl.move_down = True
                elif event.key == pygame.K_o:
                    self.right_pl.move_up = True
                elif event.key == pygame.K_l:
                    self.right_pl.move_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.left_pl.move_up = False
                elif event.key == pygame.K_s:
                    self.left_pl.move_down = False
                elif event.key == pygame.K_o:
                    self.right_pl.move_up = False
                elif event.key == pygame.K_l:
                    self.right_pl.move_down = False

    def run(self):
        while True:
            self.check_event()
            self.display_update()


class Platform:
    def __init__(self, pgame, x_rect):
        self.screen = pgame.screen
        self.screen_rect = pgame.screen.get_rect()
        self.rect = pygame.Rect(0, 0, pl_w, pl_h)
        self.rect.x = x_rect
        self.y = float(self.rect.y)
        self.move_up = False
        self.move_down = False

    def platform_update(self, pl_color):
        if self.move_up and self.rect.top > 0:
            self.y -= pl_speed
        if self.move_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += pl_speed
        self.rect.y = self.y
        pygame.draw.rect(self.screen, pl_color, self.rect)


class Ball:
    def __init__(self, pgame):
        self.screen = pgame.screen
        self.screen_rect = pgame.screen.get_rect()
        self.pgame = pgame
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(0, 0, ball_radius*2, ball_radius*2)
        self.rect.center = (win_w // 2, win_h // 2)
        self.rect.x = win_w // 2
        self.rect.y = win_h // 2
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vx = 1
        self.vy = 1

    def update_ball(self, b_color):
        self.x += self.vx * ball_speed
        self.y += self.vy * ball_speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.rect.top <= 0 or self.rect.bottom >= win_h:
            self.vy *= -1
        if self.rect.colliderect(self.pgame.left_pl.rect):
            if self.vx < 0:
                self.vx *= -1
        if self.rect.colliderect(self.pgame.right_pl.rect):
            if self.vx > 0:
                self.vx *= -1
        if self.rect.left <= 0:
            self.reset()
            self.pgame.right_player_score += 1
            self.vx = 1
        if self.rect.left >= win_w:
            self.reset()
            self.pgame.left_player_score += 1
            self.vx = -1
        pygame.draw.circle(self.screen, b_color, (self.x, self.y), ball_radius)


if __name__ == '__main__':
    pp = PingPong()
    pp.run()
