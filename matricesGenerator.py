import numpy as np


def readgri(fname):
    f = open(fname, 'r')
    Nn, Ne, dim = [int(s) for s in f.readline().split()]
    # read vertices
    V = np.array([[float(s) for s in f.readline().split()] for n in range(Nn)])
    # read boundaries
    NB = int(f.readline())
    B = [];
    Bname = []
    for i in range(NB):
        s = f.readline().split();
        Nb = int(s[0]);
        Bname.append(s[2])
        Bi = np.array([[int(s) for s in f.readline().split()] for n in range(Nb)])
        B.append(Bi)
    # read elements
    Ne0 = 0;
    E = []
    while (Ne0 < Ne):
        s = f.readline().split();
        ne = int(s[0])
        Ei = np.array([[int(s) for s in f.readline().split()] for n in range(ne)])
        E = Ei if (Ne0 == 0) else np.concatenate((E, Ei), axis=0)
        Ne0 += ne
    f.close()
    Mesh = {'V': V, 'E': E, 'B': B, 'Bname': Bname}
    return Mesh


def getI2E(fnameInput, toOutput):
    Mesh = readgri(fnameInput)
    E = Mesh['E']
    B = Mesh['B']

    output = np.array([[]])
    faces = np.array([[]])

    for i, elem in enumerate(E):
        for e in range(3):
            if e == 0:
                node1 = 1
                node2 = 2
            elif e == 1:
                node1 = 2
                node2 = 0
            else:
                node1 = 0
                node2 = 1

            newFace = np.array([[elem[node1], elem[node2]]])
            for bGroup in B:
                if np.isin(bGroup, newFace).all(axis=1).any():
                    break
            else:
                if faces.size == 0:
                    faces = newFace
                    output = np.array([[i + 1, e + 1, 0, 0]])
                else:
                    isin = np.isin(faces, newFace).all(axis=1)
                    if isin.any():
                        iFace = np.where(isin)[0][0]
                        output[iFace][2] = i + 1
                        output[iFace][3] = e + 1
                    else:
                        faces = np.append(faces, newFace, axis=0)
                        face = np.array([[i + 1, e + 1, 0, 0]])
                        output = np.append(output, face, axis=0)
                continue

    if toOutput:
        with open('I2E.txt', 'w') as f:
            for i in range(len(output)):
                f.write(f'{int(output[i][0])} {int(output[i][1])} {int(output[i][2])} {int(output[i][3])}\n')
            f.close()

    return output


def getB2E(fnameInput, toOutput):
    Mesh = readgri(fnameInput)
    E = Mesh['E']
    B = Mesh['B']
    output = np.array([[]], dtype=int)
    iElem = len(E)
    for ibGroup, bGroup in enumerate(B):
        for nb in bGroup:
            for i, ne in enumerate(np.isin(E, nb)):
                if np.count_nonzero(ne == True) == 2:
                    iElem = i
                    break
            node1 = nb[0]
            node2 = nb[1]
            elem = E[iElem]
            inode1 = np.where(elem == node1)[0][0]
            inode2 = np.where(elem == node2)[0][0]
            iface = 3 - inode1 - inode2

            newB = np.array([[int(iElem + 1), int(iface + 1), int(ibGroup + 1)]])
            if output.size == 0:
                output = newB
            else:
                output = np.append(output, newB, axis=0)

    if toOutput:
        with open('B2E.txt', 'w') as f:
            for i in range(len(output)):
                f.write(f'{int(output[i][0])} {int(output[i][1])} {int(output[i][2])}\n')
            f.close()

    return output


def edgehash(fnameInput, toOutput):
    Mesh = readgri(fnameInput)
    E = Mesh['E']
    V = Mesh['V']
    I2E = getI2E(fnameInput, False)
    B2E = getB2E(fnameInput, False)
    In = np.array([[]])
    Bn = np.array([[]])
    lIn = np.array([])
    lBn = np.array([])

    for iface, face in enumerate(I2E):
        elemL = face[0]
        faceL = face[1]
        if faceL == 1:
            node1 = 1
            node2 = 2
        elif faceL == 2:
            node1 = 2
            node2 = 0
        else:
            node1 = 0
            node2 = 1
        node1Global = E[elemL - 1][node1]
        node2Global = E[elemL - 1][node2]
        node1c = V[node1Global - 1]
        node2c = V[node2Global - 1]
        l = np.sqrt((node2c[0] - node1c[0]) ** 2 + (node2c[1] - node1c[1]) ** 2)
        n = np.array([[(node2c[1] - node1c[1]) / l, -(node2c[0] - node1c[0]) / l]])
        if In.size == 0:
            In = n
        else:
            In = np.append(In, n, axis=0)
        lIn = np.append(lIn, l)

        if toOutput:
            with open('In.txt', 'w') as f:
                for Ini in In:
                    f.write(f'{Ini[0]} {Ini[1]}\n')
            f.close()

    for iface, face in enumerate(B2E):
        elem = face[0]
        faceLocal = face[1]
        if faceLocal == 1:
            node1 = 1
            node2 = 2
        elif faceLocal == 2:
            node1 = 2
            node2 = 0
        else:
            node1 = 0
            node2 = 1
        node1Global = E[elem - 1][node1]
        node2Global = E[elem - 1][node2]
        node1c = V[node1Global - 1]
        node2c = V[node2Global - 1]
        l = np.sqrt((node2c[0] - node1c[0]) ** 2 + (node2c[1] - node1c[1]) ** 2)
        n = np.array([[(node2c[1] - node1c[1]) / l, -(node2c[0] - node1c[0]) / l]])
        if Bn.size == 0:
            Bn = n
        else:
            Bn = np.append(Bn, n, axis=0)
        lBn = np.append(lBn, l)

        if toOutput:
            with open('Bn.txt', 'w') as f:
                for Bni in Bn:
                    f.write(f'{Bni[0]} {Bni[1]}\n')
            f.close()

    return In, Bn, lIn, lBn


# input: element matrix, node coordinate matrix
# output: element area matrix (index = element index)
def area(fnameInput, toOutput):
    Mesh = readgri(fnameInput)
    E = Mesh['E']
    V = Mesh['V']

    areas = np.zeros(len(E))
    for i, ne in enumerate(E):
        coor0 = V[int(ne[0]) - 1]
        coor1 = V[int(ne[1]) - 1]
        coor2 = V[int(ne[2]) - 1]
        areas[i] = 1 / 2 * (coor0[0] * (coor1[1] - coor2[1]) + coor1[0] * (coor2[1] - coor0[1]) + coor2[0] * (
                    coor0[1] - coor1[1]))

    if toOutput:
        with open('area.txt', 'w') as f:
            for areai in areas:
                f.write(f'{areai}\n')
        f.close()


def main():
    getI2E('test.gri', True)
    getB2E('test.gri', True)
    edgehash('test.gri', True)
    area('test.gri', True)


if __name__ == "__main__":
    main()
