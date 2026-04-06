import cv2

buttons = {}

# ===== LOAD ICON =====
def load_icon(path, size):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"⚠️ Không load được {path}")
        return None
    return cv2.resize(img, size)

# ===== ICON =====
money_icon = load_icon("assets/money.png",(40,40))
bomb_icon  = load_icon("assets/bomb.png",(40,40))
star_icon  = load_icon("assets/star.png",(40,40))
speed_icon = load_icon("assets/speed.png",(40,40))
basket_icon= load_icon("assets/basket.png",(80,40))

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
def draw_button(frame, text, x, y, w, h):
    cv2.rectangle(frame, (x,y), (x+w,y+h), (40,40,40), -1)
    cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,255), 2)

    cv2.putText(frame, text, (x+15,y+40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    buttons[text] = (x,y,w,h)

def check_click(x,y):
    for name,(bx,by,bw,bh) in buttons.items():
        if bx < x < bx+bw and by < y < by+bh:
            return name
    return None

# ===== MENU =====
def draw_menu(frame):
    buttons.clear()

    cv2.putText(frame,"GAME HUNG TIEN",(120,120),
                cv2.FONT_HERSHEY_SIMPLEX,1.4,(0,255,255),3)

    draw_button(frame,"VO TAN",220,180,200,60)
    draw_button(frame,"THEO MAN",220,260,200,60)
    draw_button(frame,"HUONG DAN",220,340,200,60)

# ===== CHON LEVEL =====
def draw_level_select(frame):
    buttons.clear()

    cv2.putText(frame,"CHON MAN",(170,120),
                cv2.FONT_HERSHEY_SIMPLEX,1.4,(0,255,0),3)

    draw_button(frame,"MAN 1",220,180,200,60)
    draw_button(frame,"MAN 2",220,260,200,60)
    draw_button(frame,"MAN 3",220,340,200,60)

# ===== HUONG DAN =====
def draw_guide(frame):
    buttons.clear()

    cv2.putText(frame,"HUONG DAN",(200,80),
                cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,255),2)

    draw_png(frame, basket_icon, 80,120)
    cv2.putText(frame,"Di chuyen tay de dieu khien gio",
                (150,150), cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

    draw_png(frame, money_icon, 80,170)
    cv2.putText(frame,"Tien +1 diem",
                (150,200), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)

    draw_png(frame, star_icon, 80,220)
    cv2.putText(frame,"Sao +2 diem",
                (150,250), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)

    draw_png(frame, bomb_icon, 80,270)
    cv2.putText(frame,"Bom -5 diem",
                (150,300), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

    draw_png(frame, speed_icon, 80,320)
    cv2.putText(frame,"Tang toc (⚡)",
                (150,350), cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2)

    draw_button(frame,"QUAY LAI",220,400,200,50)

# ===== GAME =====
def draw_game(frame, game):
    cv2.putText(frame,f"Diem: {game.score}",(10,30),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

    if game.mode == "level":
        cv2.putText(frame,f"Man: {game.level}",(10,70),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.putText(frame,f"Time: {game.get_time_left()}",(10,110),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        cv2.putText(frame,f"Muc tieu: {game.target}",(10,150),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)
    else:
        cv2.putText(frame,"Mode: VO TAN",(10,70),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)

# ===== STORY (FIX BUG) =====
def draw_story(frame, speaker, text, index, total):
    buttons.clear()

    cv2.rectangle(frame, (40,300), (600,470), (0,0,0), -1)
    cv2.rectangle(frame, (40,300), (600,470), (255,255,255), 2)

    avatar = get_avatar(speaker)

    # 🔥 FIX LỖI Ở ĐÂY
    if avatar is not None:
        draw_png(frame, avatar, 50, 320)

    cv2.putText(frame, speaker.upper(), (200,330),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)

    cv2.putText(frame, text, (200,380),
                cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

    cv2.putText(frame, f"{index+1}/{total}", (520,440),
                cv2.FONT_HERSHEY_SIMPLEX,0.5,(200,200,200),1)

    draw_button(frame,"TIEP",460,410,120,40)

# ===== GAME OVER =====
def draw_gameover(frame,score,highscore):
    buttons.clear()

    cv2.putText(frame,"THUA ROI!",(200,180),
                cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3)

    cv2.putText(frame,f"Diem: {score}",(220,240),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

    cv2.putText(frame,f"Diem cao: {highscore}",(180,280),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

    draw_button(frame,"CHOI LAI",220,330,200,60)