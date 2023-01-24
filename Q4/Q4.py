import numpy as np
import numpy as py


def main():
    I2E = np.loadtxt('I2E.txt')
    np.load('B2E.npy')
    np.load('In.npy')
    np.load('Bn.npy')
    np.load('Area.npy')
    print(I2E)


if __name__ == "__main__":
    main()
