import os
import sys
import random

import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 画面サイズ
WIDTH, HEIGHT = 800, 600


class Bird(pg.sprite.Sprite):
    """
    こうかとんクラス
    """

    def __init__(self, num: int, xy: tuple[int, int]):
        super().__init__()

        img = pg.image.load(f"fig/{num}.png")
        self.image = pg.transform.rotozoom(img, 0, 1.0)
        self.rect = self.image.get_rect()
        self.rect.center = xy

        self.bird_id = num

        # 移動速度
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])

    def update(self):

        self.rect.move_ip(self.vx, self.vy)

        # 横反射
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vx *= -1

        # 縦反射
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vy *= -1


def create_stage():
    """
    ステージ生成
    """

    birds = pg.sprite.Group()

    # 使用画像
    img_nums = random.sample(range(10), 9)

    positions = []

    for _ in range(9):

        while True:

            x = random.randint(100, WIDTH - 100)
            y = random.randint(100, HEIGHT - 100)

            new_rect = pg.Rect(x, y, 80, 80)

            overlap = False

            for pos in positions:

                old_rect = pg.Rect(pos[0], pos[1], 80, 80)

                if new_rect.colliderect(old_rect):
                    overlap = True
                    break

            if not overlap:
                positions.append((x, y))
                break

    # 鳥生成
    for i in range(9):

        bird = Bird(
            img_nums[i],
            positions[i]
        )

        birds.add(bird)

    # 正解鳥
    target_bird = random.choice(birds.sprites())

    target_img = pg.transform.rotozoom(
        pg.image.load(f"fig/{target_bird.bird_id}.png"),
        0,
        2.0
    )

    return birds, target_bird, target_img


def main():

    pg.display.set_caption("正しいこうかとんを探せ！！")

    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img = pg.image.load("fig/pg_bg.jpg")

    # フォント
    font = pg.font.Font(None, 50)
    big_font = pg.font.Font(None, 100)

    # ステージ番号
    stage = 1

    # 制限時間
    remaining_time = 30

    # 初期ステージ生成
    birds, target_bird, target_img = create_stage()

    start_time = pg.time.get_ticks()

    game_clear = False
    time_up = False

    clock = pg.time.Clock()

    while True:

        # イベント処理
        for event in pg.event.get():

            if event.type == pg.QUIT:
                return

            if event.type == pg.MOUSEBUTTONDOWN:

                if game_clear or time_up:
                    continue

                for bird in birds:

                    if bird.rect.collidepoint(event.pos):

                        # 正解
                        if bird.bird_id == target_bird.bird_id:
                            game_clear = True

        # 時間計算
        now = pg.time.get_ticks()

        elapsed = (now - start_time) / 1000

        remaining = max(0, int(remaining_time - elapsed))

        # タイムアップ
        if remaining <= 0 and not game_clear:
            time_up = True

        # 更新
        if not game_clear and not time_up:
            birds.update()

        # 背景
        screen.blit(bg_img, (0, 0))

        # 鳥描画
        birds.draw(screen)

        # ターゲット表示
        screen.blit(target_img, (10, 10))

        pg.draw.rect(screen, (255, 0, 0), (5, 5, 110, 110), 3)

        # タイマー表示
        timer_text = font.render(
            f"TIME : {remaining}",
            True,
            (255, 255, 255)
        )

        screen.blit(timer_text, (560, 20))

        # ステージ表示
        stage_text = font.render(
            f"STAGE : {stage}",
            True,
            (255, 255, 0)
        )

        screen.blit(stage_text, (300, 20))

        

        # CLEAR表示
        if game_clear:

            clear_text = big_font.render(
                "CLEAR!",
                True,
                (255, 0, 0)
            )

            screen.blit(clear_text, (220, 250))

        # TIME UP表示
        if time_up:

            time_text = big_font.render(
                "TIME UP!",
                True,
                (0, 0, 255)
            )

            screen.blit(time_text, (150, 250))

        pg.display.update()

        # ステージクリア処理
        if game_clear:

            pg.time.wait(1500)

            # ステージ加算
            stage += 1

            # クリアボーナス：残り時間に2秒追加
            remaining_time = remaining + 2

            # 次ステージ開始時刻
            start_time = pg.time.get_ticks()

            # 次ステージ生成
            birds, target_bird, target_img = create_stage()

            game_clear = False

        # ゲームオーバー
        if time_up:

            pg.time.wait(3000)

            return

        clock.tick(60)


if __name__ == "__main__":

    pg.init()

    main()

    pg.quit()

    sys.exit()