#! /usr/bin/python3
import sys
import re

import pygame
import pygame.event
import pygame.locals

"""
time: 169000000000  pos 204014398881557  365041067030426
time: 267000000000  pos 216543756982911  342488222447989
time: 433000000000  pos 240098950213456  301391927875549
time: 574000000000  pos 259143574527513  270319119784192
time: 644000000000  pos 269668235332650  251775669794189
time: 757000000000  pos 283701116406167  227218127915536
time: 972000000000  pos 313270401525361  177100695510121
time: 1015000000000  pos 318783319089957  167077209029038


"""


class App:
    window_title = None

    xres = 640
    yres = 480
    framerate = 60

    def __init__(self):
        pygame.init()
        self.period = 1.0 / self.framerate
        self.surface = pygame.display.set_mode( (self.xres, self.yres) )
        self.rect = self.surface.get_bounding_rect()
        if self.window_title is not None:
            pygame.display.set_caption(self.window_title)
        self.__clock = pygame.time.Clock()
        self.__handlers = {
            pygame.locals.QUIT: self.handle_quit,
            pygame.locals.MOUSEBUTTONDOWN: self.handle_mousedown,
            pygame.locals.MOUSEBUTTONUP: self.handle_mouseup,
            pygame.locals.MOUSEMOTION: self.handle_mousemove,
            pygame.locals.KEYDOWN: self.handle_keydown,
            pygame.locals.KEYUP: self.handle_keyup,
        }
        self.mouse_pos = (0, 0)
        self.aspect_ratio = self.xres / self.yres

    def handle_quit(self, event):
        pygame.quit()
        sys.exit(0)

    def handle_mousemove(self, event):
        self.mouse_pos = event.pos

    def handle_mousedown(self, event):
        pass

    def handle_mouseup(self, event):
        pass

    def handle_keydown(self, event):
        pass

    def handle_keyup(self, event):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type in self.__handlers:
                self.__handlers[event.type](event)

    def run(self):
        try:
            while True:
                self.handle_events()
                self.do_work()
                pygame.display.update()
                self.__clock.tick(self.framerate)
        except KeyboardInterrupt:
            self.handle_quit(None)

    def do_work(self):
        raise NotImplementedError()


class StoneWatcher(App):
    window_title = 'Hailstone viewer'
    xres = 1920
    yres = 1080
    framerate = 30

    speed = 1000000000

    def __init__(self, stones):
        super().__init__()
        self.x0, self.y0, self.x1, self.y1 = self.setup_viewport(stones)
        self.xr = self.x1 - self.x0
        self.yr = self.y1 - self.y0
        self.stones = stones
        self.t = 0

    def setup_viewport(self, stones):
        x0 = min(s[0] for s in stones)
        x1 = max(s[0] for s in stones)
        y0 = min(s[1] for s in stones)
        y1 = max(s[1] for s in stones)
        xc = (x0 + x1) // 2
        yc = (y0 + y1) // 2
        xr = x1 - x0
        yr = y1 - y0
        if xr / yr > self.aspect_ratio:
            yr = xr / self.aspect_ratio
        else:
            xr = yr * self.aspect_ratio
        screen_x0 = xc - xr // 2
        screen_x1 = xc + xr // 2
        screen_y0 = yc - yr // 2
        screen_y1 = yc + yr // 2
        return screen_x0, screen_y0, screen_x1, screen_y1

    def coords_to_pos(self, x, y):
        sx = int((x - self.x0) * self.xres / self.xr)
        sy = int((y - self.y0) * self.yres / self.yr)
        return sx, sy

    def pos_to_coords(self, sx, sy):
        x = sx * self.xr / self.xres + self.x0
        y = sy * self.yr / self.yres + self.y0
        return x, y

    def handle_mousedown(self, event):
        sx, sy = event.pos
        x, y = self.pos_to_coords(sx, sy)
        print("time: %d  pos %d  %d" % (self.t, x, y))


    def draw_stones(self):
        self.surface.fill(pygame.Color("black"))
        for stone in self.stones:
            x, y, z, _, _, _ = stone
            sx, sy = self.coords_to_pos(x, y)
            self.surface.set_at((sx, sy), pygame.Color('white'))

    def move_stones(self):
        for stone in self.stones:
            stone[0] += stone[3] * self.speed
            stone[1] += stone[4] * self.speed
            stone[2] += stone[5] * self.speed
        self.t += self.speed

    def do_work(self):
        self.draw_stones()
        self.move_stones()


def main(input_file):
    stones = []
    for line in open(input_file).read().strip().split('\n'):
        stones.append([int(x) for x in re.findall(r'[0-9-]+', line)])

    app = StoneWatcher(stones)
    app.run()


if __name__ == '__main__':
    main(sys.argv[1])
