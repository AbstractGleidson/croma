import cv2 as openCV

class GetColor:
    # Variaveis para a leitura usando retangulos
    _x_start = None
    _y_start = None 
    _x_end = None
    _y_end = None
    _drawing = None 
    _endDrawing = None 
    _rectangles = [] # local onde vao ser as posicoes dos retangulos
    _points = [] # pontos para getColorByPoint
    _react = False
    
    # Escuta os eventos para a funcao getColorByRect
    @classmethod
    def _mouseEvents(cls, event, x, y, flags, param):    
    
        if event == openCV.EVENT_LBUTTONDOWN: # Mouse foi pressionado para baixo
            cls._x_start, cls._y_start, cls._x_end, cls._y_end = x, y, x, y
            cls._drawing = True # Indica que comecou um desenho 
            cls._endDrawing = False # Inidca que comecou um novo desenho
            
        elif event == openCV.EVENT_MOUSEMOVE: # Mouse em movimento
            if cls._drawing == True:
                cls._x_end, cls._y_end = x, y # define o final do desenho
                    
        elif event == openCV.EVENT_LBUTTONUP: # Mouse terminou o movimento
            cls._x_end, cls._y_end = x, y
            cls._drawing = False
            cls._endDrawing = True
            
            if cls._x_start != cls._x_end and cls._y_start != cls._y_end: # Pega retangulos
                
                if cls._x_start > cls._x_end:
                    temp = cls._x_start
                    cls._x_start = cls._x_end
                    cls._x_end = temp
                
                if cls._y_start > cls._y_end:
                    temp = cls._y_start
                    cls._y_start = cls._y_end
                    cls._y_end = temp
                
                cls._rectangles.append({"start": (cls._x_start, cls._y_start), "end": (cls._x_end, cls._y_end)})
                cls._react = True
                
            elif cls._x_start == cls._x_end and cls._y_start == cls._y_end: # Pega pontos 
                cls._points.append((cls._x_end, cls._y_end))
                cls._react = False
    
    @classmethod
    def _clearPoints(cls, imageHsv):
        
        if len(cls._points) >= 1:
            h, s, v = [], [], []
                
            for point in cls._points:
                imageCut = imageHsv[point[1], point[0]] # Por algum motico é invertido 
            
                h.append(imageCut[0])
                s.append(imageCut[1])
                v.append(imageCut[2])
                            
            minPoint = [min(h), min(s), min(v)]
            maxPoint = [max(h), max(s), max(v)]
        
            return maxPoint, minPoint

        return None, None
    
    @classmethod
    def _clearRects(cls, imageHsv):
        
        if len(cls._rectangles) >= 1:
                
            for i, rect in enumerate(cls._rectangles):
                    
                if rect["start"] != rect["end"]: # Verifica se realmente é um retangulo
                    imageCut = imageHsv[rect["start"][1]:rect["end"][1], rect["start"][0]:rect["end"][0]]
                        
                    if i == 0:
                        maxRect = [imageCut[:,:,0].max(), imageCut[:,:,1].max(), imageCut[:,:,2].max()]
                        minRect = [imageCut[:,:,0].min(), imageCut[:,:,1].min(), imageCut[:,:,2].min()]
                        
                    else:
                        maxRect = [max(imageCut[:,:,0].max(), maxRect[0]), max(imageCut[:,:,1].max(), maxRect[1]), max(imageCut[:,:,2].max(), maxRect[2])]
                        minRect = [min(imageCut[:,:,0].min(), minRect[0]), min(imageCut[:,:,1].min(), minRect[1]), min(imageCut[:,:,2].min(), minRect[2])] 

            return maxRect, minRect
        
        return None, None
        

    @classmethod
    def getColor(cls, image):
        
        if image is not None:
            cls._x_start, cls._y_start, cls._x_end, cls._y_end = 0, 0, 0, 0
            cls._drawing = False
            cls._endDrawing = False
            cls._react = False
            cls._rectangles = []
            cls._points = []
            cls._mouse = (0,0)
            
            drawingImage = image.copy()
            
            # Cria uma janle
            openCV.namedWindow("Selecione a cor do plano de fundo")
            openCV.setMouseCallback("Selecione a cor do plano de fundo", cls._mouseEvents)

            while True:
                i = drawingImage.copy()
                
                if not cls._drawing and not cls._endDrawing:
                    openCV.imshow("Selecione a cor do plano de fundo", drawingImage)
                    
                elif cls._drawing and not cls._endDrawing:
                    openCV.rectangle(i, (cls._x_start, cls._y_start), (cls._x_end, cls._y_end), (0, 0, 255), 2)
                    openCV.imshow("Selecione a cor do plano de fundo", i)
                    
                elif not cls._drawing and cls._endDrawing:
                    if cls._react:
                        openCV.rectangle(drawingImage, (cls._x_start, cls._y_start), (cls._x_end, cls._y_end), (0, 0, 255), 2)
                    else:
                        openCV.circle(drawingImage, (cls._x_end, cls._y_end), 4, (0, 0, 255), -1)
                    
                    openCV.imshow("Selecione a cor do plano de fundo", drawingImage)
                    
                key = openCV.waitKey(1) & 0xFF     
                
                if key == ord("s"): # cor selecionada
                    cls._endDrawing = False 
                    break    
                
                elif key == ord("r"): # reseta os desnhos da imagem
                    drawingImage = image.copy()
                    cls._rectangles = []
                    cls._points = []
                    cls._react = False
                    cls._drawing = False
                    cls._endDrawing = False
                
                elif key == ord("q"):
                    break                          
            
            openCV.destroyAllWindows()
            hsvImage = openCV.cvtColor(image, openCV.COLOR_BGR2HSV)
            
            maxRect, minRect = cls._clearRects(hsvImage)
            maxPoint, minPoint = cls._clearPoints(hsvImage)
            
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