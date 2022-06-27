
from operator import truediv
from typing import List
from xmlrpc.client import Boolean, boolean
import pygame
from pygame import KEYDOWN, MOUSEBUTTONUP, QUIT, mixer
pygame.init()

# Size of canvas
WIDTH = 1400
HEIGHT = 800

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)
dark_grey = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

# Creating screen and setting font and caption
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 24)

# defining varibles for fps, timer, beats, instruments
fps: int = 60
timer = pygame.time.Clock()
beats: int = 8
instruments: int = 6

# 
boxes: List = []

# Defining the grid
clicked: List[List[int]] = [[-1 for i in range(beats)] for i in range(instruments)]
active_list = [1 for _ in range(instruments)] # all channels will be initially true
bpm: int = 240 # beats per min
playing: Boolean = True # to control play pause
active_length: int = 0
active_beat: int = 1
beat_changed: Boolean = True
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)
beat_name = ''
typing = False    


# load in sounds from various locations
hi_hat = mixer.Sound("C:\\Users\\91896\\Desktop\\sounds\\bass.wav")
snare = mixer.Sound("C:\\Users\\91896\\Desktop\\sounds\\snare.WAV")
kick = mixer.Sound("C:\\Users\\91896\\Desktop\\sounds\\kick.WAV")
crash = mixer.Sound("C:\\Users\\91896\\Desktop\\sounds\\cymbal.wav")
clap = mixer.Sound("C:\\Users\\91896\\Desktop\\sounds\\clap.wav")
tom = mixer.Sound("C:\\Users\\91896\\Desktop\\sounds\\tom.WAV")
pygame.mixer.set_num_channels(instruments * 3)


def play_notes():
    for i in range(len(clicked)):
        # Checking if that particular box in the grid is set as one or not i.e, green.
        # What is active beat ? The beat which is beating right now. The blue box.
        if clicked[i][active_beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()



def draw_grid(clicks, beat: int, actives):
    # Creating left and bottom box
    # Left box for containing the instruments labels and bottom box for play/pause and save button.
    left_box = pygame.draw.rect(screen, grey, [0, 0, 210, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, grey, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colours = [grey, white, grey]

    # Creating labels for instruments and rendering it on screen
    hi_hat_text = label_font.render('Hi Hat', True, colours[actives[0]])
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render('Snare', True, colours[actives[1]])
    screen.blit(snare_text, (30, 130))
    Bass_Drum_text = label_font.render('Bass Drum', True, colours[actives[2]])
    screen.blit(Bass_Drum_text, (30, 230))
    Crush_text = label_font.render('Crush', True, colours[actives[3]])
    screen.blit(Crush_text, (30, 330))
    clap_text = label_font.render('Clap', True, colours[actives[4]])
    screen.blit(clap_text, (30, 430))
    floor_tom_text = label_font.render('Floor Tom', True, colours[actives[5]])
    screen.blit(floor_tom_text, (30, 530))

    # Drawing lines between instrument labels
    for i in range(instruments):
        pygame.draw.line(screen, grey, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)


    for i in range(beats):
        for j in range(instruments):
            # For every box in the grid, if it is -1 keep it as grey and if it is 1 then change to green.
            if clicks[j][i] == -1:
                colour = grey
            else:
                if actives[j] == 1:    
                    colour = green
                else:
                    colour = dark_grey

                        
            rect = pygame.draw.rect(screen, colour, 
                                [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10,
                                ((HEIGHT - 200)//instruments) - 10], 0, 3)
            pygame.draw.rect(screen, gold, 
                                [i * ((WIDTH - 200) // beats) + 200, (j * 100),((WIDTH - 200) // beats),
                                ((HEIGHT - 200)//instruments)], 5, 5)
            pygame.draw.rect(screen, black, 
                                [i * ((WIDTH - 200) // beats) + 200, (j * 100),((WIDTH - 200) // beats),
                                ((HEIGHT - 200)//instruments)], 2, 5)
            boxes.append((rect, (i, j)))

    active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100], 5, 3) 
    return boxes

def draw_save_menu(beat_name, typing): 
    pygame.draw.rect(screen, black, [0, 0, WIDTH , HEIGHT])
    menu_text = label_font.render('SAVE MENU: Enter a name for current beat', True, white)
    saving_button = pygame.draw.rect(screen, grey, [WIDTH // 2 - 200, HEIGHT * 0.75, 400,100], 0, 5)
    saving_text = label_font.render('Save Beat', True, white)
    screen.blit(saving_text, (WIDTH // 2 - 70, HEIGHT * 0.75 + 30))
    screen.blit(menu_text, (400, 40))
    exit_button = pygame.draw.rect(screen, grey, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close' , True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    if typing:
         pygame.draw.rect(screen, dark_grey, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, grey, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit_button, saving_button, entry_rect

def draw_load_menu(index): 
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, black,[0, 0, WIDTH , HEIGHT])
    menu_text = label_font.render('LOAD MENU: Select a beat to load', True, white)
    loading_button = pygame.draw.rect(screen, grey, [WIDTH // 2 - 200, HEIGHT * 0.87, 400, 100], 0, 5)
    loading_text = label_font.render('Load Beat', True, white)
    screen.blit(loading_text, (WIDTH // 2 - 70, HEIGHT * 0.87 + 30))
    delete_button = pygame.draw.rect(screen, grey, [(WIDTH // 2) - 500, HEIGHT * 0.87, 200, 100], 0, 5)
    delete_text = label_font.render('Delete beat', True, white)
    screen.blit(delete_text, ((WIDTH // 2) - 480, HEIGHT * 0.87 + 30))
    screen.blit(menu_text, (400, 40))
    exit_button = pygame.draw.rect(screen, grey, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close' , True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    loaded_rectangle = pygame.draw.rect(screen, grey,[190, 90, 1000, 600], 5, 5)
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, white)
            screen.blit(row_text,(200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(saved_beats[beats][name_index_start:name_index_end], True, white)
            screen.blit(name_text, (240, 100 * beat * 50))
        if 0 <= index < len(saved_beats):
            beat_index_end = saved_beats[beat].index(', bpm:')    
            loading_beats = int(saved_beats[beat][name_index_end + 8: beat_index_end])
            beat_index_end = saved_beats[beat].index(', selected:')
            loading_bpm = int(saved_beats[beat][name_index_end + 6: bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split('], ['))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item]) 
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]                    
    return exit_button, loading_button, delete_button, loaded_rectangle, loaded_info



run = True
while run:
    timer.tick(fps) #as long as run is true the code will run 60 times per second#
    screen.fill(black)    
    boxes = draw_grid(clicked, active_beat, active_list)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, grey, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT -130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_grey)
    else:
        play_text2 = medium_font.render('Paused', True, dark_grey)
    screen.blit(play_text2, (70, HEIGHT -100))

   # bpm stuff
    bpm_rect = pygame.draw.rect(screen, grey, [300, HEIGHT - 150, 230, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (308, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT -100))
    bpm_add_rect = pygame.draw.rect(screen, grey, [510, HEIGHT - 150, 50, 52], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, grey, [510, HEIGHT - 100, 50, 50], 0, 5)
    add_text = medium_font.render('+5', True, white)
    sub_text = medium_font.render('-5', True, white)
    screen.blit(add_text, (520, HEIGHT - 140))
    screen.blit(sub_text, (520, HEIGHT - 90))

    # beats stuff
    beats_rect = pygame.draw.rect(screen, grey, [600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render('Beats in loop', True, white)
    screen.blit(beats_text, (618, HEIGHT - 130))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (680, HEIGHT -100))
    beats_add_rect = pygame.draw.rect(screen, grey, [810, HEIGHT - 150, 50, 52], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, grey, [810, HEIGHT - 100, 50, 50], 0, 5)
    add_text2 = medium_font.render('+1', True, white)
    sub_text2 = medium_font.render('-1', True, white)
    screen.blit(add_text2, (820, HEIGHT - 140))
    screen.blit(sub_text2, (820, HEIGHT - 90))

    # instruments rect( turn an instrument on or off)
    instruments_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instruments_rects.append(rect)

    # save and load button
    save_button = pygame.draw.rect(screen, grey, [900, HEIGHT - 150, 200, 48], 0, 5)
    save_text = label_font.render('Save Beat', True, white)
    screen.blit(save_text, (920, HEIGHT - 140))
    load_button = pygame.draw.rect(screen, grey, [900, HEIGHT - 100, 200, 48], 0, 5)
    load_text = label_font.render('Load Beat', True, white)
    screen.blit(load_text, (920, HEIGHT - 90))

    # clear button
    clear_button = pygame.draw.rect(screen, grey,[1150, HEIGHT - 150, 200, 100], 0, 5)
    clear_text = label_font.render('Clear Board', True, white)
    screen.blit(clear_text, (1160, HEIGHT - 120))

    if save_menu:
        exit_button, saving_button, entry_rectangle = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button, loading_button, delete_button, loaded_rectangle = draw_load_menu() 


    if beat_changed:
        play_notes()
        beat_changed: Boolean = False #runs one time the beat changes

    # put all the code in this for loop, checking all the movements,any other event the computer processes will be in this for loop
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)): # checks if we clicked
                print(boxes[i][0])
                if boxes[i][0].collidepoint(event.pos): # on any of the rectangles
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True   
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5                         
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]  
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True              
            for i in range(len(instruments_rects)):
                if instruments_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True    
                beat_name = ''
                typing = False
            elif entry_rectangle.collidepoint(event.pos): # entry rectangle means whether or not we are typing or not
                if typing:
                        typing = False
                elif not typing:
                        typing = True
            elif saving_button.collidepoint(event.pos):
                file = open('saved_beats.txt', 'w')
                saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}') # saving everything to recall later
                for i in range(len(saved_beats)):
                    file.write(str(saved_beats[i]))
                file.close()
                save_menu = False
                typing = False
                beat_name = ''    
        if event.type == pygame.TEXTINPUT and typing:
             beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                 beat_name = beat_name[:-1]   # colon means start from the very beginning, and -1 is go to character which is right before the end of the character


    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
           active_length += 1    
        else:
            active_length = 0
            if active_beat < beats -1:
               active_beat += 1
               beat_changed = True      
            else:
                active_beat = 0
                beat_changed = True                  


    pygame.display.flip() #flip the image in vertical direction or horizontal direction according to our needs
pygame.quit() #quit() is a function that closes pygame (python still running) While pygame. QUIT just checks if pygame is running or not
