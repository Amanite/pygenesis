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
    
    #for a different radius just multiply all of these by r
    x=r*math.sin(angle1)*math.sin(angle2)
    y=r*math.cos(angle1)*math.sin(angle2)
    z=r*math.cos(angle2)
    
    return (x,y,z)
    
def distance(a, b):
    ax, ay = a
    bx, by = b
    result = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
    if result > math.pi:
        return math.fabs(result -(2*math.pi))
    else:
        return result
