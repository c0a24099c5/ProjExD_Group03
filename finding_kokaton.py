import os
import sys
import random
import pygame as pg
import time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 画面サイズ
WIDTH, HEIGHT = 800, 600
clear_count = 0             #クリアしたステージ数


class Bird(pg.sprite.Sprite):
    """
    こうかとんクラス
    """

    def __init__(self, num: int, xy: tuple[int, int], speed):
        super().__init__()
        # figフォルダ内の0.png~9.pngを読み込む
        img = pg.image.load(f"fig/{num}.png")
        self.image = pg.transform.rotozoom(img, 0, 1.0)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.bird_id = num  # 正誤判定用の画像番号

        # 移動速度
        self.vx = random.choice([-3, -2, 2, 3]) * speed
        self.vy = random.choice([-3, -2, 2, 3]) * speed

    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        
        # 画面端判定
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vx *= -1  # 画面の左右の端に触れたら速度を反転
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vy *= -1  # 画面の上下の端に触れたら速度を反転
            
class level_up(pg.sprite.Sprite):
    """
    難易度の上昇に関するクラス
    """
    def __init__(self):
        super().__init__()
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)#青色のフォント
        self.value = 1
        self.image = self.font.render(f"difficulty: {self.value}", True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - 50)
   
    def draw(self, screen):
        """
        更新とは別にblitを行う
        引数:blitのためのscreen
        """
        screen.blit(self.image, self.rect)


class BGM():
    """
    BGMを流す関数。
    """
    def __init__(self):
        pg.mixer.init()
        pg.mixer.music.load("sound/house_lo.wav")
        pg.mixer.music.play(-1)
            

def reset_stage(birds: pg.sprite.Group, difficulty):
    """
    担当機能：既存のこうかとんたちを消して、新しい配置とターゲットを生成する
    """
    birds.empty()  # 今いるこうかとんを全消去

    img_nums = random.sample(range(10), 9)  # 新しいステージ用の画像番号のリストを作る

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

    for i in range(9):
        birds.add(Bird(img_nums[i], positions[i], difficulty))

    target_bird = random.choice(birds.sprites())

    target_img = pg.transform.rotozoom(
        pg.image.load(f"fig/{target_bird.bird_id}.png"),
        0,
        1.5  # こうかとんをランダムな位置に再配置
    )
    
    return target_bird, target_img  # 新しいターゲットを決めて返す

def Start(screen):

    """
    スタート画面を表示する
    """ 
    font_nihongo = "C:/Windows/Fonts/msgothic.ttc"
    font_title = pg.font.Font(font_nihongo, 60)
    font_msg = pg.font.Font(font_nihongo, 40)

    while True:
        screen.fill((0, 0, 0))

        title = font_title.render("正しいこうかとんを探せ！！", True, (255, 255, 0))
        msg = font_msg.render("Enterキーでスタート", True, (200, 200, 200))

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 400))

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                return

def Result(screen, count):
    """
    ゲームオーバー時のリザルト画面を表示する
    """
    font_nihongo = "C:/Windows/Fonts/msgothic.ttc"
    font_big = pg.font.Font(font_nihongo, 80)
    font_small = pg.font.Font(font_nihongo, 30)

    screen.fill((0, 0, 0))

    result_text = font_big.render("GAME OVER", True, (255, 0, 0))
    screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 150))

    count_text = font_small.render(f"クリアしたステージ数：{count}", True, (255, 255, 255))
    screen.blit(count_text, (WIDTH//2 - count_text.get_width()//2, 300))

    msg_text = font_small.render("Enterキーで終了", True, (200, 200, 200))
    screen.blit(msg_text, (WIDTH//2 - msg_text.get_width()//2, 450))

    pg.display.update()

    # Enterキーが押されるまで待機
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                waiting = False

def main():

    pg.display.set_caption("正しいこうかとんを探せ！！")

    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img = pg.image.load("fig/pg_bg.jpg")

    Start(screen)  #スタート画面を表示
    

    BGM()
    # 基本機能：9種類の鳥を生成してグループに登録
    # フォント
    font = pg.font.Font(None, 50)
    big_font = pg.font.Font(None, 100)

    # 鳥グループ
    birds = pg.sprite.Group()
    birds = pg.sprite.Group()
    img_nums = list(range(10)) 
    random.shuffle(img_nums) # 画像をランダムに
    lvup = level_up()

    positions = []
    for _ in range(9):
    # 画面の端すぎない範囲(100〜WIDTH-100など)でランダムに決定
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        positions.append((x, y))



    target_bird, target_img = reset_stage(birds, 1)  # 初回ステージ生成

    mode = "PLAYING"  # 最初はプレイ中モード
    stage_count = 1   # 何問目かのカウント

    clock = pg.time.Clock()

    # 制限時間
    remaining_time = 30

    start_time = pg.time.get_ticks()

    game_clear = False
    time_up = False

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

        if mode == "PLAYING":  # プレイ中の更新処理
            birds.draw(screen)  # すべてのこうかとんを描画
            target_img = pg.transform.rotozoom(pg.image.load(f"fig/{target_bird.bird_id}.png"), 10, 1.5)  # ターゲットの見本を左上に表示
            screen.blit(target_img, [10, 10])
            pg.draw.rect(screen, (255, 0, 0), [5, 5, 120, 120], 3)  # 正解のこうかとんを囲む赤い枠線

        # タイマー表示
        timer_text = font.render(
            f"TIME : {remaining}",
            True,
            (255, 255, 255)
        )

        screen.blit(timer_text, (560, 20))

        # ステージ表示
        stage_text = font.render(
            f"STAGE : {stage_count}",
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

        # ステージクリア処理
        if game_clear:

            pg.time.wait(1500)

            # ステージ加算
            stage_count += 1

            # クリアボーナス：残り時間に2秒追加
            remaining_time = remaining + 2

            # 次ステージ開始時刻
            start_time = pg.time.get_ticks()

            lvup.value += 1
            lvup.image = lvup.font.render(f"difficulty: {lvup.value}", True, lvup.color)

            target_bird, target_img = reset_stage(birds, lvup.value)

            game_clear = False

        # ゲームオーバー
        if time_up:

            pg.time.wait(3000)
            Result(screen, clear_count)

            return
        
        birds.draw(screen)
        lvup.draw(screen) 
        pg.display.update()
        clock.tick(60)


if __name__ == "__main__":

    pg.init()

    main()

    pg.quit()

    sys.exit()