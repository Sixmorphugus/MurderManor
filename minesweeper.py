# imports
import tkinter as tk
from random import randint

# define globals
GRID = []
GRIDDATA = []
GRIDOPEN = []
GRIDSIZE = 40
ROOT = tk.Tk()
MODE = tk.IntVar() # 0 - open, 1 - flag
OPENMODE = None
FLAGMODE = None
MENU = tk.Menu(ROOT)
FILEMENU = tk.Menu(MENU, tearoff=0)
GAMEMENU = tk.Menu(MENU, tearoff=0)
NUMMINES = 200
FIRSTTURN = True

ROOT.title("SUPER MINESWEEPER")

# functions
def setupWindow():
  global ROOT, GRID, GRIDDATA, GRIDSIZE, GRIDOPEN, OPENMODE, FLAGMODE, FIRSTTURN

  if(GRID != []):
    # clear the grid buttons
    for x in range(0, len(GRID)):
      for y in range(0, len(GRID[x])):
        GRID[x][y].destroy()
    
  if(OPENMODE != None):
    OPENMODE.destroy()

  if(FLAGMODE != None):
    FLAGMODE.destroy()

  GRID = []
  GRIDDATA = []
  GRIDOPEN = []
  
  FIRSTTURN = True

  for x in range(0, GRIDSIZE):
    gridRow = []
    gridDataRow = []
    gridOpenRow = []
    
    for y in range(0, GRIDSIZE):
      newGridSpace = tk.Button(ROOT, width=2, height=1, command=(lambda x=x, y=y: revealSquare(x, y, False)))
      newGridSpace.grid(row=x, column=y, sticky="nesw")

      newGridSpace.bind("<ButtonRelease-3>", (lambda event, x=x, y=y: flagSquare(x, y)))
      
      gridRow.append(newGridSpace)
      gridDataRow.append(False)
      gridOpenRow.append(False)
      
      ROOT.rowconfigure(y, weight=1)

    GRID.append(gridRow)
    GRIDDATA.append(gridDataRow)
    GRIDOPEN.append(gridOpenRow)
    ROOT.columnconfigure(x, weight=1)

  #OPENMODE = tk.Radiobutton(ROOT, text="Open Box", value=0, variable=MODE);
  #OPENMODE.grid(column=0, row=GRIDSIZE, columnspan=(GRIDSIZE // 2), sticky="we")
  
  #FLAGMODE = tk.Radiobutton(ROOT, text="Flag Box", value=1, variable=MODE);
  #FLAGMODE.grid(column=(GRIDSIZE // 2), row=GRIDSIZE, columnspan=(GRIDSIZE // 2), sticky="we")

def posDown(x, y):
  global MODE
  
  if(MODE.get() == 0):
    revealSquare(x, y, False)
  else:
    flagSquare(x, y)

def revealSquare(x, y, safe):
  global GRIDDATA, GRIDOPEN, GRID, FIRSTTURN

  if(FIRSTTURN):
    FIRSTTURN = False
    generateFrom(x, y)

  # real square?
  if(x < 0 or y < 0 or x >= len(GRIDDATA) or y >= len(GRIDDATA)):
    return

  # enabled?
  if(GRIDOPEN[x][y]):
    return
  
  # reveal this square
  minesAround = getNumMinesAround(x, y);
  disp = " "
  col = "red"
  
  if(minesAround > 0):
    disp = minesAround

    if(minesAround == 1):
      col = "blue"
    elif(minesAround == 2):
      col = "green"
    elif(minesAround == 3):
      col = "yellow"
    elif(minesAround >= 4):
      col = "red"

  if(GRIDDATA[x][y]):
    disp = "BOOM"
  
  if(safe and GRIDDATA[x][y]):
    return
  
  GRID[x][y].config(text=disp, relief="sunken", fg=col)
  GRIDOPEN[x][y] = True

  if(GRIDDATA[x][y]):
    for x2 in range(len(GRID)):
      for y2 in range(len(GRID)):
        disp = " "

        minesAround = getNumMinesAround(x2, y2);
        
        if(minesAround > 0):
          disp = minesAround

        if(GRIDDATA[x2][y2]):
          disp = "BOOM"
        
        GRID[x2][y2].config(text=disp, state="disabled")

  # reveal squares next to this one
  if(minesAround == 0):
    revealSquare(x, y-1, True)
    revealSquare(x+1, y-1, True)
    revealSquare(x+1, y, True)
    revealSquare(x+1, y+1, True)
    revealSquare(x, y+1, True)
    revealSquare(x-1, y+1, True)
    revealSquare(x-1, y, True)
    revealSquare(x-1, y-1, True)


def flagSquare(x, y):
  global GRID, GRIDOPEN

  if(GRIDOPEN[x][y]):
    return

  if(GRID[x][y].cget('text') == "M"):
    GRID[x][y].config(text="")
  else:
    GRID[x][y].config(text="M")

def generateFrom(x, y):
  global GRIDDATA, NUMMINES
  
  # place random mines
  for i in range(NUMMINES):
    mineX = randint(0, len(GRIDDATA)-1)
    mineY = randint(0, len(GRIDDATA)-1)

    if((mineX == x and mineY == y)):
      # go again
      i -= 1
      continue

    # create
    GRIDDATA[mineX][mineY] = True

    if(getNumMinesAround(x, y) != 0):
      # uncreate
      GRIDDATA[mineX][mineY] = False

      # go again
      i -= 1

def mineAt(x, y):
  global GRIDDATA
  # real square?
  if(x < 0 or y < 0 or x >= len(GRIDDATA) or y >= len(GRIDDATA)):
    return

  # do the check
  return GRIDDATA[x][y]

def getNumMinesAround(x, y):
  global GRIDDATA
  numMines = 0
  size = len(GRIDDATA)
  
  # north
  if(mineAt(x,y-1)):
    numMines += 1
    
  if(mineAt(x+1, y-1)):
    numMines += 1

  if(mineAt(x+1, y)):
    numMines += 1

  # south east
  if(mineAt(x+1, y+1)):
    numMines += 1
    
  if(mineAt(x, y+1)):
    numMines += 1

  # south west
  if(mineAt(x-1, y+1)):
    numMines += 1

  # west
  if(mineAt(x-1, y)):
    numMines += 1

  # north west
  if(mineAt(x-1, y-1)):
    numMines += 1

  return numMines

# program code
# setup the menu
ROOT.config(menu=MENU)

FILEMENU.add_command(label="New", command=setupWindow)
FILEMENU.add_command(label="Save")
FILEMENU.add_command(label="Load")
FILEMENU.add_separator()
FILEMENU.add_command(label="Exit", command=ROOT.destroy)
MENU.add_cascade(label="Game", menu=FILEMENU)

GAMEMENU.add_checkbutton(label="Show Mines On Game End")
GAMEMENU.add_separator()
GAMEMENU.add_command(label="Grid Size...")
GAMEMENU.add_command(label="Mine Placement...")
GAMEMENU.add_command(label="Appearence...")
MENU.add_cascade(label="Options", menu=GAMEMENU)

setupWindow();
