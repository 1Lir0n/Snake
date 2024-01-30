import ctypes
import json
from tkinter import *
import random
import os
from json import *

class SnakeGame:
    size = 10
    score = 0
    strScore=""
    textScore=None
    highScore=0
    start=False
    rndColor=False
    input=2
    textColor="white"
    bgColor="black"

    #create a cache folder for high score
    if(not(os.path.exists("snakeCache"))):
        os.makedirs("snakeCache") 
        hs=open('./snakeCache/high_score.txt','w')
        hs.close()
    
    def __init__(self, gameSize,cellSize,color,mode):
        
        self.window = Tk()
        self.window.title("Snake Game")
        self.mode=mode
        self.changeMode()
        self.setSize(cellSize) 
        self.setCanvas(gameSize)
        self.canvas.pack()
        self.strScore="Score: "+str(self.score)
        self.textScore=self.canvas.create_text(5,5,text=self.strScore,fill=self.textColor, font=("Helvetica", 11),anchor="nw")
        self.color=color
        
        self.base=self.startPoint()
        self.setDirection(self.base)
        self.snake = [(self.base, self.base)]
        self.setColor(self.color)

        self.finish=IntVar(self.window)

        self.die=False

        self.food = self.spawn_food()

        #set highscore
        self.hs=open('./snakeCache/high_score.txt','r')
        self.highScore=self.hs.readline()
        self.hs.close()

        self.window.bind("<Key>", self.handle_key)
        self.update()
        self.window.update_idletasks()

        hwnd = ctypes.windll.user32.FindWindowW(None, "Snake Game")
        if hwnd:
            self.activate_window(hwnd)
        else:
            print("Window not found.")
    
    def changeMode(self):
        if(self.mode=="light"):
            self.setTxtColor("black")
            self.setBG("white")
        else:
            self.setTxtColor("white")
            self.setBG("black")

    def activate_window(self,hwnd):
        # Activate the window using SetForegroundWindow
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    
    def handle_key(self, event):
        if event.keysym == "space":
            self.reset_game()
        elif event.keysym == "Escape":
            self.close()
        elif event.keysym in ["Up", "Down", "Left", "Right"]:
            self.direction = event.keysym

    def reset_game(self):

        if self.die==False:
            return
        self.die=False
        self.retryB.destroy()
        self.exitB.destroy()
        self.menuB.destroy()
        self.canvas.delete("all")
        self.score=0
        self.textScore=self.canvas.create_text(5,5,text=self.strScore,fill=self.textColor, font=("Helvetica", 11),anchor="nw",tags="text")
        self.base=self.startPoint()
        self.snake = [(self.base, self.base)]
        self.setColor(self.color)
        self.setDirection(self.base)
        self.food = self.spawn_food()
        self.update()

    def close(self):
        exit()
        #self.window.destroy()

    def spawn_food(self):
        x = random.randint(1, (self.width - self.size) // self.size) * self.size
        y = random.randint(11, (self.height - self.size) // self.size) * self.size
        food = self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill="red")
        return food

    def move_snake(self):
        head = self.snake[0]
        move = {"Up": (0, -self.size), "Down": (0, self.size), "Left": (-self.size, 0), "Right": (self.size, 0)}
        new_head = (head[0] + move[self.direction][0], head[1] + move[self.direction][1])

        self.snake.insert(0, new_head)

        if new_head == tuple(self.canvas.coords(self.food)[:2]):
            self.score+=10
            strScore="Score: "+str(self.score)
            self.canvas.itemconfig(self.textScore,text=strScore)
            self.canvas.delete(self.food)
            self.food = self.spawn_food()
        else:
            self.canvas.delete(self.snake[-1])
            self.snake.pop()

    def check_collision(self):
        head = self.snake[0]
        return (
            head[0] < 0
            or head[0] >= self.width
            or head[1] < 0
            or head[1] >= self.height
            or head in self.snake[1:]
        )

    def update(self):
        
        if(self.rndColor):
            self.setColor(self.rainbowColor(self.input/2))
            if(self.input<14):
                self.input=self.input+1
            else:
                self.input=1

        if(len(self.snake)<2):
            for i in range(2):
                head = self.snake[0]
                move = {"Up": (0, -self.size), "Down": (0, self.size), "Left": (-self.size, 0), "Right": (self.size, 0)}
                new_head = (head[0] + move[self.direction][0], head[1] + move[self.direction][1])
                self.snake.insert(0, new_head)
        if(not self.start):
            self.countDown()
        
            self.window.wait_variable(self.finish)
        if not self.check_collision():
            self.move_snake()
            self.canvas.delete("snake")

            # Alternate between two colors
            for i, (x, y) in enumerate(self.snake):
                color = self.snake_colors[i % 2]
                self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill=color, tags="snake")

            self.window.after(100, self.update)
        else:
           self.deathScreen()

    def deathScreen(self):
        self.die = True
        self.setHighScore()
        self.retryB = Button(self.window,text="Retry",command=self.reset_game,font=(16))
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
    
    def menu(self):
        self.window.destroy()
        menu = MainMenu()
        menu.start()

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
    
    def startPoint(self):
        lower_limit = self.size
        upper_limit = self.width-self.size

        # Generate a random number within the specified range
        random_number = random.randint(lower_limit // self.size, upper_limit // self.size) * self.size

        return random_number

    def setDirection(self,base):
        # Define a list of possible directions
        directions = ["Up", "Down", "Right", "Left"]

        if base < self.size*9:
            directions.remove("Up") 
            directions.remove("Left") 
        
        elif base > self.width-self.size*9:
            directions.remove("Right") 
            directions.remove("Down") 

        self.direction = str(random.choice(directions))
        
    def run(self):
        self.window.mainloop()

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

    def setBG(self,input):
        self.bgColor=input
    
    def setTxtColor(self,input):
        self.textColor=input

#class 2
class MainMenu:
    textColor="white"
    bgColor="black"
    mode="dark"

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

        self.window.bind("<Key>", self.handle_key)
        self.window.update_idletasks()

        hwnd = ctypes.windll.user32.FindWindowW(None, "Snake Game")
        if hwnd:
            self.activate_window(hwnd)
        else:
            print("Window not found.")

    def loadSettings(self):
        # Define the path to the settings file
        settings_file_path = './snakeCache/settings.json'

        try:
            # Load the settings from the file
            with open(settings_file_path, 'r') as settings_file:
                settings = load(settings_file)

            # Update the current settings
            self.color = settings.get('color', 'green')
            self.cellSize = settings.get('cellSize', 'large')
            self.gameSize = settings.get('gameSize', 'medium')
            self.mode = settings.get('mode', 'dark')

            # Update the UI to reflect the loaded settings
            #self.changeMode()
            self.refreshCanvas()
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        # Save current settings to the configuration file
        settings = {
            'color': self.color,
            'cellSize': self.cellSize,
            'gameSize': self.gameSize,
            'mode': self.mode
        }

        with open('./snakeCache/settings.json', 'w') as settings_file:
            json.dump(settings, settings_file)

    def activate_window(self,hwnd):
        # Activate the window using SetForegroundWindow
        ctypes.windll.user32.SetForegroundWindow(hwnd)

    def gameStart(self):
        self.window.destroy()
        self.save_settings()  # Save settings before starting the game
        self.createGame()
        self.game.run()

    def handle_key(self, event):
        if(event.keysym=="Escape"):
            self.close()

    def createMainMenu(self):
        self._start = Button(self.window,text="Start",command=self.gameStart,width=7)
        self.option = Button(self.window,text="Options",command=self.optionMenu,width=7)
        self.exitB = Button(self.window,text="Exit",command=self.close,width=7)
        self._start.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.option.place(relx=0.5, rely=0.57, anchor=CENTER)
        self.exitB.place(relx=0.5, rely=0.639, anchor=CENTER)

        self.parmTextStr="SELECTED:\n   Color: "+str(self.color)+"\n   Snake Size: "+str(self.cellSize)+"\n   Game Size: "+str(self.gameSize)
        self.parmText=Canvas.create_text(self.canvas,5,self.height,text=self.parmTextStr,fill=self.textColor,anchor="sw",tags="text")
        
    def close(self):
        self.save_settings()
        exit()

    def createGame(self):
        self.game=SnakeGame(self.gameSize,self.cellSize,self.color,self.mode)

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

    def setBG(self,input):
        self.bgColor=input
    
    def setTxtColor(self,input):
        self.textColor=input
        
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

    def backMenu(self):
        self.canvas.delete("all")
        self.delWidgets()
        self.createMainMenu()
        
    def delWidgets(self):
        self.widgets=self.window.winfo_children()
        for widget in self.widgets:
            if(not(str(widget)==".!canvas")):
                widget.destroy()

    def optionMenu(self):
        self.canvas.delete("all")
        self.delWidgets()
        self.back = Button(self.window,text="Back To Menu",command=self.backMenu,width=15)
        self._optionCellSize = Button(self.window,text="Snake Size",command=self.optionCellSize,width=10)
        self._optionGameSize = Button(self.window,text="Game Size",command=self.optionGameSize,width=10)
        self._optionColor = Button(self.window,text="Snake Color",command=self.optionColor,width=10)
        self._optionMode = Button(self.window,text=self.mode+" mode",command=self.changeMode)
        self._optionMode.place(relx=0.5,rely=0.4,anchor=CENTER)
        self._optionCellSize.place(relx=0.3,rely=0.5,anchor=CENTER)
        self._optionColor.place(relx=0.5,rely=0.5,anchor=CENTER)
        self._optionGameSize.place(relx=0.7,rely=0.5,anchor=CENTER)
        self.back.place(relx=0.5,rely=0.6,anchor=CENTER)

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

    def start(self):
        self.window.mainloop()
#end of game code


#start of run
game=MainMenu()
game.start()