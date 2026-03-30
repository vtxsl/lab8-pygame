import random
from dataclasses import dataclass
import pygame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 120
NUM_SQUARES = 10
SIZE_MIN = 20
SIZE_MAX = 80
SPEED_MIN = 2
SPEED_MAX = 5
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


def random_velocity() -> int:
    speed = random.randint(SPEED_MIN, SPEED_MAX)
    return random.choice([-1, 1]) * speed


def random_square(existing: list[Square]) -> Square:
    for _ in range(300):
        rect = pygame.Rect(
            random.randint(0, WINDOW_WIDTH - SQUARE_SIZE),
            random.randint(0, WINDOW_HEIGHT - SQUARE_SIZE),
            SQUARE_SIZE,
            SQUARE_SIZE,
        )
        if not any(rect.colliderect(s.rect) for s in existing):
            return Square(
                rect=rect,
                vx=random_velocity(),
                vy=random_velocity(),
                size=SQUARE_SIZE,
                color=(
                    random.randint(60, 255),
                    random.randint(60, 255),
                    random.randint(60, 255),
                ),
            )

    return Square(
        rect=pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE),
        vx=random_velocity(),
        vy=random_velocity(),
        size=SQUARE_SIZE,
        color=(200, 200, 200),
    )


def resolve_square_collisions(squares: list[Square]) -> None:
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            first = squares[i]
            second = squares[j]

            if not first.rect.colliderect(second.rect):
                continue

            overlap_x = min(first.rect.right, second.rect.right) - max(
                first.rect.left, second.rect.left
            )
            overlap_y = min(first.rect.bottom, second.rect.bottom) - max(
                first.rect.top, second.rect.top
            )

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


def draw_fps(
    surface: pygame.Surface,
    font: pygame.font.Font,
    clock: pygame.time.Clock,
) -> None:
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
