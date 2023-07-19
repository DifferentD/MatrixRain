import pygame as pg
import random as rd

class App:
    def __init__(self):
        self.clock = pg.time.Clock()
        # Создаем массив слоев, который влияет на: цвет, скорость и размер символов
        # size: [x, speed]
        self.line_arr = dict()
        for sz in all_size:
            s1, s2 = speed_limit
            self.line_arr[sz] = [[i, rd.randint(s1, s2)/100] for i in range(sz//2, 740+1, sz) if rd.randint(0, 4)]

    def run(self):
        # size: x: [func()]
        sym_line = dict()
        for sz in all_size:
            sym_line[sz] = dict()
            for x, speed in self.line_arr[sz]:
                sym_line[sz][x] = [Symbol_line(sz, -height)]
                while True:
                    app_line = sym_line[sz][x]
                    app_line.append(Symbol_line(sz, -sz*2-height-sum([f.length*sz for f in app_line])))
                    if sum([f.length*sz for f in app_line])+len(app_line)*sz*2 > height:
                        break

        # Главный цикл
        while True:
            screen.fill('black')
            for sz in range(len(all_size) - 1, -1, -1):
                size = all_size[sz]
                for x, speed in self.line_arr[size]:
                    for f in sym_line[size][x]:
                        now_draw = f
                        [now_draw.replace_sym() for _ in ' ' if not rd.randint(0, change_intrv)]
                        now_draw.move(speed)
                        now_draw.draw_line(x)

            pg.display.flip()
            [exit() for e in pg.event.get() if e.type == pg.QUIT]
            self.clock.tick(60)

class Symbol_line():
    """Создаем эксемпляр строки, имеет размер length и состоит из списка символов katakana.
    Каждый символ выбирает цвет из сгенерированного списка colors.
    Первый цвет - белый. Остальные цвета - color_mtx, который становится темнее к концу.
    """
    def __init__(self, size, y):
        self.size = size
        self.y = y
        self.length = rd.randint(4, 9)
        # size: [(r, g, b) x(length)]
        dark = all_size.index(size) / len(all_size)
        self.colors = []
        for i in range(self.length):
            dark1 = (1/self.length)*(self.length-i)
            self.colors.append(tuple((j-(j*dark))*dark1 for j in color_mtx))
        self.colors.insert(0, tuple([255-(255-j)*0.2 for j in color_mtx]))

        # Список рандомных символов катаканы длиной (length)
        self.font = pg.font.Font('font/ms mincho.ttf', size)
        self.kana_arr = dict()
        self.kana_arr = [self.font.render(rd.choice(katakana), True, self.colors[k]) for k in range(self.length)]

    def move(self, move):
        # если строка вышла за границу, то строка возвращается обратно
        self.y += move - ((self.y+self.length*self.size)*(self.y > height))

    def replace_sym(self):
        # Заменяем рандомный символ из строки
        replace = rd.randint(0, self.length-1)
        self.kana_arr[replace] = self.font.render(rd.choice(katakana), True, self.colors[replace])

    def draw_line(self, x):
        # Рисуем все символы из symb_arr
        for i in range(self.length):
            screen.blit(self.kana_arr[self.length-1-i], (x-self.size//2, self.y+self.size*i))

pg.font.init()

# Начальные параметры. Количество слоев зависит от кол-во элементов all_size
res = width, height = 740, 380
color_mtx = (57, 255, 20) #85,85,255
speed_limit = (100, 300)
change_intrv = 20
all_size = [40, 30, 20, 10]

screen = pg.display.set_mode(res, pg.SCALED)
katakana = [chr(i) for i in range(0xFF66,0xFF9E)]

if __name__ == '__main__':
    app = App()
    app.run()
