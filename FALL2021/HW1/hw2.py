
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import pygame


time_duration = [5,3,8,10]
vl = [1,-1,0.8, 2]
vr = [1.5,-1.5,-2,2]

bot_width = .30 # cm
bot_length = .50 # cm

num_runs = 4
t_step = 0.001 

all_x =[]
all_y =[]

colors = ['r', 'g', 'b', 'm', 'y']
LINEWIDTH= 1000 #0.0008
fig, ax= plt.subplots(1,1)

x = 0 
y = 0
psi = 0
Psi_dot = 0
for i in range(0,num_runs):
    print('Test number: ', i)

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
    
    legend_str = ''f'time duration: {time_duration[i]}, Left Wheel Velocity: {vl[i]}, Right Wheel Velocity: {vr[i]}'
    ax.plot(xlist, ylist, colors[i] ,label=legend_str)
    ax.legend()
    ax.axis('scaled') 
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')

plt.ioff()
plt.show()