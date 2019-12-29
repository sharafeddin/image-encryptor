from PIL import Image
import numpy as np
import math
import os


def decimalToBinaryInList(x):
    l = list(bin(x))
    l = l[2:]
    result = list()
    if len(l)!=8:
        d = 8-len(l)
        for i in range(d):
            result.append(0)
        for i in range(len(l)):
            result.append(l[i])
        return result
    else:
        return l


def negatifFilter(r,g,b):
    newR = list()
    for i in range(len(r)):
        if r[i]==str(1):
            newR.append(str(0))
        else:
            newR.append(str(1))
    r = int("0b" + "".join(newR),2)
    newG = list()
    for i in range(len(g)):
        if g[i]==str(1):
            newG.append(str(0))
        else:
            newG.append(str(1))
    g = int("0b" + "".join(newG),2)
    newB = list()
    for i in range(len(b)):
        if b[i]==str(1):
            newB.append(str(0))
        else:
            newB.append(str(1))
    b = int("0b" + "".join(newB),2)
    return (r,g,b)


def encryptImage(imagePath):
    """ This function encrypt the image whose path is given in the parameter, 
    and save the enrypted image in the same directory as the original image """

    # Opening image
    image = Image.open(imagePath)    

    frontImage = Image.open("front_image.png")
    frontImage = frontImage.convert('RGB')
        
    # Converting image to a matrix
    img = image.convert('RGB')
    width = img.size[0]
    height = img.size[1]

    # Applying the negatif filter on the image
    for x in range(width):
        for y in range(height):
            r = decimalToBinaryInList(img.getpixel((x,y))[0])
            g = decimalToBinaryInList(img.getpixel((x,y))[1])
            b = decimalToBinaryInList(img.getpixel((x,y))[2])
            img.putpixel((x,y),negatifFilter(r,g,b))

    # Rotating the image by 180°
    img = img.rotate(180)


    # Mixing the pixels of the image

    method1, method2 = True, False
    a = 0
    i = 0
    while a+50<=height:
        while method1:
            i = a
            for y in range(i, i+int(height/((height/4)/10))+10):
                leftPixels = []
                rightPixels = []
                for x in range(math.floor(width/2+width/4)):
                    leftPixels.append(img.getpixel((x,y)))
                for x in range(math.floor(width/2+width/4), width):
                    rightPixels.append(img.getpixel((x,y)))
                for x in range(len(rightPixels)):
                    img.putpixel((x,y),(rightPixels[x]))
                for x in range(len(rightPixels), width):
                    img.putpixel((x,y),leftPixels[x-len(rightPixels)])
                a = y
            a = a+1
            method1 = False
            method2 = True
        while method2:
            i = a
            if a+50>height:
                method2 = False
            else:
                for y in range(i, i+int(height/((height/4)/10))+10):
                    leftPixels = []
                    rightPixels = []
                    for x in range(math.floor(width/4)):
                        leftPixels.append(img.getpixel((x,y)))
                    for x in range(math.floor(width/4), width):
                        rightPixels.append(img.getpixel((x,y)))
                    for x in range(len(rightPixels)):
                        img.putpixel((x,y),(rightPixels[x]))
                    for x in range(len(rightPixels), width):
                        img.putpixel((x,y),leftPixels[x-len(rightPixels)])
                    a = y
                a = a+1
                method2 = False
                method1 = True


    # Hiding the image behind another

    for x in range(width):
        for y in range(height):
            newR = []
            newG = []
            newB = []
            r = decimalToBinaryInList(frontImage.getpixel((x,y))[0])
            g = decimalToBinaryInList(frontImage.getpixel((x,y))[1])
            b = decimalToBinaryInList(frontImage.getpixel((x,y))[2])
            for i in range(4):
                newR.append(str(r[i]))
                newG.append(str(g[i]))
                newB.append(str(b[i]))
            r = decimalToBinaryInList(img.getpixel((x,y))[0])
            g = decimalToBinaryInList(img.getpixel((x,y))[1])
            b = decimalToBinaryInList(img.getpixel((x,y))[2])
            for i in range(4):
                newR.append(str(r[i]))
                newG.append(str(g[i]))
                newB.append(str(b[i]))
            r = int("0b" + "".join(newR),2)
            g = int("0b" + "".join(newG),2)
            b = int("0b" + "".join(newB),2)
            img.putpixel((x,y),(r,g,b))


    # Hiding the extention of the image on the left most pixel on top of the image
    # PNG = 0, JPG or JPEG = 1

    r = decimalToBinaryInList(img.getpixel((0,0))[0])
    g = decimalToBinaryInList(img.getpixel((0,0))[1])
    b = decimalToBinaryInList(img.getpixel((0,0))[2])

    if image.format=="PNG":
        r[3]=str(0)
        g[3]=str(0)
        b[3]=str(0)
    else:
        r[3]=str(1)
        g[3]=str(1)
        b[3]=str(1)
    r = int("0b" + "".join(r),2)
    g = int("0b" + "".join(g),2)
    b = int("0b" + "".join(b),2)
    img.putpixel((0,0),(r,g,b))

    img = np.array(img)
    A = img[:math.floor(height/3), :width]
    B = img[math.floor(height/3):math.floor(height/3)*2, :width]
    C = img[math.floor(height/3)*2:height, :width]
    img = np.concatenate((np.concatenate((B,A),0),C),0)

    # Converting the matrix to an image
    encryptedImage = Image.fromarray(img)

    # Saving the encrypted image
    encryptedImage.save(os.path.dirname(imagePath)+"\\Encrypted_Image.png")

    # Displaying the encrypted image
    encryptedImage.show()


def decryptImage(imagePath):
    """ This function decrypt the image whose path is given in the parameter, 
    and save the original image in the same directory as the encrypted image """

    def plus(x):
        if x/int(x)==1:
            return int(x)
        return math.floor(x)+1

    # Opening image
    img = Image.open(imagePath)

    img = np.array(img)
    width = img.shape[1]
    height = img.shape[0]

    A = img[:math.floor(height/3), :width]
    B = img[math.floor(height/3):math.floor(height/3)*2, :width]
    C = img[math.floor(height/3)*2:height, :width]
    img = np.concatenate((np.concatenate((B,A),0),C),0)

    img = Image.fromarray(img)
    img = img.convert('RGB')

    # Extracting the extention of the original image

    r = decimalToBinaryInList(img.getpixel((0,0))[0])

    if r[3]==str(0):
        imageFormat = "png"
    else:
        imageFormat = "jpg"


    for x in range(width):
        for y in range(height):
            newR = []
            newG = []
            newB = []
            r = decimalToBinaryInList(img.getpixel((x,y))[0])
            g = decimalToBinaryInList(img.getpixel((x,y))[1])
            b = decimalToBinaryInList(img.getpixel((x,y))[2])
            for i in range(4,8):
                newR.append(str(r[i]))
                newG.append(str(g[i]))
                newB.append(str(b[i]))
            for i in range(4):
                newR.append(str(0))
                newG.append(str(0))
                newB.append(str(0))
            r = int("0b" + "".join(newR),2)
            g = int("0b" + "".join(newG),2)
            b = int("0b" + "".join(newB),2)
            img.putpixel((x,y),(r,g,b))


    # Putting every pixel of the image in its correct place

    method1, method2 = True, False
    a = 0
    i = 0
    while a+50<=height:
        while method1:
            i = a
            for y in range(i, i+int(height/((height/4)/10))+10):
                leftPixels = []
                rightPixels = []
                for x in range(plus(width/4)):
                    leftPixels.append(img.getpixel((x,y)))
                for x in range(plus(width/4), width):
                    rightPixels.append(img.getpixel((x,y)))
                for x in range(len(rightPixels)):
                    img.putpixel((x,y),(rightPixels[x]))
                for x in range(len(rightPixels), width):
                    img.putpixel((x,y),leftPixels[x-len(rightPixels)])
                a = y
            a = a+1
            method1 = False
            method2 = True
        while method2:
            i = a
            if a+50>height:
                method2 = False
            else:
                for y in range(i, i+int(height/((height/4)/10))+10):
                    leftPixels = []
                    rightPixels = []
                    for x in range(plus(width/2+width/4)):
                        leftPixels.append(img.getpixel((x,y)))
                    for x in range(plus(width/2+width/4), width):
                        rightPixels.append(img.getpixel((x,y)))
                    for x in range(len(rightPixels)):
                        img.putpixel((x,y),(rightPixels[x]))
                    for x in range(len(rightPixels), width):
                        img.putpixel((x,y),leftPixels[x-len(rightPixels)])
                    a = y
                a = a+1
                method2 = False
                method1 = True

    # Rotating the image by 180°
    img = img.rotate(180)

    # Removing the negatif filter from the image
    for x in range(width):
        for y in range(height):
            r = decimalToBinaryInList(img.getpixel((x,y))[0])
            g = decimalToBinaryInList(img.getpixel((x,y))[1])
            b = decimalToBinaryInList(img.getpixel((x,y))[2])
            img.putpixel((x,y),negatifFilter(r,g,b))

    img = np.array(img)

    # Converting the matrix to an image
    originalImage = Image.fromarray(img)

    # Saving the original image
    originalImage.save(os.path.dirname(imagePath)+"\\Original_Image."+imageFormat)

    # Displaying the original image
    originalImage.show()
