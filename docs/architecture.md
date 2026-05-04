# Architecture Documentation

This document describes the concrete architecture of the pygame square simulation implemented in `main.py`.

## Scope and Entry Points

- Primary runtime entry point: `main.py` via `if __name__ == "__main__": main()`.
- Secondary variant implementation: `withcol.py` (similar structure, integer-velocity version).
- Primary execution path documented below is from `main.py`.

## Module Dependency Graph

```mermaid
graph LR
    M["main.py"] --> R["random"]
    M --> D["dataclasses.dataclass"]
    M --> P["pygame"]
    M --> H["math"]
    M --> S["Square Dataclass"]
    M --> F["Top-Level Functions"]
```

Notes:
- `random` is used for spawn position, velocity directions, color, and steering jitter.
- `pygame` provides event loop, rendering, timing, and rectangle primitives.
- `math.hypot` is used for distance and vector magnitude calculations.

## High-Level Runtime Flow

```mermaid
graph TD
    A["Process Start"] --> B["Initialize pygame"]
    B --> C["Create Window, Clock, Font"]
    C --> D["Create Initial Squares"]
    D --> E["Enter Main Loop"]
    E --> F["Tick Clock and Compute dt"]
    F --> G["Process Events"]
    G --> H{"Quit Event?"}
    H -->|"Yes"| I["Set running = False"]
    H -->|"No"| J["Update or Respawn Squares"]
    I --> T["Quit pygame and Exit"]
    J --> K["Resolve Collisions (Currently No-Op)"]
    K --> L["Apply Flee/Chase Behavior"]
    L --> M2["Clear Screen"]
    M2 --> N["Draw Squares"]
    N --> O["Draw FPS"]
    O --> P2["Flip Display"]
    P2 --> E
```

## Function-Level Call Graph

```mermaid
graph TD
    START["__main__ Guard"] --> MAIN["main()"]

    MAIN --> INIT["pygame.init()"]
    MAIN --> SETMODE["pygame.display.set_mode()"]
    MAIN --> CAPTION["pygame.display.set_caption()"]
    MAIN --> CLOCK["pygame.time.Clock()"]
    MAIN --> FONT["pygame.font.Font(...)"]
    MAIN --> CREATE["create_squares()"]

    CREATE --> RS1["random_square(existing)"]

    MAIN --> EVENTGET["pygame.event.get()"]
    MAIN --> TICK["clock.tick(FPS)"]

    MAIN --> SQUPDATE["Square.update(width, height, dt)"]
    MAIN --> RS2["random_square(alive_squares)"]

    MAIN --> COLL["resolve_square_collisions(squares)"]
    MAIN --> FLEE["apply_flee_behavior(squares, dt)"]

    MAIN --> FILL["screen.fill(COLOR_BG)"]
    MAIN --> SQDRAW["Square.draw(screen)"]
    MAIN --> DFPS["draw_fps(screen, font, clock)"]
    DFPS --> GETFPS["clock.get_fps()"]
    DFPS --> RENDER["font.render(...)"]
    DFPS --> BLIT["surface.blit(...)"]

    MAIN --> FLIP["pygame.display.flip()"]
    MAIN --> QUIT["pygame.quit()"]

    FLEE --> HYPOT1["math.hypot(dx, dy)"]
    FLEE --> HYPOT2["math.hypot(vx, vy)"]
```

## Primary Execution Sequence (Full)

```mermaid
sequenceDiagram
    participant BOOT as "Python Runtime"
    participant APP as "main()"
    participant PG as "pygame"
    participant CLK as "Clock"
    participant EVT as "Event Queue"
    participant SQ as "Square Objects"
    participant AI as "apply_flee_behavior()"
    participant REN as "Renderer"

    BOOT->>APP: "Call main()"
    APP->>PG: "init()"
    APP->>PG: "display.set_mode()"
    APP->>PG: "display.set_caption()"
    APP->>CLK: "Create Clock"
    APP->>APP: "create_squares()"
    loop "For NUM_SQUARES"
        APP->>APP: "random_square(existing)"
    end

    loop "While running is True"
        APP->>CLK: "tick(FPS)"
        CLK-->>APP: "dt (seconds)"

        APP->>EVT: "event.get()"
        EVT-->>APP: "events list"

        alt "QUIT event present"
            APP->>APP: "running = False"
        else "No QUIT"
            APP->>SQ: "update(width, height, dt) for each square"
            alt "Square still alive"
                SQ-->>APP: "True"
                APP->>APP: "append existing square"
            else "Square expired"
                SQ-->>APP: "False"
                APP->>APP: "random_square(alive_squares)"
                APP->>APP: "append replacement square"
            end

            APP->>APP: "resolve_square_collisions(squares)"
            Note over APP: "Current implementation is pass"
            APP->>AI: "apply_flee_behavior(squares, dt)"

            APP->>REN: "screen.fill(COLOR_BG)"
            APP->>SQ: "draw(screen) for each square"
            APP->>APP: "draw_fps(screen, font, clock)"
            APP->>PG: "display.flip()"
        end
    end

    APP->>PG: "quit()"
```

## Key Architectural Notes

- The simulation uses an update-render loop with time-based motion (`dt`).
- Square lifetime is enforced by `death_time`; expired squares are replaced during the frame update stage.
- Behavior steering is pairwise across all squares (`O(n^2)` check in `apply_flee_behavior`).
- Collision stage exists in the pipeline but is currently a no-op (`pass`).
- `withcol.py` is an alternate script that keeps a similar loop shape but uses integer-step movement and a placeholder collision block with commented logic.
