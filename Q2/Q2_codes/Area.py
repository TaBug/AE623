import numpy as np


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
    nodes = np.loadtxt('nodco.txt')
    areas = area(eles, nodes)
    areas = np.reshape(areas, [len(areas), 1])
    with open('../../Q4/Area.txt', 'w') as f:
        for line in areas:
            np.savetxt(f, line)


if __name__ == "__main__":
    main()
