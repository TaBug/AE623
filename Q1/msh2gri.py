# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 20:47:46 2023

@author: liton
"""


def msh2gri(fnameInput, fnameOutput):
    # input file
    with open(fnameInput, "r") as f:
        lines = f.readlines()

    # output .gri file
    with open(fnameOutput, "w") as f:
        iEntities = lines.index('$Entities\n')
        numPoints, numCurves, numSurfaces, numVolumes = map(int, lines[iEntities + 1].strip().split())
        print(numPoints, numCurves, numSurfaces, numVolumes)
        iNodes = lines.index('$Nodes\n')
        numEntityBlocks, numNodes, minNodeTag, maxNodeTag = map(int, lines[iNodes + 1].strip().split())
        index = iNodes + 2
        for i in range(numPoints + numCurves + numSurfaces):
            entityDim, entityTag, parametric, numNodesInBlock = map(int, lines[index].strip().split())
            index += numNodesInBlock
            for j in range(numNodesInBlock):
                index += 1
                x, y, z = map(float, lines[index].strip().split())
                f.write(f"{x} {y}\n")
            index += 1

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

            x = int(x);
            y = int(y);
            z = int(z)
            f.write(f"{x} {y} {z}\n")


if __name__ == "__main__":
    msh2gri('../Q1/all.msh', 'all.gri')
