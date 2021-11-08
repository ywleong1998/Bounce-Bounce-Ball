import pygame
import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import sqrt

pygame.mixer.init()

power1 = 'img/power1.png'
power2 = 'img/power2.png'
power3 = 'img/power3.png'

rope_snd = pygame.mixer.Sound('snd/rope.wav')
gun_snd = pygame.mixer.Sound('snd/gun.wav')
hitball_snd = pygame.mixer.Sound('snd/hitball.wav')
bullethit_snd = pygame.mixer.Sound('snd/bullethit.wav')
hitplayer_snd = pygame.mixer.Sound('snd/hitplayer.wav')
hitplayer1_snd = pygame.mixer.Sound('snd/hitplayer1.wav')
hitash_snd = pygame.mixer.Sound('snd/hitash.wav')
hitash_snd1 = pygame.mixer.Sound('snd/hitash1.wav')
roundclear_snd = pygame.mixer.Sound('snd/roundclear.wav')
roundclear1_snd = pygame.mixer.Sound('snd/roundclear1.wav')
roundclear2_snd = pygame.mixer.Sound('snd/roundclear2.wav')
roundclear3_snd = pygame.mixer.Sound('snd/roundclear3.wav')
roundclear4_snd = pygame.mixer.Sound('snd/roundclear4.wav')
roundclear5_snd = pygame.mixer.Sound('snd/roundclear5.wav')
powerup_snd = pygame.mixer.Sound('snd/powerup.wav')

pygame.mixer.Sound.set_volume(rope_snd, 0.1)
pygame.mixer.Sound.set_volume(gun_snd, 0.5)
pygame.mixer.Sound.set_volume(hitplayer_snd, 0.85)
pygame.mixer.Sound.set_volume(bullethit_snd, 0.4)
pygame.mixer.Sound.set_volume(roundclear_snd, 0.4)
pygame.mixer.Sound.set_volume(roundclear1_snd, 0.4)
pygame.mixer.Sound.set_volume(roundclear2_snd, 0.4)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
boundary_top = 245
boundary_bottom = -160
boundary_leftright = 330

class Bg:
    def __init__(self):
        self.cloudy = []
        self.cloud_speed = []
        self.cloud_list = []
        for i in range(9):
            self.cloudy.append(random.randrange(0, boundary_top -25))
            self.cloud_speed.append(random.randrange(1,3))
        self.clouds = []
        for i in range(9):
            self.clouds.append(random.randrange(9, 14))
        self.Cloud_Lists()
        self.car_list = []
        self.Car_Lists()
        self.rainbowmode = False

    def sky(self):
        glBegin(GL_QUADS)
        glColor3f(0.7, 0.94, 0.96)
        glVertex2f(-326, -157)
        glVertex2f(326, -157)
        glColor3f(0.3, 0.91, 1)
        glVertex2f(326, 42)
        glVertex2f(-326, 42)
        glVertex2f(-326, 42)
        glVertex2f(326, 42)
        glColor3f(0.85, 0.67, 0.57)
        glVertex2f(326, 241)
        glColor3f(0.23, 0.4, 0.9)
        glVertex2f(-326, 241)
        glEnd()

    def mountain(self):
        glBegin(GL_TRIANGLES)
        glColor3f(0.56, 0.89, 0.35)
        glVertex2f(200, -70)
        glVertex2f(0, -70)
        glVertex2f(200, 135)
        glColor3f(0.33, 0.79, 0.22)
        glVertex2f(200, -70)
        glVertex2f(400, -70)
        glVertex2f(200, 135)
        glEnd()
        glBegin(GL_POLYGON)
        glColor3f(0.98, 0.98, 0.98)
        glVertex2f(200, 135)
        glVertex2f(200, 60)
        glVertex2f(180, 70)
        glVertex2f(125, 60)
        glColor3f(0.5, 1, 0.3)
        glVertex2f(200, 135)
        glVertex2f(200, 60)
        glVertex2f(220, 50)
        glVertex2f(240, 75)
        glVertex2f(280, 55)
        glEnd()

    def mountains(self):
        glPushMatrix()
        glScale(4 / 5, 1.3, 0)
        glTranslate(-190, 0, 0)
        self.mountain()
        glPopMatrix()
        self.mountain()
        glPushMatrix()
        glScale(0.9, 0.9, 1)
        glTranslate(-385, -15, 0)
        self.mountain()
        glPopMatrix()

    def Background(self):
        self.sky()
        self.mountains()
        self.grass()

    def grass(self):
        glBegin(GL_QUADS)
        glColor3f(0.47, 0.77, 0.31)
        glVertex2f(-326, -157)
        glVertex2f(326, -157)
        glVertex2f(326, -103.5)
        glVertex2f(-326, -103.5)
        glVertex2f(-326, -103.5)
        glVertex2f(326, -103.5)
        glColor3f(0.63, 0.97, 0.47)
        glVertex2f(326, -50)
        glVertex2f(-326, -50)
        glEnd()

    def road(self):
        x, y = -316, -128.5
        glBegin(GL_QUADS)
        glColor(0.47, 0.53, 0.68)
        glVertex2f(-326, -157)
        glVertex2f(326, -157)
        glVertex2f(326, -70)
        glVertex2f(-326, -70)
        glColor(0.41, 0.41, 0.41)
        glVertex2f(-326, -100)
        glVertex2f(326, -100)
        glVertex2f(326, -95)
        glVertex2f(-326, -95)
        glEnd()
        glLineWidth(12)
        glBegin(GL_LINES)
        glColor(1, 1, 1)
        for h in range(8):
            y1 = y
            for i in range(16):
                x1 = x + i * 55
                glVertex2f(x1, y1)
        glEnd()
        glLineWidth(3)
        glBegin(GL_LINES)
        glColor3f(1, 1, 1)
        glVertex3f(-320, -100, 0)
        glVertex3f(-320, -105, 0)
        glVertex3f(-320, -110, 0)
        glVertex3f(-320, -115, 0)
        glVertex3f(300, -100, 0)
        glVertex3f(300, -105, 0)
        glVertex3f(300, -110, 0)
        glVertex3f(300, -115, 0)
        glColor3f(0, 0, 0)
        glVertex3f(-320, -95, 0)
        glVertex3f(-320, -100, 0)
        glVertex3f(-320, -105, 0)
        glVertex3f(-320, -110, 0)
        glVertex3f(300, -95, 0)
        glVertex3f(300, -100, 0)
        glVertex3f(300, -105, 0)
        glVertex3f(300, -110, 0)
        glVertex3f(-163, -95, 0)
        glVertex3f(-163, -80, 0)
        glVertex3f(163, -95, 0)
        glVertex3f(163, -80, 0)
        glVertex3f(0, -95, 0)
        glVertex3f(0, -80, 0)
        glEnd()

        glPointSize(11)
        glBegin(GL_POINTS)
        glColor(0, 1, 0)
        glVertex3f(-320, -90, 0)
        glVertex3f(300, -90, 0)
        glColor(1, 1, 0)
        glVertex3f(-320, -83, 0)
        glVertex3f(300, -83, 0)
        glColor(1, 0, 0)
        glVertex3f(-320, -76, 0)
        glVertex3f(300, -76, 0)
        glEnd()

        glPointSize(5)
        glBegin(GL_POINTS)
        glColor(1, 0.5, 0)
        glVertex3f(-163, -82, 0)
        glVertex3f(163, -82, 0)
        glVertex3f(0, -82, 0)
        glEnd()

    def windows(self, x, y, w, h):
        glBegin(GL_QUADS)
        glColor3f(0.51, 0.73, 0.92)
        glVertex2f(x - w, y - h)
        glColor3f(0, 0.8, 1)
        glVertex2f(x + w, y - h)
        glColor3f(0.75, 0.94, 0.99)
        glVertex2f(x + w, y + h)
        glColor3f(0.62, 0.91, 0.99)
        glVertex2f(x - w, y + h)
        glEnd()

    def h1(self):
        x4, y4 = -285, 105
        glBegin(GL_QUADS)
        glColor3f(0.60, 0.73, 0.77)
        glVertex2f(-300, -70)
        glColor3f(0.60, 0.65, 0.7)
        glVertex2f(-180, -70)
        glColor3f(0.67, 0.77, 0.8)
        glVertex2f(-180, 20)
        glVertex2f(-300, 20)
        glVertex2f(-300, 20)
        glVertex2f(-180, 20)
        glColor3f(0.67, 0.66, 0.63)
        glVertex2f(-180, 130)
        glColor3f(0.63, 0.7, 0.72)
        glVertex2f(-300, 130)
        glColor3f(0.66, 0.71, 0.73)
        glVertex2f(-280, 130)
        glVertex2f(-200, 130)
        glVertex2f(-200, 170)
        glVertex2f(-280, 170)
        glVertex2f(-235, 170)
        glVertex2f(-245, 170)
        glVertex2f(-245, 200)
        glVertex2f(-235, 200)
        glEnd()
        for h in range(6):
            y5 = y4 - h * 30
            for i in range(7):
                x5 = x4 + i * 15
                self.windows(x5, y5, 5, 10)

    def h2(self):
        x1, y1 = -172, 20
        glBegin(GL_QUADS)
        glColor3f(0.76, 0.71, 0.57)
        glVertex2f(-180, -70)
        glColor3f(0.69, 0.63, 0.47)
        glVertex2f(-95, -70)
        glColor3f(0.95, 0.89, 0.53)
        glVertex2f(-95, 30)
        glColor3f(0.93, 0.85, 0.65)
        glVertex2f(-180, 30)
        glColor3f(0.1, 0.15, 0.2)
        glVertex2f(-180, 30)
        glColor3f(0.2, 0.25, 0.3)
        glVertex2f(-95, 30)
        glColor3f(0.3, 0.33, 0.42)
        glVertex2f(-95, 35)
        glColor3f(0.35, 0.4, 0.48)
        glVertex2f(-180, 35)
        glEnd()
        for h in range(6):
            y2 = y1 - h * 16
            for i in range(8):
                x2 = x1 + i * 10
                self.windows(x2, y2, 3, 4)

    def h3(self):
        x1, y1 = -83, 130
        glBegin(GL_QUADS)
        glColor3f(0.81, 0.81, 0.81)
        glVertex2f(-95, -70)
        glColor3f(0.84, 0.84, 0.84)
        glVertex2f(-10, -70)
        glColor3f(0.88, 0.88, 0.88)
        glVertex2f(-10, 35)
        glColor3f(0.73, 0.71, 0.68)
        glVertex2f(-95, 35)
        glVertex2f(-95, 35)
        glColor3f(0.88, 0.88, 0.88)
        glVertex2f(-10, 35)
        glColor3f(0.95, 0.95, 0.95)
        glVertex2f(-10, 140)
        glColor3f(0.71, 0.71, 0.71)
        glVertex2f(-95, 140)

        glColor3f(0.82, 0.82, 0.82)
        glVertex2f(-105, 140)
        glVertex2f(-105, 150)
        glColor3f(1, 1, 1)
        glVertex2f(0, 150)
        glVertex2f(0, 140)
        glEnd()
        for h in range(13):
            y2 = y1 - h * 16
            for i in range(5):
                x2 = x1 + i * 15
                self.windows(x2, y2, 7.2, 4)

    def h4(self):
        x1, y1 = 5, 35
        glBegin(GL_QUADS)
        glColor3f(0.52, 0.6, 0.9)
        glVertex2f(-5, -70)
        glColor3f(0.66, 0.66, 0.98)
        glVertex2f(60, -70)
        glColor3f(0.79, 0.8, 0.99)
        glVertex2f(60, 50)
        glColor3f(0.7, 0.75, 0.88)
        glVertex2f(-5, 50)
        glVertex2f(5, 50)
        glVertex2f(50, 50)
        glColor3f(0.8, 0.9, 0.86)
        glVertex2f(50, 60)
        glVertex2f(5, 60)
        glVertex2f(15, 60)
        glVertex2f(40, 60)
        glColor3f(0.82, 0.82, 0.9)
        glVertex2f(40, 70)
        glVertex2f(15, 70)
        glEnd()

        for h in range(5):
            y2 = y1 - h * 23
            for i in range(3):
                x2 = x1 + i * 22
                self.windows(x2, y2, 6, 6)

    def h5(self):
        glPushMatrix()
        glTranslate(70, 0, 0)
        self.h4()
        glPopMatrix()

    def h6(self):
        x1, y1 = 157, -20
        glBegin(GL_QUADS)
        glColor3f(0.77, 0.82, 0.87)
        glVertex2f(135, -70)
        glColor3f(0.8, 0.76, 0.85)
        glVertex2f(220, -70)
        glColor3f(0.77, 0.69, 0.67)
        glVertex2f(220, -65)
        glColor3f(0.55, 0.65, 0.7)
        glVertex2f(135, -65)
        glColor3f(0.83, 0.85, 0.61)
        glVertex2f(140, -65)
        glColor3f(0.87, 0.89, 0.66)
        glVertex2f(215, -65)
        glColor3f(0.91, 0.92, 0.71)
        glVertex2f(215, 5)
        glColor3f(0.82, 0.88, 0.63)
        glVertex2f(140, 5)
        glColor3f(0.77, 0.82, 0.87)
        glVertex2f(135, 5)
        glColor3f(0.8, 0.76, 0.85)
        glVertex2f(220, 5)
        glColor3f(0.77, 0.69, 0.67)
        glVertex2f(220, 10)
        glColor3f(0.55, 0.65, 0.7)
        glVertex2f(135, 10)
        glColor3f(0.6, 0.3, 0.1)
        glVertex2f(170, -65)
        glVertex2f(185, -65)
        glColor3f(0.5, 0.35, 0.2)
        glVertex2f(185, -45)
        glVertex2f(170, -45)
        glEnd()

        glBegin(GL_TRIANGLES)
        glColor3f(1, 0.61, 0.5)
        glVertex2f(140, 10)
        glVertex2f(215, 10)
        glColor3f(0.94, 0.72, 0.77)
        glVertex2f(177.5, 35)
        glEnd()

        for h in range(1):
            y2 = y1 - h * 23
            for i in range(2):
                x2 = x1 + i * 40
                self.windows(x2, y2, 10, 10)

    def h7(self):
        glBegin(GL_QUADS)
        glColor3f(0.48, 0.54, 0.57)
        glVertex2f(240, -70)
        glVertex2f(270, -70)
        glColor3f(0.64, 0.69, 0.71)
        glVertex2f(262.5, 90)
        glVertex2f(247.5, 90)

        glColor3f(0.53, 0.56, 0.6)
        glVertex2f(230, 80)
        glVertex2f(280, 80)
        glColor3f(0.6, 0.66, 0.68)
        glVertex2f(290, 90)
        glVertex2f(220, 90)

        glVertex2f(220, 90)
        glVertex2f(290, 90)
        glColor3f(0.59, 0.65, 0.67)
        glVertex2f(295, 100)
        glVertex2f(215, 100)

        glVertex2f(215, 100)
        glVertex2f(295, 100)
        glColor3f(0.67, 0.7, 0.72)
        glVertex2f(295, 110)
        glVertex2f(215, 110)

        glVertex2f(215, 110)
        glVertex2f(295, 110)
        glColor3f(0.71, 0.75, 0.76)
        glVertex2f(290, 120)
        glVertex2f(220, 120)

        glVertex2f(220, 120)
        glVertex2f(290, 120)
        glColor3f(0.76, 0.79, 0.8)
        glVertex2f(280, 130)
        glVertex2f(230, 130)

        glColor3f(0.72, 0.72, 0.72)
        glVertex2f(248.5, 130)
        glVertex2f(261.5, 130)
        glColor3f(0.76, 0.83, 0.83)
        glVertex2f(255, 142)
        glVertex2f(255, 142)

        glVertex2f(295, -70)
        glVertex2f(326, -70)
        glVertex2f(326, 50)
        glVertex2f(295, 50)

        glEnd()
        x1, y1 = 230, 112
        for h in range(2):
            y2 = y1 - h * 13
            for i in range(5):
                x2 = x1 + i * 13
                self.windows(x2, y2, 6, 6)

    def boundaries(self, pause):
        glLineWidth(8.5)
        glBegin(GL_LINE_LOOP)
        if self.rainbowmode and not pause:
            glColor3f(random.random(), random.random(), random.random())
        else:
            glColor3f(0, 0, 1)
        glVertex2f(-boundary_leftright, boundary_top)
        glVertex2f(boundary_leftright, boundary_top)
        glVertex2f(boundary_leftright, boundary_bottom)
        glVertex2f(-boundary_leftright, boundary_bottom)
        glEnd()

    def drawcloud(self, x1, y1, r):
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1, 1, 1)
        glVertex2f(x1, y1)
        glColor3f(0.84, 0.84, 0.84)
        for i in range(191):
            x = r * math.cos(math.radians(i - 6)) + x1
            y = r * math.sin(math.radians(i - 6)) + y1 + r
            glVertex2f(x, y)
        for i in range(211):
            x = r * math.cos(math.radians(i + 75)) + x1 - (r + (r / 3))
            y = r * math.sin(math.radians(i + 75)) + y1
            glVertex2f(x, y)
        for i in range(111):
            x = (r + (r / 3)) * math.cos(math.radians(i + 214)) + x1
            y = (r + (r / 3)) * math.sin(math.radians(i + 214)) + y1 - (r / 6)
            glVertex2f(x, y)
        for i in range(211):
            x = r * math.cos(math.radians(i - 105)) + x1 + (r + (r / 3))
            y = r * math.sin(math.radians(i - 105)) + y1
            glVertex2f(x, y)
        glEnd()

    def Cloud_Lists(self):
        for i in range(9):
            if 3<=i<=6:
                x = -300+50*i
            else:
                x = -300+100*i
            self.cloud_list.append([x, self.cloudy[i], self.clouds[i], self.cloud_speed[i]])

    def cloud(self):
        for i in range(len(self.cloud_list)):
            cloud = self.cloud_list[i]
            if -boundary_leftright-15<cloud[0]<boundary_leftright+15:
                self.drawcloud(cloud[0], cloud[1], cloud[2])
            cloud[0] -= cloud[3]
            if cloud[0]<-boundary_leftright-15:
                cloud[0] = boundary_leftright+15

    def Car_Lists(self):
        self.car_list = [[0, -18, -1.2, None, 0], [-50, -18, -1.2, None, 0], [-20, -23.5, -1.5, None, 180], [-150, -23.5, -1.5, None, 180]]
        for car in self.car_list:
            car[3] = random.choice([(0.1, 0.7, 0.1), (0.05, 0.3, 0.75), (0.9, 0.9, 0.01), (0.7, 0.7, 0.7), (0.7, 0.3, 0.8)])

    def car(self):
        for i in range(len(self.car_list)):
            car = self.car_list[i]
            if -75 < car[0] < 75:
                glPushMatrix()
                glRotate(car[4], 0, 1, 0)
                glScaled(9 * 3 / 4, 9 * 3 / 4, 0)
                glTranslate(car[0], car[1], 0)
                self.drawcar(car[3])
                glPopMatrix()
            car[0] -= car[2]
            if car[0] < -75:
                car[0] = 75
                car[3] = random.choice([(0.1, 0.7, 0.1), (0.05, 0.3, 0.75), (0.9, 0.9, 0.01), (0.7, 0.7, 0.7), (0.7, 0.3, 0.8), (0.5, 0.25, 0.75), (0.2, 0.6, 0.95), (0.85, 0.8, 0.85), (0.8, 0.2, 0.05)])
            elif car[0] > 75:
                car[0] = -75
                car[3] = random.choice([(0.1, 0.7, 0.1), (0.05, 0.3, 0.75), (0.9, 0.9, 0.01), (0.7, 0.7, 0.7), (0.7, 0.3, 0.8), (0.5, 0.25, 0.75), (0.2, 0.6, 0.95), (0.85, 0.8, 0.85), (0.1, 0.1, 0.1)])

    def drawcar(self, carclr):
        glPushMatrix()
        glColor(carclr)
        glBegin(GL_POLYGON)
        glVertex2f(2.5, 2.5)
        glVertex2f(19.6, 2.5)
        glVertex2f(20, 2.55)
        glVertex2f(20.9, 3)
        glVertex2f(20.9, 3.5)
        glVertex2f(20.8, 4)
        glVertex2f(20.6, 4.3)
        glVertex2f(20, 4.6)
        glVertex2f(19, 4.8)
        glVertex2f(18, 4.95)
        glVertex2f(17, 5)
        glVertex2f(16, 5.1)
        glVertex2f(15, 6)
        glVertex2f(14, 6.6)
        glVertex2f(13, 7.1)
        glVertex2f(12, 7.4)
        glVertex2f(11, 7.55)
        glVertex2f(10, 7.5)
        glVertex2f(8, 7.1)
        glVertex2f(7, 6.6)
        glVertex2f(6, 5.9)
        glVertex2f(5.2, 5.2)
        glVertex2f(4, 5)
        glVertex2f(3, 4.56)
        glVertex2f(2.1, 4)
        glVertex2f(1.7, 3.5)
        glVertex2f(2, 2.5)
        glVertex2f(5, 2.5)
        glEnd()

        glColor3f(0, 0, 0)
        glLineWidth(4.5)
        glBegin(GL_LINES)
        glVertex2d(9, 4.2)
        glVertex2d(10, 4.2)
        glVertex2d(11.6, 4.2)
        glVertex2d(12.6, 4.2)
        glEnd()

        glColor3f(1, 1, 1)
        glBegin(GL_POLYGON)
        glVertex2f(6, 4.8)
        glVertex2f(10, 4.8)
        glVertex2f(10, 6.6)
        glVertex2f(9, 6.4)
        glVertex2f(8, 6.2)
        glVertex2f(7.2, 5.8)
        glVertex2f(6.6, 5.4)
        glEnd()

        glColor3f(1, 1, 1)
        glBegin(GL_POLYGON)
        glVertex2f(11, 4.8)
        glVertex2f(15, 4.8)
        glVertex2f(14.3, 5.5)
        glVertex2f(13.5, 6)
        glVertex2f(12.4, 6.4)
        glVertex2f(11, 6.6)
        glEnd()

        glColor3f(1, 0, 0)
        glBegin(GL_POLYGON)
        glVertex2f(19, 3.3)
        glVertex2f(20.5, 3.3)
        glVertex2f(21, 3)
        glVertex2f(20.5, 2.5)
        glVertex2f(19.2, 2.5)
        glVertex2f(18.6, 2.9)
        glEnd()

        glColor3f(1, 0, 0)
        glBegin(GL_POLYGON)
        glVertex2f(1.7, 3.2)
        glVertex2f(3.2, 3.2)
        glVertex2f(3.45, 2.8)
        glVertex2f(3.2, 2.5)
        glVertex2f(2, 2.5)
        glEnd()

        glColor3f(1, 1, 0)
        glBegin(GL_POLYGON)
        glVertex2f(2.2, 3.9)
        glVertex2f(3, 3.9)
        glVertex2f(3, 3.3)
        glVertex2f(2.2, 3.3)
        glEnd()

        self.circledraw(6, 2.4, 1.6, (0, 0, 0), (0.3, 0.3, 0.3))
        self.circledraw(16, 2.4, 1.6, (0, 0, 0), (0.3, 0.3, 0.3))
        self.circledraw(20.1, 3.8, 0.6, (0.8, 0.7, 0), (0.9, 0.9, 0))
        glPopMatrix()

    def circledraw(self, x1, y1, r, color1, color2):
        glBegin(GL_TRIANGLE_FAN)
        glColor3fv(color1)
        glVertex2f(x1, y1)
        glColor3fv(color2)
        for i in range(361):
            x = r * math.cos(math.radians(i)) + x1
            y = r * math.sin(math.radians(i)) + y1
            glVertex2f(x, y)
        glEnd()

    def draw(self):
        self.sky()
        self.mountains()
        self.road()
        self.h1()
        self.h2()
        self.h3()
        self.h4()
        self.h5()
        self.h6()
        self.h7()
        self.cloud()
        self.car()

class Ball:
    def __init__(self, x, y, r):
        self.level = 1
        self.r = r
        self.y = y
        self.coords = [[x, y, r, y + 70, 0, boundary_bottom + r + 1, True, False, False, True, boundary_bottom + r + 4]]
        self.coordsbackup = [[y + 70, boundary_bottom + r + 4]]
        self.gamestop = False
        self.ballhitplayer = False

    def drawBall(self):
        for i in range(len(self.coords)):
            ballcoords = self.coords[i]
            glBegin(GL_TRIANGLE_FAN)
            glColor3f(1, 0, 0)
            glVertex2f(ballcoords[0], ballcoords[1])
            glColor3f(0.7, 0, 0)
            for i in range(361):
                x = ballcoords[2] * math.cos(math.radians(i)) + ballcoords[0]
                y = ballcoords[2] * math.sin(math.radians(i)) + ballcoords[1]
                glVertex2f(x, y)
            glEnd()

    # x, y, r, hmax, v, hstop, leftright, hitside, hitbottom, freefall, (boundary_bottom + ballcoords[2] + error)
    def update(self, player, ropestop, time, mute, resetpower, resetbullet, resetweapon, resetrainbow, rightchar):
        g = 6
        dt = 0.1
        rho = 1
        reset = False
        timenow = 0
        error = 4
        self.gamestop = False
        self.levelcomplete(mute, resetpower, resetbullet, resetweapon, resetrainbow, rightchar)
        for i in range(len(self.coords)):
            ballcoords = self.coords[i]
            ballcoordsbackup = self.coordsbackup[i]
            if ballcoords[3] < 0:
                vmax = -sqrt(2 * abs(ballcoords[3]) * g)
            else:
                vmax = sqrt(2 * ballcoords[3] * g)
            if ballcoords[3] > ballcoords[5]:
                if ballcoords[9]:
                    hnew = ballcoords[1] + ballcoords[4] * dt - 0.5 * g * dt * dt
                    if hnew < ballcoords[10]:
                        ballcoords[9] = False
                        ballcoords[1] = ballcoords[10]
                        # print("HITBOTTOM")
                    else:
                        ballcoords[4] = ballcoords[4] - g * dt
                        ballcoords[1] = hnew
                else:
                    vmax = vmax * rho
                    ballcoords[4] = vmax
                    ballcoords[9] = True
                    ballcoords[1] = ballcoords[10]
                    # print("HITBOTTOM")
                # ballcoords[3] = 0.5 * vmax * vmax / g
                if ballcoords[1] > boundary_top - ballcoords[2]:
                    ballcoords[8] = False
                if ballcoords[6]:
                    if ballcoords[0] > boundary_leftright - ballcoords[2] - error:
                        ballcoords[7] = True
                        # print("RIGHTSIDE")
                    if ballcoords[7]:
                        ballcoords[0] -= 1.35
                    if ballcoords[0] < -boundary_leftright + ballcoords[2] + error:
                        ballcoords[7] = False
                        # print("LEFTSIDE")
                    if not ballcoords[7]:
                        ballcoords[0] += 1.35
                else:
                    if ballcoords[0] > boundary_leftright - ballcoords[2] - error:
                        ballcoords[7] = False
                        # print("RIGHTSIDE")
                    if ballcoords[7]:
                        ballcoords[0] += 1.35
                    if ballcoords[0] < -boundary_leftright + ballcoords[2] + error:
                        ballcoords[7] = True
                        # print("LEFTSIDE")
                    if not ballcoords[7]:
                        ballcoords[0] -= 1.35
            if self.intersects(player, ballcoords) or self.ballhitplayer:
                if not mute:
                    if not rightchar:
                        hitplayersnd = random.choice([hitplayer_snd, hitplayer1_snd])
                        hitplayersnd.play()
                    if rightchar:
                        hitashsnd = random.choice([hitash_snd, hitash_snd1])
                        hitashsnd.play()
                timenow = time + 2
                while time < timenow:
                    time = int(glutGet(GLUT_ELAPSED_TIME)/1000)
                self.coords.clear()
                self.coordsbackup.clear()
                if self.level == 1 or self.level == 2 or self.level == 3:
                    self.coords.append([-1 * boundary_leftright + 70, boundary_top - 50, 30, 240, 0, boundary_bottom + 30, True, False, False, True, boundary_bottom + 30 + 4])
                    self.coordsbackup.append([240, boundary_bottom + 30 + 4])
                elif self.level == 4 or self.level == 5:
                    self.coords.append([-1 * boundary_leftright + 70, boundary_top - 50, 30, 240, 0, boundary_bottom + 30, True, False, False, True, boundary_bottom + 30 + 4])
                    self.coords.append([1 * boundary_leftright - 70, boundary_top - 50, 30, 240, 0, boundary_bottom + 30, False, False, False, True, boundary_bottom + 30 + 4])
                    self.coordsbackup.append([240, boundary_bottom + 30 + 4])
                    self.coordsbackup.append([240, boundary_bottom + 30 + 4])
                reset = True
                ropestop = True
                self.gamestop = True
                self.ballhitplayer = False
                break
            ballcoords[3], ballcoords[10] = ballcoordsbackup[0], ballcoordsbackup[1]
        return reset, ropestop, timenow + 90

    def KillBall(self, i):
        splitball = self.coords.pop(i)
        self.coordsbackup.pop(i)
        if splitball[2] > self.r / 6:
            self.coords.append([splitball[0] - 5, splitball[1] + 20, splitball[2] / 2, splitball[3] * 2 / 3, 0,
                                boundary_bottom + splitball[2] / 2 + 1, False, False, False, True, boundary_bottom + splitball[2]/2 + 4, 1.2])
            self.coordsbackup.append([splitball[3] * 2 / 3, boundary_bottom + splitball[2]/2 + 4])
            self.coords.append([splitball[0] + 5, splitball[1] + 20, splitball[2] / 2, splitball[3] * 2 / 3, 0,
                                boundary_bottom + splitball[2] / 2 + 1, True, False, False, True, boundary_bottom + splitball[2]/2 + 4, 1.2])
            self.coordsbackup.append([splitball[3] * 2 / 3, boundary_bottom + splitball[2] / 2 + 4])

    def intersects(self, player, circle):
        distX = 0
        distY = 0
        if circle[0] < player[0]:
            distX = player[0] - circle[0]
        elif circle[0] > player[0]:
            distX = circle[0] - player[0]
        if player[1] > circle[1]:
            distY = player[1] - circle[1]
        elif player[1] < circle[1]:
            distY = circle[1] - player[1]
        distance = sqrt((distX**2) + (distY**2))
        if distance < circle[2] + player[2]:
            return True

    def ropeBall(self, rope, planklist, mute, bulletlist):
        # 0 = x, 1 = y, 2 = shoot
        boxw = 3.25
        ropehitball = False
        balldie = False
        ballradius = 0
        whichball = [0, 0]
        if bulletlist:
            for j in range(len(bulletlist)):
                bulletball = bulletlist[j]
                for i in range(len(self.coords)):
                    ballcoords = self.coords[i]
                    bullethit = self.intersects(bulletball, ballcoords)
                    if bullethit:
                        if not mute:
                            rope_snd.stop()
                            bullethit_snd.play()
                        self.KillBall(i)
                        bulletlist.pop(j)
                        ballradius = ballcoords[2]
                        whichball = [ballcoords[0], ballcoords[1]]
                        ropehitball = True
                        if random.random() > 0.9:
                            balldie = True
                        break
                if ropehitball:
                    break
                for r in range(len(planklist)):
                    blank = planklist[r]
                    if bulletball[1] > blank[1] - blank[3] - 5:
                        if blank[0] - blank[2] < bulletball[0] < blank[0] + blank[2]:
                            bulletlist.pop(j)
                            ropehitball = True
                            break
                if ropehitball:
                    break
            ropehitball = False
        else:
            if rope[2]:
                for i in range(len(self.coords)):
                    ballcoords = self.coords[i]
                    if rope[0] - boxw - ballcoords[2] < ballcoords[0] < rope[0] + boxw + ballcoords[2]:
                        if ballcoords[1] <= rope[1] + ballcoords[2]:
                            if not mute:
                                rope_snd.stop()
                                hitball_snd.play()
                            self.KillBall(i)
                            ropehitball = True
                            ballradius = ballcoords[2]
                            whichball = [ballcoords[0], ballcoords[1]]
                            if random.random() > 0.8:
                                balldie = True
                            break
                for r in range(len(planklist)):
                    blank = planklist[r]
                    if rope[1] > blank[1] - blank[3] - 5:
                        if blank[0] - blank[2] < rope[0] < blank[0] + blank[2]:
                            ropehitball = True
                            break
        return ropehitball, ballradius, whichball, balldie, bulletlist

    def levelcomplete(self, mute, resetpower, resetbullet, resetweapon, resetrainbow, rightchar):
        if len(self.coords) == 0 and self.level < 6:
            if not mute:
                if not rightchar:
                    roundsnd = random.choice([roundclear_snd, roundclear1_snd, roundclear2_snd, roundclear3_snd])
                    roundsnd.play()
                else:
                    round1snd = random.choice([roundclear_snd, roundclear1_snd, roundclear4_snd, roundclear5_snd])
                    round1snd.play()
            self.level += 1
            resetpower.clear()
            resetbullet.clear()
            resetweapon = False
            resetrainbow = False
        return resetpower, resetbullet, resetweapon, resetrainbow

    def levelreset(self):
        if 1 <= self.level<= 3:
            self.coords = [[-1 * boundary_leftright + 70, boundary_top - 50, 30, 240, 0, boundary_bottom + 30, True, False, False, True, boundary_bottom + 30 + 4]]
            self.coordsbackup = [[240, boundary_bottom + 30 + 4]]
        elif self.level == 4 or self.level == 5:
            self.coords = [[-1 * boundary_leftright + 70, boundary_top - 50, 30, 240, 0, boundary_bottom + 30, True, False, False, True, boundary_bottom + 30 + 4], [1 * boundary_leftright - 70, boundary_top - 50, 30, 240, 0, boundary_bottom + 30, False, False, False, True, boundary_bottom + 30 + 4]]
            self.coordsbackup = [[240, boundary_bottom + 30 + 4], [240, boundary_bottom + 30 + 4]]

class Player:
    def __init__(self, x, y, w, h, r, health):
        self.level = 1
        self.x = x
        self.y = y
        self.posxy = [boundary_leftright*3/4, boundary_bottom + 23.5]
        self.width = w
        self.height = h
        self.r = r
        self.restart = False
        self.health = health
        self.left = False
        self.right = False
        self.walkCount = 0
        self.idle = 0

    def loadTexture(self, image):
        textureSurface = pygame.image.load(image).convert_alpha()
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    def drawPlayer(self, rightchar):
        img = 0
        if not rightchar:
            if self.idle + 1 >= 32:
                self.idle = 0
            if self.walkCount + 1 >= 60:
                self.walkCount = 0
            if self.left:
                img = 'img/charleft00.png'
                self.walkCount += 1
                if self.walkCount >= 10 < 20:
                    img = 'img/charleft01.png'
                if self.walkCount >= 20 < 50:
                    img = 'img/charleft02.png'
            if self.right:
                img = 'img/charright00.png'
                self.walkCount += 1
                if self.walkCount >= 10 < 20:
                    img = 'img/charright01.png'
                if self.walkCount >= 20 < 50:
                    img = 'img/charright02.png'
            if not self.left and not self.right:
                img = 'img/char00.png'
                self.idle += 1
                if self.idle >= 8 < 16:
                    img = 'img/char00.png'
                if self.idle >= 16 < 24:
                    img = 'img/char01.png'
                if self.idle >= 24 < 32:
                    img = 'img/char02.png'
        if rightchar:
            if self.idle + 1 >= 32:
                self.idle = 0
            if self.walkCount + 1 >= 35:
                self.walkCount = 0
            if self.left:
                img = 'img/char1left00.png'
                self.walkCount += 1
                if self.walkCount >= 10 < 20:
                    img = 'img/char1left01.png'
                if self.walkCount >= 20 < 30:
                    img = 'img/char1left02.png'
            if self.right:
                img = 'img/char1right00.png'
                self.walkCount += 1
                if self.walkCount >= 10 < 20:
                    img = 'img/char1right01.png'
                if self.walkCount >= 20 < 30:
                    img = 'img/char1right02.png'
            if not self.left and not self.right:
                img = 'img/char.png'
                self.idle += 1
                if self.idle >= 8 < 16:
                    img = 'img/char.png'
                if self.idle >= 16 < 32:
                    img = 'img/char1.png'
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        self.loadTexture(img)
        glPushMatrix()
        glBegin(GL_QUADS)
        glTexCoord(0, 1)
        glVertex3f(self.x - self.width, self.y + self.height, 0)
        glTexCoord(1, 1)
        glVertex3f(self.x + self.width, self.y + self.height, 0)
        glTexCoord(1, 0)
        glVertex3f(self.x + self.width, self.y - self.height, 0)
        glTexCoord(0, 0)
        glVertex3f(self.x - self.width, self.y - self.height, 0)
        glEnd()
        glPopMatrix()
        glDeleteTextures(1)

    def resetPlayer(self):
        if self.level == 1 or self.level == 2 or self.level == 3:
            self.x = boundary_leftright*3/4
            self.y = boundary_bottom + 23.5
            self.posxy = [boundary_leftright*3/4, boundary_bottom + 23.5]
        if self.level == 4 or self.level == 5:
            self.x = 0
            self.y = boundary_bottom + 23.5
            self.posxy = [0, boundary_bottom + 23.5]

    def update(self, resetpower, resetbullet, resetweapon, resetrainbow):
        if self.restart and self.health > 0:
            resetpower.clear()
            resetbullet.clear()
            resetweapon = False
            resetrainbow = False
            self.x, self.y = self.posxy[0], self.posxy[1]
            self.health -= 1
            self.restart = False
        return resetpower, resetbullet, resetweapon, resetrainbow

class Powerups:
    def __init__(self):
        self.width = 10
        self.powerlist = []

    def loadImage(self, image):
        textureSurface = pygame.image.load(image).convert_alpha()
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    def update(self, startpow, poss, powertime, player):
        powpick = -1
        if startpow:
            type = random.randint(0, 2)
            self.powerlist.append([poss[0], poss[1], powertime + 10, True, type])
        if self.powerlist:
            cpow = 0
            for i in range(len(self.powerlist)):
                pickup = False
                rune = self.powerlist[i - cpow]
                if rune[2]-3 <= powertime:
                    if rune[3]:
                        rune[3] = False
                    else:
                        rune[3] = True
                if rune[2] <= powertime:
                    self.powerlist.pop(i - cpow)
                    cpow += 1
                    pickup = True
                if not pickup:
                    distX = 0
                    distY = 0
                    if rune[0] < player[0]:
                        distX = player[0] - rune[0]
                    elif rune[0] > player[0]:
                        distX = rune[0] - player[0]
                    if player[1] > rune[1]:
                        distY = player[1] - rune[1]
                    elif player[1] < rune[1]:
                        distY = rune[1] - player[1]
                    distance = sqrt((distX ** 2) + (distY ** 2))
                    if distance < self.width + player[2]:
                        self.powerlist.pop(i - cpow)
                        cpow += 1
                        powpick = rune[4]
                        break
        return powpick

    def draw(self, pause):
        if self.powerlist:
            cpow = 0
            for i in range(len(self.powerlist)):
                rune = self.powerlist[i - cpow]
                if rune[1] > boundary_bottom + self.width + 4 and not pause:
                    rune[1] -= 1.5
                if rune[3]:
                    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
                    if rune[4] == 0:
                        image = power1
                    elif rune[4] == 1:
                        image = power2
                    elif rune[4] == 2:
                        image = power3
                    self.loadImage(image)
                    glPushMatrix()
                    glBegin(GL_QUADS)
                    glTexCoord(0, 1)
                    glVertex3f(rune[0] - self.width, rune[1] + self.width, 0)
                    glTexCoord(1, 1)
                    glVertex3f(rune[0] + self.width, rune[1] + self.width, 0)
                    glTexCoord(1, 0)
                    glVertex3f(rune[0] + self.width, rune[1] - self.width, 0)
                    glTexCoord(0, 0)
                    glVertex3f(rune[0] - self.width, rune[1] - self.width, 0)
                    glEnd()
                    glPopMatrix()
                    glDeleteTextures(1)

class Rope:
    def __init__(self):
        self.count = 0
        self.time = pygame.time.get_ticks()
        self.shoot = False
        self.ready = False
        self.startx = 0
        self.starty = 0
        self.ropestop = False
        self.gun = False
        self.bullet = False
        self.bullets = []

    def draw(self, pause, mute):
        starty = boundary_bottom - 4
        bulletv = 5
        if not self.gun:
            ropeclr = self.count / 55
            if self.shoot:
                if not mute:
                    rope_snd.play()
                now = pygame.time.get_ticks()
                height = 7.35
                glLineWidth(3)
                glBegin(GL_LINE_STRIP)
                glColor(0 + ropeclr, 1 - ropeclr, 0)
                if self.count <= 55:
                    for i in range(self.count):
                        x = math.sin(starty*480)/0.25 + self.startx
                        starty += height
                        self.starty = starty
                        glVertex2f(x, starty)
                glEnd()
                if now - self.time > 20 and not pause:
                    self.time = now
                    self.count += 1
                    if not mute:
                        rope_snd.play()
                if self.count > 55:
                    rope_snd.stop()
                    self.shoot = False
                    self.ready = False
                    self.count = 0
                    self.startx = boundary_bottom - 5
                    self.starty = boundary_bottom - 5
        else:
            if self.bullets:
                g = 0
                for b in range(len(self.bullets)):
                    ammo = self.bullets[b - g]
                    glBegin(GL_TRIANGLE_FAN)
                    glColor(1, 1, 0)
                    glVertex2f(ammo[0], ammo[1])
                    glColor(0.6, 0.6, 0)
                    for i in range(361):
                        x = 4 * math.cos(math.radians(i)) + ammo[0]
                        y = 4 * math.sin(math.radians(i)) + ammo[1]
                        glVertex2f(x, y)
                    glEnd()
                    if not pause:
                        ammo[1] += bulletv
                    if ammo[1] > boundary_top + 10:
                        self.bullets.pop(b - g)
                        g += 1

    def update(self, startx, mute):
        if not self.gun:
            if not self.ready and self.shoot:
                self.startx = startx
                self.ready = True
        else:
            if self.shoot:
                self.bullets.append([startx, boundary_bottom + 10, 4])
                self.shoot = False
                if not mute:
                    gun_snd.play()
        if self.ropestop and not self.gun:
            self.shoot = False
            self.ready = False
            self.count = 0
            self.startx = boundary_bottom - 5
            self.starty = boundary_bottom - 5
            self.ropestop = False

class Planks:
    def __init__(self):
        self.level = 1
        self.planklist = []

    def drawPlank(self, x, y, w, h):
        plank = [(x-w, y+h), (x+w, y+h), (x+w, y-h), (x-w, y-h)]
        glBegin(GL_QUADS)
        glColor3f(0.5, 0.1, 0.4)
        for vertex in plank:
            glVertex2fv(vertex)
        glEnd()

    def BallCollide(self, balllist):
        error = 4
        for p in range(len(self.planklist)):
            blank = self.planklist[p]
            for i in range(len(balllist)):
                ball = balllist[i]
                if blank[0] - blank[2] - ball[2]< ball[0] < blank[0] + blank[2] + ball[2]:
                    if blank[1] - ball[2] - blank[3] < ball[1] < blank[1] + ball[2] + blank[3]:
                        if blank[0] - blank[2] - ball[2] * 0.8 - error < ball[0] < blank[0] - blank[2] - ball[2] * 0.8 or \
                            blank[0] + blank[2] + ball[2]*0.8 < ball[0] < blank[0] + blank[2] + ball[2]*0.8 + error:
                            if ball[7]:
                                ball[7] = False
                            else:
                                ball[7] = True
                    if blank[0] - blank[2] - ball[2]*0.8 < ball[0] < blank[0] + blank[2] + ball[2]*0.8:
                        if blank[1] + blank[3] < ball[1] < blank[1] + ball[2] + blank[3] + error:
                            ball[10] = blank[1] + blank[3] + ball[2]
                            ball[3] = ball[10] - blank[1] + 54 * ball[2]/30

                        elif blank[1] - ball[2] - blank[3] - error < ball[1] <= blank[1] + blank[3]:
                            ball[4] *= -1
                            ball[3] = blank[1] - blank[3] - ball[2]
        return balllist

    def draw(self):
        self.createplank()
        for drawing in range(1, len(self.planklist)):
            plankcoords = self.planklist[drawing]
            self.drawPlank(plankcoords[0], plankcoords[1], plankcoords[2], plankcoords[3])

    def createplank(self):
        if self.level == 1:
            self.planklist = [(0, boundary_top, boundary_leftright, 3.5)]
        elif self.level == 2:
            self.planklist = [(0, boundary_top, boundary_leftright, 3.5), (0, 50, 120, 3.5)]
        elif self.level == 3:
            self.planklist = [(0, boundary_top, boundary_leftright, 3.5), (-120, 75, 85, 3.5), (120, 75, 85, 3.5)]
        elif self.level == 4:
            self.planklist = [(0, boundary_top, boundary_leftright, 3.5), (0, 80, 5, 175)]
        elif self.level == 5:
            self.planklist = [(0, boundary_top, boundary_leftright, 3.5), (-255, 0, 75, 3.5), (255, 0, 75, 3.5)]
