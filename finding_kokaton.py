import os
import sys
import random
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 画面サイズ
WIDTH, HEIGHT = 800, 600

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
        self.image = pg.transform.rotozoom(img, 0, 1.0)
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
    def update(self, brds):
        """
        難易度の表示の変更、速度を上昇させる
        引数:それぞれの鳥画像をforで回すためのbirdグループ
        """
        self.value += 1
        self.image = self.font.render(f"difficulty: {self.value}", True, self.color)
        for b in brds:
            b.vx *= 1.2#速度を1.2倍する
            b.vy *= 1.2
    def draw(self, screen):
        """
        更新とは別にblitを行う
        引数:blitのためのscreen
        """
        screen.blit(self.image, self.rect)

def main():
    pg.display.set_caption("正しいこうかとんを探せ！！")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    # 基本機能：9種類の鳥を生成してグループに登録
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
                            lvup.update(birds) 
                        else:
                            print("残念...")

        birds.update()
        screen.blit(bg_img, [0, 0])
        
        # ターゲットの表示
        screen.blit(target_img, [10, 10])
        pg.draw.rect(screen, (255, 0, 0), [5, 5, 100, 100], 3) # 枠線
        
        birds.draw(screen)
        lvup.draw(screen) 
        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()