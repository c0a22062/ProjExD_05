import random
import sys
import time

import pygame as pg


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ


def check_bound(area: pg.Rect, obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数1 area：画面SurfaceのRect
    引数2 obj：オブジェクト（敵機,こうかとん）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < area.left or area.right < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < area.top or area.bottom < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    _delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1)
    }

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        img0 = pg.transform.rotozoom(pg.image.load(f"ex03-20230509/fig/{num}.png"), 0, 1.0)  # 左向き，1倍
        img1 = pg.transform.flip(img0, True, False)  # 右向き，1倍
        
        self.image = img1  # デフォルトで右      
        self.rect = self.image.get_rect()
        self.rect.center = xy



    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__._delta.items():
            if key_lst[k]:
                self.rect.move_ip(mv)
                sum_mv[0] += mv[0]  # 横方向合計
                sum_mv[1] += mv[1]  # 縦方向合計
        if check_bound(screen.get_rect(), self.rect) != (True, True):
            for k, mv in __class__._delta.items():
                if key_lst[k]:
                    self.rect.move_ip(-mv[0], -mv[1])
        
        screen.blit(self.image, self.rect)
    
class Enemy1(pg.sprite.Sprite):
    """
    敵機に関するクラス
    """
    imgs = [pg.image.load(f"ex05/fig/alien{i}.png") for i in range(1, 4)]
    
    def __init__(self):
        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH-50,random.randint(0, HEIGHT)
        self.vx = random.randint(-5,-1)

        
    def update(self):

        self.rect.centerx += self.vx


class Enemy2(pg.sprite.Sprite):
    """
    変則型敵機に関するクラス
    """
    imgs = [pg.image.load(f"ex04/fig/alien{i}.png") for i in range(1, 4)]
    
    def __init__(self):
        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.image = pg.transform.rotozoom(self.image,0,2.0)  #敵機のサイズ二倍

        self.rect = self.image.get_rect()
        self.rect.center = random.randint(1200, WIDTH), 100
        self.vy = +6
        self.vx = random.randint(-5,-2)
        self.bound = random.randint(50, HEIGHT)  # 停止位置

    def update(self):
        """
        敵機を速度ベクトルself.vyに基づき移動（降下）させる
        ランダムに決めた停止位置_boundまで降下
        """
        tmr = 0
        

        self.rect.centery += self.vy
        if self.rect.centery > self.bound:
            self.vy = 0
            while True:
                tmr += 1
                if tmr % 10000 == 0:
                    self.rect.centerx += self.vx
                    tmr = 0
                    break



        

class Coin(pg.sprite.Sprite):
    """
    コインに関するクラス
    """
    img = pg.image.load("ex05/fig/coin.png")
    
    def __init__(self):
        super().__init__()
        self.image = Coin.img
        self.image.set_colorkey((255, 255, 255))  # 白の背景を透過
        self.image = pg.transform.rotozoom(self.image,0,0.5)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH-100,random.randint(0, HEIGHT)
        self.vx = -2

        
    def update(self):
        """
        敵機を速度ベクトルself.vyに基づき移動（降下）させる
        ランダムに決めた停止位置_boundまで降下
        引数 screen：画面Surface
        """
        self.rect.centerx += self.vx


def main():
    pg.display.set_caption("たたかえ！こうかとん")

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    r_bg_img = pg.transform.flip(bg_img,True,False)

    emys1 = pg.sprite.Group()  # 敵機のグループ
    emys2 = pg.sprite.Group()  # 変則型敵機
    coins = pg.sprite.Group() # コインのグループ
    
    bird = Bird(3, (200, 100))
    

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
        tmr += 1
        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(r_bg_img, [1600 -x, 0])
        screen.blit(bg_img, [3200 -x, 0])
        screen.blit(r_bg_img, [4800 -x, 0])
        if tmr%400 == 0:  # 200フレームに1回，敵機を出現させる
            emys1.add(Enemy1())
            emys1.add(Enemy1())
            emys1.add(Enemy1())
            coins.add(Coin())
            coins.add(Coin())
            coins.add(Coin())
        elif tmr%700 == 0:
            emys2.add(Enemy2())
            emys2.add(Enemy2())


        
        if len(pg.sprite.spritecollide(bird, emys1, True)) != 0:
                pg.display.update()
                time.sleep(2)
                return
        if len(pg.sprite.spritecollide(bird, emys2, True)) != 0:
                pg.display.update()
                time.sleep(2)
                return
        if len(pg.sprite.spritecollide(bird, coins, True)) != 0:
                pg.display.update() 
            
        for emy in emys1:
            if False in check_bound(screen.get_rect(),emy.rect):
                emy.kill()
        for emy in emys2:
            if False in check_bound(screen.get_rect(),emy.rect):
                emy.kill()
        for coin in coins:
            if False in check_bound(screen.get_rect(),coin.rect):
                coin.kill()
        

        key_lst = pg.key.get_pressed()
        bird.update(key_lst, screen)

        
        emys1.update()
        emys1.draw(screen)
        emys2.update()
        emys2.draw(screen)
        coins.update()
        coins.draw(screen)
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()