import numpy as np

I2E = np.loadtxt('../Q2/Q2_results/I2E.txt', dtype=int)
B2E = np.loadtxt('../Q2/Q2_results/B2E.txt', dtype=int)
In = np.load('../Q2/Q2_results/In.npy')
Bn = np.load('../Q2/Q2_results/Bn.npy')
Area = np.loadtxt('../Q2/Q2_results/Area.txt')
# E2N = np.loadtxt('../Q2/Q2_results/E2N.txt', dtype=int)
# IE = np.loadtxt('../Q2/Q2_codes/IE.txt', dtype=int)
BE = np.loadtxt('../Q2/Q2_codes/BE.txt', dtype=int)
NE = np.loadtxt('../Q2/Q2_codes/NE.txt', dtype=int)
mainNodes = np.loadtxt('../foil_coord/main.txt')
flapNodes = np.loadtxt('../foil_coord/flap.txt')
slatNodes = np.loadtxt('../foil_coord/slat.txt')
meshNodes = np.loadtxt('../Q2//Q2_codes/nodco.txt')


def localRefine(x, y, r):
    NEcopy = NE.copy()
    meshNodesCopy = meshNodes.copy()
    eleFlagged = np.zeros(len(NE), dtype=int)
    edgeFlagged = np.zeros(len(I2E), dtype=int)
    for iEle in range(len(NE)):
        xc = (meshNodes[NE[iEle][0] - 1][0] + meshNodes[NE[iEle][1] - 1][0] + meshNodes[NE[iEle][1] - 1][0]) / 3
        yc = (meshNodes[NE[iEle][0] - 1][1] + meshNodes[NE[iEle][1] - 1][1] + meshNodes[NE[iEle][1] - 1][1]) / 3
        if np.sqrt((xc - x) ** 2 + (yc - y) ** 2) <= r:
            eleFlagged[iEle] += 1

    for iEdge, i2e in enumerate(I2E):
        if eleFlagged[i2e[0] - 1] == 1 or eleFlagged[i2e[2] - 1] == 1:
            edgeFlagged[iEdge] += 1

    eleRefine = np.zeros([len(NE), 3], dtype=int)
    for iEdge, i2e in enumerate(I2E):
        if edgeFlagged[iEdge] == 1:
            elemL = i2e[0]
            faceL = i2e[1]
            elemR = i2e[2]
            faceR = i2e[3]
            eleRefine[elemL - 1][faceL - 1] += 1
            eleRefine[elemR - 1][faceR - 1] += 1

    counter = len(meshNodes) + 1
    for iElem, elem in enumerate(eleRefine):
        index = np.where(elem == 1)
        if len(index) == 1:
            node1 = NE[iElem][index - 1]
            node2 = NE[iElem][index - 3]
            node3 = NE[iElem][index - 2]

            coordNew = np.array([[(meshNodes[node3 - 1][0] + meshNodes[node2 - 1][0]) / 2,
                                  (meshNodes[node3 - 1][1] + meshNodes[node2 - 1][1]) / 2]])
            meshNodesCopy = np.append(meshNodesCopy, coordNew, axis=0)

            elemNew1 = np.array([[counter, node1, node2]])
            elemNew2 = np.array([[counter, node3, node1]])
            NEcopy = np.append(NEcopy, elemNew1, axis=0)
            NEcopy = np.append(NEcopy, elemNew2, axis=0)
            NEcopy = np.delete(NEcopy, iElem, 0)
        elif len(index) == 2:
            elemNew1 = np.array([[counter, ne[faceL - 3], ne[faceL - 2]]])
            elemNew2 = np.array([[counter, ne[faceL - 2], ne[faceL - 1]]])
            NEcopy = np.append(NEcopy, elemNew1, axis=0)
            NEcopy = np.append(NEcopy, elemNew2, axis=0)
            NEcopy = np.delete(NEcopy, elemL - 1, 0)
        if eleRefine[elemR - 1] == 1:
            ne = NE[elemR - 1]
            elemNew1 = np.array([[counter, ne[faceL - 3], ne[faceL - 2]]])
            elemNew2 = np.array([[counter, ne[faceL - 2], ne[faceL - 1]]])
            NEcopy = np.append(NEcopy, elemNew1, axis=0)
            NEcopy = np.append(NEcopy, elemNew2, axis=0)
            NEcopy = np.delete(NEcopy, elemL - 1, 0)

    np.savetxt("NERefined.txt", NEcopy, delimiter=" ")
    np.savetxt("nodco.txt", meshNodesCopy, delimiter=" ")


def main():
    x = -.01
    y = 0
    r = .05
    localRefine(x, y, r)


if __name__ == "__main__":
    main()
