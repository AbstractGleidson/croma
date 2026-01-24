import cv2 as openCV
import numpy

class Segmentation:
    
    @classmethod
    def byColor(cls, image, min, max):
        min = numpy.array(min)
        max = numpy.array(max)
        
        # Filtro de baixa frequencia, para suavizar as bordas
        blur = openCV.medianBlur(
            image,
            7
        ) # type: ignore
        
        hsv = openCV.cvtColor(blur, openCV.COLOR_BGR2HSV) # Converte para o espaco HSV
        
        mask = openCV.inRange(hsv, min, max) # cria mascara 
        
        return mask
    
    @classmethod
    def maskMulti(cls, image, mask):
        
        c1, c2, c3 = openCV.split(image)
        
        # muiltiplica cada canal de uma imagem tridimensional por uma mascara unidimensional qualquer
        c1 *= mask
        c2 *= mask
        c3 *= mask
        
        result = openCV.merge((c1, c2, c3))
        
        return result

    @classmethod
    def chromaKey(cls, image, background, min, max):
        
        # cria mascara 
        mask_background = Segmentation.byColor(image, min, max)
        
        mask_front = openCV.bitwise_not(mask_background)
        
        # normaliza as mascaras para valores 0 e 1 
        mask_front = numpy.array(mask_front >= 1).astype("uint8")
        mask_background = numpy.array(mask_background >= 1).astype("uint8")
        
        mask = Segmentation.maskMulti(image, mask_front)
        mask_not = Segmentation.maskMulti(background, mask_background) 
        
        result = mask | mask_not # type: ignore
        
        return result   