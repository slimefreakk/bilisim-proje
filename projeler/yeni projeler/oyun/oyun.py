#kodun çalışması için pygame gereklidir
#pip install pygame (komut istemcisine yazın)
#dosyanın yanında pop.wav dosyası olursa oyun içi ses olur
#selim haftacıoğulları ve mert tangül tarafından yapılmıştır


import pygame
import random
import sys
import time

# Başlat
pygame.init()
pygame.mixer.init()

# Ekran
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Selimin Zıplayan Topları")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)

# Font
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

# Ses efekti
try:
    pop_sound = pygame.mixer.Sound("pop.wav")
except:
    pop_sound = None

# Virüs türleri: (renk, boyut, hız)
virus_types = [
    (RED, 30, 4),
    (GREEN, 25, 5),
    (YELLOW, 20, 6),
    (PURPLE, 35, 3),
]

# Ana Menü
def menu():
    selected_mode = "normal"
    while True:
        win.fill(WHITE)
        title = big_font.render("Selimin Zıplayan Topları", True, BLACK)
        normal_btn = font.render("1 - Normal Mod", True, GREEN if selected_mode == "normal" else BLACK)
        hard_btn = font.render("2 - Zor Mod", True, RED if selected_mode == "hard" else BLACK)
        start_btn = font.render("Enter - Başla", True, BLUE)

        win.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        win.blit(normal_btn, (WIDTH//2 - 80, 150))
        win.blit(hard_btn, (WIDTH//2 - 80, 190))
        win.blit(start_btn, (WIDTH//2 - 80, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_mode = "normal"
                elif event.key == pygame.K_2:
                    selected_mode = "hard"
                elif event.key == pygame.K_RETURN:
                    return selected_mode

# Virüs oluşturma
def create_virus(difficulty):
    virus = random.choice(virus_types)
    color, size, base_speed = virus
    speed = base_speed if difficulty == "normal" else base_speed + 3
    pos = [random.randint(0, WIDTH - size), random.randint(0, HEIGHT - size)]
    vel = [random.choice([-speed, speed]), random.choice([-speed, speed])]
    return {"color": color, "size": size, "pos": pos, "vel": vel}

# Oyun Fonksiyonu
def run_game(difficulty="normal"):
    player_size = 40
    player_pos = [WIDTH // 2, HEIGHT // 2]
    player_rect = pygame.Rect(*player_pos, player_size, player_size)

    virus = create_virus(difficulty)

    score = 0
    lives = 3

    clock = pygame.time.Clock()

    # Can azalması için sayaç ayarı
    kill_timer_start = time.time()
    kill_interval = 5  # saniye

    run = True
    while run:
        clock.tick(30)
        win.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        speed = 5
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= speed
        if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
            player_pos[1] += speed

        player_rect.topleft = player_pos

        # Virüs hareketi
        virus["pos"][0] += virus["vel"][0]
        virus["pos"][1] += virus["vel"][1]

        if virus["pos"][0] <= 0 or virus["pos"][0] >= WIDTH - virus["size"]:
            virus["vel"][0] *= -1
        if virus["pos"][1] <= 0 or virus["pos"][1] >= HEIGHT - virus["size"]:
            virus["vel"][1] *= -1

        # Virüsün rect'i
        virus_rect = pygame.Rect(virus["pos"][0], virus["pos"][1], virus["size"], virus["size"])

        # Çarpışma: oyuncu - virüs
        if player_rect.colliderect(virus_rect):
            score += 1
            if pop_sound:
                pop_sound.play()
            virus = create_virus(difficulty)
            kill_timer_start = time.time()  # Virüs öldü, sayacı sıfırla

        # Can azalması için süre kontrolü
        elapsed = time.time() - kill_timer_start
        time_left = max(0, kill_interval - elapsed)

        if elapsed >= kill_interval:
            lives -= 1
            kill_timer_start = time.time()  # Sayacı resetle

        if lives <= 0:
            run = False

        # Çizimler
        pygame.draw.rect(win, BLUE, (*player_pos, player_size, player_size))
        pygame.draw.circle(win, virus["color"], (virus["pos"][0] + virus["size"] // 2, virus["pos"][1] + virus["size"] // 2), virus["size"] // 2)

        score_text = font.render(f"Skor: {score}", True, BLACK)
        lives_text = font.render(f"Can: {int(lives)}", True, BLACK)
        timer_text = font.render(f"Son Virüse Kalan Süre: {time_left:.1f}s", True, RED if time_left <= 2 else BLACK)

        win.blit(score_text, (10, 10))
        win.blit(lives_text, (10, 40))
        win.blit(timer_text, (WIDTH - 250, 10))

        pygame.display.update()

    return score, int(lives)

# Bitiş Ekranı
def show_end_screen(score, lives):
    win.fill(WHITE)
    text1 = big_font.render(f"Oyun Bitti!", True, BLACK)
    text2 = font.render(f"Toplam Skor: {score}", True, BLACK)
    text3 = font.render(f"Kalan Can: {lives}", True, BLACK)
    win.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 120))
    win.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 170))
    win.blit(text3, (WIDTH // 2 - text3.get_width() // 2, 210))
    pygame.display.update()
    pygame.time.delay(4000)

# Ana Akış
while True:
    mode = menu()
    score, lives = run_game(mode)
    show_end_screen(score, lives)
