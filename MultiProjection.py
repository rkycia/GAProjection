#!/usr/bin/env python

"""MultiProjection.py: Shows that phantom projection calulcations using geometric algebra are ok"""

__author__ = "Radoslaw A. Kycia"
__copyright__ = "2017 R.K."
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Radoslaw A. Kycia"
__email__ = "kycia.radoslaw@gmail.com"
__status__ = "Proof of concept"


from visual import *

def projection( n, a ):
    """Project a vector onto n plane. """
    AN = dot(a,n)    
    NN = dot(n,n)
    al = (a*NN-n*AN)/AN
    return(al)

def rotate(vec, alpha):
        """rotate vextor using angle in the plane YZ"""
        x = vec.x 
        y = cos(alpha) * vec.y + sin(alpha) * vec.z
        z = -sin(alpha) * vec.y + cos(alpha) * vec.z
        return( vector(x,y,z))        

#draw axes
def drawE( pos, e1, e2, e3, color = color.blue, lab = true ):
    """Draw axes e1, e2, e3"""
    e1p = arrow(pos=pos, axis=e1, color=color)    
    e2p = arrow(pos=pos, axis=e2, color=color)
    e3p = arrow(pos=pos, axis=e3, color=color)
    if( lab ):
        label(pos=pos+e1, text = "e1")
        label(pos=pos+e2, text = "e2")
        label(pos=pos+e3, text = "e3")
    return([e1p,e2p,e3p])    

#scene setup
scene.forward = (0,0,1)
scene.background=(0.5,0.5,0.5)
lamp = local_light(pos=(0,0,0), color=color.yellow)
scene.lights = [vector(0,0,-1)]

#center of the phantom
O = vector( 0,0,5)  

#angle of rotation
angleDeg = 0.0 #deg
alpha = angleDeg * math.pi/180.0 #radians

#normal vector defining plane
N = vector(0,0,10)

#draw axes
e1 = vector(1,0,0)
e2 = vector(0,1,0)
e3 = vector(0,0,1)

Ebase = drawE(O, e1, e2, e3, lab = false)

#points in phantom with respect to O
##level 1:
points1O = [vector(0,0.3,-0.2), vector(0,0,0),vector(0.3,0.3,-0.2),vector(-0.3,0.3,-0.2)]
points2O = [vector(0,-0.3,-0.2),vector(0.3,-0.3,-0.2),vector(-0.3,-0.3,-0.2),vector(-0.3,-0.3,-0.2)]
points3O = [vector(0,-0.3,0.2),vector(0.3,-0.3,0.2),vector(-0.3,-0.3,0.2)]
points4O = [vector(0,0.3,0.2),vector(0.3,0.3,0.2),vector(-0.3,0.3,0.2)]

colors = [color.red, color.green, color.blue, color.yellow]


#rotate points
points1  = [rotate(x, alpha) for x in points1O]
points2  = [rotate(x, alpha) for x in points2O]
points3  = [rotate(x, alpha) for x in points3O]
points4  = [rotate(x, alpha) for x in points4O]

#shift to the origin
points1 = [ O+x for x in points1 ]
points2 = [ O+x for x in points2 ]
points3 = [ O+x for x in points3 ]
points4 = [ O+x for x in points4 ]

#radius of phantom points
radius1 = 0.1
#radius of projected points
radius2 = 0.2

#source ball
Z = sphere(pos=(0,0,0),radius=radius1, color=color.yellow)
label(pos = (0,0,0), text = "source")
#vector defining of plane
#zn = arrow(pos=(0,0,0),axis = N, color = color.yellow, shaftwidth=0.1)


Epbase = drawE(O, rotate(e1,alpha), rotate(e2,alpha), rotate(e3,alpha), color.yellow, lab = false)

#plot points of phantom:
phantom1 = map(lambda x:sphere(pos=x, radius=radius1, color=colors[0]), points1 )
phantom2 = map(lambda x:sphere(pos=x, radius=radius1, color=colors[1]), points2 )
phantom3 = map(lambda x:sphere(pos=x, radius=radius1, color=colors[2]), points3 )
phantom4 = map(lambda x:sphere(pos=x, radius=radius1, color=colors[3]), points4 )

#calculate projected points
pointsP1  = [ projection(N,x) + N for x in points1]
pointsP2  = [ projection(N,x) + N for x in points2]
pointsP3  = [ projection(N,x) + N for x in points3]
pointsP4  = [ projection(N,x) + N for x in points4]


#plot projected points
project1 = map(lambda x:sphere(pos=x, radius=radius2, color=colors[0]), pointsP1 )
project2 = map(lambda x:sphere(pos=x, radius=radius2, color=colors[1]), pointsP2 )
project3 = map(lambda x:sphere(pos=x, radius=radius2, color=colors[2]), pointsP3 )
project4 = map(lambda x:sphere(pos=x, radius=radius2, color=colors[3]), pointsP4 )


drawE(N-(0,0,0.1), e1, e2, (0,0,0), lab=false)

cube = box(pos=O, axis=e2, length=1,height=1, width=1,color=color.red, opacity=0.4, material = materials.diffuse) 


#plane of projection
plane = box(pos=N,axis=(1,1,0),length=10,height=10, width=0.1)
label( pos = N-(5,5,0.1), text = "projection plane")


####key support
print("up,down - angle alpha; \n left,right translation of phantom origin")

while(1):
    movement=scene.kb.getkey()
    if movement=='right':
        print("right")
        O = O - 0.1*vector(1,1,0)
        print("O = ", O)
    if movement=='left':
        print("left")
        O = O + 0.1*vector(1,1,0)
        print("O = ", O)
    if movement=='up':
        angleDeg += 5.0
        angleDeg %= 360
        print("alpha[deg] = ", angleDeg)
    if movement=='down':
        angleDeg -= 5.0
        angleDeg %= 360
        print("alpha[deg] = ", angleDeg)


    alpha = angleDeg * math.pi/180.0
    points1  = [rotate(x, alpha) for x in points1O]
    points2  = [rotate(x, alpha) for x in points2O]
    points3  = [rotate(x, alpha) for x in points3O]
    points4  = [rotate(x, alpha) for x in points4O]

    #shift to the origin
    points1 = [ O+x for x in points1 ]
    points2 = [ O+x for x in points2 ]
    points3 = [ O+x for x in points3 ]
    points4 = [ O+x for x in points4 ]


    for i in range(len(points1)):
        phantom1[i].pos = points1[i]
    
    for i in range(len(points2)):
        phantom2[i].pos = points2[i]
    
    for i in range(len(points3)):
        phantom3[i].pos = points3[i]
    
    for i in range(len(points4)):
        phantom4[i].pos = points4[i]
    

    Epbase[0].axis = rotate(e1,alpha) 
    Epbase[0].pos = O
    Epbase[1].axis = rotate(e2,alpha)
    Epbase[1].pos = O
    Epbase[2].axis = rotate(e3,alpha)    
    Epbase[2].pos = O
    
    Ebase[0].pos = O
    Ebase[1].pos = O
    Ebase[2].pos = O

    #calculate projected points
    pointsP1  = [ projection(N,x) + N for x in points1]
    pointsP2  = [ projection(N,x) + N for x in points2]
    pointsP3  = [ projection(N,x) + N for x in points3]
    pointsP4  = [ projection(N,x) + N for x in points4]

    for i in range(len(pointsP1)):
        project1[i].pos = pointsP1[i]

    for i in range(len(pointsP2)):
        project2[i].pos = pointsP2[i]
    
    for i in range(len(pointsP3)):
        project3[i].pos = pointsP3[i]
    
    for i in range(len(pointsP4)):
        project4[i].pos = pointsP4[i]


    cube.pos = O
    cube.axis = rotate(e2,alpha)
