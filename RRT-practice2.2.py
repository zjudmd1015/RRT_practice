#!/usr/bin/python

import math
import random
import numpy as np
import matplotlib.pyplot as mp    # draw plot like MATLAB

import matplotlib.patches as patches
#from scipy.misc import imread
from matplotlib.path import Path

from math import sqrt,cos,sin,atan2
'''
FNAME = "N.map.png"
world = imread(FNAME)
world = np.flipud(world)
Xmax = world.shape[0]
Ymax = world.shape[1]
mp.imshow(world, cmap=mp.cm.binary, interpolation='nearest', origin='lower', extent=[0, Xmax, Ymax])
mp.show()
'''
Xlim = 100  #domain size
Ylim = 100
Qinit = (10,10)
Qgoal = (75,75)
deltaQ = 1
K = 5000

collisions =[]
collisions.append((20,20))
collisions.append((30,32))
collisions.append((60,55))
collisions.append((90,82))
collisions.append((20,70))
collisions.append((60,30))

R_colli = []
R_colli.append(8)
R_colli.append(10)
R_colli.append(6)
R_colli.append(7)
R_colli.append(28)
R_colli.append(12)


def dist(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def create_qrand():
    qrand = random.random()*Xlim, random.random()*Ylim
    return qrand

def find_near(qrand,gmap):
    qnear = gmap[0]
    for p in gmap:
        if dist(p,qrand) < dist(qnear,qrand):
            qnear = p
    return qnear

def create_qnew(qnear,qrand):
    angle = atan2(qrand[1]-qnear[1],qrand[0]-qnear[0])
    return (qnear[0] + deltaQ*cos(angle), qnear[1] + deltaQ*sin(angle))


##########

def cal_dist_4colli(qnear,qnew,colli):
    cal_1 = abs((qnew[0]-qnear[0])*(colli[1]-qnear[1]) - (qnew[1]-qnear[1])*(colli[0]-qnear[0]))
    cal_2 = sqrt((qnew[0]-qnear[0])*(qnew[0]-qnear[0]) + (qnew[1]-qnear[1])*(qnew[1]-qnear[1]))
    dist_4colli = cal_1/cal_2

    return dist_4colli

def judge_side_4colli(qnear,qnew,colli):
    cal_qnear = (qnew[1]-qnear[1])*(qnear[1]-colli[1])+(qnew[0]-qnear[0])*(qnear[0]-colli[0])
    cal_qnew = (qnew[1]-qnear[1])*(qnew[1]-colli[1])+(qnew[0]-qnear[0])*(qnew[0]-colli[0])
    cal = cal_qnear * cal_qnew
    if ( cal  < 0):
        return False
    else:
        return True


def judge_collision(qnear,qnew):
    flag_colli = False

    for i in range(len(collisions)):
        if (dist(qnear, collisions[i])-deltaQ) > R_colli[i]:
            # if there cannot be collision, then drop it.
            continue
        elif dist(qnew, collisions[i]) <= R_colli[i]:
            flag_colli = True
            break
        elif cal_dist_4colli(qnear,qnew,collisions[i]) <= R_colli[i]:
            if ( judge_side_4colli(qnear,qnew,collisions[i]) == False ):
                # 'false' means different side
                # I suppose this will exactly judge if there is a collision
                flag_colli = True
                break
            else:
                continue
        else:
            flag_colli = False

    return flag_colli

##########
'''
def add_edge(qnear,qnew):
    verts = []
    codes = []
    pass
'''

def main():
    Gmap = [Qinit]
    verts = []
    codes = []

    for i in range(K):
        Qrand = create_qrand()
        Qnear = find_near(Qrand,Gmap)
        Qnew = create_qnew(Qnear, Qrand)

##########
        if ( judge_collision(Qnear,Qnew) ):
            # verify that adding Qnew doen't lead to collision
            continue
##########

        Gmap.append(Qnew)
        verts.append(Qnear)
        verts.append(Qnew)
        codes.append(Path.MOVETO)
        codes.append(Path.LINETO)

        if dist(Qnew, Qgoal) <= deltaQ:
            if ( judge_collision(Qnew,Qgoal) ):
                continue
            else:
                Gmap.append(Qgoal)
                verts.append(Qnew)
                verts.append(Qgoal)
                codes.append(Path.MOVETO)
                codes.append(Path.LINETO)
                print 'times of try: ',i  # times of try
                #print Gmap
                break

        #add_edge(qnear,qnew)

    #print Gmap

    # draw the picture
    fig = mp.figure()
    path = Path(verts, codes)
    patch = patches.PathPatch(path)
    ax = fig.add_subplot(111)
    ax.add_patch(patch)
    ax.set_xlim([0, Xlim])
    ax.set_ylim([0, Ylim])

######
    ax.plot(Qinit[0],Qinit[1],'go')
    ax.text(Qinit[0]-5,Qinit[1]-5,'init',fontsize=25,style='italic',color='green')
    ax.plot(Qgoal[0],Qgoal[1],'ro')
    ax.text(Qgoal[0]+1,Qgoal[1]+1,'goal',fontsize=25,style='italic',color='red')

    for i in range(len(collisions)):
        collision_cir = patches.Circle(xy =( collisions[i][0],collisions[i][1]), radius = R_colli[i] ,alpha = 0.6,color='grey')
        ax.add_patch(collision_cir)

    son_index = verts.index(Qgoal)
    parent_index = son_index - 1
    move_path = [Qgoal]
    move_path.append(verts[parent_index])
    codes_move_path = [Path.MOVETO]
    codes_move_path.append(Path.LINETO)
    #parent_find = move_path[-1]
    while parent_index != 0:
        son_index = verts.index(verts[parent_index])
        parent_index = son_index - 1
        move_path.append(verts[son_index])
        move_path.append(verts[parent_index])
        codes_move_path.append(Path.MOVETO)
        codes_move_path.append(Path.LINETO)

    path_2 = Path(move_path, codes_move_path)
    patch_2 = patches.PathPatch(path_2,color = 'purple',linewidth = 3)
    ax.add_patch(patch_2)

    #print len(Gmap)
    #print len(verts)
    #print tt
    #print Gmap
    #print "######"
    #print verts

######
    mp.grid(True)
    mp.axis('equal')
    #mp.axis([0,100,0,100])
    mp.show()
    return Gmap


if __name__ == '__main__':
    main()





