from segmentation.exeptions import ColorNotFound, UnableOpenWebcam, ImageNotFound
from segmentation.src.getColor import GetColor
from segmentation.src.utils import readColorYaml
from segmentation.src.segmentation import Segmentation
import cv2 as openCV
import numpy 

def chromaWebcam(webcam: int, background:str, color:str, height:int, width:int):
    
    cam = openCV.VideoCapture(webcam)
    
    if cam is None:
        raise UnableOpenWebcam("Não foi possível abrir a webcam.")
        
    else:
        
        # Configura tamanho da janela
        cam.set(openCV.CAP_PROP_FRAME_HEIGHT, height)
        cam.set(openCV.CAP_PROP_FRAME_WIDTH, width)
        
        if background is None:
            back = numpy.full((width, height, 3), (0, 0, 0)).astype("uint8")
            
        else:
            back = openCV.imread(background)
            
            if back is None:
                raise ImageNotFound("Imagem para o plano de fundo não foi encotrada")
            
            back = openCV.resize(
                back,
                (width, height),
                interpolation=openCV.INTER_CUBIC
            )
        
        if color is None:
            col = readColorYaml("green") 
        
        elif color.lower() in ["green", "red", "blue"]:
            col = readColorYaml(color.lower())
            
        else:
            raise ColorNotFound(f"A cor {color} não existe.")  
            
        while(True):
            
            isAvaliable, frame = cam.read()
            
            if isAvaliable:
                
                mask = Segmentation.chromaKey(
                    frame, 
                    back, 
                    col['min'], 
                    col['max']
                )
                
                #openCV.imshow("Frame", frame)
                openCV.imshow("Chroma", mask)
                #openCV.imshow("Plano de fundo", background)
                
                key = openCV.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
        
        cam.release()
        openCV.destroyAllWindows()