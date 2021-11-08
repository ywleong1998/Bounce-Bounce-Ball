import pygame
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from BouncingBall import *

pygame.mixer.init()

lose_snd = pygame.mixer.Sound('snd/lose.wav')
win_snd = pygame.mixer.Sound('snd/win.wav')
highscore0_snd = pygame.mixer.Sound('snd/highscore0.wav')
highscore1_snd = pygame.mixer.Sound('snd/highscore1.wav')
powerup_snd = pygame.mixer.Sound('snd/powerup.wav')
powerup0_snd = pygame.mixer.Sound('snd/powerup0.wav')

pygame.mixer.Sound.set_volume(lose_snd, 0.2)
pygame.mixer.Sound.set_volume(win_snd, 0.2)
pygame.mixer.Sound.set_volume(highscore0_snd, 0.3)
pygame.mixer.Sound.set_volume(highscore1_snd, 0.3)

class UserInterface():
    def __init__(self):
        self.level = 1
        self.TIMER = 90
        self.time = 0
        self.highscore = 0
        self.hpcoordx = [-300, -275, -250, -225, -200]
        self.points = 0
        self.scr = [0, 0, 0, 0, 0]
        self.timeleft = 0
        self.pause = False
        self.pausetime = False
        self.timepaused = 0
        self.entername = False
        self.showscore = False
        self.typing = False
        self.inputname = " "
        self.soundcount = 0

    def heart(self, heartx, hearty):
        glBegin(GL_POLYGON)
        glColor3f(1, 0, 0)
        for i in range(360):
            theta = 2 * math.pi * i / 360
            x = 0.7 * 16 * pow(math.sin(theta), 3) + heartx
            y = 0.7 * (13 * math.cos(theta) - 5 * math.cos(2 * theta) - 2 * math.cos(3 * theta) - math.cos(4 * theta)) + hearty
            glVertex2f(x, y)
        glEnd()

    def heartoutline(self, heartx, hearty):
        glLineWidth(1)
        glBegin(GL_LINE_LOOP)
        glColor3f(1, 1, 1)
        for o in range(360):
            theta = 2 * math.pi * o / 360
            x = 0.7 * 16 * pow(math.sin(theta), 3) + heartx
            y = 0.7 * (13 * math.cos(theta) - 5 * math.cos(2 * theta) - 2 * math.cos(3 * theta) - math.cos(4 * theta)) + hearty
            glVertex2f(x, y)
        glEnd()

    def timerclock(self):
        degree = int(self.timeleft/90*360)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0, 1, 1)
        glVertex2f(8, boundary_bottom - 60)
        for i in range(degree):
            x = 13 * math.cos(math.radians(i+90)) + 8
            y = 13 * math.sin(math.radians(i+90)) + boundary_bottom - 60
            glVertex2f(x, y)
        glEnd()

    def drawtext(self, text, pos, color, font):
        glColor3fv(color)
        glRasterPos3fv(pos)
        if font == 0:
            for i in range(len(text)):
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(text[i]))
        elif font == 1:
            for i in range(len(text)):
                glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(text[i]))
        elif font == 2:
            for i in range(len(text)):
                glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(text[i]))

    def text(self):
        self.time = int(glutGet(GLUT_ELAPSED_TIME) / 1000)
        if self.points > 0:
            self.scr[self.level - 1] += int(300/self.points)
        scr = str(self.scr[self.level - 1])
        highscr = str(self.highscore)
        scrtxt = "SCORE"
        highscrtxt = "HIGHSCORE"
        if self.pause:
            self.timeleft = self.TIMER - self.timepaused
        else:
            self.timeleft = self.TIMER - self.time
        timer = str(self.timeleft)
        hp = "HEALTH : " + str(PlayerBox.health)
        leveltxt = "LEVEL : " + str(self.level)
        timetext = "TIME LEFT"
        self.drawtext(hp, (-310, boundary_bottom - 23, 0), (1, 0, 1), 0)
        self.drawtext(leveltxt, (-310, boundary_bottom - 72, 0), (1, 0, 1), 0)
        self.drawtext(timer, (0, boundary_bottom - 40, 0), (0, 1, 1), 0)
        self.drawtext(timetext, (-30, boundary_bottom - 23, 0), (0, 1, 1), 0)
        self.drawtext(scr, (boundary_leftright - 55, boundary_bottom - 40, 0), (1, 0.5, 0.1), 0)
        self.drawtext(scrtxt, (boundary_leftright - 75, boundary_bottom - 23, 0), (1, 0.5, 0.1), 0)
        self.drawtext(highscr, (boundary_leftright - 65, boundary_bottom - 73, 0), (1, 0.5, 0.1), 0)
        self.drawtext(highscrtxt, (boundary_leftright - 95, boundary_bottom - 57, 0), (1, 0.5, 0.1), 0)

    def draw(self, mute):
        self.PauseMenu()
        for i in range(PlayerBox.health):
            self.heart(self.hpcoordx[i], boundary_bottom - 40)
        self.heartoutline(-300, boundary_bottom - 40)
        self.heartoutline(-275, boundary_bottom - 40)
        self.heartoutline(-250, boundary_bottom - 40)
        self.heartoutline(-225, boundary_bottom - 40)
        self.heartoutline(-200, boundary_bottom - 40)
        self.text()
        self.timerclock()
        if BounceBall.level == 6 or PlayerBox.health == 0:
            self.pause = True
            self.inputbox(mute)

    def PauseMenu(self):
        if self.pause and not self.pausetime:
            self.timepaused = self.time
            self.pausetime = True
        if self.pausetime and not self.pause:
            self.TIMER = self.TIMER + (self.time - self.timepaused)
            self.pausetime = False

    def inputbox(self, mute):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_QUADS)
        glColor4f(0.1, 0.2, 0.3, 0.8)
        glVertex2f(-boundary_leftright / 2, boundary_top / 1.5)
        glVertex2f(boundary_leftright / 2, boundary_top / 1.5)
        glVertex2f(boundary_leftright / 2, -boundary_top / 1.5)
        glVertex2f(-boundary_leftright / 2, -boundary_top / 1.5)
        glEnd()
        if not self.showscore:
            if not self.typing:
                self.inputname = "Please enter your name"
            if BounceBall.level == 6:
                if not mute and self.soundcount == 0:
                    win_snd.play()
                    self.soundcount = 1
                line1 = "YOU WIN"
            else:
                line1 = "YOU LOSE"
                if not mute and self.soundcount == 0:
                    lose_snd.play()
                    self.soundcount = 1
            line2 = "Your Score"
            line3 = str(self.scr[self.level - 1])
    
            glPushMatrix()
            glTranslate(0, -30, 0)
            glBegin(GL_QUADS)
            glColor3f(0, 0.1, 0.1)
            glVertex2f(-boundary_leftright / 3, boundary_top / 12)
            glVertex2f(boundary_leftright / 3, boundary_top / 12)
            glVertex2f(boundary_leftright / 3, -boundary_top / 12)
            glVertex2f(-boundary_leftright / 3, -boundary_top / 12)
            glEnd()
            glPopMatrix()

            self.drawtext(line1, (-35, 130, 0), (0, 1, 0), 0)
            self.drawtext(line2, (-40, 90, 0), (0, 1, 0), 0)
            self.drawtext(line3, (-10, 35, 0), (0, 1, 0), 0)
            self.drawtext(self.inputname, (-75, -35, 0), (0, 0.5, 0.5), 0)

        else:
            lime = []
            if len(self.loadscore()) >= 6:
                name = 6
            else:
                name = len(self.loadscore())
            for l in range(name):
                lame = self.loadscore()[l]
                lime.append(lame[0])
                lime.append(lame[1])
            nline0 = "HIGHSCORE"
            nline10 = str(lime[0])
            nline11 = str(lime[1])
            nlinelast = "Your Score : " + str(self.scr[self.level - 1])
            self.drawtext(nline0, (-45, 130, 0), (1, 0, 0), 1)
            self.drawtext(nline10, (-125, 80, 0), (0, 1, 0), 0)
            self.drawtext(nline11, (100, 80, 0), (0, 1, 0), 0)
            if len(lime) > 3:
                self.drawtext(str(lime[2]), (-125, 45, 0), (0, 1, 0), 0)
                self.drawtext(str(lime[3]), (100, 45, 0), (0, 1, 0), 0)
            if len(lime) > 5:
                self.drawtext(str(lime[4]), (-125, 10, 0), (0, 1, 0), 0)
                self.drawtext(str(lime[5]), (100, 10, 0), (0, 1, 0), 0)
            if len(lime) > 7:
                self.drawtext(str(lime[6]), (-125, -25, 0), (0, 1, 0), 0)
                self.drawtext(str(lime[7]), (100, -25, 0), (0, 1, 0), 0)
            if len(lime) > 9:
                self.drawtext(str(lime[8]), (-125, -60, 0), (0, 1, 0), 0)
                self.drawtext(str(lime[9]), (100, -60, 0), (0, 1, 0), 0)
            if len(lime) > 11:
                self.drawtext(str(lime[10]), (-125, -95, 0), (0, 1, 0), 0)
                self.drawtext(str(lime[11]), (100, -95, 0), (0, 1, 0), 0)
            self.drawtext(nlinelast, (-50, -140, 0), (0, 0, 1), 1)
            if self.scr[self.level - 1] == lime[1] and name >= 1:
                if not mute and self.soundcount == 1:
                    win_snd.stop()
                    lose_snd.stop()
                    highscore1_snd.play()
                    self.soundcount = 2
            elif name >= 2 and self.scr[self.level - 1] == lime[3] or name >= 3 and self.scr[self.level - 1] == lime[5] or name >= 4 and self.scr[self.level - 1] == lime[7] \
                    or name >= 5 and self.scr[self.level - 1] == lime[9] or name == 6 and self.scr[self.level - 1] == lime[11]:
                if not mute and self.soundcount == 1:
                    win_snd.stop()
                    lose_snd.stop()
                    highscore0_snd.play()
                    self.soundcount = 2

    def uploadscore(self):
        with open("HighScores.txt", 'a') as f:
            f.write(str(self.inputname)+"\n" + str(self.scr[self.level - 1]) + "\n")

    def loadscore(self):
        s = 0
        namelist, scorelist, finallist = [], [], []
        f = open("HighScores.txt", 'r')
        for x in f:
            if s % 2 == 0:
                namelist.append(x.replace('\n', ''))
            else:
                scorelist.append(int(x.replace('\n', '')))
            s += 1
        if len(scorelist) == 0:
            with open("HighScores.txt", 'a') as f:
                f.write('GodGamer' + "\n" + str(10000) + "\n")
            f = open("HighScores.txt", 'r')
            for x in f:
                if s % 2 == 0:
                    namelist.append(x.replace('\n', ''))
                else:
                    scorelist.append(int(x.replace('\n', '')))
                s += 1
        for y in range(len(namelist)):
            finallist.append((namelist[y], scorelist[y]))
        return sorted(finallist, key=lambda x: (-x[1], x[0]))

    def UIMain(self, timecounter):
        if timecounter > self.TIMER or self.timeleft < 0:
            if self.timeleft < 0:
                self.TIMER += 90
                BounceBall.ballhitplayer = True
            else:
                self.TIMER = timecounter
            if PlayerBox.health > 0:
                if self.level == 1:
                    self.scr[self.level - 1] = 0
                else:
                    self.scr[self.level - 1] = self.scr[self.level - 2]

ShootRope = Rope()
PlayerBox = Player(boundary_leftright*3/4, boundary_bottom + 23.5, 15, 20, 20, 5)
BounceBall = Ball(-1 * boundary_leftright + 70, boundary_top - 50, 30)
PlankBox = Planks()
Power = Powerups()
Background = Bg()
UI = UserInterface()

class mainloop:
    def __init__(self):
        self.nextlevel = 1
        self.startlevel = False
        self.game = True
        self.playmusic = False
        self.limit = 0
        self.switch = False

    def clearall(self):
        self.playmusic = False
        BounceBall.level = 1
        UI.hpcoordx = [-300, -275, -250, -225, -200]
        PlayerBox.health = 5
        UI.scr = [0, 0, 0, 0, 0]
        Power.powerlist.clear()
        self.nextlevel = 1
        self.startlevel = False
        self.game = True
        self.limit = 0
        ShootRope.ropestop = True
        UI.pause = False
        UI.entername = False
        UI.showscore = False
        UI.typing = False
        UI.soundcount = 0
        BounceBall.levelreset()
        Background.rainbowmode = False
        loadhighscore = UI.loadscore()
        highest = loadhighscore[0]
        UI.highscore = highest[1]

    def activate(self, powpick, mute):
        if powpick == 0:
            if not mute:
                powerup0_snd.play()
            if PlayerBox.health < 5:
                PlayerBox.health += 1
            else:
                UI.scr[UI.level - 1] += 1000
        elif powpick == 1:
            if not mute:
                powerup0_snd.play()
            UI.TIMER += 10
        elif powpick == 2:
            self.switch = True
            if not mute:
                powerup_snd.stop()
                powerup_snd.play()
        if self.switch and not ShootRope.shoot:
            self.switch = False
            ShootRope.gun = True
            Background.rainbowmode = True
            self.limit = UI.time + 5
        if ShootRope.gun and UI.time > self.limit:
            ShootRope.gun = False
            Background.rainbowmode = False
            ShootRope.bullets.clear()

    def main(self, mute, rightchar):
        self.clearall()
        clock = pygame.time.Clock()
        while self.game:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if not UI.showscore and self.nextlevel == 7 or not UI.showscore and PlayerBox.health == 0:
                        if event.key == pygame.K_RETURN:
                            UI.uploadscore()
                            UI.showscore = True
                        elif event.key == pygame.K_BACKSPACE:
                            UI.inputname = UI.inputname[:-1]
                        else:
                            if pygame.K_a <= event.key <= pygame.K_z:
                                if not UI.typing:
                                    UI.typing = True
                                    UI.inputname = ''
                                if len(UI.inputname) < 15:
                                    UI.inputname += event.unicode
                    if event.key == pygame.K_ESCAPE:
                        powerup_snd.stop()
                        self.game = False
                    if event.key == pygame.K_SPACE and not BounceBall.gamestop and not UI.pause and not self.startlevel and len(BounceBall.coords) > 0:
                        ShootRope.shoot = True
                    if event.key == pygame.K_p:
                        if UI.pause:
                            UI.pause = False
                        else:
                            UI.pause = True
                    if event.key == pygame.K_m and not UI.showscore:
                        if mute:
                            mute = False
                            if not self.playmusic:
                                pygame.mixer.music.load('snd/gamebgm.wav')
                                pygame.mixer.music.play(-1)
                                self.playmusic = True
                            pygame.mixer.music.unpause()
                        else:
                            mute = True
                            pygame.mixer.music.pause()
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and PlayerBox.x - PlayerBox.r > -boundary_leftright and not UI.pause:
                PlayerBox.left = True
                PlayerBox.right = False
                PlayerBox.x -= 2.5
            if key[pygame.K_RIGHT] and PlayerBox.x + PlayerBox.r < boundary_leftright and not UI.pause:
                PlayerBox.right = True
                PlayerBox.left = False
                PlayerBox.x += 2.5
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not UI.pause or key[pygame.K_RIGHT] and key[pygame.K_LEFT] and not UI.pause:
                PlayerBox.left = False
                PlayerBox.right = False
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glClearDepthf(1)
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LEQUAL)
            Background.Background()
            if self.startlevel:
                self.startlevel = False
                if BounceBall.level == 1:
                    UI.TIMER = UI.time + 90
            if not UI.pause:
                BounceBall.coords = PlankBox.BallCollide(BounceBall.coords)
                PlayerBox.restart, ShootRope.ropestop, timecounter = BounceBall.update((PlayerBox.x, PlayerBox.y, PlayerBox.r), ShootRope.ropestop, UI.time, mute, Power.powerlist, ShootRope.bullets, ShootRope.gun, Background.rainbowmode, rightchar)
                UI.UIMain(timecounter)
                ShootRope.update(PlayerBox.x, mute)
                Power.powerlist, ShootRope.bullets, ShootRope.gun, Background.rainbowmode = PlayerBox.update(Power.powerlist, ShootRope.bullets, ShootRope.gun, Background.rainbowmode)
                ShootRope.ropestop, UI.points, PowerPos, BallRIP, ShootRope.bullets = BounceBall.ropeBall((ShootRope.startx, ShootRope.starty, ShootRope.shoot), PlankBox.planklist, mute, ShootRope.bullets)
                powpow = Power.update(BallRIP, PowerPos, UI.time, (PlayerBox.x, PlayerBox.y, PlayerBox.r))
                self.activate(powpow, mute)
                if BounceBall.level == 1 and self.nextlevel == 1 or BounceBall.level == 2 and self.nextlevel == 2 or BounceBall.level == 3 and self.nextlevel == 3 or \
                        BounceBall.level == 4 and self.nextlevel == 4 or BounceBall.level == 5 and self.nextlevel == 5 or BounceBall.level == 6 and self.nextlevel == 6:
                    if not self.nextlevel == 6:
                        PlayerBox.level = PlankBox.level = UI.level = BounceBall.level
                        BounceBall.levelreset()
                        PlayerBox.resetPlayer()
                    else:
                        UI.scr[UI.level - 2] += (PlayerBox.health * 750)
                    if BounceBall.level >= 2:
                        UI.scr[UI.level - 2] += (UI.timeleft * 15)
                        UI.scr[UI.level - 1] = UI.scr[UI.level - 2]
                        pygame.time.delay(3000)
                        UI.TIMER = UI.time + 93
                    self.nextlevel += 1
                    self.startlevel = True
            PlankBox.draw()
            ShootRope.draw(UI.pause, mute)
            PlayerBox.drawPlayer(rightchar)
            BounceBall.drawBall()
            Power.draw(UI.pause)
            UI.draw(mute)
            Background.boundaries(UI.pause)
            pygame.display.flip()
        return mute

