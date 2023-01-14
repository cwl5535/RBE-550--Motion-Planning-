import turtle

# initialize Screen and Turtle for drawing
s = turtle.Screen()
t = turtle.Turtle()

# Change title of Window
s.title("Assignment 0 (RBE 550): Setting up Python")

# Move turtle
def reorient(t): 
    t.left(90) # rotate turtle 90 degrees to the left

def victor_sierra(t):
    """ 
    arguments: t -> turtle.Turtle() object

    """
    length = 100
    i = 0
    while i < 3: 
        t.forward(length)
        t.right(120)
        t.forward(length)
        t.right(120)
        t.forward(length)
        i += 1

def main(t):
    reorient(t)
    x = 0
    while x < 2:
        victor_sierra(t)
        t.right(30)
        x += 1

if __name__ == "__main__":
    main(t)
    turtle.done()  # needed at the end of every turtle program


