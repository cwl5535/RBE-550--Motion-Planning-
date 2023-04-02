import os
import numpy as np
from matplotlib import pyplot as plt


filename = r"\10_coverage.npy"
desktop = False

if desktop: 
    path = r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_4"
else:
    path = r"C:\Users\layhu\OneDrive\Desktop\RBE 550 (Motion Planning)\Assignment_4"

if os.getcwd() is not path: 
    os.chdir(path)
    # start_env = np.load(path + r"\10_coverage.npy")
    start_env = np.load(path + filename)
    
plt.imshow(start_env, cmap="binary")
plt.show()