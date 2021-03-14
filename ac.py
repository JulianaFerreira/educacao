from tkinter import *
import random
import copy
import matplotlib.pylab as plt
import imageio as imageio
from PIL import Image, ImageGrab
import numpy as np

# States
states1 = ['Y1', 'Y2', 'Y3', 'Y4', 'I', 'G', 'W']
# Initial Probability
probability1 = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# Transition matrix
transitionMatrix1 = [[0.057, 0.31, 0.0, 0.0, 0.603, 0.0, 0.03], [0.0, 0.187, 0.528, 0.0, 0.285, 0.0, 0.0],
     [0.0, 0.0, 0.012, 0.563, 0.097, 0.328, 0.0], [0.0, 0.0, 0.0, 0.039, 0.094, 0.814, 0.053],
     [0.001, 0.036, 0.02, 0.0, 0.0, 0.003, 0.94], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]

time = 480
cycles = 20
timeinterval = 15

# Size
width = 30
height = 40
quantCells = width * height

quantityState0 = []
quantityState1 = []
quantityState2 = []
quantityState3 = []
quantityState4 = []
quantityState5 = []
quantityState6 = []


class Cell:

    def __init__(self, time, state1, state2, state3):
        self.time = time
        self.state1 = state1
        self.state2 = state2
        self.state3 = state3

    def gettime(self):
        return self.time

    def settime(self, time):
        self.time = time

    def getstate1(self):
        return self.state1

    def setstate1(self, state1):
        self.state1 = state1

    def getstate2(self):
        return self.state2

    def setstate2(self, state2):
        self.state2 = state2

    def getstate3(self):
        return self.state3

    def setstate3(self, state3):
        self.state3 = state3


cell = [[0 for row in range(-1, width + 1)] for col in range(-1, height + 1)]
previousGen = [[0 for row in range(-1, width + 1)] for col in range(-1, height + 1)]
temporary = [[0 for row in range(-1, width + 1)] for col in range(-1, height + 1)]


def make_frames():
    processing()
    paint_cells()
    root.update()  # comment to make infinite
    # root.after(1000, make_frames) #not comment to make infinite


def make_graph():
    figure = plt.figure()
    plt.title('Students')
    # t = np.linspace(0, time, time)
    # np.arange(0.0, quantCells, 1.0)

    s1_line, = plt.plot(quantityState0, label=states1[0], color="white")
    s2_line, = plt.plot(quantityState1, label=states1[1], color="blue")
    s3_line, = plt.plot(quantityState2, label=states1[2], color="purple")
    s4_line, = plt.plot(quantityState3, label=states1[3], color="black")
    #s5_line, = plt.plot(quantityState4, label=states1[4], color="yellow")
    #s6_line, = plt.plot(quantityState5, label=states1[5], color="green")
    #s7_line, = plt.plot(quantityState6, label=states1[6], color="read")

    #plt.legend(handles=[s1_line, s2_line, s3_line, s4_line, s5_line, s6_line, s7_line])
    plt.legend(handles=[s1_line, s2_line, s3_line, s4_line])

    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    plt.xlabel('Transition')
    plt.ylabel('Cells')

    plt.savefig('myplot.png')
    plt.show()


#create automato cells
def put_cells():
    for y in range(-1, width + 1):
        for x in range(-1, height + 1):
            state1 = np.random.choice(states1, replace=True, p=probability1)
            #state2 = np.random.choice(states2, replace=True, p=probability2)
            #state3 = np.random.choice(states3, replace=True, p=probability3)
            newCell = Cell(0, state1, 0, 0)
            previousGen[x][y] = newCell
            temporary[x][y] = 0
            cell[x][y] = canvas.create_rectangle((x * 20, y * 20, x * 20 + 20, y * 20 + 20), outline="gray50",
                                                 fill="white")


def processing():
    cells_state_0 = 0
    cells_state_1 = 0
    cells_state_2 = 0
    cells_state_3 = 0
    cells_state_4 = 0
    cells_state_5 = 0
    cells_state_6 = 0

    for y in range(0, width):
        for x in range(0, height):
            neighbors_state1 = search_state(states1[0], x, y)
            neighbors_state2 = search_state(states1[1], x, y)
            neighbors_state3 = search_state(states1[2], x, y)
            neighbors = [neighbors_state1, neighbors_state2, neighbors_state3]

            temporary[x][y] = copy.copy(previousGen[x][y])
            temporary[x][y].settime(temporary[x][y].gettime() + timeinterval)
            #transitionMatrix = updateTransitionMatrix(transitionMatrix1, neighbors, temporary[x][y].getstate2())

            # Next state
            temporary[x][y].setstate1(getNewState(states1, transitionMatrix1, previousGen[x][y].getstate1()))


            #count state
            if previousGen[x][y].getstate1() == states1[0]:
                cells_state_0 += 1
            elif previousGen[x][y].getstate1() == states1[1]:
                cells_state_1 += 1
            elif previousGen[x][y].getstate1() == states1[2]:
                cells_state_2 += 1
            elif previousGen[x][y].getstate1() == states1[3]:
                cells_state_3 += 1
            elif previousGen[x][y].getstate1() == states1[4]:
                cells_state_4 += 1
            elif previousGen[x][y].getstate1() == states1[5]:
                cells_state_5 += 1
            elif previousGen[x][y].getstate1() == states1[6]:
                cells_state_6 += 1


    archive = open("ac.txt", "a")
    archive2 = open("ac.txt", "r")
    content = archive2.readlines()
    archive.write("day: %d" % temporary[0][0].gettime() + "\n")
    archive.write("----------------------------" + "\n")
    archive.write("cells state " + states1[0] + ": %d" % cells_state_0 + "\n")
    archive.write("cells state " + states1[1] + ": %d" % cells_state_1 + "\n")
    archive.write("cells state " + states1[2] + ": %d" % cells_state_2 + "\n")
    archive.write("cells state " + states1[3] + ": %d" % cells_state_3 + "\n")
    archive.write("cells state " + states1[4] + ": %d" % cells_state_4 + "\n")
    archive.write("cells state " + states1[5] + ": %d" % cells_state_5 + "\n")
    archive.write("cells state " + states1[6] + ": %d" % cells_state_6 + "\n")
    archive.write("----------------------------" + "\n")
    quantityState0.append(cells_state_0)
    quantityState1.append(cells_state_1)
    quantityState2.append(cells_state_2)
    quantityState3.append(cells_state_3)

    for y in range(0, width):
        for x in range(0, height):
            previousGen[x][y] = temporary[x][y]


# Function that implements the Markov model
def getNewState(states, transitionMatrix, currentState):
    i = 0
    newState = ""
    for x in states:
        if currentState == x:
            newState = np.random.choice(states, replace=True, p=transitionMatrix[i])
        i+=1

    return newState


# def updateTransitionMatrix(transitionMatrix, neighbors, state2):
#     newTransitionMatrix = transitionMatrix
#
#     if neighbors[0] > 4 and states2 == 1:
#         newTransitionMatrix = transitionMatrix11
#     elif neighbors[1] > 4:
#         newTransitionMatrix = transitionMatrix12
#     elif neighbors[2] > 4 and states2 == 0:
#         newTransitionMatrix = transitionMatrix13
#
#     return newTransitionMatrix


def search_state(state, a, b):
    count = 0

    if previousGen[a - 1][b + 1].getstate1() == state:
        count += 1

    if previousGen[a][b + 1].getstate1() == state:
        count += 1

    if previousGen[a + 1][b + 1].getstate1() == state:
        count += 1

    if previousGen[a - 1][b].getstate1() == state:
        count += 1

    if previousGen[a + 1][b].getstate1() == state:
        count += 1

    if previousGen[a - 1][b - 1].getstate1() == state:
        count += 1

    if previousGen[a][b - 1].getstate1() == state:
        count += 1

    if previousGen[a + 1][b - 1].getstate1() == state:
        count += 1

    return count


def paint_cells():
    for y in range(width):
        for x in range(height):
            if previousGen[x][y].getstate1() == states1[0]:
                canvas.itemconfig(cell[x][y], fill="white")
            elif previousGen[x][y].getstate1() == states1[1]:
                canvas.itemconfig(cell[x][y], fill="blue")
            elif previousGen[x][y].getstate1() == states1[2]:
                canvas.itemconfig(cell[x][y], fill="purple")
            elif previousGen[x][y].getstate1() == states1[3]:
                canvas.itemconfig(cell[x][y], fill="black")
            elif previousGen[x][y].getstate1() == states1[4]:
                canvas.itemconfig(cell[x][y], fill="green")
            elif previousGen[x][y].getstate1() == states1[5]:
                canvas.itemconfig(cell[x][y], fill="yellow")
            elif previousGen[x][y].getstate1() == states1[6]:
                canvas.itemconfig(cell[x][y], fill="red")


root = Tk()
# Original size 800 x 600
canvas = Canvas(root, width=800, height=600, highlightthickness=0, bd=0, bg='white')
canvas.pack()
put_cells()

images = []

#just numbers
# for i in range(0, cycles):
#     processing()
#     print("interation:", i)
#
# make_graph()
# make_graph_weather()

#image CA
for i in range(0, cycles):  # comment to make infinite
    make_frames()
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    xx = x + canvas.winfo_width()
    yy = y + canvas.winfo_height()
    images.append(ImageGrab.grab((x, y, xx, yy)))

make_graph()

imageio.mimsave('ac.gif', images, duration=0.5)

root.mainloop()