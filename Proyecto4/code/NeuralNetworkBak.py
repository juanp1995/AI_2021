import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sigmoidDer(x):
    return sigmoid(x) * (1.0 - sigmoid(x))

class NeuralNetwork:
    def __init__(self):
        self.trained = False
        self.learningRate = 0.05

    def cases(self):
        self.trainingImages.append(np.zeros(100, dtype=int))    #Black image
        self.trainingImages.append(np.ones(100, dtype=int))     #White image

        #50-50 black and white
        self.trainingImages.append(np.concatenate((np.zeros(50, dtype=int), np.ones(50, dtype=int))))
        self.trainingImages.append(np.concatenate((np.ones(50, dtype=int), np.zeros(50, dtype=int))))

    def createTrainingData(self):
        # stepSize = 0.02
        # steps = int(self.trainingSets / (1/stepSize))
        # rest = self.trainingSets - (steps*int((1/stepSize)))

        # self.trainingImages = []
        # prob = stepSize
        # for i in range(int((1/stepSize))):
        #     for j in range(steps):
        #         self.trainingImages.append(list(np.random.choice([0,1], 100, p=[(1-stepSize), stepSize])))
        #     prob += stepSize

        # if rest != 0:
        #     for i in range(rest):
        #         self.trainingImages.append(np.random.randint(0, 2, 100))

        self.trainingImages = [np.random.randint(0, 2, 100) for _ in range(self.trainingSets-4)]
        self.cases()
        self.trainingImages = np.array(self.trainingImages)

        self.targetOutput = []
        for img in self.trainingImages:
            countArray = np.bincount(img, minlength=2) 
            whitePixels = countArray[1]
            target = 0
            if (whitePixels/100) <= 0.5: 
                target = 0.0
            else:
                target = 1.0
            # self.targetOutput.append(whitePixels/100)
            self.targetOutput.append(target)

        self.targetOutput = np.array(self.targetOutput).reshape(self.trainingSets,1)

    def trainNetwork(self, pTrainingSets, pEpochs):
        self.trainingSets = pTrainingSets
        self.epochs = pEpochs
        self.createTrainingData()

        #Define weights
        #6500 for hidden layer -> 100 inputs * 65 nodes in hidden layer
        #65 for ouput layer -> 65 nodes in hidden layer * 1 node for output
        self.weightHidden = np.array([np.random.uniform(-1.0, 1.0, 65) for _ in range(100)])
        self.weightOutput = np.array([np.random.uniform(-1.0, 1.0, 1) for _ in range(65)])

        epochs = list(range(self.epochs))
        error = []
        for epoch in range(self.epochs):
            #Input for hidden layer
            inputHidden = np.dot(self.trainingImages, self.weightHidden)

            #Output from hidden layer
            outputHidden = sigmoid(inputHidden)

            #Input for output layer
            inputOut = np.dot(outputHidden, self.weightOutput)

            #Output from output layer
            outputOut = sigmoid(inputOut)

            #---------------------------
            #Phase 1

            #Calculate Mean Square Error
            # errorOut = ((1/2) * (np.power((outputOut - self.targetOutput), 2)))
            errorOut = ((1/2) * (np.power((outputOut - self.targetOutput), 2)))
            error.append(errorOut.sum())
            # print(errorOut.sum())

            #Derivatives for phase 1
            derror_doutO = outputOut - self.targetOutput
            doutO_dinO = sigmoidDer(inputOut)
            dinO_dwO = outputHidden
            derror_wO = np.dot(dinO_dwO.T, derror_doutO * doutO_dinO)

            #---------------------------
            #Phase 2

            #Derivatives for phase 2
            derror_dinO = derror_doutO * doutO_dinO
            dinO_doutH = self.weightOutput
            derror_doutH = np.dot(derror_dinO, dinO_doutH.T)
            doutH_dinH = sigmoidDer(inputHidden)
            dinH_dwH = self.trainingImages
            derror_wH = np.dot(dinH_dwH.T, doutH_dinH * derror_doutH)

            #Update weights
            self.weightHidden -= self.learningRate * derror_wH
            self.weightOutput -= self.learningRate * derror_wO

        self.trained = True
        return [epochs, error]


    def evaluate(self, pImage):
        result1 = np.dot(pImage, self.weightHidden)
        result2 = sigmoid(result1)

        result3 = np.dot(result2, self.weightOutput)
        result4 = sigmoid(result3)

        return result4
    