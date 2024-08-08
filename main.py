import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
screen_width = 800
screen_height = 600

# Couleurs
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# Classes du jeu
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed = -self.speed
            self.rect.y += 30

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -5

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Groupes de sprites
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Création du joueur
player = Player()
all_sprites.add(player)

# Création des aliens
for row in range(5):
    for col in range(10):
        alien = Alien(col * 50 + 20, row * 40 + 20)
        all_sprites.add(alien)
        aliens.add(alien)

# Variables de jeu
score = 0
font = pygame.font.SysFont(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Boucle de jeu
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if event.key == pygame.K_r and game_over:
                # Réinitialiser le jeu
                game_over = False
                score = 0
                player.rect.centerx = screen_width // 2
                player.rect.bottom = screen_height - 10
                aliens.empty()
                for row in range(5):
                    for col in range(10):
                        alien = Alien(col * 50 + 20, row * 40 + 20)
                        all_sprites.add(alien)
                        aliens.add(alien)

    # Mettre à jour les sprites
    if not game_over:
        all_sprites.update()

        # Vérifier les collisions
        hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for hit in hits:
            score += 10

        # Vérifier les conditions de victoire et de défaite
        if not aliens:
            game_over = True
            victory = True
        for alien in aliens:
            if alien.rect.bottom >= screen_height:
                game_over = True
                victory = False

    # Affichage
    screen.fill(black)
    all_sprites.draw(screen)
    draw_text(f'Score: {score}', font, white, screen, 10, 10)
    
    if game_over:
        if victory:
            draw_text('VICTOIRE!', font, white, screen, screen_width // 2 - 80, screen_height // 2)
        else:
            draw_text('DEFAITE!', font, white, screen, screen_width // 2 - 80, screen_height // 2)
        draw_text('Appuyez sur R pour recommencer', font, white, screen, screen_width // 2 - 150, screen_height // 2 + 50)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
