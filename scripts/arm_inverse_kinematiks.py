import math
import numpy
import cmath
def ikine_brazo(xm, ym, zm, phi=0):
    l1 = 0
    l2 = 2.6
    l3 = 2.6
    l4 = .9
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
    q1 = qlimit([-90,90],q1)
    #Para q2     
    hip=math.sqrt(xm**2+(zm-l1)**2)
    phi = math.atan2(zm-l1, xm)
    beta=cmath.acos((-l3**2+l2**2+hip**2)/(2*l2*hip))
    Q2=numpy.real(phi+beta)
    q2=numpy.rad2deg(Q2)
    q2 = qlimit([0,157,q2)
    #Para q3           
    gamma=cmath.acos((l2**2+l3**2-hip**2)/(2*l2*l3))
    Q3=numpy.real(gamma-math.pi)
    q3=numpy.rad2deg(Q3)
    q3 = qlimit([-165,0],q3)
    # Para q4
    q4 = phi - q2 -q3-phi                
    q4 = qlimit(-90,90,q4)
    print(q1,q2,q3,q4)
    acum = math.radians(q2)
    x2 = l2*math.cos(acum) 
    y2 = l2*math.sin(acum)        
    acum+=math.radians(q3)
    x3 = x2+l3*math.cos(acum)
    y3 = y2+l3*math.sin(acum)
    acum+=math.radians(q4)
    x4 = x3+l4*math.cos(acum)
    y4 = y3+l4*math.sin(acum)
    if(y4 > self.limit_z and (x4 > self.limit_chassis or y4 >= 0)):
        print("jala")
    else:
        print("no jala")

def qlimit(self, l, val):
    if (val < l[0]):
        return l[0]
    if (val > l[1]):
        return l[1]
    return val   

ikine_brazo(4.2,0,2)