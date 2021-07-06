from PIL import Image
import numpy as np


def readImages(pPath, pNimages):
    images = []
    for i in range(pNimages):
        path = pPath + "/" + str(i) + ".png"
        images.append(loadImage(path))

    return images


def loadImage(pFilename):
        image = Image.open(pFilename)
        pixels = image.load()
        imageArray = np.zeros((1, 100), dtype=int)

        if image.size == (10,10):
            for j in range(10):
                for i in range(10):
                    value = 0 if pixels[i,j]==0 else 1
                    imageArray[0][(i * 10) + j] = value

        return imageArray