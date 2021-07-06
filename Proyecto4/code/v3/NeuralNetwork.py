from PIL import Image
import numpy as np
import pylab as plt

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sigmoidDer(x):
    return sigmoid(x) * (1.0 - sigmoid(x))

# def relu(x):
#     return np.maximum(x, 0)

# def reluDer(x):
#     return np.where(x<=0, 0.0, 1 if np.any(x)!=0 else 0.0)

def loadImage(pFilename):
        image = Image.open(pFilename)
        pixels = image.load()
        imageArray = list()

        if image.size == (10,10):
            for i in range(10):
                for j in range(10):
                    value = 0 if pixels[i,j]==0 else 1
                    imageArray.append(value)
                    # imageArray[0][(i * 10) + j] = value

        return imageArray

def readImages(pPath, pNimages):
    images = list()
    for i in range(pNimages):
        path = pPath + "/" + str(i) + ".png"
        images.append(loadImage(path))

    return images

class NeuralNetwork:
    def __init__(self):
        self.trained = False
        self.stopTraining = False
        # self.learningRate = 0.02
        # self.epsilon = 0.001
        self.inputs = 100           #Each pixel of the 10x10 image
        self.hiddenLayer1 = 65      #Nodes in hidden layer 1
        self.hiddenLayer2 = 40      #Nodes in hidden layer 2
        self.outputLayer = 1        #Nodes in ouput layer
        

        #Weights of connections between layers
        # self.weightHidden1 = np.random.randn(self.inputs, self.hiddenLayer1)
        self.weightHidden1 = np.array(
            [np.random.uniform(-0.5,0.5, self.hiddenLayer1) for _ in range(self.inputs)])
        # self.weightHidden2 = np.random.randn(self.hiddenLayer1, self.hiddenLayer2)
        self.weightHidden2 = np.array(
            [np.random.uniform(-0.5,0.5, self.hiddenLayer2) for _ in range(self.hiddenLayer1)])
        # self.weightOutput = np.random.randn(self.hiddenLayer2, self.outputLayer)
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
        # n = 23
        n = 6
        #Create random "images" for training
        self.trainingImages = [np.random.randint(0, 2, 100) for _ in range(self.trainingSets-n)]
        self.cases() #Specific cases of images (all black, all white, etc)

        # #Add image patterns
        # trainingSamples = readImages(
        #     "/home/juanp1995/Documentos/I-2021/Inteligencia_Artificial/Proyecto4/training", n)

        # for i in range(len(trainingSamples)):
        #     self.trainingImages.append(trainingSamples[i])

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

    def trainNetwork(self, pTrainingSets, pLR, pEpsilon, pUpdateFunc):
        self.trainingSets = pTrainingSets
        self.learningRate = pLR
        self.epsilon = pEpsilon
        print(self.learningRate)
        self.createTrainingData()

        epoch = 0
        error = []
        prevError = 0

        while not self.stopTraining:
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
            error.append(errorOut.sum())
            epoch += 1

            if epoch%100 == 0:
                pUpdateFunc(error[-1])

            # if epoch%200 == 0:
            #     if abs(prevError - error[-1]) < 0.0001:
            #         self.learningRate /= 1.5
            #     prevError = error[-1]
            
            #Terminate training
            if error[-1] <= self.epsilon:
                break

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
        self.stopTraining = False

        epochsList = list(range(epoch))
        return [epochsList, error]

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
    