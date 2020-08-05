import pygame as pg
import time
import math

pg.init()

prozor = pg.display.set_mode((1500, 1000))
raketa1 = pg.image.load("pictures/raketa1.png")
raketa2 = pg.image.load("pictures/raketa2.png")
planeta = pg.image.load("pictures/world.png")
pg.display.set_icon(raketa1)
pg.display.set_caption("Simulacija rakete")
mainClock = pg.time.Clock()

fps = 60
x = 750
y = 100
v_x = 2.23
v_y = 0
a_p = 0
a_px = 0
a_py = 0
a_g = 0
tranparent = (0, 0, 0, 0)
ugaona_brzina = 0
ugao = 0

def ugao_o(x, y):
    o = math.atan2(y - int(prozor.get_height() / 2), x - int(prozor.get_width() / 2)) / math.pi * 180
    if(o > 0): return 360 - o
    else: return -o

def d(x, y):
    return math.sqrt(((x - int(prozor.get_width() / 2)) ** 2) + ((math.fabs(y - int(prozor.get_height() / 2)) ** 2)))

def g(x, y):
    return 2000 / d(x, y) ** 2

def draw_planeta():
    prozor.blit(planeta, (int(prozor.get_width() / 2 - 128), int(prozor.get_height() / 2 - 128)))

def draw_raketa(x, y, ugao):
    if(a_p != 0):
        img = pg.transform.rotate(raketa1, ugao - 45)
    else:
        img = pg.transform.rotate(raketa2, ugao - 45)
    prozor.blit(img, (int(x) - int(img.get_width() / 2), int(y) - int(img.get_height() / 2)))



P = True
while P:  #main loop

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                ugaona_brzina = - 3
            if event.key == pg.K_LEFT:
                ugaona_brzina = 3
            if event.key == pg.K_UP:
                a_p = 0.05
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                ugaona_brzina = 0
            if event.key == pg.K_UP:
                a_p = 0
        if event.type == pg.QUIT:
            P = False


    a_px = math.cos(ugao/180 * math.pi) * a_p
    a_py = -math.sin(ugao/180 * math.pi) * a_p

    ugao += ugaona_brzina
    if(ugao >= 360): ugao -= 360
    if (ugao < 0): ugao += 360

    a_gx = -g(x, y) * math.cos(ugao_o(x, y)/180 * math.pi)
    a_gy = g(x, y) * math.sin(ugao_o(x, y)/180 * math.pi)

    x += v_x
    v_x += a_px + a_gx
    y += v_y
    v_y += a_py + a_gy

    if(d(x, y) < 130): pg.quit()
    prozor.fill(pg.Color("Black"))
    draw_planeta()
    draw_raketa(x, y, ugao)
    draw_planeta()
    pg.display.update()
    mainClock.tick(fps)
    print(str(v_x) + "..." + str(v_y))
