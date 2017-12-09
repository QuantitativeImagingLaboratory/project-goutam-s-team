from tkinter import *
import tkinter as tk
from tkinter import ttk
import cv2
from tkinter import filedialog
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
import numpy as np


def compute_histogram(image):
    hist = [0] * 256
    row, col = image.shape

    for i in range(row):
        for j in range(col):
            hist[image[i, j]] += 1

    return hist


def find_optimal_threshold(hist):

        threshold = 0
        avg = len(hist) / 2
        overall = 0

        for i in range(int(avg)):

            if (hist[i] != 0):
                # overall pixel intensities are added up until 'avg' length
                overall = overall + hist[i]

        overall_2 = 0
        # same thing is done for the second half
        for i in range(int(avg), int(len(hist))):

            if (hist[i] != 0):
                overall_2 = overall_2 + hist[i]

        final_threshold_1 = 0
        for i in range(int(avg)):
            if (hist[i] != 0):
                probability_1 = hist[i] / overall
                prob_dist_1 = i * probability_1
                final_threshold_1 = prob_dist_1 + final_threshold_1

        final_threshold_2 = 0

        for i in range(int(avg), int(len(hist))):
            if (hist[i] != 0):
                probPix = hist[i] / overall_2
                prob_dist_2 = i * probPix
                final_threshold_2 = prob_dist_2 + final_threshold_2

        threshold = (final_threshold_1 + final_threshold_2) / 2

        return threshold


def binarize(image, threshold):

    bin_img = image.copy()
    row, column = bin_img.shape

    for i in range(row):
        for j in range(column):
            if bin_img[i, j] > threshold:
                bin_img[i, j] = 0
            else:
                bin_img[i, j] = 255

    return bin_img

def structuringElement(kernel):

    if kernel == 'Cross':
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
    elif kernel == 'Elipse':
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    elif kernel == 'Square':
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    return kernel

def Dilation(image,threshold,window):

    ImgRow, ImgColumn = image.shape
    count = 1
    r = np.zeros((ImgRow, ImgColumn), np.uint32)
    r1 = np.zeros((ImgRow, ImgColumn), np.uint8)
    flag1=flag2=flag3=0
    if(window==1):
        flag1=1
        flag2=1
    if (window == 2):
        flag1 = 1
        flag3 = 1
    if (window == 3):
        flag1 = 1
        flag2 = 1
        flag3 = 1

    for j in range(2, ImgColumn - 2):
        for i in range(2, ImgRow - 2):
            if(flag1==1):
                if image[i - 1, j] > threshold or image[i, j + 1] > threshold or image[i + 1, j] > threshold or image[
                    i, j - 1] > threshold:
                    r1[i, j] = threshold + 100
                else:
                    r1[i, j] = image[i, j]
            if(flag2==1):
                if image[i - 2, j] > threshold or image[i, j + 2] > threshold or image[i + 2, j] > threshold or image[
                    i, j - 2] > threshold:
                    r1[i, j] = threshold + 100
                    r1[i - 1, j] = threshold + 100
                    r1[i + 1, j] = threshold + 100
                    r1[i, j - 1] = threshold + 100
                    r1[i, j + 1] = threshold + 100
                else:
                    r1[i, j] = image[i, j]
            if(flag3==1):
                if image[i - 1, j - 1] > threshold or image[i + 1, j + 1] > threshold or image[
                            i + 1, j - 1] > threshold or image[i + 1, j - 1] > threshold:
                    r1[i, j] = threshold + 100
                else:
                    r1[i, j] = image[i, j]

    #for j in range(0, ImgColumn):
     #   for i in range(0, ImgRow):
      #     if r[i, j] != threshold+100 or r1[i, j] != image[i,j]  :
       #         r1[i, j] = image[i,j]

    return r1


def erosion(image,threshold,window):

    ImgRow, ImgColumn = image.shape
    count = 1
    r = np.zeros((ImgRow, ImgColumn), np.uint32)
    r1 = np.zeros((ImgRow, ImgColumn), np.uint8)
    flag1 = flag2 = flag3 = 0
    if (window == 1):
        flag1 = 1
        flag2 = 1
    if (window == 2):
        flag1 = 1
        flag3 = 1
    if (window == 3):
        flag1 = 1
        flag2 = 1
        flag3 = 1

    for j in range(2, ImgColumn - 2):
        for i in range(2, ImgRow - 2):
            if (flag1 == 1):
                if image[i - 1, j] < threshold or image[i, j + 1] < threshold or image[i + 1, j] < threshold or image[
                    i, j - 1] < threshold:
                    r1[i, j] = threshold - 100
                else:
                    r1[i, j] = image[i, j]

            if (flag2 == 1):
                if image[i - 2, j] < threshold or image[i, j + 2] < threshold or image[i + 2, j] < threshold or image[
                    i, j - 2] < threshold:
                    r1[i, j] = threshold - 100
                else:
                    r1[i, j] = image[i, j]

            if (flag3 == 1):
                if image[i - 1, j - 1] < threshold or image[i + 1, j + 1] < threshold or image[
                            i + 1, j - 1] < threshold or image[i + 1, j - 1] < threshold:
                    r1[i, j] = threshold - 100
                else:
                    r1[i, j] = image[i, j]

    #for j in range(0, ImgColumn):
     #   for i in range(0, ImgRow):
      #     if r[i, j] != threshold+100 or r1[i, j] != image[i,j]  :
       #         r1[i, j] = image[i,j]

    return r1
def median(image,kernel):
    ImgRow, ImgColumn = image.shape
    values = []
    output = np.zeros((ImgRow, ImgColumn), np.uint8)
    for x in range(ImgRow):
        for y in range(ImgColumn):
            value1 = max(x - kernel, 0)
            value2 = min(x + kernel, ImgRow)
            value3 = max(y - kernel, 0)
            value4 = min(y + kernel, ImgColumn)
    for i in range(value1, value2):
        for j in range(value3, value4):
            values.append(image[i, j])
    values = sorted(values)
    median1 = int(len(values) / 2)
    output[x, y] = values[median1]
    return output



def main():

    root=Tk()
    Label(text="Choose an image").pack()
    def ok():


        toplevel = Tk()
        toplevel.withdraw()
        filename = filedialog.askopenfilename()
        print(filename)
        k = filename.replace("/", "\\")
        print(k)

        path = k
        photo = ImageTk.PhotoImage(Image.open(path))
        global image
        image=cv2.imread(path)

        label = Label(image=photo)
        label.image = photo  # keep a reference!
        label.pack()
        Label(text="Original Image").pack()



    Button(text='Browse', command=ok).pack()

    Label(text="Select the structurig element").pack(pady=10)
    options = ['Cross', 'Square', 'Hybrid']
    combo = ttk.Combobox(values=options, state='readonly')
    combo.current()
    combo.pack(padx=35)
    def okk():
        global kernel
        kernel = format(combo.get())
        if kernel == 'Cross':
            kernel = 1
        elif kernel == 'Square':
            kernel = 2
        elif kernel == 'Hybrid':
            kernel = 3

    ttk.Button(text='Structure', command=okk).pack(side='right', padx=15, pady=10)
    ttk.Label(text="Select the morphological operation").pack(pady=20)
    optionns = ['Erode', 'Dilate', 'Median', 'Open', 'Close']
    combo1 = ttk.Combobox(values=optionns)
    combo1.current()
    combo1.pack(padx=15)

    def okkk():
        image = cv2.imread("3.jpg",0)
        print('Selection: {}'.format(combo1.get()))
        histogram = compute_histogram(image)
        threshold = find_optimal_threshold(histogram)
        o = format(combo1.get())
        if o == 'Erode':
            o = erosion(image, threshold, kernel)
        elif o == 'Dilate':
            o = Dilation(image, threshold, kernel)
        elif o == 'Median':
            o = median(image, kernel)
        elif o == 'Open':
            o = Dilation(erosion(image, threshold, kernel), threshold, kernel)
        elif o == 'Close':
            o = erosion(Dilation(image, threshold, kernel), threshold, kernel)
        cv2.imwrite('output.png', o)

        toplevel = Tk()
        toplevel.withdraw()
        Output = ImageTk.PhotoImage(Image.open('output.png'))
        label = tk.Label(image=Output)
        label.image = Output  # keep a reference!
        label.pack()
        tk.Label(text="Output Image").pack()

    ttk.Button(text='OK', command=okkk).pack(side='right', padx=25, pady=20)

    root.mainloop()

if __name__=="__main__":
    main()


