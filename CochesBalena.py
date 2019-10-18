#!/bin/python3

from sense_hat import *
from time import *
from random import randint
from copy import deepcopy

sense = SenseHat()
sense.clear()
speed = 1
score = 0
last_cicle = time()
CRASH = False


# Print speed
def print_speed2():
  temp = sense.get_temperature()
  speed = 1
  i = 1
  sense.set_pixel(7, 7, R)
  while i <= 8:
	if temp > 20:
		speed = speed + 1
		temp = temp -5
		sense.set_pixel(7, 8-i, R)
	else:
		sense.set_pixel(7, 8-i, [0,0,0])	
	i = i + 1
  
def check_time():
  global last_cicle
  if (time() - last_cicle) > (0.3/speed):
    road_run()
    last_cicle = time()

    
def print_static_walls():
  sense.set_pixel(6, 0, G)
  sense.set_pixel(6, 1, G)
  sense.set_pixel(6, 2, G)
  sense.set_pixel(6, 3, G)
  sense.set_pixel(6, 4, G)
  sense.set_pixel(6, 5, G)
  sense.set_pixel(6, 6, G)
  sense.set_pixel(6, 7, G)
  sense.set_pixel(0, 0, G)
  sense.set_pixel(0, 1, G)
  sense.set_pixel(0, 2, G)
  sense.set_pixel(0, 3, G)
  sense.set_pixel(0, 4, G)
  sense.set_pixel(0, 5, G)
  sense.set_pixel(0, 6, G)
  sense.set_pixel(0, 7, G)




road = [[2,3],[2,2],[2,1],[2,2],[1,2],[1,2],[1,2],[1,2]]

def road_run():
  clear_road()
  next_step()
  print_road()
  #print(road)
  
  
def clear_road():
  i=0
  j=0
  while i < 5:
    while j < 8:
      sense.set_pixel(i, 7-i, [0,0,0])
      j = j+1
    i = i+1


def next_step():
  global road
  road = road[1:]+[generate_step(road[-1])]
  
def generate_step(s):
  global score
  gen_p = randint(max(0, s[0]-s[1]+1),  min(s[0]+s[1]-1, 4))
  gen_r = randint(max(s[1]-1, 1) ,  min(s[1]+1, 3))
  returnable = [gen_p  ,gen_r]
  score = score + 1
  print("returnable"+str(returnable))
  return returnable

def print_road():
  global player
  auxRoad = deepcopy(road)
  #print("auxRoad: "+str(auxRoad))
  i=0
  while i < 8:
    step = [0,0,0,0,0]
    r = auxRoad[i]
    #print("r["+str(i)+"]: "+str(r))
    step[r[0]] = 1
    while r[1] > 0:
      offs=r[1]-1
      step[r[0]+offs if r[0]+offs <= 4 else 4] = 1
      step[r[0]-offs if r[0]-offs >= 0 else 0] = 1
      r[1] = r[1] - 1
    
    #print("step["+str(i)+"]: "+str(step))
    s = 0
    while s < 5:
      if player != [s +1, 7-i]:
        sense.set_pixel(s +1, 7-i, B if step[s] == 0 else [0,0,0])
      if player == [s +1, 7-i] and step[s] == 0:
        sense.set_pixel(s +1, 7-i, Y)
        crash()
      s = s+1
      
    
    i = i+1
    
def wall(s):
  step = deepcopy(road[s[1]])
  return x < step[0]-step[1]+1 or x > step[0]+step[1]-1
  
def crash():
  global CRASH
  CRASH = True

def check_if_bueno_nenes(pos):
  if wall(pos):
    crash()
    print("CRASHSSSHSHSHSH")

R = [255, 0, 0]  # red
Y = [255, 255, 0] # yellow
G = [0, 255, 0] # green
W = [255, 255, 255] # white
B = [0, 0, 255] # blue

  
#print player
player = [3,7]
sense.set_pixel(player[0], player[1], W)
x=3
y=7


while True:
  
  if CRASH:
    break
  print_speed2()
  print_static_walls()
  check_time()
  
  for e in sense.stick.get_events():
    if e.action != ACTION_RELEASED:
      if e.direction ==  DIRECTION_UP:
        y = y - 1
        
      elif e.direction ==  DIRECTION_DOWN:
        y = y + 1
    
      elif e.direction ==  DIRECTION_LEFT:
        x = x - 1
    
      elif e.direction ==  DIRECTION_RIGHT:
        x = x + 1
        
      x = x % 7
      y = y % 8
      check_if_bueno_nenes([x, y])
      sense.set_pixel(x, y, W)
      sense.set_pixel(player[0], player[1], [0,0,0])
      player = [x, y]
      if CRASH:
        break

sense.show_message("Score: " + str(score))
  
  
