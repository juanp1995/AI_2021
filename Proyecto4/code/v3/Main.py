from UI import UI
from NeuralNetwork import NeuralNetwork
import numpy as np


image = np.array(np.ones((1, 100), dtype=int))

network = NeuralNetwork()

ret = UI(10, 10, image, network)
ret.show()