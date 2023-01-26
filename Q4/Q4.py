import numpy as np
from pathlib import Path

I2E = np.loadtxt('../Q2/Q2_results/I2E.txt', dtype=int)
B2E = np.loadtxt('../Q2/Q2_results/B2E.txt', dtype=int)
In = np.load('../Q2/Q2_results/In.npy')
Bn = np.load('../Q2/Q2_results/Bn.npy')
Area = np.loadtxt('../Q2/Q2_results/Area.txt')
E2N = np.loadtxt('../Q2/Q2_results/E2N.txt', dtype=int)
IE = np.loadtxt('../Q2/Q2_results/IE.txt', dtype=int)
BE = np.loadtxt('../Q2/Q2_results/BE.txt', dtype=int)
NE = np.loadtxt('../Q2/Q2_results/NE.txt', dtype=int)
mainNodes = np.loadtxt('../foil_coord/main.txt')
flapNodes = np.loadtxt('../foil_coord/flap.txt')
slatNodes = np.loadtxt('../foil_coord/slat.txt')
meshNodes = np.loadtxt('../foil_coord/nodco.txt')


def localRefine(x, y, r):
    eleFlagged = np.zeros(len(NE))
    edgeFlagged = np.zeros(len(I2E))
    for iEle in range(len(NE)):
        xc = (meshNodes[NE[iEle][0] - 1][0] + meshNodes[NE[iEle][1] - 1][0] + meshNodes[NE[iEle][1] - 1][0]) / 3
        yc = (meshNodes[NE[iEle][0] - 1][1] + meshNodes[NE[iEle][1] - 1][1] + meshNodes[NE[iEle][1] - 1][1]) / 3
        if np.sqrt((xc - x) ** 2 + (yc - y) ** 2) <= r:
            eleFlagged[iEle] += 1

    for iEdge, i2e in I2E:
        if eleFlagged[i2e[0]] == 1 or eleFlagged[i2e[2]] == 1:
            edgeFlagged[iEdge] += 1

    for

def main():
    x = -.01
    y = 0
    r = .05
    localRefine(x, y, r)


if __name__ == "__main__":
    main()
