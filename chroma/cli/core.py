import click
from chroma.segmentation.segmentation import Segmentation
from chroma.utils.utils import readColorYaml
from chroma.utils.getColor import GetColor
from .exeptions.ColorNotFound import ColorNotFound
from .exeptions.ColorNotSelected import ColorNotSelected
import numpy
import cv2 as openCV

def SegImage(image, background, color):
    
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

def SegWebCam(webcam, background, color, height, width):
    
    webcam = openCV.VideoCapture(webcam)
    
    if webcam is None:
        click.echo("Não foi possível abrir a webcam.")
        
    else:
        
        # Configura tamanho da janela
        webcam.set(openCV.CAP_PROP_FRAME_HEIGHT, height)
        webcam.set(openCV.CAP_PROP_FRAME_WIDTH, width)
        
        background = openCV.imread(background)
        
        if background is None:
            background = numpy.full((width, height, 3), (0, 0, 0)).astype("uint8")
        else:
            background = openCV.resize(
                background,
                (width, height),
                interpolation=openCV.INTER_CUBIC
            )
        
        if color is not None and color.lower() in ["green", "red", "blue"]:
            color = readColorYaml(color.lower())
        else:
            color = readColorYaml("green")   
            
        while(True):
            
            isAvaliable, frame = webcam.read()
            
            if isAvaliable:
                
                mask = Segmentation.chromaKey(
                    frame, 
                    background, 
                    color['min'], 
                    color['max']
                )
                
                openCV.imshow("Frame", frame)
                openCV.imshow("Chroma", mask)
                openCV.imshow("Plano de fundo", background)
                
                key = openCV.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
        
        webcam.release()
        openCV.destroyAllWindows()