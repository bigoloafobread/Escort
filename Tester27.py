import pygame, sys
from pygame.locals import QUIT

pygame.init()

class PLAYERS:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.oldX = 0
    self.oldY = 0
    self.velocity = 0.6
  def movement(self):
    self.oldX = self.x
    self.oldY = self.y

#Player Object
player = PLAYERS(0, 0)

#Powerups
powerup_x = -100 
powerup_y = -100 
invisible = False
invis_powerup = False
speed_boost = False
powerup_type = 0 #0 = Invisibility, 1 = Speed Boost
powerup_activated_0 = False
powerup_activated_1 = False

#Variables
speed = 1
blink = 0
tick = 1250
blinkTrue = False
CLOCK = pygame.time.Clock()
HP = 3
strikes = 3
HOR_CELLS = 30
VER_CELLS = 30
CELLSIZE = 20
SCREEN_WIDTH = CELLSIZE*HOR_CELLS
SCREEN_HEIGHT = CELLSIZE*VER_CELLS

BG = (0,0,0)
FPS = 240
UNICOLOR = (74,246,38)
ENEMYCOLOR = (255,60,60)
POWERUPCOLOR = (100, 230, 255)
HEALTHBOOSTCOLOR = (250, 235, 125)
SCENERYCOLOR = (255, 169, 56)
PLAYER = pygame.Rect(10*CELLSIZE,10*CELLSIZE, CELLSIZE, CELLSIZE)
PLAYER_RADIUS = min(PLAYER.width, PLAYER.height)
#Tile is a Room
tile = (2,2)
pygame.display.set_caption('Escort')
enemy_detection_delay = pygame.time.get_ticks() + 3000

L1FRAME = [pygame.Rect(7.5*CELLSIZE, 7.5*CELLSIZE, 15*CELLSIZE, 10), pygame.Rect(7.5*CELLSIZE, 22.5*CELLSIZE, 15.5*CELLSIZE,10), pygame.Rect(7.5*CELLSIZE, 7.5*CELLSIZE, 10,15*CELLSIZE), pygame.Rect(22.5*CELLSIZE, 7.5*CELLSIZE, 10,15*CELLSIZE)]

#Crate
crate_pos_x = 10*CELLSIZE
crate_pos_y = 20*CELLSIZE
crate_font = pygame.font.SysFont(None, 70)
crate_detail = crate_font.render("X", True, SCENERYCOLOR)
crate = pygame.Rect(crate_pos_x, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
crate_detail_pos = crate_detail.get_rect(center = crate.center)

#Powerup
powerup_font = pygame.font.SysFont(None, 30)
qmark = powerup_font.render("?", True, (255,255,255))
powerup = pygame.Rect(powerup_x, powerup_y, CELLSIZE, CELLSIZE)
qmark_pos = qmark.get_rect(center = powerup.center)

# Pause Screen Variables
unpause_button = pygame.Rect(9*CELLSIZE, 8*CELLSIZE, 12*CELLSIZE, 4*CELLSIZE)
quit_button = pygame.Rect(9*CELLSIZE, 15*CELLSIZE, 12*CELLSIZE, 4*CELLSIZE)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
paused = 0
pause_blur = pygame.Surface((CELLSIZE*HOR_CELLS,CELLSIZE*VER_CELLS), pygame.SRCALPHA)
paused_text_box = pygame.Rect(10*CELLSIZE, 3*CELLSIZE, 10*CELLSIZE, 3*CELLSIZE)
paused_text = crate_font.render("Paused", True, (UNICOLOR))
paused_text_pos = paused_text.get_rect(center = paused_text_box.center)
unpause_text = crate_font.render("Unpause", True, (UNICOLOR))
unpause_text_pos = unpause_text.get_rect(center = unpause_button.center)
quit_text = crate_font.render("Quit", True, (UNICOLOR))
quit_text_pos = quit_text.get_rect(center = quit_button.center)

key_status = False
victory = False
boat_x = 18*CELLSIZE
locked = 2
enemytimer = [0,0,0,0,0,0,0]
pos_cachex = [0,0,0,0,0,0,0]
pos_cachey = [0,0,0,0,0,0,0]
enemy_x, enemy_y = 10*CELLSIZE, 19.5*CELLSIZE
transitioning = 1
radarsize = 3*CELLSIZE

enemy_x2, enemy_y2 = 9*CELLSIZE, 9*CELLSIZE

# Endgame Screen Variables
endgame_block = pygame.Rect(8*CELLSIZE, 6*CELLSIZE, 4*CELLSIZE, 2*CELLSIZE)
endgame_text = crate_font.render("Escorted!", True, (UNICOLOR))
endgame_text_pos = endgame_text.get_rect(center = endgame_block.center)

reset_button = pygame.Rect(7*CELLSIZE, 9*CELLSIZE, 16*CELLSIZE, 4*CELLSIZE)
reset_text = crate_font.render("Play Again?", True, (UNICOLOR))
reset_text_pos = reset_text.get_rect(center = reset_button.center)

# Game Start Instructions
instructions = [pygame.Rect(CELLSIZE, 2*CELLSIZE, 3*CELLSIZE, CELLSIZE), pygame.Rect(CELLSIZE, 4*CELLSIZE, 3*CELLSIZE, CELLSIZE), pygame.Rect(CELLSIZE, 6*CELLSIZE, 3*CELLSIZE, CELLSIZE)]
instruction_text = [powerup_font.render("WASD to Move", True, (UNICOLOR)), powerup_font.render("ESC to Pause", True, (UNICOLOR)), powerup_font.render("Hide behind crates to not get caught", True, (UNICOLOR))]

# Objectives
objective_block = pygame.Rect(CELLSIZE, 28*CELLSIZE, 6*CELLSIZE, CELLSIZE)
objective = [powerup_font.render("Objective: Find key to escape facility", True, (UNICOLOR)), powerup_font.render("Objective: Leave facility", True, (UNICOLOR))]
objective_pos = objective[0].get_rect(topleft = objective_block.topleft)

# Directions
direction = (0,0)
direction_lock = (0,0)
x = -1

# Enemy Detection
warning = 0
warning_block = pygame.Rect(enemy_x, enemy_y-20, CELLSIZE, CELLSIZE)
warning_status = [crate_font.render("?", True, (255,255,0)), crate_font.render("!", True, (255,0,0))]
warning_pos = warning_status[0].get_rect(center = warning_block.center)
new_enemy_y = enemy_y
new_enemy_x = enemy_x
enemy_detection = pygame.Rect(new_enemy_x+CELLSIZE,new_enemy_y-0.5*CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
enemy_detection2 = pygame.Rect(new_enemy_x+CELLSIZE,new_enemy_y-0.5*CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
timer = 0

# Game Over Stuff
game_over = False
game_over_block = pygame.Rect(8*CELLSIZE, 6*CELLSIZE, 4*CELLSIZE, 2*CELLSIZE)
game_over_text = crate_font.render("Mission Failed", True, (UNICOLOR))
game_over_text_pos = game_over_text.get_rect(center = game_over_block.center)
new_game_plus = 1

# Functions
# Renders all walls and doors
def base_render():
  for i in range(len(wall)):
    pygame.draw.rect(SCREEN, UNICOLOR, wall[i])
  for i in range(len(door)):
    pygame.draw.rect(SCREEN, POWERUPCOLOR, door[i])

# Moves Crate 1 Off Screen
def crate_offscreen1():
  global crate_detail_pos, crate
  crate = pygame.Rect(40*CELLSIZE, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
  crate_detail_pos = crate_detail.get_rect(center = crate.center)

# Moves Crate 2 Off Screen
def crate_offscreen2():
  global crate_detail_pos2, crate2
  crate2 = pygame.Rect(40*CELLSIZE, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
  crate_detail_pos2 = crate_detail.get_rect(center = crate2.center)

# Moves Crate 3 Off Screen
def crate_offscreen3():
  global crate_detail_pos3, crate3
  crate3 = pygame.Rect(40*CELLSIZE, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
  crate_detail_pos3 = crate_detail.get_rect(center = crate3.center)

# Moves Crate 4 Off Screen
def crate_offscreen4():
  global crate_detail_pos4, crate4
  crate4 = pygame.Rect(40*CELLSIZE, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
  crate_detail_pos4 = crate_detail.get_rect(center = crate4.center)

# Resets Game with New Game Plus Mechanics
def reset(win,loss):
  global victory, key_status, boat_x, locked, enemytimer, pos_cachex, pos_cachey, enemy_x, enemy, tile, warning, game_over, PLAYER, enemy_y, timer, new_game_plus, transitioning
  key_status = False
  victory = False
  boat_x = 18*CELLSIZE
  locked = 2
  enemytimer = [0,0,0,0,0,0,0]
  pos_cachex = [0,0,0,0,0,0,0]
  pos_cachey = [0,0,0,0,0,0,0]
  enemy_x, enemy_y = 10*CELLSIZE, 19.5*CELLSIZE
  tile = (2,2)
  PLAYER = pygame.Rect(10*CELLSIZE, 10*CELLSIZE, CELLSIZE, CELLSIZE)
  warning = 0
  game_over = False
  timer = 0
  transitioning = 1
  for i in range(new_game_plus):
    if win == 1:
      new_game_plus += 1
    if loss == 1:
      new_game_plus -= 0

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  mouse_pos = pygame.mouse.get_pos()
  keys = pygame.key.get_pressed()

  #PLAYER Control  
  if paused == 0:   
    player.movement()
    if keys[pygame.K_d] and (not direction_lock == (1,0) and not direction_lock == (1,-1) and not direction_lock == (1,1)):
      PLAYER.x += player.velocity
      direction = (1,0)
    if keys[pygame.K_a] and (not direction_lock == (-1,0) and not direction_lock == (-1,1) and not direction_lock == (-1,-1)):
      PLAYER.x -= player.velocity
      direction = (-1,0)
    if keys[pygame.K_w] and (not direction_lock == (0,1) and not direction_lock == (-1,1) and not direction_lock == (1,1)):
      PLAYER.y -= player.velocity
      direction = (0,1)
    if keys[pygame.K_s] and (not direction_lock == (0,-1) and not direction_lock == (1,-1) and not direction_lock == (-1,-1)):
      PLAYER.y += player.velocity
      direction = (0,-1)
    if keys[pygame.K_d] and keys[pygame.K_w] and not direction_lock == (1,1):
      PLAYER.x += player.velocity-.2
      PLAYER.y -= player.velocity-.2
      direction = (1,1)
    if keys[pygame.K_a] and keys[pygame.K_w] and not direction_lock == (-1,1):
      PLAYER.x -= player.velocity-.2
      PLAYER.y -= player.velocity-.2
      direction = (-1,1)
    if keys[pygame.K_d] and keys[pygame.K_s] and not direction_lock == (1,-1):
      PLAYER.x += player.velocity-.2
      PLAYER.y += player.velocity-.2
      direction = (1,-1)
    if keys[pygame.K_s] and keys[pygame.K_a] and not direction_lock == (-1,-1):
      PLAYER.y += player.velocity-.2
      PLAYER.x -= player.velocity-.2
      direction = (-1,-1)
    # Pause Button Functionality
    if keys[pygame.K_ESCAPE]:
      paused = 1
      print("paused")
    # Radar Effect Functionality
    blink += 1
    if blink >= 700:
      blink = 0

  #Boundaries(Frame)
  if PLAYER.x < 8*CELLSIZE:
    PLAYER.x = 8*CELLSIZE
  if locked == 2:
    if PLAYER.x > 21.5*CELLSIZE:
      PLAYER.x = 21.5*CELLSIZE
  if PLAYER.y < 8*CELLSIZE:
    PLAYER.y = 8*CELLSIZE
  if PLAYER.y > 21.5*CELLSIZE:
    PLAYER.y = 21.5*CELLSIZE

  # Beginning of Render
  SCREEN.fill(BG)

  #Invisibility
  if invisible:
    pygame.draw.rect(SCREEN, (100, 100, 100), PLAYER)
  else:
    pygame.draw.rect(SCREEN, UNICOLOR, PLAYER)

  # Render Frame Borders
  for i in range(len(L1FRAME)):
    pygame.draw.rect(SCREEN, UNICOLOR, L1FRAME[i])

  # Tile (2,2) Code/Visuals
  if tile == (2,2):
    wall = [pygame.Rect(15*CELLSIZE, 8*CELLSIZE, 10, 8*CELLSIZE), pygame.Rect(7.5*CELLSIZE, 15.5*CELLSIZE, 5*CELLSIZE, 10), pygame.Rect(19*CELLSIZE, 11*CELLSIZE, 10, 8*CELLSIZE), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(7.5*CELLSIZE, 18*CELLSIZE, 11, 3*CELLSIZE), pygame.Rect(22.5*CELLSIZE-1, 19*CELLSIZE, 11, 3*CELLSIZE)]

    #Instructions
    for i in range (len(instructions)):
      instruction_text_pos = instruction_text[i].get_rect(topleft = instructions[i].topleft)
      SCREEN.blit(instruction_text[i], instruction_text_pos)

    # (2,2) Enemy/Crate Positioning
    if transitioning == 1:
      powerup_x = 40*CELLSIZE
      timer = 1001
      enemy_x, enemy_y = 10*CELLSIZE, 19.5*CELLSIZE
      crate_pos_x, crate_pos_y = 11*CELLSIZE, 17*CELLSIZE
      crate = pygame.Rect(crate_pos_x, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      crate_offscreen2()
      crate_offscreen3()
      crate_offscreen4()
      enemy_detection = pygame.Rect(new_enemy_x+CELLSIZE,new_enemy_y-2.5*CELLSIZE, 5*CELLSIZE, 5*CELLSIZE)
      transitioning -= 1

    new_enemy_x, new_enemy_y = pos_cachex[0]+enemy_x, enemy_y
    enemy = pygame.Rect(new_enemy_x, new_enemy_y, CELLSIZE, CELLSIZE)

    if paused == 0 and warning != 2:
      enemytimer[0] += 1
      if 100 < enemytimer[0] < 800:
        enemy_detection = pygame.Rect(new_enemy_x+CELLSIZE,new_enemy_y-2.5*CELLSIZE, 5*CELLSIZE, 5*CELLSIZE)
        pos_cachex[0] += 0.2
      if 1100 < enemytimer[0] < 1800:
        enemy_detection = pygame.Rect(new_enemy_x-5*CELLSIZE,new_enemy_y-2.5*CELLSIZE, 5*CELLSIZE, 5*CELLSIZE)
        pos_cachex[0] -= 0.2
      if enemytimer[0] == 2100:
        enemytimer[0] = 0    

    base_render()

    if PLAYER.colliderect(door[0]):
      transitioning = 1
      tile = (1,2)
      PLAYER.x = 21.5*CELLSIZE-5
      PLAYER.y = 19*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[1]):
      transitioning = 1
      tile = (3,2)
      PLAYER.x = 8.5*CELLSIZE
      PLAYER.y = 20*CELLSIZE
      print(tile)

  if tile == (1,2): # Layout and Door Connections Done
    wall = [pygame.Rect(18*CELLSIZE, 11*CELLSIZE, 10, 3*CELLSIZE), pygame.Rect(11*CELLSIZE, 17*CELLSIZE, 11.5*CELLSIZE, 10), pygame.Rect(12*CELLSIZE, 11*CELLSIZE, 10, 3*CELLSIZE), pygame.Rect(12*CELLSIZE, 13.5*CELLSIZE, 6*CELLSIZE, 10), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(8*CELLSIZE, 22.45*CELLSIZE, 3*CELLSIZE, 11), pygame.Rect(22.5*CELLSIZE-1, 18*CELLSIZE, 11, 3*CELLSIZE), pygame.Rect(18*CELLSIZE, 7.5*CELLSIZE, 3*CELLSIZE, 11)]

    new_enemy_x, new_enemy_y = pos_cachex[1]+enemy_x, enemy_y
    enemy = pygame.Rect(new_enemy_x, new_enemy_y, CELLSIZE, CELLSIZE)

    # (1,2) Enemy 1 and 2/Crate Posistioning
    if transitioning == 1:
      enemy_detection = pygame.Rect(new_enemy_x-5*CELLSIZE,new_enemy_y-2.5*CELLSIZE, 5*CELLSIZE, 5*CELLSIZE)
      powerup_x = 40*CELLSIZE
      timer = 1001
      enemy_x, enemy_y = 9*CELLSIZE, 20*CELLSIZE
      enemy_x2, enemy_y2 = 9*CELLSIZE, 9*CELLSIZE
      crate_pos_x, crate_pos_y = 11*CELLSIZE, 18*CELLSIZE
      crate = pygame.Rect(crate_pos_x, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      crate2 = pygame.Rect(crate_pos_x+6*CELLSIZE, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      crate3 = pygame.Rect(14*CELLSIZE, 11*CELLSIZE, 2*CELLSIZE, 2*CELLSIZE)
      crate_offscreen4() 
      transitioning -= 1

    if paused == 0 and warning != 2:
      enemytimer[1] += 1
      if 100 < enemytimer[1] < 1100:
        enemy_detection = pygame.Rect(new_enemy_x+CELLSIZE,new_enemy_y-2.5*CELLSIZE, 5*CELLSIZE, 5*CELLSIZE)  
        pos_cachex[1] += 0.2 
      if 1300 < enemytimer[1] < 2300:
        enemy_detection = pygame.Rect(new_enemy_x-5*CELLSIZE,new_enemy_y-2.5*CELLSIZE, 5*CELLSIZE, 5*CELLSIZE)
        pos_cachex[1] -= 0.2
      if enemytimer[1] == 2500:
        enemytimer[1] = 0

    new_enemy_x2, new_enemy_y2 = pos_cachex[2]+enemy_x2, pos_cachey[2]+enemy_y2
    enemy2 = pygame.Rect(new_enemy_x2, new_enemy_y2, CELLSIZE, CELLSIZE)

    if warning == 0 and enemy_detection2.colliderect(PLAYER) and not invisible:
      timer = 0
      warning = 1
    if warning > 0:
      warning_block = pygame.Rect(new_enemy_x2+5, new_enemy_y2-40, CELLSIZE, CELLSIZE)
      warning_pos = warning_status[0].get_rect(center = warning_block.center)
    if warning == 1:
      SCREEN.blit(warning_status[0], warning_pos)
      timer += 1
    if PLAYER.colliderect(enemy_detection2) and timer > 500 and not invisible:
      warning = 2
    if warning == 1 and timer > 1000:
      warning = 0
    if PLAYER.colliderect(enemy2) and not invisible: 
      warning = 2
    if warning == 2:
      SCREEN.blit(warning_status[1], warning_pos)
      game_over = True

    if blink <= 250:
      pygame.draw.rect(SCREEN, ENEMYCOLOR, enemy2) 

    if paused == 0 and warning != 2:
      enemytimer[2] += 1
      if 100 < enemytimer[2] < 1200:
          pos_cachex[2] += 0.2
          enemy_detection2 = pygame.Rect(new_enemy_x2+CELLSIZE,new_enemy_y2-0.5*CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
      if 1300 < enemytimer[2] < 1900:
          pos_cachey[2] += 0.2
          enemy_detection2 = pygame.Rect(new_enemy_x2-CELLSIZE,new_enemy_y2+CELLSIZE, 3*CELLSIZE, CELLSIZE)
      if 2000 < enemytimer[2] < 3100:
          pos_cachex[2] -= 0.2
          enemy_detection2 = pygame.Rect(new_enemy_x2-5*CELLSIZE,new_enemy_y2-0.5*CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
      if 3200 < enemytimer[2] < 3800:
          pos_cachey[2] -= 0.2
          enemy_detection2 = pygame.Rect(new_enemy_x2-CELLSIZE,new_enemy_y2-2*CELLSIZE, 4*CELLSIZE, 3*CELLSIZE)
      if enemytimer[2] == 3900:
          enemytimer[2] = 0

    base_render()

    if PLAYER.colliderect(door[0]):
      transitioning = 1
      tile = (1,3)
      PLAYER.x = 9*CELLSIZE
      PLAYER.y = 8*CELLSIZE+5
      print(tile)
    if PLAYER.colliderect(door[1]):
      transitioning = 1
      tile = (2,2)
      PLAYER.x = 7.5*CELLSIZE+10
      PLAYER.y = 19*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[2]):
      transitioning = 1
      tile = (1,1)
      PLAYER.x = 19*CELLSIZE
      PLAYER.y = 21.5*CELLSIZE-10
      print(tile)

  if tile == (1,1): # Layout and Door Connections Done
    wall = [pygame.Rect(17*CELLSIZE, 17*CELLSIZE, 10, 6*CELLSIZE), pygame.Rect(8*CELLSIZE, 17*CELLSIZE, 6*CELLSIZE, 10), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(18*CELLSIZE, 22.45*CELLSIZE, 3*CELLSIZE, 11)]

    # (1,1) Enemy/Crate Positioning
    if transitioning == 1:
      powerup_x = 40*CELLSIZE
      timer = 1001
      enemy_x, enemy_y = 14*CELLSIZE, 20*CELLSIZE
      enemy_detection = pygame.Rect(40*CELLSIZE,CELLSIZE, CELLSIZE, CELLSIZE)
      crate_pos_x, crate_pos_y = 14.5*CELLSIZE, 12*CELLSIZE
      crate = pygame.Rect(crate_pos_x, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      crate_offscreen2()
      crate_offscreen3()
      crate_offscreen4()
      transitioning -= 1

    enemy = pygame.Rect(enemy_x, enemy_y, CELLSIZE, CELLSIZE)

    base_render()

    if PLAYER.colliderect(door[0]):
      transitioning = 1
      tile = (1,2)
      PLAYER.x = 19*CELLSIZE
      PLAYER.y = 7.5*CELLSIZE+10
      print(tile)

  if tile == (1,3):
    wall = [pygame.Rect(19*CELLSIZE, 11*CELLSIZE, 10, 5*CELLSIZE), pygame.Rect(8*CELLSIZE, 19*CELLSIZE, 14.5*CELLSIZE, 10), pygame.Rect(15*CELLSIZE, 11*CELLSIZE, 10, 5*CELLSIZE), pygame.Rect(11*CELLSIZE, 11*CELLSIZE, 10, 5*CELLSIZE), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(8*CELLSIZE, 7.5*CELLSIZE, 3*CELLSIZE, 11), pygame.Rect(19.5*CELLSIZE, 22.45*CELLSIZE, 3*CELLSIZE, 11), pygame.Rect(22.45*CELLSIZE, 16*CELLSIZE, 11, 3*CELLSIZE)]

    # (1,3) Enemy/Crate Positioning
    if transitioning == 1:
      timer = 1001
      enemy_x, enemy_y = 9*CELLSIZE, 17*CELLSIZE
      crate_offscreen1()
      crate_offscreen2()
      crate_offscreen3()
      crate_offscreen4()
      transitioning -= 1

    new_enemy_x = pos_cachex[3]+enemy_x
    enemy = pygame.Rect(new_enemy_x, enemy_y, CELLSIZE, CELLSIZE)

    if paused == 0 and warning != 2:
      enemytimer[3] += 1
      if 100 < enemytimer[3] < 1200:
        pos_cachex[3] += 0.2
        enemy_detection = pygame.Rect(new_enemy_x+CELLSIZE,enemy_y-0.5*CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
      if 1400 < enemytimer[3] < 2500:
        pos_cachex[3] -= 0.2
        enemy_detection = pygame.Rect(new_enemy_x-5*CELLSIZE,enemy_y-0.5*CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
      if enemytimer[3] == 2500:
        enemytimer[3] = 0

    #powerup
    if not powerup_activated_0:
      powerup_x = CELLSIZE*16.75
      powerup_y = CELLSIZE*13
      powerup_type = 0 #Invisibility
    else:
      powerup_x = -100
      powerup_y = -100

    if key_status == False:
        key = pygame.Rect(10*CELLSIZE, 21*CELLSIZE, 0.8*CELLSIZE, 3)
        pygame.draw.rect(SCREEN, (255, 255, 0), key)
        pygame.draw.rect(SCREEN, (255, 255, 0), pygame.Rect(10*CELLSIZE+7, 21*CELLSIZE-4, 3, 0.3*CELLSIZE))
        pygame.draw.rect(SCREEN, (255, 255, 0), pygame.Rect(10*CELLSIZE+11, 21*CELLSIZE-4, 3, 0.3*CELLSIZE))
        pygame.draw.circle(SCREEN, (255, 255, 0), (10*CELLSIZE-2, 21*CELLSIZE), 5, 3)
        if PLAYER.colliderect(key):
          key_status = True

    base_render()

    if PLAYER.colliderect(door[0]):
      transitioning = 1
      tile = (1,2)
      PLAYER.x = 9*CELLSIZE
      PLAYER.y = 21.5*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[1]):
      transitioning = 1
      tile = (1,4)
      PLAYER.x = 20.5*CELLSIZE
      PLAYER.y = 8*CELLSIZE+5
      print(tile)
    if PLAYER.colliderect(door[2]):
      transitioning = 1
      tile = (2,3)
      PLAYER.x = 8.5*CELLSIZE
      PLAYER.y = 17*CELLSIZE
      print(tile)

  if tile == (1,4): # Layout and Door Connections Done
    wall = [pygame.Rect(19*CELLSIZE, 7.5*CELLSIZE, 10, 4*CELLSIZE), pygame.Rect(18*CELLSIZE, 19*CELLSIZE, 5*CELLSIZE, 10), pygame.Rect(18*CELLSIZE, 14.5*CELLSIZE, 5*CELLSIZE, 10), pygame.Rect(18*CELLSIZE, 14.5*CELLSIZE, 10, 5*CELLSIZE), pygame.Rect(11*CELLSIZE, 16.5*CELLSIZE, 7*CELLSIZE, 10), pygame.Rect(11*CELLSIZE, 11*CELLSIZE, 8*CELLSIZE, 10), pygame.Rect(11*CELLSIZE, 14.5*CELLSIZE, 10, 5*CELLSIZE), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(19.5*CELLSIZE, 7.5*CELLSIZE, 3*CELLSIZE, 11), pygame.Rect(22.45*CELLSIZE, 19.5*CELLSIZE, 11, 3*CELLSIZE), pygame.Rect(22.45*CELLSIZE, 16*CELLSIZE, 11, 3*CELLSIZE)]

    # (1,4) Enemy/Crate Positioning
    if transitioning == 1:
      timer = 1001
      enemy_x, enemy_y = 9*CELLSIZE, 13*CELLSIZE

      crate_pos_x, crate_pos_y = 14*CELLSIZE, 17.5*CELLSIZE
      crate = pygame.Rect(crate_pos_x, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      crate2 = pygame.Rect(crate_pos_x, crate_pos_y-3*CELLSIZE, 2*CELLSIZE, 2*CELLSIZE)
      crate_offscreen3()
      crate_offscreen4()
      transitioning -= 1

    #powerup
    if not powerup_activated_1:
      powerup_x = CELLSIZE*16.5
      powerup_y = CELLSIZE*9
      powerup_type = 1 #Speed
    else:
      powerup_x, powerup_y = -100, -100

    new_enemy_x, new_enemy_y = pos_cachex[4]+enemy_x, pos_cachey[4]+enemy_y
    enemy = pygame.Rect(new_enemy_x, new_enemy_y, CELLSIZE, CELLSIZE)

    if paused == 0 and warning != 2:
      enemytimer[4] += 1
      if 100 < enemytimer[4] < 900: #1100
          pos_cachey[4] += 0.2
          enemy_detection = pygame.Rect(new_enemy_x-0.5*CELLSIZE,new_enemy_y+CELLSIZE, 2*CELLSIZE, 5*CELLSIZE)
      if 1000 < enemytimer[4] < 2100: #800
          pos_cachex[4] += 0.2
          enemy_detection = pygame.Rect(new_enemy_x+CELLSIZE,new_enemy_y-0.5*CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
      if 2200 < enemytimer[4] < 3300: #1100
          pos_cachex[4] -= 0.2
          enemy_detection = pygame.Rect(new_enemy_x-5*CELLSIZE,new_enemy_y-0.5*CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
      if 3400 < enemytimer[4] < 4200:
          pos_cachey[4] -= 0.2
          enemy_detection = pygame.Rect(new_enemy_x-0.5*CELLSIZE,new_enemy_y-5*CELLSIZE, 2*CELLSIZE, 5*CELLSIZE)
      if 4300 < enemytimer[4] < 5400:
          pos_cachex[4] += 0.2
          enemy_detection = pygame.Rect(new_enemy_x+CELLSIZE,new_enemy_y-0.5*CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
      if 5500 < enemytimer[4] < 6600:
          pos_cachex[4] -= 0.2
          enemy_detection = pygame.Rect(new_enemy_x-5*CELLSIZE,new_enemy_y-0.5*CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
      if enemytimer[4] == 6700:
          enemytimer[4] = 0

    base_render()

    if PLAYER.colliderect(door[0]):
      transitioning = 1
      tile = (1,3)
      PLAYER.x = 20.5*CELLSIZE
      PLAYER.y = 21*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[1]):
      transitioning = 1
      tile = (2,4)
      PLAYER.x = 8*CELLSIZE+5
      PLAYER.y = 20.5*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[2]):
      transitioning = 1
      tile = (2,4)
      PLAYER.x = 8*CELLSIZE+5
      PLAYER.y = 17*CELLSIZE
      print(tile)

  if tile == (2,4): 
    wall = [pygame.Rect(17*CELLSIZE, 13.5*CELLSIZE, 6*CELLSIZE, 10), pygame.Rect(12*CELLSIZE, 12.5*CELLSIZE, 10, 7*CELLSIZE), pygame.Rect(8*CELLSIZE, 19*CELLSIZE, 10*CELLSIZE, 10), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(22.45*CELLSIZE, 8*CELLSIZE, 11, 3*CELLSIZE), pygame.Rect(7.5*CELLSIZE, 19.5*CELLSIZE, 11, 3*CELLSIZE), pygame.Rect(7.5*CELLSIZE, 16*CELLSIZE, 11, 3*CELLSIZE)]

    # (2,4) Enemy/Crate Positioning
    if transitioning == 1:
      timer = 1001
      enemy_x, enemy_y = 10*CELLSIZE, 20*CELLSIZE
      powerup_x = 40*CELLSIZE
      crate_pos_x, crate_pos_y = 12*CELLSIZE, 20.5*CELLSIZE
      crate = pygame.Rect(crate_pos_x, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      crate2 = pygame.Rect(19*CELLSIZE, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      crate3 = pygame.Rect(19*CELLSIZE, 14*CELLSIZE, 2*CELLSIZE, 2*CELLSIZE)
      crate_offscreen4()
      transitioning -= 1

    new_enemy_x, new_enemy_y = pos_cachex[5]+enemy_x, pos_cachey[5]+enemy_y
    enemy = pygame.Rect(new_enemy_x, new_enemy_y, CELLSIZE, CELLSIZE)

    if paused == 0 and warning != 2:
      enemytimer[5] += 1
      if 100 < enemytimer[5] < 1100:
          pos_cachex[5] += 0.2
          enemy_detection = pygame.Rect(new_enemy_x+CELLSIZE,new_enemy_y-0.5*CELLSIZE, 5*CELLSIZE, 3*CELLSIZE)
      if 1200 < enemytimer[5] < 1500:
          pos_cachey[5] -= 0.2
          enemy_detection = pygame.Rect(new_enemy_x-1.5*CELLSIZE,new_enemy_y-3*CELLSIZE, 4*CELLSIZE, 3*CELLSIZE)
      if 1600 < enemytimer[5] < 2200:
          pos_cachex[5] -= 0.2
          enemy_detection = pygame.Rect(new_enemy_x-2*CELLSIZE,new_enemy_y-1.5*CELLSIZE, 2*CELLSIZE, 4*CELLSIZE)
      if 2300 < enemytimer[5] < 2900:
          pos_cachex[5] += 0.2
          enemy_detection = pygame.Rect(new_enemy_x+CELLSIZE,new_enemy_y-1.5*CELLSIZE, 5*CELLSIZE, 4*CELLSIZE)
      if 3000 < enemytimer[5] < 3300:
          pos_cachey[5] += 0.2
          enemy_detection = pygame.Rect(new_enemy_x-1.5*CELLSIZE,new_enemy_y+CELLSIZE, 5*CELLSIZE, 2*CELLSIZE)
      if 3400 < enemytimer[5] < 4400:
          pos_cachex[5] -= 0.2
          enemy_detection = pygame.Rect(new_enemy_x-5*CELLSIZE,new_enemy_y-0.5*CELLSIZE, 5*CELLSIZE, 3*CELLSIZE)
      if enemytimer[5] == 4500:
          enemytimer[5] = 0

    base_render()

    if PLAYER.colliderect(door[0]):
      transitioning = 1
      tile = (3,4)
      PLAYER.x = 8*CELLSIZE+10
      PLAYER.y = 9*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[1]):
      transitioning = 1
      tile = (1,4)
      PLAYER.x = 21*CELLSIZE
      PLAYER.y = 20.5*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[2]):
      transitioning = 1
      tile = (1,4)
      PLAYER.x = 21*CELLSIZE
      PLAYER.y = 17*CELLSIZE
      print(tile)

  if tile == (3,4): 
    wall = [pygame.Rect(11*CELLSIZE, 16*CELLSIZE, 8*CELLSIZE, 10), pygame.Rect(11*CELLSIZE, 7.5*CELLSIZE, 10, 9*CELLSIZE), pygame.Rect(19*CELLSIZE, 7.5*CELLSIZE, 10, 9*CELLSIZE), pygame.Rect(11*CELLSIZE, 20*CELLSIZE, 10, 3*CELLSIZE), pygame.Rect(19*CELLSIZE, 20*CELLSIZE, 10, 3*CELLSIZE), pygame.Rect(15*CELLSIZE, 20*CELLSIZE, 10, 3*CELLSIZE), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(19.5*CELLSIZE, 7.5*CELLSIZE, 3*CELLSIZE, 11), pygame.Rect(7.5*CELLSIZE, 8*CELLSIZE, 11, 3*CELLSIZE)]

    # (3,4) Enemy/Crate Positioning
    if transitioning == 1:
      timer = 1001
      enemy_x, enemy_y = 9*CELLSIZE, 18*CELLSIZE
      powerup_x = 40*CELLSIZE
      crate_pos_x, crate_pos_y = 8*CELLSIZE, 20.5*CELLSIZE
      crate = pygame.Rect(crate_pos_x, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      crate2 = pygame.Rect(12*CELLSIZE, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      crate3 = pygame.Rect(16*CELLSIZE, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      crate4 = pygame.Rect(20*CELLSIZE, crate_pos_y, 2*CELLSIZE, 2*CELLSIZE)
      transitioning -= 1

    new_enemy_x, new_enemy_y = pos_cachex[6]+enemy_x, enemy_y
    enemy = pygame.Rect(new_enemy_x, new_enemy_y, CELLSIZE, CELLSIZE)

    if paused == 0 and warning != 2:
      enemytimer[6] += 1
      if 100 < enemytimer[6] < 1200:
          pos_cachex[6] += 0.2
          enemy_detection = pygame.Rect(new_enemy_x+CELLSIZE,new_enemy_y-1.5*CELLSIZE, 5*CELLSIZE, 4.5*CELLSIZE)
      if 1300 < enemytimer[6] < 2400:
          pos_cachex[6] -= 0.2
          enemy_detection = pygame.Rect(new_enemy_x-5*CELLSIZE,new_enemy_y-1.5*CELLSIZE, 5*CELLSIZE, 4.5*CELLSIZE)
      if enemytimer[6] == 2500:
          enemytimer[6] = 0    

    base_render()

    if PLAYER.colliderect(door[0]):
      transitioning = 1
      tile = (3,3)
      PLAYER.x = 20.5*CELLSIZE
      PLAYER.y = 21*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[1]):
      transitioning = 1
      tile = (2,4)
      PLAYER.x = 21*CELLSIZE
      PLAYER.y = 9*CELLSIZE
      print(tile)

  if tile == (2,3): 
    wall = [pygame.Rect(7.5*CELLSIZE, 19*CELLSIZE, 15*CELLSIZE, 10), pygame.Rect(7.5*CELLSIZE, 15.5*CELLSIZE, 15*CELLSIZE, 10), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(22.5*CELLSIZE-1, 16*CELLSIZE, 11, 3*CELLSIZE), pygame.Rect(7.5*CELLSIZE, 16*CELLSIZE, 11, 3*CELLSIZE)]

    # (2,3) Enemy/Crate Positioning
    if transitioning == 1:
      powerup_x = 40*CELLSIZE
      timer = 1001
      enemy = pygame.Rect(40*CELLSIZE, enemy_y, CELLSIZE, CELLSIZE)
      enemy_detection = pygame.Rect(40*CELLSIZE,CELLSIZE, CELLSIZE, CELLSIZE)
      crate_offscreen1()
      crate_offscreen2()
      crate_offscreen3()
      crate_offscreen4()
      transitioning -= 1

    base_render()

    if PLAYER.colliderect(wall[1]):
      PLAYER.y = (16*CELLSIZE)
    if PLAYER.colliderect(wall[0]):
      PLAYER.y = (18*CELLSIZE)

    if PLAYER.colliderect(door[1]):
      transitioning = 1
      tile = (1,3)
      PLAYER.x = 21*CELLSIZE
      PLAYER.y = 17*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[0]):
      transitioning = 1
      tile = (3,3)
      PLAYER.x = 8.5*CELLSIZE
      PLAYER.y = 17*CELLSIZE
      print(tile)

  if tile == (3,3): 
    wall = [pygame.Rect(7.5*CELLSIZE, 19*CELLSIZE, 12*CELLSIZE, 10), pygame.Rect(19*CELLSIZE, 19*CELLSIZE, 10, 4*CELLSIZE), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(19.5*CELLSIZE, 22.45*CELLSIZE, 3*CELLSIZE, 11), pygame.Rect(7.5*CELLSIZE, 16*CELLSIZE, 11, 3*CELLSIZE), pygame.Rect(19.5*CELLSIZE, 7.5*CELLSIZE, 3*CELLSIZE, 11)]

    # (3,3) Enemy/Crate Positioning
    if transitioning == 1:
      powerup_x = 40*CELLSIZE
      timer = 1001
      enemy = pygame.Rect(40*CELLSIZE, enemy_y, CELLSIZE, CELLSIZE)
      enemy_detection = pygame.Rect(40*CELLSIZE,CELLSIZE, CELLSIZE, CELLSIZE)
      crate_offscreen1()
      crate_offscreen2()
      crate_offscreen3()
      crate_offscreen4()
      transitioning -= 1

    # Backup Wall Collision Code
    if PLAYER.y > 18*CELLSIZE and PLAYER.x < 19.5*CELLSIZE-10:
        PLAYER.y = 18*CELLSIZE
    if PLAYER.y > 19*CELLSIZE and PLAYER.x <= 19*CELLSIZE+10:
      PLAYER.x = 19*CELLSIZE+10

    # Exit Door Render
    exit_door = pygame.Rect(22.45*CELLSIZE, 14*CELLSIZE, 11, 3*CELLSIZE)
    key_symbol = pygame.Rect(22.6*CELLSIZE, 15*CELLSIZE+7, 4, 7)
    pygame.draw.rect(SCREEN, (255,255,255), exit_door)
    pygame.draw.circle(SCREEN, (0,0,0), (22.7*CELLSIZE, 15*CELLSIZE+5), 4)
    pygame.draw.rect(SCREEN, (0,0,0), key_symbol)

    # Exit Door Functionality
    if PLAYER.colliderect(exit_door) and key_status == True:
      tile = (4,3)
      PLAYER.x = 8.5*CELLSIZE
      PLAYER.y = 15*CELLSIZE
      print(tile)

    base_render()

    if PLAYER.colliderect(door[1]):
      transitioning = 1
      tile = (2,3)
      PLAYER.x = 21*CELLSIZE
      PLAYER.y = 17*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[0]):
      transitioning = 1
      tile = (3,4)
      PLAYER.x = 20.5*CELLSIZE
      PLAYER.y = 8.5*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[2]):
      transitioning = 1
      tile = (3,2)
      PLAYER.x = 20.5*CELLSIZE
      PLAYER.y = 21*CELLSIZE
      print(tile)  

  if tile == (3,2): 
    wall = [pygame.Rect(12*CELLSIZE, 12*CELLSIZE, 10, 11*CELLSIZE), pygame.Rect(19*CELLSIZE, 12*CELLSIZE, 10, 11*CELLSIZE), pygame.Rect(12*CELLSIZE, 12*CELLSIZE, 4*CELLSIZE, 10), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(19.5*CELLSIZE, 22.45*CELLSIZE, 3*CELLSIZE, 11), pygame.Rect(7.5*CELLSIZE, 19*CELLSIZE, 11, 3*CELLSIZE)]

    # (3,2) Enemy/Crate Positioning
    if transitioning == 1:
      powerup_x = 40*CELLSIZE
      timer = 1001
      enemy = pygame.Rect(40*CELLSIZE, enemy_y, CELLSIZE, CELLSIZE)
      enemy_detection = pygame.Rect(40*CELLSIZE,CELLSIZE, CELLSIZE, CELLSIZE)
      crate_offscreen1()
      crate_offscreen2()
      crate_offscreen3()
      crate_offscreen4()
      transitioning -= 1

    base_render()

    if PLAYER.colliderect(door[1]):
      transitioning = 1
      tile = (2,2)
      PLAYER.x = 21*CELLSIZE
      PLAYER.y = 19*CELLSIZE
      print(tile)
    if PLAYER.colliderect(door[0]):
      transitioning = 1
      tile = (3,3)
      PLAYER.x = 20.5*CELLSIZE
      PLAYER.y = 8.5*CELLSIZE
      print(tile)

    # Escape Room
  if tile == (4,3): 
    wall = [pygame.Rect(7.5*CELLSIZE, 18.5*CELLSIZE, 9.5*CELLSIZE, 10), pygame.Rect(17*CELLSIZE, 12*CELLSIZE, 10, 6.5*CELLSIZE+10), pygame.Rect(7.5*CELLSIZE, 12*CELLSIZE, 9.5*CELLSIZE, 10), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0), pygame.Rect(40*CELLSIZE, CELLSIZE, 0,0)]
    door = [pygame.Rect(7.5*CELLSIZE, 14*CELLSIZE, 11, 3*CELLSIZE)]

    # (4,3) Enemy/Crate Positioning
    if transitioning == 1:
      powerup_x = 40*CELLSIZE
      timer = 1001
      enemy = pygame.Rect(40*CELLSIZE, enemy_y, CELLSIZE, CELLSIZE)
      enemy_detection = pygame.Rect(40*CELLSIZE,CELLSIZE, CELLSIZE, CELLSIZE)
      crate_offscreen1()
      crate_offscreen2()
      crate_offscreen3()
      crate_offscreen4()
      transitioning -= 1

    boat = [pygame.Rect(boat_x, 16*CELLSIZE, 2.5*CELLSIZE, 0.2*CELLSIZE), pygame.Rect(boat_x-CELLSIZE, 15*CELLSIZE, 4*CELLSIZE, 1*CELLSIZE)]
    for i in range(len(boat)):
      pygame.draw.rect(SCREEN, POWERUPCOLOR, boat[i])
      if PLAYER.colliderect(boat[i]):
        PLAYER.x, PLAYER.y = boat_x, 14*CELLSIZE+5
        locked = 1
        victory = True
    if victory == True:
      boat_x += 0.3
      pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(22.5*CELLSIZE+10, 7.5*CELLSIZE, 10*CELLSIZE, 10*CELLSIZE))

    base_render()

    if PLAYER.colliderect(door[0]):
      tile = (3,3)
      PLAYER.x = 20.5*CELLSIZE
      PLAYER.y = 15*CELLSIZE
      print(tile)

    #Blinking Radar Effect
  if blink <= 250:
    crate_detail_pos = crate_detail.get_rect(center = crate.center)
    crate_detail_pos2 = crate_detail.get_rect(center = crate2.center)
    crate_detail_pos3 = crate_detail.get_rect(center = crate3.center)
    crate_detail_pos4 = crate_detail.get_rect(center = crate4.center)
    pygame.draw.rect(SCREEN, SCENERYCOLOR, crate, 5)
    pygame.draw.rect(SCREEN, SCENERYCOLOR, crate2, 5)
    pygame.draw.rect(SCREEN, SCENERYCOLOR, crate3, 5)
    pygame.draw.rect(SCREEN, SCENERYCOLOR, crate4, 5)
    SCREEN.blit(crate_detail, crate_detail_pos)
    SCREEN.blit(crate_detail, crate_detail_pos2)
    SCREEN.blit(crate_detail, crate_detail_pos3)
    SCREEN.blit(crate_detail, crate_detail_pos4)
    pygame.draw.rect(SCREEN, ENEMYCOLOR, enemy)

  # Enemy Detection System
  # pygame.draw.rect(SCREEN, (UNICOLOR), enemy_detection)
  # pygame.draw.rect(SCREEN, (UNICOLOR), enemy_detection2)
  if warning == 0 and enemy_detection.colliderect(PLAYER) and not invisible:
    timer = 0
    warning = 1
  if warning > 0:
    warning_block = pygame.Rect(new_enemy_x+5, new_enemy_y-40, CELLSIZE, CELLSIZE)
    warning_pos = warning_status[0].get_rect(center = warning_block.center)
  if warning == 1:
    SCREEN.blit(warning_status[0], warning_pos)
    timer += 1
  if PLAYER.colliderect(enemy_detection) and timer > 500 and not invisible:
    warning = 2
  if warning == 1 and timer > 1000:
    warning = 0
  if PLAYER.colliderect(enemy) and not invisible: 
    warning = 2
  if warning == 2:
    SCREEN.blit(warning_status[1], warning_pos)
    game_over = True
    timer += 1

  # Radar Indicator
  if paused == 0:
    if blink == 0:
      radarsize = 3*CELLSIZE
    if blink == 251:
      radarsize = 0
    if 250 < blink < 700:
      radarsize += 0.135
  pygame.draw.circle(SCREEN, UNICOLOR, (26*CELLSIZE, 4*CELLSIZE), 3*CELLSIZE, 5)
  pygame.draw.circle(SCREEN, UNICOLOR, (26*CELLSIZE, 4*CELLSIZE), radarsize, 3)

  if boat_x >= 500:
    pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(0,0 , SCREEN_WIDTH, SCREEN_HEIGHT))
  if boat_x >= 600:
    SCREEN.blit(endgame_text, endgame_text_pos)
  if boat_x >= 700:
    pygame.draw.rect(SCREEN, UNICOLOR, reset_button, 5)
    SCREEN.blit(reset_text, reset_text_pos)
    if reset_button.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
      reset(1,0)

  # Wall Collsion Code (Detection) (Sticky)
  for i in range(len(wall)):
    if i == 7:
      i = x
    if not PLAYER.colliderect(wall[i]):
      direction_lock = (0,0)
    if PLAYER.colliderect(wall[i]): 
      x = i
      if direction == (0,1):
        direction_lock = (0,1)
      if direction == (0,-1):
        direction_lock = (0,-1)
      if direction == (1,0):
        direction_lock = (1,0)
      if direction == (-1,0):
        direction_lock = (-1,0)
      if direction == (-1,1):
        direction_lock = (-1,1)
      if direction == (-1,-1):
        direction_lock = (-1,-1)
      if direction == (1,1):
        direction_lock = (1,1)
      if direction == (1,-1):
        direction_lock = (1,-1)

  #Hiding(Crates)
  if crate.colliderect(PLAYER) or crate2.colliderect(PLAYER) or crate3.colliderect(PLAYER) or crate4.colliderect(PLAYER) or invis_powerup:
    invisible = True
  else:
    invisible = False
  # Objective Updater
  if victory == False:
    if key_status == False:
      SCREEN.blit(objective[0], objective_pos)
    else:
      SCREEN.blit(objective[1], objective_pos)
  # Speed Boost Powerup Value changes
  if speed_boost:
    player.velocity = 1
  # New Game Plus Content
  else:
    player.velocity = 0.5+(new_game_plus*0.1)

  #Powerup Render
  powerup = pygame.Rect(powerup_x, powerup_y, CELLSIZE, CELLSIZE)
  qmark_pos = qmark.get_rect(center = powerup.center)
  pygame.draw.rect(SCREEN, (0, 255, 255), powerup)
  SCREEN.blit(qmark, qmark_pos)

  # Gameover Scene
  if game_over == True and timer >= 1000:
    pygame.draw.rect(SCREEN, (0,0,0), pygame.Rect(0,0 , SCREEN_WIDTH, SCREEN_HEIGHT))
    if timer >= 1200:
      SCREEN.blit(game_over_text, game_over_text_pos)
    if timer >= 1600:
      pygame.draw.rect(SCREEN, UNICOLOR, reset_button, 5)
      SCREEN.blit(reset_text, reset_text_pos)
      if reset_button.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
        reset(0,1)

  # Pause Menu and Functionality
  if paused == 1:
    pause_blur.fill((50,50,50,200))
    SCREEN.blit(pause_blur, (0,0))
    SCREEN.blit(paused_text, paused_text_pos)
    SCREEN.blit(unpause_text, unpause_text_pos)
    pygame.draw.rect(SCREEN, UNICOLOR, unpause_button, 5)
    if unpause_button.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
      paused = 0
  if boat_x >= 700 or paused == 1 or timer >= 1600:
    pygame.draw.rect(SCREEN, UNICOLOR, quit_button, 5)
    SCREEN.blit(quit_text, quit_text_pos)
    if quit_button.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
      pygame.quit()
      sys.exit()

  #Powerup Activation
  if PLAYER.colliderect(powerup):
    if powerup_type == 0:
      invis_powerup = True
      powerup_activated_0 = True
    if powerup_type == 1:
      speed_boost = True
      powerup_activated_1 = True
    tick = 1250

  #Powerup Clock
  if tick >= 0 and (invis_powerup or speed_boost):
    tick -= 1
  elif tick <= 0:
    invis_powerup = False
    speed_boost = False
    tick = 1250

  CLOCK.tick(FPS)
  pygame.display.update()
