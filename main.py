import cv2
import numpy as np
import os

from hand_tracking import HandTracker
from game import Game
from ui import *
from sound import play_music
from story import story_data

# Ẩn warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# ===== LOAD IMAGE =====
def load_img(path, size):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"❌ Không load được: {path}")
        return None
    return cv2.resize(img, size)

# ===== BACKGROUND =====
bg = cv2.imread("assets/bg.jpg")
if bg is None:
    print("⚠️ Không có bg.jpg → dùng nền mặc định")
    bg = np.zeros((480,640,3), dtype="uint8")
    bg[:] = (30,30,30)
else:
    bg = cv2.resize(bg,(640,480))

# ===== LOAD ITEM =====
money_img = load_img("assets/money.png",(40,40))
bomb_img  = load_img("assets/bomb.png",(40,40))
star_img  = load_img("assets/star.png",(40,40))
speed_img = load_img("assets/speed.png",(40,40))
basket_img= load_img("assets/basket.png",(100,50))

# ===== DRAW PNG =====
def draw_png(frame, img, x, y):
    if img is None:
        return

    x, y = int(x), int(y)
    h, w = img.shape[:2]

    if x < 0 or y < 0 or x+w > 640 or y+h > 480:
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

# ===== SCORE =====
def load_score():
    try:
        return int(open("data.txt").read())
    except:
        return 0

def save_score(score):
    open("data.txt","w").write(str(score))

# ===== INIT =====
cap = cv2.VideoCapture(0)
tracker = HandTracker()
game = Game(640,480)

state = "menu"
highscore = load_score()

# ===== STORY =====
story_index = 0
current_story = []

play_music()

# ===== MOUSE =====
mouse_x,mouse_y = 0,0
clicked = False

def mouse_event(event,x,y,flags,param):
    global mouse_x,mouse_y,clicked
    mouse_x,mouse_y = x,y
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True

cv2.namedWindow("Money Game")
cv2.setMouseCallback("Money Game",mouse_event)

# ===== LOOP =====
while True:
    frame = bg.copy()

    # ===== MENU =====
    if state == "menu":
        draw_menu(frame)

        if clicked:
            btn = check_click(mouse_x,mouse_y)

            if btn == "VO TAN":
                game.mode = "endless"
                game.reset()
                state = "play"

            elif btn == "THEO MAN":
                game.mode = "level"
                state = "level_select"

            elif btn == "HUONG DAN":
                state = "guide"

            clicked = False

    # ===== CHỌN MÀN =====
    elif state == "level_select":
        draw_level_select(frame)

        if clicked:
            btn = check_click(mouse_x,mouse_y)

            if btn in ["MAN 1","MAN 2","MAN 3"]:
                game.level = int(btn[-1])

                # 👉 load story trước khi chơi
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
                if check_click(mouse_x,mouse_y) == "TIEP":
                    story_index += 1
                clicked = False
        else:
            game.reset()
            state = "play"

    # ===== HƯỚNG DẪN =====
    elif state == "guide":
        draw_guide(frame)

        if clicked:
            if check_click(mouse_x,mouse_y) == "QUAY LAI":
                state = "menu"
            clicked = False

    # ===== GAME =====
    elif state == "play":
        ret, cam = cap.read()
        if not ret:
            print("❌ Không đọc được camera")
            break

        cam = cv2.flip(cam,1)

        x = tracker.get_x(cam)
        if x is not None:
            if hasattr(game, "speed_boost") and game.speed_boost:
                game.basket_x += (x - game.basket_x) * 0.5
            else:
                game.basket_x = x

        game.update()

        # ===== VẼ ITEM =====
        for item in game.items:
            if item["type"] == "money":
                draw_png(frame, money_img, item["x"], item["y"])
            elif item["type"] == "bomb":
                draw_png(frame, bomb_img, item["x"], item["y"])
            elif item["type"] == "star":
                draw_png(frame, star_img, item["x"], item["y"])
            elif item["type"] == "speed":
                draw_png(frame, speed_img, item["x"], item["y"])

        # ===== VẼ GIỎ =====
        draw_png(frame, basket_img, game.basket_x - 50, 420)

        draw_game(frame, game)

        # ===== WIN =====
        if game.mode == "level":
            if game.is_win():
                game.level += 1

                if game.level > 4:
                    # 👉 ENDING STORY
                    current_story = story_data.get("ending", [])
                    story_index = 0
                    state = "story_end"
                else:
                    # 👉 STORY MÀN TIẾP
                    current_story = story_data.get(game.level, [])
                    story_index = 0
                    state = "story"

            elif game.get_time_left() <= 0:
                state = "over"

    # ===== ENDING =====
    elif state == "story_end":
        if story_index < len(current_story):
            speaker, text = current_story[story_index]
            draw_story(frame, speaker, text, story_index, len(current_story))

            if clicked:
                if check_click(mouse_x,mouse_y) == "TIEP":
                    story_index += 1
                clicked = False
        else:
            if game.score > highscore:
                highscore = game.score
                save_score(highscore)
            state = "menu"

    # ===== GAME OVER =====
    elif state == "over":
        draw_gameover(frame, game.score, highscore)

        if clicked:
            if check_click(mouse_x,mouse_y) == "CHOI LAI":
                state = "menu"
            clicked = False

    # ===== SHOW =====
    cv2.imshow("Money Game", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()