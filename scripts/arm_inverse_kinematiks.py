import math
import numpy
def ikine_brazo(xm, ym, zm, phi=0):
    l1 = 0
    l2 = 2.1
    l3 = 2.1
    if (xm != 0 or ym != 0 or zm != 0):
        if(xm == 0):
            if(ym>0):
                xm = ym
                Q1 = math.pi/2
            elif ym<0:
                xm = ym
                Q1 = -math.pi/2
            elif ym == 0:
                Q1 = 0
        elif (xm < 0):
            if (ym == 0):
                Q1 = 0
            elif ym<0:
                Q1 = numpy.real(math.atan2(xm, ym))#real
            else:
                Q1 = numpy.real(math.atan2(-xm,-ym))#real
        else:
            Q1 = numpy.real(math.atan2(ym,xm))#real
    #Para q1
    q1=numpy.rad2deg(Q1)
    #Para q2     
    hip=math.sqrt(xm**2+(zm-l1)**2)
    phi = math.atan2(zm-l1, xm)
    beta=math.acos((-l3**2+l2**2+hip**2)/(2*l2*hip))
    Q2=numpy.real(phi+beta)
    q2=numpy.rad2deg(Q2) 
    print(hip, phi, beta, Q2)
    #Para q3            elif ym == 0:

    gamma=math.acos((l2**2+l3**2-hip**2)/(2*l2*l3))
    Q3=numpy.real(gamma-math.pi)
    q3=numpy.rad2deg(Q3)
    # Para q4
    q4 = phi - q2 -q3-phi                
    print(q1,q2,q3,q4)

ikine_brazo(4.2,0,2)