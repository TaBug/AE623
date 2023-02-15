import numpy as np


def readgri(fname):
    f = open(fname, 'r')
    Nn, Ne, dim = [int(s) for s in f.readline().split()]
    # read vertices
    V = np.array([[float(s) for s in f.readline().split()] for n in range(Nn)])
    # read boundaries
    NB = int(f.readline())
    B = []
    Bname = []
    for i in range(NB):
        s = f.readline().split()
        Nb = int(s[0])
        Bname.append(s[2])
        Bi = np.array([[int(s) - 1 for s in f.readline().split()] for n in range(Nb)])
        B.append(Bi)
    # read elements
    Ne0 = 0
    E = []
    while (Ne0 < Ne):
        s = f.readline().split()
        ne = int(s[0])
        Ei = np.array([[int(s) - 1 for s in f.readline().split()] for n in range(ne)])
        E = Ei if (Ne0 == 0) else np.concatenate((E, Ei), axis=0)
        Ne0 += ne
    f.close()
    Mesh = {'V': V, 'E': E, 'B': B, 'Bname': Bname}
    return V, E, B, Bname


def I2E(fnameInput):
    nodes, NE, NB, NBName = readgri(fnameInput)

    elemLs = []
    faceLs = []
    elemRs = []
    faceRs = []
    faces = []

    with open('I2E.txt', 'w') as f:
        for i, elem in enumerate(NE[1:]):
            for e in range(3):
                if e == 0:
                    node1 = 1
                    node2 = 2
                elif e == 1:
                    node1 = 2
                    node2 = 0
                else:
                    node1 = 1
                    node2 = 2

                newFace = np.array([[elem[node1], elem[node2]]])
                if np.isin(NB, newFace).all(axis=1)
                    continue

                isin = np.isin(faces, newFace).all(axis=1)
                if isin.any():
                    iFace = np.where(isin)
                    elemRs[iFace] = i + 1
                    faceRs[iFace] = e + 1
                else:
                    elemLs.append(i + 1)
                    elemRs.append(0)
                    faceLs.append(e + 1)
                    faceRs.append(0)
                    faces.append(newFace)

        for i in range(len(elemLs)):
            f.write(f'{int(elemLs[i])} {int(faceLs[i])} {int(elemRs[i])} {int(faceRs[i])}\n')
        f.close()
    return [elemLs, faceLs, elemRs, faceRs]

def B2E(fnameInput):
    nodes, NE, NB, NBName = readgri(fnameInput)
    elems = []
    faces = []
    nBGroups = []
    for iGroup, bGroup in enumerate(NB):
        for ib, nb in enumerate(bGroup):
            iElem = np.where(np.isin(NE, nb).all(axis=1))
            node1 = nb[0]
            node2 = nb[1]
            elem = NE[iElem]
            inode1 = np.where(elem, node1)
            inode2 = np.where(elem, node2)
            iface = 3 - inode1 - inode2;
            
            elems.append(elem)
            faces.append(iface)
            nBGroups.append(iGroup)

    with open('B2E.txt', 'w') as f:
        for i in range(len(elems)):
            f.write(f'{int(elems[i])} {int(faces[i])} {int(nBGroups[i])}\n')
    return [elems, faces, nBGroups]

def edgehash(fnameInput):
    nodes, NE, NB, NBName = readgri(fnameInput)
    I2E = I2E(fnameInput)
    B2E = B2E(fnameInput)
    In = []
    Bn = []
    faces = []
    lIn = []
    lBn = []
    with open('In.txt', 'w') as f:
        for iface, face in enumerate(I2E):
            elemL = face[0]
            faceL = face[1]
            elemR = face[2]
            faceR = face[3]
            if faceL == 0:
                node1 = 1
                node2 = 2
            elif faceL == 1:
                node1 = 2
                node2 = 0
            else:
                node1 = 0
                node2 = 1
            node1Global = NE[elemL][node1]
            node2Global = NE[elemL][node2]
            node1c = nodes[node1Global]
            node2c = nodes[node2Global]
            l = np.sqrt((node2c[0] - node1c[0]) ** 2 + (node2c[1] - node2c[0]) ** 2)
            n = np.array([(node2c[1] - node1c[1]) / l, -(node2c[0] - node1c[0]) / l])
            In.append(n)
            lIn.append(l)
            f.write(f'{n[0]} {n[1]}\n')

    with open(f'Bn.txt', 'w') as f:
        for iface, face in enumerate(B2E):
            elem = face[0]
            face = face[1]
            if face == 0:
                node1 = 1
                node2 = 2
            elif face == 1:
                node1 = 2
                node2 = 0
            else:
                node1 = 0
                node2 = 1
            node1Global = NE[elem][node1]
            node2Global = NE[elem][node2]
            node1c = nodes[node1Global]
            node2c = nodes[node2Global]
            l = np.sqrt((node2c[0] - node1c[0]) ** 2 + (node2c[1] - node2c[0]) ** 2)
            n = np.array([(node2c[1] - node1c[1]) / l, -(node2c[0] - node1c[0]) / l])
            Bn.append(n)
            lBn.append(l)
            f.write(f'{n[0]} {n[1]}\n')

    return In, Bn, lIn, lBn

# input: element matrix, node coordinate matrix
# output: element area matrix (index = element index)
def area(fnameInput, fnameOutput):
    nodes, NE, NB, NBName = readgri(fnameInput)
    with open(fnameOutput, 'w') as f:
        for i, ne in enumerate(NE):
            coor0 = nodes[int(ne[0]) - 1]
            coor1 = nodes[int(ne[1]) - 1]
            coor2 = nodes[int(ne[2]) - 1]
            area = 1 / 2 * (coor0[0] * (coor1[1] - coor2[1]) + coor1[0] * (coor2[1] - coor0[1]) + coor2[0] * (
                    coor0[1] - coor1[1]))
            f.write(f'area'\n)

def main():
    I2E('all.gri', 'I2E.txt')
    # B2E('all.gri', 'B2E.txt')


if __name__ == "__main__":
    main()
