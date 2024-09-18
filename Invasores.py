import pygame
import random
import sys
import traceback
import logging

# Inicializa o Pygame
pygame.init()

# Configura a janela do jogo
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Invasores")

# Define as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Configurações do jogador
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5

# Configurações dos inimigos
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_SPEED = 2
ENEMY_SPAWN_RATE = 60  # Quadros entre o surgimento de inimigos

# Configurações dos meteoros
METEOR_WIDTH = 50
METEOR_HEIGHT = 50
METEOR_SPEED = 3
METEOR_SPAWN_RATE = 120  # Quadros entre o surgimento de meteoros

# Configurações dos projéteis
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
BULLET_SPEED = 7

# Carrega a imagem do jogador
player_image = pygame.image.load("yellship.png")
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
player = player_image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))

# Carrega as imagens dos inimigos
enemy_image = pygame.image.load("alien.png")
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Carrega as imagens dos meteoros
meteor_image = pygame.image.load("meteor.png")
meteor_image = pygame.transform.scale(meteor_image, (METEOR_WIDTH, METEOR_HEIGHT))
meteor = meteor_image.get_rect(topleft=(WIDTH // 2, -METEOR_HEIGHT))

# Objetos do jogo
enemies = []
meteors = []
bullets = []

# Variáveis do jogo
score = 0
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Configura o logging
logging.basicConfig(filename='game_log.txt', level=logging.ERROR)

def spawn_enemy():
    # Cria um novo inimigo em uma posição aleatória no topo da tela
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = -ENEMY_HEIGHT
    enemy = enemy_image.get_rect(topleft=(x, y))
    enemies.append(enemy)

def spawn_meteor():
    # Cria um novo meteoro em uma posição aleatória no topo da tela
    x = random.randint(0, WIDTH - METEOR_WIDTH)
    y = -METEOR_HEIGHT
    meteor = meteor_image.get_rect(topleft=(x, y))
    meteors.append(meteor)

def move_enemies():
    # Move os inimigos para baixo e remove os que saírem da tela
    for enemy in enemies:
        enemy.y += ENEMY_SPEED
        if enemy.top > HEIGHT:
            enemies.remove(enemy)

def move_meteors():
    # Move os meteoros para baixo e remove os que saírem da tela
    for meteor in meteors:
        meteor.y += METEOR_SPEED
        if meteor.top > HEIGHT:
            meteors.remove(meteor)

def shoot_bullet():
    # Cria um novo projétil na posição do jogador
    x = player.centerx - BULLET_WIDTH // 2
    y = player.top
    bullet = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)
    bullets.append(bullet)

def move_bullets():
    # Move os projéteis para cima e remove os que saírem da tela
    for bullet in bullets:
        bullet.y -= BULLET_SPEED
        if bullet.bottom < 0:
            bullets.remove(bullet)

def check_collisions():
    # Verifica colisões entre objetos do jogo
    global score
    for enemy in enemies[:]:
        if player.colliderect(enemy):
            return True
        for bullet in bullets[:]:
            if bullet.colliderect(enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10
    for meteor in meteors[:]:
        if player.colliderect(meteor):
            return True
        for bullet in bullets[:]:
            if bullet.colliderect(meteor):
                meteors.remove(meteor)
                bullets.remove(bullet)
                score += 20
    return False

def draw_objects():
    # Desenha todos os objetos do jogo na tela
    SCREEN.fill(BLACK)
    SCREEN.blit(player_image, player)
    for enemy in enemies:
        SCREEN.blit(enemy_image, enemy)
    for meteor in meteors:
        SCREEN.blit(meteor_image, meteor)
    for bullet in bullets:
        pygame.draw.rect(SCREEN, WHITE, bullet)
    score_text = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_text, (10, 10))
    pygame.display.flip()

def game_loop():
    # Loop principal do jogo
    global player
    game_over = False
    enemy_spawn_counter = 0

    try:
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Sai da função em vez de usar sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        shoot_bullet()

            # Movimento do jogador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += PLAYER_SPEED

            # Geração de inimigos
            enemy_spawn_counter += 1
            if enemy_spawn_counter >= ENEMY_SPAWN_RATE:
                spawn_enemy()
                enemy_spawn_counter = 0

            # Atualiza posições e verifica colisões
            move_enemies()
            move_bullets()
            game_over = check_collisions()
            draw_objects()
            clock.tick(60)

        # Exibe tela de game over
        game_over_text = font.render("Game Over", True, WHITE)
        SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    except Exception as e:
        # Registra erros no arquivo de log
        logging.error(f"Ocorreu um erro: {str(e)}")
        logging.error(traceback.format_exc())
        print(f"Ocorreu um erro. Verifique game_log.txt para detalhes.")
    finally:
        pygame.quit()

if __name__ == "__main__":
    try:
        game_loop()
    except Exception as e:
        # Registra erros no arquivo de log
        logging.error(f"Ocorreu um erro no main: {str(e)}")
        logging.error(traceback.format_exc())
        print(f"Ocorreu um erro. Verifique game_log.txt para detalhes.")
    finally:
        sys.exit()

