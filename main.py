import cv2 as openCV
import numpy
from src.utils import readColorYaml, PATH_IMAGES
from src.segmentation.byColor import mergeImages

if __name__ == "__main__":
    
    path = str(PATH_IMAGES / "3.jpeg")
    save = str(PATH_IMAGES / "3_blue.jpeg")
    
    image = openCV.imread(path)
    
    if image is not None:
        
        height, width = image.shape[:2]
        
        color = readColorYaml("red")
        
        background = numpy.full((height, width, 3), (255, 12, 0)).astype("uint8")
        
        mask = mergeImages(image, background, color["min"], color["max"])
        
        openCV.imshow("Image", image) 
        openCV.imshow("Fundo", background)
        openCV.imshow("Mask", mask)
        
        openCV.imwrite(save, mask)
        
        key = openCV.waitKey(0) & 0xFF
        
        if key == ord("q"):
            openCV.destroyAllWindows()