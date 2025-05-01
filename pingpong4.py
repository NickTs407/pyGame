import pygame, sys

win_size = 800
bg_color = (200, 200, 200)
plat_h = 120
plat_w = 20
pl_color_l = (20, 250, 20)
pl_color_r = (250, 20, 20)
pl_color_u = (20, 20, 250)
pl_color_d = (0, 0, 0)
pl_speed = 0.5
ball_radius = 15
ball_color = (250, 250, 250)
ball_speed = 0.05


class PingPong:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((win_size, win_size))
        pygame.display.set_caption("Ping Pong 4")
        self.left_pl = Platform(self, 0, win_size//2, plat_w, plat_h)
        self.right_pl = Platform(self, win_size-plat_w, win_size//2, plat_w, plat_h)
        self.up_pl = Platform(self, win_size//2, 0, plat_h, plat_w)
        self.down_pl = Platform(self, win_size//2, win_size-plat_w, plat_h, plat_w)
        self.ball = Ball(self)
        self.left_player_score = 0
        self.right_player_score = 0
        self.up_player_score = 0
        self.down_player_score = 0

    def display_update(self):
        self.screen.fill((bg_color))
        self.left_pl.platform_update(pl_color_l)
        self.right_pl.platform_update(pl_color_r)
        self.up_pl.platform_update(pl_color_u)
        self.down_pl.platform_update(pl_color_d)
        self.ball.update_ball(ball_color)
        # self.draw_score(self.screen, self.left_player_score, self.right_player_score)
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
                elif event.key == pygame.K_r:
                    self.up_pl.move_left = True
                elif event.key == pygame.K_t:
                    self.up_pl.move_right = True
                elif event.key == pygame.K_v:
                    self.down_pl.move_left = True
                elif event.key == pygame.K_b:
                    self.down_pl.move_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.left_pl.move_up = False
                elif event.key == pygame.K_s:
                    self.left_pl.move_down = False
                elif event.key == pygame.K_o:
                    self.right_pl.move_up = False
                elif event.key == pygame.K_l:
                    self.right_pl.move_down = False
                elif event.key == pygame.K_r:
                    self.up_pl.move_left = False
                elif event.key == pygame.K_t:
                    self.up_pl.move_right = False
                elif event.key == pygame.K_v:
                    self.down_pl.move_left = False
                elif event.key == pygame.K_b:
                    self.down_pl.move_right = False

    def run(self):
        while True:
            self.check_event()
            self.display_update()

class Platform:
    def __init__(self, pgame, x_rect, y_rect, pl_w, pl_h):
        self.screen = pgame.screen
        self.screen_rect = pgame.screen.get_rect()
        self.rect = pygame.Rect(0, 0, pl_w, pl_h)
        self.rect.x = x_rect
        self.rect.y = y_rect
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

    def platform_update(self, pl_color):
        if self.move_up and self.rect.top > 0:
            self.y -= pl_speed
        if self.move_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += pl_speed
        if self.move_left and self.rect.left > 0:
            self.x -= pl_speed
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += pl_speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        pygame.draw.rect(self.screen, pl_color, self.rect)

class Ball:
    def __init__(self, pgame):
        self.screen = pgame.screen
        self.screen_rect = pgame.screen.get_rect()
        self.pgame = pgame
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(0, 0, ball_radius*2, ball_radius*2)
        self.rect.center = (win_size // 2, win_size // 2)
        self.rect.x = win_size // 2
        self.rect.y = win_size // 2
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vx = 1
        self.vy = 1

    def update_ball(self, b_color):
        self.x += self.vx * ball_speed
        self.y += self.vy * ball_speed
        self.rect.x = self.x
        self.rect.y = self.y
        if self.rect.colliderect(self.pgame.left_pl.rect):
            if self.vx < 0:
                self.vx *= -1
        if self.rect.colliderect(self.pgame.right_pl.rect):
            if self.vx > 0:
                self.vx *= -1
        if self.rect.colliderect(self.pgame.up_pl.rect):
            if self.vy < 0:
                self.vy *= -1
        if self.rect.colliderect(self.pgame.down_pl.rect):
            if self.vy > 0:
                self.vy *= -1
        if self.rect.left < 0:
            self.reset()
            self.pgame.right_player_score += 1
            self.vx = 1
        if self.rect.right > win_size:
            self.reset()
            self.pgame.left_player_score += 1
            self.vx = -1
        if self.rect.top < 0:
            self.reset()
            self.pgame.up_player_score += 1
            self.vy = 1
        if self.rect.bottom > win_size:
            self.reset()
            self.pgame.down_player_score += 1
            self.vy = -1
        pygame.draw.circle(self.screen, b_color, (self.x, self.y), ball_radius)


if __name__ == '__main__':
    pp = PingPong()
    pp.run()
