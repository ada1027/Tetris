import os
import pygame
from copy import deepcopy
from random import choice, randrange

width = 10
height = 12
tile = 45
screen_size = 750, 600
tetris_screen_size = width * tile, height * tile

pygame.init()
screen = pygame.display.set_mode(screen_size)
game_screen = pygame.Surface(tetris_screen_size)
clock = pygame.time.Clock()

tetris_grid = []
for y in range(height):
  for x in range(width):
    rect = pygame.Rect(x * tile, y * tile, tile, tile)
    tetris_grid.append(rect)
  
# figures: i piece, o piece, z piece, s piece, L piece, J piece, T piece 
figures_positions = [[(-2, 0), (-1, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = []
for figpos in figures_positions:
  fig_rects = []
  for x,y in figpos:
    rect = pygame.Rect(x + width // 2, y + 1, 1, 1)
    fig_rects.append(rect)
  figures.append(fig_rects)
figure_rect = pygame.Rect(0, 0, tile - 2, tile - 2)
field = []
for a in range(height):
  row = []
  for b in range(width):
    row.append(0)
  field.append(row)    

bg_image = pygame.image.load(os.path.join(os.path.dirname(__file__),'img','bg.jpg')).convert_alpha()
bg = pygame.transform.scale(bg_image, (900, 650))
game_bg_img = pygame.image.load(os.path.join(os.path.dirname(__file__),'img','skyline.jpeg')).convert_alpha()
game_bg = pygame.transform.scale(game_bg_img, (1400,700))
main_font = pygame.font.Font('font.ttf', 65)
font = pygame.font.Font('font.ttf', 45)

title_tetris = main_font.render('TETRIS', True, pygame.Color('purple'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('blue'))
get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))
#random colors
color = get_color()
next_color = get_color()
#random figures
figure = deepcopy(choice(figures))
next_figure = deepcopy(choice(figures))

  
animation_count = 0
animation_speed = 40
animation_limit = 2000
score = 0
lines = 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

def check_if_borders():
  xvalue = figure[i].x
  yvalue = figure[i].y
  if xvalue < 0 or xvalue > width - 1:
    return False
  elif yvalue > height -1 or field[yvalue][xvalue]:
    return False
  return True

def get_player_record():
  try:
    #open file for reading
    f = open("record.txt", "r")
    return f.readline()
  #error catching
  except FileNotFoundError:
    #open file for writing
    f = open("record.txt", "w")
    f.write('0')

def set_player_record(record, score):
  top_record = max(int(record), score)
  #open file for writing
  f = open("record.txt", "w")
  f.write(str(top_record))
  
while True:
  record = get_player_record()
  dx = 0
  rotate = False
  #display background images
  screen.blit(bg, (0, 0))
  screen.blit(game_screen, (20, 20))
  game_screen.blit(game_bg, (0, 0))
  #keyboard control pieces
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        dx = -1
      elif event.key == pygame.K_RIGHT:
        dx = 1
      elif event.key == pygame.K_DOWN:
        animation_limit = 100
      elif event.key == pygame.K_UP:
        rotate = True

  #moving left and right (moving x)
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_if_borders():
            figure = deepcopy(figure_old)
            break

  #moving down (moving y)
  animation_count += animation_speed
  if animation_count > animation_limit:
    animation_count = 0
    old_figure = deepcopy(figure)
    for i in range(4):
      figure[i].y += 1
      if not check_if_borders():
        for i in range(4):
          field[old_figure[i].y][old_figure[i].x] = color
        figure = next_figure 
        color = next_color
        next_figure = deepcopy(choice(figures))
        next_color = get_color()
        animation_limit = 2000
        break
        
  # rotate figure 
  center = figure[0]
  figure_old = deepcopy
  if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_if_borders():
                figure = deepcopy(figure_old)
                break
        
        
  # check lines if fully filled
  line = height - 1
  lines = 0
  for row in range(height-1, -1, -1):
        count = 0
        for i in range(width):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < width:
            line -= 1
        else:
            animation_speed += 3
            lines += 1

  # create score
  score += scores[lines]
    
#draw grid
  for gridrect in tetris_grid:
      pygame.draw.rect(game_screen, (40, 40, 40), gridrect, 1) 
 
#draw figure
  for i in range(4):
      figure_rect.x = figure[i].x * tile 
      figure_rect.y = figure[i].y * tile 
      pygame.draw.rect(game_screen, color, figure_rect)

# draw field
  for y in range(len(field)):
      row = field[y]
      for x in range(len(row)):
        column = row[x]
        if column:
          figure_rect.x = x * tile
          figure_rect.y = y * tile
          pygame.draw.rect(game_screen, column, figure_rect)
    
#draw next piece
  for i in range(4):
      figure_rect.x = next_figure[i].x * tile + 370
      figure_rect.y = next_figure[i].y * tile + 100
      pygame.draw.rect(screen, color, figure_rect)
      
  #Display the Titles
  screen.blit(title_tetris, (485, 10))
  screen.blit(title_score, (535, 250))
  screen.blit(font.render(str(score), True, pygame.Color('blue')), (590, 300))
  screen.blit(title_record, (525, 400))
  screen.blit(font.render(record, True, pygame.Color('gold')), (555, 450))

#game over
  for i in range(width):
      if field[0][i]:
          set_player_record(record, score)
          #reset field
          field = []
          for j in range(height):
              row = []
              for i in range(width):
                  row.append(0)
              field.append(row)
          animation_count = 0
          animation_speed = 60
          animation_limit = 2000
          score = 0
          for i_rect in tetris_grid:
            screen.blit(game_screen, (20, 20))
            pygame.display.flip()
            clock.tick(200)

  pygame.display.flip()
  clock.tick(60)
 