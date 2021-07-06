from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mbox
from functools import partial
from itertools import product
import matplotlib.pyplot as plt
import threading, time, re, math
from PIL import Image

def trainingThread(pWinClass):
        while pWinClass.exitThread == False:
            if pWinClass.trainBtnPress:
                pWinClass.netStatus.set("Training")
                pWinClass.btnTrain["state"] = DISABLED
                pWinClass.plotBtn["state"] = DISABLED
                pWinClass.networkErrorData = pWinClass.network.trainNetwork(
                    pWinClass.inputs[0], 
                    pWinClass.inputs[1])
                print("Network trained!!!!")
                pWinClass.btnTrain["state"] = NORMAL
                pWinClass.plotBtn["state"] = NORMAL
                pWinClass.trainBtnPress = False
                pWinClass.showPlot = True
                pWinClass.netStatus.set("Trained")

            elif pWinClass.showPlot:
                pWinClass.showPlot = False
                pWinClass.plotBtn.grid(row=1, column=0)
                # pWinClass.plotBtn.invoke()
                
            time.sleep(0.5)
        

        

class TrainingWindow:
    def __init__(self, pParentWin, pNetwork):
        self.parentWin = pParentWin
        self.network = pNetwork
        self.exitThread = False
        self.trainBtnPress = False
        self.showPlot = False
        self.networkErrorData = []

        self.win = Toplevel(pParentWin.win)
        self.win.minsize(width=320, height=240)
        self.win.resizable(False, False)
        # self.win.maxsize(width=480, height=360)
        self.win.title("Training")
        self.win.protocol("WM_DELETE_WINDOW", self.hide)

        self.mainFrame = Frame(self.win)
        self.mainFrame.pack(side="top", fill="both", expand=True)
        self.mainFrame.rowconfigure((0,2), weight=1)
        self.mainFrame.rowconfigure(1, weight=2)
        self.mainFrame.columnconfigure(0, weight=1)

        self.thread = threading.Thread(target=trainingThread, args=(self,))
        self.thread.setDaemon(True)
        self.thread.start()

        self.createUIElements()
        self.win.withdraw()
        

    def show(self):
        self.win.deiconify()
        self.win.mainloop()

    def hide(self):
        self.win.withdraw()
        self.parentWin.trainingWinOpen = False

    def close(self):
        # self.parentWin.trainingWinOpen = False
        self.exitThread = True
        self.thread.join()
        self.win.destroy()

    def trainNetwork(self):
        sets = self.entryTrainingSets.get()
        epochs = self.entryEpochs.get()

        if (re.fullmatch('^[0-9]+$',sets) and re.fullmatch('^[0-9]+$',epochs)):
            self.inputs = [int(self.entryTrainingSets.get()), int(self.entryEpochs.get())]
            self.trainBtnPress = True
        

    def plotNetworkError(self):
        errorPlot = plt.plot(self.networkErrorData[0], self.networkErrorData[1])
        plt.suptitle("Error value of neural network")
        minStr = "Final error: " + str(round(self.networkErrorData[1][-1], 4))
        plt.title(minStr, fontsize=9)
        plt.xlabel("Number of epochs")
        plt.ylabel("Error")
        plt.show()
        # self.showPlot = False

    def createUIElements(self):
        #Create frames
        self.titleFrame = Frame(self.mainFrame, height=50)
        self.titleFrame.grid(row=0, column=0, padx=2, pady=2, sticky=W+E+N+S)

        self.inputFrame = Frame(self.mainFrame, height=140)
        self.inputFrame.grid(row=1, column=0, padx=2, pady=2, sticky=W+E+N+S)
        self.inputFrame.rowconfigure((0,1), weight=1)
        self.inputFrame.columnconfigure((0,1), weight=1)

        self.btnFrame = Frame(self.mainFrame, height=50)
        self.btnFrame.grid(row=2, column=0, padx=2, pady=2, sticky=W+E+N+S)
        self.btnFrame.rowconfigure((0,1), weight=1)
        self.btnFrame.columnconfigure(0, weight=1)

        #Status indicator
        self.netStatus = StringVar()
        self.netStatus.set("Not trained")
        self.statusLabel = Label(self.titleFrame, textvariable=self.netStatus)
        self.statusLabel.config(font=('Verdana', 20))
        self.statusLabel.pack()

        #Inputs
        label = Label(self.inputFrame, text="Training images: ")
        label.grid(row=0, column=0, padx=2, pady=2)
        
        self.entryTrainingSets = Entry(self.inputFrame)
        self.entryTrainingSets.grid(row=0, column=1, padx=2, pady=2)

        label = Label(self.inputFrame, text="Epochs: ")
        label.grid(row=1, column=0, padx=2, pady=2)

        self.entryEpochs = Entry(self.inputFrame)
        self.entryEpochs.grid(row=1, column=1, padx=2, pady=2)

        #Buttons
        self.btnTrain = Button(self.btnFrame, text="Train neural network", command=partial(self.trainNetwork))
        self.btnTrain.grid(row=0, column=0)

        self.plotBtn = Button(self.btnFrame, text="Plot error", command=partial(self.plotNetworkError))
        self.plotBtn.grid(row=1, column=0)
        self.plotBtn.grid_forget()
        



##########################################################################################
class UI:
    buttonIds = []
    whitePixels = 100

    def __init__(self, pRows, pCols, pImage, pNetwork):
        self.network = pNetwork
        self.positions = product(range(pRows), range(pCols))
        self.trainingWinOpen = False

        self.win = Tk()
        self.win.minsize(width=480, height=360)
        # self.win.maxsize(width=480, height=360)
        self.win.title("Retina")
        self.win.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.trainingWin = TrainingWindow(self, self.network)

        self.createFrames()
        self.createImageButtons(pImage)
        self.addElements(pImage)

    def onClosing(self):
        self.trainingWin.close()
        self.win.destroy()

    
    """
        Changes the color of a "pixel" when a button is pressed
    """
    def changeBtnColor(self, pIdx, pImage):
        bname = (self.buttonIds[pIdx])
        row = int(pIdx/10)
        col = pIdx - (row * 10)
        if bname.cget('bg') == 'black':
            bname.configure(bg='white')
            self.whitePixels += 1
        else:
            bname.configure(bg='black')
            self.whitePixels -= 1

        # pImage[row][col] = 1 - pImage[row][col]
        pImage[0][pIdx] = 1 - pImage[0][pIdx]
        self.textVarWhite.set(str(self.whitePixels))
        self.textVarBlack.set(str(100 - self.whitePixels))        

    """
        Toggles the image to all black or all white
    """
    def toggleColor(self, pColor, pImage):
        if pColor == 'white':
            color = 1
            self.whitePixels = 100
        else:
            color = 0
            self.whitePixels = 0
        
        for (idx, btn) in enumerate(self.buttonIds):
            row = int(idx/10)
            col = idx - (row * 10)
            btn.configure(bg=pColor)
            pImage[0][idx] = color

        self.textVarWhite.set(str(self.whitePixels))
        self.textVarBlack.set(str(100 - self.whitePixels))   

    """
        Open a file explorer to select the image to load
    """
    def selectImage(self, pImage):
        filename = fd.askopenfile(
            title= 'Select the image',
            initialdir= '/home',
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("All files", "*")
            ]
        )

        if filename:
            self.loadImage(filename.name, pImage)


    """
        Loads a 10x10 black and white image
    """
    def loadImage(self, pFilename, pImage):
        image = Image.open(pFilename)
        pixels = image.load()

        if image.size == (10,10):

            self.whitePixels = 0

            for j in range(10):
                for i in range(10):
                    value = 0 if pixels[i,j]==0 else 1
                    # pImage[i][j] = value
                    pImage[0][(i * 10) + j] = value

                    button = self.buttonIds[(i * 10) + j]
                    if value:
                        button.configure(bg='white')
                        self.whitePixels += 1
                    else:
                        button.configure(bg='black')

            self.textVarWhite.set(str(self.whitePixels))
            self.textVarBlack.set(str(100 - self.whitePixels))   


    
    def openTrainingWin(self):
        if self.trainingWinOpen == False:
            self.trainingWinOpen = True
            self.trainingWin.show()



    def processImage(self, pImage):
        if self.network.trained == False:
            mbox.showwarning(title="Warning", 
                message="Neural network has not been trained!")

        result = self.network.analize(pImage)
        print(result)
        result = int(round(result[0][0], 0))
        if result:
            self.textVarResult.set("Bright image")
        else:
            self.textVarResult.set("Dark image")
          

    """
        Creates the different frames where the UI 
        elements will be placed
    """
    def createFrames(self):
        self.mainFrame = Frame(self.win)
        self.mainFrame.pack(side="top", fill="both", expand=True)
        self.mainFrame.rowconfigure(tuple(range(4)), weight=1)
        self.mainFrame.columnconfigure(0, weight=2)
        self.mainFrame.columnconfigure(1, weight=1)

        self.titleFrame = Frame(self.mainFrame, height=50)
        self.titleFrame.grid(row=0, column=0, padx=2, pady=2, sticky = W+E+N+S)

        self.imageFrame = Frame(self.mainFrame, width=400, height=300)
        self.imageFrame.grid(row=1, column=0, padx=2, pady=2)
        self.imageFrame.rowconfigure(tuple(range(10)), weight=1)
        self.imageFrame.columnconfigure(tuple(range(10)), weight=1)

        self.optionsFrame = Frame(self.mainFrame, height=50)
        self.optionsFrame.grid(row=2, column=0, padx=2, pady=2, sticky = W+E+N+S)

        self.infoFrame = Frame(self.mainFrame, width=200, height=300)
        self.infoFrame.grid(row=0, column=1, rowspan=3, padx=2, pady=2, sticky = W+E+N+S)
        self.infoFrame.rowconfigure(tuple(range(4)), weight=1)
        self.infoFrame.columnconfigure(tuple(range(2)), weight=1)

        self.resultFrame = Frame(self.mainFrame, height=60)
        self.resultFrame.grid(row=3, column=0, padx=2, pady=2, columnspan=2, sticky = W+E+N+S)

    
    """
        Create the grid of buttons representing the 10x10 image
    """
    def createImageButtons(self, pImage):
        for idx, item in enumerate(self.positions):
            button = Button(self.imageFrame, bg='white', command=partial(self.changeBtnColor, idx, pImage))
            button.grid(row=item[0], column=item[1], sticky = W+E+N+S)
            self.buttonIds.append(button)


    """
        Adds the rest of UI elements, such as labels and buttons
    """
    def addElements(self, pImage):
        #Image label
        label = Label(self.titleFrame, text="Image")
        label.config(font=('Verdana', 20))
        label.pack()

        #Color options and load image buttons
        blackBtn = Button(self.optionsFrame, text="Black", command=partial(self.toggleColor, 'black', pImage))
        blackBtn.pack(side=LEFT)

        whiteBtn = Button(self.optionsFrame, text="White", command=partial(self.toggleColor, 'white', pImage))
        whiteBtn.pack(side=LEFT)

        loadBtn = Button(self.optionsFrame, text="Load", command=partial(self.selectImage, pImage))
        loadBtn.pack(side=RIGHT)

        #Info about pixels
        label = Label(self.infoFrame, text="Information")
        label.config(font=('Verdana', 20))
        label.grid(row=0, column=0, columnspan=2, sticky = W+E+N)

        label = Label(self.infoFrame, text="White pixels = ")
        label.config(font=('Verdana', 14))
        label.grid(row=1, column=0, sticky = W+E+N)

        self.textVarWhite = StringVar()
        self.textVarWhite.set(str(self.whitePixels))
        self.whitePxLabel = Label(self.infoFrame, textvariable=self.textVarWhite)
        self.whitePxLabel.config(font=('Verdana', 14))
        self.whitePxLabel.grid(row=1, column=1, sticky = W+E+N)

        label = Label(self.infoFrame, text="Black pixels = ")
        label.config(font=('Verdana', 14))
        label.grid(row=2, column=0, sticky = W+E+N)

        self.textVarBlack = StringVar()
        self.textVarBlack.set(str(100 - self.whitePixels))
        self.blackPxLabel = Label(self.infoFrame, textvariable=self.textVarBlack)
        self.blackPxLabel.config(font=('Verdana', 14))
        self.blackPxLabel.grid(row=2, column=1, sticky = W+E+N)

        button = Button(self.infoFrame, text="Training", command=partial(self.openTrainingWin))
        button.grid(row=3, column=0, columnspan=2)

        #Result labels and process button
        label = Label(self.resultFrame, text="Result: ")
        label.config(font=('Verdana', 20))
        label.pack(side=LEFT)

        self.textVarResult = StringVar()
        self.textVarResult.set("Undefined")
        self.resultLabel = Label(self.resultFrame, textvariable=self.textVarResult)
        self.resultLabel.config(font=('Verdana', 20))
        self.resultLabel.pack(side=LEFT) 

        button = Button(self.resultFrame, text="Process", command=partial(self.processImage, pImage))
        button.pack(side=RIGHT, padx=20)
        

    def show(self):
        self.win.mainloop()