# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 20:47:46 2023

@author: liton
"""
# input file
with open("message.txt", "r") as f:
    lines = f.readlines()
with open("nodes.txt", "r") as f:
    nodes = f.readlines()

# output .gri file
with open("assem.gri", "w") as f:
    # nNode nElemTot Dim
    f.write(f"712 1288 2\n")
    
    # x y z coordinates
    for i, line in enumerate(lines):
        x, y, trash1, trash2 = map(float, line.strip().split())
        f.write(f"{x} {y}\n")
        
    # Boundaries
    f.write(f"4\n")
    f.write(f"1 2 Bottom\n")
    f.write(f"121 122\n")
    f.write(f"1 2 Right\n")
    f.write(f"122 123\n")
    f.write(f"1 2 Top\n")
    f.write(f"123 124\n")
    f.write(f"1 2 Left\n")
    f.write(f"124 121\n")
    
    # Node to Elements
    f.write(f"1288 1 TriLagrange\n")
    for i, line in enumerate(nodes):
        x, y, z, trash2 = map(float, line.strip().split())
        
        x = int(x);y=int(y);z=int(z)
        f.write(f"{x} {y} {z}\n")
