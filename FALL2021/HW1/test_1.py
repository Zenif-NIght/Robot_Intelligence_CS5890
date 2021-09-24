import numpy as np
from matplotlib import pyplot as plt

xpos = [0]
ypos = [0]
psi = [0]

def step(vl, vr, dt=0.01):
    t_step = dt
    psinew =  psi[-1] + (vl-vr)/.30 *t_step
    xnew = xpos[-1] - ((vl + vr)/2 )* np.sin(psi[-1])  * t_step#-v *np.sin(psi) * t_step
    ynew = ypos[-1] + ((vl + vr)/2 )* np.cos(psi[-1])  * t_step#  v* np.cos(psi) * t_step
    xpos.append(xnew)
    ypos.append(ynew)
    psi.append(psinew)

for i in  range(500):
    step(1.0, 1.5)
plt.plot(xpos,ypos)
plt.show()