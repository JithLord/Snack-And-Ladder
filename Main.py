import pygame, sys, random, time
from pygame.locals import *

# BLOCK_SIZE is the size of each cell in the grid. Used for position calculations.
BLOCK_SIZE = 600//10

# RGB Colors for players - Black, Red, Green, Blue
COLORS = ((0, 0, 0), (255, 0, 0), (0, 100, 0), (0, 0, 255))

# Snakes' and ladders' positions where key is from and value is to.
SNAKES = {93:28, 84:41, 59:38, 55:12, 23:3}
LADDERS = {4:36, 10:49, 26:85, 40:79, 70:92}

# Sample players
players = [ {"name": "Player 1", "pos": 1, "color": COLORS[0], "bot": True},
            {"name": "Player 2", "pos": 1, "color": COLORS[1], "bot": True},
            {"name": "Player 3", "pos": 1, "color": COLORS[2], "bot": False},
            {"name": "Player 4", "pos": 1, "color": COLORS[3], "bot": False} ]

# game_message holds value of game status to display
game_message = ""

# If game is won or not
game_won = False

# Current player number (index of player in players)
player_index = 0

# Used to get input (space) when required
user_input = None
wait_for_user_input = False

def convert_num_to_xy(num, offset=(0,0)):
    '''This function converts a given cell number into its (x,y) coordinates. '''
    if num%10 == 0:
        y = 10 - num//10
    else:
        y = 10 - num//10 - 1
    
    if y % 2 == 0:
        if num%10 == 0:
            x = 10 - num%10 - 10
        else:
            x = 10 - num%10
    else:
        if num%10 == 0:
            x = num%10 - 1 + 10
        else:
            x = num%10 - 1
    # print(num, (x,y))
    return (x*BLOCK_SIZE+offset[0], y*BLOCK_SIZE+offset[1])

def draw_players_on_map():
    '''This function runs every frame and redraws the board and all players on it.'''
    
    screen.fill((65,186,235)) # Blue
    
    # Draw board background
    board_img = pygame.image.load("board3.jpg")
    board_img = pygame.transform.scale(board_img, (600, 600))
    screen.blit(board_img, (0,0))
    
    # Draw logo
    logo_img = pygame.image.load("logo2.png")
    logo_img = pygame.transform.scale(logo_img, (240, 120))
    screen.blit(logo_img, (600,6))
    
    # Draw players' circle dots
    for player in players:
        index = players.index(player)
        if index == 0:
            offset = (BLOCK_SIZE//4, BLOCK_SIZE//4)
        elif index == 1:
            offset = (BLOCK_SIZE*3//4, BLOCK_SIZE//4)
        elif index == 2:
            offset = (BLOCK_SIZE//4, BLOCK_SIZE*3//4)
        elif index == 3:
            offset = (BLOCK_SIZE*3//4, BLOCK_SIZE*3//4)
        pygame.draw.circle(screen, player["color"], convert_num_to_xy(player["pos"], offset), BLOCK_SIZE//4, 0)

def draw_scoreboard():
    '''This function redraws the right sidebar of the game, including scoreboard and text.'''
    
    global game_won
    pygame.draw.rect(screen, (65,186,235), (600,150,300,260))   # Draw a blue rectangle to "clear" the right side.
    headingtext = heading_head.render("Players", 1, (0,0,0))    # Draw the word "Players"
    screen.blit(headingtext, (675, 125))
    
    for player in players:                                      # For each player:
        if player["pos"] == 100:
            game_won = True
        index = players.index(player)
        score = player["name"] + ": " + str(player["pos"])
        scoretext = score_font.render(score, 1, (0,0,0))        # Draw player name and score
        screen.blit(scoretext, (650, 200+50*index))
        pygame.draw.circle(screen, player["color"], (638, 210+50*index), 6, 0)                  # Draw the small color circle dot

    a=players[player_index]["name"]+"'s turn"    
    playerturntext = heading_font.render(a.center(30," "), 1, (0,0,0))   # Draw player name of who should play
    screen.blit(playerturntext, (620, 500))

    b=game_message
    gamemsgtext = score_font.render(b.center(40," "), 1, (0,0,0)) # Draw game message
    screen.blit(gamemsgtext, (620, 540))

def draw_die():
    '''Draw die.'''
    
    die_img = pygame.image.load("die/die_"+str(dice_num)+".jpg")
    die_img = pygame.transform.scale(die_img, (75, 75))
    screen.blit(die_img, (712,410))

def play_turn(player_index):
    '''This function actually "plays" and rolls the die.'''
    global user_input, wait_for_user_input, game_message, dice_num
    
    if players[player_index]["bot"]:                                # If player is a computer:
        print("play_turn", player_index, "is bot. Playing.")
        dice_num = random.randint(1,6)                              # Generate random number
        game_message = players[player_index]["name"] + " (bot) got " + str(dice_num)
    else:                                                           # If player is human:
        print("play_turn", player_index, "is user.")
        if user_input:                                              # Check if player has pressed space
            print("found user input. Setting", user_input, "for", player_index)
            dice_num = random.randint(1,6)                          # Roll a die
            user_input = None                                       # Reset player input
            game_message = players[player_index]["name"] + " played " + str(dice_num)
        else:                                                       # If no input from player:
            print("no user input. Setting wait for", player_index)
            wait_for_user_input = True                              # Keep waiting, stop function midway here
            return

    draw_die()
    
    # Check if player crosses 100
    if players[player_index]["pos"]+dice_num > 100:
        game_message = "Can only proceed with " + str(100-players[player_index]["pos"]) + ", not " + str(dice_num)
        return        # Do not increment player's position
    
    # Check if player won the game
    elif players[player_index]["pos"]+dice_num == 100:
        game_message = players[player_index]["name"] + " WON!"
    
    players[player_index]["pos"] += dice_num                        # Add die number to player's position
    
    print("new pos for", player_index, "is", players[player_index]["pos"])

def check_and_teleport(player_index):
    '''Check if a player landed at a snake's head or ladder foot. Teleport when necessary.'''
    global game_message
    
    # Check for snakes
    if players[player_index]["pos"] in SNAKES:
        print(players[player_index]["name"], "was swallowed by a snake :(")
        game_message = players[player_index]["name"] + " was swallowed by a snake :("
        players[player_index]["pos"] = SNAKES[players[player_index]["pos"]]
    
    # Check for ladders
    elif players[player_index]["pos"] in LADDERS:
        print(players[player_index]["name"], "climbed a ladder :)")
        game_message = players[player_index]["name"] + " climbed a ladder :)"
        players[player_index]["pos"] = LADDERS[players[player_index]["pos"]]

#Ask for player details
##players = []
##try:
##    n = int(input("Number of players: "))
##except ValueError:
##    print("Invalid input. Exiting.")
##    exit()
##if n not in range(2,5):
##    print("Number of players must be 2-4.")
##    exit()
##
##for i in range(n):
##    name = input("Name: ")
##    b = input("Computer Bot? (yes/no): ").lower()
##    if  b in ("yes", "y", "true","t"):
##        bot=True 
##    elif b in ("no", "n", "false","f"):
##        bot=False 
##    else:
##        print("Invalid input, Try again.")
##    players.append({"name": name, "bot": bot, "pos": 1, "color": COLORS[i] })

# Initialize pygame
pygame.init()

# Create fonts to use
heading_head = pygame.font.SysFont("bauhaus93",34)
heading_font = pygame.font.SysFont("comicsansms", 22)
score_font = pygame.font.SysFont("comicsansms", 18)

# Create a new screen of size: 900x600
screen = pygame.display.set_mode([900,600])
pygame.display.set_caption("Snake And Ladder")

# Start a "clock" for the game
fpsClock = pygame.time.Clock()

# Main game loop
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:           # If window close, exit properly
            pygame.quit()
            sys.exit()
        if i.type == pygame.KEYDOWN:        # If user input:
            key = pygame.key.name(i.key)
            print(key)
            if key == 'space':              # If key is space:
                user_input = True
                wait_for_user_input = False
                player_index -= 1
    
    draw_players_on_map()       # Draw players on map
    draw_scoreboard()           # Draw scoreboard
    
    # Do not go ahead with game if game expects input, but none is given
    if wait_for_user_input and not user_input:
        continue
    
    play_turn(player_index)     # Play turn
    draw_scoreboard()           # Draw scoreboard
    draw_die()
    pygame.display.update()     # Apply all changes made to screen
    
    # Stop if game won
    if game_won:
        time.sleep(6)
        pygame.quit()
        sys.exit()
    
    time.sleep(0.7)             # Wait so people can see what's happening
    check_and_teleport(player_index)    # Check for snakes and ladders
    
    # Go to next player. Cycle over all players.
    game_message = ""           # Reset game message
    if player_index == len(players)-1:
        player_index = 0
    else:
        player_index += 1
    
    pygame.display.update()     # Apply all changes made to screen
fpsClock.tick(1)
