#!/usr/bin/env python

"""Projection.py: Shows that phantom projection calulcations using geometric algebra are ok"""

__author__ = "Radoslaw A. Kycia"
__copyright__ = "2017 R.K."
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Radoslaw A. Kycia"
__email__ = "kycia.radoslaw@gmail.com"
__status__ = "Proof of concept"


from visual import *

def projection( n, a ):
    """Project a vector onto n plane. 
    WARNING: Assume that n = 0,0,n3"""
    al = vector( a.x*n.z/a.z, a.y*n.z/a.z, 0 )
    return(al)

def rotate(vec, alpha):
        """rotate vextor using angle"""
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
O = vector( 1,1,5)  

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
points1O = [vector(0.3,0.3,-0.2),vector(0.3,-0.3,-0.2),vector(-0.3,-0.3,-0.2),vector(-0.3,0.3,-0.2)]
#level 2:
points2O = [vector(0.5,0.5,0.2),vector(0.5,-0.5,0.2),vector(-0.5,-0.5,0.2),vector(-0.5,0.5,0.2)]


#rotate points
points1  = [rotate(x, alpha) for x in points1O]
points2 = [rotate(x, alpha) for x in points2O]

#shift to the origin
points1 = [ O+x for x in points1 ]
points2 = [ O+x for x in points2 ]



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
phantom1 = map(lambda x:sphere(pos=x, radius=radius1, color=color.black), points1 )
#map(lambda x:arrow(pos=(0,0,0),axis = x, color=color.black, shaftwidth=0.1), points1 )

phantom2 = map(lambda x:sphere(pos=x, radius=radius1, color=color.black), points2 )
#map(lambda x:arrow(pos=(0,0,0),axis = x, color=color.black, shaftwidth=0.1), points2 )


#calculate projected points
pointsP1  = [ projection(N,x) + N for x in points1]
pointsP2 = [ projection(N,x) + N for x in points2]

#plot projected points
project1 = map(lambda x:sphere(pos=x, radius=radius2, color=color.red), pointsP1 )
#map(lambda x:arrow(pos=(0,0,0),axis = x, shaftwidth=0.01, color=color.red), pointsP1 )

project2 = map(lambda x:sphere(pos=x, radius=radius2, color=color.red), pointsP2 )
#map(lambda x:arrow(pos=(0,0,0),axis = x, shaftwidth=0.01, color=color.red), pointsP2 )

drawE(N-(0,0,0.1), e1, e2, (0,0,0))



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
        print("alpha[deg] = ", angleDeg)
    if movement=='down':
        angleDeg -= 5.0
        print("alpha[deg] = ", angleDeg)


    alpha = angleDeg * math.pi/180.0
    points1  = [rotate(x, alpha) for x in points1O]
    points2 = [rotate(x, alpha) for x in points2O]

    #shift to the origin
    points1 = [ O+x for x in points1 ]
    points2 = [ O+x for x in points2 ]


    for i in range(len(points1)):
        phantom1[i].pos = points1[i]
    
    for i in range(len(points2)):
        phantom2[i].pos = points2[i]
        

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
    pointsP2 = [ projection(N,x) + N for x in points2]

    for i in range(len(pointsP1)):
        project1[i].pos = pointsP1[i]

    for i in range(len(pointsP2)):
        project2[i].pos = pointsP2[i]
