# Make a list of commands that will allow this robot
# to cover a space of 5m x 5m. Plot the resulting path (x, y) 
# and trajectory (x, y, and angular velocities).


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import pygame


# time_duration = [10,2,2,2,2] # sec
# vl = [5,0,2,0,2] # m/s
# vr = [5,2,0,2,2] # m/s



bot_width = .30 # m
bot_length = .50 # m

turn_arc = 2 * np.pi * (bot_width/2)/2 #half arc Circumference
area_to_cover =25 # 5x5 =25 m^2

time_duration = [.01,1,1] # sec
vl = [1,0,turn_arc/time_duration[1]] # m/s
vr = [1,turn_arc/time_duration[0],0] # m/s


t_step = 0.001 


colors = ['r', 'g', 'b', 'm', 'y']
LINEWIDTH=0.8
fig, ax= plt.subplots(1,1)#plt.figure()
# ax = fig.add_subplot(121)
# ax_2 = fig.add_subplot(122)

x = 0 
y = 0
for i in range(0,len(time_duration)):
    print('Test number: ', i)
    psi = 0 
    xlist =[]
    ylist =[]
    
    max_time = time_duration[i]
    for dt in np.arange(0.0, max_time,t_step):
        
        xlist = np.append(xlist,x)
        ylist = np.append(ylist,y)
        
        Psi_dot = (vr[i] - vl[i])/ bot_width
        psi =  psi + Psi_dot *t_step
        x +=  -((vl[i] + vr[i])/2 )* np.sin(psi)  * t_step#-v *np.sin(psi) * t_step
        y += ((vl[i] + vr[i])/2 )* np.cos(psi)  * t_step#  v* np.cos(psi) * t_step

    legend_str = ''f'time duration: {time_duration[i]}, Left V≈ {round(vl[i],3)}, Right V≈ {round(vr[i],3)}'
    ax.plot(xlist, ylist, colors[i],marker='o' ,label=legend_str, linewidth=LINEWIDTH)
    ax.legend(loc = "upper left")
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')

ax.plot(.3/2,0,marker='o')
ax.plot(-.3/2,0,marker='o')

# ax.plot(0,0,marker='D')
# ax.plot(0,5,marker='D')
# ax.plot(-5,5,marker='D')
# ax.plot(-5,0,marker='D')
# ax.plt.xlim(-1, 1)
# ax.plt.ylim(-1, 1)
ax.axis('scaled') #plt.gca().set_aspect('equal', adjustable='box')

plt.ioff()
plt.show()