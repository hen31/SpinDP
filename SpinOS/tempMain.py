__author__ = 'Rubens'

from MovementHandler import MovementHandler
import time

move = MovementHandler()

leg = move.legs[0]
leg.last_x = 0
leg.last_y = 150
alpha, beta, gamma = move.get_angles(200, 150, MovementHandler.min_height_mm)
leg.set_height(alpha+30)
time.sleep(0.5)
leg.set_hip(gamma)
leg.set_knee(beta)
time.sleep(0.5)
leg.set_height(alpha)
time.sleep(0.5)
alpha, beta, gamma = move.get_angles(0, 150, MovementHandler.min_height_mm)
leg.set_height(alpha+30)
time.sleep(0.5)
leg.set_hip(gamma)
leg.set_knee(beta)
time.sleep(0.5)
leg.set_height(alpha)
x=0
y=150
time.sleep(3)
alpha, beta, gamma = move.get_angles(50, 150, MovementHandler.min_height_mm+100)
alpha = 90
beta = 90
gamma = 90
#test = 90
print int(alpha)
print int(beta)
print int(gamma)
if gamma < 0:
    gamma = 180 + gamma
    
while True:
    move.legs[0].set_hip(int(gamma))
    move.legs[0].set_height(int(alpha))
    move.legs[0].set_knee(int(beta))
    break
    time.sleep(1)
