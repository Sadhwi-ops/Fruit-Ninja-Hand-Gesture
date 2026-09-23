
import cv2
import mediapipe as mp
import pygame
import random
import math
import json
import os
import time

# ============================================================
# CONFIG
# ============================================================

WIDTH = 1000
HEIGHT = 700
FPS = 60

GAME_TIME = 60
START_LIVES = 5
BLADE_RADIUS = 22

HIGH_SCORE_FILE = "highscore.json"
MODEL_PATH = "models/hand_landmarker.task"

# ============================================================
# PYGAME
# ============================================================

pygame.init()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Gesture Fruit Ninja"
)

clock = pygame.time.Clock()


# ============================================================
# FONTS
# ============================================================

font_small = pygame.font.SysFont(
    "Segoe UI",
    16
)

font_medium = pygame.font.SysFont(
    "Segoe UI",
    25
)

font_large = pygame.font.SysFont(
    "Segoe UI",
    43
)

font_huge = pygame.font.SysFont(
    "Segoe UI",
    54,
    bold=True
)

font_label = pygame.font.SysFont("Segoe UI", 13, bold=True)
font_stat = pygame.font.SysFont("Segoe UI", 28, bold=True)


# ============================================================
# COLORS
# ============================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (220, 50, 50)
GREEN = (50, 220, 100)
YELLOW = (255, 220, 50)
ORANGE = (255, 140, 40)
CYAN = (50, 220, 255)
PURPLE = (180, 80, 255)
GRAY = (80, 80, 80)

UI_ACCENT = (150, 225, 255)
UI_TEXT = (239, 247, 252)
UI_MUTED = (166, 187, 201)
UI_GLASS = (12, 24, 38)


# ============================================================
# FRUITS
# ============================================================

FRUITS = [

    {
        "name": "Apple",
        "color": (220, 40, 40),
        "score": 10,
        "radius": 32
    },

    {
        "name": "Orange",
        "color": (255, 150, 30),
        "score": 15,
        "radius": 30
    },

    {
        "name": "Watermelon",
        "color": (40, 190, 80),
        "score": 20,
        "radius": 38
    },

    {
        "name": "Guava",
        "color": (118, 205, 92),
        "score": 22,
        "radius": 31
    },

    {
        "name": "Banana",
        "color": (255, 225, 40),
        "score": 25,
        "radius": 30
    },

    {
        "name": "Pineapple",
        "color": (224, 174, 48),
        "score": 30,
        "radius": 36
    }
]


# ============================================================
# HIGH SCORE
# ============================================================

def load_high_score():

    if not os.path.exists(HIGH_SCORE_FILE):
        return 0

    try:

        with open(
            HIGH_SCORE_FILE,
            "r"
        ) as file:

            data = json.load(file)

            return data.get(
                "high_score",
                0
            )

    except:

        return 0


def save_high_score(score):

    with open(
        HIGH_SCORE_FILE,
        "w"
    ) as file:

        json.dump(
            {
                "high_score": score
            },
            file
        )


high_score = load_high_score()


# ============================================================
# PARTICLE
# ============================================================

class Particle:

    def __init__(
        self,
        x,
        y,
        color
    ):

        self.x = x
        self.y = y

        self.vx = random.uniform(
            -5,
            5
        )

        self.vy = random.uniform(
            -7,
            2
        )

        self.gravity = 0.25

        self.life = random.randint(
            20,
            40
        )

        self.size = random.randint(
            3,
            7
        )

        self.color = color


    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += self.gravity

        self.life -= 1


    def draw(self):

        if self.life <= 0:
            return

        pygame.draw.circle(
            screen,
            self.color,
            (
                int(self.x),
                int(self.y)
            ),
            self.size
        )


class FruitSliceEffect:

    def __init__(self, x, y, color, radius):

        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.life = 28
        self.angle = random.uniform(0, math.pi * 2)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-3, -1)

        self.drops = []

        for _ in range(12):

            self.drops.append(
                [
                    random.uniform(-3, 3),
                    random.uniform(-3, 3),
                    random.uniform(-4, 4),
                    random.uniform(-6, -1),
                    random.randint(2, 5)
                ]
            )


    def update(self):

        self.life -= 1
        self.angle += 0.08
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.16

        for drop in self.drops:

            drop[0] += drop[2]
            drop[1] += drop[3]
            drop[3] += 0.25


    def draw(self):

        if self.life <= 0:
            return

        alpha = max(0, min(255, self.life * 9))
        effect = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        burst_radius = int(self.radius * (1.15 + (28 - self.life) * 0.035))
        pygame.draw.circle(
            effect,
            (*self.color, max(0, alpha // 2)),
            (int(self.x), int(self.y)),
            burst_radius,
            2
        )

        for drop in self.drops:

            pygame.draw.circle(
                effect,
                (*self.color, alpha),
                (int(self.x + drop[0]), int(self.y + drop[1])),
                drop[4]
            )

        screen.blit(effect, (0, 0))

        half_offset = int((28 - self.life) * 0.7)
        left_half = pygame.Rect(
            int(self.x - self.radius - half_offset),
            int(self.y - self.radius * 0.8),
            self.radius,
            self.radius * 2
        )
        right_half = pygame.Rect(
            int(self.x + half_offset),
            int(self.y - self.radius * 0.8),
            self.radius,
            self.radius * 2
        )

        pygame.draw.ellipse(screen, self.color, left_half)
        pygame.draw.ellipse(screen, self.color, right_half)
        pygame.draw.arc(screen, (255, 246, 220), left_half, math.pi / 2, math.pi * 1.5, 2)
        pygame.draw.arc(screen, (255, 246, 220), right_half, -math.pi / 2, math.pi / 2, 2)
        pygame.draw.arc(screen, (255, 245, 220), left_half, 0, math.pi, 2)
        pygame.draw.arc(screen, (255, 245, 220), right_half, 0, math.pi, 2)


# ============================================================
# FRUIT
# ============================================================

class Fruit:

    def __init__(
        self,
        data
    ):

        self.name = data["name"]

        self.color = data["color"]

        self.score = data["score"]

        self.radius = data["radius"]

        self.x = random.randint(
            80,
            WIDTH - 80
        )

        self.y = HEIGHT + 50

        self.vx = random.uniform(
            -5,
            5
        )

        self.vy = random.uniform(
            -17,
            -13
        )

        self.gravity = 0.35

        self.active = True

        self.rotation = random.uniform(-20, 20)
        self.phase = random.uniform(0, math.pi * 2)


    def update(self):

        self.x += self.vx

        self.y += self.vy

        self.vy += self.gravity

        self.rotation += self.vx * 0.8
        self.phase += 0.08

        if self.y > HEIGHT + 100:

            self.active = False


    def draw(self):

        if not self.active:
            return

        pulse = 1 + math.sin(self.phase) * 0.035
        radius = max(4, int(self.radius * pulse))
        center = (int(self.x), int(self.y))

        shadow = pygame.Surface((radius * 2 + 18, max(12, radius // 2)), pygame.SRCALPHA)
        pygame.draw.ellipse(
            shadow,
            (0, 0, 0, 82),
            shadow.get_rect()
        )
        screen.blit(
            shadow,
            (
                int(self.x - radius - 9),
                int(self.y + radius * 0.72)
            )
        )

        glow = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(
            glow,
            (*self.color, 22),
            (radius * 2, radius * 2),
            int(radius * 1.25)
        )
        screen.blit(
            glow,
            (int(self.x - radius * 2), int(self.y - radius * 2))
        )

        pygame.draw.circle(screen, (255, 255, 255), center, radius + 3, 2)
        pygame.draw.circle(screen, self.color, center, radius)

        inner_color = tuple(max(0, channel - 28) for channel in self.color)

        pygame.draw.circle(
            screen,
            inner_color,
            center,
            max(3, int(radius * 0.82)),
            3
        )

        if self.name == "Watermelon":

            for stripe in (-12, 0, 12):

                pygame.draw.line(
                    screen,
                    (20, 115, 55),
                    (int(self.x + stripe), int(self.y - radius * 0.72)),
                    (int(self.x + stripe - 5), int(self.y + radius * 0.72)),
                    3
                )

            for seed_offset in (-10, 0, 10):
                pygame.draw.ellipse(
                    screen,
                    (18, 55, 36),
                    pygame.Rect(
                        int(self.x + seed_offset - 2),
                        int(self.y + radius * 0.18),
                        4,
                        7
                    )
                )

        elif self.name == "Guava":

            pygame.draw.ellipse(
                screen,
                (224, 245, 156),
                pygame.Rect(
                    int(self.x - radius * 0.55),
                    int(self.y - radius * 0.2),
                    int(radius * 1.1),
                    int(radius * 0.9)
                ),
                3
            )

            for seed_index in range(7):
                seed_angle = self.phase + seed_index * 0.9
                seed_x = int(self.x + math.cos(seed_angle) * radius * 0.42)
                seed_y = int(self.y + math.sin(seed_angle) * radius * 0.32)
                pygame.draw.circle(screen, (245, 238, 178), (seed_x, seed_y), 2)

        elif self.name == "Pineapple":

            for leaf_offset, leaf_height in ((-16, 18), (-8, 28), (0, 36), (8, 28), (16, 18)):

                pygame.draw.line(
                    screen,
                    (76, 174, 108),
                    (int(self.x + leaf_offset * 0.45), int(self.y - radius * 0.65)),
                    (int(self.x + leaf_offset), int(self.y - radius - leaf_height)),
                    5
                )

            for row in range(-1, 2):
                for column in range(-1, 2):
                    diamond_x = int(self.x + column * 11 + row * 5)
                    diamond_y = int(self.y + row * 13)
                    pygame.draw.line(
                        screen,
                        (169, 112, 34),
                        (diamond_x - 4, diamond_y),
                        (diamond_x, diamond_y - 4),
                        2
                    )
                    pygame.draw.line(
                        screen,
                        (169, 112, 34),
                        (diamond_x, diamond_y - 4),
                        (diamond_x + 4, diamond_y),
                        2
                    )

        # Highlight

        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(self.x - radius * 0.3),
                int(self.y - radius * 0.3)
            ),
            max(3, int(radius * 0.14))
        )

        # Stem

        pygame.draw.line(
            screen,
            (90, 50, 20),
            (
                int(self.x),
                int(self.y - radius)
            ),
            (
                int(self.x + 5),
                int(
                    self.y - radius - 12
                )
            ),
            4
        )


# ============================================================
# BOMB
# ============================================================

class Bomb:

    def __init__(self):

        self.x = random.randint(
            80,
            WIDTH - 80
        )

        self.y = HEIGHT + 50

        self.vx = random.uniform(
            -4,
            4
        )

        self.vy = random.uniform(
            -17,
            -13
        )

        self.gravity = 0.35

        self.radius = 30

        self.active = True


    def update(self):

        self.x += self.vx

        self.y += self.vy

        self.vy += self.gravity

        if self.y > HEIGHT + 100:

            self.active = False


    def draw(self):

        if not self.active:
            return

        pygame.draw.circle(
            screen,
            (35, 35, 35),
            (
                int(self.x),
                int(self.y)
            ),
            self.radius
        )

        # Highlight

        pygame.draw.circle(
            screen,
            GRAY,
            (
                int(self.x - 10),
                int(self.y - 10)
            ),
            7
        )

        # Fuse

        pygame.draw.line(
            screen,
            ORANGE,
            (
                int(self.x + 18),
                int(self.y - 22)
            ),
            (
                int(self.x + 30),
                int(self.y - 38)
            ),
            4
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (
                int(self.x + 32),
                int(self.y - 40)
            ),
            6
        )


# ============================================================
# COLLISION
# ============================================================

def line_circle_collision(
    x1,
    y1,
    x2,
    y2,
    cx,
    cy,
    radius
):

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:

        return (
            math.hypot(
                cx - x1,
                cy - y1
            )
            <= radius
        )

    t = (
        (cx - x1) * dx +
        (cy - y1) * dy
    ) / (
        dx * dx +
        dy * dy
    )

    t = max(
        0,
        min(1, t)
    )

    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    return (
        math.hypot(
            cx - closest_x,
            cy - closest_y
        )
        <= radius
    )


# ============================================================
# MEDIAPIPE HAND TRACKER
# ============================================================

class HandTracker:

    def __init__(self):

        if not os.path.exists(MODEL_PATH):

            raise FileNotFoundError(
                f"\nHand model not found!\n"
                f"Expected:\n{MODEL_PATH}\n\n"
                f"Download hand_landmarker.task "
                f"and place it inside the models folder."
            )

        BaseOptions = (
            mp.tasks.BaseOptions
        )

        HandLandmarker = (
            mp.tasks.vision.HandLandmarker
        )

        HandLandmarkerOptions = (
            mp.tasks.vision.HandLandmarkerOptions
        )

        VisionRunningMode = (
            mp.tasks.vision.RunningMode
        )

        options = HandLandmarkerOptions(

            base_options=BaseOptions(
                model_asset_path=MODEL_PATH
            ),

            running_mode=(
                VisionRunningMode.VIDEO
            ),

            num_hands=1,

            min_hand_detection_confidence=0.4,

            min_hand_presence_confidence=0.4,

            min_tracking_confidence=0.4
        )

        self.landmarker = (
            HandLandmarker.create_from_options(
                options
            )
        )

        self.timestamp = 0

        self.smoothed_point = None


    def detect(
        self,
        frame
    ):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=(
                mp.ImageFormat.SRGB
            ),
            data=rgb
        )

        self.timestamp = max(
            self.timestamp + 1,
            int(time.monotonic() * 1000)
        )

        result = self.landmarker.detect_for_video(
            mp_image,
            self.timestamp
        )

        if not result.hand_landmarks:

            self.smoothed_point = None

            return None

        hand = result.hand_landmarks[0]

        # Index fingertip = landmark 8

        fingertip = hand[8]

        height, width, _ = frame.shape

        x = int(
            fingertip.x * width
        )

        y = int(
            fingertip.y * height
        )

        if self.smoothed_point is None:

            self.smoothed_point = (x, y)

        else:

            smoothing = 0.45

            self.smoothed_point = (
                int(self.smoothed_point[0] * (1 - smoothing) + x * smoothing),
                int(self.smoothed_point[1] * (1 - smoothing) + y * smoothing)
            )

        return self.smoothed_point


    def close(self):

        self.landmarker.close()


# ============================================================
# TEXT
# ============================================================

def draw_text(
    text,
    font,
    color,
    x,
    y,
    center=False
):

    surface = font.render(
        text,
        True,
        color
    )

    if center:

        rect = surface.get_rect(
            center=(x, y)
        )

    else:

        rect = surface.get_rect(
            topleft=(x, y)
        )

    screen.blit(
        surface,
        rect
    )


# ============================================================
# BACKGROUND
# ============================================================

def draw_background():

    screen.fill((10, 15, 28))

    for y in range(HEIGHT):

        blend = y / HEIGHT

        color = (
            int(12 + 10 * blend),
            int(18 + 12 * blend),
            int(35 + 18 * blend)
        )

        pygame.draw.line(
            screen,
            color,
            (0, y),
            (WIDTH, y)
        )

    pygame.draw.circle(screen, (18, 48, 78), (WIDTH - 80, 100), 180)
    pygame.draw.circle(screen, (38, 32, 70), (90, HEIGHT - 50), 210)

    for y in range(
        0,
        HEIGHT,
        50
    ):

        pygame.draw.line(
            screen,
            (25, 40, 58),
            (0, y),
            (WIDTH, y),
            1
        )

    for x in range(-HEIGHT, WIDTH, 80):

        pygame.draw.line(
            screen,
            (18, 30, 48),
            (x, HEIGHT),
            (x + HEIGHT, 0),
            1
        )


def camera_transform(frame):

    frame_height, frame_width = frame.shape[:2]

    scale = max(
        WIDTH / frame_width,
        HEIGHT / frame_height
    )

    display_width = int(frame_width * scale)
    display_height = int(frame_height * scale)

    offset_x = (WIDTH - display_width) // 2
    offset_y = (HEIGHT - display_height) // 2

    return display_width, display_height, offset_x, offset_y


def camera_to_screen(camera_x, camera_y, frame):

    display_width, display_height, offset_x, offset_y = camera_transform(frame)

    return (
        int(camera_x * display_width / frame.shape[1] + offset_x),
        int(camera_y * display_height / frame.shape[0] + offset_y)
    )


def draw_camera_background(frame, overlay_alpha=0):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    display_width, display_height, offset_x, offset_y = camera_transform(frame)

    camera_surface = pygame.image.frombuffer(
        rgb.tobytes(),
        (frame.shape[1], frame.shape[0]),
        "RGB"
    )

    camera_surface = pygame.transform.smoothscale(
        camera_surface,
        (display_width, display_height)
    )

    screen.fill((8, 12, 20))
    screen.blit(camera_surface, (offset_x, offset_y))

    if overlay_alpha > 0:

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        overlay.fill((5, 10, 25, overlay_alpha))

        screen.blit(overlay, (0, 0))


def draw_glass_button(rect, label, accent=UI_ACCENT, hovered=False, icon=None):

    pulse = 1.0 + (0.018 if hovered else 0.0)
    draw_rect = rect.inflate(int(rect.width * (pulse - 1)), int(rect.height * (pulse - 1)))
    draw_rect.center = rect.center
    shadow = pygame.Surface((draw_rect.width + 18, draw_rect.height + 18), pygame.SRCALPHA)

    pygame.draw.rect(
        shadow,
        (0, 0, 0, 88 if hovered else 58),
        shadow.get_rect().move(5, 7),
        border_radius=16
    )
    screen.blit(shadow, (draw_rect.x - 9, draw_rect.y - 9))

    button = pygame.Surface(draw_rect.size, pygame.SRCALPHA)
    fill_alpha = 72 if not hovered else 112
    border_alpha = 128 if not hovered else 210
    pygame.draw.rect(
        button,
        (*UI_GLASS, fill_alpha),
        button.get_rect(),
        border_radius=14
    )
    pygame.draw.rect(
        button,
        (*accent, border_alpha),
        button.get_rect(),
        1,
        border_radius=14
    )
    pygame.draw.line(
        button,
        (255, 255, 255, 54 if not hovered else 92),
        (18, 2),
        (draw_rect.width - 18, 2),
        1
    )
    if hovered:
        pygame.draw.circle(button, (*accent, 28), (draw_rect.width - 20, draw_rect.height // 2), 24)

    screen.blit(button, draw_rect)
    text_surface = font_small.render(label, True, UI_TEXT)
    text_rect = text_surface.get_rect(center=draw_rect.center)
    if icon:
        icon_surface = font_small.render(icon, True, accent)
        icon_rect = icon_surface.get_rect(midright=(text_rect.left - 10, draw_rect.centery))
        screen.blit(icon_surface, icon_rect)
    screen.blit(text_surface, text_rect)


def draw_overlay(alpha):

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    overlay.fill((5, 8, 18, alpha))

    screen.blit(overlay, (0, 0))


def draw_panel(rect, fill=(17, 27, 44), border=CYAN, radius=18):
    shadow = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 72), shadow.get_rect().move(5, 8), border_radius=radius + 2)
    screen.blit(shadow, (rect.x - 10, rect.y - 10))

    glass = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(glass, (*fill, 150), glass.get_rect(), border_radius=radius)
    pygame.draw.rect(glass, (*border, 110), glass.get_rect(), 1, border_radius=radius)
    pygame.draw.line(
        glass,
        (255, 255, 255, 42),
        (radius, 2),
        (rect.width - radius, 2),
        1
    )
    screen.blit(glass, rect)


def draw_stat_card(rect, label, value):

    draw_panel(rect, fill=(16, 28, 42), border=(145, 190, 210), radius=14)
    draw_text(label, font_label, UI_MUTED, rect.x + 16, rect.y + 12)
    draw_text(value, font_stat, UI_TEXT, rect.x + 16, rect.y + 29)


def draw_section_label(text, x, y):

    draw_text(text, font_label, UI_MUTED, x, y)

def draw_hud(remaining_time):
    score_rect = pygame.Rect(WIDTH // 2 - 90, 18, 180, 58)
    draw_panel(score_rect, fill=(12, 25, 38), border=(145, 190, 210), radius=16)
    draw_section_label("SCORE", score_rect.x + 16, score_rect.y + 10)
    draw_text(str(score), font_medium, UI_TEXT, score_rect.x + 16, score_rect.y + 25)

    lives_rect = pygame.Rect(24, 22, 112, 44)
    draw_panel(lives_rect, fill=(12, 25, 38), border=(145, 190, 210), radius=14)
    draw_text("♥", font_medium, (255, 135, 145), lives_rect.x + 14, lives_rect.y + 7)
    draw_text(str(lives), font_small, UI_TEXT, lives_rect.x + 52, lives_rect.y + 13)

    time_rect = pygame.Rect(WIDTH - 136, 22, 112, 44)
    draw_panel(time_rect, fill=(12, 25, 38), border=(145, 190, 210), radius=14)
    timer_color = (255, 145, 155) if remaining_time <= 10 else UI_ACCENT
    draw_text("TIME", font_label, UI_MUTED, time_rect.x + 14, time_rect.y + 8)
    draw_text(f"{remaining_time:02d}", font_small, timer_color, time_rect.x + 65, time_rect.y + 12)

    if combo > 1:
        combo_rect = pygame.Rect(WIDTH // 2 + 108, 84, 138, 38)
        draw_panel(combo_rect, fill=(18, 39, 47), border=(125, 220, 190), radius=13)
        draw_text(f"COMBO  x{combo}", font_small, (175, 235, 210), combo_rect.centerx, combo_rect.centery, True)


# ============================================================
# BLADE TRAIL
# ============================================================

def draw_blade_trail(
    points
):

    if len(points) < 2:
        return

    glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for i in range(1, len(points)):

        x1, y1 = points[i - 1]

        x2, y2 = points[i]

        age = i / len(points)
        glow_alpha = int(18 + age * 54)
        line_width = max(1, int(1 + age * 2))

        pygame.draw.line(
            glow,
            (50, 220, 255, glow_alpha),
            (
                x1,
                y1
            ),
            (
                x2,
                y2
            ),
            line_width + 7
        )

    screen.blit(glow, (0, 0))

    for i in range(1, len(points)):

        x1, y1 = points[i - 1]
        x2, y2 = points[i]

        age = i / len(points)
        color = (int(150 + age * 105), int(220 + age * 35), 255)

        pygame.draw.circle(
            screen,
            color,
            (
                x2,
                y2
            ),
            max(1, int(1 + age * 2))
        )

        pygame.draw.line(
            screen,
            color,
            (x1, y1),
            (x2, y2),
            max(1, int(1 + age * 2))
        )

    tip_x, tip_y = points[-1]
    pygame.draw.circle(screen, (210, 248, 255), (tip_x, tip_y), 5)
    pygame.draw.circle(screen, (100, 220, 255), (tip_x, tip_y), 9, 1)


def draw_sword(points):

    global sword_direction

    if not points:
        return

    tip_x, tip_y = points[-1]

    if len(points) >= 4:
        previous_x, previous_y = points[-4]
    elif len(points) >= 2:
        previous_x, previous_y = points[-2]
    else:
        previous_x, previous_y = tip_x - sword_direction[0], tip_y - sword_direction[1]

    target_x = tip_x - previous_x
    target_y = tip_y - previous_y
    target_length = math.hypot(target_x, target_y)

    if target_length >= 2:
        target_x /= target_length
        target_y /= target_length
        direction_x = sword_direction[0] * 0.78 + target_x * 0.22
        direction_y = sword_direction[1] * 0.78 + target_y * 0.22
        direction_length = math.hypot(direction_x, direction_y)
        sword_direction = (
            direction_x / direction_length,
            direction_y / direction_length
        )

    direction_x, direction_y = sword_direction
    perpendicular_x = -direction_y
    perpendicular_y = direction_x

    blade_length = 102
    base_x = tip_x - direction_x * 24
    base_y = tip_y - direction_y * 24
    end_x = base_x + direction_x * blade_length
    end_y = base_y + direction_y * blade_length

    glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.line(
        glow,
        (70, 210, 255, 55),
        (int(base_x), int(base_y)),
        (int(end_x), int(end_y)),
        34
    )
    pygame.draw.line(
        glow,
        (190, 245, 255, 105),
        (int(base_x), int(base_y)),
        (int(end_x), int(end_y)),
        16
    )
    screen.blit(glow, (0, 0))

    shoulder_x = base_x + direction_x * 12
    shoulder_y = base_y + direction_y * 12
    tip_point = (
        int(end_x + direction_x * 14),
        int(end_y + direction_y * 14)
    )
    blade_polygon = [
        (int(base_x + perpendicular_x * 8), int(base_y + perpendicular_y * 8)),
        (int(shoulder_x + perpendicular_x * 5), int(shoulder_y + perpendicular_y * 5)),
        tip_point,
        (int(shoulder_x - perpendicular_x * 5), int(shoulder_y - perpendicular_y * 5)),
        (int(base_x - perpendicular_x * 8), int(base_y - perpendicular_y * 8))
    ]

    pygame.draw.polygon(screen, (205, 244, 255), blade_polygon)
    pygame.draw.line(
        screen,
        (115, 200, 235),
        (int(base_x - perpendicular_x * 8), int(base_y - perpendicular_y * 8)),
        tip_point,
        3
    )
    pygame.draw.line(
        screen,
        WHITE,
        (int(base_x + perpendicular_x * 4), int(base_y + perpendicular_y * 4)),
        tip_point,
        4
    )

    guard_center = (int(base_x), int(base_y))
    guard_start = (int(base_x - perpendicular_x * 19), int(base_y - perpendicular_y * 19))
    guard_end = (int(base_x + perpendicular_x * 19), int(base_y + perpendicular_y * 19))
    pygame.draw.line(screen, (45, 30, 18), guard_start, guard_end, 13)
    pygame.draw.line(screen, (255, 207, 78), guard_start, guard_end, 8)
    pygame.draw.circle(screen, (255, 246, 190), guard_center, 8)
    pygame.draw.circle(screen, ORANGE, guard_center, 4)

    handle_end = (int(base_x - direction_x * 45), int(base_y - direction_y * 45))
    pygame.draw.line(screen, (42, 24, 22), guard_center, handle_end, 15)
    pygame.draw.line(screen, (156, 76, 55), guard_center, handle_end, 10)

    for grip_step in range(4):
        grip_center_x = int(base_x - direction_x * (10 + grip_step * 10))
        grip_center_y = int(base_y - direction_y * (10 + grip_step * 10))
        pygame.draw.line(
            screen,
            (242, 173, 74),
            (int(grip_center_x - perpendicular_x * 7), int(grip_center_y - perpendicular_y * 7)),
            (int(grip_center_x + perpendicular_x * 7), int(grip_center_y + perpendicular_y * 7)),
            3
        )

    pommel = (int(handle_end[0] - direction_x * 5), int(handle_end[1] - direction_y * 5))
    pygame.draw.circle(screen, (42, 24, 22), pommel, 10)
    pygame.draw.circle(screen, ORANGE, pommel, 6)


# ============================================================
# RESET
# ============================================================

def reset_game():

    global fruits
    global bombs
    global particles
    global slice_effects

    global score
    global lives

    global combo
    global combo_timer
    global max_combo

    global game_start_time

    global blade_points
    global sword_direction

    fruits = []

    bombs = []

    particles = []

    slice_effects = []

    blade_points = []

    sword_direction = (1, -1)

    score = 0

    lives = START_LIVES

    combo = 0

    combo_timer = 0

    max_combo = 0

    game_start_time = time.time()


# ============================================================
# VARIABLES
# ============================================================

fruits = []

bombs = []

particles = []

slice_effects = []

blade_points = []

sword_direction = (1, -1)

score = 0

lives = START_LIVES

combo = 0

combo_timer = 0

max_combo = 0

game_start_time = 0

game_state = "MENU"

paused = False

last_spawn = time.time()

MENU_START_RECT = pygame.Rect(WIDTH // 2 - 132, 390, 264, 48)
MENU_SETTINGS_RECT = pygame.Rect(WIDTH // 2 - 132, 450, 264, 44)
MENU_EXIT_RECT = pygame.Rect(WIDTH // 2 - 132, 506, 264, 44)

PAUSE_RESUME_RECT = pygame.Rect(WIDTH // 2 - 132, 360, 264, 44)
PAUSE_RESTART_RECT = pygame.Rect(WIDTH // 2 - 132, 416, 264, 44)
PAUSE_QUIT_RECT = pygame.Rect(WIDTH // 2 - 132, 472, 264, 44)

GAMEOVER_AGAIN_RECT = pygame.Rect(WIDTH // 2 - 132, 430, 264, 44)
GAMEOVER_MENU_RECT = pygame.Rect(WIDTH // 2 - 132, 486, 264, 44)
GAMEOVER_EXIT_RECT = pygame.Rect(WIDTH // 2 - 132, 542, 264, 44)

settings_open = False


# ============================================================
# CAMERA
# ============================================================

camera = cv2.VideoCapture(0)

camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    640
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    480
)


if not camera.isOpened():

    print(
        "ERROR: Could not open webcam."
    )

    pygame.quit()

    raise SystemExit


# ============================================================
# HAND TRACKER
# ============================================================

try:

    tracker = HandTracker()

except Exception as e:

    print("\nERROR:", e)

    camera.release()

    pygame.quit()

    raise SystemExit


# ============================================================
# MAIN LOOP
# ============================================================

running = True


while running:

    clock.tick(FPS)


    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False


            if event.key == pygame.K_SPACE:

                if game_state == "MENU":

                    reset_game()

                    game_state = "PLAYING"

                    paused = False


                elif game_state == "PLAYING":

                    paused = not paused


                elif game_state == "GAMEOVER":

                    reset_game()

                    game_state = "PLAYING"

                    paused = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if game_state == "MENU":

                if MENU_START_RECT.collidepoint(event.pos):

                    reset_game()
                    game_state = "PLAYING"
                    paused = False

                elif MENU_SETTINGS_RECT.collidepoint(event.pos):

                    settings_open = not settings_open

                elif MENU_EXIT_RECT.collidepoint(event.pos):

                    running = False

            elif game_state == "PLAYING" and paused:

                if PAUSE_RESUME_RECT.collidepoint(event.pos):

                    paused = False

                elif PAUSE_RESTART_RECT.collidepoint(event.pos):

                    reset_game()
                    paused = False

                elif PAUSE_QUIT_RECT.collidepoint(event.pos):

                    game_state = "MENU"
                    paused = False

            elif game_state == "GAMEOVER":

                if GAMEOVER_AGAIN_RECT.collidepoint(event.pos):

                    reset_game()
                    game_state = "PLAYING"
                    paused = False

                elif GAMEOVER_MENU_RECT.collidepoint(event.pos):

                    game_state = "MENU"

                elif GAMEOVER_EXIT_RECT.collidepoint(event.pos):

                    running = False


    # --------------------------------------------------------
    # CAMERA
    # --------------------------------------------------------

    success, frame = camera.read()

    if not success:
        continue

    frame = cv2.flip(
        frame,
        1
    )


    # --------------------------------------------------------
    # HAND
    # --------------------------------------------------------

    fingertip = tracker.detect(
        frame
    )

    hand_position = None

    if fingertip:

        camera_x, camera_y = fingertip

        hand_position = camera_to_screen(
            camera_x,
            camera_y,
            frame
        )


    # ========================================================
    # MENU
    # ========================================================

    if game_state == "MENU":

        draw_camera_background(frame, 125)

        menu_panel = pygame.Rect(WIDTH // 2 - 210, 92, 420, 500)
        draw_panel(menu_panel, fill=(9, 20, 32), border=(150, 190, 208), radius=26)
        draw_section_label("COMPUTER VISION GAME", menu_panel.x + 38, menu_panel.y + 34)
        draw_text("GESTURE", font_large, UI_TEXT, menu_panel.x + 38, menu_panel.y + 70)
        draw_text("FRUIT NINJA", font_large, UI_ACCENT, menu_panel.x + 38, menu_panel.y + 116)
        draw_text("CUT WITH YOUR HAND", font_small, UI_MUTED, menu_panel.x + 40, menu_panel.y + 176)

        pygame.draw.line(
            screen,
            (160, 195, 210),
            (menu_panel.x + 38, menu_panel.y + 214),
            (menu_panel.right - 38, menu_panel.y + 214),
            1
        )
        draw_text("CAMERA READY", font_label, (168, 225, 190), menu_panel.x + 40, menu_panel.y + 232)
        draw_text("Index finger tracking enabled", font_small, UI_MUTED, menu_panel.x + 40, menu_panel.y + 252)

        mouse_position = pygame.mouse.get_pos()

        draw_glass_button(
            MENU_START_RECT,
            "START",
            UI_ACCENT,
            MENU_START_RECT.collidepoint(mouse_position),
            ">"
        )

        draw_glass_button(
            MENU_SETTINGS_RECT,
            "SETTINGS",
            UI_ACCENT,
            MENU_SETTINGS_RECT.collidepoint(mouse_position),
            "*"
        )

        draw_glass_button(
            MENU_EXIT_RECT,
            "EXIT",
            RED,
            MENU_EXIT_RECT.collidepoint(mouse_position),
            "x"
        )

        draw_text(
            f"BEST SCORE  {high_score}",
            font_label,
            UI_MUTED,
            menu_panel.x + 40,
            menu_panel.bottom - 28
        )

        if settings_open:

            draw_panel(
                pygame.Rect(menu_panel.right + 18, 210, 210, 132),
                fill=(10, 22, 36),
                border=UI_ACCENT,
                radius=18
            )

            draw_section_label("SETTINGS", menu_panel.right + 36, 232)
            draw_text("CAMERA  640 x 480", font_small, UI_TEXT, menu_panel.right + 36, 265)
            draw_text("BLADE  RESPONSIVE", font_small, (175, 235, 210), menu_panel.right + 36, 294)

        pygame.display.flip()

        continue


    # ========================================================
    # GAME OVER
    # ========================================================

    if game_state == "GAMEOVER":

        draw_camera_background(frame, 175)

        result_panel = pygame.Rect(WIDTH // 2 - 185, 76, 370, 570)
        draw_panel(result_panel, fill=(9, 19, 31), border=(150, 190, 208), radius=26)
        draw_section_label("RUN COMPLETE", result_panel.x + 36, result_panel.y + 34)
        draw_text("GAME OVER", font_medium, UI_TEXT, result_panel.x + 36, result_panel.y + 62)
        pygame.draw.line(
            screen,
            (155, 190, 205),
            (result_panel.x + 36, result_panel.y + 104),
            (result_panel.right - 36, result_panel.y + 104),
            1
        )
        draw_section_label("SCORE", result_panel.x + 36, result_panel.y + 130)
        draw_text(str(score), font_huge, UI_TEXT, result_panel.x + 36, result_panel.y + 146)

        stat_width = (result_panel.width - 92) // 2
        draw_stat_card(
            pygame.Rect(result_panel.x + 36, result_panel.y + 235, stat_width, 72),
            "BEST SCORE",
            str(high_score)
        )
        draw_stat_card(
            pygame.Rect(result_panel.x + 48 + stat_width, result_panel.y + 235, stat_width, 72),
            "MAX COMBO",
            f"x{max_combo}"
        )

        mouse_position = pygame.mouse.get_pos()

        draw_glass_button(
            GAMEOVER_AGAIN_RECT,
            "PLAY AGAIN",
            UI_ACCENT,
            GAMEOVER_AGAIN_RECT.collidepoint(mouse_position),
            ">"
        )

        draw_glass_button(
            GAMEOVER_MENU_RECT,
            "MAIN MENU",
            UI_ACCENT,
            GAMEOVER_MENU_RECT.collidepoint(mouse_position),
            "^"
        )

        draw_glass_button(
            GAMEOVER_EXIT_RECT,
            "EXIT",
            RED,
            GAMEOVER_EXIT_RECT.collidepoint(mouse_position),
            "x"
        )

        pygame.display.flip()

        continue


    # ========================================================
    # PAUSE
    # ========================================================

    if paused:

        draw_camera_background(frame, 150)

        pause_panel = pygame.Rect(WIDTH // 2 - 170, 138, 340, 390)
        draw_panel(pause_panel, fill=(9, 19, 31), border=(150, 190, 208), radius=24)
        draw_section_label("SESSION CONTROL", pause_panel.x + 34, pause_panel.y + 34)
        draw_text("PAUSED", font_large, UI_TEXT, pause_panel.x + 34, pause_panel.y + 70)
        draw_text("Your run is safely on hold", font_small, UI_MUTED, pause_panel.x + 36, pause_panel.y + 125)

        mouse_position = pygame.mouse.get_pos()

        draw_glass_button(
            PAUSE_RESUME_RECT,
            "RESUME",
            UI_ACCENT,
            PAUSE_RESUME_RECT.collidepoint(mouse_position),
            ">"
        )

        draw_glass_button(
            PAUSE_RESTART_RECT,
            "RESTART",
            UI_ACCENT,
            PAUSE_RESTART_RECT.collidepoint(mouse_position),
            "↻"
        )

        draw_glass_button(
            PAUSE_QUIT_RECT,
            "MAIN MENU",
            RED,
            PAUSE_QUIT_RECT.collidepoint(mouse_position),
            "^"
        )

        pygame.display.flip()

        continue


    # ========================================================
    # GAME TIME
    # ========================================================

    current_time = time.time()

    elapsed = (
        current_time -
        game_start_time
    )

    remaining_time = max(
        0,
        int(
            GAME_TIME -
            elapsed
        )
    )


    # ========================================================
    # DIFFICULTY
    # ========================================================

    difficulty = 1 + (
        score // 100
    )

    spawn_delay = max(
        0.25,
        0.65 -
        difficulty * 0.03
    )


    # ========================================================
    # SPAWN
    # ========================================================

    if (
        current_time -
        last_spawn
        >
        spawn_delay
    ):

        last_spawn = current_time

        data = random.choice(
            FRUITS
        )

        fruits.append(
            Fruit(data)
        )

        bomb_chance = (
            0.12 +
            difficulty * 0.01
        )

        if random.random() < bomb_chance:

            bombs.append(
                Bomb()
            )


    # ========================================================
    # UPDATE
    # ========================================================

    for fruit in fruits:

        fruit.update()


    for bomb in bombs:

        bomb.update()


    # ========================================================
    # BLADE
    # ========================================================

    previous_point = None

    if blade_points:

        previous_point = (
            blade_points[-1]
        )


    if hand_position:

        blade_points.append(
            hand_position
        )

        if len(blade_points) > 15:

            blade_points.pop(0)

    else:

        blade_points.clear()
        sword_direction = (1, -1)


    # ========================================================
    # FRUIT COLLISION
    # ========================================================

    if len(blade_points) >= 2:

        for fruit in fruits:

            if not fruit.active:
                continue

            hit = any(
                line_circle_collision(
                    blade_points[index - 1][0],
                    blade_points[index - 1][1],
                    blade_points[index][0],
                    blade_points[index][1],
                    fruit.x,
                    fruit.y,
                    fruit.radius + BLADE_RADIUS
                )
                for index in range(1, len(blade_points))
            )

            if hit:

                fruit.active = False

                slice_effects.append(
                    FruitSliceEffect(
                        fruit.x,
                        fruit.y,
                        fruit.color,
                        fruit.radius
                    )
                )

                combo += 1

                max_combo = max(
                    max_combo,
                    combo
                )

                combo_timer = time.time()

                multiplier = min(
                    combo,
                    10
                )

                score += (
                    fruit.score *
                    multiplier
                )

                for _ in range(20):

                    particles.append(
                        Particle(
                            fruit.x,
                            fruit.y,
                            fruit.color
                        )
                    )

    # ========================================================
    # BOMB COLLISION
    # ========================================================

    if len(blade_points) >= 2:

        for bomb in bombs:

            if not bomb.active:
                continue

            hit = any(
                line_circle_collision(
                    blade_points[index - 1][0],
                    blade_points[index - 1][1],
                    blade_points[index][0],
                    blade_points[index][1],
                    bomb.x,
                    bomb.y,
                    bomb.radius + BLADE_RADIUS
                )
                for index in range(1, len(blade_points))
            )

            if hit:

                bomb.active = False

                lives -= 1

                combo = 0

                for _ in range(35):

                    particles.append(
                        Particle(
                            bomb.x,
                            bomb.y,
                            ORANGE
                        )
                    )

                if lives <= 0:

                    if score > high_score:

                        high_score = score

                        save_high_score(
                            high_score
                        )

                    game_state = "GAMEOVER"


    # ========================================================
    # COMBO TIMER
    # ========================================================

    if combo > 0:

        if (
            time.time() -
            combo_timer
            > 2
        ):

            combo = 0


    # ========================================================
    # PARTICLES
    # ========================================================

    for particle in particles:

        particle.update()


    for slice_effect in slice_effects:

        slice_effect.update()


    particles = [
        p
        for p in particles
        if p.life > 0
    ]

    slice_effects = [
        effect
        for effect in slice_effects
        if effect.life > 0
    ]


    # ========================================================
    # CLEANUP
    # ========================================================

    fruits = [
        f
        for f in fruits
        if f.active
    ]

    bombs = [
        b
        for b in bombs
        if b.active
    ]


    # ========================================================
    # TIME OVER
    # ========================================================

    if remaining_time <= 0:

        if score > high_score:

            high_score = score

            save_high_score(
                high_score
            )

        game_state = "GAMEOVER"


    # ========================================================
    # DRAW
    # ========================================================

    draw_camera_background(frame)


    for fruit in fruits:

        fruit.draw()


    for bomb in bombs:

        bomb.draw()


    for particle in particles:

        particle.draw()


    for slice_effect in slice_effects:

        slice_effect.draw()


    draw_blade_trail(
        blade_points
    )

    draw_sword(
        blade_points
    )

    draw_hud(remaining_time)

    draw_text(
        "ESC  |  QUIT",
        font_small,
        (120, 145, 165),
        28,
        HEIGHT - 38
    )

    pygame.display.flip()


    # ========================================================
    # UI
    # ======


tracker.close()
camera.release()
pygame.quit()

