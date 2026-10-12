"""
Particle Art - Flying Particle Animation & Static Dot Reconstruction
Based on reference implementation by Gracy Goswami:
https://github.com/Gracyclub/Day-1-mata-python-sketch.git
Licensed under MIT License.
"""

import argparse
from pathlib import Path
import sys
import time
import cv2
import numpy as np

# ==============================================================================
# CONFIGURATION & PARAMETERS
# ==============================================================================

# Sampling and rendering parameters
SAMPLE_STEP = 4           # Grid interval (pixels) between sampled points
DOT_RADIUS = 2            # Radius (pixels) of each rendered circle
MAX_CANVAS_WIDTH = 560    # Maximum canvas width constraint
MAX_CANVAS_HEIGHT = 900   # Maximum canvas height constraint

# Animation parameters
DURATION_SECONDS = 6.0    # Total animation flight time (seconds)
TARGET_FPS = 30           # Desired display framerate
MAX_DELAY_FRACTION = 0.35 # Maximum staggered departure delay fraction
RANDOM_SEED = 42          # Seed for reproducible particle trajectory generation

# Background color (Dark navy/black BGR)
BG_COLOR = (18, 12, 10)

# Directory paths resolved relative to this script
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"

# Target reference image path
REFERENCE_IMAGE_PATH = ASSETS_DIR / "reference.jpeg"


# ==============================================================================
# IMAGE PROCESSING & SAMPLING FUNCTIONS
# ==============================================================================

def load_image(image_path: Path) -> np.ndarray:
    """
    Loads an image from disk using OpenCV and validates that it exists
    and decodes properly.
    """
    target = image_path
    if not target.exists():
        fallback_jpg = target.with_suffix(".jpg")
        fallback_png = target.with_suffix(".png")
        if fallback_jpg.exists():
            target = fallback_jpg
        elif fallback_png.exists():
            target = fallback_png
        else:
            print(
                f"\n[ERROR] Source image not found at: {image_path}\n"
                f"Please place your reference photograph at:\n"
                f"  --> {image_path}\n"
            )
            sys.exit(1)

    img = cv2.imread(str(target))
    if img is None:
        print(f"\n[ERROR] Could not decode image file: {target}")
        sys.exit(1)

    print(f"[OK] Successfully loaded: {target.name} ({img.shape[1]}x{img.shape[0]} px)")
    return img


def resize_image(image: np.ndarray, max_width: int = MAX_CANVAS_WIDTH, max_height: int = MAX_CANVAS_HEIGHT) -> np.ndarray:
    """
    Proportionally resizes the image so it fits within (max_width x max_height)
    while preserving its original aspect ratio.
    """
    h, w = image.shape[:2]
    scale = min(max_width / float(w), max_height / float(h))

    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))

    if (new_w, new_h) != (w, h):
        interp = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR
        resized = cv2.resize(image, (new_w, new_h), interpolation=interp)
        print(f"[OK] Proportionally resized to: {new_w}x{new_h} px (scale factor: {scale:.3f})")
        return resized

    return image.copy()


def sample_pixels(image: np.ndarray, step: int = SAMPLE_STEP):
    """
    Samples pixel positions (x, y) and their exact BGR colors across
    the image at regular grid intervals of `step` pixels.
    Returns:
      targets: np.ndarray of shape (N, 2), dtype float32
      colors:  np.ndarray of shape (N, 3), dtype uint8
    """
    h, w = image.shape[:2]
    targets = []
    colors = []

    for y in range(0, h, step):
        for x in range(0, w, step):
            b, g, r = image[y, x]
            targets.append((float(x), float(y)))
            colors.append((int(b), int(g), int(r)))

    print(f"[OK] Sampled {len(targets):,} particles with step={step}")
    return np.array(targets, dtype=np.float32), np.array(colors, dtype=np.uint8)


def render_dots(h: int, w: int, points: np.ndarray, colors: np.ndarray, dot_radius: int = DOT_RADIUS, bg_color=BG_COLOR) -> np.ndarray:
    """
    Creates a dark background canvas and draws filled colored circles
    at each point using the sampled pixel color.
    """
    canvas = np.full((h, w, 3), bg_color, dtype=np.uint8)
    for (x, y), (b, g, r) in zip(points, colors):
        pt = (int(round(x)), int(round(y)))
        col = (int(b), int(g), int(r))
        cv2.circle(canvas, pt, dot_radius, col, thickness=-1, lineType=cv2.LINE_AA)
    return canvas


# ==============================================================================
# PARTICLE ANIMATION FUNCTIONS
# ==============================================================================

def create_particle_starts(num_particles: int, width: int, height: int, seed: int = RANDOM_SEED):
    """
    Generates one starting position per particle distributed outside all 4 edges,
    plus a random start delay fraction per particle.
    Margins are proportional to the canvas dimensions.
    Uses a seeded NumPy generator for deterministic results.
    """
    rng = np.random.default_rng(seed)

    margin_x = 0.25 * width
    margin_y = 0.20 * height

    # Choose edge per particle: 0=Top, 1=Bottom, 2=Left, 3=Right
    sides = rng.integers(0, 4, size=num_particles)
    starts = np.zeros((num_particles, 2), dtype=np.float32)

    # Top edge (0): y above canvas
    top_mask = (sides == 0)
    starts[top_mask, 0] = rng.uniform(-margin_x, width + margin_x, size=np.sum(top_mask))
    starts[top_mask, 1] = rng.uniform(-margin_y * 1.5, -20.0, size=np.sum(top_mask))

    # Bottom edge (1): y below canvas
    bot_mask = (sides == 1)
    starts[bot_mask, 0] = rng.uniform(-margin_x, width + margin_x, size=np.sum(bot_mask))
    starts[bot_mask, 1] = rng.uniform(height + 20.0, height + margin_y * 1.5, size=np.sum(bot_mask))

    # Left edge (2): x left of canvas
    left_mask = (sides == 2)
    starts[left_mask, 0] = rng.uniform(-margin_x * 1.5, -20.0, size=np.sum(left_mask))
    starts[left_mask, 1] = rng.uniform(-margin_y, height + margin_y, size=np.sum(left_mask))

    # Right edge (3): x right of canvas
    right_mask = (sides == 3)
    starts[right_mask, 0] = rng.uniform(width + 20.0, width + margin_x * 1.5, size=np.sum(right_mask))
    starts[right_mask, 1] = rng.uniform(-margin_y, height + margin_y, size=np.sum(right_mask))

    # Random stagger delay fraction in [0.0, MAX_DELAY_FRACTION]
    delays = rng.uniform(0.0, MAX_DELAY_FRACTION, size=num_particles).astype(np.float32)

    return starts, delays


def calculate_particle_positions(starts: np.ndarray, targets: np.ndarray, delays: np.ndarray, t: float) -> np.ndarray:
    """
    Calculates current (x, y) coordinates for all particles at global progress t in [0.0, 1.0].
      local_progress = clip((t - d) / (1 - d), 0, 1)
      eased_progress = 1 - (1 - local_progress) ** 3
      position = start + (target - start) * eased_progress
    """
    denom = 1.0 - delays
    local_progress = np.clip((t - delays) / denom, 0.0, 1.0)
    eased_progress = 1.0 - np.power(1.0 - local_progress, 3)

    # Broadcast eased_progress (N, 1) across x and y
    positions = starts + (targets - starts) * eased_progress[:, np.newaxis]
    return positions


def render_particle_frame(h: int, w: int, positions: np.ndarray, colors: np.ndarray, dot_radius: int = DOT_RADIUS, bg_color=BG_COLOR) -> np.ndarray:
    """
    Renders one frame onto a fresh dark canvas.
    Skips particles completely outside canvas boundaries without clamping,
    allowing OpenCV to naturally clip partially visible border dots.
    """
    canvas = np.full((h, w, 3), bg_color, dtype=np.uint8)

    pos_int = np.round(positions).astype(np.int32)
    xs = pos_int[:, 0]
    ys = pos_int[:, 1]

    # Only render particles that touch or overlap the canvas area
    visible_mask = (
        (xs >= -dot_radius) & (xs < w + dot_radius) &
        (ys >= -dot_radius) & (ys < h + dot_radius)
    )
    visible_indices = np.nonzero(visible_mask)[0]

    for idx in visible_indices:
        pt = (int(xs[idx]), int(ys[idx]))
        col = (int(colors[idx, 0]), int(colors[idx, 1]), int(colors[idx, 2]))
        cv2.circle(canvas, pt, dot_radius, col, thickness=-1, lineType=cv2.LINE_AA)

    return canvas


def run_animation(targets: np.ndarray, colors: np.ndarray, h: int, w: int):
    """
    Runs the interactive flying particle animation:
      - Time-based interpolation using time.perf_counter()
      - Paced at TARGET_FPS
      - Controls: Esc (exit), R (restart), window close (exit)
      - On completion: renders exact targets and saves assembled_dots.png
    """
    num_particles = len(targets)
    starts, delays = create_particle_starts(num_particles, w, h, seed=RANDOM_SEED)

    window_name = "Bathukamma Particle Assembly (Esc: Exit | R: Restart)"
    frame_interval = 1.0 / TARGET_FPS

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    assembled_output_path = OUTPUT_DIR / "assembled_dots.png"

    try:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, min(700, w), min(950, h))
    except cv2.error as e:
        print(f"\n[NOTE] OpenCV GUI window cannot be opened ({e}).")
        print("Rendering sample animation milestones headlessly...")
        for sample_t, name in [(0.0, "start_dots.png"), (0.5, "mid_dots.png"), (1.0, "assembled_dots.png")]:
            pos = calculate_particle_positions(starts, targets, delays, sample_t)
            frame = render_particle_frame(h, w, pos, colors, dot_radius=DOT_RADIUS, bg_color=BG_COLOR)
            out_p = OUTPUT_DIR / name
            cv2.imwrite(str(out_p), frame)
            print(f"[OK] Generated {name} at progress t={sample_t:.1f}")
        return

    print("\n" + "=" * 65)
    print(" Flying Particle Animation Started")
    print(" Controls: [Esc] = Exit | [R] = Restart animation")
    print("=" * 65)

    # Master animation loop allowing restarts without recursion
    while True:
        start_time = time.perf_counter()
        completed = False

        while not completed:
            frame_start = time.perf_counter()
            elapsed = frame_start - start_time
            t = min(1.0, elapsed / DURATION_SECONDS)

            positions = calculate_particle_positions(starts, targets, delays, t)
            frame = render_particle_frame(h, w, positions, colors, dot_radius=DOT_RADIUS, bg_color=BG_COLOR)

            cv2.imshow(window_name, frame)

            # Check if user closed the window
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyAllWindows()
                return

            # Compute remaining time to hold TARGET_FPS pace
            render_elapsed = time.perf_counter() - frame_start
            wait_ms = max(1, int(round((frame_interval - render_elapsed) * 1000)))

            key = cv2.waitKey(wait_ms) & 0xFF
            if key == 27:  # Esc
                cv2.destroyAllWindows()
                return
            if key in (ord('r'), ord('R')):
                # Restart from the beginning
                break

            if t >= 1.0:
                completed = True

        # If user pressed restart before completion, re-run outer loop
        if not completed:
            continue

        # Animation finished: render exact target positions
        print("[OK] Animation complete! Displaying finalized reconstruction.")
        final_frame = render_dots(h, w, targets, colors, dot_radius=DOT_RADIUS, bg_color=BG_COLOR)
        cv2.imwrite(str(assembled_output_path), final_frame)
        print(f"[OK] Saved completed image to: {assembled_output_path}")

        cv2.imshow(window_name, final_frame)

        # Hold completed dotted image until Esc or R
        restart_requested = False
        while True:
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyAllWindows()
                return

            key = cv2.waitKey(50) & 0xFF
            if key == 27:  # Esc
                cv2.destroyAllWindows()
                return
            if key in (ord('r'), ord('R')):
                restart_requested = True
                break

        if not restart_requested:
            break


def run_preview(resized_img: np.ndarray, targets: np.ndarray, colors: np.ndarray, h: int, w: int):
    """
    Renders and displays the static dot reconstruction side-by-side with the source.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / "dot_preview.png"
    side_by_side_path = OUTPUT_DIR / "side_by_side_preview.png"

    dot_canvas = render_dots(h, w, targets, colors, dot_radius=DOT_RADIUS, bg_color=BG_COLOR)
    cv2.imwrite(str(out_file), dot_canvas)
    print(f"[OK] Saved dot reconstruction to: {out_file}")

    side_by_side = np.hstack([resized_img, dot_canvas])
    cv2.imwrite(str(side_by_side_path), side_by_side)
    print(f"[OK] Saved side-by-side comparison to: {side_by_side_path}")

    window_name = "Particle Art: Source (Left) vs Dot Reconstruction (Right)"
    try:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, min(1400, w * 2), min(950, h))
        cv2.imshow(window_name, side_by_side)
        print("\n[INFO] Preview window displayed.")
        print("[INFO] Press any key while focused on the window to close...")
        cv2.waitKey(0)
    except cv2.error as e:
        print(f"\n[NOTE] OpenCV GUI display is unavailable in this environment ({e}).")
        print(f"       Visual output has been saved to: {out_file}")
    finally:
        cv2.destroyAllWindows()


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Particle Art - Dot Reconstruction & Flying Animation")
    parser.add_argument(
        "--mode",
        choices=["animate", "preview"],
        default="animate",
        help="Execution mode: 'animate' (flying particle animation) or 'preview' (static dot reconstruction)",
    )
    args = parser.parse_args()

    print("=" * 65)
    print(f" Particle Art - Mode: {args.mode.upper()}")
    print("=" * 65)

    # 1. Load source image
    src_img = load_image(REFERENCE_IMAGE_PATH)

    # 2. Proportionally resize to fit canvas constraints (560 x 900)
    resized_img = resize_image(src_img, max_width=MAX_CANVAS_WIDTH, max_height=MAX_CANVAS_HEIGHT)
    h, w = resized_img.shape[:2]

    # 3. Sample pixel positions and colors
    targets, colors = sample_pixels(resized_img, step=SAMPLE_STEP)

    # 4. Execute selected mode
    if args.mode == "preview":
        run_preview(resized_img, targets, colors, h, w)
    else:
        run_animation(targets, colors, h, w)


if __name__ == "__main__":
    main()
