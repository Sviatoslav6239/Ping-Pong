from random import choice

from pygame import *
init()
font.init()


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        virtual_surface.blit(self.image, (self.rect.x, self.rect.y))


class Ball(GameSprite):
    def __init__(self):
        super().__init__("images/ball.png", (WIDTH - 50) // 2, (HEIGHT - 50) // 2, 50, 50, 10)
        self.speed_x = self.speed
        self.speed_y = self.speed
        self.disable_frames = 60
        self.disable = True

    def update(self, left_racket, right_racket):
        if not self.disable:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            if self.rect.y >= HEIGHT - self.rect.height:
                self.speed_y *= -1
            if self.rect.y < 0:
                self.speed_y *= -1

            if sprite.collide_rect(right_racket, ball):
                self.speed_x *= -1.1
                self.rect.x = right_racket.rect.x - self.rect.width
            if sprite.collide_rect(left_racket, ball):
                self.speed_x *= -1.1
                self.rect.x = left_racket.rect.right

            if ball.rect > WIDTH:
                self.respawn()
                self.update_score(left_racket.score)

            if ball.rect.x < -self.rect.w:
                self.respawn()
                self.update_score(right_racket.score)

        else:
            self.disable_frames -= 1
            if self.disable_frames <= 0:
                self.remove_disable()

    def respawn(self):
        self.rect.x = (WIDTH - 50) // 2
        self.rect.y = (HEIGHT - 50) // 2
        self.speed_x = choice((-self.speed, self.speed))
        self.speed_y = choice((-self.speed, self.speed))

    def set_disable(self):
        self.disable = True
        self.disable_frames = 60

    def remove_disable(self):
        self.disable = False

    def update_score(self, score):
        score.inscrease_score(1)

class Player(GameSprite):
    def __init__(self, player_number):
        self.width = 150
        self.player_number = player_number
        if self.player_number == 1:
            self.image_name = "images/Line.png"
            self.x = 100
            self.score = Score(WIDTH // 3, HEIGHT // 20)
        elif self.player_number == 2:
            self.image_name = "images/Line2.png"
            self.x = WIDTH - 100 - 150
            self.score = Score(WIDTH - WIDTH // 3, HEIGHT // 20)
        super().__init__(self.image_name, self.x, (HEIGHT - 150) // 2, self.width, self.width, 15)

    def update(self):
        keys_pressed = key.get_pressed()
        if self.player_number == 1:
            if keys_pressed[K_w] and self.rect.y >= 10:
                self.rect.y -= self.speed
            if keys_pressed[K_s] and self.rect.y <= HEIGHT - self.rect.height - 10:
                self.rect.y += self.speed

        if self.player_number == 2:
            if keys_pressed[K_UP] and self.rect.y >= 10:
                self.rect.y -= self.speed
                if keys_pressed[K_DOWN] and self.rect.y <= HEIGHT - self.rect.height - 10:
                    self.rect.y += self.speed



class Score:
    def __init__(self, x, y):
        self.font = font.Font(None, 60)
        self.x = x
        self.y = y
        self.num = 0
        self.text = str(self.num)
        self.image = self.font.render(self.text, True, (0, 0, 0))

    def inscrease_score(self, amount):
        self.num += amount
        self.text = str(self.num)
        self.image = self.font.render(self.text, True, (0, 0, 0))

    def drop_score(self):
        self.num = 0
        self.text = str(self.num)
        self.image = self.font.render(self.text, True, (0, 0, 0))

    def reset(self, surface):
        surface.blit(self.image, (self.x, self.y))


    def restart(self):
        ball.respawn()
        player1.score.drop_score()
        player2.score.drop_score()
        player1.rect.y = (HEIGHT - 150) // 2
        player2.rect.y = (HEIGHT - 150) // 2



WIDTH = 1280
HEIGHT = 720
ASPECT_RATIO = WIDTH / HEIGHT

FPS = 60

window = display.set_mode((WIDTH, HEIGHT), RESIZABLE)
clock = time.Clock()

virtual_surface = Surface((WIDTH, HEIGHT))
current_size = window.get_size()

ball = Ball()

player1 = Player(1)
player2 = Player(2)

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == VIDEORESIZE:
            new_width = e.w
            new_height = int(new_width / ASPECT_RATIO)
            window = display.set_mode((new_width, new_height), RESIZABLE)
            current_size = window.get_size()

    virtual_surface.fill((139, 180, 228))

    ball.reset()
    ball.update(player1, player2)


    player1.reset()
    player1.update()

    player2.reset()
    player2.update()

    player1.score.reset(virtual_surface)
    player2.score.reset(virtual_surface)

    scaled_surface = transform.scale(virtual_surface, current_size)
    window.blit(scaled_surface, (0, 0))
    display.update()
    clock.tick(FPS)
