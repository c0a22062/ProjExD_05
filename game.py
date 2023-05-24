import random
import sys
import pygame as pg
import time
WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ

delta = {
        pg.K_UP: (0, -5),  #方向キーを押したときの移動値の辞書
        pg.K_DOWN: (0, +5)
        }


def check_bound(scr_rct: pg.Rect, obj_rct: pg.Rect) -> tuple[bool,bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    引数１：画面がSurafaceのRect
    引数２：こうかとん、または、爆弾のSurafaseのRect
    戻り値：横方向、縦方向のはみ出し判定結果（画面内：True/画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02-20230425/fig/pg_bg.jpg")
    r_bg_img = pg.transform.flip(bg_img,True,False)
    kk_img = pg.image.load("ex02-20230425/fig/3.png")
    kk_img_re =pg.transform.flip(kk_img,True,False)
    kk_img_def = pg.transform.rotozoom(kk_img_re, 0,1.0)
    
    emys = pg.sprite.Group()  # 鉄器のグループ

    

    kk_rct = kk_img_def.get_rect()
    kk_rct.center = (100, 200)

    tmr = 0

    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0

        tmr += 1

        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(r_bg_img, [1600 -x, 0])
        screen.blit(bg_img, [3200 -x, 0])
        screen.blit(r_bg_img, [4800 -x, 0])
        if tmr%200 == 0:  # 200フレームに1回，敵機を出現させる
            emys.add(Enemy())
        key_lst = pg.key.get_pressed()
        for k,mv in delta.items():
            if key_lst[k]:
                kk_rct.move_ip(mv)

        if check_bound(screen.get_rect(), kk_rct) != (True, True):
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rct.move_ip(-mv[0], -mv[1])
        if tmr%200 == 0:  # 200フレームに1回，敵機を出現させる
            emys.add(Enemy())
            emys.add(Enemy())

        

        screen.blit(kk_img_def, kk_rct)  #練習 ３
        emys.update()
        emys.draw(screen)
        pg.display.update()
        clock.tick(100)


class Enemy(pg.sprite.Sprite):
    """
    敵機に関するクラス
    """
    imgs = [pg.image.load(f"ex04/fig/alien{i}.png") for i in range(1, 4)]
    
    def __init__(self):
        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH,random.randint(0, HEIGHT)
        self.vx = -6

        
    def update(self):
        """
        敵機を速度ベクトルself.vyに基づき移動（降下）させる
        ランダムに決めた停止位置_boundまで降下したら，_stateを停止状態に変更する
        引数 screen：画面Surface
        """
        self.rect.centerx += self.vx
        
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()