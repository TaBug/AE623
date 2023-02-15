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
    return V, E, B, Bname, Nn, Ne, dim


def I2E(fnameInput, fnameOutput):
    nodes, NE, NB, NBName, Nn, Ne, dim = readgri(fnameInput)

    print(NE)
    with open(fnameOutput, 'w') as f:
        elemLs = np.array([], dtype=int)
        faceLs = np.array([], dtype=int)
        elemRs = np.array([], dtype=int)
        faceRs = np.array([], dtype=int)
        faces = np.array([[NE[0][0], NE[0][1]], [NE[0][1], NE[0][2]], [NE[0][2], NE[0][0]]])

        for e in range(3):
            elemLs = np.append(elemLs, 1)
            elemRs = np.append(elemRs, 0)
            faceLs = np.append(faceLs, e + 1)
            faceRs = np.append(faceRs, 0)

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
                if np.isin(NB, newFace).all(axis=1).any():
                    continue

                isin = np.isin(faces, np.array([[elem[ePlus], elem[e]]])).all(axis=1)
                if isin.any():
                    iFace = np.where(isin)
                    elemRs[iFace] = i + 1
                    faceRs[iFace] = e + 1
                else:
                    elemLs = np.append(elemLs, i + 1)
                    elemRs = np.append(elemRs, 0)
                    faceLs = np.append(faceLs, e + 1)
                    faceRs = np.append(faceRs, 0)
                    faces = np.concatenate((faces, newFace), axis=0)

        for i in range(len(elemLs)):
            f.write(f'{int(elemLs[i])} {int(faceLs[i])} {int(elemRs[i])} {int(faceRs[i])}\n')
        f.close()


def B2E(fnameInput, fnameOutput):
    with open(fnameInput, 'r') as f:
        lines = f.readlines()

        nNode, nElemTot, Dim = map(int, lines[0].strip().split())
        index = nNode + 1
        nBGroup = int(lines[index])
        NB = np.array([[]], dtype=int)
        nBGroups = np.array([])
        index += 1
        for i in range(nBGroup):
            nBFace, nf = map(int, lines[index].strip().split()[:2])
            index += 1
            for j in range(nBFace):
                nBGroups = np.append(nBGroups, i)
                if np.size(NB) == 0:
                    NB = np.array([[int(num) for i, num in enumerate(lines[index].strip().split())]], dtype=int)
                else:
                    NB = np.concatenate(
                        (NB, np.array([[int(num) for i, num in enumerate(lines[index].strip().split())]], dtype=int)),
                        axis=0)
                index += 1

        NE = np.zeros((nElemTot, 3), dtype=int)
        iStart = index + 1
        while index <= len(lines) - 1:
            nElem = int(lines[index].strip().split()[0])
            index += 1
            for j in range(nElem):
                NE[index - iStart] = lines[index].strip().split()
                index += 1

        elems = np.zeros(len(NB), dtype=int)
        faces = np.zeros(len(NB), dtype=int)
        for i, ne in enumerate(NE):
            for e in range(3):
                if e == 2:
                    ePlus = 0
                else:
                    ePlus = e + 1
                face = np.array([ne[e], ne[ePlus]])

                isin = np.isin(NB, face).all(axis=1)
                if isin.any():
                    iface = np.where(isin)
                    elems[iface] = i + 1
                    faces[iface] = e + 1
                    break

    with open(fnameOutput, 'w') as f:
        for i in range(len(elems)):
            f.write(f'{int(elems[i])} {int(faces[i])} {int(nBGroups[i])}\n')


def main():
    I2E('all.gri', 'I2E.txt')
    # B2E('all.gri', 'B2E.txt')


if __name__ == "__main__":
    main()
