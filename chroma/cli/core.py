import click
from chroma.segmentation.segmentation import Segmentation
from chroma.utils.utils import readColorYaml, PATH_IMAGES
import numpy
import cv2 as openCV

def SegImage(image, background, color):
    
    # tenta ler imagem e plano de fundo
    image = openCV.imread(image)
    background = openCV.imread(background)
    
    if image is None:
        click.echo("Nenhuma imagem foi passada como parâmetro!")
    
    else:
        height, width = image.shape[:2]
        
        # Configura plano de fundo
        if background is None:
            background = numpy.full((height, width, 3), (0, 0, 0)).astype("uint8")
        else:
            background = openCV.resize(
                background,
                (width, height),
                interpolation=openCV.INTER_CUBIC
            )
        
        # Leitura da cor 
        if color is not None and color.lower() in ["green", "red", "blue"]:
            color = readColorYaml(color.lower())
        else:
            color = readColorYaml("green")
            
        mask = Segmentation.chromaKey(
            image, 
            background, 
            color['min'], color['max']
        )
        
        openCV.imshow('Imagem', image)
        openCV.imshow('Imagem chroma', mask)
        openCV.imshow('Plano de fundo', background) # type: ignore
        
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