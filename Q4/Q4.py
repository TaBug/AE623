import numpy as np
from pathlib import Path


def main():
    I2E = np.loadtxt('../Q2/Q2_results/I2E.txt', dtype=int)
    B2E = np.loadtxt('../Q2/Q2_results/B2E.txt', dtype=int)
    In = np.loadtxt('../Q2/Q2_results/In.txt')
    Bn = np.loadtxt('../Q2/Q2_results/Bn.txt')
    Area = np.loadtxt('../Q2/Q2_results/Area.txt')


if __name__ == "__main__":
    main()
