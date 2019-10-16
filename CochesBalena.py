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

# Just return the actions we are interested in
def wait_for_move():
  while True:
    e = sense.stick.wait_for_event()
    if e.action != ACTION_RELEASED:
      return e
      
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
  print_road()
  next_step()
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
  gen_p = randint(s[0]-s[1]-1,s[0]+s[1]-1)
  gen_r = randint(1,3)
  gen_p = 0 if gen_p < 0 else gen_p
  gen_p = 4 if gen_p > 4 else gen_p
  returnable = [gen_p  ,gen_r]
  #print("gen_step: "+str(returnable))
  return returnable
  #return [randint(s[0]-s[1]-1,s[0]+s[1]-1),randint(1,3)]

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
      s = s+1
      
    
    i = i+1 
    
      
  
  

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
  
  print_speed2()
  print_static_walls()
  #e = wait_for_move()
  check_time()
  #sleep(8/speed/4)
  
  for e in sense.stick.get_events():
    if e.action != ACTION_RELEASED:
      #sense.clear()
      if e.direction ==  DIRECTION_UP:
        y = y - 1
        
      elif e.direction ==  DIRECTION_DOWN:
        y = y + 1
    
      elif e.direction ==  DIRECTION_LEFT:
        x = x - 1
    
      elif e.direction ==  DIRECTION_RIGHT:
        x = x + 1
      print(x, y, W)
      sense.set_pixel((x % 7), (y % 8), W)
      sense.set_pixel(player[0], player[1], [0,0,0])
      player = [x % 7, y % 8]
      
sense.show_message("Score: " + str(score))
  
  
