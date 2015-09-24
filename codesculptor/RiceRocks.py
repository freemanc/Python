# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
FRAME = [WIDTH, HEIGHT]

ANGULAR_VEL = .05
ACCELERATION = .5
FRICTION_COEF = .05
MISSILE_VEL = 10

score = 0
lives = 3
time = 0
started = False

def game_init():
    global my_ship, rock_group, missile_group
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    rock_group = set()
    missile_group = set()
    soundtrack.rewind()

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(group, canvas):
    for sprite in set(group):
        if sprite.update():
            group.remove(sprite)
        sprite.draw(canvas)

def group_collide(group, other_object):
    for sprite in set(group):
        if sprite.collide(other_object):
            group.remove(sprite)
            return True # immediately return True after one collision happens
    return False
    
def group_group_collide(group1, group2):
    num_of_collision = 0
    for sprite in set(group1):
        if group_collide(group2, sprite):
            group1.discard(sprite)
            num_of_collision += 1
    return num_of_collision


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
        
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        elif self.thrust == True:
            temp_image_center = [self.image_center[0] + self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, temp_image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        if self.thrust == True:
            for dim in range(2):
                self.vel[dim] += ACCELERATION * angle_to_vector(self.angle)[dim]
        
        for dim in range(2):
            self.pos[dim] = (self.pos[dim] + self.vel[dim]) % FRAME[dim]
            self.angle += self.angle_vel
            self.vel[dim] -= FRICTION_COEF * self.vel[dim]
               
    def turn(self, direction):
        if direction == 'left':
            self.angle_vel -= ANGULAR_VEL
        elif direction == 'right':
            self.angle_vel += ANGULAR_VEL
   
    def thrusted(self):
        self.thrust = not self.thrust
        if self.thrust == True:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global missile_group
        temp_pos = [my_ship.pos[0], my_ship.pos[1]]
        temp_vel = [my_ship.vel[0], my_ship.vel[1]]
        for dim in range(2):
            temp_pos[dim] += my_ship.image_size[0] / 2 * angle_to_vector(my_ship.angle)[dim]
            temp_vel[dim] += MISSILE_VEL * angle_to_vector(my_ship.angle)[dim]
    
        missile_group.add(Sprite(temp_pos, temp_vel, 0, 0, missile_image, missile_info, missile_sound))
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_position(self):
        return self.pos
        
    def get_radius(self):
        return self.radius
        
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        for dim in range(2):
            self.pos[dim] = (self.pos[dim] + self.vel[dim]) % FRAME[dim]
            self.angle += self.angle_vel
        
        self.age += 1
        
        if self.age == self.lifespan:
            return True
        else:
            return False  

    def collide(self, other_object):
        if dist(self.get_position(), other_object.get_position()) < self.get_radius() + other_object.get_radius():
            return True
        else:
            return False
           
def draw(canvas):
    global time, started, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw and update rock, missile group
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    score += group_group_collide(rock_group, missile_group)
    if group_collide(rock_group, my_ship):
        lives -= 1

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

    # restart if lives = 0
    if lives == 0:
        started = False
        timer.stop()
        game_init()
        
    
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn('left')
    elif key == simplegui.KEY_MAP['right']:
        my_ship.turn('right')
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusted()
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn('right')
    elif key == simplegui.KEY_MAP['right']:
        my_ship.turn('left')
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusted()

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives, time
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        timer.start()
        score = 0
        lives = 3
        time = 0
        soundtrack.play()
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    difficulty = 1 + float(score) / 10
    if len(rock_group) <= 12:
        pos = [WIDTH / random.randint(1, 8), HEIGHT / random.randint(1, 6)]
        init_vel = [difficulty * (.5 - random.random()), difficulty * (.5 - random.random())]
        ang_vel = (.5 - random.random()) * .1    # generate (-.05, .05]
        if dist(pos, my_ship.get_position()) > 5 * my_ship.get_radius():
            rock_group.add(Sprite(pos, init_vel, 0, ang_vel, asteroid_image, asteroid_info))
       
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and rock, missile sprites
game_init()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()
