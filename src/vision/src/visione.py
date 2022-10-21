#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely import affinity
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
import os
ANGOLO_X=10
ANGOLO_Y= 10

def carica_macchina():
    location_macchina = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file_macchina = open(os.path.join(location_macchina, 'posizione_macchina.txt'))
    line_x = file_macchina.readline()
    line_y = file_macchina.readline()
    line_angolo = file_macchina.readline()
    pos= Point(int(line_x), int(line_y))
    angolo = int(line_angolo)
    x_macchina = [int(line_x)]
    y_macchina = [int(line_y)]
    plt.plot(x_macchina, y_macchina, marker="p", markersize=13, markeredgecolor="blue", markerfacecolor="black")
    return pos, angolo
    file_macchina.close()



def cv(landmarks, pos, angolo): #funzione che controlla se un cono si trova all'interno del triangolo di visione 
    vertice_alto_sinistra = Point (pos.x-ANGOLO_X, pos.y+ANGOLO_Y)
    vertice_alto_destra = Point (pos.x+ANGOLO_X, pos.y+ANGOLO_Y)
    triangolo = Polygon([[p.x, p.y] for p in [pos, vertice_alto_sinistra, vertice_alto_destra]]) #i punti del poligono vano messi in ordine in cui va disegnato
    triangolo_ruotato= affinity.rotate(triangolo, angolo, pos)  #l'angolo di rotazione ruota in senso antiorario
    print("Coordinate triangolo:", triangolo.boundary,"\n")
    print("Coordinate triangolo ruotato:",triangolo_ruotato.boundary, "\n")
    x, y = triangolo_ruotato.exterior.xy
    plt.plot(x, y, c="red")
    print("Vedo i coni in posizione:\n")
    for x in range(len(landmarks)):
        if triangolo_ruotato.contains(landmarks[x]) :
            print(landmarks[x], "\n")


def carica_file(lista): #funzione per caricare dal file la lista dei coni
    location_coni = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file_coni = open(os.path.join(location_coni, 'posizione_coni.txt'))
    for line in file_coni:
        line2 = file_coni.readline()
        cono = Point(int(line), int(line2))
        lista.append(cono)
        x_cono = [int(line)]
        y_cono = [int(line2)]
        
        plt.plot(x_cono, y_cono, marker="o", markersize=13, markeredgecolor="red", markerfacecolor="yellow")
        if 'str' in line:
            break
    file_coni.close()

def pose_publisher(coni, posizione_macchina, orientamento_macchina):
    cv(coni, posizione_macchina, orientamento_macchina)
    rilevati = posizione_macchina.x
    print("Posizione macchina:",posizione_macchina, "Orientamento macchina:",orientamento_macchina,"\n")
    pub = rospy.Publisher('coni', Float32, queue_size=10)
    rospy.init_node('cv_sim', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    pub.publish(rilevati)
    rate.sleep()
    


##MAIN##
if __name__ == '__main__':
    coni = []
    posizione_macchina, orientamento_macchina = carica_macchina ()
    carica_file(coni)
    pose_publisher(coni, posizione_macchina, orientamento_macchina)
    plt.xlim(0, 25)
    plt.ylim(0, 25)
    plt.grid()
    plt.show()

