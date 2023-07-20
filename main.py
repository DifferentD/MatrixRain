import pygame as pg
import random as rd

pg.font.init()
pg.display.init()

class App:
    def __init__(self):
        self.clock = pg.time.Clock()
        # size: [x, speed]
        self.line_arr = dict()
        for sz in all_size:
            s1, s2 = speed_limit
            self.line_arr[sz] = [[i, rd.randint(s1, s2)/100] for i in range(sz//2, width+1, sz) if rd.randint(0, 3)]

    def run(self):
        # size: x: [func()]
        sym_line = dict()
        for sz in all_size:
            sym_line[sz] = dict()
            for x, speed in self.line_arr[sz]:
                sym_line[sz][x] = [Symbol_line(sz, -height)]
                for _ in range(height//sz//9):
                    app_line = sym_line[sz][x]
                    app_line.append(Symbol_line(sz, -sz*2-height-sum([f.length*sz for f in app_line])))

        # Главный цикл
        while True:
            screen.fill('black')
            for sz in range(len(all_size) - 1, -1, -1):
                size = all_size[sz]
                for x, speed in self.line_arr[size]:
                    for f in range(len(sym_line[size][x])):
                        now_draw = sym_line[size][x][f]
                        # Изменить символ в строке
                        if not rd.randint(0, change_intrv):
                            now_draw.replace_sym()
                        # Движение строки вниз или в начало экрана
                        restart = f+1 if f != len(sym_line[size][x])-1 else 0
                        now_draw.move(speed, sym_line[size][x][restart].y)
                        now_draw.draw_line(x)

            pg.display.flip()
            [exit() for e in pg.event.get() if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE]
            [exit() for e in pg.event.get() if e.type == pg.QUIT]
            self.clock.tick(60)
        pg.quit()

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
        self.kana_arr = [self.font.render(rd.choice(katakana), True, self.colors[k]) for k in range(self.length)]

    def move(self, move, last):
        # если строка вышла за границу, то строка возвращается обратно
        flaq = (self.y > height) and (last > self.size)
        self.y += move - ((self.y+self.length*self.size)*flaq)

    def replace_sym(self):
        # Заменяем рандомный символ из строки
        replace = rd.randint(0, self.length-1)
        self.kana_arr[replace] = self.font.render(rd.choice(katakana), True, self.colors[replace])

    def draw_line(self, x):
        # Рисуем все символы из symb_arr
        for i in range(self.length):
            screen.blit(self.kana_arr[self.length-1-i], (x-self.size//2, self.y+self.size*i))


# START VALUE
katakana = [chr(i) for i in range(0xFF66,0xFF9E)]  # '1234567890'.strip()
all_size = [60, 30, 20, 10]  # Размеры символов и кол-во слоев
color_mtx = (57, 255, 20)     # 57, 255, 20 | 85, 85, 255 | 254, 89, 194
speed_limit = (200, 400)     # Минимальная и максимальная скорость
change_intrv = 49            # Шанс изменения символа в строке

# SCALED SCREEN
# res = width, height = 740, 380
# screen = pg.display.set_mode(res, pg.SCALED)

# FULLSCREEN
display = pg.display.Info()
res = width, height = display.current_w, display.current_h
screen = pg.display.set_mode(res, pg.FULLSCREEN)

if __name__ == '__main__':
    app = App()
    app.run()
