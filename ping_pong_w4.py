# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle1_vel = 0
paddle2_vel = 0

ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [0,0]

paddle1_center = HEIGHT/2
paddle2_center = HEIGHT/2

score1 = 0
score2 = 0

y_padd1_top = HEIGHT/2 - HALF_PAD_HEIGHT
y_padd1_bottom = HEIGHT/2 + HALF_PAD_HEIGHT
y_padd2_top = HEIGHT/2 - HALF_PAD_HEIGHT
y_padd2_bottom = HEIGHT/2 + HALF_PAD_HEIGHT

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, paddle1_vel, paddle2_vel # these are vectors stored as lists
    paddle1_vel = 0
    paddle2_vel = 0
    if direction == "RIGHT":
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        ball_vel = [int((random.randrange(120, 240))/60), int((random.randrange(-180, -60))/60)]
    if direction == "LEFT":
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        ball_vel = [int((random.randrange(-240, -120))/60), int((random.randrange(-180, -60))/60)]
    
def reset():
    global paddle1_center, paddle2_center, score1, score2
    paddle1_center = HEIGHT/2
    paddle2_center = HEIGHT/2
    
    score1 = 0
    score2 = 0
    
    new_game()
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2, ball_pos, ball_vel  # these are ints
    
    spawn_ball("RIGHT")
    
  

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_center, paddle2_center, paddle1_vel, paddle2_vel
    global score1, score2
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    


    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
        
    canvas.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, 5, "White", "White" )
    # update paddle's vertical position, keep paddle on the screen
    if ((paddle1_vel < 0) and (paddle1_center > 40)) :
        paddle1_center = paddle1_center + paddle1_vel
        #print paddle1_vel
    elif ((paddle1_vel > 0) and (paddle1_center < 360)):
        paddle1_center = paddle1_center + paddle1_vel
        #print paddle1_vel
        
    if ((paddle2_vel < 0) and (paddle2_center > 40)) :
        paddle2_center = paddle2_center + paddle2_vel
        #print paddle1_vel
    elif ((paddle2_vel > 0) and (paddle2_center < 360)):
        paddle2_center = paddle2_center + paddle2_vel
        #print paddle2_vel    
    
        
    # reflection from paddle 
    #paddle 1
    # I add "abs(ball_vel[0])" for correct place of reflection of the ball from paddle, without
    # this ball reflect from the deeper point - deeper than "tennis racket", but it cause problems 
    # at a high speed 
    if (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS + abs(ball_vel[0])) and (paddle1_center - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_center + HALF_PAD_HEIGHT):
        ball_vel[0] = - (ball_vel[0] + 0.1 * ball_vel[0])
        ball_vel[1] = (ball_vel[1] + 0.1 * ball_vel[1])
    elif (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS + abs(ball_vel[0])) and ((ball_pos[1] > paddle1_center + HALF_PAD_HEIGHT) or (ball_pos[1] < paddle1_center - HALF_PAD_HEIGHT)):
        score2 = score2 + 1
        spawn_ball("RIGHT") 
        
    #paddle 2    
    if (ball_pos[0] >= WIDTH -PAD_WIDTH - BALL_RADIUS -  abs(ball_vel[0])) and (paddle2_center - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_center + HALF_PAD_HEIGHT):
        ball_vel[0] = - (ball_vel[0] + 0.1 * ball_vel[0])
        ball_vel[1] = (ball_vel[1] + 0.1 * ball_vel[1])
    elif (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS - abs(ball_vel[0])) and ((ball_pos[1] > paddle2_center + HALF_PAD_HEIGHT) or (ball_pos[1] < paddle2_center - HALF_PAD_HEIGHT)):
        score1 = score1 + 1
        spawn_ball("LEFT")  
        
    # draw paddles
    canvas.draw_polygon([[0, paddle1_center - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_center - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_center + HALF_PAD_HEIGHT], [0, paddle1_center + HALF_PAD_HEIGHT]], 1, 'Red', 'Red')
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_center - HALF_PAD_HEIGHT], [WIDTH, paddle2_center - HALF_PAD_HEIGHT], [WIDTH, paddle2_center + HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_center + HALF_PAD_HEIGHT]], 1, 'Red', 'Red')    

    canvas.draw_text(str(score1), (140, 150), 50, "Red")
    canvas.draw_text(str(score2), (450, 150), 50, "Red")



def keydown1(key):
    global paddle1_vel, paddle2_vel
    acc = 10
    
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = -acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = acc
    
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = -acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = acc    
     
        
        
def keyup1(key):
    global paddle1_vel, paddle2_vel
    acc = 0
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = acc
        
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = acc    



# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background('Blue')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown1)
frame.set_keyup_handler(keyup1)
frame.add_button('RESET', reset, 80)


# start frame
new_game()
frame.start()        

