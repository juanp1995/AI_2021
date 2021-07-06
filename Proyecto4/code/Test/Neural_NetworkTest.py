import numpy as np

trainingImages = [np.random.randint(0, 2, 100) for _ in range(98)]
trainingImages.append(np.zeros(100, dtype=int))
trainingImages.append(np.ones(100, dtype=int))
trainingImages = np.array(trainingImages)



targetOutput = []
for img in trainingImages:
    countArray = np.bincount(img, minlength=2) 
    print(countArray)
    whitePixels = countArray[1]
    targetOutput.append(whitePixels/100)

targetOutput = np.array(targetOutput).reshape(100,1)


#Define weights
#6500 for hidden layer -> 100 inputs * 65 nodes in hidden layer
#65 for ouput layer -> 65 nodes in hidden layer * 1 node for output
weightHidden = np.array([np.random.uniform(-1.0, 1.0, 65) for _ in range(100)])
weightOutput = np.array([np.random.uniform(-1.0, 1.0, 1) for _ in range(65)])

#Learning rate
learningRate = 0.05

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sigmoidDer(x):
    return sigmoid(x) * (1.0 - sigmoid(x))


for epoch in range(10000):
    #Input for hidden layer
    inputHidden = np.dot(trainingImages, weightHidden)

    #Output from hidden layer
    outputHidden = sigmoid(inputHidden)

    #Input for output layer
    inputOut = np.dot(outputHidden, weightOutput)

    #Output from output layer
    outputOut = sigmoid(inputOut)

    #---------------------------
    #Phase 1

    #Calculate Mean Square Error
    errorOut = ((1/2) * (np.power((outputOut - targetOutput), 2)))
    # print(errorOut.sum())

    #Derivatives for phase 1
    derror_doutO = outputOut - targetOutput
    doutO_dinO = sigmoidDer(inputOut)
    dinO_dwO = outputHidden
    derror_wO = np.dot(dinO_dwO.T, derror_doutO * doutO_dinO)

    #---------------------------
    #Phase 2

    #Derivatives for phase 2
    derror_dinO = derror_doutO * doutO_dinO
    dinO_doutH = weightOutput
    derror_doutH = np.dot(derror_dinO, dinO_doutH.T)
    doutH_dinH = sigmoidDer(inputHidden)
    dinH_dwH = trainingImages
    derror_wH = np.dot(dinH_dwH.T, doutH_dinH * derror_doutH)

    #Update weights
    weightHidden -= learningRate * derror_wH
    weightOutput -= learningRate * derror_wO

    if epoch%100==0:
        print("Epoch: ", epoch, " Error: ", errorOut.sum())

#Final hidden layer weight values
# print(weightHidden)

# print("\n")
# print(weightOutput)


#Testing

#---- Test1
# testImage = np.zeros((1,50), dtype=int)
# testImage = np.array(np.concatenate((testImage, np.ones((1,50), dtype=int)), axis=1)[0])

#----- Test2
# testImage = []
# for _ in range(25):
#     testImage.append(0)

# for _ in range(75):
#     testImage.append(1)

# testImage = np.array(testImage)


#---- Test3
# testImage = np.array(np.ones((1,100), dtype=int))

result1 = np.dot(testImage, weightHidden)
result2 = sigmoid(result1)

result3 = np.dot(result2, weightOutput)
result4 = sigmoid(result3)
print(result4)



