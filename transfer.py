import matplotlib.pyplot as plt
import numpy as np
import math
import os

from PIL import Image, ImageDraw  # Подключим необходимые библиотеки.

def sum3Tuple(a, b, c):
    y = [a[temp] + b[temp] + c[temp] for temp in range(0, min(len(a), len(b)))]
    return tuple(y)

def sumTuple(a, b):
    y = [a[temp] + b[temp] for temp in range(0, min(len(a), len(b)))]
    return tuple(y)

def sub3Tuple(a, b, c):
    y = [a[temp] - b[temp] - c[temp] for temp in range(0, min(len(a), len(b)))]
    return tuple(y)

def subTuple(a, b):
    y = [a[temp] - b[temp] for temp in range(0, min(len(a), len(b)))]
    return tuple(y)

def multTuple(a, b):
    y = [a[temp] * b[temp] for temp in range(0, min(len(a), len(b)))]
    return tuple(y)

def sqrtTuple(a):
    y = [math.floor(math.sqrt(a[temp])) for temp in range(0, len(a))]
    return tuple(y)

if __name__ == "__main__":
    dirs = ["./filt", "./less", "./more", "./origin"]
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)

    F_MAX = 175
    G_MAX = 125

    G_MIN1 = 0
    F_MAX1 = 255
    F_MIN1 = 255 - G_MAX

    G_MAX2 = 255
    F_MIN2 = 0
    G_MIN2 = 255 - F_MAX

    HORIZONTAL_CORE = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
    VERTICAL_CORE = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]

    image = Image.open("image.jpg")  # Открываем изображение.
    image1 = Image.open("image.jpg")  # Открываем изображение.
    image2 = Image.open("image.jpg")  # Открываем изображение.
    image3 = Image.open("image.jpg")  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    draw1 = ImageDraw.Draw(image1)  # Создаем инструмент для рисования.
    draw2 = ImageDraw.Draw(image2)  # Создаем инструмент для рисования.
    draw3 = ImageDraw.Draw(image3)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.

    red = []
    green = []
    blue = []

    redLess = []
    greenLess = []
    blueLess = []

    redMore = []
    greenMore = []
    blueMore = []

    redFilt = []
    greenFilt = []
    blueFilt = []

    for i in range(height):
        for j in range(width):
            a = pix[j, i][0]
            b = pix[j, i][1]
            c = pix[j, i][2]
            red.append(a)
            green.append(b)
            blue.append(c)
            original = [a, b, c]
            less = []
            more = []
            if (0 < i < height - 2) and (0 < j < width - 2):
                GX = subTuple(sum3Tuple(pix[j - 1, i + 1], pix[j, i + 1], pix[j + 1, i + 1]), sum3Tuple(pix[j - 1, i - 1], pix[j, i - 1], pix[j + 1, i - 1]))
                GY = subTuple(sum3Tuple(pix[j + 1, i - 1], pix[j + 1, i], pix[j + 1, i + 1]), sum3Tuple(pix[j - 1, i - 1], pix[j - 1, i], pix[j - 1, i + 1]))
                pos = sqrtTuple(sumTuple(multTuple(GX, GX),  multTuple(GY, GY)))

                redFilt.append(pos[0])
                greenFilt.append(pos[1])
                blueFilt.append(pos[2])

                draw3.point((j, i), pos)
            for pixel in original:
                if pixel <= F_MIN1:
                    less.append(G_MIN1)
                else:
                    less.append(pixel - G_MAX)

                if pixel <= F_MAX:
                    more.append(pixel + G_MIN2)
                else:
                    more.append(G_MAX2)
            S = (a + b + c) // 3
            redLess.append(less[0])
            greenLess.append(less[1])
            blueLess.append(less[2])

            redMore.append(more[0])
            greenMore.append(more[1])
            blueMore.append(more[2])

            draw1.point((j, i), (less[0], less[1], less[2]))
            draw2.point((j, i), (more[0], more[1], more[2]))
            draw.point((j, i), (S, S, S))

    image.save("ans.jpg", "JPEG")
    image1.save("less.jpg", "JPEG")
    image2.save("more.jpg", "JPEG")
    image3.save("filt.jpg", "JPEG")
    del draw
    del draw1
    del draw2
    del draw3

    plt.hist(red, bins=range(0, 255))
    plt.savefig('origin/histRed.png')
    plt.show()
    plt.hist(green, bins=range(0, 255))
    plt.savefig('origin/histGreen.png')
    plt.show()
    plt.hist(blue, bins=range(0, 255))
    plt.savefig('origin/histBlue.png')
    plt.show()

    plt.hist(redLess, bins=range(0, 255))
    plt.savefig('less/histRed.png')
    plt.show()
    plt.hist(greenLess, bins=range(0, 255))
    plt.savefig('less/histGreen.png')
    plt.show()
    plt.hist(blueLess, bins=range(0, 255))
    plt.savefig('less/histBlue.png')
    plt.show()

    plt.hist(redMore, bins=range(0, 255))
    plt.savefig('more/histRed.png')
    plt.show()
    plt.hist(greenMore, bins=range(0, 255))
    plt.savefig('more/histGreen.png')
    plt.show()
    plt.hist(blueMore, bins=range(0, 255))
    plt.savefig('more/histBlue.png')
    plt.show()

    plt.hist(redFilt, bins=range(0, 255))
    plt.savefig('filt/histRed.png')
    plt.show()
    plt.hist(greenFilt, bins=range(0, 255))
    plt.savefig('filt/histGreen.png')
    plt.show()
    plt.hist(blueFilt, bins=range(0, 255))
    plt.savefig('filt/histBlue.png')
    plt.show()
