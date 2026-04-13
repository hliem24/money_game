import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

buttons = {}

# ===== FONT =====
FONT_PATH = "arial.ttf"

def draw_text_vn(frame, text, x, y, size=30, color=(255,255,255)):
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)

    try:
        font = ImageFont.truetype(FONT_PATH, size)
    except:
        font = ImageFont.load_default()

    draw.text((x, y), text, font=font, fill=color)
    return np.array(img_pil)

# ===== LOAD ICON =====
def load_icon(path, size):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"⚠️ Không load được {path}")
        return None
    return cv2.resize(img, size)

# ===== ICON =====
money_icon  = load_icon("assets/money.png",(40,40))
bomb_icon   = load_icon("assets/bomb.png",(40,40))
star_icon   = load_icon("assets/star.png",(40,40))
speed_icon  = load_icon("assets/speed.png",(40,40))
freeze_icon = load_icon("assets/freeze.png",(40,40))
attack_icon = load_icon("assets/attack.png",(40,40))
basket_icon = load_icon("assets/basket.png",(80,40))
heart_icon  = load_icon("assets/heart.png",(35,35))

# ===== AVATAR =====
hero_img  = load_icon("assets/hero.png",(120,120))
guide_img = load_icon("assets/guide.png",(120,120))
enemy_img = load_icon("assets/enemy.png",(120,120))

def get_avatar(name):
    if name == "hero": return hero_img
    if name == "guide": return guide_img
    if name == "enemy": return enemy_img
    return None

# ===== DRAW PNG =====
def draw_png(frame, img, x, y):
    if img is None:
        return

    x, y = int(x), int(y)
    h, w = img.shape[:2]

    if x < 0 or y < 0 or x+w > frame.shape[1] or y+h > frame.shape[0]:
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

# ===== BUTTON =====
def draw_button(frame, text, x, y, w, h, mouse_pos=None):
    hover = False

    if mouse_pos:
        mx, my = mouse_pos
        if x < mx < x+w and y < my < y+h:
            hover = True

    color = (80,80,80) if hover else (30,30,30)

    cv2.rectangle(frame, (x,y), (x+w,y+h), color, -1)
    cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,255), 2)

    frame[:] = draw_text_vn(frame, text, x+20, y+15, 28)

    buttons[text] = (x,y,w,h)

def check_click(x,y):
    for name,(bx,by,bw,bh) in buttons.items():
        if bx < x < bx+bw and by < y < by+bh:
            return name
    return None

# ===== MENU =====
def draw_menu(frame, mouse_pos=None):
    buttons.clear()
    h, w = frame.shape[:2]

    frame[:] = draw_text_vn(frame,"GAME HỨNG TIỀN", w//2 - 200,120,50,(0,255,255))

    draw_button(frame,"VÔ TẬN",w//2 - 100,200,200,60, mouse_pos)
    draw_button(frame,"THEO MÀN",w//2 - 100,280,200,60, mouse_pos)
    draw_button(frame,"HƯỚNG DẪN",w//2 - 100,360,200,60, mouse_pos)

# ===== LEVEL =====
def draw_level_select(frame, mouse_pos=None):
    buttons.clear()
    h, w = frame.shape[:2]

    frame[:] = draw_text_vn(frame,"CHỌN MÀN", w//2 - 120,120,45,(0,255,0))

    draw_button(frame,"MÀN 1",w//2 - 100,200,200,60, mouse_pos)
    draw_button(frame,"MÀN 2",w//2 - 100,280,200,60, mouse_pos)
    draw_button(frame,"MÀN 3",w//2 - 100,360,200,60, mouse_pos)
    draw_button(frame,"MÀN 4",w//2 - 100,440,200,60, mouse_pos)

# ===== GUIDE =====
def draw_guide(frame, mouse_pos=None):
    buttons.clear()
    h, w = frame.shape[:2]

    frame[:] = draw_text_vn(frame,"HƯỚNG DẪN", w//2 - 120,80,40,(0,255,255))

    y = 150

    def row(icon, text):
        nonlocal y
        draw_png(frame, icon, w//2 - 200, y)
        frame[:] = draw_text_vn(frame, text, w//2 - 140, y+10, 28)
        y += 60

    row(basket_icon, "Di chuyển tay")
    row(money_icon, "Tiền +1")
    row(star_icon, "Sao +2")
    row(bomb_icon, "Bom -1 tim")
    row(speed_icon, "Tăng tốc")

    draw_button(frame,"QUAY LẠI",w//2 - 100, h - 120,200,60, mouse_pos)

# ===== STORY =====
def draw_story(frame, speaker, text, index, total, mouse_pos=None):
    buttons.clear()
    h, w = frame.shape[:2]

    cv2.rectangle(frame,(w//2 - 320,300),(w//2 + 320,500),(0,0,0),-1)
    cv2.rectangle(frame,(w//2 - 320,300),(w//2 + 320,500),(255,255,255),2)

    avatar = get_avatar(speaker)
    if avatar is not None:
        draw_png(frame, avatar, w//2 - 300, 320)

    frame[:] = draw_text_vn(frame, speaker.upper(), w//2 - 120, 330, 25,(0,255,255))
    frame[:] = draw_text_vn(frame, text, w//2 - 120, 370, 28)

    frame[:] = draw_text_vn(frame, f"{index+1}/{total}", w//2 + 230,470,20,(200,200,200))

    draw_button(frame,"TIẾP",w//2 + 150,440,120,40, mouse_pos)

# ===== GAME =====
def draw_game(frame, game):
    frame[:] = draw_text_vn(frame,f"Điểm: {game.score}",20,20,30)

    for i in range(game.hp):
        draw_png(frame, heart_icon, 20 + i*40, 60)

    draw_png(frame, attack_icon, 20, 110)
    frame[:] = draw_text_vn(frame, f"x {len(game.projectiles)}", 60,120,25,(0,255,255))

    frame[:] = draw_text_vn(frame,f"Màn: {game.level}",20,160,30,(0,255,0))

    # ===== THÊM PHẦN NÀY =====
    if not game.boss_mode:
        frame[:] = draw_text_vn(
            frame,
            f"Thời gian: {max(0, game.get_time_left())}",
            20,200,30,(0,0,255)
        )

        frame[:] = draw_text_vn(
            frame,
            f"Mục tiêu: {game.target}",
            20,240,30,(255,255,0)
        )
    else:
        frame[:] = draw_text_vn(
            frame,
            "BOSS FIGHT!",
            500,60,35,(0,0,255)
        )

# ===== GAME OVER =====
def draw_gameover(frame,score,highscore, mouse_pos=None):
    buttons.clear()
    h, w = frame.shape[:2]

    frame[:] = draw_text_vn(frame,"THUA RỒI!", w//2 - 140,180,50,(0,0,255))
    frame[:] = draw_text_vn(frame,f"Điểm: {score}", w//2 - 100,240,35)
    frame[:] = draw_text_vn(frame,f"Điểm cao: {highscore}", w//2 - 130,280,30,(0,255,255))

    draw_button(frame,"CHƠI LẠI",w//2 - 100,330,200,60, mouse_pos)