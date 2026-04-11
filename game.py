import random
import time
from sound import play_catch, play_lose

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mode = "level"
        self.level = 1
        self.reset()

    def reset(self):
        self.basket_x = self.width // 2
        self.score = 0
        self.items = []
        self.start_time = time.time()
        self.target = 10 + self.level * 5

        # ❤️ PLAYER HP
        self.hp = 4

        # ⚡ speed boost
        self.speed_boost = False
        self.speed_time = 0

        # ❄️ freeze (làm chậm)
        self.freeze = False
        self.freeze_time = 0

        # ⚔️ đạn player
        self.projectiles = []

        # 👾 boss
        self.boss_mode = (self.level == 4)
        self.boss_hp = 20

        self.boss_x = self.width // 2
        self.boss_dir = 1
        self.boss_speed = 6

        # 💣 đạn boss
        self.enemy_bullets = []
        self.last_shot = time.time()

    # ===== SPAWN =====
    def spawn(self):
        if self.mode == "endless":
            item_type = random.choice(["money","bomb","star","speed","freeze","attack"])
        else:
            if self.level == 1:
                item_type = random.choice(["money","speed"])
            elif self.level == 2:
                item_type = random.choice(["money","bomb","speed","freeze"])
            elif self.level == 3:
                item_type = random.choice(["money","bomb","star","speed","freeze"])
            else:
                item_type = random.choice(["attack","freeze","bomb"])

        return {
            "x": random.randint(0, self.width - 40),
            "y": 0,
            "speed": random.randint(3,7) + self.level,
            "type": item_type
        }

    # ===== UPDATE =====
    def update(self):

        # ❄️ freeze = làm chậm 5s
        freeze_factor = 1
        if self.freeze:
            if time.time() - self.freeze_time > 5:
                self.freeze = False
            else:
                freeze_factor = 0.3

        # spawn item
        if random.randint(1, 12) == 1:
            self.items.append(self.spawn())

        # ⚡ hết speed boost
        if self.speed_boost and time.time() - self.speed_time > 3:
            self.speed_boost = False

        # ===== ITEM =====
        for item in self.items[:]:
            item["y"] += item["speed"] * freeze_factor

            if self.height - 100 < item["y"] < self.height - 40 and abs(item["x"] - self.basket_x) < 70:

                if item["type"] == "money":
                    self.score += 1
                    play_catch()

                elif item["type"] == "star":
                    self.score += 2
                    play_catch()

                elif item["type"] == "bomb":
                    self.hp -= 1
                    play_lose()

                elif item["type"] == "speed":
                    self.speed_boost = True
                    self.speed_time = time.time()

                elif item["type"] == "freeze":
                    self.freeze = True
                    self.freeze_time = time.time()

                elif item["type"] == "attack":
                    self.projectiles.append({
                        "x": self.basket_x,
                        "y": self.height - 120
                    })

                self.items.remove(item)

            elif item["y"] > self.height:
                self.items.remove(item)

        # ===== ĐẠN PLAYER =====
        for p in self.projectiles[:]:
            p["y"] -= 12 * freeze_factor

            if self.boss_mode:
                if abs(p["x"] - self.boss_x) < 100 and p["y"] < 150:
                    self.boss_hp -= 1
                    self.projectiles.remove(p)

            elif p["y"] < 0:
                self.projectiles.remove(p)

        # ===== BOSS =====
        if self.boss_mode:
            self.boss_x += self.boss_dir * self.boss_speed * freeze_factor

            if self.boss_x < 100 or self.boss_x > self.width - 100:
                self.boss_dir *= -1

            if time.time() - self.last_shot > 1.2:
                self.enemy_bullets.append({
                    "x": self.boss_x,
                    "y": 120
                })
                self.last_shot = time.time()

        # ===== ĐẠN BOSS =====
        for b in self.enemy_bullets[:]:
            b["y"] += 10 * freeze_factor

            if abs(b["x"] - self.basket_x) < 60 and b["y"] > self.height - 120:
                self.hp -= 1
                self.enemy_bullets.remove(b)

            elif b["y"] > self.height:
                self.enemy_bullets.remove(b)

    # ===== TIME =====
    def get_time_left(self):
        if self.mode == "endless":
            return 999

        if self.boss_mode:
            return 999

        # ✅ FIX: không cho âm
        time_left = 30 - (time.time() - self.start_time)
        return max(0, int(time_left))

    # ===== WIN =====
    def is_win(self):
        if self.mode == "endless":
            return False

        if self.boss_mode:
            return self.boss_hp <= 0

        return self.score >= self.target

    # ===== THUA =====
    def is_dead(self):
        return self.hp <= 0

    # ✅ NEW: thua vì hết thời gian
    def is_time_up(self):
        if self.mode == "endless" or self.boss_mode:
            return False
        return self.get_time_left() <= 0