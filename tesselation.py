import pointmath as pm
import scipy.spatial.qhull as q
import math


#this is just for show
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt

class tesselated_sphere:
        
    def __init__(self):
        pointm=50
        self.points=self.make_points(pointm)
        self.tesselation()
        self.fix_seams()
        
    def replicate_points(self,points):
        """this function is meant to replicate seed points around the
        2pi pi sphere, so that the voronoi tesselation has something 
        to work with and the pattern maps smoothly around the sphere"""
        
        self.newpointdict={}
        
        newpoints=[]
                
        x=-1
        y=-1
        m=2
        pc=-1
        while x < m and y < m:
            #skip the middle
            if x==y==0:
                x+=1
                continue
            for p in points:
                nx= p[0]+ x*2*math.pi
                ny= p[1]+ y * math.pi
                
                #mirror them
                if y!=0:
                    nx= 2*math.pi -nx
                    ny= math.pi - ny
                
                #these are the limits being applied to the coordinates
                if  -1/2*math.pi < nx < 5/2*math.pi and -1/2*math.pi <ny< 3/2*math.pi and not ( 0 < nx < math.pi*2 and 0 < ny < math.pi):
                    #there should be a dict where I save these in...
                    #if pc not in self.newpointdict:
                    #put the new index of the generated point into the dict
                    ind=self.points.index(p)
                    #self.points[ind]==p
                    np=(nx,ny)
                    newpoints.append(np)
                    add=[np]
                    if ind not in self.newpointdict:
                        
                        self.newpointdict[ind]=add
                    else:
                        self.newpointdict[ind]+=add
            
            if x == y == m:
                break
                
            x+=1
            if x==m:
                x=-1
                y+=1
        retp=newpoints
        
        return retp
        
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
        

    def outside(self,vert):
        
        hor= 0 < vert[0] < math.pi*2
        vertic =  0 < vert[1] < math.pi
        
        if not hor or not vertic:
            return True
        else:
            return False
            

    def tesselation(self):
        """
        creates the tesselation, the dict of incomplete regions and
        the seed points needed to create the tesselation as attributes of
        the sphere object
        
        sphere.vor
        sphere.incomplete
        sphere.points
        """
        points=self.points
        vor=q.Voronoi(points)
        self.incomplete={}
        
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
                self.incomplete[seedp]=region
            for vert in region:
                if self.outside(vor.vertices[vert]):
                    self.incomplete[seedp]=region
                    
        #duplicating some seeds
        dupseeds=[]
        for key in self.incomplete:
            dupseeds.append(points[key])
        
        newpoints=self.replicate_points(dupseeds)
        points=points+newpoints
        #run again
        vor=q.Voronoi(points)
        self.vor=vor
        self.points=points
        self.mercatorvor=vor
        self.mercatorpoints=points
        
        
        return vor,
    def visualize_seam_fix(self):
        
        vor=self.vor
        points=self.points
        incomplete=self.incomplete
        
        voronoi_plot_2d(vor)
        #vertical
        plt.plot([0,0],[-math.pi,2*math.pi],"r")
        plt.plot([math.pi*2,math.pi*2],[-math.pi,2*math.pi],"r")
        #horizontal
        plt.plot([-math.pi*2,math.pi*4],[0,0],"r")
        plt.plot([-math.pi*2,math.pi*4],[math.pi,math.pi],"r")
        
        c=0
        for spoint in self.mark_regions:
            point=points[spoint]
            plt.text(point[0],point[1],str(c))
            plt.plot(point[0],point[1],"ro")
            c+=1
            
        for p in self.newcell:
            v=vor.vertices[p]
            plt.plot(v[0],v[1],"bo")
        #duplicated points are in red, lines mark 0, 2pi for x 
        #and 0 and pi for y
        plt.savefig("tesselationtest2.jpg")
        
    def test_visualize(self):
        vor=self.mercatorvor
        points=self.mercatorpoints
        incomplete=self.incomplete
        
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
        
    def fix_seams(self):
        #this should contain the regions...
        #ok, so I need to warp around the mirror
        rel_regions={}
        
        c=0
        m=len(self.vor.point_region)-1
        #find ALL bad regions
        while c < m:
            
            c+=1
            seedp=c
            regionid = self.vor.point_region[c]
            region = self.vor.regions[regionid]
        
            okps=[]
            notokps=[]
            replacement_points=[]
            for point in region:
                cord=self.vor.vertices[point]
                
                if cord[0] < 0 or cord[1] < 0:
                    #this is a point I need to wrap around...
                    #it disqualifies this seedpoint and thus the region.
                    notokps.append(point)
                    
                elif cord[0]>math.pi*2 or cord[1]>math.pi:
                    #this is list of points that others need to be replace WITH
                    replacement_points.append(point)
                    
                else:
                    #this point is ok.
                    okps.append(point)
                    
            if notokps ==[] and replacement_points==[]:
                # this one is completely insde
                continue 
            #if okps==[] and replacement_points==[]:
            #    #this one is completely outside, just the seed point though.
            #    continue
                
            #means by this point, I have a region that is a problem.
            
            correct_seed=False
            if notokps==[] and okps!=[] and replacement_points!=[]:
                a=1
            
            rel_regions.update({seedp:[regionid,notokps,okps,replacement_points,]})
        
        
        self.mark_regions=rel_regions
        hurr=[]
        nnpd={}
        for p in rel_regions:
            if p in self.newpointdict:
                nnpd.update({p:[]})
                hurr.append(p)
                
                for po in self.newpointdict[p]:
                    ind=self.points.index(po)
                    hurr.append(ind)
                    nnpd[p].append(ind)
                
        self.mark_regions=hurr
        self.newpointdict=nnpd
        
        
        #there should be a seedpoint in incomplete that is not in the badregions.
        #the region for this seedpoint is the one we're going to use to wrap around.
        self.mark_regions=[]
        self.newcell=[]
        newregions=[]
        for orgp in self.newpointdict:
            
            m=self.newpointdict[orgp]
            right_point=None
            seeds=[orgp]
            
            for seed in m:
                seeds.append(seed)
            newcell=[]
            #print(seeds)
            m=len(seeds)
            c=0
            
            while c < m:
                
                seed=seeds[c]
                regionid = self.vor.point_region[seed]
                region = self.vor.regions[regionid]
                for p in region:
                    coord = self.vor.vertices[p]
                    x = coord[0]
                    y = coord[1]
                    
                    if (0 < x < math.pi *2) and (0 < y < math.pi):
                        newcell.append(p)
                c+=1
            self.mark_regions+=seeds
            self.newcell+=newcell
            newregions+=[newcell]
            
        #now the reassign the indices and throw away everything else
        
        #first only carry over the verts I'm using...
        newverts=[]
        remap={}
        c=0
        m=len(self.newcell)
        while c < m:
            #the index
            v=self.newcell[c]
            vcord=self.vor.vertices[v]
            if v not in self.newcell:
                c+=1
                continue
            newverts.append(vcord)
            remap.update({v:len(newverts)-1})
        self.newverts=newverts
        
        #now go through all regions and switch out the indices
        c=0
        m=len(newregions)
        while c < m:
            r=newregions[c]
            c2=0
            m2=len(r)
            while c < m2:
                vind=r[c2]
                if vind in remap:
                    r[c2]=remap[vind]
        self.newregions=self.newregions
        
        
        #the final sphere can now be built with 
        #self.newverts
        #and
        #self.newregions
        
def test():
    S=tesselated_sphere()
    S.visualize_seam_fix()
    S.test_visualize()
    print("test complete")
    
if __name__=="__main__":
    test()
