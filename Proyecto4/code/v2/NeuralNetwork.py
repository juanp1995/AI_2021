import numpy as np
import pylab as plt

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sigmoidDer(x):
    return sigmoid(x) * (1.0 - sigmoid(x))

def relu(x):
    return np.maximum(x, 0)

def reluDer(x):
    return np.where(x<=0, 0.0, 1 if np.any(x)!=0 else 0.0)

class NeuralNetwork:
    def __init__(self):
        self.trained = False
        self.learningRate = 0.005
        self.inputs = 100           #Each pixel of the 10x10 image
        self.hiddenLayer1 = 65      #Nodes in hidden layer 1
        self.hiddenLayer2 = 40      #Nodes in hidden layer 2
        self.outputLayer = 1        #Nodes in ouput layer       

        #Weights of connections between layers
        self.weightHidden1 = np.array(
            [np.random.uniform(-0.5,0.5, self.hiddenLayer1) for _ in range(self.inputs)])
        self.weightHidden2 = np.array(
            [np.random.uniform(-0.5,0.5, self.hiddenLayer2) for _ in range(self.hiddenLayer1)])
        self.weightOutput = np.array(
            [np.random.uniform(-0.5,0.5, self.outputLayer) for _ in range(self.hiddenLayer2)])


    def cases(self):
        self.trainingImages.append(np.zeros(100, dtype=int))    #Black image
        self.trainingImages.append(np.ones(100, dtype=int))     #White image

        #50-50 black and white
        self.trainingImages.append(np.concatenate((np.zeros(50, dtype=int), np.ones(50, dtype=int))))
        self.trainingImages.append(np.concatenate((np.ones(50, dtype=int), np.zeros(50, dtype=int))))

        flag = True
        img1, img2 = list(), list()
        for j in range(10):
            for i in range(10):
                if flag:
                    img1.append(1)
                    img2.append(0)
                    flag = False
                else:
                    img1.append(0)
                    img2.append(1)
                    flag =True

        self.trainingImages.append(img1)
        self.trainingImages.append(img2)

    def createTrainingData(self):
        #Create random "images" for training
        self.trainingImages = [np.random.randint(0, 2, 100) for _ in range(self.trainingSets-6)]
        self.cases() #Specific cases of images (all black, all white, etc)
        self.trainingImages = np.array(self.trainingImages)

        #Calcute the target output for each training image
        self.targetOutput = []
        for img in self.trainingImages:
            countArray = np.bincount(img, minlength=2) 
            whitePixels = countArray[1]
            target = 0
            if (whitePixels/100) <= 0.5: 
                target = 0
            else:
                target = 1
            self.targetOutput.append(target)
            # self.targetOutput.append(whitePixels/100)
            

        self.targetOutput = np.array(self.targetOutput).reshape(self.trainingSets,1)

    def trainNetwork(self, pTrainingSets, pEpochs):
        self.trainingSets = pTrainingSets
        self.epochs = pEpochs
        self.createTrainingData()

        epochs = list(range(self.epochs))
        
        error = []

        #--- LIVE PLOT -- DON'T USE IT!!!
        # epochsPlot = []
        # plt.ion()
        # figure, ax = plt.subplots()
        # lines, = ax.plot([],[])
        # ax.set_autoscale_on(True)
        prevErrorOut = []
        for epoch in range(self.epochs):
            #---- Hidden layer 1
            #Input for hidden layer 1
            inputHidden1 = np.dot(self.trainingImages, self.weightHidden1)
            #Output from hidden layer 1
            outputHidden1 = sigmoid(inputHidden1)

            #---- Hidden layer 2
            #Input for hidden layer 2
            inputHidden2 = np.dot(outputHidden1, self.weightHidden2)
            #Ouput from hidden layer 2
            outputHidden2 = sigmoid(inputHidden2)

            #Ouput layer
            #Input for output layer
            inputOut = np.dot(outputHidden2, self.weightOutput)
            #Output from output layer
            outputOut = sigmoid(inputOut)

            #---------------------------
            #Phase 1
            #Calculate Mean Square Error
            errorOut = ((1/2) * (np.power((outputOut - self.targetOutput), 2)))
            if epoch==0:
                prevErrorOut = errorOut.sum() + 1
            error.append(errorOut.sum())

            if epoch%50==0:
                if abs(errorOut.sum() - prevErrorOut.sum()) < 0.00001:
                    self.learningRate -= 0.0005
                prevErrorOut = errorOut.sum()

            
            #----- LIVE PLOT ---- DON'T USE IT!!!!
            # epochsPlot.append(epoch)
            # if epoch%100 == 0:  #Update live plot every 100 epochs
            #     lines.set_xdata(epochsPlot)
            #     lines.set_ydata(error)
            #     ax.relim()
            #     ax.autoscale_view()

            #     figure.canvas.draw()
            #     figure.canvas.flush_events()

            #Derivatives for phase 1
            derror_doutO = outputOut - self.targetOutput
            doutO_dinO = sigmoidDer(inputOut)
            dinO_dwO = outputHidden2
            derror_wO = np.dot(dinO_dwO.T, derror_doutO * doutO_dinO)

            #---------------------------
            #Phase 2
            #Derivatives for phase 2
            derror_dinO = derror_doutO * doutO_dinO
            dinO_doutH2 = self.weightOutput
            derror_doutH2 = np.dot(derror_dinO, dinO_doutH2.T)
            doutH2_dinH2 = sigmoidDer(inputHidden2)
            dinH2_dwH2 = outputHidden1
            derror_wH2 = np.dot(dinH2_dwH2.T, doutH2_dinH2 * derror_doutH2)

            #---------------------------
            #Phase 3
            #Derivatives for phase 3
            derror_dinH2 = derror_doutH2 * doutH2_dinH2
            dinH2_doutH1 = self.weightHidden2
            derror_doutH1 = np.dot(derror_dinH2, dinH2_doutH1.T)
            doutH1_dinH1 = sigmoidDer(inputHidden1)
            dinH1_dwH1 = self.trainingImages
            derror_wH1 = np.dot(dinH1_dwH1.T, doutH1_dinH1 * derror_doutH1)

            #Update weights
            self.weightHidden1 -= self.learningRate * derror_wH1
            self.weightHidden2 -= self.learningRate * derror_wH2
            self.weightOutput -= self.learningRate * derror_wO

        self.trained = True
        return [epochs, error]

    """
        Analize an image using the neural network
    """
    def analize(self, pImage):
        sumLayer1 = np.dot(pImage, self.weightHidden1)
        outputLayer1 = sigmoid(sumLayer1)

        sumLayer2 = np.dot(outputLayer1, self.weightHidden2)
        outputLayer2 = sigmoid(sumLayer2)

        sumOuputLayer = np.dot(outputLayer2, self.weightOutput)
        output = sigmoid(sumOuputLayer)

        return output
    