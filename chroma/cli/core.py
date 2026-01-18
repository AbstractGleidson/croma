import click
from chroma.segmentation.segmentation import Segmentation
from chroma.utils.utils import readColorYaml, PATH_IMAGES
import numpy
import cv2 as openCV

def SegImage(image, background, color):
    
    image = openCV.imread(image)
    background = openCV.imread(background)
    
    if image is None:
        click.echo("Nenhuma imagem foi passada como parâmetro!")
    
    else:
        height, width = image.shape[:2]
        
        if background is None:
            background = numpy.full((height, width, 3), (0, 0, 0)).astype("uint8")
        else:
            background = openCV.resize(
                background,
                (width, height),
                interpolation=openCV.INTER_CUBIC
            )
        
        if color in ["green", "red", "blue"]:
            color = readColorYaml(color)

        else:
            color = readColorYaml("green")
        
        
        openCV.imshow('Imagem', image)
        openCV.imshow('Plano de fundo', background) # type: ignore
        
        key = openCV.waitKey(0) & 0xFF
        
        if key == ord('q'):
            openCV.destroyAllWindows()

def SegWebCam():
    click.echo("Segmentacao de webcam")