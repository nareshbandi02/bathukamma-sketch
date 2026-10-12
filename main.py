"""
Bathukamma Illustration - Python Turtle Graphics
Step 2: Basic Silhouettes, Composition, and Layout Guides
"""

import math
import turtle

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================

# Canvas dimensions (logical coordinates)
CANVAS_WIDTH = 550
CANVAS_HEIGHT = 950

# Visual settings
WINDOW_TITLE = "Bathukamma Festival - 2D Illustration (Step 2: Silhouettes)"
BG_COLOR = "#0a1128"       # Deep dark navy background
SHOW_GUIDES = True          # Press 'G' key in the window to toggle guides

# Layout Guide Regions: (x_min, y_min, x_max, y_max, label, color)
GUIDE_REGIONS = [
    (155, 730, 305, 925, "Flower Arrangement (Bathukamma)", "#ffcc00"),
    (90, 80, 395, 760, "Woman (including arms)", "#ff6b6b"),
    (325, 80, 505, 500, "Young Girl", "#4ecdc4"),
    (50, 45, 515, 80, "Platform / Stage", "#95a5a6"),
]

# Color Palette for Step 2 Silhouettes
COLOR_PLATFORM_BASE = "#3e2723"     # Dark brown wood
COLOR_PLATFORM_TOP = "#4e342e"      # Slightly lighter plank edge
COLOR_SKIN = "#d29363"              # Warm skin tone
COLOR_HAIR = "#1a1a1a"              # Dark black/brown for hair silhouette
COLOR_WOMAN_SARI = "#b71c1c"        # Deep red sari
COLOR_WOMAN_BLOUSE = "#1b5e20"      # Forest green blouse
COLOR_GIRL_BLOUSE = "#ec407a"       # Bright pink blouse
COLOR_GIRL_SKIRT = "#2e7d32"        # Fresh green skirt
COLOR_FLOWER_HOLDER = "#c59b27"     # Muted golden amber placeholder


# ==============================================================================
# REUSABLE DRAWING HELPERS
# ==============================================================================

def draw_polygon(pen, points, fill_color, outline_color=None):
    """
    Draws a filled polygon connecting a list of (x, y) points.
    Lifts the pen before and after to prevent unwanted connecting lines.
    """
    if not points:
        return

    pen.penup()
    pen.goto(points[0])

    if outline_color:
        pen.pencolor(outline_color)
    else:
        pen.pencolor(fill_color)

    pen.fillcolor(fill_color)
    pen.pendown()
    pen.begin_fill()

    for pt in points[1:]:
        pen.goto(pt)
    pen.goto(points[0])

    pen.end_fill()
    pen.penup()


def draw_ellipse(pen, cx, cy, radius_x, radius_y, fill_color, outline_color=None, steps=36):
    """
    Draws a filled ellipse centered at (cx, cy) using parametric equations:
      x = cx + radius_x * cos(theta)
      y = cy + radius_y * sin(theta)
    """
    points = []
    for i in range(steps):
        theta = 2.0 * math.pi * i / steps
        x = cx + radius_x * math.cos(theta)
        y = cy + radius_y * math.sin(theta)
        points.append((x, y))

    draw_polygon(pen, points, fill_color, outline_color)


# ==============================================================================
# SCENE SILHOUETTE FUNCTIONS
# ==============================================================================

def draw_platform(pen):
    """
    Draws the raised stage/platform:
      - Region: approximately x=50–515, y=45–80
      - Top surface at y=80 acts as the standing floor
    """
    # Main platform body
    base_points = [
        (50, 45),
        (515, 45),
        (515, 75),
        (50, 75),
    ]
    draw_polygon(pen, base_points, COLOR_PLATFORM_BASE)

    # Top surface plank (highlight trim)
    top_points = [
        (45, 75),
        (520, 75),
        (520, 80),
        (45, 80),
    ]
    draw_polygon(pen, top_points, COLOR_PLATFORM_TOP)


def draw_woman_base(pen):
    """
    Draws the woman's basic silhouette and arm pose:
      - Raised left arm supporting the Bathukamma
      - Lowered right arm reaching gently toward the girl
      - Red sari, green blouse, skin, hair, and feet
    """
    # 1. Feet resting on the platform (y=80)
    draw_ellipse(pen, 205, 85, 12, 6, COLOR_SKIN)
    draw_ellipse(pen, 240, 85, 12, 6, COLOR_SKIN)

    # 2. Left Arm (Viewer's Left - Raised upward to balance Bathukamma)
    # Shoulder: (185, 625) -> Elbow: (110, 680) -> Wrist: (155, 775) -> Hand: (160, 785)
    left_upper_arm = [
        (185, 635),
        (198, 615),
        (124, 665),
        (108, 680),
    ]
    draw_polygon(pen, left_upper_arm, COLOR_SKIN)

    left_forearm = [
        (108, 680),
        (124, 665),
        (168, 770),
        (152, 780),
    ]
    draw_polygon(pen, left_forearm, COLOR_SKIN)

    # Raised hand near the base of the flower arrangement
    draw_ellipse(pen, 160, 785, 9, 13, COLOR_SKIN)

    # 3. Right Arm (Viewer's Right - Extends diagonally toward girl's shoulder)
    # Shoulder: (280, 610) down toward (380, 435)
    right_arm = [
        (275, 620),
        (292, 600),
        (386, 436),
        (370, 426),
    ]
    draw_polygon(pen, right_arm, COLOR_SKIN)

    # Lowered hand resting close to girl's shoulder
    draw_ellipse(pen, 382, 430, 11, 8, COLOR_SKIN)

    # 4. Long Sari Silhouette (Waist at y=520 down to hem at y=95)
    sari_points = [
        (150, 95),      # Bottom-left hem
        (145, 230),     # Left hip flare
        (158, 380),     # Mid-hip
        (185, 520),     # Left waist
        (270, 520),     # Right waist
        (282, 380),     # Right hip
        (295, 230),     # Right skirt fall
        (285, 95),      # Bottom-right hem
    ]
    draw_polygon(pen, sari_points, COLOR_WOMAN_SARI)

    # 5. Torso & Blouse (x=180–285, y=510–645)
    blouse_points = [
        (185, 515),     # Lower left torso
        (270, 515),     # Lower right torso
        (285, 610),     # Right shoulder seam
        (260, 645),     # Right neck edge
        (200, 645),     # Left neck edge
        (180, 620),     # Left shoulder seam
    ]
    draw_polygon(pen, blouse_points, COLOR_WOMAN_BLOUSE)

    # Blouse sleeves for visible arm connection
    left_sleeve = [
        (180, 620),
        (200, 645),
        (170, 642),
        (152, 630),
    ]
    draw_polygon(pen, left_sleeve, COLOR_WOMAN_BLOUSE)

    # Sari pallu crossing over torso diagonally
    pallu_points = [
        (185, 515),
        (215, 515),
        (255, 645),
        (230, 645),
    ]
    draw_polygon(pen, pallu_points, COLOR_WOMAN_SARI)

    # 6. Neck (Connecting torso to head)
    neck_points = [
        (222, 640),
        (238, 640),
        (236, 680),
        (224, 680),
    ]
    draw_polygon(pen, neck_points, COLOR_SKIN)

    # 7. Hair silhouette (behind head)
    draw_ellipse(pen, 230, 715, 26, 28, COLOR_HAIR)

    # 8. Head oval centered around (230, 705)
    draw_ellipse(pen, 230, 705, 21, 26, COLOR_SKIN)


def draw_girl_base(pen):
    """
    Draws the girl's basic silhouette:
      - Green skirt widening toward the bottom hem
      - Pink blouse torso
      - One arm bent toward chest, one arm lowered
      - Oval head centered around (420, 470)
      - Feet resting on the platform (y=80)
    """
    # 1. Feet resting on the platform (y=80)
    draw_ellipse(pen, 405, 85, 10, 5, COLOR_SKIN)
    draw_ellipse(pen, 440, 85, 10, 5, COLOR_SKIN)

    # 2. Green Skirt (Waist x=380–465, y=340; Hem x=340–500, y=95)
    skirt_points = [
        (345, 95),      # Bottom-left hem
        (360, 220),     # Left flare
        (385, 340),     # Left waist
        (455, 340),     # Right waist
        (480, 220),     # Right flare
        (495, 95),      # Bottom-right hem
    ]
    draw_polygon(pen, skirt_points, COLOR_GIRL_SKIRT)

    # 3. Torso / Pink Blouse (x=375–465, y=335–435)
    blouse_points = [
        (385, 335),     # Bottom-left waist
        (455, 335),     # Bottom-right waist
        (455, 435),     # Right shoulder
        (385, 435),     # Left shoulder
    ]
    draw_polygon(pen, blouse_points, COLOR_GIRL_BLOUSE)

    # 4. Arms
    # Viewer's Left Arm: Bent inward toward her chest
    left_arm_bent = [
        (385, 432),
        (398, 432),
        (424, 395),
        (412, 385),
    ]
    draw_polygon(pen, left_arm_bent, COLOR_SKIN)
    # Hand resting on chest
    draw_ellipse(pen, 420, 392, 8, 7, COLOR_SKIN)

    # Viewer's Right Arm: Lowered straight along the side
    right_arm_lowered = [
        (448, 432),
        (460, 428),
        (474, 350),
        (462, 350),
    ]
    draw_polygon(pen, right_arm_lowered, COLOR_SKIN)
    # Hand at lower side
    draw_ellipse(pen, 468, 342, 7, 7, COLOR_SKIN)

    # 5. Neck (Connecting torso to head)
    neck_points = [
        (414, 432),
        (426, 432),
        (426, 455),
        (414, 455),
    ]
    draw_polygon(pen, neck_points, COLOR_SKIN)

    # 6. Hair silhouette (behind head)
    draw_ellipse(pen, 420, 478, 22, 24, COLOR_HAIR)

    # 7. Head oval centered around (420, 470)
    draw_ellipse(pen, 420, 470, 17, 21, COLOR_SKIN)


def draw_flower_placeholder(pen):
    """
    Draws a temporary solid silhouette for the Bathukamma flower stack:
      - Broad base around x=155–305, y=760
      - Narrow rounded top near (230, 915)
      - Rests on the woman's head
    """
    # Conical stepped silhouette
    bathukamma_shape = [
        (155, 755),     # Base left
        (305, 755),     # Base right
        (292, 805),     # Lower tier right
        (275, 850),     # Mid tier right
        (252, 890),     # Upper tier right
        (238, 915),     # Crown right
        (222, 915),     # Crown left
        (208, 890),     # Upper tier left
        (185, 850),     # Mid tier left
        (168, 805),     # Lower tier left
    ]
    draw_polygon(pen, bathukamma_shape, COLOR_FLOWER_HOLDER)

    # Rounded top dome
    draw_ellipse(pen, 230, 915, 14, 10, COLOR_FLOWER_HOLDER)


def draw_scene(pen):
    """
    Assembles the basic silhouettes in sensible visual depth order:
      1. Platform
      2. Woman base (feet, arms, sari, blouse, neck, head)
      3. Girl base (feet, skirt, blouse, arms, neck, head)
      4. Flower arrangement placeholder
    """
    draw_platform(pen)
    draw_woman_base(pen)
    draw_girl_base(pen)
    draw_flower_placeholder(pen)


# ==============================================================================
# GUIDE DRAWING (SEPARATE TURTLE)
# ==============================================================================

def draw_grid(pen):
    """Draws a subtle coordinate grid with labels every 50 units."""
    grid_color = "#16223f"   # Faint dark-blue line color
    axis_color = "#243760"   # Slightly brighter line for major increments
    text_color = "#4a638d"   # Subtle coordinate text color

    # Draw vertical grid lines (x-axis steps)
    for x in range(0, CANVAS_WIDTH + 1, 50):
        pen.penup()
        pen.goto(x, 0)
        pen.color(axis_color if x % 100 == 0 else grid_color)
        pen.pendown()
        pen.goto(x, CANVAS_HEIGHT)
        pen.penup()

        # Coordinate label at the bottom
        pen.goto(x + 2, 8)
        pen.color(text_color)
        pen.write(f"{x}", font=("Consolas", 7, "normal"))

    # Draw horizontal grid lines (y-axis steps)
    for y in range(0, CANVAS_HEIGHT + 1, 50):
        pen.penup()
        pen.goto(0, y)
        pen.color(axis_color if y % 100 == 0 else grid_color)
        pen.pendown()
        pen.goto(CANVAS_WIDTH, y)
        pen.penup()

        # Coordinate label along the left side
        pen.goto(8, y + 2)
        pen.color(text_color)
        pen.write(f"{y}", font=("Consolas", 7, "normal"))


def draw_bounding_box(pen, x1, y1, x2, y2, label, color):
    """Draws a rectangular guide box with outline and title label."""
    pen.penup()
    pen.color(color)

    # Draw outline rectangle
    pen.goto(x1, y1)
    pen.pendown()
    pen.goto(x2, y1)
    pen.goto(x2, y2)
    pen.goto(x1, y2)
    pen.goto(x1, y1)
    pen.penup()

    # Draw label inside the box
    label_y = y2 - 16 if y2 < CANVAS_HEIGHT - 30 else y1 + 6
    pen.goto(x1 + 6, label_y)
    pen.write(f"{label} [{x1}-{x2}, {y1}-{y2}]", font=("Arial", 8, "bold"))


def draw_guides(guide_pen):
    """Renders the complete layout guide (grid + region boundaries)."""
    draw_grid(guide_pen)
    for x1, y1, x2, y2, label, color in GUIDE_REGIONS:
        draw_bounding_box(guide_pen, x1, y1, x2, y2, label, color)


# ==============================================================================
# SETUP & MAIN EXECUTION
# ==============================================================================

def setup_canvas():
    """Initializes the Turtle screen with custom world coordinates."""
    screen = turtle.Screen()
    screen.setup(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    screen.title(WINDOW_TITLE)
    screen.bgcolor(BG_COLOR)

    # Logical coordinate system: (0, 0) at bottom-left, (550, 950) at top-right
    screen.setworldcoordinates(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Disable automatic animation for instant rendering
    screen.tracer(0)

    return screen


def create_pen():
    """Creates a hidden, fast drawing pen."""
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()
    return pen


def main():
    global SHOW_GUIDES

    screen = setup_canvas()

    # Main pen reserved exclusively for artwork
    art_pen = create_pen()

    # Separate pen for guides so they can be toggled without redrawing artwork
    guide_pen = create_pen()

    def toggle_guides():
        """Toggles layout guides on/off without affecting artwork."""
        global SHOW_GUIDES
        SHOW_GUIDES = not SHOW_GUIDES
        guide_pen.clear()
        if SHOW_GUIDES:
            draw_guides(guide_pen)
        screen.update()

    # Keyboard listeners for 'G' key toggle
    screen.listen()
    screen.onkey(toggle_guides, "g")
    screen.onkey(toggle_guides, "G")

    # Render initial guides if enabled
    if SHOW_GUIDES:
        draw_guides(guide_pen)

    # Render the base scene artwork
    draw_scene(art_pen)

    # Explicitly flush graphics to display
    screen.update()

    # Keep window open until user closes it
    turtle.done()


if __name__ == "__main__":
    main()
