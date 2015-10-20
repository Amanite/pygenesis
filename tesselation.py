import pointmath as pm
import scipy.spatial.qhull as q
import math
import random

#this is just for show
from scipy.spatial import voronoi_plot_2d

class tesselated_sphere:
    
    #principle behind the tesselation:
    
    #get random points on a sphere
    
    #create 2 new points for every seed, one slightly outside
    #one slightly inside the sphere, but both on the same line from 
    #the origin
    
    #use the tesselation
    
    #the result is that the boundary surface between the regions inside
    #and outside the sphere describe the sphere surface in voronoi
    #cells.
    
    #just throw away all verts that are not near the surface and all
    #that's left of the cells should be the parts of the regions
    #that describe the surface.
    
    #voila, voronoi sphere
    
    
    def __init__(self, iterations = 2, pointm = 500):
        #there are some issues with radius probably...
        
        #create angle coordinate points on a sphere
        self.points = self.make_points(pointm)
        
        #angle to xyz for the list
        points = self.convert(self.points)
        
        c=0
        while c < iterations:
            #replicate the pattern
            self.verts = []
            self.regions = []
            points = self.replicate(points)
            points = self.tesselation(points)
            c+=1
        
    def tesselation(self,ps):
        
        V = q.Voronoi(ps)
        verts = V.vertices
        regions = V.regions
        
        newregions = []
        newverts = []
        for region in regions:
            newregion = []
            if -1 in region:
                continue
            stop=False
            for ind in region:
                x,y,z = verts[ind]
                if not 0.85 < math.sqrt( x**2 + y**2 + z**2 ) < 1.15:
                    #keep this one around
                    a=1
                else:
                    p=(x,y,z)
                    
                    if p not in newverts:
                        newverts.append( p )
                        ind=newverts.index( p )
                        
                        newregion.append( ind )
                    else:
                        if p not in newregion:
                            ind=newverts.index( p )
                            newregion.append( ind )
                            
            if newregion!=[]:
                newregions.append(newregion)
            else:
                a=1
                
                #use the newly created region
        
        self.verts=newverts
        self.regions=newregions
        
        #this recreates seeds from the average points of the polygons
        #resulting in llods relaxation
        
        medians=[]
        for region in self.regions:
            m=[0,0,0]
            c=0
            for vert in region:
                coord = self.verts[vert]
                m[0]+=coord[0]
                m[1]+=coord[1]
                m[2]+=coord[2]
                c+=1
            m[0]=m[0]/c
            m[1]=m[1]/c
            m[2]=m[2]/c
            l=math.sqrt(m[0]**2 + m[1]**2 + m[2]**2)
            m[0]=m[0]*(1/l)
            m[1]=m[1]*(1/l)
            m[2]=m[2]*(1/l)
            medians.append(m)
        return medians
        
    def convert(self,ps):
        newps=[]
        for p in ps:
            newps.append(pm.to_xyz(p[0],p[1]))
        return newps
        
    def replicate(self,points):
        
        newpoints=[]
        for p in points:
            
            d=0.1
            d1=1-d
            p1 = (p[0]*d1, p[1]*d1, p[2]*d1)
            d2=1+d
            p2 = (p[0]*d2, p[1]*d2, p[2]*d2)
            newpoints.append(p1)
            newpoints.append(p2)
        return newpoints
        
    def make_points(self,pointm=50):
        #this creates  points in angle format
        c=0
        points=[]
        while c < pointm:
            points.append(pm.rand_surface_point())
            c+=1
        #we have to repeat the point patter for proper interaction
        retp=points
        return retp
    
    

def test():
    S=tesselated_sphere()
    
if __name__=="__main__":
    test()
