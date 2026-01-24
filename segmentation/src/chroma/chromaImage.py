from segmentation.exeptions.colorNotFound import ColorNotFound
from segmentation.exeptions.colorNotSelected import ColorNotSelected
from segmentation.src.getColor import GetColor
from segmentation.src.utils import readColorYaml
from segmentation.src.segmentation import Segmentation
import cv2 as openCV
import numpy 

def chromaImage(image, background, color):
    
    # Leitura da cor 
    if color is None:
        color = GetColor.getColor(image)
    
        if color is None:
            raise ColorNotSelected("Você não selecinou uma cor.")
        
        col = color.copy()
        
    elif color.lower() in ["green", "blue", "red"]:
        col = readColorYaml("green")
    
    else:
        raise ColorNotFound("Cor passada como parâmetro não foi encontrada.")
    
    img = openCV.imread(image)
    
    if img is None:
        raise FileNotFoundError("O arquivo da imagem para aplicar o filtro não foi encontrado!")
    
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