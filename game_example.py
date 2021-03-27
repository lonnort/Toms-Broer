#!/usr/bin/python3

import pygame, os, platform, re, time, mysql.connector
from AStar import *
from tkinter import *
from triangulation import *
from sql import *

# Initialize database connection
database = connect_database()

# List with all locations of interest
dictionary = get_PoI(database)
lista = list()
for i in dictionary.keys():
    lista.append(i)


class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        """Checks if buttons are pressed"""

        Entry.__init__(self, *args, **kwargs)
        self.lista = lista
        self.var = self['textvariable']
        if self.var == '':
            self.var = self['textvariable'] = StringVar()

        self.var.trace('w', self.changed)
        self.bind('<Right>', self.selection)
        self.bind('<Up>', self.up)
        self.bind('<Down>', self.down)
        self.bind('<Return>', self.enter)

        self.lb_up = False

    def changed(self, name, index, mode):
        """If something is typed into the entry box"""

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind('<Double-Button-1>', self.selection)
                    self.lb.bind('<Right>', self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):
        """If right arrow key is pressed"""

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):
        """If up arrow key is pressed"""

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):
        """If down arrow key is pressed"""

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def enter(self, event):
        """If enter key is pressed"""

        global entered
        grid = matrix_reader()
        counter = 0

        if self.lb_up:  # Runs when drop-down list is active
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

        else:  # Runs when drop-down list is not active
            start = location_convert()
            for q in dictionary:
                if entry.get() == q:
                    counter = 1
                    one_upper(q)
                    end = dictionary['{}'.format(q)]
                    print(end)
                    path = dmain(start, end)
                    print(path)
                    grid[end[0]][end[1]] = 3  # Sets the end to 3 on the grid

                    for x in range(1, len(path) - 1):  # Sets the path to 4 on the grid
                        column = path[x][1]
                        row = path[x][0]
                        grid[row][column] = 4
                        print(grid[row][column])
                    grid[start[0]][start[1]] = 2   
                    grid_draw(grid)
                    entered = True
            if counter == 0:  # Runs if the entered word is not a point of interest
                print('This location does not exist, please choose another')

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]

# Initializes background picture
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

# Draws grid to screen
def grid_draw(grid):
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [499, 550]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    BackGround = Background('maps/background-blueprintv3.png', [0, 0])

    # This sets the WIDTH and HEIGHT of each grid location
    HEIGHT = WIDTH = 25

    # Determines starting point on startup
    print('======[Grid Draw]======')
    global entered

    if entered:
        # Call location_convert()
        current_location = location_convert()

        # Sets current location to 2 on the grid.
        grid[current_location[0]][current_location[1]] = 2

    # current_location = location_convert()
    # start = current_location
    # grid[start[0]][start[1]] = 2

    # This sets the margin between each cell
    MARGIN = 0

    # Define some colors
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (55, 29, 124)

    # Set the screen background
    screen.fill(WHITE)
    screen.blit(BackGround.image, BackGround.rect)

    # Draw the grid
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            color = WHITE
            if grid[row][column] == 2:
                color = GREEN
            if grid[row][column] == 3:
                color = PURPLE
            if grid[row][column] == 4:
                color = BLUE
                print(row,column)
            if color != WHITE:
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])


def location_convert():
    """Finds your location using triangulation.py"""
    try:
        current_location = menu()  # Finds your location on the map
    except:
        time.sleep(0.2)
        current_location = menu()

    if current_location[0] > (len(grid[0]) - 1) or current_location[1] > (len(grid) - 1) or current_location[0] < 0 or current_location[1] < 0:
        current_location = menu()

    if len(locationlist) <= 3:
        locationlist.append(current_location)
    else:
        del locationlist[0]
        locationlist.append(current_location)

    xTemp = []
    yTemp = []

    for i in range(len(locationlist)):
        xTemp.append(locationlist[i][1])
        yTemp.append(locationlist[i][0])

    current_location[0] = int(sum(yTemp) / len(yTemp))
    current_location[1] = int(sum(xTemp) / len(xTemp))

    return current_location
entered = False

def game_main():
    """Runs once on start up"""

    # Create a 2 dimensional array based on binary map.
    global grid
    grid = matrix_reader()

    global locationlist
    locationlist = []


    # Draw the grid.
    grid_draw(grid)
    # Initialize pygame
    pygame.init()

    # Set title of screen
    pygame.display.set_caption('Array Backed Grid')

    # Loop until done
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    global entered    

    # -------- Main Program Loop -----------
    while not done:  # Ends when
        # if entered:
        #     # Call location_convert()
        #     current_location = location_convert()

        #     # Sets current location to 2 on the grid.
        #     grid[current_location[0]][current_location[1]] = 2

        # Updates TKinter GUI
        root.update()

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

# GUI
root = Tk()
logo = PhotoImage(file = 'pictures/tomsbroer.png')
lowbanner = PhotoImage(file = 'pictures/Banner.png')
root.title('Tom\'s Broer')
root.geometry("1000x800")
root.config(bg= 'white')
banner1 = Label(root, image = logo, width = 1920, bg = '#303135')
banner1.pack(pady=1)
banner2 = Label(root, image = lowbanner, bg = 'white')
banner2.pack( pady = 0, side = BOTTOM)
embed = Frame(root, width=499, height=550)
embed.pack(pady=1, side = LEFT)
entry = AutocompleteEntry(lista, root, width=25, font = ('Arial', 20))
entry.pack(pady=20, padx= 25,)
root.update()

if platform.system == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())

pygame.quit()
game_main()

# http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/