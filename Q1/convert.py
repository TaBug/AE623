import numpy as np

# Open the input .txt file and read the node coordinates
main = np.loadtxt('../foil_coord/main.txt')
flap = np.loadtxt('../foil_coord/flap.txt')
slat = np.loadtxt('../foil_coord/slat.txt')

# Open the output .geo file
with open("../Q1/all.geo", "w") as f:
    # Write the node coordinates to the .geo file
    for i, line in enumerate(main):
        x = main[i][0]
        y = main[i][1]
        f.write(f"Point({i+1}) = {{{x}, {y}, 0}};\n")
    for i, line in enumerate(flap):
        index = i+len(main)
        x = flap[i][0]
        y = flap[i][1]
        f.write(f"Point({index+1}) = {{{x}, {y}, 0}};\n")
    for i, line in enumerate(slat):
        index = i+len(main)+len(flap)
        x = slat[i][0]
        y = slat[i][1]
        f.write(f"Point({index+1}) = {{{x}, {y}, 0}};\n")

    # Write the instructions for connecting the nodes to form a triangular mesh
    counter = 0
    for i in range(0, len(main) - 1, 4):
        f.write(f"Line({counter+1}) = {{{i+1}, {i+2}}};\n")
        counter += 1
    for i in range(0, len(flap) - 1, 4):
        index = i + len(main)
        f.write(f"Line({counter+1}) = {{{index+1}, {index+2}}};\n")
        counter += 1
    for i in range(0, len(slat) - 1, 4):
        index = i + len(main) + len(flap)
        f.write(f"Line({counter+1}) = {{{index+1}, {index+2}}};\n")
        counter += 1

    boxSize = 200
    Nnodes = len(main) + len(flap) + len(slat) - 3
    f.write(f"Point({Nnodes + 1}) = {{{-boxSize/2}, {-boxSize/2}, 0}};\n")
    f.write(f"Point({Nnodes + 2}) = {{{boxSize/2}, {-boxSize/2}, 0}};\n")
    f.write(f"Point({Nnodes + 3}) = {{{boxSize/2}, {boxSize/2}, 0}};\n")
    f.write(f"Point({Nnodes + 4}) = {{{-boxSize/2}, {boxSize/2}, 0}};\n")

    f.write(f"Line({counter + 1}) = {{{Nnodes + 1}, {Nnodes + 2}}};\n")
    f.write(f"Line({counter + 2}) = {{{Nnodes + 2}, {Nnodes + 3}}};\n")
    f.write(f"Line({counter + 3}) = {{{Nnodes + 3}, {Nnodes + 4}}};\n")
    f.write(f"Line({counter + 4}) = {{{Nnodes + 4}, {Nnodes + 1}}};\n")
    # Create a physical group for the elements of the mesh
    f.write(f"Line Loop(1) = {1:{counter}};\n")
    f.write("Plane Surface(1) = {1};\n")
