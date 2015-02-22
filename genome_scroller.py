#!/usr/bin/env python
from __future__ import division
from random import uniform

from pyglet import clock, font, image, window
from pyglet.gl import *

import sys
from textnozzle import TextNozzle
import cursebuf

class Camera(object):

    def __init__(self, win, x=0.0, y=0.0, rot=0.0, zoom=1.0):
        self.win = win
        self.x = x
        self.y = y
        self.rot = rot
        self.zoom = zoom

    def worldProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        widthRatio = self.win.width / self.win.height
        gluOrtho2D(
            -self.zoom * widthRatio,
            self.zoom * widthRatio,
            -self.zoom,
            self.zoom)

    def hudProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.win.width, 0, self.win.height)

class Line(object):
    def __init__(self, fnt, text, x, y, color):
        self.text_object = font.Text(
            fnt,
            text,
            x=x,
            y=y,
            halign=font.Text.CENTER,
            valign=font.Text.CENTER,
            color=color,
        )
    def draw(self):
        self.text_object.draw()

    def increment(self):
        self.text_object.y += 1



class Hud(object):

    def __init__(self, win, input_file, line_width):
        self.counter = 0
        self.tn = TextNozzle(input_file, line_width) 
        self.win = win
        self.helv = font.load('Helvetica', win.width / 150.0)
        self.cb = cursebuf.cursebuf(100, self.get_text_object())

    def get_text_object(self):
        return Line(
            self.helv,
            self.pull_from_file(),
            self.win.width/2,
            -10,
            (1,1,1,1)
        ) 

    def pull_from_file(self):
        return self.tn.get_line()

    def get_text(self):
        return font.Text(
            self.helv,
            self.pull_from_file(),
            x=self.win.width / 2,
            y=-10,
            halign=font.Text.CENTER,
            valign=font.Text.CENTER,
            color=(1, 1, 1, 0.5),
        )
    def increment(self):
        self.counter += 1

    def draw_texts(self):
        if self.counter > 15:
            self.counter = 0
            self.cb.add_line(self.get_text_object())
        map(lambda text: text.increment(), self.cb.get_buf())
        map(lambda text: text.draw(), self.cb.get_buf())
        self.increment()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        self.draw_texts()

class App(object):

    def __init__(self, input_file):
        self.win = window.Window(fullscreen=True)
        self.camera = Camera(self.win, zoom=100.0)
        self.hud = Hud(self.win, input_file, 200)

    def mainLoop(self):
        clock.set_fps_limit(60)
        while not self.win.has_exit:
            self.win.dispatch_events()
            self.camera.hudProjection()
            self.hud.draw()
            clock.tick()
            self.win.flip()

if __name__ == "__main__":
    app = App(sys.argv[1])
    app.mainLoop()

