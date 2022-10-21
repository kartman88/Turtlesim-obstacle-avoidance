#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from vision.msg import point
from vision.msg import point_array

import os
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely import affinity
ANGOLO_X=20
ANGOLO_Y= 20

def carica_tracciato(lista): #funzione per caricare dal file la lista dei coni
    location_coni = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file_coni = open(os.path.join(location_coni, 'posizione_coni.txt'))
    for line in file_coni:
        line2 = file_coni.readline()
        cono = Point(int(line), int(line2))
        lista.append(cono)
        if 'str' in line:
            break
    file_coni.close()

def cv(landmarks, pos): #funzione che controlla se un cono si trova all'interno del triangolo di visione 
    vertice_alto_sinistra = Point (pos.x-ANGOLO_X, pos.y+ANGOLO_Y)
    vertice_alto_destra = Point (pos.x+ANGOLO_X, pos.y+ANGOLO_Y)
    triangolo = Polygon([[p.x, p.y] for p in [pos, vertice_alto_sinistra, vertice_alto_destra]]) #i punti del poligono vano messi in ordine in cui va disegnato
    triangolo_ruotato= affinity.rotate(triangolo, pos.theta, (pos.x,pos.y))  #l'angolo di rotazione ruota in senso antiorario
    print("Coordinate triangolo:", triangolo.boundary,"\n")
    print("Coordinate triangolo ruotato:",triangolo_ruotato.boundary, "\n")
    coni = point_array()
    #x, y = triangolo_ruotato.exterior.xy
    print("Vedo i coni in posizione:\n")
    for x in range(len(landmarks)):
        if triangolo_ruotato.contains(landmarks[x]) :
            cono = point()
            cono.x = landmarks[x].x
            cono.y = landmarks[x].y
        coni.cones.append(cono)
    return coni

def callback(car_pose):
    track = [] 
    carica_tracciato(track)
    cone_pub = rospy.Publisher('coni', point_array, queue_size=10)
    lista_coni = point_array()
    lista_coni = cv(track, car_pose) 
    for z in lista_coni.cones:
        print(z.x, z.y)
    cone_pub.publish(lista_coni)

if __name__ == '__main__':
    rospy.init_node('vision', anonymous=True)
    pose_sub = rospy.Subscriber("turtle1/pose", Pose, callback)
    rospy.spin()
    print("Ciao")
