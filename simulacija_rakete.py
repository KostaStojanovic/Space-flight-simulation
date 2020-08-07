import pygame as pg
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
x = 100
y = 100
v_x = 0
v_y = 0
a_p = 0
a_px = 0
a_py = 0
a_g = 0
ugaona_brzina = 0
ugao = 0
n = 1000

def draw_vektor_g(x, y, a_gx, a_gy):
    pg.draw.line(prozor, pg.Color("green"), (int(x), int(y)), (int(x + a_gx * 600), int(y + a_gy * 600)), 2)

def draw_vektor_b(x, y, v_x, v_y):
    pg.draw.line(prozor, pg.Color("red"), (int(x), int(y)), (int(x + v_x * 20), int(y + v_y * 20)), 2)

def draw_putanja(x, y, v_x, v_y, n):
    x1 = x
    v_x1 = v_x
    y1 = y
    v_y1 = v_y
    for i in range(0, n, 1):
        a_gx = -g(x1, y1) * math.cos(ugao_o(x1, y1) / 180 * math.pi)
        a_gy = g(x1, y1) * math.sin(ugao_o(x1, y1) / 180 * math.pi)

        v_x1 += a_gx
        x1 += v_x1
        v_y1 += a_gy
        y1 += v_y1

        if(i % 10 == 0): pg.draw.circle(prozor, pg.Color("white"), (int(x1), int(y1)), 2)
        if (d(x1, y1) < 130):
            break
        if(math.fabs(x - x1) < 3 and math.fabs(y - y1) < 3 and i > 100):
            break

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

    v_x += a_px + a_gx
    x += v_x
    v_y += a_py + a_gy
    y += v_y

    if(d(x, y) < 130): pg.quit()
    prozor.fill(pg.Color("Black"))
    draw_putanja(x, y, v_x, v_y, n)
    draw_raketa(x, y, ugao)
    draw_planeta()
    draw_vektor_g(x, y, a_gx, a_gy)
    draw_vektor_b(x, y, v_x, v_y)
    pg.display.update()
    mainClock.tick(fps)
