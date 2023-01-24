# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 22:00:03 2023

@author: 15413
"""
import numpy as np

Node = []
Elem = []
Bedge = []
Iedge = []

for line in open('Nodec.txt', 'r'):
    N = line.strip().split()
    N[0] = float(N[0])
    N[1] = float(N[1])
    Node.append(N)
    
for line in open('NE.txt', 'r'):
    E = line.strip().split()
    E[0] = int(E[0])
    E[1] = int(E[1])
    E[2] = int(E[2])
    Elem.append(E)    
    
for line in open('IE.txt', 'r'):
    I = line.strip().split()
    Iedge.append(I)    
    
for line in open('BE.txt', 'r'):
    B = line.strip().split()
    Bedge.append(B)    

def lenth(P1,P2):
    L = np.sqrt((P2[0]-P1[0])**2+(P2[1]-P1[1])**2)
    return L

def norm(P1,P2):
    K = [P1[1]-P2[1],P2[0]-P1[0]]
    norm = K/lenth(P1,P2)
    return norm 

def get_area(P1,P2,P3):
    x1 = P1[0]
    x2 = P2[0]
    x3 = P3[0]
    y1 = P1[1]
    y2 = P2[1]
    y3 = P3[1]
    Area = 0.5 * abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))
    return Area

In=[]
for i in range(len(Iedge)):
    P1 = Node[int(Iedge[i][0])-1]
    P2 = Node[int(Iedge[i][1])-1]
    n = norm(P1,P2)
    In.append(n)

Bn=[]
for i in range(len(Bedge)):
    P1 = Node[int(Bedge[i][0])-1]
    P2 = Node[int(Bedge[i][1])-1]
    n = norm(P2,P1)
    Bn.append(n)
    

Area=[]
for i in range(len(Elem)):
    P1 = Node[Elem[i][0]-1]
    P2 = Node[Elem[i][1]-1]
    P3 = Node[Elem[i][2]-1]
    A = get_area(P1,P2,P3)
    Area.append(A)
      
  