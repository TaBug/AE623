import numpy as np


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
    B2E('../Q1/all.gri', 'B2E.txt')


if __name__ == "__main__":
    main()
