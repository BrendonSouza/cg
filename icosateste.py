# Código baseado no primeiro exercicio proposto.

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
  (0, 0, 1.175571),
  (1.051462, 0, 0.5257311),
  (0.3249197, 1, 0.5257311),
  (-0.8506508, 0.618034, 0.5257311),
  (-0.8506508, -0.618034, 0.5257311),
  (0.3249197, -1, 0.5257311),
  (0.8506508, 0.618034, -0.5257311),
  (0.8506508, -0.618034, -0.5257311),
  (-0.3249197, 1, -0.5257311),
  (-1.051462, 0, -0.5257311),
  (-0.3249197, -1, -0.5257311),
  (0, 0, -1.175571),
)
arestas = (
  (0, 1),
  (0, 2),
  (0, 3),
  (0, 4),
  (0, 5),
  (1, 2),
  (1, 5),
  (1, 6),
  (1, 7),
  (2, 3),
  (2, 6),
  (2, 8),
  (3, 4),
  (3, 8),
  (3, 9),
  (4, 5),
  (4, 9),
  (4, 10),
  (5, 7),
  (5, 10),
  (6, 7),
  (6, 8),
  (6, 11),
  (7, 10),
  (7, 11),
  (8, 9),
  (8, 11),
  (9, 10),
  (9, 11),
  (10, 11)
)

faces = (
  (0, 1, 2),
  (0, 2, 3),
  (0, 3, 4),
  (0, 4, 5),
  (0, 5, 1),
  (1, 5, 7),
  (1, 7, 6),
  (1, 6, 2),
  (2, 6, 8),
  (2, 8, 3),
  (3, 8, 9),
  (3, 9, 4),
  (4, 9, 10),
  (4, 10, 5),
  (5, 10, 7),
  (6, 7, 11),
  (6, 11, 8),
  (7, 10, 11),
  (8, 1, 9),
  (9, 11, 10)
)

colors = (
  (0,30,255),
  (0,0,139),
  (112,128,144),
  (0, 255, 0),
  (0, 0, 255),
  (0, 255, 255),
  (255,254,0),
  (112,128,144),
  (218,165,32),
  (245,222,179),
  (75,0,130),
  (139,0,139),
  (255,0,255),
  (128,0,0),
  (255,165,0),
  (238,232,170),
  (60,179,113),
  (106,90,205),
  (255,255,255),
  (154,205,50),
  (250,128,114)  
)


def Icosaedro():
  i=0
  glEnable(GL_CULL_FACE)
  glCullFace(GL_BACK)
  glBegin(GL_TRIANGLES)

  for face in faces:
    x = 0
    for vertex in face:
      x += 1
      glVertex3fv(vertices[vertex])
      glColor3ub(colors[i][0],colors[i][1],colors[i][2])
    i+=1
  glEnd()


def main():
  pygame.init()
  display = (1366, 766)
  pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
  gluPerspective(75, (display[0]/display[1]), 0.1, 50.0)

# gluPerspective(	GLdouble fovy,GLdouble aspect,GLdouble zNear,GLdouble zFar);

  glTranslatef(0.0, 0.0, -5)
  glRotatef(35, 2, 1, 0)
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          glTranslatef(-0.5,0,0)
        if event.key == pygame.K_RIGHT:
          glTranslatef(0.5,0,0)

        if event.key == pygame.K_UP:
          glTranslatef(0,1,0)
        if event.key == pygame.K_DOWN:
          glTranslatef(0,-1,0)

     
      # glTranslatef(0,0,0)
        
        
    # glRotatef(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Icosaedro()
    # atualiza o conteudo da tela
    pygame.display.flip()
    pygame.time.wait(10)
    
main()
