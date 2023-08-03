import numpy as np
from txt2geo import txt2geo
from msh2gri import msh2gri
from matricesGenerator import getI2E, getB2E, edgehash, area


def main():
    # Open the input .txt file and read the node coordinates
    main = np.loadtxt('main.txt')
    flap = np.loadtxt('slat.txt')
    slat = np.loadtxt('flap.txt')

    # convert geometries .txt to .geo
    txt2geo(main, flap, slat)
    # after generating mesh file from Gmsh, convert the .msh to .gri
    msh2gri('all.msh', 'all.gri')
    # local refin


if __name__ == "__main__":
    main()
