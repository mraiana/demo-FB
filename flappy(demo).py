from pygame import *
from random import randint

width = 700
height = 500
finish = False
clock = time.Clock()
FPS = 60

# окно
window = display.set_mode((width, height))
display.set_caption('Flappy Bird')
background = transform.scale(image.load("background.png"), (width, height))


# классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (90, 85))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_SPACE] and self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed * 2 if self.rect.y < height - 150 else 0  # Gravity


class Pipe(GameSprite):
    def __init__(self, pipe_image, pipe_x, pipe_y, pipe_speed):
        super().__init__(pipe_image, pipe_x, pipe_y, pipe_speed)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -50:
            self.rect.x = width
            self.rect.y = randint(100, height - 200)

#спрайты
player = Player("flappy.png", 100, height // 2, 5)
pipes = [Pipe("pipe.png", width + i * 300, randint(100, height - 200), 5) for i in range(2)]

font.init()
font = font.Font(None, 70)
score = 0

def display_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        for pipe in pipes:
            pipe.update()
            pipe.reset()
            if player.rect.colliderect(pipe.rect):
                finish = True

            if pipe.rect.x == player.rect.x:
                score += 1


        if finish != True:
            window.blit(background,(0, 0))

            player.update()
            player.reset()


        display_score()

        if pipes[-1].rect.x < width - 200:
            pipes.append(Pipe("pipe.png", width, randint(100, height - 200), 5))

        if player.rect.y > height - 150:
            finish = True

    display.update()
    clock.tick(FPS)
