import random
from dataclasses import dataclass
import pygame
import math

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 120
NUM_SQUARES = 3
SIZE_MIN = 20
SIZE_MAX = 70
SPEED_MIN = 60
GLOBAL_MAX_SPEED = 480 
COLOR_BG = (24, 24, 32)
COLOR_FPS = (245, 245, 245)
FPS_TEXT_POS = (10, 10)

@dataclass
class Square:
    rect: pygame.Rect
    vx: float
    vy: float
    px: float 
    py: float
    size: int
    color: tuple[int, int, int]
    death_time: int

    def update(self, width: int, height: int, dt: float) -> bool:
        self.px += self.vx * dt
        self.py += self.vy * dt
        
        self.rect.x = int(self.px)
        self.rect.y = int(self.py)

        if self.rect.left <= 0 or self.rect.right >= width:
            self.vx *= -1
            self.px = max(0, min(self.px, width - self.size))
            self.rect.x = int(self.px)

        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.vy *= -1
            self.py = max(0, min(self.py, height - self.size))
            self.rect.y = int(self.py)
            
        return pygame.time.get_ticks() < self.death_time

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

def random_square(existing: list[Square]) -> Square:
    size = random.randint(SIZE_MIN, SIZE_MAX)
    
    size_factor = (size - SIZE_MIN) / (SIZE_MAX - SIZE_MIN)
    local_max = int(GLOBAL_MAX_SPEED - (size_factor * (GLOBAL_MAX_SPEED - SPEED_MIN)))
    local_max = max(SPEED_MIN, local_max)   

    death_time = pygame.time.get_ticks() + (random.randint(10, 30) * 1000)

    for _ in range(300):
        x = random.randint(0, WINDOW_WIDTH - size)
        y = random.randint(0, WINDOW_HEIGHT - size)
        rect = pygame.Rect(x, y, size, size)
        
        if not any(rect.colliderect(s.rect) for s in existing):
            return Square(
                rect=rect,
                vx=random.choice([-1, 1]) * random.randint(SPEED_MIN, local_max),
                vy=random.choice([-1, 1]) * random.randint(SPEED_MIN, local_max),
                px=float(x),
                py=float(y),
                size=size,
                color=(random.randint(60, 255), random.randint(60, 255), random.randint(60, 255)),
                death_time=death_time
            )

    return Square(
        rect=pygame.Rect(0, 0, SIZE_MIN, SIZE_MIN),
        vx=SPEED_MIN, vy=SPEED_MIN, px=0.0, py=0.0,
        size=SIZE_MIN, color=(200, 200, 200),
        death_time=pygame.time.get_ticks() + 5000
    )

def resolve_square_collisions(squares: list[Square]) -> None:
    pass

def apply_flee_behavior(squares: list[Square], dt: float, danger_radius: int = 180):
    FLEE_FORCE = 1000.0 
    CHASE_FORCE = 1000.0

    for current in squares:
        dx_flee, dy_flee = 0.0, 0.0
        dx_chase, dy_chase = 0.0, 0.0
        has_threat = False
        has_target = False

        for other in squares:
            if other is current:
                continue

            dx = other.rect.centerx - current.rect.centerx
            dy = other.rect.centery - current.rect.centery
            dist = math.hypot(dx, dy)

            if 0 < dist < danger_radius:
                nx = dx / dist
                ny = dy / dist
                
                if other.size > current.size:
                    dx_flee -= nx
                    dy_flee -= ny
                    has_threat = True
                
                elif other.size < current.size:
                    dx_chase += nx
                    dy_chase += ny
                    has_target = True

        if has_threat:
            current.vx += (dx_flee + random.uniform(-0.5, 0.5)) * FLEE_FORCE * dt
            current.vy += (dy_flee + random.uniform(-0.5, 0.5)) * FLEE_FORCE * dt
            
        if has_target:
            current.vx += (dx_chase + random.uniform(-0.2, 0.2)) * CHASE_FORCE * dt
            current.vy += (dy_chase + random.uniform(-0.2, 0.2)) * CHASE_FORCE * dt

        size_factor = (current.size - SIZE_MIN) / (SIZE_MAX - SIZE_MIN)
        local_max = GLOBAL_MAX_SPEED - (size_factor * (GLOBAL_MAX_SPEED - SPEED_MIN))
        local_max = max(SPEED_MIN, local_max)

        mag = math.hypot(current.vx, current.vy)
        if mag > local_max:
            current.vx = (current.vx / mag) * local_max
            current.vy = (current.vy / mag) * local_max
            
def create_squares() -> list[Square]:
    squares: list[Square] = []
    for _ in range(NUM_SQUARES):
        squares.append(random_square(squares))
    return squares

def draw_fps(surface: pygame.Surface, font: pygame.font.Font, clock: pygame.time.Clock) -> None:
    fps_value = int(clock.get_fps())
    fps_surface = font.render(f"FPS: {fps_value}", True, COLOR_FPS)
    surface.blit(fps_surface, FPS_TEXT_POS)

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Bouncing Squares")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    squares = create_squares()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        alive_squares = []
        for square in squares:
            if square.update(WINDOW_WIDTH, WINDOW_HEIGHT, dt):
                alive_squares.append(square)
            else:
                alive_squares.append(random_square(alive_squares))
        
        squares = alive_squares

        resolve_square_collisions(squares)
        apply_flee_behavior(squares, dt)
        
        screen.fill(COLOR_BG)
        for square in squares:
            square.draw(screen)
        draw_fps(screen, font, clock)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()