import pickle
import os
from wumpus import Wumpus
from firetruck import Firetruck
from matplotlib import pyplot as plt

wumpus = Wumpus()
firetruck = Firetruck()

os.chdir(r"C:\Users\layhu\OneDrive\Desktop\RBE 550 (Motion Planning)\Assignment_4")
# with open("wumpus_path.txt", "rb") as w:
#     print(pickle.load(w))

with open('simulation_variables.txt', 'rb') as s:
    intact_sim, burning_sim, burned_sim, extinguished_sim, t_int = pickle.load(s)

with open('wumpus_path.txt', 'rb') as w:
    wumpus.finalpath_x, wumpus.finalpath_y = pickle.load(w)

with open('firetruck_path.txt', 'rb') as f:
    firetruck.finalpath_x, firetruck.finalpath_y = pickle.load(f)
# each sim list is a list of Lists that contains a coordinate of an onstacle 


# print(len(wumpus.finalpath_y[0]))

if __name__ == "__main__":

    t = list(range(360))
#     # for i in range(360):
#     #     print(i)
#     #     plt.plot(*intact_sim[i])
#     #     plt.plot(*burning_sim[i])
#     #     plt.plot(*extinguished_sim[i])  
#     #     plt.plot(*burned_sim[i])


    for x,y,t in zip(wumpus.finalpath_x, wumpus.finalpath_y, t):
        x.sort(), y.sort()
        print(t)
        plt.plot(*intact_sim[t], ".g", label="intact")
        plt.plot(*burning_sim[t], ".r", label="burning")
        plt.plot(*extinguished_sim[t], ".g", label="extinguished")  
        plt.plot(*burned_sim[t], ".k", label="burned")
        wumpus.move(x,y)


    plt.show()


