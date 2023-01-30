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
        NB = np.array([[]])
        for i in range(nBGroup):
            nBFace, nf = map(int, lines[index].strip().split()[:2])
            index += 1
            for j in range(nBFace):
                if np.size(NB) == 0:
                    NB = np.array([map(int, lines[index].strip().split())])
                else:
                    NB = np.concatenate((NB, np.array([map(int, lines[index].strip().split())])), axis=0)
                index += 1

        NE = np.zeros((nElemTot, 3))
        iStart = index + 1

        while index <= len(lines) - 1:
            nElem = int(lines[index].strip().split()[0])
            index += 1
            for j in range(nElem):
                NE[index - iStart] = lines[index].strip().split()
                index += 1

    with open(fnameOutput, 'w') as f:
        elemLs = np.array([])
        faceLs = np.array([])
        elemRs = np.array([])
        faceRs = np.array([])
        for i, elem in enumerate(NE):
            for e in range(3):
                if i in elemLs:
                    iElem = np.where(elemLs == i)
                    print(iElem)
                    elemRs[iElem] = i + 1
                    faceRs[iElem] = e + 1
                else:
                    elemLs = np.append(elemLs, i + 1)
                    elemRs = np.append(elemRs, 0)
                    faceLs = np.append(faceLs, e + 1)
                    faceRs = np.append(faceRs, 0)

        for i in range(len(elemLs)):
            f.write(f'{int(elemLs[i])} {int(faceLs[i])} {int(elemRs[i])} {int(faceRs[i])}\n')

        f.close()


def main():
    I2E('../Q1/all.gri', 'I2E.txt')


if __name__ == "__main__":
    main()
