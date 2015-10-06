import pointmath as pm
import scipy.spatial.qhull as q
import math


#this is just for show
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt


def make_points(pointm=50):
    #this creates  points in angle format
    c=0
    
    points=[]
    while c < pointm:
        
        points.append(pm.rand_surface_point())
        c+=1

    #we have to repeat the point patter for proper interaction

    #although this is pretty 
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
            newpoints.append((p[0]+ x*2*math.pi , p[1]+ y * math.pi))
        
        if x == y == m:
            break
            
        x+=1
        if x==m:
            x=-1
            y+=1
    retp=points+newpoints        
    return retp

def find_original_point(vor,pointm):
    
    #to find the duplicates we use vor.point_region
    c=0
    while c < pointm:
        r=vor.regions[c]
    #for p in vor.point_region:
    #    #print(p)
    #    if p > pointm: #this is a point we added
    #        continue
        
        #r=vor.regions[p]#this is a region on our sphere
        
        #now we have to see if the coordinates of a vertex are outside
        #angular spherical coords
        
        vertices=vor.vertices
        for v_ind in r:
            
            vert = vertices[v_ind]
            #print(vert)
            
            x_org=None
            y_org=None
            #if any onf these are true this point is not on our sphere
            #but it has a proper original on our sphere...
            if vert[0] > math.pi*2:
                x_org = vert[0] - math.pi*2
            
            if vert[0] < 0:
                x_org = vert[0] + math.pi*2
                
            if 0 < vert[0] < math.pi*2:
                x_org=vert[0]
                
            if vert[1] > math.pi:
                y_org = vert[1] - math.pi
            if vert[1] < 0:
                y_org = vert[1] + math.pi
            if 0 < vert[1] < math.pi:
                y_org = vert[1]
                
            if x_org==vert[0] and y_org==vert[1]:
                continue
            
            org_p=[x_org,y_org]
            
            #print(org_p)
            
            #we now have coordinates for our original point.
            #can we just find it?
            
            for p in vor.vertices:
                #print(p,vert,org_p)
                round_to=4
                if ((round(p[0],round_to) != round(vert[0],round_to) and round(p[0],round_to) == round(org_p[0],round_to)) and
                 (round(p[1],round_to) != round(vert[1],round_to) and round(p[1],round_to) == round(org_p[1],round_to)) ):
                    print("these two",vert, p)
                    #return
        c+=1

pointm=50 #this is outside because we need it here
points=make_points(pointm)
vor=q.Voronoi(points)

find_original_point(vor,pointm)
            


voronoi_plot_2d(vor)
plt.savefig("plot.jpg")
#plt.show()
