import numpy as np
from pathlib import Path

I2E = np.loadtxt('../Q2/Q2_results/I2E.txt', dtype=int)
B2E = np.loadtxt('../Q2/Q2_results/B2E.txt', dtype=int)
In = np.loadtxt('../Q2/Q2_results/In.txt')
Bn = np.loadtxt('../Q2/Q2_results/Bn.txt')
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
    eleFlagged = np.array([])
    edgeFlagged = np.array([])
    for i in range(len(NE)):
        xc = (meshNodes[NE[i][0] - 1][0] + meshNodes[NE[i][1] - 1][0] + meshNodes[NE[i][1] - 1][0]) / 3
        yc = (meshNodes[NE[i][0] - 1][1] + meshNodes[NE[i][1] - 1][1] + meshNodes[NE[i][1] - 1][1]) / 3
        if np.sqrt((xc - x)**2 + (yc - y)**2) <= r:
            np.append(eleFlagged, i)

    for i in I2E:


def main():
    x = -.01
    y = 0
    r = .05
    localRefine(x, y, r)


if __name__ == "__main__":
    main()
