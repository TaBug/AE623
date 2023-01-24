import numpy as np
from scipy import sparse
from scipy.sparse import linalg


# input: element matrix, node coordinate matrix
# output: element area matrix (index = element index)
def area(eles, nodes):
    areas = np.zeros(len(eles))
    for i, ele in enumerate(eles):
        coor0 = nodes[int(ele[0]) - 1]
        coor1 = nodes[int(ele[1]) - 1]
        coor2 = nodes[int(ele[2]) - 1]
        areas[i] = 1 / 2 * (coor0[0] * (coor1[1] - coor2[1]) + coor1[0] * (coor2[1] - coor0[1]) + coor2[0] * (
                coor0[1] - coor1[1]))
    return areas


def main():
    eles = np.loadtxt('NE.txt')
    nodes = np.loadtxt('Nodec.txt')
    areas = area(eles, nodes)


if __name__ == "__main__":
    main()
