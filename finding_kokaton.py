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
    こうかとんに関するクラス
    """
    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像を初期化する
        引数1 num：画像番号(0-9)
        引数2 xy：配置座標
        """
        super().__init__()
        # figフォルダ内の0.png~9.pngを読み込む想定
        img = pg.image.load(f"fig/{num}.png")
        self.image = pg.transform.rotozoom(img, 0, 2.0)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.bird_id = num  # 正誤判定用のID

        # --- 基本機能：移動速度を設定 ---
        # 向きをランダムにするために -3 ~ 3 の乱数を設定
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])

    def update(self):
        """
        こうかとんを移動させ、画面端で跳ね返らせる
        """
        self.rect.move_ip(self.vx, self.vy)
        
        # 画面端判定（第2回資料のチェック機能と同じ考え方）
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vx *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vy *= -1

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
    # 基本機能：9種類の鳥を生成してグループに登録
    birds = pg.sprite.Group()
    img_nums = list(range(10)) 
    random.shuffle(img_nums) # 画像をランダムに
    # ★ スタート画面を表示 ★
    Start(screen)
    
    positions = []
    for _ in range(9):
    # 画面の端すぎない範囲(100〜WIDTH-100など)でランダムに決定
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        positions.append((x, y))

    for i in range(9):
        bird = Bird(img_nums[i], positions[i])
        birds.add(bird)
    for i in range(9):
        bird = Bird(img_nums[i], positions[i])
        birds.add(bird)
        
    # 基本機能：ターゲット（正解）を1つ決める
    target_bird = random.choice(birds.sprites())
    target_img = pg.transform.rotozoom(pg.image.load(f"fig/{target_bird.bird_id}.png"), 0, 1.0)

    clock = pg.time.Clock()
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            
            # 基本機能：クリック判定
            if event.type == pg.MOUSEBUTTONDOWN:
                for bird in birds:
                    if bird.rect.collidepoint(event.pos):
                        if bird.bird_id == target_bird.bird_id:
                            print("正解！")
                        else:
                            print("残念...")
                            Result(screen, clear_count)
                            return            

        birds.update()
        screen.blit(bg_img, [0, 0])
        
        # ターゲットの表示
        screen.blit(target_img, [10, 10])
        pg.draw.rect(screen, (255, 0, 0), [5, 5, 100, 100], 3) # 枠線
        
        birds.draw(screen)
        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()