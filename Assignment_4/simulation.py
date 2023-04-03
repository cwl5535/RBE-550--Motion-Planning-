import pickle
import os
from wumpus import Wumpus
from firetruck import Firetruck
from matplotlib import pyplot as plt
import numpy as np

wumpus = Wumpus()
firetruck = Firetruck()

os.chdir(r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_4\Run_1")
# with open("wumpus_path.txt", "rb") as w:
#     print(pickle.load(w))

# with open("CPU_times_run2.txt", "rb") as c:
#     total_wumpus_CPU_time, total_firetruck_CPU_time, t = pickle.load(c)

with open('simulation_variables.txt', 'rb') as s:
    intact_sim, burning_sim, burned_sim, extinguished_sim, t_int = pickle.load(s)

with open('wumpus_path.txt', 'rb') as w:
    wumpus.finalpath_x, wumpus.finalpath_y = pickle.load(w)

with open('firetruck_path.txt', 'rb') as f:
    firetruck.finalpath_x, firetruck.finalpath_y = pickle.load(f)
# each sim list is a list of Lists that contains a coordinate of an onstacle 
intact_x = []
intact_y = []
burning_x = []
burning_y = []
extinguished_x = []
extinguished_y = []
burned_x = []
burned_y = []



for x,y in intact_sim[-1]:
    intact_x.append(x)
    intact_y.append(y)

for x,y,z in burning_sim[-1]:
    burning_x.append(x), burning_y.append(y)

for x,y in extinguished_sim[-1]:
    extinguished_x.append(x), extinguished_y.append(y)

for x,y in burned_sim[-1]:
    burned_x.append(x), burned_y.append(y)

# Coverage Plots
# plt.plot(intact_x,intact_y, ".b", label = "Intact")
# plt.plot(burning_x,burning_y, ".r", label = "Burning")
# plt.plot(extinguished_x,extinguished_y, ".g", label = "Extinguished")
# plt.plot(burned_x,burned_y, ".k", label = "Burned")
plt.title("Wumpus vs. Firetruck, Run 1, 360 Iterations")
plt.legend()


total = len(intact_sim[-1]) + len(burning_sim[-1]) + len(burned_sim[-1]) + len(extinguished_sim[-1])
ratio_1 = len(intact_sim[-1])/total
ratio_2 = len(burned_sim[-1])/total
ratio_3 = len(extinguished_sim[-1])/total

## Ratio Plots

# plt.bar(1,ratio_1, 2, color = "blue", label = "Intact Ratio")
# plt.bar(3, ratio_2, 2, color = "black", label = "Burned Ratio")
# plt.bar(5,ratio_3, 2, color = "green", label = "Extinguished Ratio")
# plt.title("Wumpus vs. Firetruck, Run 1, 360 Iterations")
# plt.legend()


# CPU Time Plots
plt.bar(1, 50000, 2, color = "black", label = "Wumpus")
plt.bar(3, 1500,2, color = "red", label = "Firetruck")
plt.title("CPU Time (s): Wumpus vs. Firetruck, Run 1, 360 Iterations")
plt.legend()

plt.show()


print("Run 2")
print(f"intact ratio: {ratio_1}")
print(f"burned ratio: {ratio_2}")
print(f"extinguished ratio: {ratio_3}")


# print(intact_sim[0])
# print(len(wumpus.finalpath_y[0]))
# print((extinguished_sim[0]))

# if __name__ == "__main__":

#     t = list(range(360))
#     # for i in range(360):
#     #     print(i)
#     #     plt.plot(*intact_sim[i])
#     #     plt.plot(*burning_sim[i])
#     #     plt.plot(*extinguished_sim[i])  
#     #     plt.plot(*burned_sim[i])


    # for x, y, intact, burned, extinguished, burning, t in zip(wumpus.finalpath_x, wunmpus.finalpath_y, intact_sim, burned_sim, extinguished_sim, burning_sim,  t):
    #     x.sort(), y.sort()
    #     print(t)
    #     # plt.cla()
    #     plt.plot(intact[t][0], intact[t][1], ".g", label="intact")
    #     plt.plot(burning[t][0], burning[t][1], ".r", label="burning")
    #     plt.plot(extinguished[t][0], extinguished[t][1], ".g", label="extinguished")  
    #     plt.plot(burned[t][0], burned[t][1], ".k", label="burned")
    #     # wumpus.move(x,y)



    # plt.show()


