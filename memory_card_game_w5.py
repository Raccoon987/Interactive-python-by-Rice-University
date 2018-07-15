# implementation of card game - Memory

import simplegui
import random

memory = []
exposed = []
state = 0
#variables for comparison if two opened cards are equal or not
first_card_number = 0
second_card_number = 0
#variables for counting number of turns
turn_counter = 0

# helper function to initialize globals
def new_game():
    global state, memory, exposed, first_card_number, second_card_number, turn_counter 
    state = 0  
    memory = range(0, 8)
    memory_2 = range(0, 8)
    memory.extend(memory_2)
    random.shuffle(memory)
    #print memory
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    first_card_number = 0
    second_card_number = 0
    turn_counter = 0
    label.set_text("Turns =  " + str(turn_counter))
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, first_card_number, second_card_number, turn_counter 
    counter = range(0, 16)
    #state == 0 means no card open
    if state == 0:
        for count in counter:
            if (0 <= pos[1] <= 100) and (50 * count <= pos[0] < 50 + 50 * count):
                #condition for ignoring click at the already opened cards
                if exposed[count] == False:
                    exposed[count] = True
                    first_card_number = count
                    state = 1
    
    #state == 1 means one card open
    elif state == 1: 
        
        for count in counter:
            if (0 <= pos[1] <= 100) and (50 * count <= pos[0] < 50 + 50 * count):
                if exposed[count] == False:
                    exposed[count] = True
                    second_card_number = count
                    state = 2 
                    turn_counter = turn_counter + 1
                    label.set_text("Turns =  " + str(turn_counter))
    
    #two cards opened
    else:
         
        if memory[first_card_number] == memory[second_card_number]:
            
            for count in counter:
                if (0 <= pos[1] <= 100) and (50 * count <= pos[0] < 50 + 50 * count):
                    if exposed[count] == False:
                        second_card_number = 0
                        first_card_number = 0
                        exposed[count] = True
                        first_card_number = count
                        state = 1        
        elif  memory[first_card_number] != memory[second_card_number]:  
            
            for count in counter:
                if (0 <= pos[1] <= 100) and (50 * count <= pos[0] < 50 + 50 * count):
                    if exposed[count] == False:
                        exposed[first_card_number] = False
                        exposed[second_card_number] = False
                        second_card_number = 0
                        first_card_number = 0
                        exposed[count] = True
                        first_card_number = count
                        state = 1    
    
                
                
# cards are logically 50x100 pixels in size    
def draw(canvas):
    counter = range(0, 16)
    for count in counter:
        if exposed[count] == True:
            canvas.draw_text(str(memory[count]), (25 + 50 * count, 50), 32, 'Red')
        elif exposed[count] == False:
            canvas.draw_polygon([(50 * count, 0), (50 + 50 * count, 0), (50 + 50 * count, 100), (50 * count, 100)], 2, 'Orange', 'Green')
                


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns =  " + str(turn_counter))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
frame.set_canvas_background("White")
# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric

