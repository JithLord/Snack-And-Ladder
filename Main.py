import pygame, sys, random, time
from pygame.locals import *

BLOCK_SIZE = 600//10
WHITE = (255, 255, 255)
COLORS = ((0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255))
SNACKS = {93:28, 84:41, 59:38, 55:12, 23:3}
LADDERS = {4:36, 10:49, 26:85, 40:79, 70:92}

players = [ {"name": "Player 1", "pos": 1, "color": COLORS[0], "bot": True},
            {"name": "Player 2", "pos": 1, "color": COLORS[1], "bot": True},
            {"name": "Player 3", "pos": 1, "color": COLORS[2], "bot": False},
            {"name": "Player 4", "pos": 1, "color": COLORS[3], "bot": False} ]
game_message = ""
player_index = 0
user_input = None
wait_for_user_input = False

def convert_num_to_xy(num, offset=(0,0)):
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
    screen.fill((65,186,235)) # Blue
    
    board_img = pygame.image.load("board3.jpg")
    board_img = pygame.transform.scale(board_img, (600, 600))
    screen.blit(board_img, (0,0))
    
    logo_img = pygame.image.load("logo1.png")
    logo_img = pygame.transform.scale(logo_img, (288, 144))
    screen.blit(logo_img, (620,10))
    
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
    headingtext = heading_head.render("Players", 1, (0,0,0))
    screen.blit(headingtext, (675, 175))
    
    for player in players:
        index = players.index(player)
        score = player["name"] + ": " + str(player["pos"])
        scoretext = score_font.render(score, 1, (0,0,0))
        screen.blit(scoretext, (650, 250+50*index))
        pygame.draw.circle(screen, player["color"], (638, 260+50*index), 6, 0)
    playerturntext = heading_font.render(players[player_index]["name"]+"'s turn", 1, (0,0,0))
    screen.blit(playerturntext, (620, 500))
    
    gamemsgtext = heading_font.render(game_message, 1, (0,0,0))
    screen.blit(gamemsgtext, (620, 540))

def play_turn(player_index):
    global user_input, wait_for_user_input, game_message
    if players[player_index]["bot"]:
        print("play_turn", player_index, "is bot. Playing.")
        dice_num = random.randint(1,6)
        game_message = players[player_index]["name"] + "(bot) got " + str(dice_num)
    else:
        print("play_turn", player_index, "is user.")
        dice_num = 0
        if user_input:
            print("found user input. Setting", user_input, "for", player_index)
            if not 1 <= int(user_input) <= 6:
                print("Invalid Number. Waiting for input again.")
                user_input = None
                wait_for_user_input = True
                return
            dice_num = int(user_input)
            user_input = None
            game_message = players[player_index]["name"] + " played " + str(dice_num)
        else:
            print("no user input. Setting wait for", player_index)
            wait_for_user_input = True
            return
    players[player_index]["pos"] += dice_num
    print("new pos for", player_index, "is", players[player_index]["pos"])

def check_and_teleport(player_index):
    global game_message
    if players[player_index]["pos"] in SNACKS:
        print(players[player_index]["name"], "was swallowed by a snake :(")
        game_message = players[player_index]["name"] + " was swallowed by a snake :("
        players[player_index]["pos"] = SNACKS[players[player_index]["pos"]]
    
    elif players[player_index]["pos"] in LADDERS:
        print(players[player_index]["name"], "climbed a ladder :)")
        game_message = players[player_index]["name"] + " climbed a ladder :)"
        players[player_index]["pos"] = LADDERS[players[player_index]["pos"]]

#players=[]
#n = int(input("Number of players: "))
#for i in range(n):
    players.append({"name": input("Name: "), "bot": bool(input("Computer Bot?: ")), "pos": 0, "color": COLORS[i]})

pygame.init()
heading_head = pygame.font.SysFont("bauhaus93",34)
heading_font = pygame.font.SysFont("comicsansms", 22)
score_font = pygame.font.SysFont("comicsansms", 18)
screen = pygame.display.set_mode([900,600])
pygame.display.set_caption("Snack And Ladder")
fpsClock = pygame.time.Clock()

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if i.type == pygame.KEYDOWN:
            key = pygame.key.name(i.key)
            print(key)
            if key.isdigit() or key[1:-1].isdigit():
                user_input = key if key.isdigit() else key[1:-1]
                wait_for_user_input = False
                player_index -= 1
    
    draw_players_on_map()
    draw_scoreboard()
    
    if wait_for_user_input and not user_input:
        continue
    
    play_turn(player_index)
    draw_scoreboard()
    pygame.display.update()
    check_and_teleport(player_index)
    
    if player_index == len(players)-1:
        player_index = 0
    else:
        player_index += 1
    
    pygame.display.update()
    fpsClock.tick(30)
