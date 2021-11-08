import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from settings import *
from BouncingBall import Bg
from win32com.client import Dispatch

pygame.mixer.init()

selection_snd = pygame.mixer.Sound('snd/selection.wav')
select_snd = pygame.mixer.Sound('snd/select.wav')
instruction_snd = pygame.mixer.Sound('snd/instruction.wav')
exit_snd = pygame.mixer.Sound('snd/exit.wav')
ash_snd = pygame.mixer.Sound('snd/ash.wav')
claptrap_snd = pygame.mixer.Sound('snd/claptrap.wav')

game_icon = pygame.image.load('img/iconv2.ico')

speak = Dispatch("SAPI.SpVoice")

pygame.mixer.Sound.set_volume(claptrap_snd, 0.65)
pygame.mixer.Sound.set_volume(ash_snd, 0.65)

class MainMenu:
    def __init__(self):
        self.option1 = True
        self.option2 = False
        self.option3 = True
        self.option4 = False
        self.start = False
        self.mute = False
        self.playmusic = False
        self.keys = False
        self.exit = False
        self.close = False
        self.char = False
        self.rightchar = False
        self.idle = 0
        self.redc = 0.7

    def mainpage(self):
        Background.draw()

    def selection(self):
        UI.drawtext("START GAME", (-200, -210, 0), (0, 1, 0), 1)
        UI.drawtext("INSTRUCTIONS", (100, -210, 0), (0, 1, 0), 1)
        if self.option1:
            self.selectball(-220, -205, 13, (1, 0, 0), (0.6, 0, 0))
            self.option2 = False
        else:
            self.selectball(80, -205, 13, (1, 0, 0), (0.6, 0, 0))
            self.option2 = True

    def instruction(self):
        glBegin(GL_QUADS)
        glColor4f(0.3, 0.5, 0.3, 0.9)
        glVertex2f(-boundary_leftright / 2, boundary_top / 1.5)
        glVertex2f(boundary_leftright / 2, boundary_top / 1.5)
        glVertex2f(boundary_leftright / 2, -boundary_top / 1.5)
        glVertex2f(-boundary_leftright / 2, -boundary_top / 1.5)
        glEnd()
        UI.drawtext("INSTRUCTIONS", (-75, boundary_top / 1.5 - 25, 0), (0.9, 0.8, 0.1), 1)
        UI.drawtext("Welcome to BOUNCE BOUNCE BALL      !", (-145, 110, 0), (0, 0, 0), 0)
        UI.drawtext("V2", (120, 110, 0), (1, 0, 0), 0)
        UI.drawtext("New content added into the game:", (-154, 85, 0), (0, 0, 0), 0)
        UI.drawtext("-New character selection", (-155, 60, 0), (0.3, 0.9, 0.8), 0)
        UI.drawtext("-Powerups added", (-155, 40, 0), (0.3, 0.9, 0.8), 0)
        UI.drawtext("-And more...", (-155, 20, 0), (0.3, 0.9, 0.8), 0)
        UI.drawtext("ESC: Back to Main Menu", (-154, -10, 0), (0, 0, 1), 2)
        UI.drawtext("LEFT RIGHT ARROW KEYS: Move left and right", (-154, -35, 0), (0, 0, 1), 2)
        UI.drawtext("SPACEBAR: Shoot rope", (-154, -60, 0), (0, 0, 1), 2)
        UI.drawtext("ENTER: Confirm", (-154, -85, 0), (0, 0, 1), 2)
        UI.drawtext("M: Mute sound and background music", (-154, -110, 0), (0, 0, 1), 2)
        UI.drawtext("P: Pause", (-154, -135, 0), (0, 0, 1), 2)

    def exitbox(self):
        glBegin(GL_QUADS)
        glColor4f(0.4, 0.1, 0.8, 0.9)
        glVertex2f(-boundary_leftright / 4, boundary_top / 7)
        glVertex2f(boundary_leftright / 4, boundary_top / 7)
        glVertex2f(boundary_leftright / 4, -boundary_top / 7)
        glVertex2f(-boundary_leftright / 4, -boundary_top / 7)
        glEnd()
        UI.drawtext("Exit Game?", (-40, 10, 0), (0, 1, 1), 1)
        UI.drawtext("Yes", (-50, -20, 0), (0.9, 0.8, 0.1), 0)
        UI.drawtext("No", (45, -20, 0), (0.9, 0.8, 0.1), 0)
        if self.option3:
            self.selectball(-60, -16, 5, (1, 0, 0), (0.6, 0, 0))
            self.option4 = False
        else:
            self.selectball(35, -16, 5, (1, 0, 0), (0.6, 0, 0))
            self.option4 = True

    def selectball(self, x1, y1, r, c1, c2):
        glBegin(GL_TRIANGLE_FAN)
        glColor(c1)
        glVertex2f(x1, y1)
        glColor(c2)
        for i in range(361):
            x = r * math.cos(math.radians(i)) + x1
            y = r * math.sin(math.radians(i)) + y1
            glVertex2f(x, y)
        glEnd()

    def selecttriangle(self, x, y, c1, c2, c3):
        glBegin(GL_TRIANGLES)
        glColor(c1)
        glVertex2f(-5 + x, -5 + y)
        glColor(c2)
        glVertex2f(5 + x, 0 + y)
        glColor(c3)
        glVertex2f(-5 + x, 5 + y)
        glEnd()

    def draw(self):
        if self.keys:
            self.instruction()
        if self.close:
            self.exitbox()
        if self.char:
            self.characterpage()

    def characterpage(self):
        self.redc += 0.002
        if self.redc >= 1:
            self.redc = 0.7
        red1 = self.redc
        red2 = self.redc + 0.1
        red3 = self.redc+ 0.2
        if red1 >= 1:
            red1 -= 0.3
        if red2 >=1:
            red2 -= 0.2
        if red3 >=1:
            red3 -= 0.15
        glBegin(GL_QUADS)
        glColor3f(0.47, 0.77, 0.31)
        glVertex2f(-500, -500)
        glVertex2f(500, -500)
        glVertex2f(500, 500)
        glVertex2f(-500, 500)
        glEnd()
        UI.drawtext("Choose Your Player", (-100, boundary_top - 50, 0), (0, 0, 0), 1)
        UI.drawtext("________________", (-103, boundary_top - 53, 0), (0, 0, 0), 1)
        UI.drawtext("Play as CL4P-TP", (-boundary_leftright + 95, boundary_bottom + 25, 0), (1, 1, 1), 1)
        UI.drawtext("Play as Ash Ketchum", (boundary_leftright - 240, boundary_bottom + 25, 0), (1, 1, 1), 1)
        if not self.rightchar:
            self.selecttriangle(-boundary_leftright + 80, boundary_bottom + 31, (red1, 0, 0), (red2, 0, 0), (red3, 0, 0))
        if self.rightchar:
            self.selecttriangle(boundary_leftright - 255, boundary_bottom + 31, (red1, 0, 0), (red2, 0, 0), (red3, 0, 0))
        img = 'img/char00.png'
        if not self.rightchar:
            if self.idle + 1 >= 32:
                self.idle = 0
            self.idle += 1
            if self.idle >= 8 < 16:
                img = 'img/char01.png'
            if self.idle >= 16 < 32:
                img = 'img/char02.png'
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        self.loadTexture(img)
        glPushMatrix()
        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex2f(-boundary_leftright + 60, boundary_bottom + 75)
        glTexCoord(1, 0)
        glVertex2f(-60, boundary_bottom + 75)
        glTexCoord(1, 1)
        glVertex2f(-60, boundary_top - 125)
        glTexCoord(0, 1)
        glVertex2f(-boundary_leftright + 60, boundary_top - 125)
        glEnd()
        glPopMatrix()
        glDeleteTextures(1)
        img1 = 'img/char.png'
        if self.rightchar:
            if self.idle + 1 >= 32:
                self.idle = 0
            self.idle += 1
            if self.idle >= 8 < 16:
                img1 = 'img/char1.png'
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        self.loadTexture(img1)
        glPushMatrix()
        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex2f(60, boundary_bottom + 75)
        glTexCoord(1, 0)
        glVertex2f(boundary_leftright - 60, boundary_bottom + 75)
        glTexCoord(1, 1)
        glVertex2f(boundary_leftright - 60, boundary_top - 125)
        glTexCoord(0, 1)
        glVertex2f(60, boundary_top - 125)
        glEnd()
        glPopMatrix()
        glDeleteTextures(1)

    def loadTexture(self, image):
        textureSurface = pygame.image.load(image).convert_alpha()
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData, GL_LUMINANCE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

UI = UserInterface()
Background = Bg()
MM = MainMenu()
startmain = mainloop()

def main():
    glutInit(sys.argv)
    pygame.init()
    display = (SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_icon(game_icon)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    pygame.display.set_caption('BOUNCE BOUNCE BALL V2')
    gluPerspective(45, (display[0] / display[1]), 0.1, 1000)
    glTranslatef(0, 0, -600)
    speak.Speak("Welcome to Bounce Bounce Ball version 2, prepared by Leong Yau Wah, BS18110437. Enjoy")
    pygame.mixer.music.load('snd/startbgm.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        MM.mainpage()
        MM.selection()
        Background.boundaries(UI.pause)
        MM.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer_music.stop()
                speak.Speak("Thank you for playing")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not MM.keys and not MM.close and not MM.char:
                    MM.option1 = True
                    MM.option2 = False
                    if not MM.mute:
                        selection_snd.play()
                if event.key == pygame.K_RIGHT and not MM.keys and not MM.close and not MM.char:
                    MM.option2 = True
                    MM.option1 = False
                    if not MM.mute:
                        selection_snd.play()
                if event.key == pygame.K_SPACE and not MM.close and not MM.char or event.key == pygame.K_RETURN and not MM.close and not MM.char:
                    if not MM.mute:
                        select_snd.play()
                        instruction_snd.play()
                    if MM.option1:
                        MM.char = True
                        claptrap_snd.play()
                    elif MM.option2:
                        if MM.keys:
                            MM.keys = False
                        else:
                            MM.keys = True
                elif event.key == pygame.K_SPACE and not MM.close or event.key == pygame.K_RETURN and not MM.close:
                    if not MM.rightchar:
                        MM.start = True
                    if MM.rightchar:
                        MM.start = True
                if MM.char:
                    if event.key == pygame.K_RIGHT:
                        MM.rightchar = True
                        if not MM.mute:
                            selection_snd.play()
                            ash_snd.stop()
                            claptrap_snd.stop()
                            ash_snd.play()
                    if event.key == pygame.K_LEFT:
                        MM.rightchar = False
                        if not MM.mute:
                            selection_snd.play()
                            ash_snd.stop()
                            claptrap_snd.stop()
                            claptrap_snd.play()
                if event.key == pygame.K_m:
                    if MM.mute:
                        MM.mute = False
                        if not MM.playmusic:
                            pygame.mixer.music.load('snd/startbgm.wav')
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.5)
                            MM.playmusic = True
                        pygame.mixer.music.unpause()
                    else:
                        MM.mute = True
                        pygame.mixer.music.pause()
                if event.key == pygame.K_ESCAPE and not MM.keys and not MM.char:
                    if not MM.mute:
                        exit_snd.play()
                    MM.close = True
                    MM.option3 = False
                    MM.option4 = True
                if event.key == pygame.K_LEFT and MM.close and not MM.char:
                    if not MM.mute:
                        selection_snd.play()
                    MM.option3 = True
                    MM.option4 = False
                if event.key == pygame.K_RIGHT and MM.close and not MM.char:
                    if not MM.mute:
                        selection_snd.play()
                    MM.option3 = False
                    MM.option4 = True
                if event.key == pygame.K_SPACE and MM.close or event.key == pygame.K_RETURN and MM.close and not MM.char:
                    if not MM.mute:
                        select_snd.play()
                    if MM.option3:
                        pygame.mixer_music.stop()
                        speak.Speak("Thank you for playing")
                        pygame.quit()
                        sys.exit()
                    elif MM.option4:
                        if MM.close:
                            MM.close = False
                        else:
                            MM.close = True
        if MM.start:
            if not MM.mute:
                pygame.mixer.music.load('snd/gamebgm.wav')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)
            else:
                pygame.mixer.music.stop()
            MM.mute = startmain.main(MM.mute, MM.rightchar)
            MM.start = False
            MM.playmusic = False
            MM.char = False
            MM.rightchar = False
            if not MM.mute:
                pygame.mixer.music.load('snd/startbgm.wav')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
            else:
                pygame.mixer.music.stop()
        pygame.display.flip()
if __name__ == "__main__":
    main()