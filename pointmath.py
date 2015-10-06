#http://mathproofs.blogspot.de/2005/04/uniform-random-distribution-on-sphere.html

import random
import math

def rand_surface_point():
    
    r1=random.random()
    r2=random.random()
    angle1= r1 * 2 * math.pi
    angle2= math.acos( 1 - 2* r2)
    
    #angle one is sideways, our x
    #angle two is updown, our y
    
    return angle1,angle2
    
def to_xyz(angle1,angle2,r=1):
    
    a1,a2=rand_surface_point()
    
    #for a different radius just multiply all of these by r
    x=r*math.sin(a1)*math.sin(a2)
    y=r*math.cos(a1)*math.sin(a2)
    z=r*math.cos(a2)
    
    return (x,y,z)
    
    
def distance(a, b):
    ax, ay = a
    bx, by = b
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
