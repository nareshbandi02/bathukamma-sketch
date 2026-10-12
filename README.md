# bathukamma-sketch

An image-based particle assembly and pointillism reconstruction tool for the Bathukamma festival portrait, built in Python using OpenCV and NumPy.

Particles spawn outside all four edges, fly inward along cubic deceleration curves, and assemble smoothly into a colored-dot portrait of the Bathukamma scene.

This implementation is inspired by and adapted from the open-source particle sketch work by [Gracyclub/Day-1-mata-python-sketch](https://github.com/Gracyclub/Day-1-mata-python-sketch.git).

---

## Attribution & License

- **Reference Implementation:** [Day-1-mata-python-sketch](https://github.com/Gracyclub/Day-1-mata-python-sketch.git) by Gracy Goswami.
- **License:** MIT License (see [`LICENSE`](LICENSE)).

---

## Prerequisites

- **Python 3.8+**
- **OpenCV & NumPy** with GUI support

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/nareshbandi02/bathukamma-sketch.git
cd bathukamma-sketch
pip install -r requirements.txt
```

---

## How to Run

The working application entry point is [`particle_art/main.py`](particle_art/main.py).

### 1. Flying Particle Animation (Default)

Watch colored dots fly in from outside the canvas boundaries and settle into position:

```bash
python particle_art/main.py --mode animate
```

Or change into the directory:

```bash
cd particle_art
python main.py
```

### 2. Static Dot Preview

Inspect the pointillism density and original reference image side-by-side:

```bash
python particle_art/main.py --mode preview
```

---

## Interactive Controls

| Key / Action | Function |
| :--- | :--- |
| **`R` / `r`** | Restart the animation from the beginning using the deterministic seed. |
| **`Esc`** | Exit the application cleanly. |
| **Window Close (`X`)** | Exits cleanly without hangs or errors. |
| **Completion State** | Final assembled dot artwork is held on screen until you choose to restart (`R`) or exit (`Esc`). |

---

## Project Structure

```
bathukamma-sketch/
├── LICENSE                    # MIT License with original attribution
├── README.md                  # Project overview, setup, and controls
├── requirements.txt           # opencv-python, numpy
├── .gitignore                 # Excludes caches, outputs, and environments
└── particle_art/
    ├── main.py                # Final working animation & reconstruction script
    ├── README.md              # Particle art specific documentation
    ├── requirements.txt       # Dependencies
    ├── LICENSE                # Attribution license
    └── assets/
        ├── reference.jpeg     # Essential input Bathukamma photograph
        ├── foreground_mask.png# Segmentation mask
        └── README.txt         # Notes on reference assets
```

---

## Configuration & Tuning

Adjustable parameters in [`particle_art/main.py`](particle_art/main.py):

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `DURATION_SECONDS` | `6.0` | Total flight duration from departure to final assembly. |
| `TARGET_FPS` | `30` | Target display framerate. |
| `MAX_DELAY_FRACTION`| `0.35` | Fraction of total time over which departures are staggered. |
| `RANDOM_SEED` | `42` | Seed for reproducible particle spawn positions. |
| `SAMPLE_STEP` | `4` | Pixel distance between sampled grid dots. |
| `DOT_RADIUS` | `2` | Radius in pixels of each rendered particle. |
| `MAX_CANVAS_WIDTH` | `560` | Maximum width constraint preserving aspect ratio. |
| `MAX_CANVAS_HEIGHT`| `900` | Maximum height constraint preserving aspect ratio. |
| `BG_COLOR` | `(18, 12, 10)` | Dark background canvas color in BGR format. |

---

## Output Files

Output images are automatically saved to `particle_art/output/`:
- `assembled_dots.png`: Finalized full dot reconstruction saved at completion.
- `dot_preview.png`: Static dot reconstruction from preview mode.
- `side_by_side_preview.png`: Source image and static dot reconstruction side-by-side.
