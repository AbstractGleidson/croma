import cv2 as openCV
from segmentation.exeptions import ImageNotFound

class GetColor:
    """
        Classe resposável por implemetar um forma de seleção de cor em Imagens.
    """
    
    _x_start = None
    _y_start = None 
    _x_end = None
    _y_end = None
    _drawing = None 
    _endDrawing = None 
    _rectangles = [] # Armazena as posições dos retângulos
    _points = [] # Armazena as posições dos pontos
    _react = False
    _REACT_PIXES = 4 # Quantidade minima de pixeis para ser cosiderado um retangulo
      
    @classmethod
    def _mouseEvents(cls, event, x, y, flags, param):    
        """
        Escuta os eventos de mouse da janela.
        Guardando a posições dos pontos e retângulos.
        Args:
            event (_type_): Tipo de evento
            x (_type_): Posição do mouse no eixo X
            y (_type_): Posição do mouse no eixo Y
        """
    
        if event == openCV.EVENT_LBUTTONDOWN: # Mouse foi pressionado para baixo
            cls._x_start, cls._y_start, cls._x_end, cls._y_end = x, y, x, y
            cls._drawing = True # Indica que comecou um desenho 
            cls._endDrawing = False # Inidca que comecou um novo desenho
            
        elif event == openCV.EVENT_MOUSEMOVE: # Mouse em movimento
            if cls._drawing == True:
                cls._x_end, cls._y_end = x, y # define o final do desenho
                    
        elif event == openCV.EVENT_LBUTTONUP: # Mouse terminou o movimento
            cls._drawing = False
            cls._endDrawing = True
            
            dx = abs(x - cls._x_start)
            dy = abs(y - cls._y_start)
            
            if dx >= cls._REACT_PIXES and dy >= cls._REACT_PIXES: # Pega retangulos
                cls._x_end, cls._y_end = x, y
                x1, x2 = sorted([cls._x_end, cls._x_start]) # type: ignore
                y1, y2 = sorted([cls._y_end, cls._y_start]) # type: ignore
                
                cls._rectangles.append(
                    {
                        "start": (x1, y1), 
                        "end": (x2, y2)
                    }
                )
                cls._react = True
                
            elif cls._x_start == x and cls._y_start == y: # Pega pontos 
                cls._points.append((cls._x_end, cls._y_end))
                cls._react = False
    
    @classmethod
    def _computer_points(cls, imageHsv):
        """
        Pega os pontos mínimos e máximos de cada região de interesse.
        Args:
            imageHsv (_type_): Imagem no espaço de core HSV

        Returns:
            (min, max): tuplas com valores mínimos e máximos de Hue, Saturatio e Value.
        """
        
        if len(cls._points) >= 1:
            h, s, v = [], [], []
                
            for point in cls._points:
                imageCut = imageHsv[point[1], point[0]] # Por padrão a os eixos da imagem são (Y, X) 
            
                h.append(imageCut[0])
                s.append(imageCut[1])
                v.append(imageCut[2])
                            
            minPoint = [min(h), min(s), min(v)]
            maxPoint = [max(h), max(s), max(v)]
        
            return minPoint, maxPoint

        return None, None
    
    @classmethod
    def _computer_rects(cls, imageHsv):
        """
        Pega os pontos mínimos e máximos de cada região de interesse.
        Args:
            imageHsv (_type_): Imagem no espaço de core HSV

        Returns:
            (min, max): tuplas com valores mínimos e máximos de Hue, Saturatio e Value.
        """
        
        if len(cls._rectangles) >= 1:
            
            maxRect = None
            minRect = None
                
            for rect in cls._rectangles:
                    
                if rect["start"] != rect["end"]: # Verifica se realmente é um retangulo
                    imageCut = imageHsv[rect["start"][1]:rect["end"][1], rect["start"][0]:rect["end"][0]]
                        
                    if imageCut.size == 0: # Nao coleta "ruidos"
                        continue
                    
                    if minRect is None:
                        maxRect = [imageCut[:,:,0].max(), imageCut[:,:,1].max(), imageCut[:,:,2].max()]
                        minRect = [imageCut[:,:,0].min(), imageCut[:,:,1].min(), imageCut[:,:,2].min()]
                        
                    else:
                        maxRect = [max(imageCut[:,:,0].max(), maxRect[0]), max(imageCut[:,:,1].max(), maxRect[1]), max(imageCut[:,:,2].max(), maxRect[2])] # type: ignore
                        minRect = [min(imageCut[:,:,0].min(), minRect[0]), min(imageCut[:,:,1].min(), minRect[1]), min(imageCut[:,:,2].min(), minRect[2])] 

            return minRect, maxRect
        
        return None, None
    
    @classmethod
    def _reset(cls):
        cls._drawing = False
        cls._endDrawing = False
        cls._react = False
        cls._rectangles = []
        cls._points = []

    @classmethod
    def getColor(cls, image) -> dict | None:
        """
        Realiza a leitura de cores de uma imagem.
        Args:
            image (_type_): Imagem no espaço de cores BGR

        Raises:
            ImageNotFound: Dispara exceção caso a imagem seja None

        Returns:
            _type_: Dicionário com os dados da leitura
        """
        
        if image is None:
            raise ImageNotFound("Imagem não encontrada ou inválida")
            
        cls._reset()
        cls._x_start, cls._y_start, cls._x_end, cls._y_end = 0, 0, 0, 0
        cls._mouse = (0,0)
            
        drawingImage = image.copy()
            
        # Cria uma janela 
        WINDOW_NAME = "s: salvar | q: sair | r: reverter"
        openCV.namedWindow(WINDOW_NAME)
        openCV.setMouseCallback(WINDOW_NAME, cls._mouseEvents)

        while True:
            i = drawingImage.copy()
                
            if not cls._drawing and not cls._endDrawing:
                openCV.imshow(WINDOW_NAME, drawingImage)
                
            elif cls._drawing and not cls._endDrawing:
                openCV.rectangle(i, (cls._x_start, cls._y_start), (cls._x_end, cls._y_end), (0, 0, 255), 2)
                openCV.imshow(WINDOW_NAME, i)
                    
            elif not cls._drawing and cls._endDrawing:
                if cls._react:
                    openCV.rectangle(drawingImage, (cls._x_start, cls._y_start), (cls._x_end, cls._y_end), (0, 0, 255), 2)
                else:
                    openCV.circle(drawingImage, (cls._x_end, cls._y_end), 4, (0, 0, 255), -1)
                    
                openCV.imshow(WINDOW_NAME, drawingImage)
                    
            key = openCV.waitKey(10) & 0xFF     
                
            if key == ord("s"): # cor selecionada
                cls._endDrawing = False 
                break    
                
            elif key == ord("r"): # reseta os desnhos da imagem
                drawingImage = image.copy()
                cls._reset()
                
            elif key == ord("q"):
                return None              
            
        openCV.destroyAllWindows()
        hsvImage = openCV.cvtColor(image, openCV.COLOR_BGR2HSV)
            
        minRect, maxRect = cls._computer_rects(hsvImage)
        minPoint, maxPoint = cls._computer_points(hsvImage)
            
        if maxPoint is not None and maxRect is not None:
            
            return {
                "min": [min(minRect[0], minPoint[0]), min(minRect[1], minPoint[1]), min(minRect[2], minPoint[2])], # type: ignore
                "max": [max(maxRect[0], maxPoint[0]), max(maxRect[1], maxPoint[1]), max(maxRect[2], maxPoint[2])]
            }
            
        elif maxPoint is not None:
            return {
                "min": minPoint,
                "max": maxPoint
            }
            
        elif maxRect is not None:    
            return {
                "min": minRect,
                "max": maxRect
            }
            
        return None