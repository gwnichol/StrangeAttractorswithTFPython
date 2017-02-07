from PIL import Image # Imports Python Image Library for PNG
import random # Imports the random library
import numpy as np
from math import log # Imports log
from colorsys import hsv_to_rgb # Imports hsv to rbg color scheme converter.

SIZE = 800 #Sets the width and hight of the image

img_index = 0 #Starts counter at 0

def plotmap(x):
    # scales the x or y up to an integer that fits in the image array

    catchSize = 1

    return int((x+catchSize)*(SIZE/(catchSize*2)))

run = True
MAXVAL = 1000 #Sets the maximum value for brightness

def iterate(x,y,a): # Simple quadratic map.
    xnew = a[0] + x*(a[1]+a[2]*x+a[3]*y) + y*(a[4]+a[5]*y)
    ynew = a[6] + x*(a[7]+a[8]*x+a[9]*y) + y*(a[10]+a[11]*y)
    return xnew, ynew
def name(a): # Pairs constant values with letters then appends them to name array
    alphabet = ["A","B","C","D","E",'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    name = ""
    for n in a:
        index = np.linspace(-1.2,1.2,num=25).tolist().index(n)
        name = name + alphabet[index]
    return name
def calcL(Lsum, Ye, Xe, N, a, x, y): # To extimate the lyapunov exponent. #Remade from BASIC code I found.
    xnew, ynew = iterate(Xe, Ye, a) # Iterates the different x and y values
    DLX = xnew - x # Finds difference between the x on the image and the x on the slightly different initial conditions.
    DLY = ynew - y # Same for y
    DL2 = DLX**2 + DLY**2  # First step to finding distance
    DF = 1000000000000 * DL2 # First step to finding rotation scalar.
    RS = 1 / (DF**(1/2)) # Calculates rotation scalar
    XE = x + RS*(xnew-x)
    YE = y + RS*(ynew-y)
    Lsum = Lsum + log(DF)
    L = .721347 * Lsum / N # Approximation for base 2 log
    return L, Lsum, YE, XE

def hist(im,nbr_bins=2**8):
    imhist, bins = np.histogram(im.flatten(),nbr_bins,density=True) # Uses numpy's histogram method to find the distrubution brightness arroc the image
    imhist[0] = 0 # Sets the brightness for black to be unchanged

    cdf = imhist.cumsum() # Cumulative sum that continues the sum across the array in order to equlize. Example:
    # [ 0, 3, 0 ]       [ 0, 3, 3 ]
    # [ 4, 0, 0 ] ----> [ 7, 7, 7 ]
    # [ 2, 3, 5 ]       [ 9, 12, 17]
    cdf = (2**8-1) * cdf / cdf[-1] # Scales the cumulative sum array so that the upermost value is at 255.
    im2 = np.interp(im.flatten(),bins[:-1],cdf) # Interpulate values for each pixel based on new equlazed histogram.
    return np.array(im2,np.uint8).reshape(im.shape) # Reshape the new equalized array to that of the original and return.

while run:

    x, y = .5 , .5 # Sets the initial x and y values. Any small changes in these and the resulting image is changed.

    imgarray = np.zeros([SIZE, SIZE, 3], float) # Creates the empty array to hold the color values of the image.
    imgcount = np.zeros([SIZE, SIZE], int) # Creates empty array to hold the brighness level for the pixel
    a = [] # Sets the constants array to zero.
    for i in range(12): # Sets the constants
        a.append(random.choice(np.linspace(-1.2,1.2,num=25))) # Randomly picks one of 25 numbers between -1.2 and 1.2
    Lsum = 0 # Sets the sum for lyapunov estimation to 0
    Ye = y # Sets the altered y value to the initial condition.
    Xe = x + .000001 # Sets the altered x value to slightly off the initial condition.
    length = 0 # Signifies that nothing has happened to the image array yet.
    while imgcount[plotmap(x), plotmap(y)] < MAXVAL: # Checks the the brightness level has not yet reached the set threshold.
        if length > 1: # Will not do the lyapunov calculation with nothing done yet or will result in divide by 0.
            L, Lsum, Ye, Xe = calcL(Lsum, Ye, Xe,length,a, x, y) # Lyapunov exponent estimation.
        color = hsv_to_rgb(x+1, .8, 1) # Sets color for next pixel based on parent x position.
        x, y = iterate(x,y,a) # Iterates the function once.

        if not(plotmap(x) and plotmap(y)): # Checks if the map scaling resulted in negative number.
            break # Restarts with new constants
        try:
            imgcount[plotmap(x), plotmap(y)] += 1 # Checks for index error
        except IndexError:
            break # Restarts with new constants.
        imgarray[plotmap(x), plotmap(y)] += np.array(color) # edits the color value for the image.
        if length > 200 and L < .005: # Will stop is lyapunov exponent is too small meaning there is not enough caos.
            break
        length = length + 1 # Steps up the lengh value.

    else:
        imgarray = np.array(imgarray / ((MAXVAL-.5*MAXVAL)/256.), np.uint8) # Scales all the color values to the 0-255 range and converts to 8bit integer.
        if L > .01 and sum(imgarray[imgarray==True].flatten()) > (SIZE **2) * .001: # Checks the lyapunov shows caos and that there is enought color on the image.
            imgarray = hist(imgarray) # Runs the histogram equlization.
            img = Image.fromarray(imgarray, "RGB") # Makes state of image class from the PIL.
            img.save("found_" + name(a) + "_" +str(L) + "_colorized" +".png", "PNG") # Saves the image as PNG with name including lyapunov estimation and unique name.
            img_index += 1 # tells that one more image has been found.
            if img_index == 1000: # Sets to stop creating after 1000 images have been found.
                run = False
            print("SAVED! Name: found_" + name(a) + "_" + str(L) + "_colorized" + ".png") # Prints to console that an image has been found.
