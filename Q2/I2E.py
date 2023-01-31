import numpy as np


def I2E(fnameInput, fnameOutput):
    # input file
    with open(fnameInput, "r") as f:
        lines = f.readlines()

        nNode, nElemTot, Dim = map(int, lines[0].strip().split())
        nodeCoord = np.zeros((nNode, 2))
        index = 1
        for i in range(nNode):
            x, y = map(float, lines[index].strip().split())
            nodeCoord[i][0] = x
            nodeCoord[i][1] = y
            index += 1

        nBGroup = int(lines[index])
        index += 1
        NB = np.array([[]], dtype=int)
        for i in range(nBGroup):
            nBFace, nf = map(int, lines[index].strip().split()[:2])
            index += 1
            for j in range(nBFace):
                if np.size(NB) == 0:
                    NB = np.array([[int(num) for i, num in enumerate(lines[index].strip().split())]], dtype=int)
                else:
                    NB = np.concatenate((NB, np.array([[int(num) for i, num in enumerate(lines[index].strip().split())]], dtype=int)), axis=0)
                index += 1

        NE = np.zeros((nElemTot, 3), dtype=int)
        iStart = index + 1

        while index <= len(lines) - 1:
            nElem = int(lines[index].strip().split()[0])
            index += 1
            for j in range(nElem):
                NE[index - iStart] = lines[index].strip().split()
                index += 1

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
                if e == 2:
                    ePlus = 0
                else:
                    ePlus = e + 1

                newFace = np.array([[elem[e], elem[ePlus]]])
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


def main():
    I2E('../Q1/all.gri', 'I2E.txt')


if __name__ == "__main__":
    main()
