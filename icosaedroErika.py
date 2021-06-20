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


def Icosaedro():
    glBegin(GL_POLYGON)
   # for aresta in arestas:
     #   for vertex in aresta:
       #     glVertex3fv(vertices[vertex])
    for face in faces:
      glColor3fv((1,1,0))
      for vertex in face:
        glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

  # gluPerspective(	GLdouble fovy,GLdouble aspect,GLdouble zNear,GLdouble zFar);

    glTranslatef(0.0, 0.0, -5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(1, 1, 3, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Icosaedro()
        # atualiza o conteudo da tela
        pygame.display.flip()

        pygame.time.wait(10)


main()
