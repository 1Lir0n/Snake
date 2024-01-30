import ctypes
import json
from tkinter import *
import random
import os
from json import *

class SnakeGame:
    #parameters
    size = 10
    score = 0
    strScore=""
    textScore=None
    highScore=0
    start=False
    rndColor=False
    colorNum=1
    textColor="white"
    bgColor="black"

    #movement keys
    up="Up"
    down="Down"
    left="Left"
    right="Right"
    retry="space"
    exitK="Escape"

    #create a cache folder for high score
    if(not(os.path.exists("snakeCache"))):
        os.makedirs("snakeCache") 
        hs=open('./snakeCache/high_score.txt','w')
        hs.close()
    
    #initialize game
    def __init__(self, gameSize,cellSize,color,mode,keys):
        
        #create the window
        self.window = Tk()
        self.window.title("Snake Game")

        #canvas creation
        self.mode=mode
        self.changeMode()
        self.setSize(cellSize) 
        self.setCanvas(gameSize)
        self.canvas.pack()
        
        #score text
        self.strScore="Score: "+str(self.score)
        self.textScore=self.canvas.create_text(5,5,text=self.strScore,fill=self.textColor, font=("Helvetica", 11),anchor="nw")
    
    #snake creation
        #snake color
        self.color=color
        #snake location
        self.base=self.startPoint()

        #head snake creation
        self.snake = [(self.base, self.base)]
        self.setColor(self.color)
        
        #keys config
        self.setKeys(keys)

        #snake direction
        self.setDirection(self.base)

        #checks
        self.finish=IntVar(self.window)
        self.die=False

        #food creation
        self.food = self.spawnFood()

        #set highscore
        self.hs=open('./snakeCache/high_score.txt','r')
        self.highScore=self.hs.readline()
        self.hs.close()

        #player input
        self.window.bind("<Key>", self.handleKey)
        
        #loop
        self.update()
        self.window.update_idletasks()

        #active game window
        hwnd = ctypes.windll.user32.FindWindowW(None, "Snake Game")
        if hwnd:
            self.activateWindow(hwnd)
        else:
            print("Window not found.")
    
    #set keys from saved config
    def setKeys(self,keys):
            self.up=keys[0]
            self.down=keys[1]
            self.left=keys[2]
            self.right=keys[3]
            self.retry=keys[4]
            self.exitk=keys[5]

    #set dark/light mode from saved config
    def changeMode(self):
        if(self.mode=="light"):
            self.setTxtColor("black")
            self.setBG("white")
        else:
            self.setTxtColor("white")
            self.setBG("black")

    #rainbow colors
    def changeColor(self):
        self.colorNum+=1
        if(self.colorNum>=7):
            self.colorNum=1
        if(self.colorNum==1):
            self.setColor("green")
        elif(self.colorNum==2):
            self.setColor("blue")
        elif(self.colorNum==3):
            self.setColor("purple")
        elif(self.colorNum==4):
            self.setColor("red")
        elif(self.colorNum==5):
            self.setColor("orange")
        elif(self.colorNum==6):
            self.setColor("yellow")        

    # Activate the window using SetForegroundWindow
    def activateWindow(self,hwnd):
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    
    #player input decryption
    def handleKey(self, event):
        if event.keysym == "space":
            self.resetGame()
        elif event.keysym == "Escape":
            self.close()
        elif event.keysym in [self.up, self.down, self.left, self.right]:
            self.direction = event.keysym

    #game reset
    def resetGame(self):

        if self.die==False:
            return
        self.die=False
        self.retryB.destroy()
        self.exitB.destroy()
        self.menuB.destroy()
        self.canvas.delete("all")
        self.colorNum=1
        self.score=0
        self.textScore=self.canvas.create_text(5,5,text=self.strScore,fill=self.textColor, font=("Helvetica", 11),anchor="nw",tags="text")
        self.base=self.startPoint()
        self.snake = [(self.base, self.base)]
        self.setColor(self.color)
        self.setDirection(self.base)
        self.food = self.spawnFood()
        self.update()

    #closes the whole game 
    def close(self):
        exit()

    #spawn food at random 
    def spawnFood(self):
        x = random.randint(1, (self.width - self.size) // self.size) * self.size
        y = random.randint(11, (self.height - self.size) // self.size) * self.size
        food = self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill="red")
        return food

    #moves the snake one square
    def moveSnake(self):
        head = self.snake[0]
        move = {self.up: (0, -self.size), self.down: (0, self.size), self.left: (-self.size, 0), self.right: (self.size, 0)}
        new_head = (head[0] + move[self.direction][0], head[1] + move[self.direction][1])

        self.snake.insert(0, new_head)
        #checks for food collision
        if new_head == tuple(self.canvas.coords(self.food)[:2]):
            self.score+=10
            strScore="Score: "+str(self.score)
            self.canvas.itemconfig(self.textScore,text=strScore)
            self.canvas.delete(self.food)
            if(self.rndColor):
                self.changeColor()
            self.food = self.spawnFood()
        else:
            self.canvas.delete(self.snake[-1])
            self.snake.pop()

    #check if self collided
    def checkCollision(self):
        head = self.snake[0]
        return (
            head[0] < 0
            or head[0] >= self.width
            or head[1] < 0
            or head[1] >= self.height
            or head in self.snake[1:]
        )

    #update every frame
    def update(self):
        #if small grow big insta to start with 3 squares
        if(len(self.snake)<2):
            for i in range(2):
                head = self.snake[0]
                move = {self.up: (0, -self.size), self.down: (0, self.size), self.left: (-self.size, 0), self.right: (self.size, 0)}
                new_head = (head[0] + move[self.direction][0], head[1] + move[self.direction][1])
                self.snake.insert(0, new_head)
        #checks if the game run first time or reseted
        if(not self.start):
            self.countDown()
            self.window.wait_variable(self.finish)
        #if snake good pos move snake
        if not self.checkCollision():
            self.moveSnake()
            self.canvas.delete("snake")

            # Alternate between two color variant for the snake
            for i, (x, y) in enumerate(self.snake):
                color = self.snake_colors[i % 2]
                self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill=color, tags="snake")
            #loops
            self.window.after(100, self.update)
        else:
           #died
           self.deathScreen()

    #end game screen
    def deathScreen(self):
        self.die = True
        self.setHighScore()
        self.retryB = Button(self.window,text="Retry",command=self.resetGame,font=(16))
        self.retryB.place(relx=0.35,rely=0.6,anchor=CENTER,width=55)
        self.exitB = Button(self.window,text="Exit",command=self.close,font=(16))
        self.exitB.place(relx=0.65,rely=0.6,anchor=CENTER,width=55)
        self.menuB = Button(self.window,text="Menu",command=self.menu,font=(16))
        self.menuB.place(relx=0.5,rely=0.6,anchor=CENTER,width=55)
        self.canvas.create_text(
            self.width // 2, self.height // 2+20, text="HighScore: "+str(self.highScore), fill=self.textColor, font=("Helvetica", 16),tags="text"
        )
        self.canvas.create_text(
            self.width // 2, self.height // 2, text="Game Over", fill=self.textColor, font=("Helvetica", 16),tags="text"
        )
    
    #creates the main menu and delete the game
    def menu(self):
        self.window.destroy()
        menu = MainMenu()
        menu.start()

    #give a diff color
    def rainbowColor(self,input):
        if(input==1):
            return "green"
        elif(input==2):
            return "blue"
        elif(input==3):
            return "purple"
        elif(input==4):
            return "red"
        elif(input==5):
            return "orange"
        elif(input==6):
            return "yellow"
    
    #set the snake color
    def setColor(self,color):
        if((color)=="blue"):
            self.snake_colors = ["#3d9af2", "#0c6bc4"]
        elif((color)=="red"):
            self.snake_colors = ["#d63840", "#a6171e"]
        elif((color)=="yellow"):
            self.snake_colors = ["#fff82e", "#d6c313"]
        elif((color)=="orange"):
            self.snake_colors = ["#c45d14", "#8f3e04"]
        elif((color)=="purple"):
            self.snake_colors = ["#911ec7", "#5914a3"]
        elif((color)=="green"):
            self.snake_colors = ["#2b9e1e", "#124d17"]
        elif((color)=="rainbow"):
            self.rndColor = True
            self.setColor("green")

    #set the snake size
    def setSize(self,cellSize):
        if(str(cellSize).lower()=="small"):
            self.size = 5
        elif(str(cellSize).lower()=="medium"):
            self.size = 10
        elif(str(cellSize).lower()=="large"):
            self.size = 20
        else:
            print("invalid value")
            exit()
    
    #set the game window size
    def setCanvas(self,gameSize):
        if(str(gameSize).lower()=="small"):
            self.width = 300
            self.height = 300
        elif(str(gameSize).lower()=="medium"):
            self.width = 500
            self.height = 500
        elif(str(gameSize).lower()=="large"):
            self.width = 700
            self.height = 700
        else:
            print("invalid value")
            exit()
        self.canvas = Canvas(self.window, width=self.width, height=self.height, bg=self.bgColor)
        self.canvas.pack()
    
    #choose a random location for snake
    def startPoint(self):
        lower_limit = self.size
        upper_limit = self.width-self.size

        # Generate a random number within the specified range
        random_number = random.randint(lower_limit // self.size, upper_limit // self.size) * self.size

        return random_number

    #choose a random start direction for snake based on location
    def setDirection(self,base):
        # Define a list of possible directions
        directions = [self.up, self.down, self.right, self.left]

        if base < self.size*9:
            directions.remove(self.up) 
            directions.remove(self.left) 
        
        elif base > self.width-self.size*9:
            directions.remove(self.right) 
            directions.remove(self.down) 

        self.direction = str(random.choice(directions))
        
    #run the game
    def run(self):
        self.window.mainloop()

    #set the highscore to either the last or new one
    def setHighScore(self):
        with open('./snakeCache/high_score.txt', 'r') as hs_file:
            saved_high_score = hs_file.readline()

        if saved_high_score == '':
            self.highScore = 0
        else:
            self.highScore = int(saved_high_score)

        if self.score > self.highScore:
            with open('./snakeCache/high_score.txt', 'w') as hs_file:
                hs_file.write(str(self.score))
            self.highScore = self.score

    #simple count down
    def countDown(self, count=3):
        self.start=True
        if count > 0:
            self.canvas.delete("timer")
            self._text=self.canvas.create_text(250,250, text=str(count),fill=self.textColor, font=("Helvetica", 30),anchor=CENTER,tags=("timer","text"))
            self.window.after(1000, lambda: self.countDown(count-1))
            
        elif count == 0:
            self.canvas.delete("timer")
            self._text=self.canvas.create_text(250,250, text="Go!",fill=self.textColor, font=("Helvetica", 30),anchor=CENTER,tags=("timer","text"))
            self.window.after(500, lambda: self.canvas.delete("timer"))
            self.finish.set(1)

    #sets the windows background
    def setBG(self,input):
        self.bgColor=input
    
    #sets the text color
    def setTxtColor(self,input):
        self.textColor=input

#class 2
class MainMenu:
    textColor="white"
    bgColor="black"
    mode="dark"
    #player controls
    ctrl=False
    key=""
    up="Up"
    down="Down"
    left="Left"
    right="Right"
    retry="space"
    exitK="Escape"    

    def __init__(self):
        #create window
        self.window = Tk()
        self.window.title("Snake Game")
        self.width = 500
        self.height = 500
        self.canvas = Canvas(self.window, width=self.width, height=self.height, bg=self.bgColor)
        self.canvas.pack()

        #default paramaters
        self.cellSize="large"
        self.gameSize="medium"
        self.color="green"

        self.loadSettings()

        self.createMainMenu()
        self.g=IntVar(self.window)
        self.window.bind("<Key>", self.handleKey)
        self.window.update_idletasks()

        hwnd = ctypes.windll.user32.FindWindowW(None, "Snake Game")
        if hwnd:
            self.activateWindow(hwnd)
        else:
            print("Window not found.")

    #load settings from config
    def loadSettings(self):
        # Define the path to the settings file
        settings_file_path = './snakeCache/config.json'

        try:
            # Load the settings from the file
            with open(settings_file_path, 'r') as settings_file:
                settings = load(settings_file)

            # Update the current settings
            
            j=0
            self.keys=settings.get('keys','i')
            for key in self.keys:
                self.keys[j]=key
                j+=1
            self.up=self.keys[0]
            self.down=self.keys[1]
            self.left=self.keys[2]
            self.right=self.keys[3]
            self.retry=self.keys[4]
            self.exitk=self.keys[5]
            self.color = settings.get('color', 'green')
            self.cellSize = settings.get('cellSize', 'large')
            self.gameSize = settings.get('gameSize', 'medium')
            self.mode = settings.get('mode', 'dark')

            # Update the UI to reflect the loaded settings
            #self.changeMode()
            self.refreshCanvas()
        except Exception as e:
            print(f"Error loading settings: {e}")

    #save settings to the config
    def saveSettings(self):
        # Save current settings to the configuration file
        settings = {
            'keys': [self.up,self.down,self.left,self.right,self.retry,self.exitK],
            'color': self.color,
            'cellSize': self.cellSize,
            'gameSize': self.gameSize,
            'mode': self.mode
        }

        with open('./snakeCache/config.json', 'w') as settings_file:
            json.dump(settings, settings_file)

    #activate the main menu window
    def activateWindow(self,hwnd):
        # Activate the window using SetForegroundWindow
        ctypes.windll.user32.SetForegroundWindow(hwnd)

    #start the snake game
    def gameStart(self):
        self.window.destroy()
        self.saveSettings()  # Save settings before starting the game
        self.createGame()
        self.game.run()

    #player input decryption
    def handleKey(self, event):
        if(event.keysym=="Escape"):
            self.close()
        elif(self.ctrl):
            self.g.set(1)
            self.key=event.keysym

    #creates the main menu
    def createMainMenu(self):
        self._start = Button(self.window,text="Start",command=self.gameStart,width=7)
        self.option = Button(self.window,text="Options",command=self.optionMenu,width=7)
        self.exitB = Button(self.window,text="Exit",command=self.close,width=7)
        self._start.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.option.place(relx=0.5, rely=0.57, anchor=CENTER)
        self.exitB.place(relx=0.5, rely=0.639, anchor=CENTER)

        self.parmTextStr="SELECTED:\n   Color: "+str(self.color)+"\n   Snake Size: "+str(self.cellSize)+"\n   Game Size: "+str(self.gameSize)
        self.parmText=Canvas.create_text(self.canvas,5,self.height,text=self.parmTextStr,fill=self.textColor,anchor="sw",tags="text")
        
    #close the main menu
    def close(self):
        self.saveSettings()
        exit()

    #create the snake game
    def createGame(self):
        self.game=SnakeGame(self.gameSize,self.cellSize,self.color,self.mode,self.keys)

    #sets the snake color
    def setColor(self,input):
        if(input==1):
            self.color="green"
        elif(input==2):
            self.color="blue"
        elif(input==3):
            self.color="purple"
        elif(input==4):
            self.color="red"
        elif(input==5):
            self.color="orange"
        elif(input==6):
            self.color="yellow"
        elif(input==7):
            self.color="rainbow"
        if(input>0 and input<8):
            self.canvas.delete("all")
            self._color=self.canvas.create_text(self.width/2,self.height/2-50,text="Selected Color: "+self.color,anchor=CENTER,fill=self.textColor,tags="text")

    #sets the window color
    def setBG(self,input):
        self.bgColor=input
    
    #set the text color
    def setTxtColor(self,input):
        self.textColor=input
    
    #sets the snake size
    def setCellSize(self,input):
        if(input==1):
            self.cellSize="small" 
        elif(input==2):
            self.cellSize="medium"
        elif(input==3):
            self.cellSize="large" 
        if(input>0 and input<4):
            self.canvas.delete("all")
            self._color=self.canvas.create_text(self.width/2,self.height/2-50,text="Selected Size: "+self.cellSize,anchor=CENTER,fill=self.textColor,tags="text")

    #sets the window size
    def setGameSize(self,input):
        if(input==1):
            self.gameSize="small" 
        elif(input==2):
            self.gameSize="medium"
        elif(input==3):
            self.gameSize="large" 
        if(input>0 and input<4):
            self.canvas.delete("all")
            self._color=self.canvas.create_text(self.width/2,self.height/2-50,text="Selected Size: "+self.gameSize,anchor=CENTER,fill=self.textColor,tags="text")

    #recreate the main menu
    def backMenu(self):
        self.canvas.delete("all")
        self.delWidgets()
        self.createMainMenu()
        
    #delete all widgets exept for the canvas
    def delWidgets(self):
        self.widgets=self.window.winfo_children()
        for widget in self.widgets:
            if(not(str(widget)==".!canvas")):
                widget.destroy()

    #option menu gui
    def optionMenu(self):
        self.canvas.delete("all")
        self.delWidgets()
        self.back = Button(self.window,text="Back To Menu",command=self.backMenu,width=15)
        self.controls = Button(self.window,text="Controls",command=self.controlsMenu,width=10)
        self._optionCellSize = Button(self.window,text="Snake Size",command=self.optionCellSize,width=10)
        self._optionGameSize = Button(self.window,text="Game Size",command=self.optionGameSize,width=10)
        self._optionColor = Button(self.window,text="Snake Color",command=self.optionColor,width=10)
        self._optionMode = Button(self.window,text=self.mode+" mode",command=self.changeMode,width=10)
        self._optionMode.place(relx=0.5,rely=0.4,anchor=CENTER)
        self._optionCellSize.place(relx=0.3,rely=0.5,anchor=CENTER)
        self._optionColor.place(relx=0.5,rely=0.5,anchor=CENTER)
        self._optionGameSize.place(relx=0.7,rely=0.5,anchor=CENTER)
        self.controls.place(relx=0.5,rely=0.6,anchor=CENTER)
        self.back.place(relx=0.5,rely=0.7,anchor=CENTER)

    #control key menu
    def controlsMenu(self):
        self.delWidgets()
        self.canvas.delete("all")
        self.moveLabel=self.canvas.create_text(self.width//2,self.height//2-95,text="Movement",font=("Helvetica",24," underline"),fill=self.textColor,tags=("text","ctrl"),anchor=CENTER)
        self.menuLabel=self.canvas.create_text(self.width//2,self.height//2+75,text="Misc.",font=("Helvetica",24,"bold underline"),fill=self.textColor,tags=("text","ctrl"),anchor=CENTER)
        #key labels
        self.upLabel=self.canvas.create_text(self.width//2-2.5,self.height//2-60,text="Up:",font=("Helvetica",12),fill=self.textColor,tags=("text","ctrl"),anchor="e")
        self.downLabel=self.canvas.create_text(self.width//2-2.5,self.height//2-30,text="Down:",font=("Helvetica",12),fill=self.textColor,tags=("text","ctrl"),anchor="e")
        self.leftLabel=self.canvas.create_text(self.width//2-2.5,self.height//2-0,text="Left:",font=("Helvetica",12),fill=self.textColor,tags=("text","ctrl"),anchor="e")
        self.rightLabel=self.canvas.create_text(self.width//2-2.5,self.height//2+30,text="Right:",font=("Helvetica",12),fill=self.textColor,tags=("text","ctrl"),anchor="e")
        self.retryLabel=self.canvas.create_text(self.width//2-2.5,self.height//2+112,text="Retry:",font=("Helvetica",12),fill=self.textColor,tags=("text","ctrl"),anchor="e")
        self.exitLabel=self.canvas.create_text(self.width//2-2.5,self.height//2+142,text="Exit:",font=("Helvetica",12),fill=self.textColor,tags=("text","ctrl"),anchor="e")
        self.setOptionKeys()  
  
    #control key menu buttons
    def setOptionKeys(self):
        self.backK = Button(self.window,text="Back To Menu",command=self.backMenu,width=15)
        self.upButton=Button(self.window,text=self.up,command=lambda:self.changeKey(self.up),borderwidth=0,bg=self.bgColor,fg=self.textColor,font=("Helvetica",12,"underline"),height=1)
        self.downButton=Button(self.window,text=self.down,command=lambda:self.changeKey(self.down),borderwidth=0,bg=self.bgColor,fg=self.textColor,font=("Helvetica",12,"underline"),height=1)
        self.leftButton=Button(self.window,text=self.left,command=lambda:self.changeKey(self.left),borderwidth=0,bg=self.bgColor,fg=self.textColor,font=("Helvetica",12,"underline"),height=1)
        self.rightButton=Button(self.window,text=self.right,command=lambda:self.changeKey(self.right),borderwidth=0,bg=self.bgColor,fg=self.textColor,font=("Helvetica",12,"underline"),height=1)
        self.retryButton=Button(self.window,text=self.retry,command=lambda:self.changeKey(self.retry),borderwidth=0,bg=self.bgColor,fg=self.textColor,font=("Helvetica",12,"underline"),height=1)
        self.exitButton=Button(self.window,text=self.exitK,command=lambda:self.changeKey(self.exitK),borderwidth=0,bg=self.bgColor,fg=self.textColor,font=("Helvetica",12,"underline"),height=1)
        self.upButton.place(relx=0.5,rely=0.35)
        self.downButton.place(relx=0.5,rely=0.41)
        self.leftButton.place(relx=0.5,rely=0.47)
        self.rightButton.place(relx=0.5,rely=0.53)
        self.retryButton.place(relx=0.5,rely=0.69)
        self.exitButton.place(relx=0.5,rely=0.75)
        self.backK.place(relx=0.5,rely=0.85,anchor=CENTER)

    #changes key to a pressed one
    def changeKey(self,key):
        self.ctrl = True
        self.window.wait_variable(self.g)
        if(key==self.up):
            self.up=str(self.key)
        elif(key==self.down):
            self.down=str(self.key)
        elif(key==self.left):
            self.left=str(self.key)
        elif(key==self.right):
            self.right=str(self.key)
        elif(key==self.retry):
            self.retry=str(self.key)
        elif(key==self.exitK):
            self.exitK=str(self.key)
        self.delWidgets()
        self.setOptionKeys()
        
    #change light/dark mode
    def changeMode(self):
        if(self.mode=="dark"):
            self.mode="light"
            self.setTxtColor("black")
            self.setBG("white")
        else:
            self.mode="dark"
            self.setTxtColor("white")
            self.setBG("black")
        self.refreshCanvas()

    #refresh the data in the window
    def refreshCanvas(self):
        if(self.mode=="light"):
            self.setTxtColor("black")
            self.setBG("white")
        else:
            self.setTxtColor("white")
            self.setBG("black")
        self.canvas.configure(bg=self.bgColor)
        for item in self.canvas.find_withtag(tagOrId="text"):
            item.configure(fill=self.textColor)
        try:
            self._optionMode.configure(text=self.mode+" mode")
        except:
            pass

    #snake size menu
    def optionCellSize(self):
        self.canvas.delete("all")
        self.delWidgets()
        self._cellSize=self.canvas.create_text(self.width/2,self.height/2-50,text="Selected Size: "+self.cellSize,anchor=CENTER,fill=self.textColor,tags="text")
        self.back = Button(self.window,text="Back To Menu",command=self.backMenu,width=15)
        self.small = Button(self.window,text="Small",command=lambda:self.setCellSize(1),width=10)
        self.medium = Button(self.window,text="Medium",command=lambda:self.setCellSize(2),width=10)
        self.large = Button(self.window,text="Large",command=lambda:self.setCellSize(3),width=10)
        self.small.place(relx=0.3,rely=0.5,anchor=CENTER)
        self.medium.place(relx=0.5,rely=0.5,anchor=CENTER)
        self.large.place(relx=0.7,rely=0.5,anchor=CENTER)
        self.back.place(relx=0.5,rely=0.6,anchor=CENTER)

    #game size menu
    def optionGameSize(self):
        self.canvas.delete("all")
        self.delWidgets()
        self._gameSize=self.canvas.create_text(self.width/2,self.height/2-50,text="Selected Size: "+self.gameSize,anchor=CENTER,fill=self.textColor,tags="text")
        self.back = Button(self.window,text="Back To Menu",command=self.backMenu,width=15)
        self.small = Button(self.window,text="Small",command=lambda:self.setGameSize(1),width=10)
        self.medium = Button(self.window,text="Medium",command=lambda:self.setGameSize(2),width=10)
        self.large = Button(self.window,text="Large",command=lambda:self.setGameSize(3),width=10)
        self.small.place(relx=0.3,rely=0.5,anchor=CENTER)
        self.medium.place(relx=0.5,rely=0.5,anchor=CENTER)
        self.large.place(relx=0.7,rely=0.5,anchor=CENTER)
        self.back.place(relx=0.5,rely=0.6,anchor=CENTER)

    #color menu
    def optionColor(self):
        self.canvas.delete("all")
        self.delWidgets()
        self._color=self.canvas.create_text(self.width/2,self.height/2-50,text="Selected Color: "+self.color,anchor=CENTER,fill=self.textColor,tags="text")
        self.back = Button(self.window,text="Back To Menu",command=self.backMenu,width=15)
        self.green=Button(self.window,text="Green",command=lambda:self.setColor(1),width=5)
        self.blue=Button(self.window,text="Blue",command=lambda:self.setColor(2),width=5)
        self.purple=Button(self.window,text="Purple",command=lambda:self.setColor(3),width=5)
        self.red=Button(self.window,text="Red",command=lambda:self.setColor(4),width=5)
        self.orange=Button(self.window,text="Orange",command=lambda:self.setColor(5),width=5)
        self.yellow=Button(self.window,text="Yellow",command=lambda:self.setColor(6),width=5)
        self.rainbowColorB=Button(self.window,text="Rainbow",command=lambda:self.setColor(7),width=8)
        self.rainbowColorB.place(relx=0.5,rely=0.44,anchor=CENTER)
        self.green.place(relx=0.195,rely=0.5,anchor=CENTER)
        self.blue.place(relx=0.32,rely=0.5,anchor=CENTER)
        self.purple.place(relx=0.445,rely=0.5,anchor=CENTER)
        self.red.place(relx=0.57,rely=0.5,anchor=CENTER)
        self.orange.place(relx=0.695,rely=0.5,anchor=CENTER)
        self.yellow.place(relx=0.82,rely=0.5,anchor=CENTER)
        self.back.place(relx=0.5,rely=0.6,anchor=CENTER)

    #start the main menu
    def start(self):
        self.window.mainloop()
#end of game code


#start of run
game=MainMenu()
game.start()