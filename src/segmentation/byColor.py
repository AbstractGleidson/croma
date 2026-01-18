import cv2 as openCV
import numpy

def segmentationByColor(image, min, max):
    
    min = numpy.array(min)
    max = numpy.array(max)
    
    hsv = openCV.cvtColor(image, openCV.COLOR_BGR2HSV) # Converte para o espaco HSV
    
    mask = openCV.inRange(hsv, min, max)
    mask = openCV.bitwise_not(mask)
    
    return mask

def mergeImages(image, background, minc, maxc):
    
    mask1 = segmentationByColor(image, minc, maxc)
    mask2 = segmentationByColor(image, min=[0,100,100], max=[0,255,255])
    
    mask = mask1 & mask2 # type: ignore
    
    mask_not = openCV.bitwise_not(mask)
    
    mask = numpy.array(mask >= 1).astype("uint8")
    mask_not = numpy.array(mask_not >= 1).astype("uint8")
    
    mask = openCV.merge((mask, mask, mask))
    mask_not = openCV.merge((mask_not, mask_not, mask_not))
    
    mask *= image
    mask_not *= background
    
    result = mask | mask_not
    
    return result