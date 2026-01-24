from segmentation.exeptions.colorNotFound import ColorNotFound
from segmentation.exeptions.colorNotSelected import ColorNotSelected
from segmentation.exeptions.unableOpenWebcam import UnableOpenWebcam
from segmentation.src.getColor import GetColor
from segmentation.src.utils import readColorYaml
from segmentation.src.segmentation import Segmentation
import cv2 as openCV
import numpy 

def chromaWebcam(webcam, background, color, height, width):
    
    webcam = openCV.VideoCapture(webcam)
    
    if webcam is None:
        raise UnableOpenWebcam("Não foi possível abrir a webcam.")
        
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