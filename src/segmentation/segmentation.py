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
        mask = openCV.bitwise_not(mask) # inverte a mascara
        
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
        mask = Segmentation.byColor(image, min, max)
        
        # complemento da mascara
        mask_not = openCV.bitwise_not(mask)
        
        # normaliza as mascaras para valores 0 e 1 
        mask = numpy.array(mask >= 1).astype("uint8")
        mask_not = numpy.array(mask_not >= 1).astype("uint8")
        
        mask = Segmentation.maskMulti(image, mask)
        mask_not = Segmentation.maskMulti(background, mask_not) 
        
        result = mask | mask_not # type: ignore
        
        return result   