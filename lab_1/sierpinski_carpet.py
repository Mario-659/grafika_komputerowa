#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def draw_rectangle(c1, c2, c3, c4):
    glBegin(GL_TRIANGLES)
    glVertex2f(c1[0], c1[1])
    glVertex2f(c2[0], c2[1])
    glVertex2f(c4[0], c4[1])    
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(c1[0], c1[1])
    glVertex2f(c4[0], c4[1])
    glVertex2f(c3[0], c3[1])    
    glEnd()


def draw_middle_rectangle(c1, c2 , c3, c4, iteration, recursion_depth):
    if iteration > recursion_depth:
        return
    
    x_3 = math.dist(c1, c2) / 3
    y_3 = math.dist(c1, c3) / 3
    
    for x_i in range(3):
        for y_i in range(3):
            d1 = (c1[0] + x_3 * x_i, c1[1] - y_3 * y_i)
            d2 = (d1[0] + x_3, d1[1])
            d3 = (d1[0], d1[1] - y_3)
            d4 = (d1[0] + x_3, d1[1] - y_3)

            if x_i == 1 and y_i == 1:
                draw_rectangle(d1, d2, d3, d4)
            else:                
                draw_middle_rectangle(d1, d2, d3, d4, iteration+1, recursion_depth)
    

def render(time):

    if len(sys.argv) == 1:
        print("Pass recursion depth as a parameter")
        sys.exit(-1)
    else:
        depth = int(sys.argv[1])

    glClear(GL_COLOR_BUFFER_BIT)

    c1, c2, c3, c4 = (-100, 100), (100, 100), (-100, -100), (100, -100)

    glColor(1, 0, 0)
    draw_rectangle(c1, c2, c3, c4)

    glColor(1, 1, 1)
    draw_middle_rectangle(c1, c2, c3, c4, 0, depth)

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
