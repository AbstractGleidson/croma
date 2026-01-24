from segmentation.exeptions import ImageNotFound, ColorNotSelected, ColorNotFound
from .segmentation import Segmentation
from .getColor import GetColor
from .utils import getPath, readColorYaml
import cv2 as openCV


def segObject(imagePath, color):
    
    path = getPath(imagePath)
    
    img = openCV.imread(
        path
    )
    
    if img is None:
        raise ImageNotFound(f"Não foi possível abrir a imagem. Verifique o caminho: {path}")  
    
    if color is None:
        col = GetColor.getColor(img)
        
        if col is None:
            raise ColorNotSelected("A cor não foi selecionada.")
        
    elif color.lower() in ["green", "red", "blue"]:
        col = readColorYaml(color.lower())
        
    else:
        raise ColorNotFound(f"A cor {color} não existe.")       
    
    segImage = Segmentation.segObject(img, col["min"], col["max"])
    
    openCV.imshow("Imagem", img)
    openCV.imshow("Objeto segmentado", segImage)
    
    key = openCV.waitKey(0) & 0xFF
    
    if key == ord('q'):
        openCV.destroyAllWindows()