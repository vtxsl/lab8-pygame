import random
from dataclasses import dataclass
import pygame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 120
NUM_SQUARES = 15
SIZE_MIN = 20
SIZE_MAX = 70
SPEED_MIN = 1
GLOBAL_MAX_SPEED = 8
COLOR_BG = (24, 24, 32)
COLOR_FPS = (245, 245, 245)
FPS_TEXT_POS = (10, 10)

@dataclass
class Square:
    rect: pygame.Rect
    vx: int
    vy: int
    size: int
    color: tuple[int, int, int]

    def update(self, width: int, height: int) -> None:
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= width:
            self.vx *= -1
            self.rect.left = max(0, self.rect.left)
            self.rect.right = min(width, self.rect.right)

        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.vy *= -1
            self.rect.top = max(0, self.rect.top)
            self.rect.bottom = min(height, self.rect.bottom)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

def random_square(existing: list[Square]) -> Square:
    size = random.randint(SIZE_MIN, SIZE_MAX)
    
    size_factor = (size - SIZE_MIN) / (SIZE_MAX - SIZE_MIN)
    local_max = int(GLOBAL_MAX_SPEED - (size_factor * (GLOBAL_MAX_SPEED - SPEED_MIN)))
    local_max = max(SPEED_MIN, local_max)   

    for _ in range(300):
        rect = pygame.Rect(
            random.randint(0, WINDOW_WIDTH - size),
            random.randint(0, WINDOW_HEIGHT - size),
            size,
            size,
        )
        if not any(rect.colliderect(s.rect) for s in existing):
            return Square(
                rect=rect,
                vx=random.choice([-1, 1]) * random.randint(SPEED_MIN, local_max),
                vy=random.choice([-1, 1]) * random.randint(SPEED_MIN, local_max),
                size=size,
                color=(random.randint(60, 255), random.randint(60, 255), random.randint(60, 255)),
            )

    return Square(
        rect=pygame.Rect(0, 0, SIZE_MIN, SIZE_MIN),
        vx=SPEED_MIN,
        vy=SPEED_MIN,
        size=SIZE_MIN,
        color=(200, 200, 200),
    )

def resolve_square_collisions(squares: list[Square]) -> None:
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            first = squares[i]
            second = squares[j]

            if not first.rect.colliderect(second.rect):
                continue

            overlap_x = min(first.rect.right, second.rect.right) - max(first.rect.left, second.rect.left)
            overlap_y = min(first.rect.bottom, second.rect.bottom) - max(first.rect.top, second.rect.top)

            first.vx, second.vx = second.vx, first.vx
            first.vy, second.vy = second.vy, first.vy

            if overlap_x < overlap_y:
                if first.rect.centerx < second.rect.centerx:
                    first.rect.x -= overlap_x // 2
                    second.rect.x += overlap_x - overlap_x // 2
                else:
                    first.rect.x += overlap_x - overlap_x // 2
                    second.rect.x -= overlap_x // 2
            else:
                if first.rect.centery < second.rect.centery:
                    first.rect.y -= overlap_y // 2
                    second.rect.y += overlap_y - overlap_y // 2
                else:
                    first.rect.y += overlap_y - overlap_y // 2
                    second.rect.y -= overlap_y // 2

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for square in squares:
            square.update(WINDOW_WIDTH, WINDOW_HEIGHT)

        resolve_square_collisions(squares)
        screen.fill(COLOR_BG)
        for square in squares:
            square.draw(screen)
        draw_fps(screen, font, clock)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()