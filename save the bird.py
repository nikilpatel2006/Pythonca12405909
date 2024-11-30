import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400

# Game constants
GRAVITY = 0.5
JUMP_VELOCITY = -10
GROUND_HEIGHT = SCREEN_HEIGHT - 50
PIPE_SPEED = 5
OPPONENT_SPEED = 6
GAP = 120

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("save the bird")
clock = pygame.time.Clock() 

# Load and resize your assets here
def load_image(path, width, height):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (width, height))

# Customize these paths with your asset file paths
bird_img = load_image("bird2.png", 40, 40)
cactus_img = load_image("cactus.png", 30, 50)
pipe_img = load_image("pipe12.png ", 50, 200)
opponent_bird_img = load_image("eagle2.png", 40, 40)
background_img = load_image("sunset2.png", SCREEN_WIDTH, SCREEN_HEIGHT)

# Bird Class
class Bird:
    def __init__(self):
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT // 2
        self.velocity_y = 0

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.y < 0 or self.rect.y > GROUND_HEIGHT - self.rect.height:
            return False  # Bird dies if it touches ground or top
        return True

    def jump(self):
        self.velocity_y = JUMP_VELOCITY

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Obstacle Classes
class Cactus:
    def __init__(self, x):
        self.image = cactus_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = GROUND_HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_WIDTH + random.randint(200, 400)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Pipe:
    def __init__(self, x):
        self.image = pipe_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.randint(-150, -50)

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_WIDTH + random.randint(200, 400)
            self.rect.y = random.randint(-150, -50)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class OpponentBird:
    def __init__(self, x):
        self.image = opponent_bird_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = random.randint(50, GROUND_HEIGHT // 2)

    def update(self):
        self.rect.x -= OPPONENT_SPEED
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_WIDTH + random.randint(300, 500)
            self.rect.y = random.randint(50, GROUND_HEIGHT // 2)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Main Game Loop
def main():
    bird = Bird()
    cacti = [Cactus(SCREEN_WIDTH + i * 300) for i in range(3)]
    pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(3)]
    opponent_birds = [OpponentBird(SCREEN_WIDTH + i * 400) for i in range(2)]

    ground = pygame.Rect(0, GROUND_HEIGHT, SCREEN_WIDTH, 10)
    running = True
    score = 0
    last_score_update = pygame.time.get_ticks()

    while running:
        screen.blit(background_img, (0, 0))  # Draw background
        pygame.draw.rect(screen, (139, 69, 19), ground)  # Draw ground

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Update game objects
        if not bird.update():
            print("Game Over!")
            running = False

        for cactus in cacti:
            cactus.update()
            if bird.rect.colliderect(cactus.rect):
                print("Game Over!")
                running = False

        for pipe in pipes:
            pipe.update()
            if bird.rect.colliderect(pipe.rect):
                print("Game Over!")
                running = False

        for opponent_bird in opponent_birds:
            opponent_bird.update()
            if bird.rect.colliderect(opponent_bird.rect):
                print("Game Over!")
                running = False

        # Draw game objects
        bird.draw(screen)
        for cactus in cacti: 
            cactus.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)
        for opponent_bird in opponent_birds:
            opponent_bird.draw(screen)

        # Update and display score
        current_time = pygame.time.get_ticks()
        if current_time - last_score_update > 1000:  # Update score every 1000ms
            score += 1
            last_score_update = current_time

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Refresh display and set frame rate
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()