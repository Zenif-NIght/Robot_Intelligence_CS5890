
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import pygame


time_duration = [5,3,8,10]
vl = [1,-2,0.8, 2]
vr = [1.5,-1.5,-2,2]

bot_width = 30 # cm
bot_length = 50 # cm

num_runs = 4
t_step = 0.001 

all_x =[]
all_y =[]

colors = ['r', 'g', 'b', 'm', 'y']
LINEWIDTH=0.8
fig, ax= plt.subplots(1,1)#plt.figure()
# ax = fig.add_subplot(121)
# ax_2 = fig.add_subplot(122)

for i in range(0,num_runs):
    print('Test number: ', i)
    x = 0 
    y = 0
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

    all_x = np.append(all_x,xlist)
    all_y = np.append(all_y,ylist)
    
    legend_str = ''f'time duration: {time_duration[i]}, Left Wheel Velocity: {vl[i]}, Right Wheel Velocity: {vr[i]}'
    ax.plot(xlist, ylist, colors[i],marker='o' ,label=legend_str, linewidth=LINEWIDTH)
    ax.legend()
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')



plt.ioff()
plt.show()