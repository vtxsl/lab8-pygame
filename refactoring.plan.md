# Refactoring Plan

## 1. Overview

`main.py` is a small pygame simulation that creates moving squares, bounces them off the window edges, replaces squares when they expire, and applies flee/chase behavior based on nearby squares.

The code already works, so the goal is not to redesign it. The main improvements are readability, clearer helper boundaries, and a little less repeated logic so a beginner can follow the flow more easily.

## 2. Refactoring Goals

- Make the main loop easier to read from top to bottom.
- Give repeated calculations clearer names.
- Keep related logic close together but split large steps into small helpers.
- Add short inline comments in the final code that explain what changed and why it helps.
- Preserve the current behavior exactly.

## 3. Step-by-Step Refactoring Plan

### Step 1: Group the top-level configuration values

What to do:
- Keep the window, speed, size, and color constants near the top of the file.
- Add a short comment block above each group, such as movement settings, spawn settings, and display settings.

Why this helps:
- Beginners can find the important tuning values faster.
- Related settings are easier to understand when they are grouped by purpose.

Inline comment requirement for the final code:
- Add concise comments that explain that these values control game behavior and are kept together for readability.

### Step 2: Add an explicit return type to `apply_flee_behavior`

What to do:
- Change the function signature to include `-> None`.
- Leave the logic the same.

Why this helps:
- The rest of the file already uses return types in most places.
- A consistent type hint makes the code easier to scan and understand.

Inline comment requirement for the final code:
- Add a short comment if needed to explain that the function updates square velocity in place and does not return a value.

### Step 3: Extract the wall-bounce logic from `Square.update`

What to do:
- Move the left/right bounce code into a small helper such as `bounce_x` or `handle_horizontal_bounce`.
- Move the top/bottom bounce code into a matching helper such as `bounce_y` or `handle_vertical_bounce`.
- Keep the position clamp and velocity flip behavior unchanged.

Why this helps:
- The `Square.update` method is easier to read when it says “move, then bounce, then check lifetime.”
- Small helpers make repeated logic easier to test and explain.

Inline comment requirement for the final code:
- Add brief comments that explain the helpers separate movement from boundary handling.

### Step 4: Separate speed limiting into a named helper

What to do:
- Extract the block that calculates `local_max` and clamps velocity into a helper such as `limit_square_speed`.
- Reuse the same size-based speed rule in `random_square` and `apply_flee_behavior`.

Why this helps:
- The same formula appears in more than one place.
- A helper reduces duplication and makes the speed rule easier to change later.

Inline comment requirement for the final code:
- Add a small comment that explains the helper keeps size-based speed limits consistent.

### Step 5: Simplify `random_square` by naming its substeps

What to do:
- Break the function into short pieces mentally or with tiny helpers: choose size, compute speed limit, choose a position, check overlap, and build the square.
- Keep the 300-attempt fallback behavior exactly as it is.

Why this helps:
- Spawn logic is currently doing several jobs in one block.
- Naming the steps makes the purpose of each part clearer to beginners.

Inline comment requirement for the final code:
- Add a comment near the fallback square that explains it is a safety path when the search runs out of attempts.

### Step 6: Make the main loop read like a simple story

What to do:
- Keep the same order of operations, but make each phase obvious with short helper calls or short comment headers:
  - get frame time
  - handle quit events
  - update live squares
  - resolve collisions
  - apply flee/chase behavior
  - draw and flip the screen

Why this helps:
- The `while running` loop is the most important part of the program.
- A clearer loop helps beginners understand the game frame flow quickly.

Inline comment requirement for the final code:
- Add short comments that explain the purpose of each frame stage, not the mechanics of every single line.

### Step 7: Give placeholder functions and unclear branches a clearer explanation

What to do:
- Add a comment above `resolve_square_collisions` that explains it is currently a placeholder.
- If you keep `pass`, explain that the function exists for future collision handling.
- Add a short note near the replacement branch in `main` so it is clear why `random_square(alive_squares)` is used.

Why this helps:
- Beginners will not wonder whether the empty function is a bug or a deliberate stub.
- The replacement branch becomes easier to understand when its purpose is stated explicitly.

Inline comment requirement for the final code:
- Explain what the placeholder means and why the replacement logic uses the current live list.

## 4. Final Output Requirements (Mandatory)

When this plan is executed, the output must:

- Contain only the refactored code.
- Include concise inline comments that explain what changed.
- Include concise inline comments that explain why each change improves readability, maintainability, or correctness.
- Mention important beginner-friendly programming ideas such as helper functions, return types, and separation of concerns.
- Keep behavior the same unless a change is clearly necessary for readability only.

## 5. Key Concepts for Students

- `dt` time step: movement is scaled by elapsed time, not by frame count alone.
- Helper functions: small functions make code easier to read and reuse.
- Separation of concerns: each block should do one job.
- Type hints: return annotations make function intent clearer.
- Clamping: limiting values keeps motion and position inside safe bounds.
- Placeholder functions: a `pass` body can mark future work without breaking the program.

## 6. Safety Notes

- Test after each small change so behavior does not drift.
- Preserve the current bounce, spawn, and lifetime behavior unless a comment-only change is enough.
- Avoid turning the file into a large abstraction layer; keep helpers small and beginner-friendly.
- Do not remove the fallback spawn path unless a replacement strategy is added first.
- If you refactor the repeated speed formula, make sure both spawn and steering still use the same limits.