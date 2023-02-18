import numpy as np
from matricesGenerator import readgri, I2E, B2E, edgehash, area


def meshTest(griFile):
    nodes, NE, NB, NBName = readgri(griFile)
    I2E = I2E('griFile')
    B2E = B2E('griFile')
    In, Bn, lIn, lBn = edgehash('griFile')
    EI = np.zeros(len(NE))
    for i, face in enumerate(I2E):
        elemL = face[0]
        faceL = face[1]
        elemR = face[2]
        faceR = face[3]
        EI[elemL] += In[i] * lIn[i]
        EI[elemR] -= In[i] * lIn[i]

    EB = np.zeros(len(NE))
    for i, face in enumerate(I2E):
        elemL = face[0]
        faceL = face[1]
        elemR = face[2]
        faceR = face[3]
        EI[elemL] += In[i] * lIn[i]
        EI[elemR] -= In[i] * lIn[i]
    return [EI, EB]


def main():
    EmaxTest = max(abs(meshTest('test.gri')))
    EmaxAll = max(abs(meshTest('all.gri')))
