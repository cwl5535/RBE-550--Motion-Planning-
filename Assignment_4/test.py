import pickle

# test = [1,2,3,4]
# test_1 = [0,0,0,0]
# test_2 = [1,1,1,1]

# with open("test.txt", "wb") as f: 
#     pickle.dump([test, test_1, test_2], f)

def add(a,b):
    return a+b

# print(add((1,2)))
print(add(*(1,2)))
# with open('test.txt', 'rb') as f:
#     test, test_1, test_2 = pickle.load(f)

# print(test, end = "\n\n")
# print(test_1, end = "\n\n")
# print(test_2, end = "\n\n")