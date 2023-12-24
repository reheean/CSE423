from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import time
import random

offset = 20
W_Width = 800
W_Height = 950
char_x = 400
char_y = 500 # 50  
char_radius = 20
score = 0
score_str = str(score)
prev_time = time.time()
char_accY = -50
char_velY = 0
char_velX = 0
char_speedX = 20
jump_power = 40
frictionX = 0.95
frictionY = 0.95
canJump = False
paused = False
W_Height_initial = 850
paused_time = time.time()
platform_gap = 120
vanishing_weight = 30
vanishing_time = 2
max_platform_distance = 525

#button boundaries
pb_xmax = 635
pb_xmin = 590
pb_ymax = 80
pb_ymin = 20

xb_xmax = 770
xb_xmin = 710
xb_ymax = 80
xb_ymin = 20

rb_xmax = 515 
rb_xmin = 435
rb_ymax = 80
rb_ymin = 20

left_key = b'a'
right_key = b'd'
jump_key = b' '

keyState = {
    left_key: False,
    right_key: False,
    jump_key: False
}

paused_state = {
    "char_x": 0,
    "char_y": 0,
    "char_velX": 0,
    "char_velY": 0,
    "paused_time": 0
}

digit_segments = {
    '0': [1, 1, 1, 1, 1, 1, 0],  
    '1': [0, 0, 0, 0, 1, 1, 0],  
    '2': [1, 0, 1, 1, 0, 1, 1],  
    '3': [1, 0, 0, 1, 1, 1, 1],  
    '4': [0, 1, 0, 0, 1, 1, 1],  
    '5': [1, 1, 0, 1, 1, 0, 1],  
    '6': [1, 1, 1, 1, 1, 0, 1],  
    '7': [1, 0, 0, 0, 1, 1, 0],  
    '8': [1, 1, 1, 1, 1, 1, 1],  
    '9': [1, 1, 0, 1, 1, 1, 1]  
}

class score8:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.c1 = [0.161, 0.161, 0.114]
        self.s1 = [self.x, self.y, self.x + 30, self.y, self.c1]
        self.s2 = [self.x, self.y - 30, self.x, self.y, self.c1]
        self.s3 = [self.x, self.y - 60, self.x, self.y - 30, self.c1]
        self.s4 = [self.x, self.y - 60, self.x + 30, self.y - 60, self.c1]
        self.s5 = [self.x + 30, self.y - 60, self.x + 30, self.y - 30, self.c1]
        self.s6 = [self.x + 30, self.y - 30, self.x + 30, self.y, self.c1]
        self.s7 = [self.x, self.y - 30, self.x + 30, self.y - 30, self.c1]

score_objects = [score8(250, 930, 1), score8(290, 930, 2), score8(330, 930, 3)] 

def update_score_color(score_str):
    j = list(score_str)
    for k, digit in enumerate(j):
        segment_state = digit_segments[digit]
        segment_attributes = [score_objects[k].s1, score_objects[k].s2, score_objects[k].s3,
                              score_objects[k].s4, score_objects[k].s5, score_objects[k].s6, score_objects[k].s7]
        for m in range(len(segment_state)):
            color = [0.980, 0.980, 0.478] if segment_state[m] == 1 else [0.161, 0.161, 0.114]
            segment_attributes[m][4] = color

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = [0, 1, 0]
        self.radius = 10
        self.direction = random.choice([-1, 1])

enemies = [] 

class Platform:
    def __init__(self, x, y, vanishing = False):
        self.x = x
        self.y = y
        self.vanishing = vanishing
        self.collision_time = 0
        self.collided = False
        self.colors = [1,0,0] if self.vanishing == True else [1,1,1]
        self.width = 150
        self.x1 = int(self.x - self.width/2)
        self.x2 = int(self.x + self.width/2)

platforms = []
platforms.append(Platform(400, 300))
for i in range(7):
    if random.uniform(1, 100) <= vanishing_weight:
        v = True
    else:
        v = False
    
    max_x = min(W_Width - 50, platforms[-1].x + max_platform_distance)
    min_x = max(50, platforms[-1].x - max_platform_distance)
    
    if platforms[-1].x > W_Width - max_platform_distance:
        new_x = random.uniform(min_x, platforms[-1].x)
    elif platforms[-1].x < max_platform_distance:
        new_x = random.uniform(platforms[-1].x, max_x)
    else:
        new_x = random.uniform(min_x, max_x)
    
    new_platform = Platform(new_x, platforms[-1].y + platform_gap, vanishing=v)
    platforms.append(new_platform)

for platform in platforms:
    if random.uniform(0, 1) < 0.3:  
        enemy_x = random.uniform(platform.x1, platform.x2)
        enemy_y = platform.y + offset
        enemies.append(Enemy(enemy_x, enemy_y))


def draw_points(x, y):
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

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
    
    return x1, y1


def lineAlgo(x1, y1, x2, y2):
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

def drawLine(x1, y1, x2, y2, c1=1, c2=1, c3=1):
    glColor3f(c1, c2, c3)
    line_zone = findZone(x1, y1, x2, y2)
    a, b = convertZone(x1, y1, line_zone)
    c, d = convertZone(x2, y2, line_zone)
    points = lineAlgo(a, b, c, d)
    temp = []
    for point in points:
        x, y = point[0], point[1]
        old_x, old_y = convertZone(x, y, line_zone)
        temp.append((old_x, old_y))
    for point in temp:
        e, f = point[0], point[1]
        draw_points(e, f)

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

def reset_game():
    global char_x, char_y, char_velX, char_velY, prev_time, paused, paused_time, platforms, enemies, max_platform_distance
    max_platform_distance = 530
    char_x = 400
    char_y = 500
    char_velX = 0
    char_velY = 0
    prev_time = time.time()
    paused = False
    paused_time = time.time()
    char_x = 400
    char_y = 500
    char_velY = 0
    char_velX = 0
    platforms = []
    platforms.append(Platform(400, 300))
    for i in range(7):
        if random.uniform(1, 100) <= vanishing_weight:
            v = True
        else:
            v = False
    
        max_x = min(W_Width - 50, platforms[-1].x + max_platform_distance)
        min_x = max(50, platforms[-1].x - max_platform_distance)
    
        if platforms[-1].x > W_Width - max_platform_distance:
            new_x = random.uniform(min_x, platforms[-1].x)
        elif platforms[-1].x < max_platform_distance:
            new_x = random.uniform(platforms[-1].x, max_x)
        else:
            new_x = random.uniform(min_x, max_x)
    
        new_platform = Platform(new_x, platforms[-1].y + platform_gap, vanishing=v)
        platforms.append(new_platform)


    enemies = []
    used_platforms = []  
    for platform in platforms:
        if random.uniform(0, 1) < 0.3 and platform not in used_platforms:
            enemy_x = random.uniform(platform.x1, platform.x2)
            enemy_y = platform.y + offset
            enemies.append(Enemy(enemy_x, enemy_y))
            used_platforms.append(platform)

    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global paused
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print(x, y)
        if pb_xmin <= x <= pb_xmax and pb_ymin <= y <= pb_ymax:
            paused = not paused
            glutPostRedisplay()
        if xb_xmin <= x <= xb_xmax and xb_ymin <= y <= xb_ymax:
            glutLeaveMainLoop()
            print("You quit! Score: ", score)
        if rb_xmin <= x <= rb_xmax and rb_ymin <= y <= rb_ymax:
            print("Reset Pressed")
            reset_game()

def keyListener(key, x, y):
    global keyState, platforms

    for k in keyState.keys():
        if key == k:
            keyState[k] = True
            # print(k)


def keyUpListener(key, x, y):
    global keyState

    for k in keyState.keys():
        if key == k:
            keyState[k] = False
            # print(k)

def handleKeyPress():
    global char_velY, char_velX, char_speedX, jump_power, keyState, canJump, paused_state

    if not paused:
        if keyState[left_key]:
            char_velX = -char_speedX * 10
        if keyState[right_key]:
            char_velX = char_speedX * 10
        if keyState[jump_key] and canJump == True:
            char_velY = jump_power * 10
            canJump = False
    else:
        paused_state['char_x'] = char_x
        paused_state['char_y'] = char_y
        paused_state['char_velX'] = char_velX
        paused_state['char_velY'] = char_velY

def pauseButton():
    drawLine(590,870, 590, 930,  0.647, 0.475, 0.988)
    drawLine(630,870, 630, 930,  0.647, 0.475, 0.988)

def playButton():
    drawLine(590,870, 590, 930,  0.647, 0.475, 0.988)
    drawLine(590,870, 635, 900,  0.647, 0.475, 0.988)
    drawLine(590, 930, 635, 900, 0.647, 0.475, 0.988)

def drawShapes():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    #s
    drawLine(20, 930, 50, 930, 0.980, 0.980, 0.478)
    drawLine(20, 900, 20, 930, 0.980, 0.980, 0.478)
    drawLine(20, 900, 50, 900, 0.980, 0.980, 0.478)
    drawLine(50, 870, 50, 900, 0.980, 0.980, 0.478)
    drawLine(20, 870, 50, 870, 0.980, 0.980, 0.478)
    #c
    drawLine(60, 930, 90, 930, 0.980, 0.980, 0.478)
    drawLine(60, 870, 60, 930, 0.980, 0.980, 0.478)
    drawLine(60, 870, 90, 870, 0.980, 0.980, 0.478)
    #o
    drawLine(100, 930, 130, 930, 0.980, 0.980, 0.478)
    drawLine(100, 870, 130, 870, 0.980, 0.980, 0.478)
    drawLine(100, 870, 100, 930, 0.980, 0.980, 0.478)
    drawLine(130, 870, 130, 930, 0.980, 0.980, 0.478)
    #r
    drawLine(140, 930, 170, 930, 0.980, 0.980, 0.478)
    drawLine(140, 870, 140, 930, 0.980, 0.980, 0.478)
    drawLine(140, 900, 170, 930, 0.980, 0.980, 0.478)
    drawLine(140, 900, 170, 870, 0.980, 0.980, 0.478)
    #e
    drawLine(180, 930, 210, 930, 0.980, 0.980, 0.478)
    drawLine(180, 870, 180, 930, 0.980, 0.980, 0.478)
    drawLine(180, 870, 210, 870, 0.980, 0.980, 0.478)
    drawLine(180, 900, 210, 900, 0.980, 0.980, 0.478)

    glColor3f(0.980, 0.980, 0.478)
    draw_circle(230, 920, 5)
    draw_circle(230, 880, 5)

    drawLine(710, 870, 770, 930, 0.988, 0.475, 0.576)
    drawLine(710, 930, 770, 870, 0.988, 0.475, 0.576)
    drawLine(435, 900, 515, 900, 0.4745, 0.8863, 0.9882)
    drawLine(435, 900, 475, 930, 0.4745, 0.8863, 0.9882)
    drawLine(435, 900, 475, 870, 0.4745, 0.8863, 0.9882)
    glColor3f(0.505, 0.38, 1)
    draw_circle(char_x, char_y, char_radius)
    if paused == True:
        playButton()
    else:
        pauseButton()
    update_score_color(score_str)
    for scobjs in score_objects:
        drawLine(scobjs.s1[0], scobjs.s1[1], scobjs.s1[2], scobjs.s1[3], *scobjs.s1[4])
        drawLine(scobjs.s2[0], scobjs.s2[1], scobjs.s2[2], scobjs.s2[3], *scobjs.s2[4])
        drawLine(scobjs.s3[0], scobjs.s3[1], scobjs.s3[2], scobjs.s3[3], *scobjs.s3[4])
        drawLine(scobjs.s4[0], scobjs.s4[1], scobjs.s4[2], scobjs.s4[3], *scobjs.s4[4])
        drawLine(scobjs.s5[0], scobjs.s5[1], scobjs.s5[2], scobjs.s5[3], *scobjs.s5[4])
        drawLine(scobjs.s6[0], scobjs.s6[1], scobjs.s6[2], scobjs.s6[3], *scobjs.s6[4])
        drawLine(scobjs.s7[0], scobjs.s7[1], scobjs.s7[2], scobjs.s7[3], *scobjs.s7[4])
    for obj in platforms:
        if obj.y < 850:
            drawLine(obj.x1, obj.y, obj.x2, obj.y, *obj.colors)
            bottom_y = obj.y - 10
            drawLine(obj.x1, bottom_y, obj.x2, bottom_y, *obj.colors)
            drawLine(obj.x1, bottom_y, obj.x1, obj.y, *obj.colors)
            drawLine(obj.x2, bottom_y, obj.x2, obj.y, *obj.colors)

    for enemy in enemies:
        if enemy.y < 850:
            glColor3f(*enemy.color)
            draw_circle(enemy.x, enemy.y, enemy.radius)

    glutSwapBuffers()



def display():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W_Width, 0, W_Height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()

def poolObjects(obj):
    pooled_obj = platforms.pop(platforms.index(obj))
    y = platforms[-1].y + platform_gap
    max_x = min(W_Width - 50, platforms[-1].x + max_platform_distance)
    min_x = max(50, platforms[-1].x - max_platform_distance)
    
    if platforms[-1].x > W_Width - max_platform_distance:
        new_x = random.uniform(min_x, platforms[-1].x)
    elif platforms[-1].x < max_platform_distance:
        new_x = random.uniform(platforms[-1].x, max_x)
    else:
        new_x = random.uniform(min_x, max_x)

    if random.uniform(1,100) <= vanishing_weight:
        v = True
    else:
        v = False

    new_obj = Platform(new_x, y, vanishing=v)
    del pooled_obj
    platforms.append(new_obj)

def poolEnemies(enemy):
    pooled_enemy = enemies.pop(enemies.index(enemy))
    y = platforms[-1].y + offset
    x = random.uniform(50, W_Width - 50)

    new_enemy = Enemy(x, y)

    del pooled_enemy
    enemies.append(new_enemy)

def update():
    global char_x, char_y, prev_time, char_velY, char_accY, frictionX, char_velX, platforms, canJump, paused_time, paused_state, score, score_str
    
    if not paused:
        handleKeyPress()


        # Delta Time
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time

        elapsed_time = current_time - paused_time
        score = int(elapsed_time) // 5
        score_str = str(score).zfill(3)

        # Gravity
        char_velY += (char_accY * 10) * dt
        char_y += (char_velY * dt)

        # Charecter X Movement
        char_x += (char_velX * dt)
        if char_x - char_radius <= 0:  
            char_x = char_radius
            char_velX = 0  
        elif char_x + char_radius >= W_Width:  
            char_x = W_Width - char_radius
            char_velX = 0
        char_velX *= frictionX 
        if char_y + char_radius >= 850:  
            char_y = 850 - char_radius
            char_velY = 0
        if char_y - char_radius <= 0: 
            print("You fell! Score:", score) 
            glutLeaveMainLoop() 

        for enemy in enemies:
            distance = math.sqrt((char_x - enemy.x) ** 2 + (char_y - enemy.y) ** 2)
            if distance < char_radius + enemy.radius:
                print("Collision with Enemy! Score:", score)
                glutLeaveMainLoop()

        for obj in platforms:
        
            # Platform Collision Checks
            # X collision
            if char_x > obj.x1 - char_radius and char_x < obj.x2 + char_radius:
                # Y Collision
                if char_y <= obj.y + char_radius and char_y >= obj.y - char_radius:
                    # Colliding while falling down only
                    if char_velY < 0:
                        char_velY = 0
                        char_y = obj.y + char_radius
                        canJump = True

                        if not obj.collided and obj.vanishing:
                            obj.collision_time = time.time()
                            obj.collided = True
        
            # Falling Platform
            obj.y -= 1

            # Vanishing Platform
            if obj.vanishing and obj.collided:
                elapsed_time = time.time() - obj.collision_time
                obj.colors[0] = 1 - (elapsed_time/vanishing_time)
                if elapsed_time >= vanishing_time:
                    poolObjects(obj)
            

            if obj.y < -5:
                poolObjects(obj)
        
            for enemy in enemies:
                enemy.x += 0.5 * enemy.direction
                enemy.y -= 0.125
                if enemy.x <= 0 or enemy.x >= W_Width:
                    enemy.direction *= -1
                if enemy.y < -20: 
                    poolEnemies(enemy)

    else:
        if 'paused_state' not in globals():
            paused_state = {
                "char_x": char_x,
                "char_y": char_y,
                "char_velX": char_velX,
                "char_velY": char_velY,
                "paused_time": time.time()
            }
        else:
            paused_state['char_x'] = char_x
            paused_state['char_y'] = char_y
            paused_state['char_velX'] = char_velX
            paused_state['char_velY'] = char_velY
            prev_time = time.time() - (paused_state['paused_time'] - prev_time)

    if paused:
        char_x = paused_state['char_x']
        char_y = paused_state['char_y']
        char_velX = paused_state['char_velX']
        char_velY = paused_state['char_velY']

        prev_time = time.time()
    glutPostRedisplay()



def main():
    glutInit()
    glutInitWindowSize(W_Width, W_Height)
    glutCreateWindow(b"Project 423")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W_Width, 0, W_Height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutDisplayFunc(drawShapes)
    glutMouseFunc(mouseListener)
    glutKeyboardFunc(keyListener)
    glutKeyboardUpFunc(keyUpListener)
    glutIdleFunc(update)
    # glutSpecialFunc(specialKeyListener)
    glutMainLoop()

if __name__ == "__main__":
    main() ext.shazid.mahbub@bracu.ac.bd ext.marshia.nujhat@bracu.ac.bd