#!/usr/bin/env python
from __future__ import division
from random import uniform

from pyglet import clock, font, image, window
from pyglet.gl import *

import sys
from textnozzle_chrom import TextNozzleChrom
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
        self.tn = TextNozzleChrom(input_file, line_width) 
        self.win = win
        self.chrom = "bh"
        self.helv = font.load('Monaco', win.width / 150.0)
        self.cb = cursebuf.cursebuf(90, self.get_text_object(self.pull_from_file()))
        self.chrom_object = self.get_text_object(self.chrom)

    def get_text_object(self, text):
        return Line(
            self.helv,
            text,
            self.win.width/2,
            -10,
            (1,1,1,1)
        ) 
        
    def get_chrom_text_object(self, text):
        return Line(
            self.helv,
            text,
            200,
            self.win.height - 20 ,
            (1,0,0,1)
        ) 

    def pull_from_file(self):
        (chrom, line) = self.tn.get_line()
        if chrom != self.chrom:
          self.chrom_object = self.get_chrom_text_object(chrom)
          self.chrom = chrom
        return line

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
            self.cb.add_line(self.get_text_object(self.pull_from_file()))
        map(lambda text: text.increment(), self.cb.get_buf())
        map(lambda text: text.draw(), self.cb.get_buf())
        self.increment()

    def draw_chrom(self):
        pyglet.gl.glColor4f(0.0, 0.0, 0.0, 1.0)
        y1 = self.win.height
        y2 = y1 - 50
        x1 = 0
        x2 = 600
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))
        self.chrom_object.draw()

    def draw(self):
        #print "{0} text objects".format(len(self.cb.get_buf()))
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.draw_texts()
        self.draw_chrom()

class App(object):

    def __init__(self, input_file):
        self.win = window.Window(fullscreen=True)
        self.win.set_mouse_visible(False)
        self.camera = Camera(self.win, zoom=100.0)
        self.hud = Hud(self.win, input_file, 189)

    def mainLoop(self):
        clock.set_fps_limit(25)
        while not self.win.has_exit:
            self.win.dispatch_events()
            self.camera.hudProjection()
            self.hud.draw()
            clock.tick()
            self.win.flip()

if __name__ == "__main__":
    app = App(sys.argv[1])
    app.mainLoop()

