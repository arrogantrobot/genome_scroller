#!/usr/bin/env python
from __future__ import division
from random import uniform

from pyglet import clock, font, image, window
from pyglet.gl import *

import random
import sys
from textnozzle import TextNozzle

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


class Hud(object):

    def __init__(self, win, input_file, line_width):
        self.tn = TextNozzle(input_file, line_width) 
        self.win = win
        self.helv = font.load('Helvetica', win.width / 150.0)
        self.text = self.get_text()

    def pull_from_file(self):
        return self.tn.get_line()


    def get_text(self):
        line = str(random.random())
        return font.Text(
            self.helv,
            self.pull_from_file(),
            x=self.win.width / 2,
            y=self.win.height / 2,
            halign=font.Text.CENTER,
            valign=font.Text.CENTER,
            color=(1, 1, 1, 0.5),
        )

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        self.get_text().draw()


class App(object):

    def __init__(self, input_file):
        self.win = window.Window(fullscreen=True)
        self.camera = Camera(self.win, zoom=100.0)
        self.hud = Hud(self.win, input_file, 100)

    def mainLoop(self):
        clock.set_fps_limit(6)
        while not self.win.has_exit:
            self.win.dispatch_events()
            self.camera.hudProjection()
            self.hud.draw()
            clock.tick()
            self.win.flip()

if __name__ == "__main__":
    app = App(sys.argv[1])
    app.mainLoop()

