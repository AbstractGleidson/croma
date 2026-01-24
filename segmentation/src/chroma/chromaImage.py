from segmentation.exeptions import ColorNotFound, ColorNotSelected, ImageNotFound
from segmentation.src.getColor import GetColor
from segmentation.src.utils import readColorYaml, getPath
from segmentation.src.segmentation import Segmentation
import cv2 as openCV
import numpy 

def chromaImage(imagePath, background, color):
    
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
        raise ColorNotFound(f'A cor "{color}" não existe.')       
    
    height, width = img.shape[:2]
        
    # Configura plano de fundo
    if background is None:
        back = numpy.full((height, width, 3), (0, 0, 0)).astype("uint8")
    else:
        back = openCV.imread(background)
            
        if back is None:
            raise FileNotFoundError("O arquivo do plano de fundo não foi encontrado!")
            
        back = openCV.resize(
            back,
            (width, height),
            interpolation=openCV.INTER_CUBIC
        )
            
    mask = Segmentation.chromaKey(
        img, 
        back, 
        col['min'], col['max']
    )
        
    openCV.imshow('Imagem', img)
    openCV.imshow('Imagem chroma', mask)
    openCV.imshow('Plano de fundo', back) # type: ignore
        
    key = openCV.waitKey(0) & 0xFF
        
    if key == ord('q'):
        openCV.destroyAllWindows()