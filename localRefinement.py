import numpy as np
from matricesGenerator import readgri, getI2E, getB2E, edgehash, area


def localRefine(x, y, r, mesh, I2E):
    E = mesh['E']
    V = mesh['V']
    B = mesh['B']
    Ecopy = E.copy()
    Vcopy = V.copy()
    eleFlagged = np.zeros(len(E), dtype=int)
    edgeFlagged = np.zeros(len(I2E), dtype=int)

    # flag the elements that fall in the range
    for iElem, elem in enumerate(E):
        xc = (V[elem[0] - 1][0] + V[elem[1] - 1][0] + V[elem[2] - 1][0]) / 3
        yc = (V[elem[0] - 1][1] + V[elem[1] - 1][1] + V[elem[2] - 1][1]) / 3
        if np.sqrt((xc - x) ** 2 + (yc - y) ** 2) <= r:
            eleFlagged[iElem] += 1

    # flag the faces of the flagged elements
    for iEdge, i2e in enumerate(I2E):
        if eleFlagged[i2e[0] - 1] == 1 or eleFlagged[i2e[2] - 1] == 1:
            edgeFlagged[iEdge] += 1

    # flag the elements that are adjacent to the flagged faces
    # record the local index of the face that is to be refined
    eleRefine = np.zeros([len(E), 3], dtype=int)
    for iEdge, i2e in enumerate(I2E):
        if edgeFlagged[iEdge] == 1:
            elemL = i2e[0]
            faceL = i2e[1]
            elemR = i2e[2]
            faceR = i2e[3]
            eleRefine[elemL - 1][faceL - 1] += 1
            eleRefine[elemR - 1][faceR - 1] += 1

    for iElem, elem in enumerate(eleRefine):
        if sum(elem) == 1:
            index = np.where(elem == 1)[0][0]
            node1 = E[iElem][index]
            node2 = E[iElem][index - 2]
            node3 = E[iElem][index - 1]

            coordNew = np.array([[(V[node3 - 1][0] + V[node2 - 1][0]) / 2, (V[node3 - 1][1] + V[node2 - 1][1]) / 2]])
            Vcopy = np.append(Vcopy, coordNew, axis=0)

            elemNew1 = np.array([[len(Vcopy), node1, node2]])
            elemNew2 = np.array([[len(Vcopy), node3, node1]])
            Ecopy[iElem] = elemNew1
            Ecopy = np.append(Ecopy, elemNew2, axis=0)

        elif sum(elem) == 2:
            index = np.where(elem == 1)[0]
            node1 = E[iElem][index[0]]
            node2 = E[iElem][index[1]]
            node3 = E[iElem][3 - index[0] - index[1]]
            node1c = V[node1 - 1]
            node2c = V[node2 - 1]
            node3c = V[node3 - 1]

            # find the angle of node1
            v1 = node1c - node2c
            v2 = node1c - node3c
            angle1 = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

            # find the angle of node2
            v1 = node2c - node1c
            v2 = node2c - node3c
            angle2 = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

            # find the bigger angle
            if angle1 > angle2:
                nodeBig = node1
                nodeSml = node2
            else:
                nodeBig = node2
                nodeSml = node1

            # create new nodes
            nodeBigc = np.array([[(node3c[0] + V[nodeSml - 1][0]) / 2, (node3c[1] + V[nodeSml - 1][1]) / 2]])
            nodeSmlc = np.array([[(node3c[0] + V[nodeBig - 1][0]) / 2, (node3c[1] + V[nodeBig - 1][1]) / 2]])
            Vcopy = np.append(Vcopy, nodeBigc, axis=0)
            Vcopy = np.append(Vcopy, nodeSmlc, axis=0)

            # create new elements
            elemNew1 = np.array([[len(Vcopy) - 1, nodeSml, nodeBig]])
            elemNew2 = np.array([[len(Vcopy) - 1, nodeBig, len(Vcopy)]])
            elemNew3 = np.array([[len(Vcopy) - 1, len(Vcopy), node3]])

            # add to the new E matrix
            Ecopy = np.append(Ecopy, elemNew1, axis=0)
            Ecopy = np.append(Ecopy, elemNew2, axis=0)
            Ecopy[iElem] = elemNew3

        elif sum(elem) == 3:
            node1 = E[iElem][0]
            node2 = E[iElem][1]
            node3 = E[iElem][2]

            # create new nodes
            node1New = np.array(
                [[(V[node2 - 1][0] + V[node3 - 1][0]) / 2, (V[node2 - 1][1] + V[node3 - 1][1]) / 2]])
            node2New = np.array(
                [[(V[node1 - 1][0] + V[node3 - 1][0]) / 2, (V[node1 - 1][1] + V[node3 - 1][1]) / 2]])
            node3New = np.array(
                [[(V[node1 - 1][0] + V[node2 - 1][0]) / 2, (V[node1 - 1][1] + V[node2 - 1][1]) / 2]])
            Vcopy = np.append(Vcopy, node1New, axis=0)
            Vcopy = np.append(Vcopy, node2New, axis=0)
            Vcopy = np.append(Vcopy, node3New, axis=0)

            # create new elements
            elemNew1 = np.array([[len(Vcopy) - 2, node3, len(Vcopy) - 1]])
            elemNew2 = np.array([[len(Vcopy) - 1, node1, len(Vcopy)]])
            elemNew3 = np.array([[len(Vcopy), node2, len(Vcopy) - 2]])
            elemNew4 = np.array([[len(Vcopy) - 2, len(Vcopy) - 1, len(Vcopy)]])

            # add to the new E matrix
            Ecopy = np.append(Ecopy, elemNew1, axis=0)
            Ecopy = np.append(Ecopy, elemNew2, axis=0)
            Ecopy = np.append(Ecopy, elemNew3, axis=0)
            Ecopy[iElem] = elemNew4

    omega = 0.3
    elemIndices = np.array([])
    for i, elem in enumerate(eleRefine):
        if sum(elem) != 0:
            elemIndices = np.append(elemIndices, i)

    for i, elem in enumerate(elemIndices):
        for node in elem:

    genGri('allLocalRefined.gri', Vcopy, Ecopy, B)


def genGri(fnameOutput, V, E, B):
    f = open(fnameOutput, 'w')
    nNode = len(V)
    nElemTot = len(E)
    f.write(f"{nNode} {nElemTot} 2\n")
    # node coordinates
    for node in V:
        f.write(f"{node[0]} {node[1]}\n")
    f.write(f"{len(B)}\n")

    # boundary faces
    for i, bGroup in enumerate(B):
        f.write(f"{len(bGroup)} 2 {i}\n")
        for j, bFace in enumerate(bGroup):
            f.write(f"{bFace[0]} {bFace[1]}\n")

    # elements
    f.write(f"{len(E)} 1 TriLagrange\n")
    for i, elem in enumerate(E):
        f.write(f"{elem[0]} {elem[1]} {elem[2]}\n")


def main():
    x = 1
    y = 0
    r = .05
    griFile = 'all.gri'

    I2E = getI2E(griFile, False)
    In, Bn, lIn, lBn = edgehash(griFile, False)
    mesh = readgri(griFile)
    localRefine(x, y, r, mesh, I2E)


if __name__ == "__main__":
    main()
