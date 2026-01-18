import cv2 as openCV
import numpy
from src.utils import readColorYaml, PATH_IMAGES, hsvToOpenCV
from src.segmentation.byColor import mergeImages

if __name__ == "__main__":
    
    
    # Inicio
    
    # Baixo
    print(hsvToOpenCV(0, 100, 100))
    print(hsvToOpenCV(0, 50, 50))
    
    # Alto
    print(hsvToOpenCV(12, 100, 100))
    print(hsvToOpenCV(12, 50, 50))
    
    # Fim
    
    # Alto
    print(hsvToOpenCV(350, 100, 100))
    print(hsvToOpenCV(350, 50, 50))
    
    # Baixo
    print(hsvToOpenCV(360, 100, 100))
    print(hsvToOpenCV(360, 50, 50))
    
    
    # Inicio 
    
    # # claro
    v1 = background = numpy.array((0, 255, 255)).astype("uint8")
    
    # # escuro 
    v2 = background = numpy.array((0, 127, 127)).astype("uint8")
    
    # claro
    v1 = background = numpy.array((10, 255, 255)).astype("uint8")
    
    # # escuro 
    v2 = background = numpy.array((2, 127, 127)).astype("uint8")
    
    v1 = background = numpy.array((175, 255, 255)).astype("uint8")
    
    # escuro 
    v2 = background = numpy.array((175, 127, 127)).astype("uint8")
    
    v3 = background = numpy.array((180, 255, 255)).astype("uint8")
    
    # escuro 
    v4 = background = numpy.array((180, 127, 127)).astype("uint8")
    
    
    path1 = str(PATH_IMAGES / "3.jpeg")
    path2 = str(PATH_IMAGES / "4.jpg")
    #save = str(PATH_IMAGES / "3_blue.jpeg")
    
    image = openCV.imread(path1)
    background = openCV.imread(path2)
    
    if image is not None and background is not None:
        
        height, width = image.shape[:2]
        
        background = openCV.resize(
            background,
            (width, height),
            interpolation=openCV.INTER_CUBIC
        )
        
        color = readColorYaml("red")
        
        #background = numpy.full((height, width, 3), (255, 12, 0)).astype("uint8")
        
        mask = mergeImages(image, background, v2, v3)
        
        blur = openCV.GaussianBlur(
            mask,
            (9, 9),
            3
        )
        
        edges = openCV.Laplacian(blur, openCV.CV_8U)
        
        mask = openCV.subtract(mask, edges)
        
        openCV.imshow("Image", image) 
        openCV.imshow("Fundo", background)
        openCV.imshow("Mask", mask)
        openCV.imshow("Bordas", edges)
        
        #openCV.imwrite(save, mask)
        
        key = openCV.waitKey(0) & 0xFF
        
        if key == ord('q'):
            openCV.destroyAllWindows()
    
    # webcam = openCV.VideoCapture(0)
    # webcam.set(openCV.CAP_PROP_FRAME_HEIGHT, 640)
    # webcam.set(openCV.CAP_PROP_FRAME_WIDTH, 640)
    
    # if webcam is not None:
        
    #     background = image = openCV.imread(str(PATH_IMAGES / "4.jpg"))
        
    #     while(True):
    #         isAvai, frame = webcam.read()
            
    #         if isAvai:
                
    #             height, width = frame.shape[:2]
            
    #             background = openCV.resize(background, (width, height), None, interpolation=openCV.INTER_CUBIC) # type: ignore
    #             color = readColorYaml("blue")
                
    #             #background = numpy.full((height, width, 3), (0, 255, 255)).astype("uint8")
                
    #             mask = mergeImages(frame, background, color["min"], color["max"])
                
    #             # blur = openCV.GaussianBlur(
    #             #     mask,
    #             #     (9, 9),
    #             #     3
    #             # )
                
    #             # edges = openCV.Laplacian(blur, openCV.CV_8U)
                
    #             # mask = openCV.subtract(mask, edges)
                
    #             openCV.imshow("Image", frame) 
    #             #openCV.imshow("Fundo", background)
    #             openCV.imshow("Mask", mask)
    #             #openCV.imshow("Bordas", edges)
                
    #             key = openCV.waitKey(1) & 0xFF
            
    #             if key == ord("q"):
    #                 break
        
    #     webcam.release()
    #     openCV.destroyAllWindows()