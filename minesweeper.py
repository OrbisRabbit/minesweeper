#Requirements:
# *1. incorporate sprites *
# *2. Make a map *
#     *2a. place bombs *
#     *2b. Recursive function to check for adjacent bombs 
# 3. Click functions
#     *3a. first click is always not a bomb
#     *3b. pulling away cancels click
#     3c. Recursive function to reveal squares
#     3d. right click to flag
# 4. Win/Loss Condition

#libraries
import pygame
import numpy as np
import spritesheet as sp
import time

#pygame initialization and settings
pygame.init()
screen_width = 16*25
screen_height = 16*20
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minesweeper')
clock = pygame.time.Clock()
running = True
background = (50,50,50)
black = (0,0,0)
mouse_click_count = 0
left = 1
right = 3
no_of_bombs = 0

# loading in sprite sheets
sprite_sheet_FILE = pygame.image.load('minesweeper.png').convert_alpha()
minesw_sprites = sp.SpriteSheet(sprite_sheet_FILE)

# important board variables
board_width = int(screen_width/16)
board_height =  int(screen_height/16) -5
game_size = (board_width,board_height)

#initialization of maps
game_field = np.ones(game_size) * 14
bomb_field = np.ones(game_size)*12
revealed_field = np.zeros(game_size)

#sprites
frame_0 = minesw_sprites.sprite(0) # bomb (0, 1, 4)
frame_1 = minesw_sprites.sprite(1)
frame_2 = minesw_sprites.sprite(2) #flag
frame_3 = minesw_sprites.sprite(3)
frame_4 = minesw_sprites.sprite(4)# numbers (1-8)
frame_5 = minesw_sprites.sprite(5)
frame_6 = minesw_sprites.sprite(6)
frame_7 = minesw_sprites.sprite(7)
frame_8 = minesw_sprites.sprite(8)
frame_9 = minesw_sprites.sprite(9)
frame_10 = minesw_sprites.sprite(10)
frame_11 = minesw_sprites.sprite(11) 
frame_12 = minesw_sprites.sprite(12) #empty
frame_13 = minesw_sprites.sprite(13) #empty
frame_14 = minesw_sprites.sprite(14) #starting tile
frame_15 = minesw_sprites.sprite(15) #selected tile

#functions

    #draw the map
def draw_map(arr1):
    x = len(arr1)
    y = len(arr1[0])
    for i in range(x):
        for j in range(y):
            sprite = arr1[i, j]
            match sprite:
                case 0:
                    screen.blit(frame_0, (i*16 , (j*16)+16*5))
                case 1:
                    screen.blit(frame_1, (i*16 , (j*16)+16*5))
                case 2:
                    screen.blit(frame_2, (i*16 , (j*16)+16*5))
                case 3:
                    screen.blit(frame_3, (i*16 , (j*16)+16*5))
                case 4:
                    screen.blit(frame_4, (i*16 , (j*16)+16*5))
                case 5:
                    screen.blit(frame_5, (i*16 , (j*16)+16*5))
                case 6:
                    screen.blit(frame_6, (i*16 , (j*16)+16*5))
                case 7:
                    screen.blit(frame_7, (i*16 , (j*16)+16*5))
                case 8:
                    screen.blit(frame_8, (i*16 , (j*16)+16*5))
                case 9:
                    screen.blit(frame_9, (i*16 , (j*16)+16*5))
                case 10:
                    screen.blit(frame_10, (i*16 , (j*16)+16*5))
                case 11:
                    screen.blit(frame_11, (i*16 , (j*16)+16*5))
                case 12:
                    screen.blit(frame_12, (i*16 , (j*16)+16*5))
                case 13:
                    screen.blit(frame_13, (i*16 , (j*16)+16*5))
                case 14:
                    screen.blit(frame_14, (i*16 , (j*16)+16*5))
                case 15:
                    screen.blit(frame_15, (i*16 , (j*16)+16*5))
                case _:
                    screen.blit(frame_15, (i*16 , (j*16)+16*5))
                    
            
    return

    #generate bombs

#generate a field of mines from empty fields
def generate_bombs( gamePos):
    global game_field
    global no_of_bombs
    no_of_bombs = int(len(game_field) * len(game_field[0]) * (40/(256)))
    #vector of unique element numbers of bomb positions
    bomb_vector = np.random.permutation(bomb_field.size)[:no_of_bombs]

    #set bombs into bomb_field
    for i in range(len(bomb_vector)):
        bomb_field[int(bomb_vector[i]/board_height), int(bomb_vector[i] % board_height)] = 0
    
    adjacent_bombs_number_generation()    
    first_click(gamePos)


    return

# assign numbers to each position
def adjacent_bombs_number_generation():
    for row in range(len(bomb_field)):
        for col in range(len(bomb_field[0])):
                        #check what is adjacent to all spaces
                        if (bomb_field[row, col] != 0):
                            for deltarow in [-1, 0, 1]:
                                for deltacol in [-1, 0, 1]:
                                    if (deltarow == 0 and deltacol == 0):
                                        continue
                                    else:
                                        if ((0 <= (row+deltarow)) and ((row+deltarow) < len(bomb_field)) and (0 <= (col+deltacol)) and ((col+deltacol) < len(bomb_field[0]))):
                                            if (bomb_field[row+deltarow, col+deltacol] == 0):
                                                bomb_field[row, col] = bomb_field[row, col] + 1  

                                    
    return

#if the first click isnt empty generate a map until it is
def first_click(gamePos):
    global bomb_field
    while(bomb_field[gamePos] != 12):
        bomb_field = np.ones(game_size)*12
        generate_bombs(gamePos)
    return

#when an empty tile is revealed reveal all surrounding tiles
def adjacent_EmptySpaceCheck(gamePos):
    global game_field
    (row, col) = gamePos
    deltas = [(-1, -1), (0,-1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1,1)]
    for position_shifts in deltas:
        (deltarow, deltacolumn) = position_shifts
        (surrounding_row, surrounding_column) = (row + deltarow, col + deltacolumn)
        surrounding_position = (surrounding_row, surrounding_column)
        if ((0 <= surrounding_row) and (surrounding_row < len(bomb_field)) and (0 <= surrounding_column) and (surrounding_column < len(bomb_field[0])) and revealed_field[surrounding_position] == 0):
            if any((bomb_field[surrounding_position]==[13, 14, 15, 16, 17, 18, 19, 20, 12])):
                revealed_field[surrounding_position] = 1
            if (bomb_field[surrounding_position] >=13 and bomb_field[surrounding_position] <= 20):
                game_field[surrounding_position] = bomb_field[surrounding_position] - 9
            elif (bomb_field[surrounding_position] == 12 and game_field[surrounding_position] == 12):
                continue
            elif (bomb_field[surrounding_position] == 12 and game_field[surrounding_position] != 12):
                game_field[surrounding_position] = 12
                adjacent_EmptySpaceCheck(surrounding_position)
            
    return

#function to check for wins or losses
def winlosscheck():
    uncovered = 0
    for row in range(len(revealed_field)):
        for col in range(len(revealed_field[0])):
            uncovered += revealed_field[row, col]
    print(uncovered)
    print(board_height*board_width - no_of_bombs)
    if (uncovered == ((board_height*board_width - no_of_bombs))):
        print("You Win")
    return

while running:
    
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            mousePosDown = (int(mouse_x/16), int(mouse_y/16-5))
            if game_field[mousePosDown] == 14:
                game_field[mousePosDown] = 15           
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == left:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            mousePosUp = (int(mouse_x/16), int(mouse_y/16-5))
            
            if (mousePosDown != mousePosUp and game_field[mousePosDown] == 15): 
                game_field[mousePosDown] = 14

            elif mousePosDown == mousePosUp:
                if mouse_click_count == 0:
                    generate_bombs(mousePosDown)
                    mouse_click_count = 1
                    adjacent_EmptySpaceCheck(mousePosDown)
                    winlosscheck()

                elif (game_field[mousePosDown] != 2):
                    revealed_field[mousePosDown] = 1
                    match (bomb_field[mousePosDown]):
                        case 0:
                            game_field[mousePosDown] = 0
                            draw_map(game_field)
                            pygame.display.update()
                            time.sleep(0.5)
                            game_field[mousePosDown] = 1
                            draw_map(game_field)
                            pygame.display.update()
                            time.sleep(0.5)
                            game_field[mousePosDown] = 3
                            print("You lose")
                        case 13:
                            game_field[mousePosDown] = 4
                        case 14:
                            game_field[mousePosDown] = 5
                        case 15:
                            game_field[mousePosDown] = 6
                        case 16:
                            game_field[mousePosDown] = 7
                        case 17:
                            game_field[mousePosDown] = 8
                        case 18:
                            game_field[mousePosDown] = 9
                        case 19:
                            game_field[mousePosDown] = 10
                        case 20:
                            game_field[mousePosDown] = 11
                        case 12:
                            adjacent_EmptySpaceCheck(mousePosDown)
                            game_field[mousePosDown] = 12
                    winlosscheck()
                
   
                            
        if event.type == pygame.MOUSEBUTTONUP and event.button == right:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            mousePosDown = (int(mouse_x/16), int(mouse_y/16-5))
            if game_field[mousePosDown] == 14:
                game_field[mousePosDown] = 2
            elif game_field[mousePosDown] == 2:
                game_field[mousePosDown] = 14         

    # render visuals
    screen.fill(background)
    
    screen.blit(frame_0, (0 , 0))
    screen.blit(frame_1, (16 , 0))
    screen.blit(frame_2, (16*2 , 0))
    screen.blit(frame_3, (16*3 , 0))
    screen.blit(frame_4, (0 , 16))
    screen.blit(frame_5, (16 , 16))
    screen.blit(frame_6, (16*2 , 16))
    screen.blit(frame_7, (16*3 , 16))
    screen.blit(frame_8, (0 , 32))
    screen.blit(frame_9, (16 , 32))
    screen.blit(frame_10, (16*2 , 32))
    screen.blit(frame_11, (16*3 , 32))
    screen.blit(frame_12, (0 , 48))
    screen.blit(frame_13, (16 , 48))
    screen.blit(frame_14, (16*2 , 48))
    screen.blit(frame_15, (16*3 , 48))
    
    draw_map(game_field)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
