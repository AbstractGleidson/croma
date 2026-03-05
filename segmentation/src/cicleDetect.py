import cv2 as openCv
import numpy
from .utils import readColorYaml
 
def ligh_adjustment(img, gamma=1.9):
        """
            Realiza o ajuste do brilho de um frame deacordo com o gamma passado como parametro
        Args:
            frame (numpy array): imagem que se deseja ajustar o brilho.
            gamma (float, optional): valor de ajuste. gamma > 1: escurece o frame. gamma < 1 clareia o frame Defaults to 1.9.
        
        returns (numpy array): imagem com o brilho ajustado.
        """
        
        # tabela de correção (0–255), faz uma nova quantização das cores
        table = numpy.array([
            ((i / 255.0) ** gamma) * 255
            for i in range(256)
        ]).astype("uint8")

        # Aplica a nova quantização aos pixels do frame
        corrected = openCv.LUT(
            img, table
        )
        
        return corrected
    
def color_segmentation(img, low=(0, 120, 70), upper=(10, 255, 255)):
        """
            Aplica segmentacao por cor, utilizando os tons de cores passados como parametro.
            Por padrão segmenta a cor vemelha
        Args:
            frame (numpy array): Imagem que se deseja segmentar.
            low_color1 (tuple, optional): Nivel baixo da cor. Defaults to (0, 120, 70).
            upper_color1 (tuple, optional): Nivel altor da cor. Defaults to (10, 255, 255).
            low_color2 (tuple, optional): Nivel baixo da cor. Defaults to (170, 120, 70).
            upper_color2 (tuple, optional): Nivel alto da cor. Defaults to (180, 255, 255).
        
        return (numpy array): imagem com a cor segmentada.
        """
        
        # Converte a escala de por par HSV
        color_hsv = openCv.cvtColor(img, openCv.COLOR_BGR2HSV)
        
        # Cria mascara com os cores passadas por parâmetro
        mask = openCv.inRange(color_hsv, numpy.array(low), numpy.array(upper))
        
        # limpa o ruido das mascaras
        mask = openCv.morphologyEx(mask, openCv.MORPH_OPEN, numpy.ones((5, 5), numpy.uint8))
        
        # Preenche buracos internos na mascara
        kernel_close = numpy.ones((15, 15), numpy.uint8)
        mask_close = openCv.morphologyEx(mask, openCv.MORPH_CLOSE, kernel_close)
        
        # preparando preenchimento de regioes por meio do floodfil
        fil = mask_close.copy()
        h, w = fil.shape[:2]
        
        # Mascara de preenchimento
        flood_mask = numpy.zeros((h + 2, w + 2), numpy.uint8)
        openCv.floodFill(fil, flood_mask, (0, 0), 255)
        fil_inv = openCv.bitwise_not(fil)
        
        # aplica floodfil na mascara
        mask_fil = mask_close | fil_inv # type: ignore
        
        # Borra imagem 
        mask_fil = openCv.GaussianBlur(mask_fil, (9, 9), 2)
        
        return mask_fil

def voting(hough: numpy.ndarray, contour: numpy.ndarray, thers_xy: int = 20, thers_r: float = 0.3) -> numpy.ndarray:
    """
    Função de votação, para os dois métodos de detectção do círculo.

    Args:
        hough (tuple[int, int, int]): x, y e r da detecção da transformada de Hough
        contorno (tuple[int, int, int]): x, y e r  da detecção do método de contornos
        thers_xy (int, optional): Limiar de diferença para as coordenadas x e y. Por padrão 20.
        thers_r (float, optional): Limiar de diferença entre os raios. Por padrão 0.3.

    Returns:
        numpy.ndarray: Retorna uma média da coordenadas caso a discordância for menos que os limiares. Caso contrário retorna o método mais confiavel. 
    """
    
    # votação
    if abs(numpy.sum(hough[:2] - contour[:2])) < thers_xy:
        if abs(hough[2] - contour[2]) < (hough[2] * thers_r):
            return (hough + contour) // 2 

    # Se a discordancia for alta, retorna o metodo mais seguro
    return contour
    
    
def inInterval(v1: numpy.ndarray, v2: numpy.ndarray, thers: float) -> bool:
    """
    Verifica se a diferença de dois vetores é menor que que o limiar.

    Args:
        v1 (numpy.ndarray): Primeiro array. 
        v2 (numpy.ndarray): Segundo array.
        thers (int): limiar de diferença.

    Returns:
        bool: True se a diferença for menor que o limiar.
    """
    
    if abs(numpy.sum(v1 - v2)) > thers:
        return False
    
    return True

def color_dual_segmentation(img, gamma=2.3, low=(0, 120, 70), upper=(10, 255, 255)):
        """
            Aplica segmentacao por cor, utilizando os tons de cores passados como parametro.
            Por padrão segmenta a cor vemelha. Realiza segmentacao dupla, para diferentes niveis de brilho de acordo com o gamma passado.
        Args:
            img (_type_): _description_
            gamma (float, optional): _description_. Defaults to 2.3.
            low_color1 (tuple, optional): _description_. Defaults to (0, 120, 70).
            upper_color1 (tuple, optional): _description_. Defaults to (10, 255, 255).
            low_color2 (tuple, optional): _description_. Defaults to (170, 120, 70).
            upper_color2 (tuple, optional): _description_. Defaults to (180, 255, 255).

        Returns:
            _type_: _description_
        """
        
        frame = openCv.resize(img, (640, 640))
        
        # Aplica filtro para escurecer a imagem
        dark = ligh_adjustment(frame, 2.5)

        mask_red_dark = color_segmentation(dark, low, upper) # Aplica segmentação por cor na mascara escurecida
        mask_red_normal = color_segmentation(frame, low, upper) # Aplica segmentação por cor na mascara normal
        
        # Mescla as duas mascaras
        mask_final = openCv.bitwise_or(mask_red_dark, mask_red_normal)

        return mask_final
    
def houghCircleDetect(img, dp=1.3, minDist=50, canny=100, accumulation=40, minRadius=5, maxRadius=300):
        """
            Transformada de hough mais completa ultilizando alguns filtros para aproximar ilipses de ciculos
        """
        
        edges = openCv.Canny(
            img,
            50, 
            150 
            ) # Aplica filtro de segmentacao de bordas
        
        # Cria uma mascara para formas elipticas
        kernel = openCv.getStructuringElement(openCv.MORPH_ELLIPSE, (7,7))
        
        # Aplica mascara eliptica para detectar bordas elipticas
        edges_ellipse = openCv.morphologyEx(edges, openCv.MORPH_CLOSE, kernel)

        circles = openCv.HoughCircles(
            edges_ellipse,
            openCv.HOUGH_GRADIENT,
            dp=dp,
            minDist=minDist,
            param1=canny,
            param2=accumulation,
            minRadius=minDist,
            maxRadius=maxRadius
        )

        # Reconhece o maior ciculo
        if circles is not None:
            circles = numpy.uint16(numpy.around(circles[0]))
            circles = sorted(circles, key=lambda c: c[2], reverse=True) # type:ignore
            return tuple(circles[0]), edges_ellipse # retorna os dados do circulo e segmentação

        return None, edges_ellipse

def circleCannyDetect(img, MINRADIUS=3, MINAREA=300, canny=(70, 150)):
        """Deteccao de circulos via contorno e coeficiente de circularidade, por meio das bordas"""
        
        # Aplica canny para reconhecimento de bordas
        edges = openCv.Canny(img, canny[0], canny[1])
        contornos, _ = openCv.findContours(edges, openCv.RETR_EXTERNAL, openCv.CHAIN_APPROX_SIMPLE)

        # Ciculo com maior cicularidade detectado
        bestCircle = None
        bestScore = 999

        for cnt in contornos:
            area = openCv.contourArea(cnt)
            if area < MINAREA: # Descarta circulos muito pequenos
                continue

            # Detecta ciculos
            (x, y), r = openCv.minEnclosingCircle(cnt)
            r = int(r)

            if r <= MINRADIUS: # Descarta raios muito pequenos
                continue

            area_circ = numpy.pi * (r ** 2)
            erro = abs(area - area_circ) / area_circ

            # circularidade aceitável
            if erro < bestScore and erro < 0.35:
                bestScore = erro
                bestCircle = (int(x), int(y), r)

        return bestCircle

def smoothDetect(color):
    HEIGHT = 640
    WIDTH = 640
    
    
    camera = openCv.VideoCapture(0)
    camera.set(openCv.CAP_PROP_FRAME_HEIGHT, HEIGHT) # definindo altura do frame
    camera.set(openCv.CAP_PROP_FRAME_WIDTH, WIDTH) # definindo largura
    
    circleHistory = None  # média acumulada
    cont = 0
    LIMIAR = 20  # tolerância para considerar mesma bola
    NO_DET_LIMIT = 20  # número máximo de frames sem detecção
    noDetCounter = 0
    
    col = readColorYaml(color)
    
    while True:
        available, frame = camera.read()
        
        if available:

            mask = color_dual_segmentation(frame, gamma=1.9, low=col["min"], upper=col["max"])
            hough, _ = houghCircleDetect(mask)
            contour = circleCannyDetect(mask)
            
            hough = (numpy.array(hough) if hough is not None else None)
            contour = (numpy.array(contour) if contour is not None else None) 

                # escolhe a melhor detecção entre hough e canny
            if hough is not None and contour is not None:
                det = voting(
                    hough, 
                    contour
                )    
            elif hough is not None:
                det = hough
            else:
                det = contour

            if det is not None:
                noDetCounter = 0  # reset contador de frames sem detecção

                if circleHistory is None or not inInterval(det, circleHistory, LIMIAR):
                    circleHistory = det.copy()  # converte tupla para lista
                else:
                    # acumula valores
                    circleHistory = (det + circleHistory) // 2 # Talves dê problema, mas vamo na fé
                    
            else:
                noDetCounter += 1
                # se muitos frames sem detecção, zera histórico
                if noDetCounter >= NO_DET_LIMIT:
                    circleHistory = None

            txt = "Nenhum circulo detectado"
            if circleHistory is not None:
                # calcula média real
                x, y, r = circleHistory
                
                openCv.circle(frame, (x, y), r, (0, 255, 0), 3)
                openCv.circle(frame, (x, y), 3, (0, 255, 255), -1)
                txt = f"X={x}  Y={y}  R={r}"

            openCv.putText(frame, txt, (10, 35), openCv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            openCv.imshow("Detecção Final", frame)
            openCv.imshow("Mascara", mask)

            if openCv.waitKey(1) & 0xFF == ord('q'):
                break

    openCv.destroyAllWindows()
    
