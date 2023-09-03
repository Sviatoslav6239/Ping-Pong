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


class Player(GameSprite):
    def __init__(self, player_number):
        self.width = 150
        self.player_number = player_number
        if self.player_number == 1:
            self.image_name = "images/Line.png"
            self.x = 100
        elif self.player_number == 2:
            self.image_name = "images/Line.png"
            self.x = WIDTH - 100 - 150
        super().__init__(self.image_name, self.x, (HEIGHT - 150) // 2, self.width, self.width, 15)


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
finish  = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == VIDEORESIZE:
            new_width = e.w
            new_height = int(new_width / ASPECT_RATIO )
            window = display.set_mode((new_width, new_height), RESIZABLE)
            current_size = window.get_size()

    virtual_surface.fill((139, 180, 228))

    ball.reset()

    player1.reset()
    player2.reset()

    scaled_surface = transform.scale(virtual_surface, current_size)
    window.blit(scaled_surface, (0, 0))
    display.update()
    clock.tick(FPS)








