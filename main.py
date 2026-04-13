import cv2
import numpy as np
import os
import ctypes
import time

from hand_tracking import HandTracker
from game import Game
from ui import *
from sound import play_music
from story import story_data

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# ===== FULL SCREEN =====
user32 = ctypes.windll.user32
SCREEN_W = user32.GetSystemMetrics(0)
SCREEN_H = user32.GetSystemMetrics(1)

# ===== LOAD IMAGE =====
def load_img(path, size):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"❌ Không load được: {path}")
        return None
    return cv2.resize(img, size)

# ===== BACKGROUND THEO MÀN =====
def load_bg(path):
    img = cv2.imread(path)
    if img is None:
        print(f"⚠️ Không load được bg: {path}")
        img = np.zeros((SCREEN_H, SCREEN_W, 3), dtype="uint8")
        img[:] = (30,30,30)
    return cv2.resize(img, (SCREEN_W, SCREEN_H))

bg_list = {
    1: load_bg("assets/bg1.png"),
    2: load_bg("assets/bg2.png"),
    3: load_bg("assets/bg3.png"),
    4: load_bg("assets/bg4.png"),
}

bg_menu = load_bg("assets/bg_menu.png")

# ===== LOAD ITEM =====
money_img  = load_img("assets/money.png",(60,60))
bomb_img   = load_img("assets/bomb.png",(60,60))
star_img   = load_img("assets/star.png",(60,60))
speed_img  = load_img("assets/speed.png",(60,60))
freeze_img = load_img("assets/freeze.png",(60,60))
attack_img = load_img("assets/attack.png",(60,60))
basket_img = load_img("assets/basket.png",(150,80))
boss_img   = load_img("assets/boss.png",(200,150))

# ===== DRAW PNG =====
def draw_png(frame, img, x, y):
    if img is None:
        return

    x, y = int(x), int(y)
    h, w = img.shape[:2]

    if x < 0 or y < 0 or x+w > SCREEN_W or y+h > SCREEN_H:
        return

    if img.shape[2] == 4:
        alpha = img[:,:,3] / 255.0
        for c in range(3):
            frame[y:y+h, x:x+w, c] = (
                alpha * img[:,:,c] +
                (1-alpha) * frame[y:y+h, x:x+w, c]
            )
    else:
        frame[y:y+h, x:x+w] = img

# ===== INIT =====
cap = cv2.VideoCapture(0)
tracker = HandTracker()
game = Game(SCREEN_W, SCREEN_H)

smooth_x = SCREEN_W // 2
SMOOTHING = 0.2

# ===== STATE =====
state = "menu"
story_index = 0
current_story = []

play_music()

mouse_x,mouse_y = 0,0
clicked = False

def mouse_event(event,x,y,flags,param):
    global mouse_x,mouse_y,clicked
    mouse_x,mouse_y = x,y
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True

cv2.namedWindow("Money Game", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Money Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback("Money Game",mouse_event)

# ===== LOOP =====
while True:

    # ===== CHỌN BACKGROUND =====
    if state == "menu":
        frame = bg_menu.copy()
    else:
        frame = bg_list.get(game.level, bg_list[1]).copy()

    # ===== MENU =====
    if state == "menu":
        draw_menu(frame, (mouse_x, mouse_y))

        if clicked:
            btn = check_click(mouse_x,mouse_y)

            if btn == "VÔ TẬN":
                game.mode = "endless"
                game.reset()
                state = "play"

            elif btn == "THEO MÀN":
                game.mode = "level"
                state = "level_select"

            elif btn == "HƯỚNG DẪN":
                state = "guide"

            clicked = False

    # ===== LEVEL SELECT =====
    elif state == "level_select":
        draw_level_select(frame, (mouse_x, mouse_y))

        if clicked:
            btn = check_click(mouse_x,mouse_y)

            if btn in ["MÀN 1","MÀN 2","MÀN 3","MÀN 4"]:
                game.level = int(btn[-1])

                current_story = story_data.get(game.level, [])
                story_index = 0
                state = "story"

            clicked = False

    # ===== STORY =====
    elif state == "story":
        if story_index < len(current_story):
            speaker, text = current_story[story_index]
            draw_story(frame, speaker, text, story_index, len(current_story))

            if clicked:
                if check_click(mouse_x,mouse_y) == "TIẾP":
                    story_index += 1
                clicked = False
        else:
            game.reset()
            state = "play"

    # ===== GUIDE =====
    elif state == "guide":
        draw_guide(frame, (mouse_x, mouse_y))

        if clicked:
            if check_click(mouse_x,mouse_y) == "QUAY LẠI":
                state = "menu"
            clicked = False

    # ===== PLAY =====
    elif state == "play":
        ret, cam = cap.read()
        if not ret:
            break

        cam = cv2.flip(cam,1)
        x = tracker.get_x(cam)

        if x is not None:
            cam_w = cam.shape[1]
            x = int(x * SCREEN_W / cam_w)

            smooth_x = int(smooth_x * (1 - SMOOTHING) + x * SMOOTHING)

            speed = 0.3 if not game.speed_boost else 0.6
            game.basket_x += (smooth_x - game.basket_x) * speed
            game.basket_x = max(0, min(SCREEN_W, game.basket_x))

        game.update()

        # ===== ITEM =====
        for item in game.items:
            draw_png(frame, {
                "money": money_img,
                "bomb": bomb_img,
                "star": star_img,
                "speed": speed_img,
                "freeze": freeze_img,
                "attack": attack_img
            }[item["type"]], item["x"], item["y"])

        # ===== ĐẠN =====
        for p in game.projectiles:
            cv2.circle(frame, (int(p["x"]), int(p["y"])), 8, (0,255,255), -1)

        # ===== BOSS =====
        if game.boss_mode:
            # làm tối nền
            frame = (frame * 0.5).astype(np.uint8)

            draw_png(frame, boss_img, game.boss_x - 100, 50)

            bar_w = 300
            x1 = SCREEN_W//2 - bar_w//2

            cv2.rectangle(frame,(x1,20),(x1+bar_w,40),(80,80,80),-1)
            cv2.rectangle(frame,(x1,20),
                          (x1 + int(bar_w * game.boss_hp / 20),40),
                          (0,0,255),-1)

            for b in game.enemy_bullets:
                cv2.circle(frame, (int(b["x"]), int(b["y"])), 10, (0,0,255), -1)

        draw_png(frame, basket_img, game.basket_x - 75, SCREEN_H - 100)
        draw_game(frame, game)

        # ===== WIN =====
        if game.is_win():
            game.level += 1

            if game.level > 4:
                current_story = story_data.get("ending", [])
                story_index = 0
                state = "story_end"
            else:
                current_story = story_data.get(game.level, [])
                story_index = 0
                state = "story"

        # ===== LOSE =====
        if game.is_dead() or game.is_time_up():
            state = "over"

    # ===== ENDING =====
    elif state == "story_end":
        if story_index < len(current_story):
            speaker, text = current_story[story_index]
            draw_story(frame, speaker, text, story_index, len(current_story))

            if clicked:
                if check_click(mouse_x,mouse_y) == "TIẾP":
                    story_index += 1
                clicked = False
        else:
            state = "menu"

    # ===== GAME OVER =====
    elif state == "over":
        draw_gameover(frame, game.score, 0, (mouse_x, mouse_y))

        if clicked:
            if check_click(mouse_x,mouse_y) == "CHƠI LẠI":
                state = "menu"
            clicked = False

    cv2.imshow("Money Game", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()