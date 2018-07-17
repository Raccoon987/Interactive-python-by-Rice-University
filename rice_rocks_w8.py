# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
#when ship is moving - change image ship to image of ship with thusters
thrusters_on = False
age = 0 
#list containing rocks and missiles
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# radius - for easier detection of collisions, lifespan for rockets - after some 
# period of time they dissapear, animation for possible explosion of asteriods 
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
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
#ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    global missile_group, missiles
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.thrust = False
       
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_velocity(self):
        return self.vel
    
    def get_angle(self):
        return self.angle
    
    def get_angle_velocity(self):
        return self.angle_vel
        
    #def dist(p,q):  return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)
    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius():
            return True
        return False
    
    def draw(self,canvas):
       
        #canvas.draw_image(self.image, center_source, width_height_source, center_dest, width_height_dest, rotation)
        if thrusters_on:
            new_image_center = (self.image_center[0] + 90, self.image_center[1])
            canvas.draw_image(ship_image, new_image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        #update angle
        self.angle = self.angle + self.angle_vel
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
        #friction
        c = 0.05
        #position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        #friction update
        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)
        #thrust update - acceleration in direction of forward vector
        forward = [math.cos(self.angle), math.sin(self.angle)]
        if self.thrust:
            self.vel[0] += forward[0]*0.8
            self.vel[1] += forward[1]*0.8    
        
    def set_position(self, position):
        self.pos[0] = position[0] 
        self.pos[1] = position[1] 
    
    def set_angle(self, angle):
        self.angle = angle
    
    def set_angle_vel(self, angle_vel):
        self.angle_vel = angle_vel
    
    def set_thrust(self, change):
        self.thrust = change
    
    def set_vel(self, velocity):
        self.vel[0] = velocity[0] 
        self.vel[1] = velocity[1] 
    
    def shoot(self):
        
        velocity = [0, 0]
        
        velocity[0] = 12 * angle_to_vector(self.angle)[0] + self.vel[0] 
        velocity[1] = 12 * angle_to_vector(self.angle)[1] + self.vel[1]
        
        # missile must appear at the front of ship. my_ship.get_position() - center of the ship "+"
        # projection of "radius" of the ship at "x" and "y" axes
        missile_position = [0, 0]
        # I add "5 * angle_to_vector(self.angle)" because I could not adjust missile start 
        # position with symmetry center of the ship. Missile start not at canon position.
        # So I add mystery constant "5"
        missile_position[0] = 5 * angle_to_vector(self.angle)[1] + self.pos[0] + (self.radius) * angle_to_vector(self.angle)[0]
        missile_position[1] = -5 * angle_to_vector(self.angle)[0] + self.pos[1] + (self.radius) * angle_to_vector(self.angle)[1] 
        
        #a_missile1 = Sprite(missile_position, velocity, self.angle, 0, missile_image, missile_info, missile_sound)
        #I add first missile to list. Later this list will contain many missiles
        missile_group.add(Sprite(missile_position, velocity, self.angle, 0, missile_image, missile_info, missile_sound))
        # ----------------------------------------------------------------------
                
    
# Sprite class
class Sprite:
    global age
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
    
    def get_velocity(self):
        return self.vel
    
    def get_angle(self):
        return self.angle
    
    def get_angle_velocity(self):
        return self.angle_vel
    
    def draw(self, canvas):
        global age  
        if self.animated == False:
            #canvas.draw_image(ship_image, center_source, width_height_source, center_dest, width_height_dest, rotation)
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        elif self.animated == True:
            # explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
            explosion_index = age % 24
            canvas.draw_image(self.image, [self.image_center[0] + explosion_index * self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
            age +=1
            
        
    def update(self):
        # increase age of missile by "1" each call of update method. When this age is greater 
        # than lifespan of missile in missile_info - destroy this missile
        self.age += 1
        
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0])% WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1])% HEIGHT 
        
        if self.age >= self.lifespan:
            return True
        else:
            return False
        
    #def dist(p,q):  return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)
    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius():
            return True
        return False
        
        
# define keyhandlers to control spaceship_angle
def keydown(key):
    global my_ship, thrusters_on 
        
    if (simplegui.KEY_MAP["left"] == key):
        my_ship.set_angle_vel(-0.05)
    elif (simplegui.KEY_MAP["right"] == key):
        my_ship.set_angle_vel(0.05)
    elif (simplegui.KEY_MAP["up"] == key):
        my_ship.set_thrust(True)
        direct = angle_to_vector(my_ship.angle)
        direction = [direct[0] * 0.5, direct[1] * 0.5]
        
        my_ship.set_vel(direction)
        thrusters_on = True
    elif (simplegui.KEY_MAP["space"] == key):
        my_ship.shoot() 
    

  
def keyup(key):
    global my_ship, thrusters_on 
    
    if (simplegui.KEY_MAP["left"] == key):
        my_ship.set_angle_vel(0)
    elif (simplegui.KEY_MAP["right"] == key):
        my_ship.set_angle_vel(0)
    elif (simplegui.KEY_MAP["up"] == key):
        thrusters_on = False
        my_ship.set_thrust(False)    
    

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True    
           
def draw(canvas):
    global rock_group, missile_group, explosion_group, lives, score, time, my_ship, started, thrusters_on, explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    #WIDTH = 800
    #HEIGHT = 600
    canvas.draw_text("LIVES", (WIDTH - 700, HEIGHT - 500), 30, "White")
    canvas.draw_text("SCORE", (WIDTH - 200, HEIGHT - 500), 30, "White")
    canvas.draw_text(str(lives), (WIDTH - 675, HEIGHT - 440), 35, "White")
    canvas.draw_text(str(score), (WIDTH - 165, HEIGHT - 440), 35, "White")

    
    if started:
        
        soundtrack.play()
                
        # draw ship and sprites
        my_ship.draw(canvas)
        
        # update ship and sprites
        my_ship.update()
        
        timer.start()
        
        # draw all rocks, update all rocks.   
        process_sprite_group(rock_group, canvas)
    
        # draw all missiles, update all missiles. 
        process_sprite_group(missile_group, canvas)
        
        process_sprite_group(explosion_group, canvas)
    
        # use the group_collide helper to determine if the ship 
        # hit any of the rocks. If so, decrease the number of lives by one
        if group_collide(rock_group, my_ship):
            lives = lives - 1
    
        group_group_collide(rock_group, missile_group) 
        
        # check if lives = 0 - restart game
        if lives == 0:
            timer.stop()
            ship_thrust_sound.rewind()
            thrusters_on = False
            remove_rock_group = set([])
            remove_missile_group = set([])
            remove_explosion_group = set([])
            
            clear_set(rock_group, remove_rock_group)
            clear_set(missile_group, remove_missile_group)
            clear_set(explosion_group, remove_explosion_group)
                                  
            started = False
            lives = 3
            score = 0
            my_ship.set_vel([0, 0])
            my_ship.set_position([WIDTH / 2, HEIGHT / 2])
            my_ship.set_angle(0)
            
    else:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
           

# helper function takes set group and an a sprite "other_object"
# and check for collisions between "other_object" and elements of the group       
def group_collide(group, other_object):
    global explosion_group
    remove_set = set([])
    for element_1 in group:
        if other_object.collide(element_1):
            # remove "element" from group
            remove_set.add(element_1)
            explosion_group.add(Sprite(element_1.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
            group.difference_update(remove_set)  
            return True
    return False    

# helper function takes set group, another set group and check for collisions
# between s of this groups
def group_group_collide(group_one, group_two):
    global score
    remove_set = set([])
    for element_2 in group_one:
        if group_collide(group_two, element_2):
           remove_set.add(element_2)
           score = score + 10 
           group_one.difference_update(remove_set)
        
    
# helper function for drawing and updating rocks and missiles 
def process_sprite_group(a_set, canvas):
    # verify update() method in "Sprite" class. If the missile is "too old" - it's age
    # exceeds its lifespan - then remove it from set of missiles
    # also draw and update missiles and rocks
    remove_set = set([])
    for element in a_set:
        element.draw(canvas)
        if element.update():
            remove_set.add(element)
            a_set.difference_update(remove_set)
            
            
# helper function for clearing sets with rocks and asteriods   
def clear_set(group, remove_group):
    for i in group:
        remove_group.add(i)
    group.difference_update(remove_group)

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    #pos, vel, ang, ang_vel, image, info, sound = None
    # rocks centers appear only in screen range
    pos = [random.randrange(1, 800 - asteroid_info.get_radius()), random.randrange(1, 600 - asteroid_info.get_radius())]
    vel = (0, 0)
    ang_vel = 0
    
    lower_vel = 1
    upper_vel = 2
    range_width = upper_vel - lower_vel
    rock_vel = random.random() * range_width + lower_vel
    rand_vel_constant = random.randrange(0, 4)
    
    lower_ang = 0.08
    upper_ang = 0.25
    rand_ang_constant = random.randrange(0, 2)
    ang_vel = 0
    
    if rand_vel_constant == 0:
        vel = (rock_vel, rock_vel)
    elif rand_vel_constant == 1:
        vel = (-rock_vel, rock_vel) 
    elif rand_vel_constant == 2:
        vel = (rock_vel, -rock_vel)
    elif rand_vel_constant == 3:
        vel = (-rock_vel, -rock_vel)    
    
    if rand_ang_constant == 0:
        ang_vel = 0.08 * (float(random.randint(5, 16))) / 5
    elif rand_ang_constant == 1:
        ang_vel = -0.08 * (float(random.randint(5, 16))) / 5    
        
    #add new rock to the set rock_group if position of new rock is too close to the ship - shift it!
    if len(rock_group) < 3:
        coord = my_ship.get_position()
        if ( (pos[0] < coord[0] - 2 * my_ship.get_radius() or pos[0] > coord[0] + 2 * my_ship.get_radius()) and (pos[1] < coord[1] - 2 * my_ship.get_radius() or pos[0] > coord[1] + 2 * my_ship.get_radius()) ):
            rock_group.add(Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info))
        else:
            pos[0] = pos[0] + 5 * my_ship.get_radius()
            pos[1] = pos[1] + 5 * my_ship.get_radius()
            rock_group.add(Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info))
    #rock_group.add(Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info))
    
       
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()



