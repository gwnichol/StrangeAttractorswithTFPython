from PIL import Image
import numpy as np
from math import log

SIZE = int(input("Size:"))

img_index = 0

def plotmap(x):
    # scales the x or y up to an integer that fits in our image array

    catchSize = 1

    return int((x+catchSize)*(SIZE/(catchSize*2)))

run = True
MAXVAL = 600

def iterate(x,y,a):
    xnew = a[0] + x*(a[1]+a[2]*x+a[3]*y) + y*(a[4]+a[5]*y)
    ynew = a[6] + x*(a[7]+a[8]*x+a[9]*y) + y*(a[10]+a[11]*y)
    return xnew, ynew
def name(name):
    a = []
    alphabet = ["A","B","C","D","E",'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    values = np.linspace(-1.2,1.2,num=25)
    for n in name:
        index = alphabet.index(n)
        a.append(values[index])
    return a
def calcL(Lsum, Ye, Xe, N, a, x, y):
    xnew, ynew = iterate(Xe, Ye, a)
    DLX = xnew - x
    DLY = ynew - y
    DL2 = DLX**2 + DLY**2
    DF = 1000000000000 * DL2
    RS = 1 / (DF**(1/2))
    XE = x + RS*(xnew-x)
    YE = y + RS*(ynew-y)
    Lsum = Lsum + log(DF)
    L = .721347 * Lsum / N
    return L, Lsum, YE, XE

def histq(im,nbr_bins=2**16):
    imhist,bins = np.histogram(im.flatten(),nbr_bins,density=True)
    imhist[0] = 0

    cdf = imhist.cumsum()
    cdf ** .5
    cdf = (2**16-1) * cdf[-1]
    cdf = cdf / (2**16.)

    im2 = np.interp(im.flatten().asfarray(),bins[:-1],cdf)
    return np.array(im2, int).reshape(im.shape)

x, y = .5 , .5

imgarray = np.zeros([SIZE, SIZE], float)
nam= input("Name:")
a = name(nam)

values = []
Lsum = 0
Ye = y
Xe = x + .000001
length = 0
run = True
while run:

    if length > 1:
        L, Lsum, Ye, Xe = calcL(Lsum, Ye, Xe,length,a, x, y)

    x, y = iterate(x,y,a)

    if length > 200:
        if not(plotmap(x) and plotmap(y)):
            #print "break"
            print("Neggg")
            break
            # catch negative numbers... the "IndexError" won't
            # do this resulting in "wrap-around" images

        try:
            imgarray[plotmap(x), plotmap(y)] += 1.

        except IndexError:
            print("Index:", plotmap(x), plotmap(y))
            #print "break!"
            break
        if imgarray[plotmap(x), plotmap(y)] == MAXVAL:
                run = False
    length = length + 1

else:
        #print sum(imgarray[imgarray==True].flatten()), SIZE **2
    imgarray = np.array(imgarray / (MAXVAL/256.), np.uint8)
    if L > .01 and sum(imgarray[imgarray==True].flatten()) > (SIZE **2) * .001:
        img = Image.fromarray(imgarray, "L")

        img.save("custom_" + nam + "_" +str(L) + ".png", "PNG")
        print("SAVED!")
