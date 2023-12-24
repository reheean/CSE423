from OpenGL.GL import *
from OpenGL.GLUT import *

W_Width = 800
W_Height = 800
circle_points = []
paused = False
speed = 0.5

def draw_points(x, y):
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_circle(center_x, center_y, radius):
    x, y = 0, radius
    d = 1 - radius

    while x <= y:
        draw_points(x + center_x, y + center_y)
        draw_points(y + center_x, x + center_y)
        draw_points(-y + center_x, x + center_y)
        draw_points(-x + center_x, y + center_y)
        draw_points(-x + center_x, -y + center_y)
        draw_points(-y + center_x, -x + center_y)
        draw_points(y + center_x, -x + center_y)
        draw_points(x + center_x, -y + center_y)

        if d < 0:
            d += 2 * x + 3
            x += 1
        else:
            d += 2 * (x - y) + 5
            x += 1
            y -= 1

def drawShapes():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(0.96, 0.537, 0.8)

    for point in circle_points:
        draw_circle(point[0], point[1], point[2])

    glutSwapBuffers()

def mouseListener(button, state, x, y):
    global circle_points, paused
    if not paused and button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        y = W_Height - y
        circle_points.append((x, y, 0))
        glutPostRedisplay()

def pause(key, x, y):
    global paused
    if key == b' ':
        paused = not paused

def specialKeyListener(key, x, y):
    global speed
    if key == GLUT_KEY_LEFT:
        speed += 0.1
    elif key == GLUT_KEY_RIGHT:
        speed = max(0.1, speed - 0.1)

def radius(value):
    global circle_points
    if not paused:
        i = 0
        while i < len(circle_points):
            circle_points[i] = (circle_points[i][0], circle_points[i][1], circle_points[i][2] + value)
            x, y, radius = circle_points[i]
            if (x + radius > W_Width) or (y + radius > W_Height) or (x - radius < 0) or (y - radius < 0):
                del circle_points[i]
            else:
                i += 1
        glutPostRedisplay()


def display():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W_Width, 0, W_Height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()

def idle():
    radius(speed)
    glutPostRedisplay()

def main():
    glutInit()
    glutInitWindowSize(W_Width, W_Height)
    glutCreateWindow(b"Midpoint Circle_21301417")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W_Width, 0, W_Height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutDisplayFunc(drawShapes)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutKeyboardFunc(pause)
    glutSpecialFunc(specialKeyListener)
    glutMainLoop()

if __name__ == "__main__":
    main()