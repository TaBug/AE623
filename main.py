import numpy as np
from txt2geo.py import txt


def main():
    # Open the input .txt file and read the node coordinates
    main = np.loadtxt('../foil_coord/main.txt')
    flap = np.loadtxt('../foil_coord/flap.txt')
    slat = np.loadtxt('../foil_coord/slat.txt')

    txt2geo(main, flap, slat)


if __name__ == "__main__":
    main()
