from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

score = 0

W_Width, W_Height = 500, 800
play = True
collision = False
displacement = 0
pb_xmax = 270
pb_xmin = 230
pb_ymax = 65
pb_ymin = 15

xb_xmax = 483
xb_xmin = 416
xb_ymax = 67
xb_ymin = 12

rb_xmax = 81
rb_xmin = 17
rb_ymax = 68
rb_ymin = 11

def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0:
            if dy >= 0:
                return 0  
            else:
                return 7  
        else:
            if dy >= 0:
                return 3  
            else:
                return 4  
    else:
        if dx >= 0:
            if dy >= 0:
                return 1  
            else:
                return 6  
        else:
            if dy >= 0:
                return 2  
            else:
                return 5 
        
def convertZone(x1, y1, zone):
    if zone == 1:
        return y1, x1
    elif zone == 2:
        return -y1, x1
    elif zone == 3:
        return -x1, y1
    elif zone == 4:
        return -x1, -y1
    elif zone == 5:
        return -y1, -x1
    elif zone == 6:
        return y1, -x1
    elif zone == 7:
        return x1, -y1

def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x,y) 
    glEnd()

def drawLine(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1
    points = []

    for x in range(x1, x2 + 1):
        points.append((x, y))  

        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE

    return points

def drawPauseButton():
    glColor3f(0.909, 0.623, 0)
    line_xzone = findZone(-10, 215, -10, 245)
    line_yzone = findZone(10, 215, 10, 245)
    m, n = convertZone(-10, 215, line_xzone)
    o, w = convertZone(-10, 245, line_xzone)
    h, z = convertZone(10, 215, line_yzone)
    u, t = convertZone(10, 245, line_yzone)
    val = drawLine(m, n, o, w)
    vall = drawLine(h, z, u, t)
    temp3 = []
    temp4 = []
    for point in val:
        x, y = point[0], point[1]
        old_x, old_y = convertZone(x, y, line_xzone)
        temp3.append((old_x, old_y))
    for point in temp3:
        a, b = point[0], point[1]
        draw_points(a, b)
    
    for point in vall:
        x, y = point[0], point[1]
        old_x, old_y = convertZone(x, y, line_yzone)
        temp4.append((old_x, old_y))
    for point in temp4:
        a, b = point[0], point[1]
        draw_points(a, b)    

def drawPlayButton():
    glColor3f(0.909, 0.623, 0)
    line_dzone = findZone(-20, 215, -20, 245)
    v, f = convertZone(-20, 215, line_dzone)
    c, d = convertZone(-20, 245, line_dzone)
    val = drawLine(v, f, c, d)
    temp3 = []
    for point in val:
        x, y = point[0], point[1]
        old_x, old_y = convertZone(x, y, line_dzone)
        temp3.append((old_x, old_y))
    for point in temp3:
        a, b = point[0], point[1]
        draw_points(a, b)

    line_c = drawLine(-20, 215, 20, 230)
    for point in line_c:
        a, b = point[0], point[1]
        draw_points(a, b)

    line_dzone = findZone(-20, 245, 20, 230)
    q, r = convertZone(-20, 245, line_dzone)
    s, t = convertZone(20, 230, line_dzone)
    vall = drawLine(q, r, s, t)
    temp4 = []
    for point in vall:
        x, y = point[0], point[1]
        old_x, old_y = convertZone(x, y, line_dzone)
        temp4.append((old_x, old_y))
    for point in temp4:
        a, b = point[0], point[1]
        draw_points(a, b)

catmin = -55
catmax = 55
def drawCatcher():
    global catmax, catmin

    if collision == False:
        glColor3f(1, 1, 1)
    else:
        glColor3f(1.0, 0, 0.066)

    if catmin <= -250:
        catmin = -250
        catmax = catmin + 110 
    elif catmax >= 250:
        displacement = 250 - catmax
        catmin += displacement
        catmax += displacement
    line_a = drawLine(catmin, -235, catmax, -235)
    line_b = drawLine(catmin + 10, -245, catmax - 10, -245)
    line_c = drawLine(catmax - 10, -245, catmax, -235)

    for point in line_a + line_b + line_c:
        x, y = point[0], point[1]
        draw_points(x, y)

    line_dzone = findZone(catmin + 10, -245, catmin, -235)
    a, b = convertZone(catmin + 10, -245, line_dzone)
    c, d = convertZone(catmin, -235, line_dzone)
    val = drawLine(a, b, c, d)
    temp = []
    for point in val:
        x, y = point[0], point[1]
        old_x, old_y = convertZone(x, y, line_dzone)
        temp.append((old_x, old_y))

    for point in temp:
        x, y = point[0], point[1]
        draw_points(x, y)
    glutPostRedisplay()


starting_y = 205
starting_x = 0
drop_speed = 100
last_time = time.time()
catcher_collision = False
diamond_color = (0.505, 0.38, 1)
game_over_printed = False
def drawDiamond():
    global starting_x, starting_y, last_time, collision, drop_speed, score, catcher_collision, diamond_color, game_over_printed

    current_time = time.time()
    elapsed_time = current_time - last_time

    if not collision:
        if -245 <= (starting_y - 10) <= -235 and catmin <= starting_x <= catmax:
            score += 1
            print("Score: ", score)
            catcher_collision = True
            starting_y = 205
            starting_x = int(random.uniform(-250, 250))
            if score % 2 == 0:
                drop_speed += 20
                drop_speed = int(drop_speed)
            diamond_color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
        else:
            starting_y -= int(drop_speed * elapsed_time)
            if starting_y + 10 <= -240:
                collision = True
                
    glColor3f(*diamond_color)
    if catcher_collision:
        starting_y = 205
        starting_x = int(random.uniform(-250, 250))
        catcher_collision = False

    if not collision:
        line_a = drawLine(starting_x - 10, starting_y, starting_x, starting_y + 10)
        line_b = drawLine(starting_x, starting_y - 10, starting_x + 10, starting_y)

        for point in line_a + line_b:
            x, y = point[0], point[1]
            draw_points(x, y)

        line_czone = findZone(starting_x - 10, starting_y, starting_x, starting_y - 10)
        line_dzone = findZone(starting_x, starting_y + 10, starting_x + 10, starting_y)
        a, b = convertZone(starting_x - 10, starting_y, line_czone)
        c, d = convertZone(starting_x, starting_y - 10, line_czone)
        e, f = convertZone(starting_x, starting_y + 10, line_dzone)
        g, h = convertZone(starting_x + 10, starting_y, line_dzone)
        val = drawLine(a, b, c, d)
        vall = drawLine(e, f, g, h)
        temp1 = []
        temp2 = []

        for point in val:
            x, y = point[0], point[1]
            old_x, old_y = convertZone(x, y, line_czone)
            temp1.append((old_x, old_y))

        for point in vall:
            x, y = point[0], point[1]
            old_x, old_y = convertZone(x, y, line_dzone)
            temp2.append((old_x, old_y))

        for point in temp1 + temp2:
            x, y = point[0], point[1]
            draw_points(x, y)
    else:
        if not game_over_printed:
            print("Game Over! Score:", score)
            game_over_printed = True

    if collision and starting_y <= -240 and catmin <= starting_x <= catmax:
        collision = False
        starting_y = 205
        starting_x = int(random.uniform(-250, 250))

    last_time = current_time

def resetScene():
    global starting_x, starting_y, score, collision, drop_speed, diamond_color
    starting_x = 0
    starting_y = 205
    score = 0
    collision = False
    drop_speed = 100
    diamond_color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
    print("Starting Over!")

def drawShapes():
    if play:
        drawPauseButton()
    else:
        drawPlayButton()

    drawCatcher()

    #restart button
    glColor3f(0.086,0.78, 0.572)
    line1 = drawLine(-235, 230, -175, 230)
    line2 = drawLine(-235, 230, -205, 245)
    line3zone = findZone(-235, 230, -205, 215)
    for point in line1 + line2:
        xi, yi = point[0], point[1]
        draw_points(xi, yi)
    p, q = convertZone(-235, 230, line3zone)
    r, s = convertZone(-205, 215, line3zone)
    temp = drawLine(p, q, r, s)
    temp1 = []
    for point in temp:
        x, y = point[0], point[1]
        old_x, old_y = convertZone(x, y, line3zone)
        temp1.append((old_x, old_y))
    for point in temp1:
        a, b = point[0], point[1]
        draw_points(a, b)

    #cross button
    glColor3f(1.0,0,0.066)
    line_a = drawLine(175, 215, 235, 245)
    for point in line_a:
        x1, y1 = point[0], point[1]
        draw_points(x1, y1)
    line_bzone = findZone(175, 245, 235, 215)
    i, j = convertZone(175, 245, line_bzone)
    k, l = convertZone(235, 215, line_bzone)
    tempp = drawLine(i, j, k, l)
    temp2 = []
    for point in tempp:
        x, y = point[0], point[1]
        old_x, old_y = convertZone(x, y, line_bzone)
        temp2.append((old_x, old_y))
    for point in temp2:
        a, b = point[0], point[1]
        draw_points(a, b)

def mouseListener(button, state, x, y):
    global play, starting_y, collision, last_time
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if pb_xmin <= x <= pb_xmax and pb_ymin <= y <= pb_ymax:
            play = not play
            glutPostRedisplay()
        if xb_xmin <= x <= xb_xmax and xb_ymin <= y <= xb_ymax:
            glutLeaveMainLoop()
            print("Goodbye! Score: ", score)
        if rb_xmin <= x <= rb_xmax and rb_ymin <= y <= rb_ymax:
            resetScene()
            starting_y = 205
            play = True
            last_time = time.time()
        

def specialKeyListener(key, x, y):
    global catmin, catmax
    if play == True and collision == False:
        if key == GLUT_KEY_LEFT:
            catmin -= 10
            catmax -= 10
            glutPostRedisplay()
        elif key == GLUT_KEY_RIGHT:
            catmin += 10
            catmax += 10
            glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    drawShapes()
    drawDiamond()

    glutSwapBuffers()

def idle():
    global starting_x, starting_y, collision, drop_speed, last_time, score, play
    
    current_time = time.time()
    elapsed_time = current_time - last_time
    
    if play and not collision:
        starting_y -= drop_speed * elapsed_time
        
        if starting_y <= -240 and catmin <= int(starting_x) <= catmax:
            score += 1
            print("Score: ", score)
            collision = True
            starting_y = 205
            starting_x = random.uniform(-250, 250)
        
        if starting_y <= -250:
            collision = True
            starting_y = -240

    last_time = current_time
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
wind = glutCreateWindow(b"423 Lab 2")
init()
glutDisplayFunc(display)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutIdleFunc(idle)
glutMainLoop()