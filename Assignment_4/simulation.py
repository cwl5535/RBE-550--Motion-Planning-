import pickle
import os

os.chdir(r"C:\Users\layhu\OneDrive\Desktop\RBE 550 (Motion Planning)\Assignment_4")
# with open("wumpus_path.txt", "rb") as w:
#     print(pickle.load(w))

with open('simulation_variables.txt', 'rb') as s:
    intact_sim, burning_sim, burned_sim, extinguished_sim, t = pickle.load(s)

with open('wumpus_path.txt', 'rb') as w:
    wumpus_finalpath_x, wumpus_finalpath_y = pickle.load(w)

with open('firetruck_path.txt', 'rb') as f:
    firetruck_finalpath_x, firetruck_finalpath_y = pickle.load(f)


