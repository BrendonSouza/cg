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
id_textures = []
rotacao=1
y=2.2
x=-10
def iluminacao():
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.0, 0.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, (50))
    glLightfv(GL_LIGHT0, GL_POSITION,(0, 0, -30, 1))
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_MODELVIEW)

def criar_texturas(width, height, pbits):
    id_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id_texture)

    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pbits)
    
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return id_texture

def carregar_imagem(filename):
    global id_textures
    image = Image.open(filename)
    id_texture = criar_texturas(image.size[0], image.size[1], image.convert("RGBA").tobytes("raw", "RGBA"))
    id_textures.append (id_texture)


def point(x,y):
  
  glClear(GL_COLOR_BUFFER_BIT)

  glColor3f(0.0,1.0,0.0)

  glPointSize(5.0)

  glBegin(GL_Points)        # GL_POINTS -> GL_LINES

 

  glVertex2f(x, y)         # Added another Vertex specifying end coordinates of line

  glEnd()

  glFlush()



def main():
  global rotacao, y, x
  flag=True

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
    glScale(3,3,1)
    glTranslatef(8,-1,0)
    visualization.draw(aro) 
    glPopMatrix()
   
    rotacao += 5

    glPushMatrix()
    glScale(2,2,1)
    
    #Para a bola acertar a cesta, ela deve eestar nas cordenadas
    #O ponto máximo da parabola glTranslatef(0.8,10.3,0)
    #Acerta a cesta em: glTranslatef(10.3,7,0)
    if True:
      
      y=((-0.1*x*x)+10.2)
      x+=0.05

      glTranslatef(x,y,0)

    # else:
    #   print("caindo: "+str(y))
    #   glTranslatef(x,y,0)
    #   y-=0.007
    #   x+=0.005
   
    glRotatef(rotacao,10,8,10)
    visualization.draw(basquetebola)
    
    glPopMatrix()
    



    pygame.display.flip()
    pygame.time.wait(10)

    

   
basquetebola = Wavefront('./objetos/bola.obj')
aro = Wavefront('./objetos/tabelinha.obj')

main()
