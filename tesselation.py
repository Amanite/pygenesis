import pointmath as pm
import scipy.spatial.qhull as q
import math


#this is just for show
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt

def replicate_points(points):
    """this function is meant to replicate seed points around the
    2pi pi sphere, so that the voronoi tesselation has something 
    to work with and the pattern maps smoothly around the sphere"""
    newpoints=[]
    x=-1
    y=-1
    m=2
    while x < m and y < m:
        #skip the middle
        if x==y==0:
            x+=1
            continue
        for p in points:
            nx=p[0]+ x*2*math.pi
            ny=p[1]+ y * math.pi
            #these are the limits being applied to the coordinates
            if  -1/2*math.pi < nx < 5/2*math.pi and -1/2*math.pi <ny< 3/2*math.pi:
                newpoints.append((nx,ny))
        
        if x == y == m:
            break
            
        x+=1
        if x==m:
            x=-1
            y+=1
    retp=newpoints
    return retp
    
def make_points(pointm=50):
    #this creates  points in angle format
    c=0
    
    points=[]
    while c < pointm:
        
        points.append(pm.rand_surface_point())
        c+=1

    #we have to repeat the point patter for proper interaction

    #although this is pretty 
    newpoints=replicate_points(points)
    retp=points#+newpoints        
    return retp
    

def outside(vert):
    
    hor= 0 < vert[0] < math.pi*2
    vertic =  0 < vert[1] < math.pi
    
    if not hor or not vertic:
        return True
    else:
        return False
        

def tesselation(pointm=50):
    
    points=make_points(pointm)
    vor=q.Voronoi(points)
    incomplete={}
    
    #ok this loops through the cells...
    c=0
    m=len(vor.point_region)-1
    while c < m:
        c+=1
        seedp=c
        regionid=vor.point_region[c]
        region = vor.regions[regionid]
        #if the point ends either in infinity or on the second round around the
        #sphere, it needs a counter point on the other side.
        #so the pattern is incomplete right now.
        if -1 in region:
            incomplete[seedp]=region
        for vert in region:
            if outside(vor.vertices[vert]):
                incomplete[seedp]=region
                
    #duplicating some seeds
    dupseeds=[]
    for key in incomplete:
        dupseeds.append(points[key])
    newpoints=replicate_points(dupseeds)
    points=points+newpoints
    #run again
    vor=q.Voronoi(points)
    return vor,points,incomplete
    
def test_visualize(vor,points,incomplete):
    voronoi_plot_2d(vor)
    #vertical
    plt.plot([0,0],[-math.pi,2*math.pi],"r")
    plt.plot([math.pi*2,math.pi*2],[-math.pi,2*math.pi],"r")
    #horizontal
    plt.plot([-math.pi*2,math.pi*4],[0,0],"r")
    plt.plot([-math.pi*2,math.pi*4],[math.pi,math.pi],"r")
    
    c=0
    for spoint in incomplete:
        point=points[spoint]
        plt.text(point[0],point[1],str(c))
        plt.plot(point[0],point[1],"ro")
        c+=1
    
    #duplicated points are in red, lines mark 0, 2pi for x 
    #and 0 and pi for y
    plt.savefig("tesselationtest.jpg")
    
def test():
    tup=tesselation()
    test_visualize(*tup)
    print("test complete")
    
if __name__=="__main__":
    test()
