from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math

W_Width, W_Height = 500, 500

points = []
time = 0
diagonal = [(0.01, 0.01), (-0.01, 0.01), (0.01, -0.01), (-0.01, -0.01),(0.01, 0.02), (-0.01, 0.02), (0.02, 0.01), (0.02, -0.01), (-0.02, 0.01), (-0.02, -0.01)]

time_step = 0.01  
speed_multiplier = 1.0  

animation_frozen = False
background_color = (0.0, 0.0, 0.0)  

def display():
    global time
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glPointSize(5.0)
    glBegin(GL_POINTS)

    for i in range(len(points)):
        x, y, color, vx, vy = points[i]

        if not animation_frozen:
            x += vx * time_step * speed_multiplier
            y += vy * time_step * speed_multiplier
            points[i] = (x, y, color, vx, vy)

        glColor3f(*color)
        glVertex2f(x, y)

    glEnd()

    if not animation_frozen:
        time += 1

    glutSwapBuffers()



def generateRandomColor():
    return [random.random() for i in range(3)]

def assignRandomVelocity():
    return random.choice(diagonal)

def mouseListener(button, state, x, y):
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        num_points = random.randint(1, 10) 
        for _ in range(num_points):
            ndc_x = (x / W_Width * 2) - 1.0
            ndc_y = 1.0 - (y / W_Height * 2)

            color = generateRandomColor()
            vx, vy = assignRandomVelocity()
            points.append((ndc_x, ndc_y, color, vx, vy))
        glutPostRedisplay()

def increaseSpeed():
    global speed_multiplier
    speed_multiplier += 0.1

def decreaseSpeed():
    global speed_multiplier
    speed_multiplier -= 0.1

def specialKeyListener(key, x, y):
    if key == GLUT_KEY_UP:
        increaseSpeed()
    elif key == GLUT_KEY_DOWN:
        decreaseSpeed()
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global animation_frozen, time

    if key == b' ':
        animation_frozen = not animation_frozen
        if animation_frozen:
            time = 0
        glutPostRedisplay()

def idle():
    glutPostRedisplay()

def init():
    global original_background_color
    glClearColor(*background_color, 1.0) 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1) 

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"423 Lab 2 Task 2")
init()

glutDisplayFunc(display)
glutMouseFunc(mouseListener)
glutSpecialFunc(specialKeyListener)  
glutIdleFunc(idle)  
glutKeyboardFunc(keyboardListener)
glutMainLoop()