import cv2 as openCV
import numpy

def segmentationByColor(image, min, max):
    
    min = numpy.array(min)
    max = numpy.array(max)
    
    blur = openCV.medianBlur(
        image,
        7
    )
    
    hsv = openCV.cvtColor(blur, openCV.COLOR_BGR2HSV) # Converte para o espaco HSV
    
    mask = openCV.inRange(hsv, min, max)
    mask = openCV.bitwise_not(mask)
    
    return mask

def mergeImages(image, background, min, max):
    
    mask = segmentationByColor(image, min, max)
    
    mask_not = openCV.bitwise_not(mask)
    
    mask = numpy.array(mask >= 1).astype("uint8")
    mask_not = numpy.array(mask_not >= 1).astype("uint8")
    
    mask = openCV.merge((mask, mask, mask))
    mask_not = openCV.merge((mask_not, mask_not, mask_not))
    
    mask *= image
    mask_not *= background
    
    result = mask | mask_not
    
    return result