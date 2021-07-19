from pywavefront import visualization
from pywavefront import Wavefront
from pygame import mixer
from pygame.locals import *
from OpenGL.GLU import *
from OpenGL.GL import *
import pygame
import math
import numpy as np
from PIL import Image

rotacao=1
y=-1
x=0
basquetebola = Wavefront('./objetos/bola.obj')
aro = Wavefront('./objetos/quadra2.obj')

def iluminacao():
    glLightfv(GL_LIGHT0, GL_POSITION, (0.1, 0.1, 0.1, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.0, 0.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, (50))
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_MODELVIEW)

def groundColision(y):
  if(y<=-11.3):
    return True
  else:
    return False

def fakecolision(x,y):
  coordxmax=37.5
  coordymin=-1.5

  if(x<coordxmax and y>coordymin):
    return False
  else:
    return True


def main():
  global rotacao, y, x
  pygame.init() 
  display = (1280, 720) 
  pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
  gluPerspective(45, (display[0]/display[1]), 0.1, 100) 
  glEnable(GL_TEXTURE_2D)
  glEnable(GL_LIGHT0)
  glEnable(GL_LIGHTING)
  glEnable(GL_COLOR_MATERIAL)
  glEnable(GL_DEPTH_TEST)
  glTranslatef(0, 0, -55)
  glRotatef(0,1,1,0)
  iluminacao()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
              
    glPushMatrix()
    glScale(5,5,5)
    glTranslatef(0,-2,0)
    glRotatef(90,0,1,0)
    visualization.draw(aro) 
    glPopMatrix()

    #defino a rotacao incremental, fora da matriz
    rotacao += 5

    #Configurações da Bola
    glPushMatrix()
    glScale(0.9,0.9,1)
    
    # verifico se há colisão com o ferro da tabela
    if(not fakecolision(x,y)):
      y=(-0.045*(x*x)+(1.8*x))
      x+=0.1
      glTranslatef(x,y,-2)
      glRotatef(rotacao,10,8,10)
    else:
      # Verifica colisao com o chao
      if(not groundColision(y)):
        y-=0.2
        glTranslatef(x,y,-2)
        glRotatef(rotacao,10,8,10)
      else:
        glTranslatef(x,-11.3,-2)

    visualization.draw(basquetebola)
    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)

    

   


main()
