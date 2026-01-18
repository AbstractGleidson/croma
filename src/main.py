import cv2 as openCV
import numpy
from src.utils.utils import readColorYaml, PATH_IMAGES, hsvToOpenCV
from segmentation.segmentation import Segmentation

if __name__ == "__main__":
    
    
    path = str(PATH_IMAGES / "2.jpeg")
    image = openCV.imread(path)
    
    if image is not None:
        
        height, width = image.shape[:2]
        
        color = readColorYaml("green")
    
        background = numpy.full((height, width, 3), (255,255, 255)).astype("uint8")
        
        mask = Segmentation.chromaKey(image, background, color["min"], color["max"])
        
        openCV.imshow("Image", image) 
        openCV.imshow("Mask", mask)
        
        key = openCV.waitKey(0) & 0xFF
        
        if key == ord('q'):
            openCV.destroyAllWindows()