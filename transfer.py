import math
import os

import matplotlib.pyplot as plt
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


def maxTuple(a, b):
    y = [max(abs(a[temp]), abs(b[temp])) for temp in range(0, len(a))]
    return tuple(y)


def validateTuple(a):
    y = []
    for i in range(0, 3):
        if a[i] < 0:
            y.append(0)
        elif a[i] > 255:
            y.append(255)
        else:
            y.append(a[i])
    return tuple(y)


def toGrayScale(__input_name: str, __output_name: str):
    image = Image.open(__input_name)
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.

    for i in range(height):
        for j in range(width):
            a = pix[j, i][0]
            b = pix[j, i][1]
            c = pix[j, i][2]
            S = int(0.3 * a + 0.59 * b + 0.11 * c)
            draw.point((j, i), (S, S, S))

    image.save(__output_name, "JPEG")
    del draw
    del image


def preparationLess(__input_name: str, __output_name: str, F_MIN1: int, G_MIN1: int, G_MAX: int):
    image = Image.open(__input_name)
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.

    for i in range(height):
        for j in range(width):
            less = []
            a = pix[j, i][0]
            b = pix[j, i][1]
            c = pix[j, i][2]
            original = [a, b, c]
            for pixel in original:
                if pixel <= F_MIN1:
                    less.append(G_MIN1)
                else:
                    less.append(pixel - G_MAX)
            draw.point((j, i), (less[0], less[1], less[2]))

    image.save(__output_name, "JPEG")
    del draw
    del image


def preparationMore(__input_name: str, __output_name: str, F_MAX: int, G_MIN2: int, G_MAX2: int):
    image = Image.open(__input_name)
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.

    for i in range(height):
        for j in range(width):
            more = []
            a = pix[j, i][0]
            b = pix[j, i][1]
            c = pix[j, i][2]
            original = [a, b, c]
            for pixel in original:
                if pixel <= F_MAX:
                    more.append(pixel + G_MIN2)
                else:
                    more.append(G_MAX2)
            draw.point((j, i), (more[0], more[1], more[2]))

    image.save(__output_name, "JPEG")
    del draw
    del image


def previsFilter(__input_name: str, __output_name: str):
    image = Image.open(__input_name)  # Открываем изображение.
    imageRes = Image.open(__input_name)  # Открываем изображение.
    drawRes = ImageDraw.Draw(imageRes)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.

    for i in range(height):
        for j in range(width):
            if (0 < i < height - 2) and (0 < j < width - 2):
                GX = subTuple(sum3Tuple(pix[j - 1, i + 1], pix[j, i + 1], pix[j + 1, i + 1]),
                              sum3Tuple(pix[j - 1, i - 1], pix[j, i - 1], pix[j + 1, i - 1]))
                GY = subTuple(sum3Tuple(pix[j + 1, i - 1], pix[j + 1, i], pix[j + 1, i + 1]),
                              sum3Tuple(pix[j - 1, i - 1], pix[j - 1, i], pix[j - 1, i + 1]))
                pos = maxTuple(GX, GY)
                pos = validateTuple(pos)
                drawRes.point((j, i), pos)
    imageRes.save(__output_name, "JPEG")
    del image
    del imageRes
    del drawRes


def histogram(__input_name: str, __output_dir: str):
    if not os.path.exists(__output_dir):
        os.makedirs(__output_dir)

    image = Image.open(__input_name)
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.

    red = []
    green = []
    blue = []

    for i in range(height):
        for j in range(width):
            a = pix[j, i][0]
            b = pix[j, i][1]
            c = pix[j, i][2]
            red.append(a)
            green.append(b)
            blue.append(c)

    plt.hist(red, bins=range(0, 255))
    plt.savefig(__output_dir + "/histRed.png")
    plt.show()
    plt.hist(green, bins=range(0, 255))
    plt.savefig(__output_dir + "/histGreen.png")
    plt.show()
    plt.hist(blue, bins=range(0, 255))
    plt.savefig(__output_dir + "/histBlue.png")
    plt.show()
    del image


if __name__ == "__main__":
    F_MAX = 175
    G_MAX = 125

    G_MIN1 = 0
    F_MAX1 = 255
    F_MIN1 = 255 - G_MAX

    G_MAX2 = 255
    F_MIN2 = 0
    G_MIN2 = 255 - F_MAX

    # print("origin hist ...")
    # histogram("./image1.jpg", "origin")
    # print("to gray ...")
    # toGrayScale("./image1.jpg", "ans.jpg")
    # print("preparation less ...")
    # preparationLess("./image1.jpg", "less.jpg", F_MIN1, G_MIN1, G_MAX)
    # print("preparation more ...")
    # preparationMore("./image1.jpg", "more.jpg", F_MAX, G_MIN2, G_MAX2)
    print("filter ...")
    previsFilter("./image1.jpg", "filt.jpg")

    # print("hist less ...")
    # histogram("./less.jpg", "less")
    # print("hist more ...")
    # histogram("./more.jpg", "more")
    # print("hist filt ...")
    # histogram("./filt.jpg", "filt")
