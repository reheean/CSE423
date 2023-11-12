from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import radians, tan
import random

W_Width, W_Height = 500,500
rain = []
x_spacing = 5

x_position = -250

while x_position <= 250:
    x1 = x_position
    y1 = random.uniform(-20, 250)
    length = random.uniform(10, 20)
    y2 = max(y1 - length, -250.0)
    rain.append((x1, y1, y2))
    x_position += x_spacing

def draw_points(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

rain_direction = 0.0

def drawRain():
    global rain_direction

    glColor3f(0.019, 0.988, 0.956)
    glLineWidth(2.0)

    glBegin(GL_LINES)
    for line in rain:
        x1, y1, y2 = line
        angle = -rain_direction if rain_direction < 0 else rain_direction
        max_angle = 60.0
        if angle > max_angle:
            angle = max_angle
        if rain_direction < 0:
            angle = -angle 
        x2_new = x1 + (y2 - y1) * tan(radians(angle))

        glVertex2f(x1, y1)
        glVertex2f(x2_new, y2)
    glEnd()


def specialKeyListener(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction += 2
    elif key == GLUT_KEY_RIGHT:
        rain_direction -= 2

intensity = 0.0

def drawShapes():
    #bg
    global intensity
    red = 0.0 + intensity
    green = 0.0 + intensity
    blue = 0.0 + intensity
    glColor3f(red, green, blue)
    glBegin(GL_QUADS)
    glVertex2d(-250,-250)
    glVertex2d(-250,250)
    glVertex2d(250,250)
    glVertex2d(250,-250)
    glEnd()

    drawRain()

    # roof
    glColor3f(0.501,0.69, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2d(180,0)
    glVertex2d(-180, 0)
    glVertex2d(0,150)
    glEnd()

    #house
    glColor3f(0.96,0.537,0.8)
    glBegin(GL_QUADS)
    glVertex2d(-150,0)
    glVertex2d(-150,-150)
    glVertex2d(150,-150)
    glVertex2d(150,0)
    glEnd()

    #windows
    glColor3f(0.505,0.38,1)
    glBegin(GL_QUADS)
    glVertex2d(-110,-20)
    glVertex2d(-110,-60)
    glVertex2d(-70,-60)
    glVertex2d(-70,-20)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(-90,-20)
    glVertex2f(-90,-60)
    glVertex2f(-110,-40)
    glVertex2f(-70,-40)
    glEnd()

    glColor3f(0.505,0.38,1)
    glBegin(GL_QUADS)
    glVertex2d(110,-20)
    glVertex2d(110,-60)
    glVertex2d(70,-60)
    glVertex2d(70,-20)
    glEnd()

    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(90,-20)
    glVertex2f(90,-60)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(110,-40)
    glVertex2f(70,-40)
    glEnd()

    #door
    glColor3f(0.364,0.062, 0.76)
    glBegin(GL_QUADS)
    glVertex2d(-30,-60)
    glVertex2d(-30,-150)
    glVertex2d(30,-150)
    glVertex2d(30,-60)
    glEnd()

    glColor3f(0.505,0.38,1)
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex2f(-15, -110)
    glEnd()

def specialKeyListener(key, x, y):
    global rain_direction
    global intensity

    if key == GLUT_KEY_LEFT:
        rain_direction += 2
    elif key == GLUT_KEY_RIGHT:
        rain_direction -= 2 
    elif key == GLUT_KEY_UP:
        intensity += 0.01
        if intensity > 1.0:
            intensity = 1.0  
    elif key == GLUT_KEY_DOWN:
        intensity -= 0.01
        if intensity < 0.0:
            intensity = 0.0 

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    drawShapes()
    glutSwapBuffers()

def idle():
    glutPostRedisplay()

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"423 Lab 1 Task 1")
init()

glutDisplayFunc(display)
glutIdleFunc(idle)
glutSpecialFunc(specialKeyListener)


glutMainLoop()