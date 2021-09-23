# Make a list of commands that will allow this robot
# to cover a space of 5m x 5m. Plot the resulting path (x, y) 
# and trajectory (x, y, and angular velocities).

import matplotlib.pyplot as plt
import numpy as np

bot_width = .30 # m
bot_length = .50 # m

turn_arc = np.pi * (bot_width) #half arc Circumference

x_side_length = 5
y_side_length = 5
area_to_cover =x_side_length * y_side_length # 5x5 =25 m^2

# plan [time_duration , vl, vr]
go_straight_up = np.array([y_side_length,1,1])
go_straight_down = np.array([y_side_length,-1,-1])
turn_r_180 = np.array([1,turn_arc/1,0])
turn_l_180 = np.array([1,-turn_arc/1,0])


execution_plan =[] 
for i in range(0,int((x_side_length/bot_width)/2+1)):

    # print('Iteration:',i)
    execution_plan.append(go_straight_up)
    execution_plan.append(turn_r_180)
    execution_plan.append(go_straight_down)
    execution_plan.append(turn_l_180)

t_step = 0.01 

colors = ['r', 'g', 'b', 'm', 'y']
LINEWIDTH=3 #0.8

fig = plt.figure()
ax = fig.add_subplot(111)

fig2 = plt.figure()
ax_2 = fig2.add_subplot(311)
ax_3 = fig2.add_subplot(312)
ax_4 = fig2.add_subplot(313)

xDot = 0 
yDot = 0
Psi_dot = 0

x = 0 
y = 0

xDot_list =[]
yDot_list =[]
Psi_dot_list =[]

execution_plan = np.array(execution_plan)
# print(len(execution_plan))
plotLIst = []
for i in range(0,len(execution_plan)):
    
    psi = 0 

    xlist =[]
    ylist =[]
    
    
    time_duration = execution_plan[i][0]
    max_time = time_duration
    for dt in np.arange(0.0, max_time,t_step):
        
        xlist = np.append(xlist,x)
        ylist = np.append(ylist,y)
        
        xDot_list = np.append(xDot_list,xDot)
        yDot_list = np.append(yDot_list,yDot)
        Psi_dot_list = np.append(Psi_dot_list,Psi_dot)
        vl = execution_plan[i][1]
        vr = execution_plan[i][2]
        
        Psi_dot = (vr - vl)/ bot_width
        psi =  psi + Psi_dot *t_step
        xDot = -((vl + vr)/2 )* np.sin(psi) 
        yDot = ((vl + vr)/2 )* np.cos(psi) 
        
        x += xDot * t_step#-v *np.sin(psi) * t_step
        y += yDot * t_step#  v* np.cos(psi) * t_step
        

    ax.plot(xlist, ylist,marker='o' , linewidth=LINEWIDTH)
    
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')

ax.plot(.3/2,0,marker='o')
ax.plot(-.3/2,0,marker='o')

ax.plot(0,0,marker='D')
ax.plot(0,5,marker='D')
ax.plot(5,5,marker='D')
ax.plot(5,0,marker='D')
ax.axis('scaled') 

vel_linewidth = 1

ax_2.set_ylabel('X velocity')
ax_3.set_ylabel('Y velocity')
ax_4.set_ylabel('Ψ velocity')

ax_4.set_xlabel('Time 0.01 Seconds')

ax_2.plot( xDot_list , linewidth=vel_linewidth)
ax_3.plot( yDot_list  , linewidth=vel_linewidth)
ax_4.plot( Psi_dot_list  , linewidth=vel_linewidth)


plt.ioff()
plt.show()
