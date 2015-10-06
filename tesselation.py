import pointmath as pm
import scipy.spatial.qhull as q

#this is just for show
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt


#this creates a hundred points in angle format
c=0
m=100
points=[]
while c < 100:
    
    points.append(pm.rand_surface_point())
    c+=1

#we can simply plug those in and get a 2d tesselation
vor=q.Voronoi(points)


#this is also just for show
voronoi_plot_2d(vor)
plt.show()
