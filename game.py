import random
import time
from sound import play_catch, play_lose

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mode = "level"   # 🔥 thêm mode
        self.level = 1
        self.reset()

    def reset(self):
        self.basket_x = self.width // 2
        self.score = 0
        self.items = []
        self.start_time = time.time()
        self.target = 10 + self.level * 5

        # ⚡ speed boost
        self.speed_boost = False
        self.speed_time = 0

    def spawn(self):
        # 🔥 chế độ vô tận
        if self.mode == "endless":
            item_type = random.choice(["money","bomb","star","speed"])

        # 🔥 chế độ theo màn
        else:
            if self.level == 1:
                item_type = random.choice(["money","speed"])
            elif self.level == 2:
                item_type = random.choice(["money","bomb","speed"])
            elif self.level == 3:
                item_type = random.choice(["money","bomb","star","speed"])
            else:
                item_type = random.choice(["money","bomb","star","speed"])

        return {
            "x": random.randint(0, self.width - 40),
            "y": 0,
            "speed": random.randint(3,7) + self.level,
            "type": item_type
        }

    def update(self):
        if random.randint(1, 12) == 1:
            self.items.append(self.spawn())

        # ⚡ hết hiệu ứng speed
        if self.speed_boost and time.time() - self.speed_time > 3:
            self.speed_boost = False

        for item in self.items[:]:
            item["y"] += item["speed"]

            if self.height - 100 < item["y"] < self.height - 40 and abs(item["x"] - self.basket_x) < 70:

                if item["type"] == "money":
                    self.score += 1
                    play_catch()

                elif item["type"] == "star":
                    self.score += 2
                    play_catch()

                elif item["type"] == "bomb":
                    self.score = max(0, self.score - 5)
                    play_lose()

                elif item["type"] == "speed":
                    self.speed_boost = True
                    self.speed_time = time.time()

                self.items.remove(item)

            elif item["y"] > self.height:
                self.items.remove(item)

    def get_time_left(self):
        if self.mode == "endless":
            return 999  # vô tận
        return int(30 - (time.time() - self.start_time))

    def is_win(self):
        if self.mode == "endless":
            return False
        return self.score >= self.target