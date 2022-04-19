


import numpy as np
import math
import matplotlib.pyplot as plt
import time

#set de valores para los ángulos
n_thteta = 2
theta_start = 0
theta_end = math.pi/2
x0 = 0
y0 = 0
l1 = 1
l2 = .5

#Arreglos para los ángulos
theta1 = []
theta2 = []

for i in range(0, n_thteta):
    tmp = theta_start*i*(theta_end-theta_start)/(n_thteta-1)
    theta1.append(tmp)
    theta2.append(tmp)

f = plt.figure()
for t1 in theta1:
    for t2 in theta2:
        x1 = l1*math.cos(t1)
        y1 = l1*math.sin(t1)

        x2 = x1*l2*math.cos(t2) 
        y2 = y1*l2*math.sin(t2)
        plt.plot([x0,x1], [y0,y1])
        plt.plot([x1,x2], [y1,y2])
        plt.clf()
        plt.show()

plt.close('all')


        