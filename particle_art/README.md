# Particle Art (Stage 2: Flying Particle Animation)

An image-based particle assembly and pointillism reconstruction tool built in Python using OpenCV and NumPy.

Particles spawn outside all four edges, fly inward with cubic deceleration curves, and assemble smoothly into a colored-dot portrait of the Bathukamma scene.

This implementation is inspired by and adapted from the open-source particle sketch work by [Gracyclub/Day-1-mata-python-sketch](https://github.com/Gracyclub/Day-1-mata-python-sketch.git).

---

## Attribution & License

- **Reference Implementation:** [Day-1-mata-python-sketch](https://github.com/Gracyclub/Day-1-mata-python-sketch.git) by Gracy Goswami.
- **License:** MIT License (see [`LICENSE`](LICENSE)).

---

## Prerequisites

- **Python 3.8+**
- **OpenCV & NumPy** with local GUI window support:
  ```bash
  cd particle_art
  python -m pip install -r requirements.txt
  ```

---

## How to Run

### 1. Flying Particle Animation (Default)
Watch colored dots fly in from outside the canvas boundaries and settle into position:

```bash
python main.py --mode animate
```
*(Or simply `python main.py`)*

### 2. Static Dot Preview
Inspect the pointillism density and original source side by side:

```bash
python main.py --mode preview
```

---

## Interactive Controls (During Animation)

- **`R` / `r`**: Restart the animation from the beginning using the same deterministic seed.
- **`Esc`**: Exit the application cleanly.
- **Window Close (`X`)**: Exits cleanly without hangs or errors.
- **At Completion**: The assembled dot image is held on screen until you choose to restart (`R`) or exit (`Esc`).

---

## Animation Settings

You can customize the parameters directly in [`main.py`](main.py):

| Setting | Default | Description |
| :--- | :--- | :--- |
| `DURATION_SECONDS` | `6.0` | Total flight duration from departure to final assembly. |
| `TARGET_FPS` | `30` | Target display framerate (render time is accounted for during pacing). |
| `MAX_DELAY_FRACTION` | `0.35` | Fraction of total time over which particle departure is staggered. |
| `RANDOM_SEED` | `42` | Seed for deterministic, reproducible particle spawn positions. |
| `SAMPLE_STEP` | `4` | Distance in pixels between sampled grid dots. |
| `DOT_RADIUS` | `2` | Radius in pixels of each rendered particle. |
| `MAX_CANVAS_WIDTH` | `560` | Maximum width constraint for proportional image resizing. |
| `MAX_CANVAS_HEIGHT` | `900` | Maximum height constraint for proportional image resizing. |
| `BG_COLOR` | `(18, 12, 10)` | Dark background canvas color in BGR format. |

---

## Output Files

Output images are automatically saved to `particle_art/output/`:
- **`assembled_dots.png`**: The finalized full dot reconstruction saved at completion.
- **`dot_preview.png`**: Static dot reconstruction from preview mode.
- **`side_by_side_preview.png`**: Source image and static dot reconstruction side by side.
